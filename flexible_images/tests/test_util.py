from .. import util
from .base import FlexibleImageTestCase


class UtilsTest(FlexibleImageTestCase):
    def test_aspect_ratio(self):
        """Our test image has an aspect ratio of exactly 1:0.6625."""
        self.assertEqual(
            util.aspect_ratio(self.image),
            0.6625,
        )

    def test_aspect_ratio_percent(self):
        self.assertEqual(
            util.aspect_ratio_percent(self.image),
            66.25
        )

    def test_get_thumbnail_engine(self):
        # Ensure that giving an invalid thumbnail engine causes
        # get_thumbnail_engine to fail.
        with self.settings(FLEXIBLE_IMAGE_ENGINE="invalid"):
            self.assertRaises(util.FlexibleImageError, util.get_thumbnail_engine)

        # Ensure that it will give the correct thumbnail engine if it is set
        # to something valid.
        with self.settings(FLEXIBLE_IMAGE_ENGINE="sorl"):
            self.assertEqual(util.get_thumbnail_engine(), "sorl")

    def test_get_thumbnail_shim(self):
        # Make sure that if a thumbnailer is given, then this returns an image
        # of the specified width.
        with self.settings(FLEXIBLE_IMAGE_ENGINE="sorl"):
            scaled = util.get_thumbnail_shim(self.image, 500)
            self.assertEqual(scaled.width, 500)

        with self.settings(FLEXIBLE_IMAGE_ENGINE=None):
            thesame = util.get_thumbnail_shim(self.image, 500)
            self.assertEqual(self.image, thesame)

    def test_settings_sizes(self):
        # Make sure FLEXIBLE_IMAGE_SIZES is being obeyed.
        with self.settings(FLEXIBLE_IMAGE_SIZES=self.settings_sizes):
            self.assertEqual(util.settings_sizes(), self.settings_sizes)

        # Make sure the defaults still work.
        with self.settings(FLEXIBLE_IMAGE_SIZES=None):
            self.assertEqual(util.settings_sizes(), [
                480,
                768,
                1024,
                1280,
                1440,
            ])

    def test_get_image_sizes(self):
        # We need to test the case of multiple images having the same size.
        # It must never return multiple images of the same size.
        fake_sizes = [1024, 1024, 800, 400]
        with self.settings(FLEXIBLE_IMAGE_SIZES=fake_sizes):
            items = util.get_image_sizes(self.image)

        seen_widths = []
        for item in items:
            self.assertFalse(item["width"] in seen_widths)
            seen_widths.append(item["width"])

    def test_get_template_context(self):
        with self.settings(FLEXIBLE_IMAGE_ENGINE=None):
            context = util.get_template_context(self.image)
            # Ensure that it returns something that makes sense.
            self.assertTrue(isinstance(context, dict))
            # Ensure that in this case it's just returning itself.
            self.assertFalse("image_sizes_json" in context)
            self.assertFalse("image_sizes" in context)

        with self.settings(FLEXIBLE_IMAGE_ENGINE="sorl"):
            context = util.get_template_context(self.image)
            self.assertTrue("image_sizes" in context)
            self.assertTrue("image_sizes_json" in context)
            self.assertTrue(len(context["image_sizes"]) > 0)
