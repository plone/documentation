Where to find what you need
===========================

How configuration works through the web and how to track down files on
the file system.

Through the Web
---------------

There are a number of different routes to configure your site through
the web. The
`Elements <http://plone.org/documentation/manual/theme-reference/elements/elementsindex>`_
section of this manual should give you pointers on where to look to
configure particular page elements. In general

-  Site Setup leads you to configlets for the site settings
-  Site Setup > Zope Management Interface will lead you to the style
   sheet and JavaScript registry (portal\_css and portal\_javascripts)
-  Adding /@@viewlet\_manager to a URL will enable you to order viewlets

Plone Default Configuration on the File System
----------------------------------------------

You will find most of the configuration files you need in:

-  [your products location]/CMFPlone/profiles/default

However, be aware that some configuration files may be located in
third-party products. For instance, if you want to add some styles to
the visual editor, Kupu, as part of your theme, then you will need
kupu.xml which you'll find in [your products
location]/kupu/plone/profiles/default.

There's an alternative to hunting around the file system, and that's to
use the Generic Setup Tool to export the profile.

In your own Theme Product
-------------------------

 |The configuration directory in your theme product|/profiles/default/
    This directory holds the XML for Generic Setup. The plone3\_theme
    paster template will have provided you with some ready-made files -
    for setting up your skin layers, registering your style sheets and
    JavaScript, and ordering your viewlets.

/profiles/default/import\_steps.xml
    Is an essential file for installation, you shouldn't need to change
    this.
/profiles/default/cssregistry.xml \| jssregistry.xml
    will register any style sheets and JavaScript in your skin. You will
    have to edit these yourself if you have any css or Javascript files
    to add.
/profiles/default/skins.xml
    Will drop your skin layers into the right order of precedence. You
    won't need to change this unless you've renamed, removed, or added
    directories in the skins directory of your theme egg.
/profiles/default/viewlets.xml
    will determine in what order viewlets appear in viewlet managers.
    You will need to edit this yourself if you want to add your own
    viewlets.
/profiles.zcml
    When your Zope instance starts up, this file makes the profile
    available for Generic Setup to use.

.. |The configuration directory in your theme product| image:: /old-reference-manuals/plone_3_theming/images/your_theme_egg_config_cutdown.gif
