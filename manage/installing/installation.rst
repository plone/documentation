=======================
 Installation
=======================

.. admonition:: Description

    Installation instructions for Plone for various operating systems and situations.

.. contents:: :local:

.. highlight:: console

Introduction
=============

This document covers the basics of installing Plone on popular operating systems.
It will also point you to other documents for more complex or demanding installations.

Plone runs as an application on the Zope application server. That server is installed automatically by the install process.

.. warning::

    We strongly advise against installing Plone via OS package or port. There is no .rpm, .deb, or BSD port that is supported by the Plone community. Plone dependencies can and should be installed via package or port -- but not Plone itself.

Download Plone
===================

Plone is available for Microsoft Windows, Mac OSX X, Linux and BSD operating systems.

`Download the latest Plone release <http://plone.org/products/plone/latest_release>`_.

Binary installers are available for Windows and OS X. Installation on Linux, BSD and other Unix workalikes requires a source code installation, made easy by our Unified Installer. "Unified" refers to its ability to install on most Unix workalikes.

Plone installation requirements
========================================================

See :doc:`Plone installation requirements <requirements>` for detailed requirements.

* You need at a dedicated or virtual private server (VPS) with 512 MB RAM available.
  Shared hosting is not supported unless the shared hosting company says Plone is good to go.
  See :doc:`Plone installation requirements <requirements>`.


* If you are installing for production - rather than testing or evaluation - review :doc:`Deploying and installing Plone in production </manage/deploying/production/index>` before installation.




How to install Plone
========================================================

Plone can run on all popular desktop or server operating systems, including
Linux, OS X, BSD and Microsoft Windows.

* You can install Plone on a server for production usage

* You can install Plone locally on your own computer for development and test drive

Ubuntu / Debian
---------------

We describe Ubuntu/Debian installation in detail as an example of installation on a common Unix workalike. The only difference for most other systems would be in package-manager commands and package names. See :doc:`Plone installation requirements <requirements>` for package names and commands on other platforms.

Installing Plone using the Unified UNIX Installer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

.. note::

  This is the recommended method for
  a *development or evaluation* installation of Plone on a Unix workalike.
  For a *production* installation, :doc:`Installing Plone for Production on Ubuntu </manage/deploying/production/ubuntu_production>` is a much better guide.

This recipe is good for:

* Plone development and testing on Ubuntu / Debian

* Operating system installations where you have administrator (root) access. Note that
  root access is not strictly necessary as long as you have required software installed
  beforehand on the server, but this tutorial assumes you need to install the software
  yourself and you are the admin. If you don't have the ability to install system libraries, you'll need to get your sysadmin to do it for you. The libraries required are in common use.

The resulting installation is self-contained,
does not touch system files,
and is safe to play with (no root/sudoing is needed).

If you are not familiar with UNIX operating system command line
you might want to study this `Linux shell tutorial <http://linuxcommand.org/learning_the_shell.php>`_
first.

For information on using this installation with more advanced production
hosting environments and deployments,
see the :doc:`deployment guide </manage/deploying/production/index>`.

Instructions are tested for the *Ubuntu 12.04 Long Term Support* release.

Install the operating system software and libraries needed to run Plone
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    sudo apt-get install python-setuptools python-dev build-essential libssl-dev libxml2-dev libxslt1-dev libbz2-dev libjpeg62-dev

You will probably also want these optional system packages (see `Plone manual for more information <http://plone.org/documentation/manual/installing-plone/installing-on-linux-unix-bsd/debian-libraries>`_):

.. code-block:: console

    sudo apt-get install libreadline-dev wv poppler-utils

.. note::

    **libreadline-dev** is only necessary if you wish to build your own python rather than use your system's python 2.7.

If you're planning on developing with Plone, install git version control support::

    sudo apt-get install git

.. note::

    If sudo command is not recognized or does not work you don't have administrator rights to Ubuntu / Debian operating system.
    Please contact your server vendor or consult the operating system support forum.

.. note::

    For Ubuntu 14.04 please also install **libz-dev**


Download the latest Plone unified installer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Download from `the plone.org download page <http://plone.org/download>`_ to your server using wget command. Curl also works.
Substitute the latest version number for 4.3.4
in the instructions below.

.. code-block:: console

    wget --no-check-certificate https://launchpad.net/plone/4.3/4.3.4/+download/Plone-4.3.4-UnifiedInstaller.tgz

Run the Plone installer in standalone mode
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: console

    # Extract the downloaded file
    #
    tar -xf Plone-4.3.4-UnifiedInstaller.tgz
    #
    # Go the folder containing installer script
    #
    cd Plone-4.3.4-UnifiedInstaller
    #
    # Run script
    ./install.sh standalone

install.sh has many options, use:

.. code-block:: console

    ./install.sh --help

to discover them.

The default admin credentials will be printed to the console.
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
That may be changed by editing buildout.cfg and re-running buildout.

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

Installing Plone using buildout on Ubuntu / Debian
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Here are quick instructions to install Plone using a pre-installed buildout and the OS-provided
Python interpreter.
This procedure is only useful if you know buildout well enough to
tailor your own buildout configuration.

You need to manage dependencies (``Python``, ``libxml``, ``Pillow``) yourself.

This will:

* create a default ``buildout.cfg`` configuration file and folder structure
  around it;

* automatically download and install all packages from `pypi.python.org <http://pypi.python.org>`_;

* configure Plone and Zope for you.

1. Install ``virtualenv`` for python (on Ubuntu):

   .. code-block:: console

        sudo apt-get install python-virtualenv

2. Create a ``virtualenv`` where you can install some Python packages
   (``ZopeSkel``, ``Pillow``):

   .. code-block:: console

        virtualenv plone-virtualenv

3. In this virtualenv install ``ZopeSkel`` (from the release 2 series):

   .. code-block:: console

        source plone-virtualenv/bin/activate
        easy_install "ZopeSkel<2.99"

4. Create Plone buildout project using ZopeSkel:

   .. code-block:: console

        paster create -t plone4_buildout myplonefolder

5. Optionally edit ``buildout.cfg`` at this point.
   Run buildout (use Python 2.6 for Plone 4.1):

   .. code-block:: console

    python2.6 bootstrap.py
    bin/buildout

More info:

* :doc:`ZopeSkel </develop/addons/paste>`
* `virtualenv <https://pypi.python.org/pypi/virtualenv>`_
* `Pillow <https://pypi.python.org/pypi/Pillow/>`_
* `lxml <http://lxml.de/>`_

Installing Plone using RPMs, .dev, ... packages
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Not supported by Plone community.

(i.e. you're on your own, and don't say we didn't tell you.)

Microsoft Windows
-------------------------

Installing Plone on Windows
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

By far the easiest way to install on Windows is to use the binary installer provided on plone.org. This installation is adequate for Python development.
It is very rare to need C language extensions.

If you have needs beyond those met by the Windows Installer, read on.

For Plone 4.1 and later, see these instructions:

* https://docs.google.com/document/d/19-o6yYJWuvw7eyUiLs_b8br4C-Kb8RcyHcQSIf_4Pb4/edit

If you wish to develop Plone on Windows you need to set-up a working MingW
environment (this can be somewhat painful if you aren't used to it)


OSX
----------------------------------------------------

Installing Plone using OSX binary installer
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This is the recommended method if you want to try Plone for the first time.

Please use the installer from the download page `<http://plone.org/products/plone/releases>`_.

The binary installer is intended to provide an environment suitable for testing, evaluating, and developing theme and add-on packages.
It will not give you the ability to add or develop components that require a C compiler.
This is *very* rarely needed.

Installing Plone from source on OS X
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Installation via the Unified Installer or buildout is very similar to Unix. However, you will
need to install a command-line build environment. To get a free build kit from Apple, do one of the following:

* Download gcc and command-line tools from
  https://developer.apple.com/downloads/. This will require an Apple
  developer id.

* Install Xcode from the App Store. After installation, visit the Xcode
  app's preference panel to download the command-line tools.

After either of these steps, you immediately should be able to install Plone using the Unified Installer.

Proceed as with Linux.

LibXML2/LibXSLT Versions
------------------------

If you are installing Plone 4.2+ or 4.1 with Diazo, you will need up-to-date versions of libxml2 and libxslt::

    LIBXML2 >= "2.7.8"
    LIBXSLT >= "1.1.26"

Ideally, install these via system packages or ports. If that's not possible,
use most current version of the z3c.recipe.staticlxml buildout recipe to build an lxml (Python wrapper) egg with static libxml2 and libxslt components.

Don't worry about this if you're using an installer.

Entering debug mode after installation
=========================================

When you have Plone installed and want to start
development you need do :doc:`enter debug mode </develop/plone/getstarted/debug_mode>`.

Installer source code
======================

* https://github.com/plone/Installers-UnifiedInstaller
