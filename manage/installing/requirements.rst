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

Plone 3.3
=========

Python
------

Python 2.4 (dev), built with support for expat (xml.parsers.expat), zlib and ssl.
(Python XML support may be a separate package on some platforms.)*

virtualenv*

Libraries
---------

* libz (dev)
* libjpeg (dev)*
* readline (dev)*
* libssl or openssl (dev)
* libxml2 (dev)*
* libxslt (dev)*

