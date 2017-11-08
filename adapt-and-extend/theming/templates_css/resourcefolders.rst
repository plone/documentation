================
Resource folders
================

.. admonition:: Description

    How to use resource directories to expose static media files (CSS, JavaScript, other) in your Plone add-on product


Introduction
============

Resource folders are the Zope Toolkit way to expose static media files to Plone URL mapping.

Resource folders provide a mechanism which allows conflict free way to have static media files mapped to Plone URL space.
Each URL is prefixed with ``++resource++your.package`` resource identified.

ZCML resourceDirectory
======================

If you want to customize media folder mapping point, you need to use the resourceDirectory directive.

Below is an example how to map *static* folder in your add-on root folder to be exposed via ++resource++your.product/ URI

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser">

      <!-- Resource directory for static media files -->
      <browser:resourceDirectory
          name="your.product"
          directory="static"
          />

    </configure>
