=============
Introduction
=============

.. admonition:: Description

		Introducing a sample AT Product and the contents of the tutorial. 

In this part of the manual, we discuss a sample AT Product to explain
CMF/Archetypes practices. We will be building a product called
**example.archetype**, which will implement a content type
(InstantMessage) that members with specific rights can use to add
messages readable by other members. However, as you may have guessed,
this is more a learning example than a usable product for a real website
application.

What is a Product ? A product - a Zope product to be precise - is a
third party add-on that can be integrated to provide additional
functionality. It is a code package written using the Python language
and conventions.

In order to understand this section you will need to have some prior
knowledge of working on the file system and programming protocols common
to Python and Zope.

The **example.archetype** product features the following CMF and
Archetypes capabilities:

-  basic fields and widgets;

-  defining and using a vocabulary for a field with a selection widget;

-  defining specific “Add” permissions for the contents.

The code of the product can be downloaded here:
`http://plone.org/products/example.archetype/`_

.. _`http://plone.org/products/example.archetype/`: ../../../../products/example.archetype/