#!/usr/bin/python
import json

from django import template
from ..util import aspect_ratio_percent, HAS_THUMBNAILER, get_thumbnail_shim
from django.conf import settings
register = template.Library()


try:
    FLEXIBLE_IMAGE_SIZES = settings.FLEXIBLE_IMAGE_SIZES
except:
    # Image sizes. These should be in size order, smallest first.
    FLEXIBLE_IMAGE_SIZES = [
        480,
        768,
        1024,
        1280,
        1440,
    ]


@register.inclusion_tag("flexible-images/flexible-image.html", takes_context=True)
def flexible_image(context, src, container="div", classes="", alt="", background_image=False):
    rv = {
        "container": container,
        "classes": classes,
        "aspect_padding_bottom": aspect_ratio_percent(src),
        "alt": alt,
        "background_image": background_image,
    }

    # We can't do any of the srcset (or JS switching fallback) if we don't
    # have a thumbnail library installed.
    if not HAS_THUMBNAILER:
        rv["image"] = src
        return rv
    # For browsers that support srcset: Give them all the sizes and let the
    # browser decide what to use.
    # For ones that do not: Serve up the first image (which should be the
    # smallest), then swap it out with a larger version in JS if their device
    # merits it.
    first = True
    sizes = []

    # It is possible to have the same width appear more than once, if
    # THUMBNAIL_UPSCALE is set to False and the image's width is less than the
    # largest value in FLEXIBLE_IMAGE_SIZES. So keep track of widths and
    # don't output more than one image with the same width (which would result
    # in an invalid `srcset` attribute).
    seen_widths = []

    for size in FLEXIBLE_IMAGE_SIZES:
        image = get_thumbnail_shim(src, size)

        if image.width in seen_widths:
            continue
        seen_widths.append(image.width)

        sizes.append({
            "url": image.url,
            "width": image.width,
            "height": image.height,
        })
        if first:
            rv["image"] = image
            first = False
    rv["image_sizes"] = sizes
    rv["image_sizes_json"] = json.dumps(sizes)
    return rv
