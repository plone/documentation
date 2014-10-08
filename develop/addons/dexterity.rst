============================
Creating a Dexterity project
============================

This document explains how to setup a Dexterity-based project with minimum
effort, using ``zopeskel.dexterity``.

Prerequisites
=============

 * Python 2.6 or 2.7
 * virtualenv

Creating a virtual environment
==============================

We'll be using _paster_ to create a Dexterity project.
First, a virtual environment is created,
followed by the Python eggs that are needed for Paster.

.. code-block:: console

    $ ./bin/virtualenv-2.7 example-testing
    $ cd example-testing
    $ . ./bin/activate
    $ pip install ZopeSkel==2.21.2  Paste PasteDeploy PasteScript zopeskel.dexterity

.. topic:: Templer or Paster

    Templer is the replacement for ZopeSkel/Paster. 
    However, because of a bug in ``zopeskel.dexterity`` it isn't
    usable with Templer.
    Instead, ZopeSkel is pinned to version 2.12.2.

Create a dexterity product
==========================

Use ``zopeskel`` to create a Python egg which contains a Dexterity-based product.
(Note: just select default options for all questions during installation,
except for _project name_, for which we'll use ``collective.example``.)

.. code-block:: console

    $ ./bin/zopeskel dexterity
    dexterity: A Dexterity-based product

    This template expects a project name with 1 dot in it (a 'basic
    namespace', like 'foo.bar').

    Enter project name: collective.example

    [...]

    usage: paster COMMAND

    Commands:
      addcontent  Adds plone content types to your project

    For more information: paster help COMMAND
    ------------------------------------------------------------------------

Fix content generation in zopeskel.dexterity
--------------------------------------------

We need to work around a bug in ``zopeskel.dexterity``. 
Please visit 
[github issue 1](https://github.com/collective/zopeskel.dexterity/issues/1#issuecomment-58310600)
and apply the fix, then come back here and proceed.


Add content using paster
========================

Use ``paster`` to list the types of content that can be added:

.. code-block:: console

    $ paster addcontent -l
    Available templates:
        dexterity_behavior:  A behavior skeleton
        dexterity_content:   A content type skeleton

Add a content-type:

.. code-block:: console

    $ paster addcontent dexterity_content
    Enter contenttype_name (Content type name ) ['Example Type']: Example content
    Enter contenttype_description (Content type description ) ['Description of the Example Type']: Just an example
    (Use default values for rest - press Enter)


Fix buildout
============

Edit the generated ``buildout.cfg`` & ``plone.cfg`` files.

1. Add the following line to the ``[buildout]`` part:

    .. code-block:: console

        develop = .

2. Remove the following line from the ``[instance]`` part:

    .. code-block:: console

        effective-user = ${buildout:effective-user}

3. Not a bug, but when editing the buildout, update Plone to the latest
   version:

    .. code-block:: console

        extends = http://dist.plone.org/release/4.2.1/versions.cfg


Running buildout
================

Finally, run the buildout:

.. code-block:: console

    $ cd collective.example
    $ python bootstrap.py
    $ ./bin/buildout -c plone.cfg

And start the Plone instance to add the Dexterity content type:

.. code-block:: console

    $ ./bin/instance fg

