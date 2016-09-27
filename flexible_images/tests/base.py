import os.path

from django import forms
from django.core.files.base import ContentFile
from django.test import TestCase

from ..models import FlexibleImageTestImage


class ImageTestForm(forms.Form):
    image = forms.ImageField()


class FlexibleImageTestCase(TestCase):
    def setUp(self):
        super(TestCase, self).setUp()
        image_path = os.path.join(
            os.path.dirname(__file__),
            "../static/responsive-test-image-1.jpg",
        )

        fd = open(image_path, "rb")
        self.image_model = FlexibleImageTestImage(title="Test image 1")
        self.image_model.image.save(
            os.path.basename(fd.name),
            ContentFile(fd.read()),
        )
        self.image = self.image_model.image
        # Sample image sizes.
        self.settings_sizes = [1024, 800, 400]
