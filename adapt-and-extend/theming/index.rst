Theming Plone
=============

.. admonition:: Description

   The current best-practice way to theme a Plone site is by using an engine called "Diazo".
   This allows designers to design a theme in just plain, flat HTML, CSS (and javascript, if wanted) and then to hook that into the Plone backend to fill it with sophisticated content.



.. toctree::
   :maxdepth: 2

   intro
   plone_app_theming
   /external/diazo/docs/index
   theme_product_with_diazo
   quick_test

Using Diazo is also possible as a standalone service. That makes it possible to include several back-end applications under one 'look'

.. toctree::
   :maxdepth: 2

   deliverance

General information on the stylesheets and other resources in Plone

.. toctree::
   :maxdepth: 2

   templates_css/index

Information on 'old-style' theming for Plone 3, but still valid in Plone 4.
So upgrading from Plone3 to Plone4 is possible without switching to the new style of theming.

Do note that for all **new** theme development, Diazo is strongly recommended.

.. toctree::
   :maxdepth: 2

   old_style_theming.rst