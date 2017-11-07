====================
Preparing The Server
====================

Plone and Zope are generally not available via platform package or port systems.

You can’t “apt-get install plone” to add it to a Debian server.
(There are packages and ports out there, if you search hard enough to find them.

Do not do it: they’ve generally had a poor record for maintenance.)

This means that you typically need to build Plone (compiling source code to binary components) on your target server.


A build environment for Plone requires two sets of components:

* The GNU compiler kit and supporting components
* The development versions of system libraries required by Plone.
  The libraries themselves are in common use, and often included in standard distributions. But, we need the development header files.



It's generally best to install as many of these components as you can via platform packages or ports.
That way, you'll be able to use your platform's automated mechanisms to keep these up-to-date, particularly with security fixes.

System Python?
--------------

Plone's Unified Installer will install a suitable Python for you.
However, you may wish to use your system's Python if it meets Plone's requirements.
Plone 5 requires Python 2.7.

If you choose to use the system Python, you'll want to use virtualenv to create a virtual Python environment to isolate the Zope/Plone install from system Python packages.
The Unified Installer will automatically do this for you.
If you're not using the Unified Installer, learn to use virtualenv.

Basic Build Components
----------------------

All installs will require the basic GNU build and archive tools: gcc, g++, gmake, gnu tar, gunzip, bunzip2 and patch.

On Debian/Ubuntu systems, this requirement will be taken care of by installing build-essential.
On RPM systems (RedHat, Fedora, CentOS), you'll need the gcc-c++ (installs most everything needed as a dependency) and patch RPMs.

On Arch Linux you'll need base-devel (installs most everything needed as a dependency).

System Python
~~~~~~~~~~~~~

If you're using your system's Python, you will need to install the Python development headers so that you'll be able to build new Python components.

On Debian/Ubuntu systems, this is usually the python-dev package.

Port installs will automatically include the required python.h requirement as part of their build process.

If you're using your system Python, you will not need the readline and libssl development packages mentioned below.
The required libraries should already be linked to your Python.

System libraries
~~~~~~~~~~~~~~~~

For any install, the development versions of:

* libssl
* libz
* libjpeg
* readline
* libxml2/libxslt

If you're using the System Python, add:

* build-essential (gcc/make tools)
* python-dev

Without the system Python (Unified Installer builds Python):

build-essential (gcc/make)

You may also need to install dependencies needed by `Pillow <https://pillow.readthedocs.org/en/latest/>`_ a fork of the Python Image Libary.
For further information please read: https://pillow.readthedocs.org/en/latest/installation.html


Optional libraries
~~~~~~~~~~~~~~~~~~

If Plone can find utilities that convert various document formats to text, it will include them in the site index.
To get PDFs and common office automation formats indexed, add:

* poppler-utils (PDFs)
* wv (office docs)

Development versions are not needed for these.


Platform Notes
~~~~~~~~~~~~~~

Debian/Ubuntu
+++++++++++++

.. note::

   If you want to use System Python Packages with Ubuntu 16.04 you need to install:

   - pyhon2.7
   - python2.7-dev

   ``apt install pyhon2.7 python2.7-dev``


Use ``apt install``. The matching package names are:

* build-essential
* libssl-dev
* libz-dev
* libjpeg-dev
* libreadline-dev
* libxml2-dev
* libxslt-dev
* python-dev


Fedora
++++++

Using ``dnf install``:

* gcc-c++
* patch
* openssl-devel
* libjpeg-devel
* libxslt-devel
* readline-devel
* make
* which
* python-devel
* wv
* poppler-utils


CentOS
++++++

Using ``yum install``:

* gcc-c++
* patch
* openssl-devel
* libjpeg-devel
* libxslt-devel
* readline-devel
* make
* which
* python-devel
* wv
* poppler-utils

OpenSUSE
++++++++

Using ``zypper in``

* gcc-c++
* make
* readline-devel
* libjpeg-devel
* zlib-devel
* patch
* libopenssl-devel
* libexpat-devel
* man

``--build-python`` will be needed as the system Python 2.7 is missing many standard modules.

Arch Linux
++++++++++

Using ``pacman -S``

* base-devel
* libxml2
* libxslt
* libjpeg-turbo
* openssl

OS X
++++

Installing XCode and activating the optional command-line utilities will give you the basic GNU tools environment you need to install Plone with the Unified Installer.
You may also use MacPorts (the BSD ports mechanism, tailored to OS X) to install libjpeg, libxslt and readline.

If you do, remember to keep your ports up-to-date, as Apple's updates won't do it for you.

Creating a Plone User
---------------------

While testing or developing for Plone, you may have used an installation in a home directory, owned by yourself.
That is not suitable for a production environment.

Plone's security record is generally excellent, however there have been - and probably will be again in the future - vulnerabilities that allow an attacker to execute arbitrary commands with the privileges of the process owner.

To reduce this kind of risk, Plone - and all other processes that allow Internet connections - should be run with user identities that have the minimum privileges necessary to maintain their data and write logs.

In a Unix-workalike environment, the most common way of accomplishing this is to create a special user identity under which you will run Plone/Zope.

That user identity should ideally have no shell, no login rights, and write permissions adequate only to change files in its ./var directory.

The ideal is hard to achieve, but it's a good start to create an unprivileged "plone" user, then use "sudo -u plone command" to install Plone and run buildout.

This is what the Unified Installer will do for you if you run its install program via sudo.
The installer uses root privileges to create a "plone" user (if one doesn't exist), then drops them before running buildout.

.. warning:: Don't run buildout as root!

    Don't use bare "sudo" or a root login to run buildout.
    Buildout fetches components from the Python Package Index and other repositories.
    As part of package installation, it necessarily executes code in the setup.py file of each package.
