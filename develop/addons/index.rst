Develop Plone Add ons
=====================

To develop an add-on, you need a package to put your code in, plus ways to make it interact with Plone itself and the user.
And a way to release your package to your audience.

In short:

Create a package
----------------

With the help of Mr.Bob and templates for plone, that is quickly done:


.. toctree::
   :maxdepth: 2

   bobtemplates.plone/README

Develop with Dexterity
----------------------

Dexterity is covered in detail in the :doc:`Dexterity Developer Manual </external/plone.app.dexterity/docs/index>`, which includes an extensive tutorial on
setting up a Dexterity development environment.


Upgrading to Plone 5.0
----------------------

.. toctree::
   :maxdepth: 2

   upgrade_to_50

Add your package to buildout
----------------------------

Edit your ``buildout.cfg`` file to add the package to your ``egg`` list and your ``develop`` list. Run buildout.

Releasing your package
----------------------

.. toctree::
   :maxdepth: 2

   releasing

Working with Javascript
-----------------------

.. toctree::
   :maxdepth: 2

   javascript

   javascript_standards

   ajax

Background
----------

.. toctree::
   :maxdepth: 2

   components/index

.. toctree::
   :maxdepth: 2


   schema-driven-forms/index

Example
-------

.. toctree::
   :maxdepth: 2

   helloworld/index

Also make sure to check out the `Training material <http://training.plone.org>`_