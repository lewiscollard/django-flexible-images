function doSwitch(elem) {
  "use strict";
  var sizes, newImage, containerWidth, useThis, j;
  var nativeSize = parseInt(elem.getAttribute("data-native-size"), 10);

  var sizeAttr = elem.getAttribute("data-sizes");
  if (!sizeAttr) {
    return;
  }

  sizes = JSON.parse(sizeAttr);
  containerWidth = elem.parentElement.offsetWidth;

  // If we can't find a size of an image that is bigger than or equal to the
  // size of the image's container, then default to using the largest one.
  useThis = sizes[sizes.length - 1];

  for (j = 0; j < sizes.length; j += 1) {
    if (sizes[j].width >= containerWidth) {
      useThis = sizes[j];
      break;
    }
  }

  // Obviously, no point in switching for the same image.
  if (useThis.url === elem.getAttribute("src")) {
   return;
  }

  // And don't switch out a high-res image for a low-res one! There are
  // circumstances in which this would otherwise happen, like when scaling
  // down a window (or resizing a tablet.)
  if (useThis.width < nativeSize) {
    return;
  }

  // Switcheroo.
  newImage = new Image();
  newImage.onload = function () {
    elem.removeAttribute("srcsset");
    elem.src = useThis.url;
    elem.setAttribute("data-native-size", elem.width);
  };
  newImage.src = useThis.url;
}

function flexibleImageSwitcher() {
  "use strict";
  // Ancient.
  if (!JSON) {
    return;
  }
  var elems = document.getElementsByClassName("flexible-image-image");
  if (!elems.length) {
    return;
  }

  var i, elem;
  for (i = 0; i < elems.length; i += 1) {
    // Safari (and perhaps others) try to parse the srcset attribute in a
    // bad way, and won't let you
    elem = elems[i];
    // Unset for old Safari (and maybe others) with incomplete srcset support.
    // They will attempt to parse it, but will think that they want the
    // low resolution version, and it'll stay that way because `srcset` takes
    // precedence over `src`.
    elem.removeAttribute("srcset");
    doSwitch(elem);
  }
}

(function () {
  // Don't bother with any of the JS switching stuff if proper srcset support
  // is present.
  // Edge 12, Safari 8, iOS Safari 8.4 and Android browser <= 44 implement one
  // which doesn't support width queries (only pixel-density ones).
  // Fortunately, they don't support the `sizes` attribute either. As far as
  // I know, all devices that support `srcset` in full also support `sizes`.
  var img = document.createElement("img");
  if (("srcset" in img) && ("sizes" in img)) {
    return;
  }

  // Sorry, prehistory.
  if (!window.addEventListener) {
    return;
  }

  var resizeTimeout = null;
  window.addEventListener("DOMContentLoaded", flexibleImageSwitcher);
  window.addEventListener("resize", function() {
    // Avoid storms of events being fired during resize by doing it once,
    // 500ms after the last resize.
    if (resizeTimeout) {
      window.clearTimeout(resizeTimeout);
      resizeTimeout = null;
    }
    resizeTimeout = window.setTimeout(flexibleImageSwitcher, 500);
  });
})();
