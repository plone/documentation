===================
 Image-like content
===================

.. admonition:: Description

    How to programmatically manipulate images on your Plone site.


Introduction
============

Plone supports image content in several forms:

stand-alone content type
    As stand-alone content type, images will be visible in the sitemap (configurable via the Navigation control panel).
    This is the case for the default ``Image`` content type, but you can create custom content types with similar properties.

image field
    As a field, the image is directly associated with one content object.
    Use ``plone.namedfile.field.namedfile.NamedBlobImage``:

    .. code-block:: python

        custom_image = NamedBlobImage(
            title=_(u'label_customimage', default=u'Custom Image'),
            description=_(u'help_customimage', default=u''),
            required=False,
        )


behavior using an image field
    The ``plone.leadimage`` behavior in ``plone.app.contenttypes.behaviors.leadimage`` provides a field called ``leadimage``.
    Custom behaviors like this can be created too.


Custom image content type
==========================

If you want to have your custom content type behave like the stock Plone ``Image`` content type:

* Inherit from the content class ``plone.app.contenttype.content.Image`` and use the XML schema from that class.

* When writing the ``GenericSetup`` XML of your type,
  follow the example of `Image.xml <https://github.com/plone/plone.app.contenttypes/blob/master/plone/app/contenttypes/profiles/default/types/Image.xml>`_.

* Do not set workflow for your type in ``profiles/default/workflows.xml``.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="portal_workflow" meta_type="Plone Workflow Tool">

     <bindings>
      <type type_id="YourImageType"/>
     </bindings>
    </object>


Accessing images
================

Both Dexterity and Archetypes offer the same traversable ``@@images`` view.
It can be used from page templates and Python code to provide access to the image and different image scales for image fields on content.

The code for image access and scales for Dexterity based content is handled by `plone.namedfile <https://pypi.python.org/pypi/plone.namedfile>`_. Old Archetypes based content image scales is handled by `plone.app.imaging <https://plone.org/products/plone.app.imaging>`_.


Using direct URLs
-----------------

If your image field is a primary field, such as for the default ``Image`` content type,
you access the image by calling the URL without specifying a view::

    http://yoursite/imagecontent

The generic way to access any image on your content is an URL like so::

    http://yoursite/imagecontent/@@images/FIELDNAME

Predefined image scales from the configuration registry settings are accessed this way::

    http://yoursite/imagecontent/@@images/FIELDNAME/SCALENAME

You might find URLs of custom (on-the-fly) image scales accessed this way (see below)::

    http://yoursite/imagecontent/@@images/FIELDNAME/CUSTOM_SCALE_UID.jpg

Example 1,
show the original image from the ``plone.leadimage`` behavior::

    http://yoursite/imagecontent/@@images/leadimage

Example 2,
show the scale ``mini`` from the field ``custom_image``::

    http://yoursite/imagecontent/@@images/custom_image/mini

Determining the image scales available
--------------------------------------

To find out or change which image scales are available in a particular Plone site, go to the Image Handling control panel.

.. figure:: /_static/image_handling_control_panel.png
   :align: center
   :alt: the Image Handling control panel

You can also use the Configuration Registry control panel and filter by ``allowed_sizes``. The value of the ``plone.allowed_sizes`` registry entry will be something like ``[u'high 1400:1400', u'large 768:768', u'preview 400:400', u'mini 200:200', u'thumb 128:128', u'tile 64:64', u'icon 32:32', u'listing 16:16']``, so your available scales will be ``high``, ``large``, ``preview``, ``mini``, ``thumb``, ``tile``, ``icon``, and ``listing``.

Access by creating tags programmatically
----------------------------------------

In code a lookup of the ``images`` multi-adapter is needed.
It implements the ``plone.app.imaging.interfaces.IImageScaling`` interface, thus it provides:

``scale(fieldname=None, scalename=None, **parameters)``
    Retrieve a scale based on the given name or set of parameters.
    The parameters can be anything supported by `scaleImage` and would usually consist of at least a width & height.

    Returns either an object implementing `IImageScale` or `None`

``tag(fieldname=None, scalename=None, **parameters)``
    Like ``scale`` but returns a tag for a scale.

``getAvailableSizes(fieldname=None)``
    returns a dictionary of scale name => (width, height)

``getImageSize(fieldname=None)``
    returns the original image size, a tuple of (width, height)

``getInfo(fieldname=None, scalename=None, **parameters)``
    returns metadata for the requested scale from the storage

``images`` is in fact a view (a multi-adapter between context and request),
we can use ``plone.api.content.get_view`` for lookup:

.. code-block:: python

    from plone import api

    ...

    scale_util = api.content.get_view('images', context, request)
    tag = scale_util.tag('leadimage', 'mini')


Creating Scales
===============

Named scales
------------

In the Plone Control Panel under ``Image Handling`` images scales can be defined (and redefined).
Those scales are stored in the configuration registry.
In a custom GenericSetup profile additional scales can be added by adding some lines to ``registry.xml`` like so:

.. code-block:: xml

    <?xml version="1.0"?>
    <registry>
      <records
          interface="Products.CMFPlone.interfaces.controlpanel.IImagingSchema"
          prefix="plone">
        <value key="allowed_sizes" purge="false">
          <element>custom_4to3 400:300</element>
          <element>custom_3to4 300:400</element>
        </value>
      </records>
      ...
    </registry>

A scale has the format ``NAME WIDTH:HEIGHT``.
A width or height set to zero ``0`` means to scale this side dynamically,
i.e. ``300:0`` scales an image to a width of 300 and a height according to its aspect ratio with no cropping.


Scales On-The-Fly
-----------------

Sometimes scales need to be created on-the-fly.
This can be done programmatically only.
In order to create scale on the fly the ``images`` multi-adapter is used.

The methods ``scale``, ``tag`` or ``getInfo`` can be used to create a scale.

In order to create a custom scale skip the ``scalename`` parameter and use ``height`` and ``width`` parameters.

Optional choose the ``direction`` parameter:

up
    Scaling scales the smallest dimension up to the required size and scrops the other dimension if needed.

down
    Scaling starts by scaling the largest dimension to the required size and scrops the other dimension if needed.

thumbnail
    scales to the requested dimensions without cropping.
    The resulting image may have a different size than requested.
    This option requires both width and height to be specified.
    `keep` is accepted as  an alternative spelling for this option, but its use is deprecated.

Example, scale down (crop) to 300x200:

.. code-block:: python

    from plone import api

    ...

    scale_util = api.content.get_view('images', context, request)
    tag = scale_util.tag('leadimage', width=300, height=200, direction='down')

Attention: The generated URL is based on a generated UID which points to the current scaled down version of the image.
After modification of the content type the scale is not updated,
but a new URL to the new scale will be generated.
But the generated UID will be reused for the same upload, so one version is scaled only once.


``portal_catalog`` and images
==============================

Never index image objects or store them as metadata,
as adding image data to the ``portal_catalog`` brain objects would greatly increase their site and make brain look-up slow.

Instead recreate the path of the image

Or if you have custom scales not available in configuration,
index only image paths with ths scale information using :doc:`getPhysicalPath() </develop/plone/serving/traversing>`.

Addons
======

Manual croppings can be choosen by using `plone.app.imagecropping <https://pypi.python.org/pypi/plone.app.imagecropping>`_
