from django.template.loader import render_to_string
from django_jinja import library

from ..util import get_image_sizes, get_template_context


@library.global_function
def flexible_image(image, *args, **kwargs):
    context = get_template_context(image, *args, **kwargs)
    html = render_to_string("flexible-images/flexible-image.html", context)
    return html


@library.filter
def flexible_image_list(image):
    return get_image_sizes(image)
