=========
Relations
=========

.. contents :: :local:

.. admonition:: Description

        Create relations between portal-types model-driven. Support for
        Relations Product (complex references). Define sets of rules for
        validation, creation and lifetime of Archetypes references. ArchGenXML
        can generate the necessary code and XML-configuration data to use this
        product.

Prerequisites
-------------
To enable Relations install the Product (`code-location <http://plone.org/products/relations/>`_).

Basics
------
As an option on command line, up to a tagged-value on model-level or on a single UML-Association you just define the ``relation_implementation`` and set it to ``relations``. A directed Assoziation results in one Relation.

**Give the association and its assoziation ends names.** They'll be used as the names for the RelationField. If you dont want a field turn it off by setting a tagged value ``generate_reference_fields`` on class (or package, model) level to ``0``.

Inverse Relation
----------------
If the association is not directed (navigable on both association ends) an inverse relation will be created.

The tagged-value ``inverse_relation_name`` will be used for the back-relation on undirected associations. It defaults to a relation named ``toend_fromend``, where these are the lowercased versions of the association ends. If the two ends are named the same, then the relation will be named ``association_inv``, where ``association`` is the name of the association. (Finally, if the option ``old_inverse_relation_name`` is set, then it defaults to the association name postfixed by ``_inverse``.)

Cardinality
-----------
You can use the Multiplicity on in UML to define the cardinality of an Relation.
You can use the minimum and maximun value here using the syntax ``1..5`` which means at least one relationrelated objects but not more than five.

Constraints
-----------
type-constraint
   as described above an association between two portal-types will be created.

interface-constraint
   an association between an archetypes class and an interface will create an interface-constraint. the relation is allowed to all classes implementing this interface.

Association classes
-------------------
Association classes can be used to store data on the relation as an object. You can model it using the UML association class or using a tagged value ``association_class`` on the association.
