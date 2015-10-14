django-flexible-images, a responsive image solution for Django
==============================================================

Quick usage
-----------

1. Add `flexible_images` to your `INSTALLED_APPS`.
2. Load the `flexible_images` template tag library.
3. Use `{% flexible_image your_model_instance.some_imagefield %}` inside a
   container of the desired width.

For sample usage and for testing, this comes with a `FlexibleImageTestView`
view class in `views.py` and a sample 3:2 (ish) image.

Smarter aspect ratio preservation
---------------------------------
We want to ensure that images will fit on any screen size without overflowing,
but preserve their aspect ratio.

The simple approach is to use `max-width: 100%` and `height: auto` on an
image. However, because the browser *cannot know in advance how high
`auto` will be*, when an image starts to load it causes a reflow of the
document. This is usually experienced as document elements being pushed down
as images load. Most commonly, this means that the thing you are reading
will be pushed down as images above it load.

Fortunately, two quirks of the CSS specification are here to help us.

1. When specified as a percentage, vertical `padding` of CSS elements is
   calculated as a percentage of the parent element's width.
2. When specified as a percentage, the height of an absolutely positioned
   element within a relative-positioned element will be the height of the
   bounding box of the image, which is to say, the inner height of the box
   *plus its padding*.

Therefore, 1) will allow us to create a container with a certain aspect ratio
(e.g. if the box has `padding-bottom` set to 66.666%, the container will have
a 3:2 aspect ratio). This will be the case at any size, and this size is
computed immediately as the element is added into the document; no reflows
will occur.

From there, if we absolutely position an image to the top left of that and
set both width and height to 100%, it will fill that container, and it will
preserve its aspect ratio at any screen size.

The rest is trivial; this README and the test HTML file is nearly an order of
magnitude larger than the code. We know the width and height of a file in an
ImageField, so the template tag renders a container element with CSS for the
correct aspect ratio for the image, and uses CSS to position the element
within it.

How?
----
For most uses, just pass any ImageField as an argument to the
`{% flexible_image %}` template tag.

There are a few arguments you can pass to the tag if required:

* `container`: The HTML tag in which to wrap the image. Defaults to `div`.
* `classes`: A space-separated list of extra classes to apply to the container
  element. Defaults to empty string.
* `alt`: [Alt text](https://en.wikipedia.org/wiki/Alt_attribute) for the
  image.

Don't use `container` or `classes` to style the width of the image's container
element with CSS; iOS Safari (unlike most others, but correctly) calculates
`padding-bottom` percentages from the width of the _parent_ element. Wrap your
`{% flexible_image %}` tag in a container of the desired width instead.

Bonus
-----
The `{% flexible_image_js %}` tag can be placed after all the flexible images
have been loaded into your site; it'll add a "loading" class to your images
as they are loading. See `templates/flexible-image-test.html` for a
demonstration of how this could be useful.

Who?
----
This was written by Lewis Collard at [Onespacemedia](http://www.onespacemedia.com/).

Compatibility
-------------
This should work in any recent version of Django. This has been tested with
1.8, but most earlier versions should work fine.

This works with `ImageField`s, but it also plays nice with
[sorl-thumbnail](https://sorl-thumbnail.readthedocs.org),
[easy-thumbnails](https://github.com/SmileyChris/easy-thumbnails), or anything
else that returns an object with `width` and `height` attributes.

This works in any sane web browser, desktop and mobile. IE 7 and 8 should
work, too.

It is CSS-framework-agnostic; it'll work with any framework, or no framework.

License
-------
[Public domain](https://creativecommons.org/publicdomain/zero/1.0/).
