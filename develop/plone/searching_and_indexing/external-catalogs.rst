.. _using_external_catalogs:

=======================
Using external catalogs
=======================

.. admonition:: Description

    The Plone catalog can be extend to use external catalogs like Solr or Elasticsearch.
    Add-ons like collective.solr use that to hook into the catalog API and do some Indexing outside of Plone in Solr,
    which increases performance and flexibility of indexing a lot.


Implement IIndexingQueueProcessor
---------------------------------

To hook into the catalog one can implement the IIndexingQueueProcessor
`interface from Products.CMFCore <https://github.com/zopefoundation/Products.CMFCore/blob/master/Products/CMFCore/interfaces/_tools.py>`_.


.. versionadded:: 5.1
   For Plone versions **before 5.1** you need to use the
   `interfaces from collective.indexing <https://github.com/plone/collective.indexing/blob/master/src/collective/indexing/interfaces.py>`_ package!


.. code-block:: python

    class IIndexQueueProcessor(IIndexing):
        """A queue processor, i.e. an actual implementation of index operations
        for a particular search engine, e.g. the catalog, solr etc
        """

        def begin():
            """Called before processing of the queue is started"""

        def commit():
            """Called after processing of the queue has ended"""

        def abort():
            """Called if processing of the queue needs to be aborted"""


Implement IIndexing
-------------------

And also the underlying IIndexing interface.

.. code-block:: python

    class IIndexing(Interface):
        """ interface for indexing operations, used both for the queue and
            the processors, which perform the actual indexing;  the queue gets
            registered as a utility while the processors (portal catalog, solr)
            are registered as named utilties """

        def index(obj, attributes=None):
            """ queue an index operation for the given object and attributes """

        def reindex(obj, attributes=None):
            """ queue a reindex operation for the given object and attributes """

        def unindex(obj):
            """ queue an unindex operation for the given object """

Example implementation
----------------------

For an example implementation of an external IndexingQueueProcessor,
look at the `SolrIndexProcessor <https://github.com/collective/collective.solr/blob/master/src/collective/solr/indexer.py>`_ of
`collective.solr <https://github.com/collective/collective.solr/>`_, which implements ISolrIndexQueueProcessor (IIndexQueueProcessor).

Catalog queue and tests
-----------------------

When running tests,
specially during the transition to Plone 5.1,
some tests might fail due to the queue holding back and processing until a transaction happens.

If that behavior is not desired one can use the ``CATALOG_OPTIMIZATION_DISABLED`` environment variable to disable the catalog queue.

.. code-block:: shell

    CATALOG_OPTIMIZATION_DISABLED=y ./bin/test
