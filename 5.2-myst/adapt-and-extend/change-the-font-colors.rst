Change the Font Colors - deprecated
====================================

.. note::

  This tutorial is deprecated for Plone 5. New documentation is almost ready.


How to change the font colors - a through-the-web approach.

You'll be introduced to some very simple techniques here for
through-the-web customizations of Plone's CSS.

-  How to locate the styles you want to change
-  How to override these styles using the ploneCustom.css style sheet

In this case we'll change the color of page titles from black to
turquoise.

Before you start
----------------

For convenience, Plone themes often comprise a number of separate style
sheets, but for speed and efficiency, in production mode, Plone has a
mechanism (portal\_css) for packaging these up into just one or two
files.

You'll need to disable this when making changes to your site or
customizing CSS. So make sure you've followed the instructions on how to
put your site into :doc:`debug mode </develop/plone/getstarted/debug_mode>`.

Locating the styles you want to change
--------------------------------------

-  If you don't already have a page in your Plone site, add one, save it
   and inspect it in view mode.
-  Use `Firebug <https://getfirebug.com/>`_ , or a similar
   tool, to locate the class name of the page title - in this case its
   h1.documentFirstHeading.

Locating the ploneCustom.css style sheet
----------------------------------------

As a matter of course, the last style sheet to load on every Plone page
is ploneCustom.css. You'll see this if you inspect the HTML head tag of
your page using Firebug. If you dig further, you'll probably find that
this style sheet is completely empty. By the rules of precedence in the
CSS Cascade, any styles in this sheet will override styles specified in
the preceding sheets. So you have a "blank sheet" here for your own
customizations.

The trick now is to locate this file, so that you can make it available
for editing.

To make life easier for yourself, you might like to open a second tab or
browser window at this point - you can then quickly switch back to the
first tab to see your changes.

Go to Site Setup > Management Interface and click portal\_skins

Use the Find option in the tabs across the top to locate
ploneCustom.css:

-  Type *ploneCustom.css* in the "with ids:" box and click Find
-  You may get more than one result, it doesn't matter which you choose
   to click on, however best practice is to choose the one flagged with
   the red asterisk.

Customizing and Editing ploneCustom.css
---------------------------------------

When you click on ploneCustom.css you'll find that you can't edit it.
The next stage is to put the ploneCustom.css in a place where it can be
edited. You'll see a Customize option just above the grey text area,
click the Customize button and you'll find that the style sheet has been
automatically copied to portal\_skins/custom.

You're now free to edit the file as you like. To change the color of
our page titles, add:

::

    h1.documentFirstHeading {
        color: #0AAE95;
    }

and save.

If you've installed Plone 4 with the Sunburst theme, the ploneCustom.css
comes with a number of commented out pre-packaged styles that you might
like to experiment with. You can override the layout styles to a fixed
width and alter the colors of the links.

Rolling back your changes
-------------------------

You've got a couple of options for reverting back to the original CSS:

comment out your styles in the ploneCustom.css - the usual CSS
commenting syntax applies

delete (or, if you want to keep a note of what you did, rename) your
version of ploneCustom.css, you'll find it here:

-  Site Setup > Management Interface > portal\_skins > custom
-  you can choose the delete or rename options - try renaming to
   ploneCustom.css.old
-  you can then go back to the beginning of the process of locating and
   customizing ploneCustom.css

Further Information
-------------------

You've actually encountered two types of customization here.

#. The first is a standard method of using order of precedence - the
   Cascade - to overwrite CSS styles as they reach the browser.
#. The second is a Plone/Zope specific method of overriding the style
   sheets themselves by dropping them into the custom folder of
   portal\_skins. This method can also be used for templates and other
   resources and is explained in more :doc:`depth in the section on Skin
   Layers </adapt-and-extend/theming/templates_css/skin_layers>`
   in this manual.

More advanced techniques, including incorporating your own style sheets
into a theme product, are covered later in this manual.

You can find out more about how the CSS Registry (portal\_css) packages
up the style sheets to deliver them to the page in the :doc:`Templates and
Components to
Page </adapt-and-extend/theming/templates_css/index>`
section of this manual.
