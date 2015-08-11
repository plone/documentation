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

.. deprecated:: may_2015
   Using :doc:`Paster/Zopeskel <paste>` is possible, but deprecated

Develop with Dexterity
----------------------

Dexterity is covered in detail in the `Dexterity Developer Manual <http://docs.plone.org/external/plone.app.dexterity/docs/>`_, which includes an extensive tutorial on
setting up a Dexterity development environment.


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