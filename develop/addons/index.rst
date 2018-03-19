=====================
Develop Plone Add ons
=====================

To develop an add-on, you need a package to put your code in, plus ways to make it interact with Plone itself and the user.
And a way to release your package to your audience.

In short:

Create a package
================

With the help of Mr.Bob and templates for plone, that is quickly done:


.. toctree::
   :maxdepth: 2

   bobtemplates.plone/README

Develop with Dexterity
======================

Dexterity is covered in detail in the :doc:`Dexterity Developer Manual </external/plone.app.dexterity/docs/index>`, which includes an extensive tutorial on
setting up a Dexterity development environment.


Upgrading to Plone 5.1
======================

.. toctree::
   :maxdepth: 2

   upgrade_to_51


Add your package to buildout
============================

Edit your ``buildout.cfg`` file to add the package to your ``egg`` list and your ``develop`` list. Run buildout.


The Plone Collective
====================

This is an organization for developers of Plone add-ons to work collectively. Software that is released in here follows a simple, collaborative model: every member can contribute to every project.

This means you will have the best chance of having other people contributing to your add-on. When your add-on is generic enough to be useful to other people, please consider to release it here.

`Read more on how to become a member of the Plone Collective <https://collective.github.io/>`_


Releasing your package
======================

.. toctree::
   :maxdepth: 2

   releasing

Working with JavaScript
=======================

.. note::
    Working with JavaScript has changed considerably in Plone 5. Read the note at the beginning of the document.

.. toctree::
   :maxdepth: 2

   javascript/index

Background
==========

.. toctree::
   :maxdepth: 2

   components/index

.. toctree::
   :maxdepth: 2


   schema-driven-forms/index

Training
========

A number of Plone trainers have joined forces to create completely open  `Training materials <https://training.plone.org/>`_.

While following a real-life course is the best way to get up to speed with Plone, the material is also very useful for self-study.
You will find separate chapters on creating packages, writing your own theme and much more here.
