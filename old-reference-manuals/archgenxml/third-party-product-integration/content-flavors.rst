===============
Content Flavors
===============

.. contents :: :local:

.. admonition:: Description

        When you want to add a couple of fields to an existing content type
        (including reference fields), you may decide to create a whole new
        product that subclasses that type. You then have a whole bunch of code
        to maintain and you are dependent on changes that may occur in your
        parent class. Or you let ArchGenXML use the Content Flavors product and
        your day gets brighter. Note that the use of the experimental content
        flavors product is now deprecated in favor of the more reliable and
        feature-rich archetypes.schemaextender.

Prerequisites
-------------
You must install the `Content Flavors <http://plone.org/products/contentflavors>`_ product.

Adding a field to an existing content typ
-----------------------------------------
1. Let an existing content type, e.g. *"ExistingType"*, be present in your diagram (as a **class** with stereotypes ``<<archetype>>`` and ``<<stub>>``)
2. Create a **class**, e.g. *"MyCoolFlavor"*, in your diagram and give it the ``<<flavor>>`` stereotype
3. Add any field(s), e.g. *"MyAdditionalField"*, to this flavor class
4. Create a **realization** arrow from *"ExistingType"* to *"MyCoolFlavor"*
5. Generate & Done

Now every new instance of *ExistingType* will have the *MyAdditionalField* field in its schema, default view and default edit form.

Limits
------
.. note:: The use of the experimental content flavors product is now deprecated in favor of the more reliable and feature-rich archetypes.schemaextender.

* Content Flavors also allows **custom views** to be used by existing types but this feature is not supported by ArchGenXML yet.
* You may not be able to see the additional field(s) if the ExistingType uses some non-default view. You then have to manually manage this by **overriding these existing views** with some of your own, with or without the help of the Content Flavors product.
* The existing content type may have to be based on ATCT (to be tested)?
* Several flavors can be applied to a given type. The order of precedence can be managed through the web if the existing type follows some requirements detailed in the `Content Flavors documentation <http://plone.org/products/contentflavors/documentation>`_.
* There are possible issues with indexing the additional fields, see `CF documentation for details <http://plone.org/products/contentflavors/documentation>`_.
* Content Flavors was an experiment and is now deprecated in favour of the `archetypes.schemaextender <http://plone.org/products/realestatebroker/documentation/how-to/customize-the-fields-of-the-content-types>`_, which is also supported by AGX.
