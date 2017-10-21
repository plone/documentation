==========================
Upgrading Plone 5.0 to 5.1
==========================


.. admonition:: Description

   Instructions and tips for upgrading to Plone 5.1

.. note::

   If you want to upgrade add-ons to Plone 5.1, please see :doc:`/develop/addons/upgrade_to_51`

General Information
===================

- Before you upgrade read :doc:`../intro` and :doc:`../preparations`.
- Always upgrade from the latest version of 5.0.x to the latest version of 5.1.x.
  This will resolve many migration-specific issues.
- If you have problems don't be afraid to ask for help on https://community.plone.org

Changes Between Plone 5.0 And 5.1
=================================

The following Plone Improvement Proposals have been implemented for 5.1:

* `Meta bundles generation`_
* `Portal actions control panel`_
* `Add direct link from a group name on Sharing tab to that group's member list <https://github.com/plone/Products.CMFPlone/issues/1310>`_
* `Remove plone.app.openid from core <https://github.com/plone/Products.CMFPlone/issues/1659>`_
* `Get rid of portal_quickinstaller <https://github.com/plone/Products.CMFPlone/issues/1340>`_
* `Add support for conditionally import registry records  <https://github.com/plone/Products.CMFPlone/issues/1406>`_
* `Auto-Rotation for Images <https://github.com/plone/Products.CMFPlone/issues/1673>`_
* `assimilate collective.indexing <https://github.com/plone/Products.CMFPlone/issues/1343>`_
* `Use lxml cleaner for savehtml transforms <https://github.com/plone/Products.CMFPlone/issues/1343>`_
* `Easily change default search order <https://github.com/plone/Products.CMFPlone/issues/1600>`_
* `HiDPI image scales <https://github.com/plone/Products.CMFPlone/issues/1483>`_
* `Registry Improvements <https://github.com/plone/Products.CMFPlone/issues/1484>`_
* `Cleanup and enhance icon and thumb aspects <https://github.com/plone/Products.CMFPlone/issues/1734>`_

For details about rejected or posponed PLIPs see https://github.com/plone/Products.CMFPlone/projects/1
and https://docs.google.com/spreadsheets/d/15Cut73TS5l_x8djkxNre5k8fd7haGC5OOSGigtL2drQ/


Upgrading
=========

To run the upgrade to 5.1 follow the links on top of the controlpanel or the ZMI to the form `/@@plone-upgrade`


Major changes
=============

These are details of the major changes that are in Plone 5.1 through the PLIP (Plone Improvement Proposal) process.

Meta bundles generation
-----------------------

This is `PLIP 1277 <https://github.com/plone/Products.CMFPlone/issues/1277>`_.

For end users
^^^^^^^^^^^^^

Pages will load faster because JavaScript and CSS resources are bundled.
An anonymous user will usually get one JavaScript file and one CSS file, instead of multiple.

For developers
^^^^^^^^^^^^^^

To make use of this, you should register your resource bundle to merge with the ``default`` or ``loggedin`` bundle.

.. code-block:: python

  <records prefix="plone.bundles/my-addon"
            interface='Products.CMFPlone.interfaces.IBundleRegistry'>
    <value key="merge_with">default</value>
    ...
  </records>

See :ref:`Aggregate Bundles for Production <resource_bundle_aggregation>`.

Portal actions control panel
----------------------------

This is `PLIP 1342 <https://github.com/plone/Products.CMFPlone/issues/1342>`_.

For end users
^^^^^^^^^^^^^

You can manage the actions from Site Setup using the Actions control panel.
See :ref:`Creating actions through-the-web <create_actions_ttw>`.

For developers
^^^^^^^^^^^^^^

Nothing changes.


Known Issues
============

Catalog-Errors During Upgrades
------------------------------

With the PLIP `assimilate collective.indexing <https://github.com/plone/Products.CMFPlone/issues/1343>`_ the operations for indexing,
reindexing and unindexing are queued, optimized and only processed at the end of the transaction.

Only one indexing operation is done per object on any transaction.
Some tests and features might expect that objects are being indexed/reindexed/unindexed right away.

You can disable queuing altogether by setting the environment-variable `CATALOG_OPTIMIZATION_DISABLED` to `1`:

.. code-block:: console

    CATALOG_OPTIMIZATION_DISABLED=1 ./bin/instance start

It is a good idea to set `CATALOG_OPTIMIZATION_DISABLED=1` when upgrading if you get error messages related to the catalog.
