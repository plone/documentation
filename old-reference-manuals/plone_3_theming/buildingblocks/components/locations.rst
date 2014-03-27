Where to find what you need
===========================

Where to put components in your own product and how to track them down
in the Zope Management Interface and on the file system.

Through the Web
---------------

The templates for most components can be customized through the web:

-  Site Setup > Zope Management Interface > portal\_view\_customizations

The
`Elements <http://plone.org/documentation/manual/theme-reference/elements/elementsindex>`_
section can help you identify the component you need.

Plone Default Components on the File system
-------------------------------------------

If you're planning to wire up your own components, you may need to track
down the relevant files of existing components to copy. This can be
tricky. They are packaged up into a number of different eggs, so you
need first to locate where your eggs are stored, and then work out which
of these contains the component elements you need.

-  To work out where your eggs are stored, look at the `Where is
   What <http://plone.org/documentation/manual/theme-reference/whereiswhat/egglocation>`_
   section of this manual?
-  The
   `Elements <http://plone.org/documentation/manual/theme-reference/elements/elementsindex>`_
   section of this manual will help you track down the egg containing
   the component you need.

In your own Theme Product
-------------------------

 |The browser folder in your theme product|/browser/viewlet.py \|
viewlet.pt
    An example viewlet component
/browser/interfaces.py
    This is used to create your theme interface
/profiles/default/viewlets.xml
    Use this file to order your viewlets within viewlet managers
/browser/configure..zcml
    Use this file to wire up your components
/browser/templates \| styles
    These directories can be used for templates, styles, and images. You
    will need to register these as directories as resources in
    configure.zcml

.. |The browser folder in your theme
product| image:: http://plone.org/documentation/manual/theme-reference/images/your_theme_egg_components_cutdown.gif
