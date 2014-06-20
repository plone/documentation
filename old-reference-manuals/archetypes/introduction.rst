===============
Introduction
===============

What is Archetypes?
---------------------

.. admonition:: Description

		Brief presentation of Archetypes.


Archetypes is a framework for developing new content types for a Plone
project. Most content management projects involve introducing new types
of content, which in the non-trivial case requires an informed
understanding of how Zope and the CMF work. Archetypes provides a
simple, extensible framework that can ease both the development and
maintenance costs of CMF content types while reducing the learning curve
for the simpler cases.

Compared to building content types using the stock CMF (through
subclassing), Archetypes gives you the following advantages:

#. automatically generates forms and views;
#. provides a library of stock field types, form widgets, and field
   validators;
#. allows defining custom fields, widgets, and validators;
#. automates transformations of rich content;
#. a built-in reference engine that gives the ability to link two
   objects together with a relation; such a “link” from a given object
   to another one is a Python object called a *reference*.

Since Plone 2.1, Archetypes has become the de-facto way of developing
new content types, and a majority of third party products that are
released these days use Archetypes.

Archetypes schemas
--------------------

.. admonition:: Description

		Introducing Archetypes-based schemas and fields.

Archetypes provides a robust framework for storing data attributes on
content objects.  This framework consist of a number of **Fields**
stored in a container called a **Schema**. Fields are simply specialized
Python classes that allow you to store and retrieve data associated with
an Archetypes object.

Fields provide a few functionalities. First, there are specialized field
types for strings, lists of strings, integers, floating-point numbers,
etc., that allow special handling of fields based on the type of data
stored.

Some definitions
~~~~~~~~~~~~~~~~

Before we go diving in, let’s define some often-used terms:

-  Field: An Archetypes Field. This refers to an instance of a Field
   class defined in a Schema.
-  Schema: The “container” that Archetypes uses to store fields.
-  Schemata: A named grouping of fields. One Schema can have many
   schematas.
-  AT: Abbreviation for Archetypes.

Fields, Classes, and Objects
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Archetypes Fields are Python objects contained within the Schema. A
Field is defined once for an Archetypes content class. This single Field
instance is used for every instance of that class.  Therefore, the
relationship between Field instances and content classes is described as
such: “A field instance belongs to exactly one class.” A class, however,
can have many *different* Field instances. Furthermore, every instance
of an AT class uses the *same* set of Fields.  AT objects themselves do
not contain unique Fields.

When Zope starts up, during product initialization, Archetypes reads the
schema of the registered classes and “automagically” generates methods
to read (the *accessor*) and change (the *mutator*) each of the fields
defined.

Stock schemas
~~~~~~~~~~~~~

Archetypes includes three stock schemas:

-  BaseSchema: defines a normal content type,
-  BaseFolderSchema: defines a folderish content type (object can
   contain other objects),
-  BaseBTreeFolderSchema: for folders which need to handle hundreds or
   thousands of objects (even up to millions).

All three include two fields, ``id`` and ``title``, as well as the
standard Dublin Core metadata fields.

Modifying the fields of an existing schema
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Modifying an existing schema field is possible using the syntax
``schema['<field_name>'].attribute = value``. For example, to change the
label of the *description* field widget (already available in
*BaseSchema*), you can write (*in your defined schema definition that
reuses BaseSchema*):

::

    schema['description'].widget.label = u'Summary'

The fields in the schema are ordered, and normally first fields come
first in “add” and “edit” forms. To rearrange a field within the schema
use the ``moveField`` method:

-  Place it before a specific field:
   ``schema.moveField('<field_to_move>', before='<field_to_place_it_before>')``
-  Place it after a specific field:
   `` schema.moveField('<field_to_move>', after='<field_to_place_it_after>')``
-  Place it at the top of the schema:
   `` schema.moveField('<field_to_move>', pos='top')``
-  Place it at the bottom:
   `` schema.moveField('<field_to_move>', pos='bottom')``
-  Place it in a specific position:
   `` schema.moveField('<field_to_move>', pos=0)``


What is ATContentTypes?
--------------------------

.. admonition:: Description

		ATContentTypes is the Plone core product that provides the default
		content types (since Plone 2.1).

One of the major changes introduced in Plone 2.1 was that the core
content types (Page, Image, etc) were changed from being based on stock
CMF types, to using Archetypes. The new core types are housed in the
ATContentTypes product.

ATContentTypes introduces a number of base classes and tools that
provide common “Plone-ish” behaviour. This includes things like support
for the “display” menu and the “more…” menu and restrictions for the
“add item” menu.

You can use ATContentTypes’ base classes and tools in your own products.
The `RichDocument tutorial`_ covers the core techniques, and is probably
a good place to go when you have finished this reference.

.. _RichDocument tutorial: /documentation/tutorial/richdocument

