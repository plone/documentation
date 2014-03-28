Files for the Skin
==================

These files and directories will be relevant when working on the Skin
part of your theme.

/skins/[your theme namespace].[your theme name]\_custom\_templates \|
custom\_images \| styles

These directories will form your skin layers. Your templates, images,
and stylesheets can go here. If you asked it to, the plone3\_theme
paster template will have provided blank style sheets to override the
Plone Default ones.

/skins.zcml

When your Zope instance starts up, this turns your directories into skin
layers

/profiles/default/skins.xml \| cssregistry.xml \| jsregistry.xml

When your theme is installed in your Plone site, this sets up the
hierarchy of skin layers, and registers your style sheets and JavaScript
with the registries

.. figure:: /old-reference-manuals/plone_3_theming/images/your_theme_egg_skin.gif
   :align: center
   :alt: your theme egg - the skin files

   your theme egg - the skin files
 
