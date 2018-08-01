=======
Theming
=======

.. admonition:: Intro

   The current best-practice way to theme a Plone site is by using an engine called `"Diazo" <http://www.diazo.org>`_.
   This allows designers to design a theme in just plain, flat HTML, CSS and JavaScript.

   The way to do this is to use `plone.app.theming <https://github.com/plone/plone.app.theming>`_.
   If you need to integrate Plone with other back-end servers, legacy systems, or any webservice,
   you can use Diazo to all combine it in a unified look & feel.



.. toctree::
   :maxdepth: 2

   theme_product


.. toctree::
   :maxdepth: 2


   /external/plone.app.theming/docs/index
   /external/diazo/docs/index

.. toctree::
   :maxdepth: 2

   resourceregistry
   barceloneta

An older (Plone 4.2) quick guide which may help to understand Diazo better:

.. toctree::
   :maxdepth: 2

   quick_test


Using Diazo is also possible as a standalone service.

Normally the Diazo theme transformation is running inside the Plone process.
You can compile the Diazo rules to low level XSLT and let a webserver
do the actual transformation, or run the Diazo transformations in a `WSGI <https://en.wikipedia.org/wiki/Web_Server_Gateway_Interface>`_ enabled service.

If you want this advanced stand alone set up, please take a look at documentation on `www.diazo.org <http://www.diazo.org>`_,
especially the `Compilation <http://docs.diazo.org/en/latest/compiler.html>`_ and `Deployment <http://docs.diazo.org/en/latest/deployment.html>`_ chapters.

General information CSS and other resources in Plone:

.. toctree::
   :maxdepth: 2

   templates_css/index

.. note::

   Up to version 4.1, Plone was using an older style of theming.
   Using that is **not** considered best practice anymore.

   See `older versions of these docs <https://docs.plone.org/4/en/adapt-and-extend/theming/old_style_theming.html>`_ if you need the information.
