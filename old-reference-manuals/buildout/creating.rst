=====================================
Creating a buildout for your project
=====================================

.. admonition:: Description

  How to create a new buildout for a project, adding Plone and other third party products as dependencies


We are now ready to create a new buildout. The "buildout" is a
directory containing all the parts that make up a project,
including a Zope instance, the Plone sources, custom configuration
options, and your our project's source code.


.. note:: 

     As of Plone 3.2, all of the Plone installers are buildout based. 
     You can get the latest `installer`_ and run it to have a working
     buildout without having to follow these steps. However, these steps
     are still valid if you want to create the buildout manually with
     ZopeSkel.

Create one like this:

::

    $ paster create -t plone3_buildout myproject

This will ask a series of questions. If you want to use an existing
installation of Zope rather than have buildout download and compile
one for you, specify an absolute path as the *zope2\_install*.
Similarly, if you do not want buildout to download the core Plone
products, you can point it to an existing directory containing all
the products (it will still download Plone 3's eggs, but as we will
see later, it is possible to share an eggs directory among multiple
buildouts). You will need to enter a Zope administrator username
and password, and you may want to turn debug mode and verbose
security *on* during development.

Now, enter the newly created myproject directory, and run the
buildout bootstrap script.  NOTE: Python 2.4 is currently required
to Plone 3.x:

::

    $ cd myproject
    $ python2.4 bootstrap.py

This will create a number of directories and scripts and download
the latest version of the zc.buildout egg. This step should be
needed only once.

To get started straight away, run:

::

    $ ./bin/buildout

This reads the generated buildout.cfg file and executes its various
"parts", setting up Zope, creating a Zope instance, downloading and
installing Plone. We will explain this file in more detail
shortly.

You will need to run *./bin/buildout* again each time you change
*buildout.cfg*. If you do not want buildout to go online and look
for updated versions of eggs or download other archives, you can
run it in non-updating, offline mode, with;

::

    $ ./bin/buildout -No

To start Zope in foreground and debug mode, run:

::

    $ ./bin/instance fg

The *instance* script is analogous to *zopectl* as found in a
standard Zope instance. You can use *./bin/instance start* to run
Zope in daemon mode. It can also be used to run tests:

::

    $ ./bin/instance test -s plone.portlets

Running:

::

    bin/instance console

is equivalent to *bin/instance fg*, but does not implicitly turn on
debug mode but respects the *debug-mode* setting in *buildout.cfg*.
This can be useful to run Zope in non-development mode with
daemon-control programs like supervisord.

Once your buildout installation is up and running, you will still
need to install a Plone site.  Log in to the Zope Management
Interface (ZMI) and from "select type to add..." choose Plone
Site.  Fill in the required details and submit.  Now you have a
Plone site at the ID that you specified.

Directories in the buildout
---------------------------

Before we dive into buildout.cfg, let us take a quick look at the
directories that buildout has created for us:

bin/
    Contains various executables, including the *buildout* command, and
    the *instance* Zope control script.
eggs/ 
    Contains eggs that buildout has downloaded. These will be
    explicitly activated by the control scripts in the *bin/*
    directory.
downloads/ 
    Contains non-egg downloads, such as the Zope source code archive.
var/ 
    Contains the log files (in *var/log/*) and the file storage ZODB
    data (in *var/filestorage/Data.fs*). Buildout will never overwrite
    these.
    If you want to import a .zexp file, place it in the
    *var/instance/imports* folder.
    Previously one had to put that file into *parts/instance/import*,
    but this folder gets wiped and regenerated when running
    *bin/buildout*, so the import location was changed.

src/ 
    Initially empty. You can place your own development eggs here and
    reference them in *buildout.cfg*. More on that later.
products/ 
    This is analogous to a Zope instance's *Products/* directory (note
    the difference in capitalisation). If you are developing any
    old-style Zope 2 products, place them here. We will see how
    buildout can automatically download and manage archives of
    products, but if you want to extract a product dependency manually,
    or check one out from Subversion, this is the place to do so.
parts/
    Contains code and data managed by buildout. In our case, it will
    include the local Zope installa TRUNCATED! Please download pandoc
    if you want to convert large files.

.. note::

   You can check in a buildout directory to a source code repository
   to share it  among developers. In this case, you should ignore
   the directories bin/, eggs/, downloads/, var/, and parts/. Each
   developer can run bootstrap.py to get these back, and will
   normally need local copies anyway. All your configuration should be
   in the buildout.cfg file, and all custom code in src/ or products/.

.. _installer: http://plone.org/products/plone
