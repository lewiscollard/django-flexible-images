#!/usr/bin/python
from django import template
from ..utils import aspect_ratio_percent

register = template.Library()


@register.inclusion_tag("flexible-images/flexible-image.html")
def flexible_image(src, container="div", classes="", alt=""):
    rv = {
        "image": src,
        "container": container,
        "classes": classes,
        "aspect_padding_bottom": aspect_ratio_percent(src),
        "alt": alt,
    }
    return rv


@register.inclusion_tag("flexible-images/images-loading.html")
def flexible_image_js(selector=".flexible-image"):
    ctx = {
        "selector": selector,
    }
    return ctx
