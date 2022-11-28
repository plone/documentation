/**
 * Patch of scrollToActive of sphinxbook theme
 * Scroll to active navigation item
 */

/**
 * A helper function to load scripts when the DOM is loaded.
 * This waits for everything to be on the page first before running, since
 * some functionality doesn't behave properly until everything is ready.
 */
 var sbRunWhenDOMLoaded = (cb) => {
  if (document.readyState != "loading") {
    cb();
  } else if (document.addEventListener) {
    document.addEventListener("DOMContentLoaded", cb);
  } else {
    document.attachEvent("onreadystatechange", function () {
      if (document.readyState == "complete") cb();
    });
  }
};

/**
 * Sidebar scroll on load.
 *
 * Detect the active page in the sidebar, and scroll so that it is centered on
 * the screen.
 */

var scrollToActive = () => {
  let navbar_scrollable = $("#site-navigation").children()[0];
  let active_navigation_item = $("#site-navigation .active").last();
  if (active_navigation_item) {
    if (active_navigation_item.offset().top > $(window).height() * 0.5) {
      navbar_scrollable.scrollTop = active_navigation_item.offset().top - $(window).height() * 0.2;
    }
  }
};


sbRunWhenDOMLoaded(scrollToActive);
