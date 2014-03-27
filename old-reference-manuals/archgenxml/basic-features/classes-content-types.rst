=======================
Classes / Content Types
=======================

.. contents :: :local:

.. admonition:: Description

        Use classes to generate content types and portal tools.

Overview
--------
By default, when you create a class in your class diagram, it represents an
Archetypes content type. You can add operations in your model to generate
methods on the class, and attributes to generate fields in the schema. The
quick reference at the end of this tutorial will tell you which field types
you can use. You should also browse the "Archetypes quick reference
documentation":/documentation/manual/archetypes-developer-manual/fields to
see what properties are available for each field and widget type. You may set
these using tagged values (see below).

There are three basic ways in which you can alter the way your content types
are generated:

* You may set one or more stereotypes on your class, which alters the "type" of class. A stereotype ``<<portal_tool>>``, for example means you are generating a portal tool rather than just a simple content type.
* You can use tagged values in your model to configure many aspects of your classes, their attributes and their methods. A list of recognised tagged values acting on classes, fields and methods are found in the "quick reference":archgenxmlquickref at the end of this tutorial.

When reading tagged values, ArchGenXML will generally treat them as strings, with a few exceptions where only non-string values are permitted, such as the ``required`` tagged value. If you do not wish your value to be quoted as a string, prefix it with ``python:``. For example, if you set the tagged value ``default`` to ``python:["high", "low"]`` on a ``lines`` attribute, you will get ``default=["high", "low"]`` in a LinesField in your schema.

* ArchGenXML is clever about aggregation and composition. If your class aggregates other classes, it will be automatically made into a folder with those classes as the allowed content types. If you use composition (signified by a filled diamond in the diagram) rather than aggregation, the contained class will only be addable inside the container, otherwise it will be addable globally in your portal by default.

Variants of Content Types
-------------------------
Simple Classes
^^^^^^^^^^^^^^
A simple class is what we had in HelloWorld in the previous chapter.
A simple class is based on ``BaseContent`` and ``BrowserDefault``. This is the default if no other options override.

Folderish Classes
^^^^^^^^^^^^^^^^^
The easiest way to make a content type folderish is to introduce composition
or aggregation in your model - the parent class will become folderish and will
be permitted to hold objects of the child classes. You can also make a class
folderish just by giving it the ``<<folder>>`` stereotype. Both of these
approaches will result in an object derived from ``BaseFolder``.

You can also give a class the ``<<ordered>>`` stereotype (possibly in addition
to ``<<folder>>``) in order to make it derive from ``OrderedBaseFolder`` and thus
have ordering support. Alternatively, you can set the ``base_class`` tagged
value on the class to ``OrderedBaseFolder``. This is a general technique which
you can use to override the base folder should you need to. As an aside, the
``additional_parents`` tagged value permits you to derive from multiple parents.

Another option is to derive from ATFolder (from ATContentTypes) by giving the
class the stereotype ``<<atfolder>>``.

Other tagged values which may be useful when generating folders are:

filter_content_types -- Set this to ``0`` or ``1`` to turn on/off filtering of
content types. If content types are not filtered, the class will act as a
general folder for all globally addable content.

allowed_content_types -- To explicitly set the allowable content types, for
example to only allow images and documents, set this to: 'Image, Document'.
Note that if you use aggregation or composition to create folderish types as
described above, setting the allowed content types manually is not necessary.

Portal tools
------------
A portal tool is a unique singleton which other objects may find via
``getToolByName`` and utilise. There are many tools which ship with Plone,
such as portal_actions or portal_skins. To create a portal tool instead of
a regular content type, give your class the ``<<portal_tool>>`` stereotype.
Tools can hold attributes and provide methods just like a regular content
type. Typically, these hold configuration data and utility methods for the
rest of your product to use. Tools may also have configlets - configuration
pages in the Plone control panel. See the quick reference at the end of this
document for details on the tagged values you must set to generate configlets.

Abstract mixin classes
----------------------
By marking your class as ``abstract`` in your model (usually a separate
tick-box), you are signifying that it will not be added as a content type.
Such classes are useful as mixin parents and as abstract base classes for more
complex content types, and will not have the standard Archetypes registration
machinery, factory type information or derive from BaseClass.

Stub classes
------------
By giving your class the ``<<stub>>`` stereotype, you can prevent it from being
generated at all. This is useful if you wish to show content types which are
logically part of your model, but which do not belong to your product. For
instance, you could create a stub for Plone's standard Image type if you wish
to include this as an aggregated object inside your content type - that is,
your content type will become folderish, with Image as an allowable contained
type.

Deriving/Subclassing Classes
----------------------------
Deriving or subclassing a class is used to extend existing classes, or change
their behavior. Using generalisation arrows in your model, you can inherit
the methods and schema from another content type or mixin class in your class.

Simple Derivation
^^^^^^^^^^^^^^^^^
All content types in Archetypes are derived from one of the base classes -
BaseContent, BaseFolder, OrderedBaseFolder and so on. If you wish to turn
this off, for example because the base class is being inherited from a
parent class, you can set the ``base_class`` tagged value to ``0``.

Multiple Derivation
^^^^^^^^^^^^^^^^^^^
You can of course use multiple inheritance via multiple generalisation
arrows in your model. However, if you need to use a base class that is not
on your model, you can set the ``additional_parents`` tagged value on your
class to a comma-separated list of parent classes.

Deriving from other Products
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
If you want to derive from a class of an other product create a stub class
with a tagged value ``import_from``: This will generate a import line
``from VALUE import CLASSNAME`` in classes derived from this class.

Deriving form ATContentTypes
^^^^^^^^^^^^^^^^^^^^^^^^^^^^
To derive from ATDocument just use a stereotype ``<<atdocument>>``. Also
possible with ``<<atfile>>``, ``<<atevent>>`` and ``<<atfolder>>``.

Packages - bring order to your code
-----------------------------------
Packages are both a UML concept and a Python concept. In Python, packages are
directories under your product containing a set of modules (.py files). In
UML, a package is a logical grouping of classes, drawn as a large "folder"
with classes inside it. To modularise complex products, you should use
packages to group classes together.
