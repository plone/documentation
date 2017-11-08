===============
Change The Logo
===============

.. topic:: Description

   How to substitute the standard Plone logo with your own logo.
   A through-the-web approach.



The Basics
==========

In Plone 5, the logo can be changed TTW (Through-The-Web) in the ``@@site-controlpanel``.


Changing The Image (Site control panel)
---------------------------------------

Since Plone 5 you can directly change the logo in the Site control panel.
Upload your custom logo image with the Site logo field.


.. figure:: ../_robot/change-logo-in-site-control-panel.png
   :alt: Change site logo image
   :align: center

Changing HTML
-------------

To change the HTML of the logo part you can use Diazo to copy the *src* and *href* of the logo elements and put them in your custom HTML in your static HTML Theme.

For further information's about Diazo please have a look at the Diazo documentation in :doc:`Theming Plone </adapt-and-extend/theming/index>`.

Further Information
-------------------

-  There are further HOWTOs in the Logo section of the Plone documentation dealing with more advanced customization methods.
-  More guidance on TAL and ZPT can be found in the ZPT tutorial.
-  If you want to transfer your changes to the file system in your own theme product, then proceed to the :doc:`viewlets overview section </develop/plone/views/viewlets>`.
