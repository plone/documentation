===============================
Plone Installation Requirements
===============================

.. admonition:: Description

    Requirements for installing Plone. Details the tools and libraries (dependencies) required to install Plone.


Hosting requirements
====================

To run a Plone based web site on your own server you need:

* A server machine connected to Internet (public sites) or your intranet (company intranet sites);

* Remote console, like SSH access, for installing Plone. FTP is not enough.

Plone requires several system libraries.
These need to be installed by a user with root access.
If you would like to install Plone using a consumer hosting service, you must ensure that the service includes SSH and root access.

Operating system
----------------

Plone has been successfully installed on:

* Nearly every popular Linux distribution;

* Nearly every popular BSD distribution

* OS X (using our OS X installer or XCode)

* Solaris and several other proprietery \*nix systems

* Windows

Hardware (or virtual environment) requirements
----------------------------------------------

The hardware requirements below give a rough estimate of the minimum hardware setup needed for a Plone server.

Add-on products and caching solutions may increase RAM requirements.

A single Plone installation is able to run many Plone sites.
This makes it easy to host multiple sites on the same server.

Plone runs on:

* Raspberry Pi
* Chromebooks
* Windows PCs
* Macs
* servers
* containers such as Docker
* virtual machines such as Vagrant
* cloud services such as Amazon, Rackspace, and Linode

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

What follows is an overview of Plone's overall software requirements.
Each Plone installer (Unified Installer, Vagrant/VirtualBox, Windows buildout) will manage its dependencies and requirements differently.

Windows
-------

Plone requires Python and Visual C++.

UNIX-based platforms
--------------------

Plone requires Python and a complete GNU build kit including GCC including gcc, gmake, patch, tar,
gunzip, bunzip2, wget.

Most required libraries listed below must be installed as development versions (dev).

Tools and libraries marked with "\*" are either included with the Unified Installer or automatically downloaded.

If you use your system Python, you should use Python's virtualenv to create an isolated virtual Python.
System Pythons may use site libraries that will otherwise interfere with Zope/Plone.

Optional libraries
------------------

If Plone can find utilities that convert various document formats to text, it will include them in the site index.
To get PDFs and common office automation formats indexed, add:

* poppler-utils (PDFs)
* wv (office docs)

These may be added after initial installation.

Plone 5
=======

Python
------

Python 2.7 (dev), built with support for expat (xml.parsers.expat), zlib and ssl.
With Plone 5.2 or greater, Python 2.7.14, 3.6, and 3.7 are supported.
See :doc:`manage/upgrading/version_specific_migration/upgrade_to_python3` for Plone 5.2 requirements.
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


You may also need to install dependencies needed by `Pillow <https://pillow.readthedocs.org/en/latest/>`_ a fork of the Python Image Libary.
For further information please read: https://pillow.readthedocs.org/en/latest/installation.html

