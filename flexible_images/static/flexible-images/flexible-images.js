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
    elem = elems[i];
    doSwitch(elem);
  }
}

if (window.addEventListener) {
  window.addEventListener("DOMContentLoaded", flexibleImageSwitcher);
  window.addEventListener("resize", flexibleImageSwitcher);
}
