/*global window*/
(function () {
    "use strict";
    // This will be set to true if the browser fully supports srcset (width as
    // well as pixel density).
    var supportsSrcSet = false;

    function doSwitch(elem) {
        var sizes, newImage, containerWidth, useThis, j;
        var nativeSize = parseInt(elem.getAttribute("data-native-size"), 10);
        var usingBackgroundImage = false;
        if (elem.tagName.toLowerCase() !== "img") {
            usingBackgroundImage = true;
        }

        if (!usingBackgroundImage && supportsSrcSet) {
            // Don't do anything, it's an <img> tag and the browser properly
            // supports srcset.
            return;
        }

        var sizeAttr = elem.getAttribute("data-sizes");
        if (!sizeAttr) {
            return;
        }

        sizes = JSON.parse(sizeAttr);
        containerWidth = elem.parentElement.offsetWidth;

        // If we can't find a size of an image that is bigger than or equal to
        // the size of the image's container, then default to using the
        // largest one.
        useThis = sizes[sizes.length - 1];

        for (j = 0; j < sizes.length; j += 1) {
            if (sizes[j].width >= containerWidth) {
                useThis = sizes[j];
                break;
            }
        }

        var currentsrc, bgimage;
        if (!usingBackgroundImage) {
            currentsrc = elem.getAttribute("src");
        } else {
            bgimage = elem.style.backgroundImage;
            if (!bgimage) {
                // ?
                return;
            }
            currentsrc = bgimage.substr(4, bgimage.length - 5);
        }

        // Obviously, no point in switching for the same image.
        if (useThis.url === currentsrc) {
            return;
        }

        // And don't replace a high-res image with a low-res one! There are
        // circumstances in which this would otherwise happen, like when
        // scaling down a window (or rotating a tablet).
        if (useThis.width < nativeSize) {
            return;
        }

        // Switcheroo.
        newImage = new Image();
        newImage.onload = function () {
            elem.removeAttribute("srcsset");
            elem.setAttribute("data-native-size", newImage.width);
            if (usingBackgroundImage) {
                elem.style.backgroundImage = 'url(' + useThis.url + ')';
            } else {
                elem.src = useThis.url;
            }
        };
        newImage.src = useThis.url;
    }

    function flexibleImageSwitcher() {
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
            // Unset for old Safari (and maybe others) with incomplete srcset
            // support. They will attempt to parse it, but will think that
            // they want the low resolution version, and it'll stay that way
            // because `srcset` takes precedence over `src`.
            if (!supportsSrcSet) {
                elem.removeAttribute("srcset");
            }
            doSwitch(elem);
        }
    }

    // Don't bother with any of the JS switching stuff if full srcset support
    // is present.
    //
    // Edge 12, Safari 8, iOS Safari 8.4 and Android browser <= 44 implement
    // one which doesn't support width queries (only pixel-density ones).
    // Fortunately, they don't support the `sizes` attribute either. As far as
    // I know, all devices that support `srcset` in full also support `sizes`.
    var img = document.createElement("img");
    if (("srcset" in img) && ("sizes" in img)) {
        supportsSrcSet = true;
    }

    // Sorry, prehistory.
    if (!window.addEventListener) {
        return;
    }

    var resizeTimeout = null;

    // If the DOMContentLoaded event has already happened, then run
    // flexibleImageSwitcher immediately. This allows flexible-images.js to
    // be loaded asynchronously.
    if (document.readyState === "complete" || document.readyState === "interactive") {
        flexibleImageSwitcher();
    } else {
        window.addEventListener("DOMContentLoaded", flexibleImageSwitcher);
    }

    window.addEventListener("resize", function () {
        // Avoid storms of events being fired during resize by doing it once,
        // 500ms after the last resize.
        if (resizeTimeout) {
            window.clearTimeout(resizeTimeout);
            resizeTimeout = null;
        }
        resizeTimeout = window.setTimeout(flexibleImageSwitcher, 500);
    });
}());
