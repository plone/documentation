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

Archetypes based content image scales is handled by `plone.namedfile <https://pypi.python.org/pypi/plone.namedfile>`_.

Dexterity based content image scales are handled by `plone.namedfile <https://pypi.python.org/pypi/plone.namedfile>`_.

Archetypes based content image scales is handled by `plone.app.imaging <https://plone.org/products/plone.app.imaging>`_.

Both packages offer the same traverseable `@@images` view which can be used from page templates and Python code
to provide different image scales for image fields on content.


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

In **Plone 4** this behavior comes from the monkey-patch applied by the
`plone.app.imaging <https://plone.org/products/plone.app.imaging>`_ package.


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

For Plone 4
-------------

`plone.app.imaging <https://plone.org/products/plone.app.imaging>`_ allows
you to configure available image scales in ``portal_properties`` ->
``imaging_properties``.

You can update these through-the-web or using :doc:`GenericSetup profile
</develop/addons/components/genericsetup>`.

``propertiestool.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_properties" meta_type="Plone Properties Tool">
     <object name="imaging_properties" meta_type="Plone Property Sheet">
      <property name="title">Image handling properties</property>
      <property name="allowed_sizes" type="lines">
       <element value="large 768:768"/>
       <element value="preview 400:400"/>
       <element value="mini 200:200"/>
       <element value="thumb 128:128"/>
       <element value="tile 64:64"/>
       <element value="icon 32:32"/>
       <element value="listing 16:16"/>

       <!-- Include our custom sizes here -->
       <element value="custom1 290:290"/>
       <element value="custom2 210:210"/>
       <element value="custom_210_189 210:189"/>
       <element value="custom_290_258 290:256"/>

      </property>
     </object>
    </object>

.. note ::

    For Plone 4, after adding new scales no batch processing of existing images
    are needed and new scales are created on-demand when the images are viewed
    for the first time.


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
