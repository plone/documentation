========
Querying
========

.. admonition:: Description

    How to programmatically search and query content from a Plone site.

.. contents::
  :local:

Introduction
============

*Querying* is the action to retrieve data from search indexes.
In Plone's case this usually means querying content items using either the :doc:`plone.api.content.find </develop/plone.api/docs/api/content>` function or directly using the ``portal_catalog`` tool.

Plone uses the :doc:`portal_catalog </develop/plone/searching_and_indexing/catalog>` tool to perform most content-related queries.
Other special catalogs, like ``reference_catalog`` for Archetypes, exist, for specialized and optimized queries.


Accessing the ``portal_catalog`` tool
=====================================

Plone queries are performed using ``portal_catalog`` which is available as an persistent object at the site root.

The recommended way to get the tool is using :doc:`plone.api.portal_get_tool </develop/plone.api/docs/api/portal>`:

.. code-block:: python

    from plone import api
    portal_catalog = api.portal.get_tool('portal_catalog')

Another safe method is to use the ``getToolByName`` helper function:

.. code-block:: python

    from Products.CMFCore.utils import getToolByName
    catalog = getToolByName(context, 'portal_catalog')

Given the portal-object (site) itself is available also possible is the direct attribute access:

.. code-block:: python

    # portal_catalog is defined in the site root
    portal_catalog = site.portal_catalog


There is also a another way, using traversing.
This is discouraged, as this includes extra processing overhead:

.. code-block:: python

    # Use magical Zope acquisition mechanism
    portal_catalog = context.portal_catalog

And here the same in TAL template, also discouraged:

.. code-block:: xml

    <div tal:define="portal_catalog context/portal_catalog" />


Querying ``portal_catalog``
===========================


To search for something and get the resulting brains, write:

.. code-block:: python

    results = catalog.searchResults(**kwargs)

.. Note:: The catalog returns "*brains*". A brain is a lightweight proxy
   for a found object, which has attributes corresponding to the metadata
   defined for the catalog.

Where ``kwargs`` is a dictionary of index names and their associated query values.
Only the indexes that you care about need to be included.
This is really useful if you have variable searching criteria.
For example, coming from a form where the users can select different fields to search for.

.. code-block:: python

    results = catalog.searchResults(**{'portal_type': 'Event', 'review_state': 'pending'})

It is worth pointing out at this point that the indexes that you include are treated as a logical AND, rather than OR.
In other words, the query above will find all the items that are both an Event, AND in the review state of pending.

Additionally, you can call the catalog tool directly, which is exactly the same to calling ``catalog.searchResults()``:

.. code-block:: python

    results = catalog(portal_type='Event')

If you call portal_catalog() without arguments it will return all indexed content objects:

.. code-block:: python

        # Print all content on the site
        all_brains = catalog()
        for brain in all_brains:
            print('Name: ' + brain.Title + ', URL:' + brain.getURL())

The catalog tool queries return an iterable of catalog brain objects.

As mentioned previously, brains contain a subset of the actual content object information.
The available subset is defined by the metadata columns in portal_catalog.
You can see available metadata columns on the portal_catalog "Metadata" tab in Management Interface.
For more information, see :doc:`indexing </develop/plone/searching_and_indexing/indexing>`.


Available Indexes
-----------------

To see the full list of available indexes in your catalog

* open the Management Interface (which usually means navigating to *http://yoursiteURL/manage*)
* look for the *portal\_catalog* object tool in the root of your Plone site and
* check the *Indexes* tab.

Note that there are different types of indexes, and each one admits different types of search parameters, and behaves differently.
For example, *FieldIndex* and *KeywordIndex* support sorting, but *ZCTextIndex* doesn't.
To learn more about indexes, see `The Zope Book, Searching and Categorizing Content <http://docs.zope.org/zope2/zope2book/SearchingZCatalog.html>`_.

Some of the most commonly used ones are:

Title
    The title of the content object.
Description
    The description field of the content.
Subject
    The keywords used to categorize the content. Example:

    .. code-block:: python

        catalog.searchResults(Subject=('cats', 'dogs'))

portal\_type
    As its name suggests, search for content whose portal type is
    indicated. For example:

    .. code-block:: python

        catalog.searchResults(portal_type='News Item')

    You can also specify several types using a list or tuple format:

    .. code-block:: python

        catalog.searchResults(portal_type=('News Item', 'Event'))

review\_state
    The current workflow review state of the content. For example:

    .. code-block:: python

        catalog.searchResults(review_state='pending')

created, last_modified, effective, expires, start, end
    The dates stored with the content ("start" and "end" only on events).
    Example to find all content expired before now

    .. code-block:: python

        import datetime

        catalog.searchResults(
            expired={'query': datetime.datetime.now(), range='max')
        }

object\_provides
    You can search by the interface provided by the content.
    Example:

    .. code-block:: python

        from Products.MyProduct.path.to import IIsCauseForCelebration
        catalog(object_provides=IIsCauseForCelebration.__identifier__)

    Searching for interfaces can have some benefits.
    Suppose you have several types,
    for example, event types like *Birthday*, *Wedding*  and *Graduation*,
    in your portal which implement the same interface (for example, ``IIsCauseForCelebration``).
    Such an interface can be an Dexterity behavior (the behavior itself or its marker).
    Suppose you want to get items of these types from the catalog by their interface.
    This is more exact and more flexible than naming the types explicitly (like portal\_type=['Birthday','Wedding','Graduation' ]),
    because you don't really care what the types' names really are:
    all you really care for is the interface.
    This has the additional advantage that if products added or modified later add types which implement the interface,
    these new types will also show up in your query.


Brain Result Id
===============

Result ID (RID) is given with the brain object and you can use this ID to query
further info about the object from the catalog.

Example::

        (Pdb) brain.getRID()
        872272330

Brain Result Path
=================

Brain result path can be extraced as string using ``getPath()`` method::

        print(r.getPath())
        /site/sisalto/ajankohtaista


Brain Object Schema
===================

To see what metadata columns a brain object contain,
you can access this information from ``__record_schema__`` attribute which is a dict.

Example::

        for i in brain.__record_schema__.items():
            print(i)

        ('startDate', 32)
        ('endDate', 33)
        ('Title', 8)
        ('color', 31)
        ('data_record_score_', 35)
        ('exclude_from_nav', 13)
        ('Type', 9)
        ('id', 19)
        ('cmf_uid', 29)

.. TODO::
    What do those numbers represent?


Getting the underlying object, its path, and its URL from a brain
-----------------------------------------------------------------

Searching inside the catalog returns catalog brains, not the object themselves.
If you want to get the object associated with a brain, do:

.. code-block:: python

    brain.getObject()

To get the path of the object without fetching it:

.. code-block:: python
    brain.getPath()

which returns the path as an string, corresponding to ``obj.getPhysicalPath()``

And finally, to get the URL of the underlying object, usually to provide a link to it:

.. code-block:: python

    brain.getURL()

which is equivalent to ``obj.absolute_url()``.

.. Note::

        Calling getObject() has performance implications.
        Waking up each object needs a separate query to the database.


getObject() and unrestrictedSearchResults() permission checks
-------------------------------------------------------------

You cannot call ``getObject()`` for a restricted result, even in trusted code.

Instead, you need to use::

        unrestrictedTraverse(brain.getPath())

.. TODO::

   How to call ``unrestrictedTraverse``. Also validate if this is still true.

For more information, see

* http://www.mail-archive.com/zope-dev@zope.org/msg17514.html


Counting value of a specific index
----------------------------------

The efficient way of counting the number value of an index is to work directly in this index.
For example we want to count the number of each portal_type.
Quering via search results is a performance bootleneck for that.
Iterating on all brains put those in zodb cache.
This method is also a memory bottleneck.

A good way to achieve this would be:

.. code-block:: python

   # count portal_type index
   stats = {}
   x = getToolByName(context, 'portal_catalog')
   index = x._catalog.indexes['portal_type']
   for key in index.uniqueValues():
       t = index._index.get(key)
       if type(t) is not int:
           stats[str(key)] = len(t)
       else:
           stats[str(key)] = 1



Sorting and limiting the number of results
==========================================

To sort the results, use the sort\_on and sort\_order arguments.
The sort\_on argument accepts any available index, even if you're not searching by it.
The sort\_order can be either 'ascending' or 'descending', where 'ascending' means from A to Z for a text field.
'reverse' is an alias equivalent to 'descending'.

.. code-block:: python

    results = catalog_searchResults(
        Description='Plone documentation',
        sort_on='sortable_title',
        sort_order='ascending'
    )

It is possible to order to sort first in order of ``portal_type`` and second for the same types in order of ``sortable_title``.

.. code-block:: python

    results = catalog_searchResults(
        Description='Plone documentation',
        sort_on='portal_type, sortable_title',
        sort_order='ascending'
    )

.. note::

    If you sort on something, the result will not contain items which aren't in the sort index.
    I.e. if you sort on ``start`` only items will be found having a ``start`` date, like events.

The catalog.searchResults() returns a list-like object, so to limit the number of results you can just use Python's slicing.
For example, to get only the first 3 items:

.. code-block:: python

    results = catalog.searchResults(Description='Plone documentation')[:3]

In addition, ZCatalogs allow a sort\_limit argument.
The sort\_limit is only a hint for the search algorithms and can potentially return a few more items,
so it's preferable to use both ``sort_limit`` and slicing simultaneously:

.. code-block:: python

    limit = 50
    results = catalog.searchResults(
        Description='Plone documentation',
        sort_limit=limit
    )[:limit]


portal_catalog query takes *sort_on* argument which tells the index used for sorting.
*sort_order* defines sort direction. It can be string "reverse".

Sorting is supported only on FieldIndexes and some derived indexes.
Due to the nature of searchable text indexes (they index split text, not strings) they cannot be used for sorting.
For example, to do sorting by title, an index called *sortable_tite* should be used.

Example of how to sort by id:

.. code-block:: python

    results = context.portal_catalog.searchResults(
        sort_on='id',
        portal_type='Document',
        sort_order='reverse'
    )


Text Format
===========

Indexes use direct attribute access (Dexterity) and so return they the raw value.
This depends on the schema and is i.e. for a ``TextLine`` unicode.

For some indexes special index-adapters are registered.
Here it is upon the indexer implementation how the value is returned.

With Archetypes, accessors are used to index the field value and the returned text is UTF-8 encoded.
This is a limitation inherited from the early ages of Plone.
To get unicode value for e.g. title you need to do the following:

.. code-block:: python

    title = brain['Title']
    title = title.decode('utf-8')


Accessing indexed data
======================

Normally you don't get copy of indexed data with brains, only metadata.
You can still access the raw indexed data if you know what you are doing by using RID of the brain object.

.. note::

    This is a very rare use case and documented here for completeness.

Example::

        (Pdb) data = self.context.portal_catalog.getIndexDataForRID(872272330)
        (Pdb) for i in data.items(): print i
        ('Title', ['ulkomuseon', 'tarinaopastukset'])
        ('effectiveRange', (21305115, 278752140))
        ('object_provides', ['Products.CMFCore.interfaces._content.IDublinCore', 'Products.ATContentTypes.interface.interfaces.IHistoryAware', 'AccessControl.interfaces.IOwned', 'OFS.interfaces.ITraversable', 'plone.portlets.interfaces.ILocalPortletAssignable', 'Products.Archetypes.interfaces._base.IBaseObject', 'zope.annotation.interfaces.IAttributeAnnotatable', 'vs.event.interfaces.IVSEvent', 'Products.CMFCore.interfaces._content.IMutableMinimalDublinCore', 'OFS.interfaces.IPropertyManager', 'OFS.interfaces.IZopeObject', 'AccessControl.interfaces.IRoleManager', 'zope.annotation.interfaces.IAnnotatable', 'Acquisition.interfaces.IAcquirer', 'Products.ATContentTypes.interface.event.IATEvent', 'OFS.interfaces.ICopySource', 'Products.ATContentTypes.interface.interfaces.ICalendarSupport', 'Products.ATContentTypes.interface.interfaces.IATContentType', 'plone.app.iterate.interfaces.IIterateAware', 'Products.Archetypes.interfaces._base.IBaseContent', 'Products.CMFCore.interfaces._content.ICatalogableDublinCore', 'Products.CMFDynamicViewFTI.interface._base.IBrowserDefault', 'Products.Archetypes.interfaces._referenceable.IReferenceable', 'plone.locking.interfaces.ITTWLockable', 'plone.app.imaging.interfaces.IBaseObject', 'persistent.interfaces.IPersistent', 'webdav.interfaces.IDAVResource', 'AccessControl.interfaces.IPermissionMappingSupport', 'OFS.interfaces.ISimpleItem', 'plone.app.kss.interfaces.IPortalObject', 'plone.app.kss.interfaces.IContentish', 'archetypes.schemaextender.interfaces.IExtensible', 'App.interfaces.IUndoSupport', 'OFS.interfaces.IManageable', 'App.interfaces.IPersistentExtra', 'Products.CMFCore.interfaces._content.IMutableDublinCore', 'Products.Archetypes.interfaces._athistoryaware.IATHistoryAware', 'dateable.kalends.IRecurringEvent', 'OFS.interfaces.IItem', 'zope.interface.Interface', 'OFS.interfaces.IFTPAccess', 'Products.CMFDynamicViewFTI.interface._base.ISelectableBrowserDefault', 'webdav.interfaces.IWriteLock', 'Products.CMFCore.interfaces._content.IMinimalDublinCore', 'Products.CMFCore.interfaces._content.IDynamicType', 'Products.CMFCore.interfaces._content.IContentish'])
        ('Type', u'VSEvent')
        ('id', 'ulkomuseon-tarinaopastukset')
        ('cmf_uid', 2)
        ('recurrence_days', [733960, 733981, 733974, 733967])
        ('end', 1077028380)
        ('Description', ['saamelaismuseon', 'ulkomuseossa', ...
        ('is_folderish', False)
        ('getId', 'ulkomuseon-tarinaopastukset')
        ('start', 1077028380)
        ('is_default_page', False)
        ('Date', 1077036795)
        ('review_state', 'published')
        ('Language', <LanguageIndex.IndexEntry id 872272330 language fi, cid 8b9a08c216b8e086f3446775ad71a748>)
        ('portal_type', 'VSEvent')
        ('expires', 1339244460)
        ('allowedRolesAndUsers', ['Anonymous'])
        ('getObjPositionInParent', 10)
        ('path', '/siida/sisalto/8-vuodenaikaa/ulkomuseon-tarinaopastukset')
        ('in_reply_to', '')
        ('UID', '8b9a08c216b8e086f3446775ad71a748')
        ('Creator', 'admin')
        ('effective', 1077036795)
        ('getRawRelatedItems', [])
        ('getEventType', [])
        ('created', 1077036792)
        ('modified', 1077048720)
        ('SearchableText', ['ulkomuseon', 'tarinaopastukset', ...
        ('sortable_title', 'ulkomuseon tarinaopastukset')
        ('meta_type', 'VSEvent')
        ('Subject', [])

You can also directly access a single index::

    # Get event brain result id
    rid = event.getRID()
    # Get list of recurrence_days indexed value.
    # ZCatalog holds internal Catalog object which we can directly poke in evil way
    # This call goes to Products.PluginIndexes.UnIndex.Unindex class and we
    # read the persistent value from there what it has stored in our index
    # recurrence_days
    index = portal_catalog._catalog.getIndex('recurrence_days')
    indexed_days = index.getEntryForObject(rid, default=[])



Dumping portal catalog content
==============================

Following is useful in unit test debugging.

.. code-block:: python

    # Print all objects visible to the currently logged in user
    for i in portal_catalog(): print i.getURL()

.. note:

        Security: This portal_catalog() query respects the permissions of the currently logged in user


Bypassing query security check
==============================

.. note::
   Security: All portal_catalog queries are limited to the current user permissions by default.

If you want to bypass this restriction, use the unrestrictedSearchResults() method.

.. code-block:: python

    # Print absolute content of portal_catalog
    for i in portal_catalog.unrestrictedSearchResults():
        print i.getURL()

With ``unrestrictedSearchResults()`` you need also a special way to get access to the objects without triggering a security exception:

.. code-block:: python

    obj = brain._unrestrictedGetObject()

Bypassing language check
========================

.. note::
   All portal_catalog() queries are limited to the selected language of the current user.
   You need to explicitly bypass the language check if you want to do multilingual queries.

Language is only a factor when a multilingual product is installed - which basically comes down to one of the venerable ``LinguaPlone`` or the more modern ``plone.app.multilingual``.
Bypassing the language check depends on which of these you are using.

In *LinguaPlone* and *plone.app.multilingual 1.x* (what you would probably use in versions 4.3 or earlier of Plone), a patch is applied to the portal_catalog.
To bypass this add the parameter ``Language='all'`` to your catalog query like so:

.. code-block:: python

    all_content_brains = portal_catalog(Language='all')

*plone.app.multilingual 2.x and later* (part of Plone 5.x) creates Root Language Folders for each of your site's languages.
It keeps ("jails") content within the appropriate folders.
Each Root Language Folder is also a NavigationRoot, so the portal_catalog is already effectively limited to searches in the users current language.
This means that the way to bypass this is to add the query parameter ``path='/'`` to your catalog query like so:

.. code-block:: python

    all_content_brains = portal_catalog(path='/')

.. note::
   Although in LinguaPlone eventually the language folders are also marked to be an INavigationRoot.
   The language of the content is not enforced inside the language folder.
   In plone.app.multilingual there's a subscriber that moves the content to the appropriate folder.


Bypassing Expired content check
===============================

Plone and its portal_catalog have a mechanism to list only active (non-expired) content by default.

Below is an example of how the expired content check is made:

.. code-block:: python

    mtool = context.portal_membership
    show_inactive = mtool.checkPermission('Access inactive portal content', context)

    contents = context.portal_catalog.queryCatalog(show_inactive=show_inactive)

See also:

* :doc:`Listing <../content/listing>`

None as query parameter
=======================

.. warning::
   Usually if you pass in None as the query value, it will match all the objects instead of zero objects.

.. note::
   Querying for None values is possible with AdvancedQuery_ (see below).


Query by path
=============

ExtendedPathIndex_ is the index used for content object paths.
The *path* index stores the physical path of the objects.

.. warning::
   If you ever rename your Plone site instance,
   the path index needs to be completely rebuilt.

Example, return myfolder and all child content.

.. code-block:: python

    portal_catalog(path={ "query": "/myploneinstance/myfolder" })

Searching for content within a folder
-------------------------------------

Use the 'path' argument to specify the physical path to the folder you want to search into.

By default, this will match objects into the specified folder and all existing sub-folders.
To change this behaviour, pass a dictionary with the keys 'query' and 'depth' to the 'path' argument, where

- 'query' is the physical path, and
- 'depth' can be either 0, which will return only the brain for the path queried against,
  or some number greater,
  which will query all items down to that depth (eg, 1 means searching just inside the specified folder,
  or 2, which means searching inside the folder, and inside all child folders, etc).

The most common use case is listing the contents of an existing folder,
which we'll assume to be the ``context`` object in this example:

.. code-block:: python

    folder_path = '/'.join(context.getPhysicalPath())
    results = catalog(path={'query': folder_path, 'depth': 1})

The above can be achieved much easier using plone.api:

.. code-block:: python

    from plone import api
    results = api.content.find(context=context, depth=1)


Query multiple values
=====================

``KeywordIndex`` index type indexes lists of values.
It is used e.g. by Plone's categories (subject) feature and ``object_provides`` provided interfaces index.

You can either query

* a single value in the list

* many values in the list (all must present)

* any value in the list

The index of the catalog to query is either the name of the
keyword argument, a key in a mapping, or an attribute of a record
object.

Attributes of record objects

* ``query`` -- either a sequence of objects or a single value to be
  passed as query to the index (mandatory)

* ``operator`` -- specifies the combination of search results when
  query is a sequence of values. (optional, default: 'or'). Allowed values:
  'and', 'or'

Below is an example of matching any of multiple values gives as a Python list in KeywordIndex.
It queries all event types and recurrence_days KeywordIndex must match any of the given dates:

.. code-block:: python

    # Query all events on the site
    # Note that there is no separate list for recurrent events
    # so if you want to speed up you can hardcode
    # recurrent event type list here.
    matched_recurrence_events = self.context.portal_catalog(
        portal_type=supported_event_types,
        recurrence_days={
            'query':recurrence_days_in_this_month,
            'operator' : 'or'
        }
    )


Querying by interface
=====================

Suppose you have several content types (for example, event types like
'Birthday','Wedding','Graduation') in your portal which implement the same
interface (for example, ``IIsCauseForCelebration``). Suppose you want to get
items of these types from the catalog by their interface. This is more exact
than naming the types explicitly (like ``portal_type=['Birthday', 'Wedding',
'Graduation' ]``), because you don't really care what the types' names really
are: all you really care for is the interface.

This has the additional advantage that if products added or modified later add
types which implement the interface, these new types will also show up in your
query.

Import the interface::

    from Products.MyProduct.interfaces import IIsCauseForCelebration
    catalog(object_provides=IIsCauseForCelebration.__identifier__)

In a script, where you can't import the interface due to restricted Python,
you might do this::

    object_provides='Products.MyProduct.interfaces.IIsCauseForCelebration'

The advantage of using ``.__identifier__`` instead instead of a dotted
name-string is that you will get errors at startup time if the interface cannot
be found. This will catch typos and missing imports.

Caveats
-------

* ``object_provides`` is a KeywordIndex which indexes absolute
  Python class names. A string matching is performed for the dotted name. Thus,
  you will have zero results for this::

      catalog(object_provides="Products.ATContentTypes.interface.IATDocument")

  because Products.ATContentTypes.interface imports everything from
  ``document.py``. But this will work::

      catalog(object_provides="Products.ATContentTypes.interface.document.IATDocument")
      # products.atcontenttypes.document.iatdocument declares the interfacea

* As with all catalog queries, if you pass an empty value for search parameter,
  it will return all results. so if the interface you defined would yield a none
  type object, the search would return all values of object_provides.

(Originally from `this tutorial <https://plone.org/documentation/how-to/query-portal_catalog-for-interfaces>`_.)

.. note::
   Looks like query by Products.CMFCore.interfaces._content.IFolderish does not seem to work in Plone 4.1
   as this implementation information is not populated in portal_catalog.

Query by content type
=====================

To get all catalog brains of certain content type on the whole site::

        campaign_brains = self.context.portal_catalog(portal_type="News Item")

To see available type names, visit portal_types in the Management Interface.

Query published items
=====================

By default, the portal_catalog query does not care about the workflow state.
You might want to limit the query to published items.

Example::

        campaign_brains = self.context.portal_catalog(portal_type="News Item", review_state="published")


review_state is a portal_catalog index which reads portal_workflow variable "review_state".
For more information, see what portal_workflow tool *Content* tab in Management Interface contains.

Getting a random item
=====================

The following view snippet allows you to get one random item on the site::

    import random

    def getRandomCampaign(self):
        """
        """


        campaign_brains = self.context.portal_catalog(portal_type="CampaignPage", review_state="published")

        # Filter out the current item which we have

        bad_ids = [ "you", "might", "want to black  list some ids here" ]

        items = [ brain for brain in campaign_brains if brain["getId"] not in bad_ids ]

        # Check that we have items left after filtering

        items = list(items)

        if len(items) >= 1:
            # Pick one
            chosen = random.choice(items)
            return chosen.getObject()
        else:
            # Fallback to the current content item if no random options available
            return self.context


Querying FieldIndexes by Range
==============================
The following examples demonstrate how to do range based queries.
This is useful if you want to find the "minimum" or "maximum" values
of something, the example assumes that there is an index called 'getPrice'.

Get a value that is greater than or equal to 2::

   items = portal_catalog({'getPrice':{'query':2,'range':'min'}})

Get a value that is less than or equal to 40::

   items = portal_catalog({'getPrice':{'query':40,'range':'max'}})

Get a value that falls between 2 and 1000::

   items = portal_catalog({'getPrice':{'query':[2,1000],'range':'min:max'}})

Querying by date
================

See `DateIndex <http://svn.zope.org/Zope/trunk/src/Products/PluginIndexes/DateIndex/tests/test_DateIndex.py?rev=102443&view=auto>`_.

Example:

.. code-block:: python

    date_range = {
        'query': (
            DateTime('2002-05-08 15:16:17'),
            DateTime('2062-05-08 15:16:17'),
        ),
        'range': 'min:max',
    }

    items = portal_catalog(effective=date_range)

Note that ``effectiveRange`` may be a lot more efficient. This will return only
objects whose ``effective_date`` is in the past, ie. objects that are not
unpublished::

    items = portal_catalog(effectiveRange=DateTime())


Example 2 - how to get items one day old of FeedFeederItem content type::

        # DateTime deltas are days as floating points
        end = DateTime.DateTime() + 0.1 # If we have some clock skew peek a little to the future
        start = DateTime.DateTime() - 1

        date_range_query = { 'query':(start,end), 'range': 'min:max'}

        items = portal_catalog.queryCatalog({"portal_type":"FeedFeederItem",
                                             "created" : date_range_query,
                                             "sort_on":"positive_ratings",
                                             "sort_order":"reverse",
                                             "sort_limit":count,
                                             "review_state":"published"})


Example 3: how to get news items for a particular year in the template code

.. code-block:: html

    <div metal:fill-slot="main" id="content-news"
     tal:define="boundLanguages here/portal_languages/getLanguageBindings;
                 prefLang python:boundLanguages[0];
                 DateTime python:modules['DateTime'].DateTime;
                 start_year request/year| python: 2004;
                 end_year request/year| python: 2099;
                 start_year python: int(start_year);
                 end_year python: int(end_year);
                 results python:container.portal_catalog(
                    portal_type='News Item',
                    sort_on='Date',
                    sort_order='reverse',
                    review_state='published',
                    id=prefLang,
                    created={ 'query' : [DateTime(start_year,1,1), DateTime(end_year,12,31)], 'range':'minmax'}
                    );
                 results python:[r for r in results if r.getObject()];
                 Batch python:modules['Products.CMFPlone'].Batch;
                 b_start python:request.get('b_start',0);
                 portal_discussion nocall:here/portal_discussion;
                 isDiscussionAllowedFor nocall:portal_discussion/isDiscussionAllowedFor;
                 getDiscussionFor nocall:portal_discussion/getDiscussionFor;
                 home_url python: mtool.getHomeUrl;
                 localized_time python: modules['Products.CMFPlone.PloneUtilities'].localized_time;">
        ...
    </div>

Example 4 - how to get upcoming events of next two months::

    def formatDate(self, event):
        """
        """
        dt = event["start"]
        return  dt.strftime("%d.%m.%Y")

    def update(self):
        portal_catalog = self.context.portal_catalog

        start = DateTime.DateTime() - 1  # yesterday
        end = DateTime.DateTime() + 60   # Two months future
        date_range_query = {'query': (start, end), 'range': 'min:max'}

        count = 5

        self.events = portal_catalog.queryCatalog({"portal_type": "Event",
                                     "start": date_range_query,
                                     "sort_on": "start",
                                     "sort_order": "reverse",
                                     "sort_limit": count,
                                     "review_state": "published"})

More info

* http://www.ifpeople.net/fairsource/courses/material/apiPlone_en

Query by language
=================

You can query by language::

        portal_catalog({"Language":"en"})

.. note::
   plone.app.multilingual must be installed.

Boolean queries (AdvancedQuery)
===============================

AdvancedQuery is an add-on product for Zope's ZCatalog providing queries
using boolean logic. AdvancedQuery is developer level product,
providing Python interface for constructing boolean queries.

AdvancedQuery monkey-patches ``portal_catalog`` to provide
new method ``portal_catalog.evalAdvancedQuery()``.

Example::

    from Products import AdvancedQuery

    portal_catalog = self.portal_catalog # Acquire portal_catalog from higher hierarchy level

    path = self.getPhysicalPath() # Limit the search to the current folder and its children

    # object.getPhysicalPath() returns the path as tuples of path parts
    # Convert path to string
    path = "/".join(path)

    # Limit search to path in the current contex object and
    # match all children implementing either of two interfaces
    # AdvancedQuery operations can be combined using Python expressions & | and ~
    # or AdvancedQuery objects
    query = AdvancedQuery.Eq("path", path) & (AdvancedQuery.Eq("getMyIndexGetter1", "foo") | AdvancedQuery.Eq("getMyIndexGetter2", "bar"))

    # The following result variable contains iterable of CatalogBrain objects
    results = portal_catalog.evalAdvancedQuery(query)

    # Convert the catalog brains to a Python list containing tuples of object unique ID and Title
    pairs = []
    for nc in results:
        pairs.append((nc["UID"], nc["Title"]))


    # query = Eq("path", diagnose_path) & Eq("SearchableText", text_query_target)

    query = Eq("path", diagnose_path) & Eq("SearchableText", text_query_target)

    return self.context.portal_catalog.evalAdvancedQuery(query)

.. note::
   Plone 3 ships with AdvancedQuery but it is not part of Plone. Always declare
   AdvancedQuery dependency in your egg's setup.py install_requires.

.. warning::
   AdvancedQuery does not necessarily apply the same automatic limitations which normal
   portal_catalog() queries do, like language and expiration date.
   Always check your query code against these limitations.

More information

* See AdvancedQuery_.

* https://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/removed-advanced-query


Setting Up A New Style Query
============================

With Plone 4.2, collections use so-called new-style queries by
default. These are, technically speaking, canned queries, and they
appear to have the following advantages over old-style collection's
criteria:

 * They are not complicated sub-objects of collections, but comparably
   simple subobjects that can be set using simple Python expressions.
 * These queries are apparently much faster to execute, as well as
 * much easier to understand, and
 * content type agnostic in the sense that they are no longer tied to
   ArcheTypes.

The easiest way to get into these queries is to grab a debug shell
alongside an instance, then fire up a browser pointing to that
instance, then manipulate the queries and watch the changes on the
debug shell, if you want to experiment. I've constructed a dummy
collection for demonstration purposes, named `testquery`. I've
formatted the output a little, for readability.

Discovering the query:

    >>> site.invokeFactory('Collection', id='testquery') # actually with my browser
    >>> tq = site['testquery']
    >>> tq.getRawQuery()
    [
        {'i': 'created', 'o': 'plone.app.querystring.operation.date.today'},
        {'i': 'Description', 'o': 'plone.app.querystring.operation.string.contains', 'v': 'my querystring'},
        {'i': 'portal_type', 'o': 'plone.app.querystring.operation.selection.is', 'v': ['Document']},
        {'i': 'Subject', 'o': 'plone.app.querystring.operation.selection.is', 'v': ['some_tag']}
    ]
    >>> tq.getSort_on()
    'effective'
    >>> tq.getSort_reversed()
    True
    >>> tq.getLimit()
    1000
    >>> tq.selectedViewFields()
    [
        ('Title', u'Title'),
        ('Creator', 'Creator'),
        ('Type', u'Item Type'),
        ('ModificationDate', u'Modification Date'),
        ('ExpirationDate', u'Expiration Date'),
        ('getId', u'Short Name'),
        ('getObjSize', u'Size')
    ]

This output should be pretty self-explaining: This query finds objects
that were created today, which have "my querystring" in their
description, are of type "Document" (ie, "Page"), and have "some_tag"
in their tag set (you'll find that under "Classification"). Also,
the results are being sorted in reverse order of the Effective Date
(ie, the publishing date). We're getting at most 1000 results, which
is the default cut-off.

You can set the query expression (individual parts are evaluated as logical AND) using

    >>> tq.setQuery( your query expression, see above )

The three parts of an individual query term are

    * 'i': which index to query
    * 'o': which operator to use (see `plone.app.querystring` for a list)
    * 'v': the possible value of an argument to said operator - eg. the query string.

Other parameters can be manipulated the same way:

    >>> tq.setSort_reversed(True)


Accessing metadata
==================

Metadata is collected from the object during cataloging and is copied to brain object
for faster access (no need to wake up the actual object from the database).

ZCatalog brain objects use Python dictionary-like API to access metadata.
Below is a fail-safe example for a metadata access::

    def getImageTag(self, brain):
        """
        Get lead image for ZCatalog brain in folder listing.

        (Based on collective.contentleadimage add-on product)

        @param brain: Products.ZCatalog.Catalog.mybrains object

        @return: HTML source code for content lead <img>
        """

        # First check if the index exist
        if not brain.has_key("hasContentLeadImage"):
            return None

        # Index can have indexed value None or
        # custom value Missing.Value if the indexer
        # for brain's object failed to run or returned Missing.
        # Both of these values evaluate to False in Python
        has_image = brain["hasContentLeadImage"]

        # The value was missing, None or False
        if not has_image:
            return None

        context = brain.getObject()

        # AT inspection API
        field = context.getField(IMAGE_FIELD_NAME)
        if not field:
            return None

        # ImageField.tag() API
        if field.get_size(context) != 0:
            scale = "tile" # 64x64
            return field.tag(context, scale=scale)

.. note::
   This is for example purposes only - the code above is working, but not optimal,
   and can be written up without waking up the object.

Fuzzy search
============

* https://pypi.python.org/pypi/c2.search.fuzzy/

Unique values
=============

ZCatalog has *uniqueValuesFor()* method to retrieve all unique values for a certain index.
It is intended to work on FieldIndexes only.

Example::

    # getArea() is Archetype accessor for area field
    # which is a string and tells the content area.
    # Custom getArea FieldIndex indexes these values
    # to portal catalog.
    # The following line gives all area values
    # inputted on the site.
    areas = portal_catalog.uniqueValuesFor("getArea")


Performance
===========

The following community mailing list blog posts is very insightful about the performance characteristics
of Plone search and indexing:

* http://plone.293351.n2.nabble.com/Advice-for-site-with-very-large-number-of-objects-millions-tp5513207p5529103.html

Batching
========

.. TODO:: Complete writeup

Example::

    results = Batch(contents, self.b_size, self.b_start, orphan=0)

* orphan - the next page will be combined with the current page if it does not contain more than orphan elements

Walking through all content
===========================

``portal_catalog()`` call without search parameters will return all indexed
site objects.

Here is an example how to crawl through Plone content to search HTML
snippets. This can be done by rendering every content object and check
whether certain substrings exists the output HTML This snippet can be
executed through-the-web in the Management Interface.

This kind of scripting is especially useful if you need to find old links or
migrate some text / HTML snippets in the content itself. There might be
artifacts which only appear on the resulting pages (portlets, footer texts,
etc.) and thus they are invisible to the normal full text search.

Example::

    # Find arbitrary HTML snippets on Plone content pages

    # Collect script output as text/html, so that you can
    # call this script conveniently by just typing its URL to a web browser
    buffer = ""

    # We need to walk through all the content, as the
    # links might not be indexed in any search catalog
    for brain in context.portal_catalog(): # This queries cataloged brain of every content object
        try:
            obj = brain.getObject()
            # Call to the content object will render its default view and return it as text
            # Note: this will be slow - it equals to load every page from your Plone site
            rendered = obj()
            if "yourtextmatch" in rendered:
                # found old link in the rendered output
                buffer += "Found old links on <a href='%s'>%s</a><br>\n" % (obj.absolute_url(), obj.Title())
        except:
            pass # Something may fail here if the content object is broken

    return buffer

More info:

* http://blog.mfabrik.com/2011/02/17/finding-arbitary-html-snippets-on-plone-content-pages/

Other notes
===========

* `Indexing tutorial <https://plone.org/documentation/tutorial/using-portal_catalog/tutorial-all-pages>`_ on plone.org

* `Manual sorting example <http://www.universalwebservices.net/web-programming-resources/zope-plone/advanced-sorting-of-plone-search-results/>`_

* `Getting all unique keywords <http://stackoverflow.com/questions/10497342/python-plone-getting-all-unique-keywords-subject>`_

.. _AdvancedQuery: http://www.dieter.handshake.de/pyprojects/zope/AdvancedQuery.html

.. _ExtendedPathIndex: https://github.com/plone/Products.ExtendedPathIndex/blob/master/README.txt

.. _PluginxIndexes: http://svn.zope.org/Zope/trunk/src/Products/PluginIndexes/
