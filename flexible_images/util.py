#!/usr/bin/python
import json

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


class FlexibleImageError(ImproperlyConfigured):
    pass


def possible_engines():
    # Mostly a helper to aid with testing.
    return ["sorl", None]


def settings_sizes():
    sizes = getattr(settings, "FLEXIBLE_IMAGE_SIZES", None)
    if sizes is None:
        sizes = [
            480,
            768,
            1024,
            1280,
            1440,
        ]
    return sizes


def aspect_ratio(image):
    return float(image.height) / float(image.width)


def aspect_ratio_percent(image):
    return aspect_ratio(image) * 100


def get_thumbnail_engine():
    engine = getattr(settings, "FLEXIBLE_IMAGE_ENGINE", "sorl")

    if not engine in possible_engines():
        raise FlexibleImageError("FLEXIBLE_IMAGE_ENGINE must be one of: 'sorl', None")

    return engine


def get_thumbnail_shim(image, width):
    # This is in its own function because it'll make it easy to add support
    # for other thumbnailers in future. (easy_thumbnails should be easy,
    # and I had it written, but it refuses to work properly with anything that
    # is not an ImageField, i.e. in our test view in views.py.)
    engine = get_thumbnail_engine()

    if engine == "sorl":
        # Let's do a sorl!
        from sorl.thumbnail import get_thumbnail
        im = get_thumbnail(image, '{}'.format(width), upscale=False)
        return im

    # No thumbnailer. :(
    return image


def get_image_sizes(image):
    """Given an ImageField `image`, returns a list of images sizes in this
    form:

    [
        {
            "url": "http://example.com/xxx.jpg",
            "width": 1440,
            "height": 960
        },
        [...]
    ]"""

    # It is possible to have the same width appear more than once, if
    # THUMBNAIL_UPSCALE is set to False and the image's width is less than the
    # largest value in FLEXIBLE_IMAGE_SIZES. So keep track of widths and
    # don't output more than one image with the same width (which would result
    # in an invalid `srcset` attribute).
    sizes = []
    seen_widths = []

    for size in settings_sizes():
        img = get_thumbnail_shim(image, size)

        if img.width in seen_widths:
            continue

        seen_widths.append(img.width)

        sizes.append({
            "url": img.url,
            "width": img.width,
            "height": img.height,
        })
    return sizes


def get_template_context(src, container="div", classes="", inner_classes="", alt="", background_image=False, no_css=False, aria_hidden=False):
    """Returns a template context for a flexible image template
    tag implementation."""
    context = {
        "container": container,
        "classes": classes,
        "aspect_padding_bottom": aspect_ratio_percent(src),
        "alt": alt,
        "background_image": background_image,
        "no_css": no_css,
        "inner_classes": inner_classes,
        "aria_hidden": aria_hidden,
    }

    # We can't do any of the srcset (or JS switching fallback) if we don't
    # have a thumbnail library installed.
    if not get_thumbnail_engine():
        context["image"] = src
        return context

    sizes = get_image_sizes(src)
    context["image_sizes"] = sizes

    # Set the first image in the list as the one to be rendered initially
    # (pre-JS-fallback). `if sizes` might not be a necessary check...
    context["image"] = sizes[0]

    context["image_sizes_json"] = json.dumps(sizes)
    srcset_items = ["{} {}w".format(size["url"], size["width"]) for size in sizes]

    context["image_sizes_srcset"] = ", ".join(srcset_items)
    return context
