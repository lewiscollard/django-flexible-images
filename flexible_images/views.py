#!/usr/bin/python
import os.path

from django.views.generic import TemplateView
from django.core.files.images import ImageFile
from django.conf import settings


class FlexibleImageTestView(TemplateView):
    """Ugly test view for responsive images."""
    template_name = "flexible-images/flexible-image-test.html"

    def get_context_data(self, **kwargs):
        context = super(FlexibleImageTestView, self).get_context_data(**kwargs)
        filename1 = os.path.join(settings.MEDIA_ROOT, "responsive-test-image-1.jpg")
        fd1 = open(filename1)
        image_file1 = ImageFile(fd1)

        filename2 = os.path.join(settings.MEDIA_ROOT, "responsive-test-image-2.jpg")
        fd2 = open(filename2)
        image_file2 = ImageFile(fd2)
        # XXX Change this for your environment.
        image_file1.url = "/static/responsive-test-image-1.jpg"
        image_file2.url = "/static/responsive-test-image-2.jpg"
        context = {
            "image_1": image_file1,
            "image_2": image_file2,
        }
        return context
