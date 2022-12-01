Adding Collections
=======================

Collections (formerly called Smart Folders) are virtual containers of
lists of items found by doing a specialized search.

Learning to think about content being stored wherever it is stored, and
about using custom collections to gather up different "views" of the
content, is an important step to using Plone most effectively. It is an
intelligent system.

To add a collection, use the *Add new...* menu, as for adding other
content types:

.. figure:: /_static/p4_addnewmenu.png
   :align: center
   :alt: p4\_addnewmenu

   p4\_addnewmenu

You will see the Add*Collection*panel:

.. figure:: /_static/copy_of_p4_addcollection.png
   :align: center
   :alt: p4\_addcollection2

   p4\_addcollection2

Below the title and description fields is a set of fields for specifying
the format of search results returned by the search criterion for the
new collection. The four fields in the panel above are in pairs. The top
two fields let you limit the search results to a number of items that
will be displayed. The bottom two fields let you control the order of
the search result items.

Setting the search criterion
----------------------------

After setting the display configuration in the edit panel shown above,
click the criteria tab to show the panel for setting search criteria:

.. figure:: /_static/copy2_of_copy_of_p4_collectionssearchcrit1.png
   :align: center
   :alt: p4\_collectionssearchcrit1 2

   p4\_collectionssearchcrit1 2

The top area of the panel, *Add New Search Criteria*, lets you set a
field and a matching criterion. The bottom area, *Set Sort Order*, is a
simple selection for a field to sort on:

.. figure:: /_static/copy_of_p4_collectionssearchcrit2.png
   :align: center
   :alt: p4\_collectionssearchcrit2 2

   p4\_collectionssearchcrit2 2

The criteria types for matching data in content items depend on which
field is selected.

After saving the collection, the search criteria will be applied and the
results shown when the collection is clicked. You can create any number
of collections for such custom views. For the butterfly example
described above, in addition to a date constraint to find recent items,
the categories field could be used to match color to have a series of
collections for "Blue Butterflies," "White Butterfles," etc.

Multiple criteria can be used for a collection. For example, a
collection called "Butterflies Photographed in the Last Month," could be
made by setting a criterion on Creation Date and on Item Type as Image.
Such date-based collections are really effective to show up-to-date
views of content that don't require any administrative hand-work -- once
such a collection has been created, it will automatically stay up to
date.

*Note:* A collection doesn't behave like a normal folder, you can't
add content items via the add item menu, as you can for a normal folder.

