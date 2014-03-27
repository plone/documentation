============================
CompoundField and ArrayField
============================

.. contents :: :local:

.. admonition:: Description

        How to make custom fields: a list of some default field type, a
        compound of a two or more default fields.

Prerequisites
-------------
Install the `CompoundField <http://plone.org/products/compoundfield>`_ extension into you Products folder.

List of fields - ArrayField
---------------------------
Assume you want to have content type where the user can provide one or more files.
Its easy by making the type folderish. But for some use-cases this is to heavy or to
difficult, you want the user to use a form for those files.

You could say, ok, up to 5 files is enough and model 5 file fields into your class.
Not very elegant, huh?

The easiest way is to to use the UML ``multiplicity`` feature on your attribute aka field of the class. If you want to enable unlimited attachments use multiplicity ``*``. Or choose a number like ``5``, as in our above example.

You can set the initial size of the array by using the tagged value ``array:size`` to ``python:10`` for example. Prefixed with ``array:`` you can access also the label ``array:widget:label`` of it and so on. If you prefer the EnhancedArrayWidget you need to add an tagged value ``imports`` ``from Products.Compoundfield.EnhancedArrayWidget import EnhancedArrayWidget`` to your class and set on the attribute the tagged value ``array:widget:type`` to ``EnhanceArrayWidget``.

Custom Fields compounds - CompoundField
---------------------------------------
With ArchGenXML you can create compounds of fields from existing fields. Such a set of fields behaves almost like a normal field. To create such a compounded field create a new class and give it the stereotype ``<<field>>``

Now add attributes to it like you would do on a content type class. You can use almost every field type, just some special fields, mostyl those acting as a proxy without own storage, wont work (such as ReferenceField or AttachementField).

For example we create a ``PointField`` consisting out of two ``FloatFields`` by just adding a ``x`` and ``y`` attribute of type ``float``.

To use the new field create a fresh content class and name it ``Polygon``. Take a dependency arrow pointing from your Polygon class to the field class. This ensures it gets imported!

Next add an attribute ``points`` to the class. The type of the new points attribute is ``PointsField``. Now to make it a polygon give it a multiplicity of ``*`` and you are done: You have a list of Points as one field.
