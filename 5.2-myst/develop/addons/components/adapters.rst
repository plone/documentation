========
Adapters
========


Introduction
============

Adapters make it possible to extend the behavior of a class without
modifying the class itself. This allows more modular, readable code in
complex systems where there might be hundreds of methods per class. Some
more advantages of this concept are:

* The class interface itself is more readable (less visible clutter);
* class functionality can be extended outside the class source code;
* add-on products may extend or override parts of the class functionality.
  Frameworks use adapters extensively, because adapters provide easy
  integration
  points.  External code can override adapters to retrofit/modify
  functionality. For example: a theme product might want to override a
  searchbox viewlet to have a search box with slightly different
  functionality and theme-specific goodies.

The downside is that adapters cannot be found by "exploring" classes or
source code. They must be well documented in order to be discoverable.

Read more about adapters in the
`zope.component README <http://docs.zope.org/zope.component/narr.html#adapters>`_.

`Adapter ZCML <http://docs.zope.org/zope.component/zcml.html#adapter>`_.

Adapters are matched by:

* Provider interface (what functionality adapter provides).
* Parameter interfaces.

There are two kinds of adapters:

* Normal adapters that take only one parameter.
* Multi-adapters take many parameters in the form of a tuple.

Example adapters users
-----------------------

* `Theme specific adapters <http://docs.plone.org/4/en/old-reference-manuals/plone_3_theming/buildingblocks/components/themespecific.html>`_

Registering an adapter
======================

Registering using ZCML
---------------------------

An adapter provides functionality to a class. This functionality becomes
available when the interface is queried from the instance of class.

Below is an example how to make a custom "image provider". The image
provider provides a list of images for arbitrary content.

This is the image provider interface::

    from zope.interface import Interface

    class IProductImageProvider(Interface):

        def getImages(self):
            """ Get Images associated with the product.

            @return: iterable of Image objects
            """

This is our content class::

    class MyShoppableItemType(folder.ATFolder):
        """ Buyable physical good with variants of title and price and multiple images
        """
        implements(IVariantProduct)

        meta_type = "VariantProduct"
        schema = VariantProductSchema

This is the adapter for the content class::

    import zope.interface

    from getpaid.variantsproduct.interfaces.multiimageproduct import IProductImageProvider

    class FolderishProductImageProvider(object):
        """ Mix-in class which provide product image management functions.

        Assume the content itself is a folderish archetype content type and
        all contained image objects are product images.
        """

        zope.interface.implements(IProductImageProvider)

        def __init__(self, context):
            # Each adapter takes the object itself as the construction
            # parameter and possibly provides other parameters for the
            # interface adaption
            self.context = context

        def getImages(self):
            """ Return a sequence of images.

            Perform folder listing and filter image content from it.
            """

            images = self.context.listFolderContents(
                            contentFilter={"portal_type" : "Image"})
            return images

Register the adapter for your custom content type ``MyShoppableItemType`` in
the ``configure.zcml`` file of your product:

.. code-block:: xml

    <adapter
        for=".shop.MyShoppableItemType"
        provides=".interfaces.IProductImageProvider"
        factory=".images.FolderishProductImageProvider"
        />

Then we can query the adapter and use it. Unit testing example::

    def test_get_images(self):
        self.loginAsPortalOwner()
        self.portal.invokeFactory("MyShoppableItemType", "product")
        product = self.portal.product
        image_provider = IProductImageProvider(product)
        images = image_provider.getImages()

        # Not yet any uploaded images
        self.assertEqual(len(images), 0)


Registering using Python
---------------------------

Register to *Global Site Manager* using ``registerAdapter()``.

Example::

    from zope.component import getGlobalSiteManager

    layer = klass.layer

    gsm = getGlobalSiteManager()
    gsm.registerAdapter(factory=MyClass, required=(layer,),
                        name=klass.__name__, provided=IWidgetDemo)
    return klass

More info

* http://www.muthukadan.net/docs/zca.html#registration

Generic adapter contexts
------------------------

The following interfaces are useful when registering adapters:

``zope.interface.Interface``
    Adapts to any object

``Products.CMFCore.interfaces.IContentish``
    Adapts to any Plone content object

``zope.publisher.interfaces.IBrowserView``
    Adapts to any ``BrowserView(context, request)`` object

Multi-adapter registration
---------------------------

You can specify any number of interfaces in the ``<adapter for="" />``
attribute. Separate them with spaces or newlines.

Below is a view-like example which registers against:

* any context (``zope.interface.Interace``);
* HTTP request objects (``zope.publisher.interfaces.browser.IBrowserRequest``).

Emulate view registration (context, request):

.. code-block:: xml

    <adapter
        for="zope.interface.Interface
             zope.publisher.interfaces.browser.IBrowserRequest"
        provides="gomobile.mobile.interfaces.IMobileTracker"
        factory=".bango.BangoTracker"
        />

Getting the adapter
===================

There are two functions that may be used to get an adapter:

* ``zope.component.getAdapter`` will raise an exception if the adapter is
  not found.

* ``zope.component.queryAdapter`` will return ``None`` if the adapter is not
  found.

``getAdapter``/``queryAdapter`` arguments:

# Tuple consisting of: (*Object implementing the first interface*,
  *object implementing the second interface*, ...)
  The interfaces are in the order in which they were declared in the
  ``<adapter for="">`` attribute.

# Adapter marker interface.

Example registration:

.. code-block:: xml

    <!-- Register header animation picking logic - override this for your custom logic -->
    <adapter
        provides="plone.app.headeranimation.interfaces.IHeaderAnimationPicker"
        for="plone.app.headeranimation.behaviors.IHeaderBehavior
             Products.CMFCore.interfaces.IContentish
             zope.publisher.interfaces.browser.IBrowserRequest"
        factory=".picker.RandomHeaderAnimationPicker"
        />


Corresponding query code, to look up an adapter implementing the interfaces::

    from zope.component import getUtility, getAdapter, getMultiAdapter

    # header implements IHeaderBehavior
    # doc implements Products.CMFCore.interfaces.IContentish
    # request implements zope.publisher.interfaces.browser.IBrowserRequest

    from Products.CMFCore.interfaces import IContentish
    from zope.publisher.interfaces.browser import IBrowserRequest

    self.assertTrue(IHeaderBehavior.providedBy(header))
    self.assertTrue(IContentish.providedBy(doc))
    self.assertTrue(IBrowserRequest.providedBy(self.portal.REQUEST))

    # Throws exception if not found
    picker = getMultiAdapter((header, doc, self.portal.REQUEST), IHeaderAnimationPicker)

.. note::

    You cannot get adapters on module-level code during import, as the Zope
    Component Architecture is not yet initialized.


Listing adapter registers
=========================

The following code checks whether the ``IHeaderBehavior`` adapter is
registered correctly::

    from zope.component import getGlobalSiteManager
    sm = getGlobalSiteManager()

    registrations = [a for a in sm.registeredAdapters() if a.provided == IHeaderBehavior ]
    self.assertEqual(len(registrations), 1)


Alternative listing adapters
----------------------------

Getting all multi-adapters (context, request)::

    from zope.component import getAdapters
    adapters = getAdapters((context, request), provided=Interface)

.. warning::

    This does not list locally-registered adapters such as Zope views.


Local adapters
==============

Local adapters are effective only inside a certain container, such as a
folder.  They use ``five.localsitemanager`` to register themselves.

* https://opkode.com/blog/2010/01/26/schema-extending-an-object-only-inside-a-specific-folder/


