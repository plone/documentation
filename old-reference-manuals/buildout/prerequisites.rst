==============
Prerequisites
==============

.. admonition:: Description

   A few things you need before we can get started.

Before we can create a buildout to manage Zope and Plone, there are
a few prerequisites to take care of.

As of Plone 3.2, all of the Plone installers are buildout based. 
You can get the latest `installer`_ and run it to have a working
buildout without having to follow these steps. However, these steps
are still valid if you want to create the buildout manually with
ZopeSkel.

First, you will need an appropriate Python interpreter, if you do
not have one already:


-  Install `Python 2.4`_ for your platform, and add it to your
   system *PATH*. It is easiest if Python 2.4 is what you get when you
   type *python -V* on a command line. Make sure you're using Python
   2.4 and not 2.5, since Plone 3.x doesn't support Python 2.5 or
   later. You might need to type *python2.4* instead of just *python*
   when running some of the following commands.
-  If you installed Python using an operating system package (e.g.
   an RPM), make sure you get the development package (e.g.
   python-devel) as well. This includes Python header files that we
   will use later to compile Zope. If you installed from source, or
   used the Python Windows installer, you should already have these.
-  Install `PIL`_, the Python Imaging Library into this Python
   interpreter.
-  Install `setuptools`_. If you're using Linux and your
   distribution doesn't provide a package for setuptools, download
   `ez\_setup.py`_ and run it with:
   ::

       $ python ez_setup.py

   This will download and install setuptools and the
   *easy\_install* script. Watch the console output to understand where
   *easy\_install* is installed. If this is not in your system *PATH*,
   you should add this directory to the path as well.


Finally, use *easy\_install* to get *ZopeSkel*, a collection of
skeleton templates for Zope and Plone development:

::

    $ easy_install -U ZopeSkel

This will get *Paste Script* and various other dependencies.

Linux note: If you're installing setuptools and ZopeSkel
system-wide, you will probably need to become superuser or use
sudo, if you're not using virtualenv or similar. But please note
that bin/buildout (introduced later) should never be run as root.
If you really can't avoid running this script as root, don't forget
to change the owner of created files (chown -R) so the unprivileged
user that runs the zope instance will be able to read those files.

If you added the Python console scripts directory (where
*easy\_install* was placed) to your system path, you should now be
able to run the *paster* command. You can test it with:

::

    $ paster create --list-templates
    Available templates:
      archetype:                A Plone project that uses Archetypes content types
      basic_namespace:          A basic Python project with a namespace package
      basic_package:            A basic setuptools-enabled package
      basic_zope:               A Zope project
      kss_plugin:               A project for a KSS plugin
      nested_namespace:         A basic Python project with a nested namespace (2 dots in name)
      paste_deploy:             A web application deployed through paste.deploy
      plone:                    A project for Plone products
      plone2.5_buildout:        A buildout for Plone 2.5 projects
      plone2.5_theme:           A theme for Plone 2.5
      plone2_theme:             A theme for Plone 2.1
      plone3_buildout:          A buildout for Plone 3 installation
      plone3_portlet:           A Plone 3 portlet
      plone3_theme:             A theme for Plone 3
      plone4_buildout:          A buildout for Plone 4 developer installation
      plone_app:                A project for Plone products with a nested namespace (2 dots in name)
      plone_hosting:            Plone hosting: buildout with ZEO and Plone versions below 3.2
      plone_pas:                A project for a Plone PAS plugin
      recipe:                   A recipe project for zc.buildout
      silva_buildout:           A buildout for Silva projects


Your output may differ slightly, but make sure you have the
*plone3\_buildout* and *plone* templates at least.

Additional installation steps for Windows
-----------------------------------------

If you are using Windows, there are a few more things you need to
do.

First, get and install the `Python Win32 extensions`_ for Python
2.4.

If you intend to compile Zope yourself, rather than using a binary
installer, or if you ever need to compile an egg with C extensions,
you will need the `mingw32 compiler`_. Make sure you choose the
"base" and "make" modules at a minimum when the installer asks. By
default, this installs into *C:\\MingW32*. Inside the installation
directory, there will be a bin directory, e.g. *C:\\MingW32\\bin*.
Add this to your system *PATH*.

Finally, you need to configure Python's *distutils* package to use
the mingw32 compiler. Create a file called *distutils.cfg* in the
directory *C:\\Python24\\Lib\\distutils* (presuming Python was
installed in *C:\\Python24*, as is the default). Edit this with
Notepad, and add the TRUNCATED! Please download pandoc if you want
to convert large files.

.. _installer: http://plone.org/products/plone
.. _Python 2.4: http://www.python.org/download/releases/
.. _PIL: http://www.pythonware.com/products/pil/
.. _setuptools: http://peak.telecommunity.com/DevCenter/setuptools
.. _ez\_setup.py: http://peak.telecommunity.com/dist/ez_setup.py
.. _Python Win32 extensions: http://downloads.sourceforge.net/pywin32/pywin32-210.win32-py2.4.exe?modtime=1159009237&big_mirror=0
.. _mingw32 compiler: http://downloads.sourceforge.net/mingw/MinGW-5.1.3.exe?modtime=1168794334&big_mirror=1
