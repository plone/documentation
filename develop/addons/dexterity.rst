============================
Creating a Dexterity project
============================

Dexterity is covered in detail in the `Dexterity Developer Manual <http://docs.plone.org/external/plone.app.dexterity/docs/>`_, which includes an extensive tutorial on setting up a Dexterity development environment and creating Dexterity add-on packages.

Here, we'll just add a few details on setting up and using the ZopeSkel package creator for use with Dexterity.

The only prerequisite is a working Plone buildout and to have added the ZopeSkel part described in :doc:`bootstrapping </develop/addons/paste>`.


Create a dexterity product
==========================

Use zopeskel to create a Python package which contains a Dexterity-based product.
(Note: just select default options - press Enter - for all questions during installation, except for project name which must be collective.example)

Use ``zopeskel`` to create a Python egg which contains a Dexterity-based product.
(Note: just select default options for all questions during installation,
except for _project name_, for which we'll use ``collective.example``.)

.. code-block:: console

    # cd to your buildout directory
    $ cd src
    $ ../bin/zopeskel dexterity
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

Add your package to buildout
============================

Edit your ``buildout.cfg`` file to add the package to your ``egg`` list and your ``develop`` list. Run buildout.

.. note::

    If you try to use a local command without this step, paster will suggest you run ``python setup.py develop``. **Do not do that.** Instead, add your package to your buildout and run buildout.

Add content using paster
========================

Use ``paster`` to list the types of content that can be added:

.. code-block:: console

        $ ../bin/paster addcontent -l
        Available templates:
            dexterity_behavior:  A behavior skeleton
            dexterity_content:   A content type skeleton

Add a content-type:

.. code-block:: console

        $ ../bin/paster addcontent dexterity_content
        Enter contenttype_name (Content type name ) ['Example Type']: Example content
        Enter contenttype_description (Content type description ) ['Description of the Example Type']: Just an example
        (Use default values for rest - press Enter)

