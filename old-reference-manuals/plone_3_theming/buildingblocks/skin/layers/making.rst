Making and Naming your own Skin
===============================

How do you actually create a Skin?

Through the ZMI
---------------

-  Go to Site Setup > Zope Management Interface > portal\_skins
-  Click the Properties tab
-  Choose Add New and give your skin a name
-  You can now type in a list of the layers you want to use, in the
   order you want to use them
-  Finally, at the bottom of the page, set your new skin as the default

On the File System
------------------

If you use the plone3\_theme paster template, code will be provided
which, when your theme product is installed, will register your skin
directories as skin layers and put these together into a new skin.

The paster template gives you the option of basing your skin on Plone
Default. That is, when you install the theme in your site, the Plone
skin layers will be added to yours - but below yours in the order of
precedence. This is a good idea, you can then re-use bits of Plone
Default without duplicating it, and overwrite the bits you don't want.

The key steps are:

#. Register your skin directories as Filesystem Directory Views, so that
   they can become skin layers. This happens in two places:[your theme
   package]/skins.zcml and [your theme
   package]/profiles/default/skins.xml

   ::

       <cmf:registerDirectory
              name="[Your Skin Directory Name]"/>

   ::

       <object name="[Your Skin Directory Name]"
           meta_type="Filesystem Directory View"
           directory="[your namespace].[your theme name]:skins/[Your Skin Directory Name]"/>

#. Add and organize your skin layers into a skin in [your theme
   package]/profiles/default/skins.xml

   ::

       <skin-path name="[your skin name" based-on="Plone Default">
         <layer name="[Your Skin Directory Name]"
            insert-after="custom"/>
        </skin-path>

#. Set your skin as the default skin in [your theme
   package]/profiles/default/skins.xml by wrapping this node around the
   nodes in the previous two examples.

   ::

       <object name="portal_skins" allow_any="False" cookie_persistence="False"
          default_skin="[your skin name]">
           .........
       </object>

 About the Skin Name
--------------------

The name of your skin is required in a few places in your theme product.
It is worth knowing where and why, so, for reference, the occurrences
are listed here.

Where

Attributes/Directives used

Use

profiles/default/skins.xml

<skin\_path name="[your skin name]"

Used to name your set of skin layers.

profiles/default/skins.xml

<object name="portal\_skins"

default\_skin="[your skin name]">

Used to set your set of skin layers as the default skin.

browser/configure.zcml

<interface …

name="[your skin name]"

/>

Used to name the theme specific interface (see
`Components <http://plone.org/documentation/manual/theme-reference/buildingblocks/skin/components>`_
section)

profiles/default/viewlets.xml

<order manager="plone.portalfooter" skinname="[your skin name]"

>

Used to specify the theme when reordering viewlets in viewlet managers

(see
`Components <http://plone.org/documentation/manual/theme-reference/buildingblocks/skin/components>`_
section)
