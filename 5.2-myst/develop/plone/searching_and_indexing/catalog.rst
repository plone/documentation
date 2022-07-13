========
Catalogs
========

.. admonition:: Description

   A brief introduction to ZCatalogs, the Catalog Tool and what
   they're used for.


Why ZCatalogs
=============

Plone uses the ZODB to store content in a very free-form manner with arbitrary hierarchy and a lot of flexibility in general.
For some content use cases, however, it is very useful to treat content as more ordered, or tabular.
This is where ZCatalog comes in.

Searching, for example, requires being able to query content on structured data such as dates or workflow states.
Additionally, query results often need to be sorted based on structured data of some sort.
When it comes to searching it is very valuable to treat our free-form persistent ZODB objects as if they were more tabular.
ZCatalog indexes do exactly this.

Since the ZCatalog is in the business of treating content as tabular when it isn't necessarily so,
it is very tolerant of any missing data or exceptions when indexing.
For example, Plone includes "start" and "end" indexes to support querying events on their start and end dates.
When a page is indexed, however, it doesn't have start or end dates.
Since the ZCatalog is tolerant, it doesn't raise any exception when indexing the start or end dates on a page.
Instead it simply doesn't include pages in those indexes.
As such, it is appropriate to use indexes in the catalog to support querying or sorting when not all content provides the data indexed.

This manual is intended to be a brief start guide to ZCatalogs,
specially aimed to tasks specific to Plone,
and will not treat advanced ZCatalogs concepts in depth.
If you want to learn more about ZCatalogs in the context of Zope,
please refer to `The Zope Book, Searching and Categorizing Content`_.


Quick start
===========

Every ZCatalog is composed of indexes and metadata.
Indexes are fields you can search by,
and metadata are copies of the contents of certain fields which can be accessed without waking up the associated content object.

Most indexes are also metadata fields.
For example, you can search objects by *Title* and then display the *Title* of each object found without fetching them,
but note not all indexes need to be part of metadata.

When you search inside the catalog,
what you get as a result is a list of elements known as brains.
Brains have one attribute for each metadata field defined in the catalog,
in addition to some methods to retrieve the underlying object and its location.
Metadata values for each brain are saved in the metadata table of the catalog upon the (re)indexing of each object.

Brains are said to be lazy for two reasons;
first, because they are only created 'just in time' as your code requests each result,
and second, because retrieving a catalog brain doesn't wake up (or load) the objects themselves, avoiding a huge performance hit.

To see the ZCatalogs in action, use your favorite browser and open the Management Interface.
You'll see an object in the root of your Plone site named *portal\_catalog*.
This is the Catalog Tool, a Plone tool based on ZCatalog created by default in every Plone site which indexes all the created content.

Open it and click the *Catalog* tab, at the top of the screen.
There you can see the full list of currently indexed objects,
filter them by path, and update and remove entries.
If you click on any entry, a new tab (or window) will open showing the metadata and index values for the selected indexed object.
Note that most fields are "duplicated" in the *Index Contents* and *Metadata Contents* tables,
but its contents have different formats.
This is because indexes are meant to search in,
and metadata to retrieve certain attributes from the content object without waking it up.

Back to the management view of the Catalog Tool,
if you click the *Indexes* or the *Metadata* tab you'll see the full list of currently available indexes and metadata fields with its types and more. There you can also add and remove indexes and metadata fields.
If you're working in a test environment, you can use this manager view for playing with the catalog,
but beware indexes and metadata are usually added through GenericSetup and not using the Management Interface.

Other catalogs
--------------

Besides, the main portal catalog, the site contains other catalogs.

* uid_catalog maintains object look up by Unique Identified (UID). UID is given to the object
  when it is created and it does not change even if the object is moved around the site.

* reference_catalog maintains inter-object references by object unique identified (UID).
  Archetypes's ReferenceField uses this catalog. The catalog contains indexes
  UID, relationship, sourceUID, targetId and targetUID.

* Add-on products may install their own catalogs which are optimized for specific purposes.
  For example, `betahaus.emaillogin <https://pypi.python.org/pypi/betahaus.emaillogin>`_
  creates email_catalog is which is used to speed-up login by email process.

Manually indexing object to a catalog
-------------------------------------

The default content ``obj.reindexObject()`` is defined in
`CMFCatalogAware <https://github.com/zopefoundation/Products.CMFCore/blob/2.2/Products/CMFCore/CMFCatalogAware.py#L78-L88>`_
and will update the object data to ``portal_catalog``.

If you don't need to reindex all the indexes you can speed up quite a bit by being more selective:

.. code-block:: python

    obj.reindexObject(idxs=['some_index'])

You can use the ``portal_catalog`` directly if you need to update more than one object:

.. code-block:: python

    from plone import api

    catalog = api.portal.get_tool('portal_catalog')
    catalog.catalog_object(obj, idxs=['some_index'])

If it's only an index that needs to be updated and not catalog metadata you can speed up even more like this:

.. code-block:: python

    catalog.catalog_object(obj, idxs=['some_index'], update_metadata=False)

If your code uses additional catalogs, you need to manually update cataloged values after the object has been modified.

.. code-block:: python

    # Update email_catalog which mantains loggable email addresses
    email_catalog = api.portal.get_tool('email_catalog')
    email_catalog.catalog_object(obj)

For more information and tips on how to speed up the indexing process see `Best practices on reindexing the catalog <https://community.plone.org/t/best-practices-on-reindexing-the-catalog/4157>`_ on the Plone Community Forum.

Manually uncatalog object to a catalog
--------------------------------------

Sometimes is useful to uncatalog object.

code ::

    ### uncatalog object name id
    >>> brains = catalog(getId=id)
    >>> for brain in brains:
    ...     catalog.uncatalog_object(brain.getPath())


Rebuilding a catalog
--------------------

Catalog rebuild means walking through all the objects on Plone site and adding them to the catalog.
Rebuilding the catalog is very slow as the whole database must be read through.
Reasons for you to do this in code could be

* Creating catalog after setting up objects in the unit tests

* Rebuilding after massive content migration

How to trigger rebuild::

    portal_catalog = self.portal.portal_catalog
    portal_catalog.clearFindAndRebuild()

Retrieving unique values from a catalog
---------------------------------------
Catalogs have a uniqueValues method associated with each index.
There are times when you will need to get a list of all the values
currently stored on a particular index. For example if you wanted
the highest and lowest price you might first need to retrieve the
values currently indexed for price. This example demonstrates how
you can list all the unique values on an index named 'price'.

::

    portal_catalog = self.portal.portal_catalog
    portal_catalog.Indexes['price'].uniqueValues()

the result would be a listing of all the prices stored in the 'price' index::

    (0, 100000, 120000, 200000, 220000, 13500000, 16000000, 25000000)


Minimal code for creating a new catalog
---------------------------------------

::

    from zope.interface import Interface, implements
    from zope.component import getUtility

    from Acquisition import aq_inner
    from Acquisition import aq_parent


    from AccessControl import ClassSecurityInfo
    from Globals import InitializeClass
    from Products.CMFPlone.utils import base_hasattr
    from Products.CMFPlone.utils import safe_callable
    from Products.CMFCore.permissions import ManagePortal
    from Products.CMFCore.utils import getToolByName
    from Products.ZCatalog.ZCatalog import ZCatalog
    from Products.CMFPlone.CatalogTool import CatalogTool




    class IMyCatalog(Interface):
       """
       """

    class MyCatalog(CatalogTool):
       """
       A specific launch catalog tool
       """

       implements(IMyCatalog)

       title = 'specific catalog'
       id = 'my_catalog'
       portal_type = meta_type = 'MyCatalog'
       plone_tool = 1

       security = ClassSecurityInfo()
       _properties=(
          {'id':'title', 'type': 'string', 'mode':'w'},)

       def __init__(self):
           ZCatalog.__init__(self, self.id)

       security.declarePublic('enumerateIndexes')
       def enumerateIndexes(self):
            """Returns indexes used by catalog"""
            return (
                ('id', 'FieldIndex', ()),
                ('portal_type', 'FieldIndex', ()),
                ('path', 'ExtendedPathIndex', ('getPhysicalPath')),
                ('getCanonicalPath', 'ExtendedPathIndex', ('getCanonicalPath')),
                ('isArchived', 'FieldIndex', ()),
                ('is_trashed', 'FieldIndex', ()),
                ('is_obsolete', 'FieldIndex', ()),
                ('Language', 'FieldIndex', ()),
                ('review_state', 'FieldIndex',()),
                ('allowedRolesAndUsers', 'DPLARAUIndex', ()),

                )

        security.declarePublic('enumerateMetadata')
        def enumerateMetadata(self):
            """Returns metadata used by catalog"""
            return (
                'Title',
                'getId',
                'UID',
                'review_state',
                'created',
                'modified',
               )

        security.declareProtected(ManagePortal, 'clearFindAndRebuild')
        def clearFindAndRebuild(self):
            """Empties catalog, then finds all contentish objects (i.e. objects
               with an indexObject method), and reindexes them.
               This may take a long time.
            """



            def indexObject(obj, path):
                self.reindexObject(obj)

            self.manage_catalogClear()

            portal = getToolByName(self, 'portal_url').getPortalObject()
            portal.ZopeFindAndApply(portal,
                                    #""" put your meta_type here """,

                                    obj_metatypes=(),

                                    search_sub=True, apply_func=indexObject)

    InitializeClass(MyCatalog)

Register a new catalog via portal_setup
---------------------------------------

In toolset.xml add this lines

::

 <?xml version="1.0"?>
 <tool-setup>

   <required tool_id="my_catalog"
            class="catalog.MyCatalog"/>

 </tool-setup>



archetype_tool catalog map
==========================

archetype_tool maintains map between content types and catalogs which are interested int them.
When object is modified through Archetypes mechanisms, Archetypes post change notification
to all catalogs enlisted.

See *Catalogs* tab on archetype_tool in Management Interface.

Map an catalog for an new type
------------------------------

code

::

 at = getToolByName(context,'archetype_tool')
 at.setCatalogsByType('MetaType', ['portal_catalog','mycatalog',])




Additional info
----------------

* `ZCatalog source code <https://github.com/zopefoundation/Products.ZCatalog/blob/master/src/Products/ZCatalog/ZCatalog.py>`_.

* `Searching the Catalog <https://web.archive.org/web/20140401005054/https://wyden.com/plone/basics/searching-the-catalog>`_ by Wyden Silvan


.. _The Zope Book, Searching and Categorizing Content: http://docs.zope.org/zope2/zope2book/SearchingZCatalog.html
.. _AdvancedQuery: http://www.dieter.handshake.de/pyprojects/zope/AdvancedQuery.html
.. _Boolean queries (AdvancedQuery): query.html#boolean-queries-advancedquery
