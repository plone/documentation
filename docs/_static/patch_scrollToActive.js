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
  var navbar = document.getElementById("site-navigation");
  var navbar_scrollable = navbar.children[0];
  var active_pages = navbar.querySelectorAll(".active");
  var active_page = active_pages[active_pages.length - 1];
  // Only scroll the navbar if the active link is lower than 50% of the page
  if (
    active_page !== undefined &&
    active_page.offsetTop > $(window).height() * 0.5
  ) {
    navbar_scrollable.scrollTop =
      active_page.offsetTop - $(window).height() * 0.2;
  }
};


sbRunWhenDOMLoaded(scrollToActive);

$(document).ready(function() {
  console.debug("debug patch_scrollToActive")
});
