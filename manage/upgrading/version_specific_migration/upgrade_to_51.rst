==========================
Upgrading Plone 5.0 to 5.1
==========================


.. admonition:: Description

   Instructions and tips for upgrading to Plone 5.1

.. note::

   If you want to upgrade add-ons to Plone 5.1, also see: ../../../develop/addons/upgrade_to_51.rst

General information
===================

- Before you upgrade read :doc:`../into.rst` and :doc:`../preparations.rst`.
- Always upgrade from the latest version of 5.0.x to the latest version of 5.1.x. This will resolve many migration-specific issues.
- If you have problems don't be afraid to ask for help on http://community.plone.org

Changes between Plone 5.0 and 5.1
=================================

The following Plone Improvement Proposals have been implemented for 5.1:

* `Meta bundles generation <https://github.com/plone/Products.CMFPlone/issues/1277>`_
* `Portal actions control panel <https://github.com/plone/Products.CMFPlone/issues/1342>`_
* `Add direct link from a group name on Sharing tab to that group's member list <https://github.com/plone/Products.CMFPlone/issues/1310>`_
* `Remove plone.app.openid from core <https://github.com/plone/Products.CMFPlone/issues/1659>`_
* `Get rid of portal_quickinstaller <https://github.com/plone/Products.CMFPlone/issues/1340>`_
* `Add support for conditionally import registry records  <https://github.com/plone/Products.CMFPlone/issues/1406>`_
* `Auto-Rotation for Images <https://github.com/plone/Products.CMFPlone/issues/1673>`_
* `assimilate collective.indexing <https://github.com/plone/Products.CMFPlone/issues/1343>`_
* Use lxml cleaner for savehtml transforms
* `Easily change default search order <https://github.com/plone/Products.CMFPlone/issues/1600>`_
* `HiDPI image scales <https://github.com/plone/Products.CMFPlone/issues/1483>`_
* `Registry Improvements <https://github.com/plone/Products.CMFPlone/issues/1484>`_
* `Cleanup and enhance icon and thumb aspects <https://github.com/plone/Products.CMFPlone/issues/1734>`_

For details about rejected or posponed PLIPs see https://github.com/plone/Products.CMFPlone/projects/1 and https://docs.google.com/spreadsheets/d/15Cut73TS5l_x8djkxNre5k8fd7haGC5OOSGigtL2drQ/


Know issues
===========

Catalog-Errors in tests or the migration from Archetypes to Dexterity
---------------------------------------------------------------------

With the PLIP `assimilate collective.indexing <https://github.com/plone/Products.CMFPlone/issues/1343>`_ the operations for indexing, reindexing and unindexing are queued, optimized and only processed at the end of the transaction. Only one indexing operation is done per object on any transaction. Some tests and features might expect that objects are being indexed/reindexed/unindexed right away.

You can disable queuing alltogether by setting the environment-variable `CATALOG_OPTIMIZATION_DISABLED` to `1`:

.. code-block:: bash

    CATALOG_OPTIMIZATION_DISABLED=1 ./bin/instance start

Here is a example of a traceback that happened when migrating topics from Archetypes to Dexterity that can be prevented with this:

.. code-block::

    (...)
      Module plone.app.contenttypes.migration.browser, line 227, in __call__
      Module plone.app.contenttypes.migration.topics, line 702, in migrate_topics
      Module Products.contentmigration.basemigrator.walker, line 144, in go
      Module Products.contentmigration.basemigrator.walker, line 177, in migrate
      Module Products.contentmigration.walker, line 64, in walk
      Module Products.ZCatalog.CatalogBrains, line 93, in getObject
      Module Products.ZCatalog.CatalogBrains, line 57, in getPath
      Module Products.ZCatalog.ZCatalog, line 518, in getpath
    KeyError: 487546660

It is probably a good idea to set `CATALOG_OPTIMIZATION_DISABLED=1` when upgrading or migrating.

You can also force processing the queue directly in your code with:

.. code-block:: python

    from Products.CMFCore.indexing import processQueue
    processQueue()

For an example see https://github.com/plone/plone.app.upgrade/pull/75/files
