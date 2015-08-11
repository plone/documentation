=========================
Using ZopeSkel and Paster
=========================

.. deprecated:: may_2015
    Use :doc:`bobtemplates.plone <bobtemplates.plone/README>`

.. note ::

    Using ZopeSKel is not considered *best practice* anymore, if you know how
    to handle it and its dependencies it fine, otherwise we advise you to use
    :doc:`bobtemplates <bobtemplates.plone/README>`.


.. admonition:: Description

    ZopeSkel is a tool which generates a code skeleton template for your
    Plone add-on you wish to develop.

.. contents:: :local:

Introduction
============

ZopeSkel provides a command-line utility and a number of templates that help
you to generate skeleton code for a Plone project.  Using ZopeSkel you can
create Plone buildouts, add-on packages and themes.  The skeleton code
created by ZopeSkel follows generally accepted best practices, and will get
you started developing for the Plone CMS.


Add-on creation and installation steps
======================================

There are three steps in your add-on creation and installation procedure:

* Create the add-on code skeleton using ZopeSkel as instructed below. The
  tool will provide sensible
  defaults for all options, so if you unsure about an answer, simple accept
  the default.

* Make your new add-on available in buildout as described in the
  installation instructions below.
  Adding code to buildout is done only once.
  After this you can see your package listed in the
  ``bin/instance`` script when you open the file.

* After this, Zope will load your Python and ZCML code every time Zope is
  restarted.

Adding ZopeSkel to your buildout
================================

To install ZopeSkel in your buildout, add the following to your
``buildout.cfg`` in the appropriate places::

    # add a 'zopeskel' part to the list of parts in the [buildout] section.
    parts =
        ... # some other parts here
        zopeskel # Add this as the last line

    # Add this bit at the end of your buildout.cfg
    # create zopeskel command in bin/
    # with Plone templates
    [zopeskel]
    recipe = zc.recipe.egg
    unzip = true
    eggs =
        ZopeSkel <= 3.0
        Paste
        PasteDeploy
        PasteScript
        zopeskel.dexterity
        zopeskel.diazotheme
        ${buildout:eggs}

.. note ::

     In buildout.cfg # marks comment at the end of the line - you don't need to type those

After adding this, run buildout and it will install ZopeSkel
that it requires. After buildout completes, you will find the ``zopeskel``
command in the ``bin``
directory of your buildout.  You can use this command to list template, run
them, and build the
skeleton code you need to get started.

To find out what templates are available, run:

.. code-block:: console

    bin/zopeskel --list

To get extensive documentation on the abilities of ZopeSkel, run:

.. code-block:: console

    bin/zopeskel --help

Troubleshooting
-----------------

If you get any exceptions running this command see
:doc:`troubleshooting </manage/troubleshooting/exceptions>`.
If self-service help doesn't get you anywhere `file issues on Github
<https://github.com/collective/ZopeSkel/issues>`_.

.. note::

    If you are migrating from a version of ZopeSkel prior to 3.0,
    you may need to remove the old ZopeSkel
    egg before you begin.


ZopeSkel Templates
==================

.. note::

    The templates listed below may not be the only ones available when you
    install ZopeSkel.
    New templates are being developed actively.

``archetypes``
    Creates a package skeleton for
    :doc:`Archetypes </develop/plone/content/archetypes/index>` based content types.

``dexterity``
    Creates a package for developing Dexterity content types.

``plone_basic``
    Creates a basic skeleton good for general Plone add-on packages.
    Minimal and clean.  You can use this package to set up views, forms,
    portlets, and many other add-on features.

``plone3_theme``
    Creates a basic skeleton good for creating old style theme for Plone
    (views, viewlets and so on)

``plone_nested``
    Creates a nested namespace package with the same basic skeleton as
    ``plone_basic``.  This is generally used for packages that are meant to
    be part of a set, like ``collective.blog.feeds``,
    ``collective.formwidget.autocomplete`` or ``collective.geo.mapwidget``.

Creating an add-on product skeleton
===================================

After you have followed the steps above how include ZopeSkel to your
buildout, you can create your first add-on.

To create an Archetypes-based content types package:

.. code-block:: console

    # Actual location is your Plone installation
    # Usually the folder name is zintance or  zeocluster
    cd /path/to/buildout
    cd src
    # Here replace "archetype" with scaffold name you want to use
    # For the complete list of different templates
    # run ../bin/zopeskel command without arguments
    ../bin/zopeskel archetype yourcompany.productname

Now it will ask you a series of question for the add-on properties. After this ``yourcompany.productname``
folder is created with prepopulated subfolders and files.

.. note::

    If you are unsure about questions, you may type ``?`` to get more
    information.
    You can also just hit enter to accept the default value.
    These are sensible for most cases.


After answering the questions, you'll have a new python package in the
``src`` directory of your buildout.
To begin using this code, you'll need to include the newly created package
in your ``buildout.cfg``::

    eggs =
        yourcompany.productname

    develop =
        src/yourcompany.productname

Rerun buildout to pick up the new package.

:doc:`Restart Plone in foreground mode </manage/troubleshooting/basic>`.
If your new code files contain errors it usually fails at this point
with a :doc:`Python traceback </manage/troubleshooting/exceptions>`.
This traceback will contain valuable information about what went wrong,
and will be the first thing anyone will ask for if you seek help.

Once Plone has started, log in as admin and go to :guilabel:`Site Setup` >
:guilabel:`Add-ons`.
If your package has a ``GenericSetup`` profile, you should see your add-on
in the list of available add-ons at the top of the page.

Local commands
==============

Besides project templates, ZopeSkel allows templates to define **local commands**.
Local commands are context-aware commands that allow you to add more
functionality to an existing project generated by ZopeSkel.

Examples of the kind of Plone functionality you can add with local commands:

* Content types inside your add-on.
* Schemas for your content types.
* Browser views
* Browser layers (to allow you to isolate add-on code to sites where your
  package is activated)

* etc.

.. warning::

    Local commands work only with paster command run from buildout bin/
    directory. Do not try to run local commands with system-wide paster
    command.


Local commands are not available until your egg is registered as
development egg in your buildout, you have run buildout and
you use paster command provided by buildout.

If you follow the instructions
below and do not see an ``add`` local command, please verify that your
package has been properly added to your buildout and that buildout has
been re-run afterwards.



Adding a Content Type to your package
-------------------------------------

In this example we will continue ``yourcompany.productname`` development
and add our first Archetypes-based content type.

Example of creating a content type:

.. code-block:: console

    # First create an add-on skeleton if one does not exist
    cd yourcompany.productname/src

.. note::

    You must create the ``src`` folder **inside** your package.
    Otherwise the ``paster add`` command cannot work.

To list the local commands available to your package, type:

.. code-block:: console

    ../../../bin/paster add --list

This will display local commands that will work for the package you have
created.
Different package types have different local commands.
Next you can use the ``paster add`` local
command to add new functionality to your existing code.

For example, to add a special content type for managing lectures:

.. code-block:: console

    ../../../bin/paster add at_contenttype

After the content type is added, you can add schema fields for the type:

.. code-block:: console

    ../../../bin/paster add at_schema_field

.. note::

    New content types are added to Plone using GenericSetup.
    GenericSetup profiles are run when an add-on product is **activated**.
    To see the content type you create, you'll need
    to restart Plone **and** reinstall the add-on.

Site setup and Add-on installation
====================================

If you want your add-on to be 'activated' by going to the Plone Add-on
control panel, you will
need to have a :doc:`GenericSetup profile </develop/addons/components/genericsetup>`.
ZopeSkel can set this up for you, just say 'Yes' if you are asked.
Some templates require a profile, and will not ask.
This profile modifies the site database
**every time you run Add-on installer your site setup**.
If you make changes to your profile, you need to
**re-run the installation of your package** to pick up those changes.

A GenericSetup profile is just a bunch of XML files with information that is
written to the database when the add-on is installed. This is independent of
Python and ZCML code, and GenericSetup XML can be updated without restarting
the site.

Not all add-ons provide GenericSetup profiles.
If an add-on does not modify the site database
in any way, e.g. they provide only new :doc:`views </develop/plone/views/browserviews>`,
it may not require one.
But a GenericSetup profile is required in order to have the add-on appear in
the list of 'available add-ons' in the Plone Add-ons control panel.


In-depth background information
=================================

How paster local commands work
--------------------------------

Paster reads ``setup.py``. If it finds a ``paster_plugins`` section there,
it will look for local commands.

This allows paster to know that packages created by that template provide
local commands
defined by the templer system which underlies ZopeSkel.

:doc:`More about paster templates </develop/plone/misc/paster_templates>`.

setup.py install_requires
-------------------------

Python modules can specify dependencies to other modules by using the
``install_requires`` section in ``setup.py``.
For example, a Plone add-on might read::

    install_requires=['setuptools',
            # -*- Extra requirements: -*-
            "plone.directives.form"
            ],

This means that when you use setuptools/buildout/pip/whatever Python package
installation tool to install your package from the
`Python Package Index (PyPi) <https://pypi.python.org/pypi>`_
it will also automatically install Python packages declared in
``install_requires``.

paster and ``install_requires``
--------------------------------

.. warning::

    Never use a system-wide paster installation with local
    commands. This is where things usually go haywire. Paster is not
    aware of this external Python package configuration set (paster
    cannot see them in its ``PYTHONPATH``). Also don't try to execute
    system-wide ``paster`` in a Python source code
    folder containing ``setup.py``. Otherwise paster downloads all the
    dependencies mentioned in the ``setup.py`` into that folder even
    though they would be available in the ``eggs`` folder (which
    paster is not aware of).

