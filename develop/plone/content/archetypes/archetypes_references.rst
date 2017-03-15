==========================
Archetypes ReferenceFields
==========================

.. admonition:: Description

    Using ReferenceField to have references to other Archetypes content
    items in Plone.


Introduction
============

Archetypes comes with a kind of field called ReferenceField which is used
to store references to other Archetypes objects, or any object providing the
IReferenceable interface.

References are maintained in the ``uid_catalog`` and ``reference_catalog``
catalogs.  You can find both at the root of your Plone site. Check them to
see their indexes and metadata.

Although you could use the ZCatalog API to manage Archetypes references,
these catalogs are rarely used directly. A ``ReferenceField`` and its API is
used instead.

Example declaration of a ``ReferenceField`` inside a schema::

    MyCTSchema = atapi.Schema((
    ...
        atapi.ReferenceField('myReferenceField',
            relationship = 'somerelationship',
            ),
    ...
    ))

Check the *Fields Reference* section in the *Archetypes Developer Manual* at
https://plone.org to learn about the ``ReferenceField`` available options.

Archetypes reference fields just store the UID (Universal Object Identifier)
of an object providing the ``IReferenceable`` interface. Continuing with the
example above, you will usually use the regular field API (getters/setters).

Get the UID of a referenceable object::

    >>> areferenceableobject_uid = areferenceableobject.UID()

To set a reference, you can use the the setter method with either a list of
UIDs or one UID string, or one object or a list of objects (in the case the
``ReferenceField`` is multi-valued) to which you want to add a reference to.
``None`` and ``[]`` are equal.

In this example we set a reference from the ``myct1`` object to the
``areferenceableobject`` object::

    >>> myct1.setMyReferenceField(areferenceableobject_uid)

To get the object(s) referenced, just use the getter. Note that what you get
is the objects themselves, not their
":doc:`brains </develop/plone/searching_and_indexing/query>`"::

.. TODO:: Add a glossary entry for brains.

:doc:`More info in Varnish section of this manual </manage/deploying/caching/varnish3>`.

    >>> myct1.getMyReferenceField() == areferenceableobject
    True

.. TODO::

    Code to exercise the ``IReferenceable`` API, including relationships and
    back-references.

