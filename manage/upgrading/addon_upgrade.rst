=======================
Upgrade add-on products
=======================

.. admonition:: Description

   The steps to take to migrate your third party products

#. Shut down your Plone server instance.
#. If you specified concrete versions of the third-party products in your *buildout.cfg* file (so-called "pinning", and a recommended practice), like *Products.PloneFormGen* = 1.7.17, update these references to point to the new versions.
   Without pinning, i.e. specifying only, for example, *Products.PloneFormGen* and no version, buildout will pick the newest version of the products by default.
#. Run *bin/buildout*. Wait until all new software is downloaded and installed.
#. Start Plone again - your site may look weird, or even be inaccessible until you have performed the next step - don't panic :)
#. Navigate to the Add-on screen (just add ``/prefs_install_products_form`` to your site URL, and upgrade products if you can (products that support both your current and new version of Plone).
   Perform product-specific upgrade procedures (if any).
   You will find these in the documentation of each product.

Should the ``/prefs_install_products_form`` be unreachable, you should try doing the add-on upgrades from the ZMI.
Navigate to the quickinstaller in the ZMI, and reinstall or upgrade products that are shown to be outdated.

.. note::

   Be careful when updating add-ons through the ZMI.
   It may show outdated themes as well with a hint to update.
   If you do that, the updated theme will activate itself, overriding your current theme.
   If this happens, just re-enable your theme in the theming panel.
