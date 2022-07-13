===========
Collections
===========

.. admonition:: Description

     Collections are site editor enabled searches.  They provide automatic, folder like view, for the content fetched from the Plone site by criteria defined by the site editor.


Introduction
------------

.. note:: In Plone 4.2, old style collections have been replaced with new style collections, featuring a vastly improved user interface and a de-coupling from the ATTopic content type (i.e. they no longer use ATTopic).

They are useful to generate different listings.

Collections are internally called "topics" and the corresponding content type is "ATTopic" (< 4.2 only). Collections were renamed from topics in Plone 3.0.

Collection searches are driven by two factors:

* User visible "criteria" which is mapped to portal_catalog queries

* portal_catalog() indexes which you need to add yourself for custom content types. Read more about them in :doc:`Searching and Indexing chapter </develop/plone/searching_and_indexing/index>`

Add new collection criteria (new style, plone.app.collection installed)
-----------------------------------------------------------------------
How to add your own criteria to a collection
plone.app.collection and (or more precisely the underlying plone.app.querystring) uses plone.app.registry records to define possible search criteria for a collection.

If you want to add your own criteria, say to choose a value from a custom index, you have to create a plone.app.registry record for this index in your generic setup profile (e.g profiles/default/registry.xml)::

    <registry>
      <records interface="plone.app.querystring.interfaces.IQueryField"
               prefix="plone.app.querystring.field.department">
        <value key="title">Department</value>
        <value key="description">A custom department index</value>
        <value key="enabled">True</value>
        <value key="sortable">False</value>
        <value key="operations">
            <element>plone.app.querystring.operation.string.is</element>
        </value>
        <value key="group">Metadata</value>
      </records>
    </registry>

The title-value refers to the custom index ("Department"), the operations-value is used to filter the items and the group-value defines under which group the entry shows up in the selection widget.

Note

For a full list of all existing QueryField declarations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L197

For a full list of all existing operations see https://github.com/plone/plone.app.querystring/blob/master/plone/app/querystring/profiles/default/registry.xml#L1

Adding new collection criteria (old style, < 4.2 only)
------------------------------------------------------

portal_catalog search indexes are not directly exposed to the collection
criteria management backend, since portal_catalog indices do not support
features like localization and user-friendly titles.

.. note:: In Plone 4.2, the Collection configlet is no longer listed in Site Setup. But you can still access it here: http://localhost:8080/Plone/portal_atct/atct_manageTopicIndex.

New criteria can be created through-the-web in Site setup -> Collection section.  Click "All fields" to see unenabled portal_catalog criteria.  Later the edited settings can be exported to GenericSetup XML profile using portal_setup tool (no need to create profile XMl files by hand).

portal_catalog indices can be added through-the-web (TTW) through the Management Interface portal_catalog tool tabs.

If you still want to create XML files by hand, read more about it in `Enable Collection Indices (fields for searching) for custom types HOW TO <https://plone.org/documentation/how-to/enable-collection-indices-fields-for-searching-for-custom-types>`_.

Sticky sorting
--------------

See:

* http://stackoverflow.com/questions/8791132/how-to-create-sticky-news-items-in-plone-4
