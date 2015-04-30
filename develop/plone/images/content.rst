=====================
 Image-like content
=====================

.. admonition:: Description

    How to programmatically manipulate images on your Plone site.

.. contents :: :local:

Introduction
============

Plone supports image content in two forms:

* As stand-alone content type, images will be visible in the sitemap. This is
  the case for the default ``Image`` content type, but you can create custom
  content types with similar properties.

* As a field, the image is directly associated with one content object.  Use
  ``Archetypes.fields.ImageField``.


Custom image content type
==========================

If you want to have your custom content type behave like the stock Plone ``Image``
content type:

* Inherit from the content class ``Products.ATContentType.content.image.ATImage``
  and use the schema from that class.

* When writing the ``GenericSetup`` XML of your type, follow the example of `Image.xml <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/profiles/default/types/Image.xml>`_.

* Do not set workflow for your type in ``profiles/default/workflows.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_workflow" meta_type="Plone Workflow Tool">

     <bindings>
      <type type_id="YourImageType"/>
     </bindings>
    </object>


Image scales
============

When the image is uploaded, both field or content, Plone creates scaled-down
versions from it by default.

These are configured using the ``ImageField`` *``sizes``* parameter. See the
``ImageField`` class notes here:

* https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/Field.py

The default image scales for ``Image`` content are configured in:

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/image.py

Configuration::

    sizes= {'large':   (768, 768),
            'preview': (400, 400),
            'mini':    (200, 200),
            'thumb':   (128, 128),
            'tile':    (64, 64),
            'icon':    (32, 32),
            'listing': (16, 16),
           },

More info:

* http://plone.293351.n2.nabble.com/Register-browser-view-for-image-scales-tp5626267p5626267.html

``getScale()``
--------------

``ImageField`` provides a ``getScale()`` method to get the scaled version of
the image based on the ``sizes`` configuration key.

See example in ``__bobo_traverse__``:

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/image.py


Accessing images
================

``ImageField`` is mapped to a traversable attribute of your content type.
E.g. if your content object has a field ``imageOne`` and is found at this URL::

    http://yoursite/content

the image can be directly downloaded from::

    http://yoursite/content/imageOne


Scaled versions for Image content (``ATImage``)
------------------------------------------------

If you want different scales you can add ``image_XXX`` prefix where ``XXX`` is
the corresponding scale name::

    http://yoursite/content/imageOne/image_preview

In **Plone 3** this hook is defined in ``__bobo_traverse__`` in ``ATImage`` class:
* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/image.py


``portal_catalog`` and images
==============================

Do not index image objects themselves, as adding image data to the
``portal_catalog`` brain objects would greatly increase their site and make
brain look-up slow.

Instead, index only image paths using :doc:`getPhysicalPath() </develop/plone/serving/traversing>`.
When you need to display image using metadata columns, you can generate the image
URL manually. Then, the image object will be woken up when the browser makes a
HTTP request for the image.


Custom image scales and recreating scale data
=============================================

Below is an example showing how to make custom image scales available in your
Plone site.

* Monkey-patch ``ATImages`` to have new scale versions available.

* Have migration code which will run all through all ``ATImage`` content on the
  site and recreate their scale versions, thus populating image scale data for
  new scale versions also.

* The new sizes are automatically effected to rich text editor image sizes
  options (active WYSIWYG editor on Plone site)

``images.py``::

    """ Add alternative image sizes to default ATImage scales.
        NOTE: This does not effect available user interface options in the visual editor etc.
    """

    import transaction
    from zope.app.component.hooks import setHooks, setSite, getSite

    from Products.Five.browser import BrowserView

    from Products.ATContentTypes.content.image import ATImage
    from Products.ATContentTypes.interface.image import IATImage

    # Monkeypatch our new image sizes to be available in ATImage default scales.
    # This will also affect the "image sizes" option in the WYSIWYG text editor.
    ATImage.schema["image"].sizes.update({
        "custom1": (290, 290),
        "custom2": (210, 210),
        "custom_210_189": (210, 189),
        "custom_290_258": (290, 258),
    })

    class RescaleImages(BrowserView):
        """ Migration view to recreate all image scale versions on all Image content types on the site.

        To trigger this migration code, enter the view URL manually in the browser address bar::

            http://yourhost/site/@@rescale_images

        We assume that you are running Zope in the foreground, monitoring the console for messages.

        This code is designed to work with sites with plenty of images.
        Tested with > 5000 images.

        Note that you need to run this rescale code only once to migrate the existing image content.
        New images will have custom scale versions available when the images are created.
        """

        def __call__(self):
            """ View processing entry point.
            """

            portal = getSite()

            # Iterate through all Image content items on the site
            all_images = portal.portal_catalog(show_inactive=True, language="ALL", object_provides=IATImage.__identifier__)

            done = 0

            for brain in all_images:
                content = brain.getObject()

                # Access schema in Plone 4 / archetypes.schemaextender compatible way
                schema = content.Schema()

                # This will trigger ImageField scale rebuild
                if "image" in schema:
                    schema["image"].createScales(content)
                else:
                    print "Has bad ATImage schema:" + content.absolute_url()

                # Since this is a HUGE operation (think of resizing 2 GB images)
                # it is not a good idea to buffer the transaction in memory
                # (Zope default behavior).
                # Using subtransactions we hint Zope when it would be a good
                # time to buffer the changes on disk.
                # http://www.zodb.org/documentation/guide/transactions.html
                if done % 10 == 0:
                    # Commit subtransaction for every 10th processed item
                    transaction.commit(True)

                done += 1
                print "(%d / %d) created scales for image: %s" % (done, len(all_images), "/".join(content.getPhysicalPath()))

            # Final commit
            transaction.commit()

            # Note that when entire transaction is committed, there will be a
            # huuuge delay before the message below is returned to the browser.
            # This is because Zope is busy updating the ZODB storage.

            # Make simple HTTP 200 answer
            return "Recreated image scales for %d images" % len(all_images)


``configure.zcml``

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:browser="http://namespaces.zope.org/browser"
        >
        <browser:page
            for="*"
            name="rescale_images"
            permission="cmf.ManagePortal"
            class=".images.RescaleImages"
            />
    </configure>

Automatic image scales on ReferenceFields
--------------------------------------------

Python code::

     from zope.component import adapts
     from zope.interface import implements, Interface
     from plone.app.imaging.interfaces import IImageScaleHandler


     def dereference(func_name):
         def new_func(self, instance, *args, **kw):
             if self.context is None:
                 instance = self.reference_field.get(instance)
                 self.context = instance.getPrimaryField()
             handler = IImageScaleHandler(self.context)
             func = getattr(handler, func_name)
             return func(instance, *args, **kw)
         return new_func


     class IReferenceField(Interface):
         """ marker """

     class ReferencedImageScaleHandler(object):
         """ proxy the standard image scale handler so that it operates on a referenced image """
         implements(IImageScaleHandler)
         adapts(IReferenceField)

         def __init__(self, context):
             self.reference_field = context
             self.context = None

         getScale = dereference('getScale')
         createScale = dereference('createScale')
         retrieveScale = dereference('retrieveScale')
    storeScale = dereference('storeScale')


in configure.zcml::


    <class class="Products.Archetypes.Field.ReferenceField">
      <implements interface=".IReferenceField"/>
    </class>

    <adapter
        factory=".ReferencedImageScaleHandler" />
