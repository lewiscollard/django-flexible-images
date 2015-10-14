function doSwitch (elem) {
  "use strict";
  var sizeAttr, sizes, newImage, containerWidth, useThis, j;
  var nativeSize = parseInt(elem.getAttribute("data-native-size"));

  var sizeAttr = elem.getAttribute("data-sizes");
  if (!sizeAttr) {
    return;
  }

  sizes = JSON.parse(sizeAttr);
  containerWidth = elem.parentElement.offsetWidth;

  // If we can't find a size of an image that is bigger than or equal to the
  // size of the image's container, then default to using the largest one.
  useThis = sizes[sizes.length - 1];

  for (j = 0; j < sizes.length; j++) {
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
  // circumstances in which this would otherwise happen
  console.log("elem.width=" + elem.width, "useThis.width=" + useThis.width)

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
  for (i=0; i < elems.length; i++) {
    elem = elems[i];
    doSwitch(elem);
  }
}

function flexibleImageDoCookie() {
  "use strict";
  if (!document.flexibleImageSetCookie) {
    return;
  }
  var match = document.cookie.match(new RegExp('flexible-images=([^;]+)'));
  if (!match) {
      var d = new Date();
      var width = window.screen.width;
      d.setTime(d.getTime() + (10*24*60*60*1000));
      var expires = "expires=" + d.toUTCString();
      document.cookie = "flexible-images=max-size_" + width.toString();
  }
}

if (window.addEventListener) {
  window.addEventListener("DOMContentLoaded", flexibleImageSwitcher);
  window.addEventListener("DOMContentLoaded", flexibleImageDoCookie);
  window.addEventListener("resize", flexibleImageSwitcher);
}

