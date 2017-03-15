======
Layers
======

.. admonition:: Description

   Layers allow you to enable and disable views and other site functionality based on installed add-ons and themes.


Introduction
============

Layers allow you to activate different code paths and modules depending on
the external configuration.

Examples:

* Code belonging to a theme is only active when that theme has been selected.

* Mobile browsing code is only active when the site is being browsed on a
  mobile phone.

Layers are marker interfaces applied to the HTTPRequest_ object.
They are usually used in conjunction with :term:`ZCML` directives to
dynamically activate various parts
of the configuration (theme files, add-on product functionality).

Layers ensure that only one add-on product can override the specific Plone
instance functionality in your site at a time, while still allowing you
to have possibly conflicting add-on products in your buildout and
ZCML. Remember that multiple Plone site instances can share
the same ZCML and code files.

Many ZCML directives take the optional ``layer`` parameter. See example,
resourceDirectory_

Layers can be activated when an add-on product is installed or a certain
theme is picked.

For more information, read

* `Making components theme specific <https://plone.org/documentation/manual/theme-reference/buildingblocks/components/themespecific>`_

* `Browser Layer tutorial <https://plone.org/documentation/tutorial/customization-for-developers/browser-layers>`_.

* `Zope 3 Developer Handbook, Skinning <http://zope3.xmu.me/skinning.html>`_

Using layers
============

Some ZCML directives (for example: `browser:page
<http://apidoc.zope.org/++apidoc++/ZCML/http_co__sl__sl_namespaces.zope.org_sl_browser/page/index.html>`_)
take a ``layer`` attribute.

If you have:

# ``plonetheme.yourthemename.interfaces.IThemeSpecific`` layer defined in
  Python code

# ``YourTheme`` product installed through add-on product installer on your
  site instance

then views and viewlets from your product can be enabled on the site
instance using the following ZCML::

     <!-- Site actions override in YourTheme -->
     <browser:viewlet
         name="plone.site_actions"
         manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
         class=".siteactions.SiteActionsViewlet"
         layer="plonetheme.yourthemename.interfaces.IThemeSpecific"
         permission="zope2.View"
         />

Unconditional overrides
-----------------------

If you want to override a view or a viewlet unconditionally for all sites
without the add-on product installer
support you need to use ``overrides.zcml``.

Creating a layer
================

Theme layer
-----------

Theme layers can be created via the following steps:

1. Subclass an interface from ``IDefaultPloneLayer``::

       from plone.theme.interfaces import IDefaultPloneLayer

       class IThemeSpecific(IDefaultPloneLayer):
           """Marker interface that defines a Zope 3 skin layer bound to a Skin
              Selection in portal_skins.
              If you need to register a viewlet only for the "YourSkin"
              skin, this is the interface that must be used for the layer attribute
              in YourSkin/browser/configure.zcml.
           """

2. Register it in ZCML. The name must match the theme name.

   .. code-block:: xml

       <interface
           interface=".interfaces.IThemeSpecific"
           type="zope.publisher.interfaces.browser.IBrowserSkinType"
           name="SitsSkin"
           />

3. Register and set your theme as the default theme in ``profiles/default/skins.xml``. Theme layers require that they are set as the default theme and not just activated on your Plone site. Example:

   .. code-block:: xml

       <object name="portal_skins" allow_any="False" cookie_persistence="False"
           default_skin="SitsSkin">

           <!-- define skins-based folder objects here if any -->

           <skin-path name="SitsSkin" based-on="Plone Default">
               <layer name="plone_skins_style_folder_name"
                   insert-before="*"/>
           </skin-path>

       </object>

Add-on layer for clean extensions
---------------------------------

An add-on product layer is enabled when an add-on product is installed.
Since one Zope application server may contain several Plone sites,
you need to keep enabled code paths separate by using add-on layers -
otherwise all views and viewlets apply to all sites in one Zope application server.

* You can enable views and viewlets specific to functional add-ons.

* Unlike theme layers, add-on layers depend on the activated add-on
  products, not on the selected theme.

An add-on layer is a marker interface which is applied on the
:doc:`HTTP request object </develop/plone/serving/http_request_and_response>`
by Plone core logic.

First create an :doc:`interface </develop/addons/components/interfaces>` for your layer in
``your.product.interfaces.py``::

    """ Define interfaces for your add-on.
    """

    import zope.interface

    class IAddOnInstalled(zope.interface.Interface):
        """ A layer specific for this add-on product.

        This interface is referred in browserlayer.xml.

        All views and viewlets register against this layer will appear on
        your Plone site only when the add-on installer has been run.
        """

You then need to refer to this in the ``profile/default/browserlayer.xml``
file of your add-on installer
:doc:`setup profile </develop/addons/components/genericsetup>`:

.. code-block:: xml

    <layers>
        <layer
            name="your.product"
             interface="your.product.interfaces.IAddOnInstalled"
             />
    </layers>

.. note::

    The add-on layer registry is persistent and stored in the database.
    The changes to add-on
    layers are applied only when add-ons are installed or uninstalled.

More information

* https://pypi.python.org/pypi/plone.browserlayer


Add-on layer for changing existing behavior
-------------------------------------------

You can also use layers to modify the behavior of plone or another Add-on.

To make sure that your own view is used, your Layer must be more specific than the layer where original view is registered.

For example, some z3cform things register their views on the ``IPloneFormLayer`` from plone.app.z3cform.interfaces.

If you want to override the ploneform-macros view that is registered on the ``IPloneFormLayer``, your own Layer must be a subclass of IPloneFormLayer.

If a view does not declare a specific Layer,  it becomes registered on the ``IDefaultBrowserLayer`` from zope.publisher.interfaces.browser.IDefaultBrowserLayer.

Manual layers
-------------

Apply your layer to the HTTPRequest_ in the ``before_traverse`` hook or
before you call the code which looks up the interfaces.

Choosing skin layer dynamically 1: http://blog.fourdigits.nl/changing-your-plone-theme-skin-based-on-the-objects-portal_type

Choosing skin layer dynamically 2: http://code.google.com/p/plonegomobile/source/browse/trunk/gomobile/gomobile.mobile/gomobile/mobile/monkeypatch.py

See the `plone.app.z3cform.z2 <http://svn.zope.org/plone.z3cform/trunk/plone/z3cform/z2.py?rev=88331&view=markup>`_ module.

In the example below we turn on a layer for the request which is later
checked by the rendering code.
This way some pages can ask for special View/Viewlet rendering.

Example::

    # Defining layer

    from zope.publisher.interfaces.browser import IBrowserRequest

    class INoHeaderLayer(IBrowserRequest):
        """ When applied to HTTP request object, header animations or images are not rendered on this.

        If this layer is on request do not render header images.
        This allows uncluttered editing of header animations and images.
        """

    # Applying layer for some requests (manually done in view)
    # The browser page which renders the form
    class EditHeaderAnimationsView(FormWrapper):

        form = HeaderCRUDForm

        def __call__(self):
            """ """

            # Signal viewlet layer that we are rendering
            # edit view for header animations and it is not meaningful
            # to try to render the big animation on this page
            zope.interface.alsoProvides(self.request, INoHeaderLayer)

            # Render the edit form
            return FormWrapper.__call__(self)


Troubleshooting instructions for layers
=============================================

* Check that your view or whatever is working without a layer assigned
  (globally);

* Check that ``configure.zcml`` has a layer entry. Put some garbage to
  trigger a syntax error in ``configure.zcml`` to make sure that it is being
  loaded;

* Add-on layer: check that ``profiles/default/browserlayer.xml`` has a
  matching entry with a matching name;

* Theme layer: if it's a theme layer, check that there is a matching
  ``skins.xml`` entry

* Check that layer name is correctly spelt in the view declaration.

Checking active layers
======================

Layers are activated on the current request object
----------------------------------------------------------------

Example::

    if INoHeaderLayer.providedBy(self.request):
        # The page has asked to suspend rendering of the header animations
        return ""

Active themes and add-on products
--------------------------------------

The ``registered_layers()`` method returns a list of all layers active on
the site.
Note that this is different to the list of layers which are applied on the
current HTTP request object:
the request object may contain manually activated layers.

Example::

    from interfaces import IThemeSpecific
    from plone.browserlayer.utils import registered_layers

    if IThemeSpecific in registered_layers():
        # Your theme specific code
        pass
    else:
        # General code
        pass

Getting active theme layer
--------------------------

Only one theme layer can be active at once.

The active theme name is defined in ``portal_skins`` properties.
This name can be resolved to a theme layer.

Debugging active layers
-----------------------

You can check the activated layers from HTTP request object by looking at
``self.request.__provides__.__iro__``.
Layers are evaluated from zero index (highest priority) the last index
(lowest priority).

.. _HTTPRequest: http://svn.zope.org/Zope/trunk/src/ZPublisher/HTTPRequest.py?rev=99866&view=markup

.. _resourceDirectory: http://apidoc.zope.org/++apidoc++/ZCML/http_co__sl__sl_namespaces.zope.org_sl_browser/resourceDirectory/index.html


Testing Layers
==============

Plone testing tool kits won't register layers for you, you have to do it
yourself somewhere in the boilerplate code::

    from zope.interface import directlyProvides

    directlyProvides(self.portal.REQUEST, IThemeLayer)

