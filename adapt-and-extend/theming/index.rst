Theming Plone
=============

.. admonition:: Intro

   The current best-practice way to theme a Plone site is by using an engine called "Diazo".
   This allows designers to design a theme in just plain, flat HTML, CSS (and javascript, if wanted) and then to hook that into the Plone backend to fill it with sophisticated content.

   The easiest way to do this is to use "plone.app.theming". But if you need to integrate Plone with other back-end servers, legacy systems, or any webservice, you can use Diazo to all combine it in a unified look & feel.



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


    Using Diazo is also possible as a standalone service. Normally the Diazo theme transformation is running inside the Plone process. But you can compile the Diazo rules to low level XSLT and let a webserver
    do the actual transformation, or run the Diazo transformations in a wsgi enabled service. 
    If you want this advnced stand alone set up, please take a look at documentaiton on `www.diazo.org <http://www.diazo.org>`_, especially the
    `Compilation <http://docs.diazo.org/en/latest/compiler.html>`_ and `Deployment <http://docs.diazo.org/en/latest/deployment.html>`_ chapters. 

General information on the stylesheets and other resources in Plone

.. toctree::
   :maxdepth: 2

   templates_css/index

.. note ::

    Up to version 4.1, Plone was using an older style of theming. Using that is not considered *best practice* anymore.
    See `older versions of these docs <http://docs.plone.org/4/en/adapt-and-extend/theming/old_style_theming.html>`_ if you need the information.
