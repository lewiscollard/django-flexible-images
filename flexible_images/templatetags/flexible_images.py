#!/usr/bin/python
from django import template

from ..util import get_image_sizes, get_template_context

register = template.Library()


@register.inclusion_tag("flexible-images/flexible-image.html")
def flexible_image(image, *args, **kwargs):
    """The flexible_image template tag. This is a thin wrapper around
    get_template_context in util.py - see that file or the documentation for
    parameters. """
    return get_template_context(image, *args, **kwargs)


@register.assignment_tag
def flexible_image_list(image):
    """Given an ImageField `image`, returns a list of images sizes in this
    form:

    [
        {
            "url": "http://example.com/xxx.jpg",
            "width": 1440,
            "height": 960
        },
        [...]
    ]

    This permits you to use your own preferred HTML implementation.
    """
    return get_image_sizes(image)
