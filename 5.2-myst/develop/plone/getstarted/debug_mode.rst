==========
Debug mode
==========

.. admonition:: Description

    Plone can be put in the debug mode where one can diagnose start up failures and
    any changes to CSS, JavaScript and page templates take effect immediately.

Introduction
============

By default when you start Plone you start it in a **production mode**.

* Plone is faster

* CSS and JavaScript files are *merged* instead of causing multiple HTTP request to load these assets.
  CSS and JavaScript behavior is different in production versus debug mode, especially with files with syntax errors
  because of merging.

* Plone does not reload changed files from the disk

Because of above optimizations the development against a production mode is not feasible.
Instead you need to start Plone in debug mode (also known as development mode) if you
are doing any site development.

In **debug mode**

* If Plone start-up fails, the Python traceback of the error is printed in the terminal

* All logs and debug messages are printed in the terminal; Zope process does not detach
  from the terminal

* Plone is slower

* CSS and JavaScript files are read file-by-file so line numbers match on the actual files on the disk.
  (*portal_css* and *portal_javascript* is set to debug mode when Plone is started in debug mode)

* Plone reloads CSS, JavaScript and .pt files when the page is refreshed

.. note::

     Plone does not reload .py or .zcml files in the debug mode by default.

Reloading Python code
=====================

Reloading Python code automatically can be enabled with `sauna.reload add-on <https://pypi.python.org/pypi/sauna.reload/>`_.

JavaScript and CSS issues with production mode
==============================================

See **portal_css** and **portal_javascript** in the Management Interface to inspect how your scripts are bundled.

Make sure your JavaScript and CSS files are valid, mergeable and compressable.
If they are not then you can tweak the settings for individual file in the corresponding management tool.

Refresh issues
==============

Plone **production mode** should re-read CSS and JavaScript files on Plone start-up.

Possible things to debug and force refresh of static assets

* Check HTML <head> links and the actual file contents

* Go to *portal_css*, press *Save* to force CSS rebundling

* Make sure you are not using *plone.app.caching* and doing caching forever
* Use `hard browser refresh <http://support.mozilla.org/en-US/questions/746138>`_ to override local cache

Starting Plone in debug mode on Microsoft Windows
=================================================

This document explains how to start and run the latest Plone (Plone 4.1.4) on Windows 7. This document explains post-installer steps on how to start and enter into a Plone site.
Installation

Installation
------------
This quick start has been tested on Windows 7.  Installation remains the same on older versions of Windows through WinXP.

1. Run installer from `Plone.org <https://plone.org/products>`_ download page

2. The Plone buildout directory will be installed in C:\\Plone41

3. The installer will launch your Plone instance when it finishes.  To connect, direct your browser to: http://localhost:8080

.. note::
   In the buildout bin directory you'll find the executable files to control Plone instance.

Starting and Stopping Plone
---------------------------

If your Plone instance is shutdown you can start and control it from the command prompt.

.. note::
   To control Plone you need to execute your command prompt as an administrator.

In the command prompt enter the following command to access your buildout directory
(the varies according to Plone version)::


   cd "C:\\Plone41"

To start Plone in debug mode type::

   bin\instance fg

You can interrupt the instance by pressing CTRL-C. This will also take down the Zope application server and your Plone site.

Accessing Plone
---------------

When you launch Plone in debug or daemon mode it will take a few moments to launch.  If you are in debug mode, Plone will be ready serve pages when the following line is displayed in your command prompt::

   INFO Zope Ready to handle requests

When the instance is running and listing to port 8080, point your browser to address on your local computer::

   http://localhost:8080

The Plone welcome screen will load and you can create your first Plone site directly by clicking the **Create a new Plone Site** button.

A form will load asking for the *Path Identifier* (aka the site id) and *Title* for a new Plone site.  It will also allow you to select the main site language, and select any add-on products you wish to install with the site.

.. note::
   These entries can all be modified once the site is created.  Changing the site id is possible, but not recommended.

To create your site, fill in this form and click the *Create Plone Site* button.  Plone will then create and load your site.

.. note::
   The url of your local Plone instance will end with the site id you set when setting up your site.  If the site id were *Plone* then the resultant URL is: *http://localhost:8080/Plone*.

Congratulations! You should be now logged in as an admin to your new Plone instance and you'll see the front page of Plone.

Starting Plone in debug mode on UNIX
====================================

Single instance installation ("zope")
-------------------------------------

Enter to your installation folder using ``cd`` command (depends on where you have installed Plone)::

   cd ~/Plone/zintance # Default local user installation location

For root installation the default location is ``/usr/local/Plone``.

Type in command::

    bin/instance fg

Press CTRL+C to stop.

Clustered installation ("zeo")
------------------------------

If you have ZEO cluster mode installation you can start individual processes in debug mode::

    cd ~/Plone/zeocluster
    bin/zeoserver fg & # Start ZODB database server
    bin/client1 fg &  # Start ZEO front end client 1 (usually port 8080)
    # bin/client2 fg  # For debugging issues it is often enough to start client1

Determining programmatically whether Zope is in debug mode
==========================================================

Zope2's shared global data *Globals*, keeps track on whether Zope2 is started
in debug mode or not.::

    import Globals
    if Globals.DevelopmentMode:
        # Zope is in debug mode

.. note::
   There is a difference between Zope being in debug mode and the JavaScript
   and CSS resource registries being in debug mode (although they will
   automatically be set to debug mode if you start Zope in debug mode).

