=======================
Upgrade add-on products
=======================

.. admonition:: Description

   The steps to take to migrate your third party products

#. Shut down your Plone server instance.
#. If you specified concrete versions of the third-party products in your *buildout.cfg* file (what is so-named "pinning"), like *Products.CacheSetup* = 1.0, update these references to point to the new versions.
   Without pinning, i.e. specifying only, for example, *Products.CacheSetup* and no version, buildout will pick the newest version of the products by default.
#. Run *bin/buildout*. Wait until all new software is downloaded and installed.
#. Start Plone again - your site may be inaccessible until we have performed the next step - don't panic :)
#. Navigate to the quickinstaller in the ZMI, and reinstall or upgrade products if you can (products that support both your current and new version of Plone).
   Perform product-specific upgrade procedures (if any).
   You will find these in the documentation of each product.
