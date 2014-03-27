Making Components Theme Specific
================================

You may want to make components only available for your particular
theme. To do this you will need an interface.

As components come into being as soon as Zope starts up and reads the
.zcml files, they are available for every Plone site you have in a Zope
instance. You might not want this to happen.

A Theme Interface
-----------------

You can specify that your components are available only for your theme
with a marker interface and a layer attribute in ZCML. Here's a rewired
version of the presentation viewlet:

::

    <browser:viewlet
          name="[your namespace].[your presentation viewlet]"
          for="Products.ATContentTypes.interface.IATDocument"
          manager="plone.app.layout.viewlets.interfaces.IAboveContentBody"
          class=".[your viewlet module].[your viewlet class]"
          layer=".interfaces.IThemeSpecific"
          permission="zope2.View"
          />

Note: Don't confuse the layer attribute with a skin layer. Here, layer
refers to the whole theme rather than just one slice of it.

There are two methods for creating a theme interface:

Using plone.theme
~~~~~~~~~~~~~~~~~

In Plone 3.0, plone.theme is used:

-  A marker interface is defined in [your theme
   package]/browser/interfaces.py:

::

    from plone.theme.interfaces import IDefaultPloneLayer

    class IThemeSpecific(IDefaultPloneLayer):
        """Marker interface that defines a Zope 3 browser layer.    """

-  and this is registered in ZCML in [your theme
   package]/browser/configure.zcml

::

    <interface
            interface=".interfaces.IThemeSpecific"
            type="zope.publisher.interfaces.browser.IBrowserSkinType"
            name="[your skin name]"
            />

Note: [your skin name] crops up here; refer back to the skins section if
you are wondering what this is.

Using plone.browserlayer
~~~~~~~~~~~~~~~~~~~~~~~~

In Plone 3.1, plone.browserlayer is available to you.

-  Create your interface (e.g. in [your theme
   package]/browser/interfaces.py)

::

    from zope.interface import Interface
        class IThemeSpecific(Interface):
            """A layer specific to my product        """

-  Register this in the configuration (in [your theme
   package]/profiles/default/browserlayer.xml):

::

    <layers>
     <layer name="[your skin name]"
       interface="[your namespace].[your theme name].browser.interfaces.IThemeSpecific"
     />
    </layers>

If you generate your file system product or egg using the plone3\_theme
paster template, then the basics will be done for you (using the
plone.theme method), you will simply need to track down the interface to
find its name. Look in

-  [your theme package]/browser/interfaces.py or configure.zcml

and you should find it with the name IThemeSpecific. When you refer to
it, use its path

::

    layer=".interfaces.IThemeSpecific"

