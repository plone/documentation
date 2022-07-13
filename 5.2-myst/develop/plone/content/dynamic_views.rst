==============
 Dynamic views
==============


.. admonition:: Description

    How to programmatically change the active view of a Plone content item

Introduction
============

Dynamic views are views which the content editor can choose for his or her
content from the :guilabel:`Display...` drop-down menu in the green edit
frame.

By default, Plone comes with dynamic views for:

* Folder listing
* Summary
* Photo album
* etc.

The default view can be also a content item picked from the folder.

Available content item types can be managed from the: Site Setup Control Panel -> Content Rules (site.com/@@content-controlpanel) -> Select your new type from the drop down menu -> Click the "Can be used as default page" checkbox.

Permission for changing the view template of an item
----------------------------------------------------

A user needs the :guilabel:`Modify view template` permission to use the
dynamic view dropdown.
If you want to restrict this ability,
grant or revoke this permission as appropriate.

This can be useful for some content types like Dexterity ones, where
dynamic views are enabled by default, and the easiest way to disable
them is using this permission.


Default dynamic views
=====================

Plone supports a few dynamic views for folders out of the box:

* Summary view (``folder_summary_view``)
* Tabular view (``folder_tabular_view``)
* Album view (``atct_album_view``)
* Listing (``folder_listing``)
* Full view (``folder_full_view``)

These are defined in :doc:`portal_types information </develop/plone/content/types>`
for the *Folder* content type and mapped to the *Display* menu all
over in ZCML using ``browser:menuItem`` as described below.

Newly created folders have this dynamic view applied:

* ``Products.CMFPlone/skins/plone_content/folder_summary_view.pt``
  (a non-view based old style Zope 2 page template)

More info

* :doc:`Overriding views </develop/plone/views/browserviews>`

Creating a dynamic view
========================

Here are instructions how to create your own dynamic view.

There is also an example product
`Listless view <https://github.com/miohtama/listlessview>`_,
which provides "no content listing" view for Folder content types.

Registering a dynamic view menu item
------------------------------------

In order to be able to register dynamic views,
your content type must support them.

To do this, the content type should subclass
``Products.CMFDynamicViewFTI.browserdefault.BrowserDefaultMixin``.

Then, you need to register a dynamic view menu item with the corresponding
view in your ``configure.zcml``:

.. code-block:: xml

    <browser:menuItem
            for="Products.ATContentTypes.interface.IATFolder"
            menu="plone_displayviews"
            title="Product listing"
            action="@@product_listing"
            description="List folder contents as product summary view"
            />

.. note::
    ``Products.ATContentTypes`` uses a non-standard name for the
    ``interfaces`` package.
    There, it is ``interface``, while all other packages use ``interfaces``.

The view must be listed in ``portal_types`` for the content type.
In this case, we should enable it for Archetypes folders using the following
GenericSetup XML: ``profiles/default/types/Folder.xml``.

Note that you don't need to copy the whole ``Folder.xml`` / ``Topic.xml``
from ``Products/CMFPlone/profiles/default/types``.
Including the changed ``view_methods`` in the XML code is enough.

You can also change this through portal_types in the Management Interface.

.. note::

    ``view_methods`` must not have the ``@@view`` signature in their method
    name.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="Folder"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="plone"
        meta_type="Factory-based Type Information with dynamic views" >
        <property name="view_methods" purge="False">
            <!-- We retrofit these new views for Folders in portal_types info -->
            <element value="product_listing"/>
        </property>
    </object>

Also, if you want :guilabel:`Collection`\s to have this listing, you need to
add the following ``profiles/default/types/Topic.xml``.

.. code-block:: xml

    <?xml version="1.0"?>
    <object name="Topic"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="plone"
        meta_type="Factory-based Type Information with dynamic views" >
        <property name="view_methods">
            <element value="folder_listing"/>
            <element value="folder_summary_view"/>
            <element value="folder_tabular_view"/>
            <element value="atct_album_view"/>
            <element value="atct_topic_view"/>

            <!-- We retrofit these new views for Folders in portal_types info -->
            <element value="product_listing"/>

        </property>
    </object>

Working around broken default view
====================================

If you manage to:

* Create a new view
* set it to the default as a folder
* and this view has a bug

... you cannot access the folder anymore, because you are taken to the
broken view stack trace instead instead of rendering the green edit menubar.

The fix is to reset the view by browsing to the ``select_default_view``
directly.
Access your folder like this::

    http://servername/plonesite/folder/select_default_view

Checking that your view is available
=====================================

``Products.CMFDynamicViewFTI.browserdefault.BrowserDefaultMixin.getAvailableLayouts()``
returns the list of known layouts in the following format::

    [('folder_summary_view', 'Summary view'),
    ('folder_tabular_view', 'Tabular view'),
    ('atct_album_view', 'Thumbnail view'),
    ('folder_listing', 'Standard view'),
    ('product_listing', u'Product listing')]

To see if your view is available, check it against the ids from that
result::

    layout_ids = [id for id, title in self.portal.folder.getAvailableLayouts() ]
    self.assertTrue("product_list" in layout_ids)

Getting active layout
=====================

.. code-block:: python

    >>> self.portal.folder.getLayout()
    'atct_album_view'

.. _set-default-view-programmatically-label:

Changing default view programmatically
======================================

.. code-block:: python

    self.portal.folder.setLayout("product_listing")

Default page
============

The default page is a *content item* chosen to be displayed when the visitor
arrives at a URL without any subpages or views selected.

This is useful if you are doing the folder listing manually and you want
to replace the default view.

The ``default_page`` helper view can be used to manipulate default pages.

Getting the default page::

    # Filter out default content
    container = self.getListingContainer()
    default_page_helper = getMultiAdapter(
            (container, self.request), name='default_page')

    # Return content object which is the default page or None if not set
    default_page = default_page_helper.getDefaultPage(container)

Another example how to use this::

    from Products.CMFCore.interfaces import IFolderish

    def hasTabs(self):
        """Determine whether the page itself, or default page, in the case
        of folders, has setting showTabs set true.

        Show tab setting defined in dynamicpage.py.
        """

        page = self.context

        try:
            if IFolderish.providedBy(self.context):
                folder = self.context
                default_page_helper = getMultiAdapter(
                        (folder, self.request), name='default_page')
                page_name = default_page_helper.getDefaultPage(folder)
                page = folder[page_name]
        except:
            pass

        tabs = getattr(page, "showTabs", False)

        return tabs

.. TODO:: Bare except?

Setting the default page can be done by calling the ``setDefaultPage`` on the folder, passing id of the default
page::

    folder.setDefaultPage("my_content_id")

More information can be found in

* https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/globals/context.py

* https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/navigation/defaultpage.py

Disabling dynamic views
========================

Add to your content type class::

    def canSetDefaultPage(self):
        """
        Override BrowserDefaultMixin because default page stuff doesn't make
        sense for topics.
        """
        return False

Setting a view using marker interfaces
======================================

If you need to have a view for few individual content items only,
it is best to do this using marker interfaces.

Create a marker interface in python:

.. code-block:: python

    from zope.interface import Interface

    class IMyMarkerInterface(Interface):
        """Used to create a specific view for a generic content type"""

Register the marker interface with ZCML, see :doc:`marker interfaces </develop/addons/components/interfaces>`:

.. code-block:: xml

     <interface interface="my.package.interfaces.IMyMarkerInterface" />

Register the view against a marker interface:

.. code-block:: xml

       <browser:page
         class="my.package.browser.views.MySpecificView"
         for="my.package.interfaces.IMyMarkerInterface"
         layer="my.package.interfaces.IBrowserLayer"
         name="my-custom-view"
         permission="zope2.View"
         template="view.pt"
       />

* Assign this marker interface to a content item using the Management Interface, via the Interfaces tab
  or with Python code:

.. code-block:: python

    from my.package.interfaces import IMyMarkerInterface
    from plone import api
    from Products.Five.utilities.interfaces import IMarkerInterfaces

    portal = api.portal.get()
    folder = portal['my-folder']
    adapter = IMarkerInterfaces(folder)
    adapter.update(add=(IMyMarkerInterface, ))

* If the view should be the default view for that given object,
  add a ``layout`` property with value ``my-custom-view``.
  To do the same with python, see :ref:`set-default-view-programmatically-label`.

Migration script from default view to another
==============================================

Below is a script snippet which allows you to change the default view
for all folders to another type.
You can execute the script through the Management Interface as a Python script.

Script code::

    from StringIO import StringIO

    orignal = 'fancy_zoom_view'
    target = 'atct_album_view'
    for brain in context.portal_catalog(portal_type="Folder"):
        obj = brain.getObject()
        if getattr(obj, "layout", None) == orignal:
            print "Updated:" + obj.absolute_url()
            obj.setLayout(target)
    return printed

This will allow you to migrate from ``collective.fancyzoom`` to Plone
4's default album view or ``Products.PipBox``.

Method aliases
=================

Method aliases allow you to redirect basic actions (view, edit) to
content type specific views.  Aliases are configured in ``portal_types``.

Other resources
================

* https://plone.org/documentation/how-to/how-to-create-and-set-a-custom-homepage-template-using-generic-setup

* `CMFDynamicView plone.org product page <https://plone.org/products/cmfdynamicviewfti/>`_
