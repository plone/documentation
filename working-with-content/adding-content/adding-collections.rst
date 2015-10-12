Adding collections
========================

Collections (formerly called Smart Folders) are virtual containers of
lists of items found by doing a specialized search.

See the later section of the manual :doc:`../using-collections/index`

.. include:: ../../_robot.rst

Choose "Collection" in the *Add new...* menu for a folder to start defining your collection:

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show add collection menu
       Go to  ${PLONE_URL}
       Wait until element is visible
       ...  css=span.icon-plone-contentmenu-factories
       Click element  css=span.icon-plone-contentmenu-factories
       Wait until element is visible
       ...  css=#plone-contentmenu-factories li.plone-toolbar-submenu-header

       Mouse over  collection
       Update element style  portal-footer  display  none

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/adding-collections_add-menu.png
       ...  css=div.plone-toolbar-container
       ...  css=#plone-contentmenu-factories ul

.. figure:: ../../_robot/adding-collections_add-menu.png
   :align: center
   :alt: add new collection menu image

Select **Collection** from the drop-down menu, and you'll see the *Add Collection* panel:



.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   Show new collection add form
       Page should contain element  collection
       Click link  collection
       Wait until element is visible
       ...  css=#mceu_16-body
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/adding-collections_add-form.png
       ...  css=#content

.. figure:: ../../_robot/adding-collections_add-form.png
   :align: center
   :alt: collection form


Apart from the usual fields, the interesting part starts with the **Search terms**

.. code:: robotframework
   :class: hidden

   *** Test Cases ***

   select criteria
       Go to  ${PLONE_URL}/++add++Collection
       Click element  css=div.querystring-criteria-index a
       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/collection-criteria.png
       ...  css=div.select2-drop-active

.. figure:: ../../_robot/collection-criteria.png
   :align: center
   :alt:


You can pick all *meta-data* that Plone has on content items as criteria.
By combining more criteria, you can create sophisticated queries, which will be automatically updated.

So your collection can search for all items of types ``Page`` and ``News Item`` that have a Tag of ``Sport``, created in the last 3 months.
Or all ``Events`` that have a Start date in the next month.

The possibilities are endless, and Plone will always show the results according to the criteria.
So if you create a new content item later with the tag of "Sport", it will automatically show up in the collection you have just defined.

History
-------

Collections have been around under various names. They used to be called "Smart Folders" in earlier versions of Plone, and you may find references to that in older documentation. It may even be that your site has so-called "Old Style collections" enabled as well.

See the later section of the manual :doc:`../using-collections/index`