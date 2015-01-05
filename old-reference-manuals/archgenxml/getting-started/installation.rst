============
Installation
============

.. contents :: :local:

.. admonition:: Description

        How to install ArchGenXML and get up and running.

Installation
============

ArchGenXML has a dependency on some Zope 3 eggs. To avoid messing up your
global site-packages directory, using buildout or virtualenv is recommended.

.. note::

   In an older version of AGX, a Zope 3 installation could be configured in a
   ``~/.agx_zope_path`` file. This case is not supported anymore. You can
   delete this file if you have it.

On Windows, I assume that you installed Python 2.4.4 using the
`msi installer <http://www.python.org/download/releases/2.4.4/>`_ installer,
and that you installed it in the default location. If you have not already
done so, configure the ``Path`` environment variable to include your python
path and scripts directory. For this, go to *Control Panel*, *Advanced*,
*Environment Variables*, edit *Path*, and append
``;C:\\Python24;C:\\Python24\Scripts`` to the existing string.

Installing stable version
--------------------------

.. attention::

   Adding the ArchGenXML egg to a Plone buildout is not supported! The Plone
   3.x buildout is shipped with an old Zope 3.3. ArchGenXML depends on the
   latest version of Zope 3 eggs. So please create a buildout only for
   ArchGenXML like described below.

If you want to install archgenxml via buildout (recommended), read
:ref:`agx-installation-using-buildout` and skip the
:ref:`agx-installation-using-easy-install` part.

It can happen that the ArchGenXML version on https://plone.org is older than
PyPI because the release manager forgot to upload it on https://plone.org or for
another reason.  ``easy_install`` and ``buildout`` will get the latest
ArchGenXML version from PyPI by default, so it's fine.

.. _agx-installation-using-buildout:

Using buildout
""""""""""""""

Create a fresh directory and go into it:

.. code-block:: console

   $ mkdir archgenxml_buildout
   $ cd archgenxml_buildout

Download the normal `bootstrap.py
<http://svn.zope.org/*checkout*/zc.buildout/trunk/bootstrap/bootstrap.py>`_
and put it in this directory. You can copy an existing bootstrap.py file of
one of your buildout, it's the same file.

Then create a ``buildout.cfg`` file in this directory with the following
snippet:

.. code-block:: ini

   [buildout]
   parts =
       archgenxml

   [archgenxml]
   recipe = zc.recipe.egg:scripts
   eggs = archgenxml

.. TODO:: Is ini the appropriate lexer here?

Finally bootstrap the buildout and run it:

.. code-block:: console

   $ python bootstrap.py
   $ ./bin/buildout

On Windows, it's ``bin\buildout``; you have to replace '/' by '\' in all following examples.

The ``archgenxml`` command is now available as ``./bin/archgenxml``.

To update ArchGenXML later, go in your directory and run buildout again:

.. code-block:: console

   $ ./bin/buildout

It will download latest version of ArchGenXML and all its dependencies.

In the following, I refer to the *<path to archgenxml>* as the
``archgenxml_buildout`` directory.

.. _agx-installation-using-easy-install:

Using ``easy_install`` in a virtualenv
"""""""""""""""""""""""""""""""""""""""

If you don't want to use buildout, you can use ``virtualenv`` to create an
isolated environment. You have to install the ``setuptools`` egg in order to
have the ``easy_install`` command available. On Ubuntu you can do it with
``apt-get install python-setuptools``. On Windows, go to the
`setuptools pypi page <https://pypi.python.org/pypi/setuptools>`_, download the
``exe`` which matches the Python version you are using, and execute it to
install it.

Install virtualenv with easy_install:

.. code-block:: console

   $ easy_install virtualenv

On Windows, ``easy_install.exe`` is in ``C:\Python24\Scripts``, so you have to
invoke it with the full path if you haven't added this directory to your
``PATH``.

Create the virtualenv with the ``--no-site-packages`` option to ignore
globally-installed packages:

.. code-block:: console

   $ virtualenv --no-site-packages agx
   $ cd agx/
   $ source bin/activate
   $ easy_install archgenxml

Every time you want use ArchGenXML, you have to go in the *agx* directory and
type ``source bin/activate`` to activate the environment. To deactivate the
environment, type ``deactivate``.

To update ArchGenXML, you have to update each egg. The most important ones are
``archgenxml`` and ``xmiparser``:

.. code-block:: console

   $ easy_install -U archgenxml
   $ easy_install -U xmiparser

If you have a problem with ArchGenXML, please be sure to recreate the
virtualenv completely so you have the latest versions of all eggs before asking
on the archetypes-users mailing-list.

I call below *<path to archgenxml>* the path to the virtualenv agx directory.

Installing the development version
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

ArchGenXML's svn trunk is for the 2.x development version.

As usual, the goal is to keep trunk workable. Some of the developers work and develop on the edge: trunk.

If you need stability, use the latest release.

The only supported way to use the ArchGenXML trunk is with buildout. You install it like this:

.. code-block:: console

   $ svn co https://svn.plone.org/svn/archetypes/ArchGenXML/buildout archgenxml_buildout
   $ cd archgenxml_buildout
   $ python bootstrap.py
   $ bin/buildout

To update your buildout:

.. code-block:: console

   $ cd archgenxml_buildout
   $ svn up
   $ bin/buildout

If you are interested in AGX 3 development, see http://dev.plone.org/archetypes/browser/AGX

I call below *<path to archgenxml>* the archgenxml_buildout directory.

Get the ArchGenXML profile
^^^^^^^^^^^^^^^^^^^^^^^^^^

The ``archgenxml_profile.xmi`` file contains information about stereotypes,
fields, and other stuff that AGX needs to generate valid Python code from your
model. You can `get the profile
<http://svn.plone.org/svn/archetypes/ArchGenXML/trunk/umltools/argouml/archgenxml_profile.xmi>`_
from subversion.

Or you can regenerate it with ``<path to archgenxml>/bin/agx_argouml_profile``.
An ``archgenxml_profile.xmi`` file is generated in the current directory.

Create a ``<path to archgenxml>/profiles`` directory and put the file here.

Note: In an older version of AGX, this file was called ``argouml_profile.xmi``.
You should not use it with ArgoUML > 0.24.

Troubleshooting
^^^^^^^^^^^^^^^

On Windows, you may have to install and configure the `mingw32 compiler
<https://plone.org/documentation/kb/using-buildout-on-windows>`_ to compile the
``zope.proxy`` egg, an indirect dependency of ArchGenXML. Now ``zope.proxy``
eggs are built for Windows, so you should not have this problem anymore.

Support
^^^^^^^

For any questions or problems, please ask on the `archetypes-users mailing-list
<https://plone.org/support/forums/archetypes>`_. Please don't use comments on
the manual pages. Not everybody is alerted when a comment is added.

If you want to contribute to this documentation, please post on the `plone-docs
mailing-list <https://plone.org/support/forums/docs>`_.
