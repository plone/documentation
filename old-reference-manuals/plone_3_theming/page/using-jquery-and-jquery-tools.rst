Using jQuery and jQuery Tools
=============================

Plone includes the jQuery and jQuery Tools JavaScript libraries out of
the box, which you can use in your own scripts right away.

`jQuery <http://jquery.com/>`_ is a popular JavaScript Library that
simplifies HTML document traversal, event handling, animating, and Ajax
interactions. `jQuery Tools <http://flowplayer.org/tools/index.html>`_
is a collection of user-interface components including overlays, tabs,
accordions and tooltips.

jQuery has been shipped with Plone since 3.1. jQuery Tools was added
with Plone 4.0.

Using jQuery
~~~~~~~~~~~~

jQuery has excellent documentation available at
`http://api.jquery.com <http://api.jquery.com>`_. Note, though, that it
is never wise to depend on the availability of the "$" alias for the
jQuery function since other libraries may redefine it.

So, Instead of:

::

    $(document).ready(function(){
       $("a").click(function(event){
         alert("Thanks for visiting!");
       });
     });

you should embed and jQuery code that uses the "$" alias in a wrapper
like:

::

    (function($) {
     $(document).ready(function(){
       $("a").click(function(event){
         alert("Thanks for visiting!");
       });
     });
    })(jQuery);

Using jQuery Tools
~~~~~~~~~~~~~~~~~~

jQuery Tools is a jQuery plugin, and Plone 4 includes the tabs, tooltip,
scrollable, overlay and expose toolset. The remainder of the jQuery
Tools kit plugins are available by enabling the
plone.app.jquerytools.plugins.js resource Plone's JavaScript registry.

The integration with jQuery Tools is provided through the package
`plone.app.jquerytools <http://pypi.python.org/pypi/plone.app.jquerytools/>`_,
which includes a set of overlay helpers for common AJAX overlay needs.
This kit is used to provide many of Plone's overlayed forms. See the
`plone.app.jquerytools pypi
page <http://pypi.python.org/pypi/plone.app.jquerytools/>`_ for
documentation and examples.
