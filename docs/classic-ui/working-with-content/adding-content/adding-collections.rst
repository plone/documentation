==================
Adding Collections
==================

Collections (formerly called Smart Folders) are virtual containers of
lists of items found by doing a specialized search.

See the later section of the manual :doc:`../using-collections/index`

Choose "Collection" in the *Add new...* menu for a folder to start defining your collection:

.. figure:: ../../_robot/adding-collections_add-menu.png
   :align: center
   :alt: add new collection menu image

Select **Collection** from the drop-down menu, and you'll see the *Add Collection* panel:

.. figure:: ../../_robot/adding-collections_add-form.png
   :align: center
   :alt: collection form


Apart from the usual fields, the interesting part starts with the **Search terms**

.. figure:: ../../_robot/collection-criteria.png
   :align: center
   :alt:


You can pick all *meta-data* that Plone has on content items as criteria.
By combining more criteria, you can create sophisticated queries, which will be automatically updated.

Your collection can search for all items of types ``Page`` and ``News Item`` that have a Tag of ``Sport``, created in the last 3 months.
Or all ``Events`` that have a Start date in the next month.

The possibilities are endless, and Plone will always show the results according to the criteria.

If you create a new content item later with the tag of "Sport", it will automatically show up in the collection you have just defined.

History
-------

Collections have been around under various names. They used to be called "Smart Folders" in earlier versions of Plone, and you may find references to that in older documentation. It may even be that your site has so-called "Old Style collections" enabled as well.

See the later section of the manual :doc:`../using-collections/index`
