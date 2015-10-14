#!/usr/bin/python
from uuid import uuid4
import json

from django import template
from ..util import aspect_ratio_percent, HAS_THUMBNAILER, get_thumbnail_shim
from django.conf import settings
register = template.Library()


try:
    FLEXIBLE_IMAGES_SIZES = settings.FLEXIBLE_IMAGES_SIZES
except:
    # Image sizes. These MUST be in size order for this to function properly.
    FLEXIBLE_IMAGES_SIZES = [
        {
            "width": 480,
        },
        {
            "width": 768,
        },
        {
            "width": 1024,
        },
        {
            "width": 1280,
        },
        {
            "width": 1440,
        },
    ]


@register.inclusion_tag("flexible-images/flexible-image.html", takes_context=True)
def flexible_image(context, src, container="div", classes="", alt=""):
    request = context["request"]

    try:
        use_js = settings.FLEXIBLE_IMAGES_USE_JS
    except:
        # Default to True.
        use_js = True
    try:
        use_cookies = settings.FLEXIBLE_IMAGES_USE_COOKIES
    except:
        # Default to True. Is this evil?
        use_cookies = True

    rv = {
        "container": container,
        "classes": classes,
        "aspect_padding_bottom": aspect_ratio_percent(src),
        "alt": alt,
        "use_js": use_js,
        "use_cookies": use_cookies,
        "uuid": "id_{}".format(uuid4().hex.replace("-", "")),
    }

    serve_now = False

    # Don't do any image swapping out and just serve the full-resolution
    # image if FLEXIBLE_IMAGES_USE_JS is not set.
    if not use_js:
        serve_now = True

    # And we can't do any of the JS cookie stuff if we don't have a thumbnail
    # library installed.
    elif not HAS_THUMBNAILER:
        serve_now = True
        rv["use_js"] = False

    if serve_now == True:
        rv["image"] = src
        return rv

    # If they have a width cookie set, then we can skip any thumbnailing
    # stuff.
    if use_cookies and request.COOKIES.get("flexible-images"):
        kvp = {}

        # Cookie is in the format key_value/key_value. We only use the
        # 'max-size' key, but
        for part in request.COOKIES.get("flexible-images").split("/"):
            bits = part.split("_", 1)
            kvp[bits[0]] = bits[1]

        if "max-size" in kvp:
            width = int(kvp["max-size"])
            print "XXXXXX", width
            width_match = FLEXIBLE_IMAGES_SIZES[-1]["width"]
            for size in FLEXIBLE_IMAGES_SIZES:
                if size["width"] >= width:
                    width_match = size["width"]
                    break
            rv["image"] = get_thumbnail_shim(width_match, src)
            return rv

    # In which we don't know the width of their device. So we'll serve up
    # the first image (which should be the smallest), then swap it out with
    # a larger version in JS if their device merits it.
    first = True
    sizes = []
    for size in FLEXIBLE_IMAGES_SIZES:
        image = get_thumbnail_shim(src, size["width"])
        sizes.append({
            "url": image.url,
            "width": image.width,
            "height": image.height,
        })
        if first:
            rv["image"] = image
            first = False
    rv["image_sizes"] = json.dumps(sizes)
    return rv


@register.inclusion_tag("flexible-images/images-loading.html")
def flexible_image_js(selector=".flexible-image"):
    ctx = {
        "selector": selector,
    }
    return ctx
