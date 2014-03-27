=======================
Manipulating objects
=======================

.. contents :: :local:

Introduction
============

Manipulating objects depends on whether they are based on the Archetypes
subsystem or on the Dexterity subsystem.

For more information, consult the manual of the relevant subsystem:

* `Archetypes examples <http://plone.org/documentation/tutorial/manipulating-plone-objects-programmatically/reading-and-writing-field-values>`_.

* See `Manipulating Content Objects </reference_manuals/external/plone.app.dexterity/reference/manipulating-content-objects.html>`_ in the Dexterity manual

Reindexing modified objects
===========================

After modifying the object, you need to reindex it in the ``portal_catalog``
to update the search and listing information.

Cataloging has a quirk regarding the ``modified`` metadata: when calling
``reindexObject`` on an object, the value for ``modified`` in
``portal_catalog`` will be set to the time of the reindex, regardless of the
value of the modified property of the object. 

In order to store the correct value you can do an extra reindex of the
object with the ``modified`` index as parameter.

First do a normal ``reindexObject``, then call it with the modified index
explicitly::

        object.reindexObject()
        object.reindexObject(idxs=['modified']) 

For more information, see :doc:`\** How to update this document </develop/plone/searching_and_indexing/indexing>`.
