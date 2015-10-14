#!/usr/bin/python
HAS_THUMBNAILER = False

try:
    from sorl.thumbnail import get_thumbnail as sorl_thumbnail
    USE_SORL = True
    HAS_THUMBNAILER = True
except ImportError:
    USE_SORL = False
    sorl_thumbnail = None


def aspect_ratio(image):
    return float(image.height) / float(image.width)


def aspect_ratio_percent(image):
    return aspect_ratio(image) * 100


def get_thumbnail_shim(image, width):
    # This is in its own function because it'll make it easy to add support
    # for other thumbnailers in future. (easy_thumbnails should be easy,
    # and I had it written, but it refuses to work properly with anything that
    # is not an ImageField, i.e. in our test view in views.py.)
    if USE_SORL:
        # Let's do a sorl!
        im = sorl_thumbnail(image, '{}x{}'.format(width, width), upscale=False)
        return im

    # No thumbnailer. :(
    return image
