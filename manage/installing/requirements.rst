===============================
Plone Installation Requirements
===============================

.. admonition:: Description

    Requirements for installing Plone. Details the tools and libraries
    (dependencies) required to install Plone.

.. contents:: :local:

.. highlight:: console

Hosting requirements
====================

To run a Plone based web site on your own server you need:

* A server machine connected to Internet (public sites) or your intranet (company intranet sites);

* Remote console, like SSH access, for installing Plone. FTP is not enough.

Plone requires several system libraries. These need to be installed by a user
with root access.

Operating system
----------------

Plone has been successfully installed on:

* Windows

* Nearly every popular Linux distribution;

* Nearly every popular BSD distribution

* OS X (using our OS X installer or XCode)

* Solaris and several other proprietery \*nix systems

To install on Windows, it is strongly recommended to use the Plone Windows
Installer. Otherwise, you will need `Cygwin <http://www.cygwin.com>`_ to
provide a \*nix build environment.

Hardware (or virtual environment) requirements
----------------------------------------------

The hardware requirements below give a rough estimation of the minimum hardware setup needed for a Plone server.

Add-on products and caching solutions may increase RAM requirements.

One Zope application server is able to run several Plone sites with the same software configuration. This lowers the requirements when hosting multiple sites on the same server.

Minimum requirements
~~~~~~~~~~~~~~~~~~~~

* Minimum 256 MB RAM and 512 MB of swap space per Plone site

* Minimum 512 MB hard disk space

Recommended
~~~~~~~~~~~

* 2 GB or more RAM per Plone site

* 40 GB or more hard disk space


All Plone versions
==================

A complete GNU build kit including GCC including gcc, gmake, patch, tar,
gunzip, bunzip2, wget.

Most required libraries listed below must be installed as development versions (dev).

Tools and libraries marked with "*" are either included with the Unified
Installer or automatically downloaded.

If you use your system Python, you should use Python's virtualenv to create an
isolated virtual Python. System Pythons may use site libraries that will
otherwise interfere with Zope/Plone.

Optional libraries
------------------

If Plone can find utilities that convert various document formats to text, it will include them in the site index. To get PDFs and common office automation formats indexed, add:

* poppler-utils (PDFs)
* wv (office docs)

These may be added after initial installation.

Plone 4.3 / 4.2
===============

Python
------

Python 2.7 (dev), built with support for expat (xml.parsers.expat), zlib and ssl.
(Python XML support may be a separate package on some platforms.)*

virtualenv*

Libraries
---------

* libz (dev)
* libjpeg (dev)*
* readline (dev)*
* libexpat (dev)
* libssl or openssl (dev)
* libxml2 >= 2.7.8 (dev)*
* libxslt >= 1.1.26 (dev)*

Plone 4.1
=========

Python
------

Python 2.6 (dev), built with support for expat (xml.parsers.expat), zlib and ssl.
(Python XML support may be a separate package on some platforms.)*

virtualenv*

Libraries
---------

* libz (dev)
* libjpeg (dev)*
* readline (dev)*


Minimal build
=============

With complete requirements in place, a barebones Plone install may be created with a few steps. 
``~/$`` is a system prompt. 

.. code-block:: bash

    ~/$ mkdir Plone-4.3
    ~/$ cd Plone-4.3
    ~/Plone-4.3$ virtualenv-2.7 Python-2.7
    ~/Plone-4.3$ mkdir zinstance
    ~/Plone-4.3$ cd zinstance
    ~/Plone-4.3/zinstance$ wget http://downloads.buildout.org/1/bootstrap.py
    ~/Plone-4.3/zinstance$ echo """
    [buildout]
    extends =
        http://dist.plone.org/release/4.3-latest/versions.cfg

    parts =
        instance

    [instance]
    recipe = plone.recipe.zope2instance
    user = admin:admin
    http-address = 8080
    eggs =
        Plone
        Pillow

    """ > buildout.cfg
    ~/Plone-4.3/zinstance$ ../Python-2.7/bin/python bootstrap.py
    ~/Plone-4.3/zinstance$ bin/buildout

This will start a long download and build process ...

Errors like "SyntaxError: ("'return' outside function"..."" may be ignored.

After it finished you can start Plone in foreground-mode with:

.. code-block:: bash
    
    ~/Plone-4.3/zinstance$ bin/instance fg

You can stop it with ``ctrl + c``.

Start and stop this Plone-instance in production-mode like this;

.. code-block:: bash
    
    ~/Plone-4.3/zinstance$ bin/instance start

    ~/Plone-4.3/zinstance$ bin/instance stop

Plone will run on port 8080 and can be accessed via http://localhost:8080. 
Use login id "admin" and password "admin" for initial login so you can create a site.

This build would be adequate for a quick evaluation installation. For a
production or development installation, use one of `Plone's installers
<http://plone.org/products/plone>`_.
