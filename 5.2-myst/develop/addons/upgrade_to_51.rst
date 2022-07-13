====================================
Upgrade A Custom Add-on To Plone 5.1
====================================


.. _addon_installation_code:

Installation Code
=================

See `PLIP 1340 <https://github.com/plone/Products.CMFPlone/issues/1340>`_ for a discussion of this change.


From CMFQuickInstallerTool To GenericSetup
------------------------------------------

The add-ons control panel in Plone 5.1 no longer supports installation or uninstallation code
in ``Extensions/install.py`` or  ``Extensions/Install.py``.

If you have such code, you must switch to a GenericSetup profile.

GenericSetup is already the preferred way of writing installation code since Plone 3.
If you must use the old way, you can still use the ``portal_quickinstaller`` in the Management Interface.

In a lot of cases, you can configure ``xml`` files instead of using Python code.
In other cases you may need to write custom installer code (setuphandlers.py).

See the :doc:`GenericSetup documentation </develop/addons/components/genericsetup>`.


Default Profile
---------------

Historically, when your add-on had multiple profiles,their names would be sorted alphabetically
and the first one would be taken as the installation profile.

It was always recommended to use ``default`` as name of this first profile.

Since Plone 5.1, when there is a ``default`` profile, it is always used as the installation profile,
regardless of other profile names.

Exception: when this ``default`` profile is marked in an ``INonInstallable`` utility,
it is ignored and Plone falls back to using the first from the alphabetical sorting.


Uninstall
---------

An uninstall profile is not required, but it is highly recommended.

Until Plone 5.0 the CMFQuickInstallerTool used to do an automatic partial cleanup,
for example removing added skins and CSS resources.

This was always only partial, so you could not rely on it to fully cleanup the site.

Since Plone 5.1 this cleanup is no longer done.
Best practice is to create an uninstall profile for all your packages.

If you were relying on this automatic cleanup, you need to add extra files to clean it up yourself.

You need to do that when your default profile contains one of these files:

- ``actions.xml``
- ``componentregistry.xml``
- ``contenttyperegistry.xml``.
  This seems rarely used.

.. note::

   The `contenttyperegistry import step <https://github.com/zopefoundation/Products.CMFCore/blob/2.2.10/Products/CMFCore/exportimport/contenttyperegistry.py#L73>`_ only supports adding, not removing.

   You may need to improve that code based on the old `CMFQuickInstallerTool code <https://github.com/plone/Products.CMFQuickInstallerTool/blob/3.0.13/Products/CMFQuickInstallerTool/InstalledProduct.py#L364>`_.

- ``cssregistry.xml``
- ``jsregistry.xml``
- ``skins.xml``
- ``toolset.xml``
- ``types.xml``
- ``workflows.xml``

When there is no uninstall profile, the add-ons control panel will give a warning.
An uninstall profile is a profile that is registered with the name ``uninstall``.

See https://github.com/plone/plone.app.multilingual/tree/master/src/plone/app/multilingual/profiles/uninstall


Do Not Use portal_quickinstaller
--------------------------------

Old code:

.. code-block:: python

    qi = getToolByName(self.context, name='portal_quickinstaller')

or:

.. code-block:: python

    qi = self.context.portal_quickinstaller

or:

.. code-block:: python

    qi = getattr(self.context, 'portal_quickinstaller')

or:

.. code-block:: python

    qi = getUtility(IQuickInstallerTool)

New code:

.. code-block:: python

    from Products.CMFPlone.utils import get_installer
    qi = get_installer(self.context, self.request)

or if you do not have a request:

.. code-block:: python

    qi = get_installer(self.context)

Alternatively, since it is a browser view, you can get it like this:

.. code-block:: python

    qi = getMultiAdapter((self.context, self.request), name='installer')

or with ``plone.api``:

.. code-block:: python

    from plone import api
    api.content.get_view(
        name='installer',
        context=self.context,
        request=self.request)

If you need it in a page template:

.. code-block:: python

   tal:define="qi context/@@installer"

.. warning::

   Since the code really does different things than before,
   the method names were changed and they may accept less arguments or differently named arguments.


Products Namespace
------------------

There used to be special handling for the Products namespace.
Not anymore.

Old code:

.. code-block:: python

    qi.installProduct('CMFPlacefulWorkflow')

New code:

.. code-block:: python

    qi.install_product('Products.CMFPlacefulWorkflow')


isProductInstalled
------------------

Old code:

.. code-block:: python

    qi.isProductInstalled(product_name)

New code:

.. code-block:: python

    qi.is_product_installed(product_name)


installProduct
--------------

Old code:

.. code-block:: python

    qi.installProduct(product_name)

New code:

.. code-block:: python

    qi.install_product(product_name)

.. note::


   No keyword arguments are accepted.


installProducts
---------------

This was removed.
You should iterate over a list of products instead.

Old code:

.. code-block:: python

    product_list = ['package.one', 'package.two']
    qi.installProducts(product_list)

New code:

.. code-block:: python

    product_list = ['package.one', 'package.two']
    for product_name in product_list:
       qi.install_product(product_name)


uninstallProducts
-----------------

Old code:

.. code-block:: python

    qi.uninstallProducts([product_name])

New code:

.. code-block:: python

    qi.uninstall_product(product_name)

Note that we only support passing one product name.
If you want to uninstall multiple products, you must call this method multiple times.


reinstallProducts
-----------------

This was removed.
Reinstalling is usually not a good idea: you should use an upgrade step instead.
If you need to, you can uninstall and install if you want.


getLatestUpgradeStep
--------------------

Old code:

.. code-block:: python

    qi.getLatestUpgradeStep(profile_id)

New code:

.. code-block:: python

    qi.get_latest_upgrade_step(profile_id)


upgradeProduct
--------------

Old code:

.. code-block:: python

    qi.upgradeProduct(product_id)

New code:

.. code-block:: python

    qi.upgrade_product(product_id)


isDevelopmentMode
-----------------

This was a helper method that had got nothing to with the quick installer.

Old code:

.. code-block:: python

    qi = getToolByName(aq_inner(self.context), 'portal_quickinstaller')
    return qi.isDevelopmentMode()

New code:

.. code-block:: python

    from Globals import DevelopmentMode
    return bool(DevelopmentMode)

.. note::

   The new code works already since Plone 4.3.


All Deprecated Methods
----------------------

Some of these were mentioned already.

Some methods are no longer supported.
These methods are still there, but they do nothing:

- ``listInstallableProducts``

- ``listInstalledProducts``

- ``getProductFile``

- ``getProductReadme``

- ``notifyInstalled``

- ``reinstallProducts``

Some methods have been renamed.
The old method names are kept for backwards compatibility.
They do roughly the same as before, but there are differences.
And all keyword arguments are ignored.
You should switch to the new methods instead:

- ``isProductInstalled``, use ``is_product_installed`` instead

- ``isProductInstallable``, use ``is_product_installable`` instead

- ``isProductAvailable``, use ``is_product_installable`` instead

- ``getProductVersion``, use ``get_product_version`` instead

- ``upgradeProduct``, use ``upgrade_product`` instead

- ``installProducts``, use ``install_product`` with a single product instead

- ``installProduct``, use ``install_product`` instead

- ``uninstallProducts``, use ``uninstall_product`` with a single product instead.


INonInstallable
---------------

There used to be one ``INonInstallable`` interface in ``CMFPlone`` (for hiding profiles) and
another one in ``CMFQuickInstallerTool`` (for hiding products).

In the new situation, these are combined in the one from CMFPlone.

Sample usage:

In configure.zcml:

.. code-block:: xml

    <utility factory=".setuphandlers.NonInstallable"
        name="your.package" />

In setuphandlers.py:

.. code-block:: python

    from Products.CMFPlone.interfaces import INonInstallable
    from zope.interface import implementer

    @implementer(INonInstallable)
    class NonInstallable(object):

        def getNonInstallableProducts(self):
            # (This used to be in CMFQuickInstallerTool.)
            # Make sure this package does not show up in the add-ons
            # control panel:
            return ['collective.hidden.package']

        def getNonInstallableProfiles(self):
            # (This was already in CMFPlone.)
            # Hide the base profile from your.package from the list
            # shown at site creation.
            return ['your.package:base']

When you do not need them both, you can let the other return an empty list, or you can leave that method out completely.

.. note::

    If you need to support older Plone versions at the same time, you can let your class implement the old interface as well:

    .. code-block:: python

        from Products.CMFQuickInstallerTool.interfaces import (
            INonInstallable as INonInstallableProducts)

        @implementer(INonInstallableProducts)
        @implementer(INonInstallable)
        class NonInstallable(object):
            ...

.. _content-type-icons-changed:

Content Type Icons
==================

Since Plone 3 there have been several breaking changes relating to content type icon rendering.

**Plone 3**

Content type icons where rendered as HTML tags, which were rendered with methods from plone.app.layout.icon ...:

.. code-block:: html

   <span class="contenttype-document summary">
          <img width="16" height="16" src="http://192.168.1.230:8322/Plone/document_icon.gif" alt="Page">
          <a href="http://192.168.1.230:8322/Plone/front-page" class="state-published url">Welcome to Plone</a>
   </span>


.. note::

    Related code in plone.app.layout  (especially `getIcon()` and  `IContentIcon`) and other locations was
    more then deprecated - it is obsolete and confusing and is getting removed.

    The catalog metadata item getIcon used to be a string containing the file name of the appropriate icon (unused since Plone 4).

    Since Plone 5.02 the catalog metadata item **getIcon** is reused for another purpose.
    Now it is boolean and it is set to `True` for items which are images or have an image property (e.g. a lead image).



**Plone 4**

Content type icons are rendered as background images using a sprite image and css:

.. code-block:: html

   <span class="summary">
         <a href="http://192.168.1.230:8412/Plone/front-page" class="contenttype-document state-published url">Welcome to Plone</a>
   </span>

   .icons-on .contenttype-document {
       background: no-repeat transparent 0px 4px url(contenttypes-sprite.png);

**Plone 5**

Content type icons are rendered as `fontello fonts <http://fontello.com/>`_ using css elements *before* or *after*.

.. code-block:: html

   <span class="summary" title="Document">
        <a href="http://192.168.1.230:8082/Plone/front-page"
             class="contenttype-document state-published url"
             title="Document">Welcome to Plone</a>
   </span>

   body#visual-portal-wrapper.pat-plone .outer-wrapper [class*="contenttype-"]:before, .plone-modal-body [class*="contenttype-"]:before {
       font-family: "Fontello";
       font-size: 100%;
       padding: 0;
       margin: 0;
       position: relative;
       left: inherit;
       display: inline-block;
       color: inherit;
       width: 20px;
       height: 20px;
       text-align: center;
       margin-right: 6px;
       content: '\e834';
   }

Example from plonetheme.barceloneta/plonetheme/barceloneta/theme/less/contents.plone.less:

.. code-block:: less

     body#visual-portal-wrapper.pat-plone .outer-wrapper, .plone-modal-body{
      [class*="contenttype-"]:before {
         font-family:"Fontello"; font-size: 100%;
         padding: 0; margin:0; position: relative; left: inherit; display: inline-block; color: inherit;
         width: 20px; height: 20px; text-align: center; margin-right: @plone-padding-base-vertical;
         content: '\e834';
      }
      .contenttype-folder:before {  content: '\e801';}
      .contenttype-document:before {   content: '\e80e';}
      .contenttype-file:before {   content: none;}
      .contenttype-link:before {    content: '\e806';}
      .contenttype-image:before {      content: '\e810';}
      .contenttype-collection:before {content: '\e808';}
      .contenttype-event:before {      content: '\e809';}
      .contenttype-news-item:before {  content: '\e80f';}
   }

The wildcard definition :code:`[class*="contenttype-"]:before ....content: '\e834'`
renders the default icon for dexterity content types for all dexterity items
which have no specific CSS rule (e.g. custom dexterity content types).

The rule :code:`.contenttype-file:before {   content: none;}` prevents rendering
a fontello font for **file** type items (e.g. ``*.pdf``, ``*.docx``, etc..).

Instead a **mimetype icon** (fetched from the mime type registry) is rendered as HTML tag
(there would be too many fonts needed for all the mime types) in affected templates
e.g. in ``plone.app.contenttypes.browser.templates.listing.pt``:

.. code-block:: html

   <span class="summary" tal:attributes="title item_type">
     <a tal:condition="python:item_type == 'File' and showicons"
       tal:attributes="href item_link;
                       class string:$item_type_class $item_wf_state_class url;
                       title item_type">
       <image class="mime-icon"
               tal:attributes="src item/MimeTypeIcon">
     </a>
     <a tal:attributes="href item_link;
                          class string:$item_type_class $item_wf_state_class url;
                          title item_type"
         tal:content="item_title">Item Title
     </a>
    .....
   </span>
          .

.. image:: ../../_static/content-type-icons.png
   :align: center
   :alt: content type icons

The design decision to use Fontello fonts throws up the question
how to easily create custom fonts for new created custom dexterity items.

A workaround for that is to use an icon URL in the :before clause.
For the custom dexterity type *dx1* you might add the line
:code:`.contenttype-dx1:before {content: url('dx1_icon.png')}` to your less
file and place the icon file in to the same folder.

Preview Images (Thumbs)
=======================

Preview images (aka thumbs) can be shown in listings, tables and portlets.


HiDPI Image Scales
===================

In the Image Handling Settings control panel in Site Setup, you can configure HiDPI mode for extra sharp images.
When you enable this, it will result in image tags like this, for improved viewing on HiDPI screens:

.. code-block:: html

    <img src="....jpeg" alt="alt text" title="some title" class="image-tile"
         srcset="...jpeg 2x, ...jpeg 3x" height="64" width="48">

To benefit from this new feature in add-on code, you must use the ``tag`` method of image scales:

.. code-block:: html

    <img tal:define="images obj/@@images"
         tal:replace="structure python:images.scale('image', scale='tile').tag(css_class='image-tile')">

If you are iterating over a list of image brains, you should
use the new ``@@image_scale`` view of the portal or the navigation root.

This will cache the result in memory, which avoids waking up the objects the next time.

.. code-block:: html

    <tal:block define="image_scale portal/@@image_scale">
        <tal:results tal:repeat="brain batch">
            <img tal:replace="structure python:image_scale.tag(item, 'image', scale='tile', css_class='image-tile')">
        </tal:results>
    </tal:block>


Assimilate collective.indexing
==============================

With the PLIP `assimilate collective.indexing <https://github.com/plone/Products.CMFPlone/issues/1343>`_
the operations for indexing, reindexing and unindexing are queued,
optimized and only processed at the end of the transaction.

Only one indexing operation is done per object on any transaction.
Some tests and features might expect that objects are being indexed/reindexed/unindexed right away.

You can force processing the queue directly in your code with to work around this:

.. code-block:: python

    from Products.CMFCore.indexing import processQueue
    processQueue()

For an example of a test that needed a change see https://github.com/plone/plone.app.upgrade/pull/75/files

You can also disable queuing alltogether by setting the environment-variable `CATALOG_OPTIMIZATION_DISABLED` to `1`:

.. code-block:: bash

    CATALOG_OPTIMIZATION_DISABLED=1 ./bin/instance start

It is a good idea to try this when your tests are failing in Plone 5.1.


CMFDefault removal
==================

CMFDefault was removed with Plone 5.0 but some addons still depend on in.
If your addon depends on CMFDefault you need to include a specific
zcml snippet.

.. code-block:: xml

  <include package="Products.CMFPlone" file="meta-bbb.zcml" />

You can either do this by putting the above snippet as first declaration
into the `configure.zcml` of your policy addon or by including it
via buildout:

.. code-block:: cfg

  [instance]
  ...
  zcml +=
     Products.CMFPlone-meta:meta-bbb.zcml
  ...
