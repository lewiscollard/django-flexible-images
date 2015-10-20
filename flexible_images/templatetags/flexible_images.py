#!/usr/bin/python
import json

from django import template
from ..util import aspect_ratio_percent, HAS_THUMBNAILER, get_thumbnail_shim
from django.conf import settings
register = template.Library()


try:
    FLEXIBLE_IMAGE_SIZES = settings.FLEXIBLE_IMAGE_SIZES
except:
    # Image sizes. These MUST be in size order for this to function properly.
    FLEXIBLE_IMAGE_SIZES = [
        480,
        768,
        1024,
        1280,
        1440,
    ]


@register.inclusion_tag("flexible-images/flexible-image.html", takes_context=True)
def flexible_image(context, src, container="div", classes="", alt=""):
    rv = {
        "container": container,
        "classes": classes,
        "aspect_padding_bottom": aspect_ratio_percent(src),
        "alt": alt,
    }

    # We can't do any of the JS stuff if we don't have a thumbnail
    # library installed.
    if not HAS_THUMBNAILER:
        rv["image"] = src
        return rv
    # Serve up the first image (which should be the smallest), then swap it
    # out with a larger version in JS if their device merits it.
    first = True
    sizes = []
    for size in FLEXIBLE_IMAGE_SIZES:
        width = size['width'] if 'width' in size else size
        image = get_thumbnail_shim(src, width)
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


@register.inclusion_tag("flexible-images/images-loading.html")
def flexible_image_js(selector=".flexible-image"):
    ctx = {
        "selector": selector,
    }
    return ctx
