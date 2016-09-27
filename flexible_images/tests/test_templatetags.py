from xml.etree.ElementTree import fromstring as et_fromstring

from ..templatetags.django_jinja_flexible_images \
    import flexible_image as django_jinja_flexible_image, \
    flexible_image_list as django_jinja_flexible_image_list

from ..templatetags.flexible_images import flexible_image, flexible_image_list
from ..util import possible_engines
from .base import FlexibleImageTestCase

from django.template.loader import render_to_string


class TemplateTagsTestCase(FlexibleImageTestCase):
    def test_templatetags_flexible_image(self):
        # Test it with every one of our parameters.
        test_parameters = [
            (None, None),
            ("container", "p"),
            ("no_css", True),
            ("alt", "Testing!!"),
            ("classes", "fake-class"),
            ("inner_classes", "fake-inner-class"),
            ("aria_hidden", True),
            ("background_image", True),
        ]

        # Check that with every possible engine, and with every possible
        # parameter tested, that 1) it always returns something sane and 2)
        # it always renders to well-formed XML.
        for engine in possible_engines():
            with self.settings(FLEXIBLE_IMAGE_ENGINE=engine):
                for parameter in test_parameters:
                    if parameter[0]:
                        argdict = {parameter[0]: parameter[1]}
                    else:
                        argdict = {}

                    context = flexible_image(self.image, **argdict)
                    # Make sure we're getting back so0mething sane.
                    self.assertTrue(isinstance(context, dict))

                    html = render_to_string("flexible-images/flexible-image.html", context)
                    # While it returns HTML, it should also be well-formed XML.
                    et_fromstring(html)

                    # Make sure the django-jinja output is always,
                    # byte-for-byte, identical to the normal HTML output.
                    django_jinja_html = django_jinja_flexible_image(self.image, **argdict)
                    self.assertEqual(html, django_jinja_html)

    def test_flexible_image_list(self):
        images = flexible_image_list(self.image)
        images_pj = django_jinja_flexible_image_list(self.image)
        self.assertEqual(images, images_pj)
        self.assertTrue(isinstance(images, list))
        self.assertTrue(isinstance(images_pj, list))

        for item in images:
            self.assertTrue(isinstance(item, dict))
