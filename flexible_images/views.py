#!/usr/bin/python
from django.views.generic import TemplateView
from django.core.files.images import ImageFile

import os.path


class FlexibleImageTestView(TemplateView):
    """Ugly test view for responsive images."""
    template_name = "flexible-images/flexible-image-test.html"

    def get_context_data(self, **kwargs):
        context = super(FlexibleImageTestView, self).get_context_data(**kwargs)
        filename = os.path.join(os.path.dirname(__file__), "static/responsive-test-image.jpg")
        fd = open(filename)
        image_file = ImageFile(fd)
        # XXX Change this for your environment.
        image_file.url = "/static/responsive-test-image.jpg"
        context = {
            "image": image_file,
        }
        return context
