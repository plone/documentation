========================
Images in page templates
========================

.. admonition:: Description

    How to link to images in page templates in Plone.


Putting a static image into a page template
===========================================

Here is an example how to create an ``<img>`` tag in a ``.pt`` file:

.. code-block:: html

    <img tal:attributes="src string:${context/@@plone_portal_state/portal_url}/++resource++plonetheme.mfabrik/close-icon.png" alt="[ X ]"/>

Let's break this down:

* We are rendering an ``<img>`` tag.

* The ``src`` attribute is dynamically generated using a :term:`TALES`
  expression.

* We use *string comprehension* to create the ``src`` attribute.
  Alternatively we could use e.g. the ``python:`` :term:`TALES` expression
  type and embed one line python of code to generate the attribute value.

* We look up a helper view called :doc:`plone_portal_state </develop/plone/misc/context>`.
  This is a ``BrowserView`` shipped with Plone. Its purpose is to expose
  different helper methods to page templates and Python code.

* We call ``plone_portal_state``'s ``portal_url()`` method. This will return
  the root URL of our site.
  Note that this is not necessary the domain's top-level URL,
  as Plone sites can be nested in folders, or served on a path among
  unrelated web properties.

* We append our Zope 3 resource path to our site root URL (see below). This
  maps to some static media folder in our add-on files on the disk.

* There we point to ``close-icon.png`` image file.

* We also add the ``alt`` attribute of the ``<img>`` tag normally.
  It is not dynamically generated.

When the page template is generated, the following snippet could look like,
for example:

.. code-block:: html

    <img src="http://localhost:8080/mfabrik/++resource++plonetheme.mfabrik/logo.png" alt="[ X ]">

... or:

.. code-block:: html

    <img src="http://mfabrik.com/++resource++plonetheme.mfabrik/logo.png" alt="[ X ]">

... depending on the site virtual hosting configuration.

Relative image look-ups
-----------------------

.. warning::

    Never create relative image look-ups without prefixing the image source
    URL with the site root.

Hardcoded relative image path might seem to work:

.. code-block:: html

    <img src="++resource++plonetheme.mfabrik/logo.png" >

... but this causes a different image *base URL* to be used on every page.
The image URLs, from the browser point of view, would be:

.. code-block:: html

    <img src="http://yoursite/++resource++plonetheme.mfabrik/logo.png" >

... and then in another folder:

.. code-block:: html

    <img src="http://yoursite/folder/++resource++plonetheme.mfabrik/logo.png" >

... which **prevents the browser from caching the image**.

Registering static media folders in your add-on product
=======================================================

Zope 3 resource directory
-------------------------

The right way to put in a static image is to use a Zope 3 resource
directory.

* Create folder ``yourcompany.product/yourcompany/product/browser/static``.

* Add the following :term:`ZCML` to
  ``yourcompany.product/yourcompany/product/browser/configure.zcml``.

.. code-block:: xml

    <browser:resourceDirectory
        name="yourcompany.product"
        directory="static"
        layer=".interfaces.IThemeSpecific"
        />

This will be picked up at the ``++resource++yourcompany.product/`` static
media path.

Layer is optional: the static media path is available only
when your add-on product is installed if the
:doc:`layer </develop/plone/views/layers>` is specified.

Also see :doc:`Resource folders </adapt-and-extend/theming/templates_css/resourcefolders>`


Rendering Image content items
=============================

You can refer to ``ATImage`` object's content data download by adding
``/image`` to the URL:

.. code-block:: html

    <img alt="" tal:attributes="src string:${context/getImage/absolute_url}/image" />

The magic is done in the ``__bobo_traverse__`` method of ``ATImage`` by
providing traversable hooks to access image download:

* https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/image.py

Rendering ``ImageField``
========================

Archetypes's ``ImageField`` maps its data to the content object at attribute
which is the field's name.
If you have a field ``campaignVideoThumbnail`` you can generate an image tag
as follows:

.. code-block:: html

    <img class="thumbnail" tal:attributes="src string:${campaign/absolute_url}/campaignVideoThumbnail" alt="Campaign video" />

If you need more complex ``<img>`` output,
create a helper function in your ``BrowserView`` and use Python code
to perform the ``ImageField`` manipulation.

See ``ImageField`` for more information:

* https://github.com/plone/Products.Archetypes/blob/master/Products/Archetypes/Field.py

``tag()`` method
================

.. note::

    Using ``tag()`` is discouraged. Create your image tags manually.

Some content provides a handy ``tag()`` method to generate
``<img src="" />`` tags
with different image sizes.

``tag()`` is available on

* Archetypes ``ImageField``

* ``ATNewsItem``

* ``ATImage``

* ``FSImage`` (Zope 2 image object on the file-system)

``tag()`` is defined in `OFS.Image <http://svn.zope.org/Zope/trunk/src/OFS/Image.py?rev=96262&view=auto>`_.

Scaling images
--------------

``tag()`` supports scaling. Scale sizes are predefined.
When an ``ATImage`` is uploaded,
various scaled versions of it are stored in the database.

Displaying a version of the image using the "preview" scale::

	image.tag(scale="preview", alt="foobar text")

This will generate:

.. code-block:: html

	<img src="http://something/folder/image/image_preview" alt="foobar text" />

.. note::

	If you are not using the ``alt`` attribute, you should set it to an
	empty string: ``alt=""``. Otherwise screen readers will read
	the ``src`` attribute of the ``<img>`` tag aloud.

In order to simplify accessing these image scales, use
`archetypes.fieldtraverser <https://pypi.python.org/pypi/archetypes.fieldtraverser>`_.
This package allows you to traverse to the stored image scales while still
using ``AnnotationStorage`` and is a lot simpler to get going (in the
author's humble opinion :).

Default scale names and sizes are defined in ``ImageField`` declaration for
custom ``ImageField``\s.
For ``ATImage``, those are in
`Products.ATContentTypes.content.image
<https://github.com/plone/Products.ATContentTypes/blob/master/Products/ATContentTypes/content/image.py>`_.

Lightbox style image pop-ups
============================

Plone comes with `plone.app.jquerytools <https://pypi.python.org/pypi/plone.app.jquerytools>`_ which offers easy integration
for lightbox style image pop-ups.

You can use Plone standard image content type, defining scales using `plone.app.imaging <https://github.com/plone/plone.app.imaging/>`_
or you can define image fields in your schema.

In the example below we define custom image fields in Archetypes schema.

contenttype.py::

    atapi.ImageField(
        'imageTwo',
        widget=atapi.ImageWidget(
            label=_(u"Kuva #2"),
        ),
        validators=('isNonEmptyFile'),
        languageIndependent=True,
        sizes={
               'thumb': (90, 90),
               'large': (768, 768),
        },
    ),

    atapi.ImageField(
        'imageThree',
        widget=atapi.ImageWidget(
            label=_(u"Kuva #3"),
        ),
        validators=('isNonEmptyFile'),
        languageIndependent=True,
        sizes={
               'thumb': (90, 90),
               'large': (768, 768),
        },
    ),

Related view page template file

.. code-block:: html

        <div class="product-all-images">

            <img class="product-image-preview" tal:condition="context/getImageTwo" tal:attributes="src string:${context/absolute_url}/@@images/imageTwo/thumb" alt="" />

            <img class="product-image-preview" tal:condition="context/getImageThree" alt="" tal:attributes="src string:${context/absolute_url}/@@images/imageThree/thumb" />

        </div>

And then we activate all this in a JavaScript using ``prepOverlay()`` from ``plone.app.jquerytools``

.. code-block:: javascript


     /*global window,document*/

    (function($) {

        "use strict";

        /**
         * Make images clickable and open a bigger version of the image when clicked
         */
        function prepareProductImagePreviews() {

            // https://pypi.python.org/pypi/plone.app.jquerytools/1.4#examples
            $('.product-image-preview')
            .prepOverlay({
                subtype: 'image',
                urlmatch: 'thumb',
                urlreplace: 'large'
                });
            }

        $(document).ready(function() {
            prepareProductImagePreviews();
        });

    })(jQuery);

Rotating banners
------------------

Simple rotating banneres can be done with `jQuery Cycle plug-in (lite) <http://jquery.malsup.com/cycle/>`_.

Example TAL code... render list of content items and extract one image from each of them

.. code-block:: html

    <dd class="cycle">

        <tal:hl repeat="obj view/obj">
            <a tal:attributes="href python:view.getLink(obj); title python:view.getAltText(obj)" class="outer-wrapper">
                <img tal:attributes="src python:view.getImageURL(obj)" />
            </a>
        </tal:hl>

    </dd>

Then use the the following JavaScript to boostrap the cycling

.. code-block:: javascript

    (function($) {

        "use strict";

        function rotateBanners() {
            $(".cycle").cycle();
        }

        $(document).ready(function() {
            rotateBanners();
        });

    })(jQuery);

You need to have this snippet and ``jquery.cycle.light.js`` in your portal_javascripts registry.

You also may need to set pixel height for ``cycle`` elements, as they use absolute
positioning making the element take otherwise 0 pixel of height.


