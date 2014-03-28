Files for Components
====================

These files and directories will be relevant when working on the
Components part of your theme.

/browser/viewlet.py \| viewlet.pt

An example viewlet component

/browser/interfaces.py

This is used to create your theme interface (and any other interfaces
you might need)

/profiles/default/viewlets.xml

Use this file to order your viewlets within viewlet managers

/browser/configure.zcml

Use this file to wire up your components

/browser/templates \| styles

These directories can be used for templates, styles, and images. You
will need to register these as directories as resources in
configure.zcml.

.. figure:: /old-reference-manuals/plone_3_theming/images/your_theme_egg_components.gif
   :align: center
   :alt: your theme egg - the components files

   your theme egg - the components files
 
