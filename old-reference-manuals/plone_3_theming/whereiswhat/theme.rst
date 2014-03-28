Files for Installing your Theme
===============================

These are the files used when you install your theme product using Site
Setup > Add / Remove Products or Zope Management Interface >
portal\_quickinstaller

/profiles/default/

Generic Setup will install your theme profile when your theme is
installed. import\_steps.xml points to a 'handler' for installation
steps which aren't yet part of Generic Setup or can't be expressed as
XML.

/setuphandlers.py

This contains the handler for non-Generic Setup installation steps.

.. figure:: /old-reference-manuals/plone_3_theming/images/your_theme_egg_qi_installation.gif
   :align: center
   :alt: your theme egg - the files used by quick installer

   your theme egg - the files used by quick installer

