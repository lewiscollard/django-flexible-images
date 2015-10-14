#!/usr/bin/python

HAS_THUMBNAILER = False
try:
    from easy_thumbnails import get_thumbnailer
    USE_EASY = True
    HAS_THUMBNAILER = True
except ImportError:
    get_thumbnailer = None
    USE_EASY = False

try:
    from sorl.thumbnail import get_thumbnail as sorl_thumbnail
    USE_SORL = True
    HAS_THUMBNAILER = True
except ImportError:
    sorl_thumbnail = None
    USE_SORL = False


def aspect_ratio(image):
    return float(image.height) / float(image.width)


def aspect_ratio_percent(image):
    return aspect_ratio(image) * 100


def get_thumbnail_shim(image, width):

    # Prefer easy_thumbnails if it's installed, because it's awesome!
    if USE_EASY:
        thumbnailer = get_thumbnailer(image)
        params = {
            "size": (width, width),
            "crop": False,
        }
        return thumbnailer.get_thumbnailer(params)

    if USE_SORL:
        # Let's do a sorl!
        im = sorl_thumbnail(image, '{}x{}'.format(width, width), upscale=False)
        return im

    # No thumbnailer. :(
    return image
