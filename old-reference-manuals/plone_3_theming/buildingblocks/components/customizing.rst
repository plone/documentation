Customizing or Creating New
===========================

You can customize through the web, but on the file system, the way to
customize or create components for your theme is to wire up new ones.

Through the Web
---------------

Just as for Skins and Layers, it is possible to customize the templates
used by components through the Zope Management Interface.

-  Site Setup > Zope Management Interface > portal\_view\_customizations

You will need to know the name of your component (plone.presentation for
instance). The
`Elements <http://plone.org/documentation/manual/theme-reference/elements/elementsindex>`_
section of this manual will help if the name isn't obvious. You can only
rewrite the template, which might be limiting.

On the File System
------------------

You can achieve much more if you are building your own theme product on
the file system, and in this case the approach is slightly different.

Rather than overwrite a component (as you could for skins), it is far
easier to create your own version. This involves some rewiring or new
wiring in your own .zcml file, but is actually simpler than it sounds.

Here's an example of the presentation viewlet - as it is used by Plone:

::

    <browser:viewlet
          name="plone.presentation"
          for="Products.ATContentTypes.interface.IATDocument"
          manager="plone.app.layout.viewlets.interfaces.IAboveContentBody"
          class=".presentation.PresentationViewlet"
          permission="zope2.View"
          />

Imagine, for your purposes, you need to use a new class to get this
viewlet as you want. In your own configure.zcml file, give it a new name
and wire in your own class.

::

    <browser:viewlet
          name="[your namespace].[your presentation viewlet]"
          for="Products.ATContentTypes.interface.IATDocument"
          manager="plone.app.layout.viewlets.interfaces.IAboveContentBody"
          class=".[your viewlet module].[your viewlet class]"
          permission="zope2.View"
          />

-  Remember that the dot in front of your class namespace indicates that
   it can be found in the same directory as this configure.zcml file.
-  If you're not sure where your configure.zcml file lives, consult the
   `Where to Find What you
   Need <http://plone.org/documentation/manual/theme-reference/buildingblocks/components/locations>`_
   page of this section.

