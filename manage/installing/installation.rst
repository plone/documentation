==============
 Installation
==============

.. admonition:: Description

    Installation instructions for Plone for various operating systems and situations.

.. contents:: :local:

.. highlight:: console

.. note::

    This is a beta for Plone 5 and still WIP

    Todo:

    - mention docker
    - more ?


Introduction
============

This document covers the basics of installing Plone on popular operating systems.
It will also point you to other documents for more complex or demanding installations.

Plone runs as an application on the Zope application server.
That server is installed automatically by the install process.

.. warning::

    We strongly advise against installing Plone via OS packages or ports.
    There is no .rpm, .deb, or BSD port that is supported by the Plone community. Plone dependencies can and should be installed via package or port -- but not Plone itself.

Download Plone
==============

Plone is available for Mac OSX X, Linux and BSD operating systems.
For Windows, we currently advise running Plone 5 in a virtualmachine or Vagrant image. We anticipate having a binary windows installer for later releases.

`Download the latest Plone release <http://plone.org/products/plone/latest_release>`_.

From here, you can also find links to the Vagrant install kit (if you wish to install Plone for evaluation or development on a Windows, OS X or any other machine that supports VirtualBox and Vagrant).

Installation on Linux, BSD and other Unix workalikes requires a source code installation, made easy by our Unified Installer.
"Unified" refers to its ability to install on most Unix workalikes.

Plone installation requirements
===============================

See :doc:`Plone installation requirements <requirements>` for detailed requirements.

* You need at a dedicated or virtual private server (VPS) with 512 MB RAM available.
  Shared hosting is not supported unless the shared hosting company says Plone is good to go.



How to install Plone
====================

Plone can run on all popular desktop or server operating systems, including Linux, OS X, BSD and Microsoft Windows.
(Note: currently there is no binary installer for Plone 5 on Windows, we recommend using the `Vagrant kit <https://github.com/plone/plonedev.vagrant>`__)

* You can install Plone on a server for production usage

* You can install Plone locally on your own computer for development and test drive

Ubuntu / Debian
---------------

We describe Ubuntu/Debian installation in detail as an example of installation on a common Linux distribution.
The only difference for most other systems would be in package-manager commands and package names. See :doc:`Plone installation requirements <requirements>` for package names and commands on other platforms.

Installing Plone using the Unified UNIX Installer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

  Running Plone in **production** will normally also entail other software for optimal security and performance, like a front-end webserver, caching, and firewall.

  See :doc:`Deploying and installing Plone in production </manage/deploying/production/index>` , and you may also be interested in :doc:`automated full-stack deployment </external/ansible-playbook/docs/index>`.

This recipe is good for:

* Plone development and testing on Ubuntu / Debian

* Operating system installations where you have administrator (root) access.
  Note that root access is not strictly necessary as long as you have required software installed beforehand on the server, but this tutorial assumes you need to install the software yourself and you are the admin.
  If you don't have the ability to install system libraries, you'll need to get your sysadmin to do it for you.
  The libraries required are in common use.

The resulting installation is self-contained, does not touch system files, and is safe to play with (no root/sudoing is needed).

If you are not familiar with UNIX operating system command line you might want to study this `Linux shell tutorial <http://linuxcommand.org/learning_the_shell.php>`_ first.

Instructions are tested for the *Ubuntu 14.04 Long Term Support* release.

Install the operating system software and libraries needed to run Plone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    sudo apt-get install python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev

.. note::

    If the **sudo** command is not recognized or does not work you don't have administrator rights to Ubuntu / Debian operating system.
    Please contact your server vendor or consult the operating system support forum.


You will probably also want these optional system packages for handling of PDF and Office files:

.. code-block:: console

    sudo apt-get install libreadline-dev wv poppler-utils

.. note::

    **libreadline-dev** is only necessary if you wish to build your own python rather than use your system's python 2.7.

If you're planning on developing with Plone, install git version control support::

    sudo apt-get install git






Download the latest Plone unified installer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download from `the plone.org download page <http://plone.org/download>`_ to your server using wget command. Curl also works.
Substitute the latest version number for 5.0rc1 in the instructions below.

.. code-block:: console

    wget --no-check-certificate https://launchpad.net/plone/5.0/5.0rc2/+download/Plone-5.0rc2-UnifiedInstaller.tgz

Run the Plone installer in standalone mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    # Extract the downloaded file
    #
    tar -xf Plone-5.0rc2-UnifiedInstaller.tgz
    #
    # Go the folder containing installer script
    #
    cd Plone-5.0rc2-UnifiedInstaller
    #
    # Run script
    ./install.sh


install.sh has many options, and will guide you through the options.

If you prefer to set the options directly on the command-line, use:

.. code-block:: console

    ./install.sh --help

to discover all of the command-line switches.

The default admin credentials will be printed to the console, and saved in the file adminPassword.txt in the resulting install.
You can change this password after logging in to the Zope Management Interface.

.. note::

   The password is also written down in the ``buildout.cfg`` file, but this
   setting is not effective after Plone has been started for the first time.
   Changing this setting does not do any good.

Install the Plone developer tools
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're using this Plone install for development, add the common development tool set.

.. code-block:: console

    cd ~/Plone/zinstance
    bin/buildout -c develop.cfg

You'll need to add the "-c develop.cfg" again each time you run buildout, or you'll lose the extra development tools.

Start Plone
~~~~~~~~~~~

If you're developing, start Plone in foreground mode for a test run (you'll see potential errors in the console):

.. code-block:: console

    cd ~/Plone/zinstance
    bin/plonectl fg

When you start Plone in the foreground, it runs in debug mode, which is much slower than production mode since it reloads templates for every request.

For evaluation, instead use:

.. code-block:: console

    cd ~/Plone/zinstance
    bin/plonectl start

Use

.. code-block:: console

    cd ~/Plone/zinstance
    bin/plonectl stop

to stop the instance.

By default, Plone will listen to port 8080 on available network interfaces.
The port may be changed by editing buildout.cfg and re-running buildout.

You've got Plone
~~~~~~~~~~~~~~~~

Now take a look at your Plone site by visiting the following address in your webbrowser::

    http://yourserver:8080

The greeting page will let you create a new site.
For this you need the login credentials printed to your terminal earlier, also available at ``~/Plone/zinstance/adminPassword.txt``.

If everything is OK, press ``CTRL-C`` in the terminal to stop Plone if you're running in debug mode. Use the ``plonectl stop`` command if you didn't start in debug mode.

If you have problems, please see the `help guidelines <http://plone.org/help>`_.

For automatic start-up when your server boots up, init scripts, etc.
please see the :doc:`deployment guide </manage/deploying/production/index>`.


Installing Plone using RPMs, .dev, ... packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not supported by Plone community. Plone dependencies can and should be installed via your operating system package manager, to profit from security updates and maintenance, but not Plone itself. The packages that have been offered in the past via apt, yup, port etcetera tend to be unmaintained, old and unsuitable.


Microsoft Windows
-----------------

Installing Plone on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^

For Plone 5, there currently is no binary installer. We recommend using the `Vagrant kit <https://github.com/plone/plonedev.vagrant>`__

We anticipate offering a binary installer for Windows at a later moment.

For the Plone 4.3 series, there is a `binary installer <https://plone.org/products/plone/releases/4.3.6>`_.

If you wish to develop Plone on Windows you need to set-up a working MingW environment (this can be somewhat painful if you aren't used to it).


OSX
---

Installing Plone using VirtualBox/Vagrant install kit or VirtualBox appliance
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the recommended method if you want to try Plone for the first time.

Please use the installer from the download page `<http://plone.org/products/plone/releases>`_.



Installing Plone from source on OS X
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installation via the Unified Installer or buildout is very similar to Unix.
However, you will need to install a command-line build environment. To get a free build kit from Apple, do one of the following:

* Download gcc and command-line tools from
  https://developer.apple.com/downloads/. This will require an Apple
  developer id.

* Install Xcode from the App Store. After installation, visit the Xcode
  app's preference panel to download the command-line tools.

After either of these steps, you immediately should be able to install Plone using the Unified Installer.

Proceed as with Linux.

LibXML2/LibXSLT Versions
------------------------

Don't worry about this if you're using an installer.

Entering debug mode after installation
======================================

When you have Plone installed and want to start development you need do :doc:`enter debug mode </develop/plone/getstarted/debug_mode>`.

Installer source code
======================

* https://github.com/plone/Installers-UnifiedInstaller
