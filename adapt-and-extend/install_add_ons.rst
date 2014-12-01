Installing Add-ons
==================

quick instructions

These instructions cover add-on installation process for Plone 3.3.x and 4 installation.

Introduction
------------

This page covers add-on installation instructions for Plone 4 and Plone 3.3.x systems. Legacy systems are not covered in these instructions.

Prerequisitements
-----------------

What you need to know in order to install add-ons for Plone

- How to use command line of your operating system. This is a hard requirement - you cannot achieve your goal unless you know how to interact with the command line. Here are basics tutorials for `Windows <http://www.hacking-tutorial.com/tips-and-tricks/16-steps-tutorial-basic-command-prompt/>`_ and `Linux <http://linuxcommand.org/learning_the_shell.php>`_
- Working with plain text based configuration files and editing them with a text editor like Notepad
- First create a :doc:`development / back-up copy </manage/deploying/copy>` of your site. Never install to the working production server directly, without first testing the add-on on a test instance.


Background
----------

Since Plone 3, Plone installations are managed using :term:`Buildout`. Plone add-ons are distributed as Python modules, also known as eggs.

- the `Plone product <https://plone.org/products>`_ download area contains popular add-ons for Plone
- Add-on file downloads are hosted on the `PyPi Python package repository <https://pypi.python.org/pypi>`_ - along with tons of other Python software
- the buildout.cfg file in your Plone configuration defines which add-ons are available for your sites to install in Site Setup > Add-ons control panel
- the bin/buildout command (or bin/buildout.exe on Windows) in your Plone installation reads buildout.cfg and automatically downloads required packages when run - you do not need to download any Plone add-ons manually
- Plone site setup -> Add ons control panel defines which add-ons are installed for the current Plone site (remember, there can be many Plone sites on a single Zope application server)

.. note::

    Plone add-ons, though Python eggs, must be installed through buildout as only buildout will regenerate the config files reflecting newly downloaded and installed eggs. Other Python installation tools like easy_install and pip do not apply in a Plone context.

Finding add-ons
----------------

Browse the `plone.org product area <https://plone.org/products>`_ or `search on PyPi <https://pypi.python.org/pypi?:action=search&term=plone&submit=search>`_ for possible add-ons.

When you find a suitable add-on you must note down its Python package name. Quite often, this is in the form of a name with a dot in it. For example, for the add-on PloneFormGe  the package id is Products.PloneFormGen. The id is visible in the PyPi page URL if it is not mentioned anywhere else. Capitalization is important here!

Before proceeding make sure that the add-on is compatible with your Plone version. If you cannot find this information on the package page please contact the add-on author.

Downloading and configuring an add-on package for Plone
--------------------------------------------------------

Please do not directly test new add-ons on your production site. Instead, have a development copy of the site around where you can safely test the add-ons. Before proceeding to the production environment, always take a back up copy of your Plone site.

Edit the file buildout.cfg in your Plone folder with a text editor. Find line

.. code-block:: console

  eggs =
      Plone
      Pillow
      etc...


There you can include your package in the  list.

.. code-block:: console

  eggs =
       Plone
       Pillow
       Products.PloneFormGen
       ...

.. note::

  Some older Plone add-ons (released before Plone 3.3.x) also require you to add add-on package name to zcml= section in buildout.cfg. As a a rule of the thumb, all add-ons released since  the second half of 2010 should no longer require this.

After the buildout.cfg has been changed run command buildout from the command line. The buildout command reads buildout.cfg and download the packages defined in the eggs section and makes them available for Plone.

Note: Run buildout from command line using the instructions below. You don't double click buildout.exe.



On UNIX

.. code-block:: console

  bin/buildout



On Windows (for Plone 4.1)

.. code-block:: console

  cd C:\Plone41
  bin\buildout.exe


If buildout fails please see the :doc:`troubleshooting buildout </manage/troubleshooting/buildout>` section.

Downloading and configuring add-on package from github
------------------------------------------------------

Sometimes you need the newest version of an add-on, this is only suggested for experienced developers or for testing purposes. See :doc:`this section</manage/installing/installing_addons>`



Further help
-------------

More detailed instructions for installing Plone add-ons are available for dealing with legacy systems.

Please visit the  :doc:`help asking guidelines</askforhelp>` and `Plone support <https://plone.org/support>`_ options page to find further help if these instructions are not enough. Also, contact the add-on author, as listed on Plone product page, to ask specific instructions regarding a particular add-on.
