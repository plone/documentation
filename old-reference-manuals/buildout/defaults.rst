===================================
Creating a buildout defaults file
===================================


.. admonition:: Description

  This makes it possible to share configuration across multiple
  buildouts, and save some time and disk space.

To set "global" options affecting all buildouts, create a directory
*.buildout* (note leading dot) in your home directory, and add a
file there called *default.cfg*. Any option set here will be
applied to the corresponding section in any *buildout.cfg that you
run, unless it is overridden by a more specific option in the
*buildout.cfg* file itself.

.. note ::

        Windows may error when creating the *.buildout* directory with
        "You must type a file name" due to the leading dot. This directory
        can be created using the command line. Once created, it can
        be accessed normally in the Windows gui.

The most common options are:

executable 
    Specify a python interpreter other than the system default. This is
    useful if you have Python 2.5 installed, say, but you want your
    buildouts to use another installation of Python 2.4.
eggs-directory 
    Specify a directory where eggs will be downloaded. This allows
    multiple buildouts to share the same eggs, saving disk space and
    download time. Note that only those eggs explicitly required by a
    particular buildout will be activated. The eggs directory may
    contain many more eggs (or many different versions of the same
    package) than what is used at any one time.
download-cache 
    Specify a shared directory for downloaded archives. Again, this can
    save disk space and download time. NOTE: before zc.buildout 1.0,
    this was called download-directory
extends-cache 
    Specify a shared directory for extended buildout configurations
    that are downloaded from a URL. As of Plone 3.2 this is how Plone
    pins the `versions`_ of its eggs. This option was added in
    `zc.buildout 1.4.1`_, prior to that the offline mode in combination
    with a extends URL would not work.

Here is an example *~/.buildout/default.cfg* setting all three:

::

    [buildout]
    executable = /opt/python24/bin/python
    eggs-directory = /home/username/.buildout/eggs
    download-cache = /home/username/.buildout/downloads
    extends-cache = /home/username/.buildout/extends

This assumes Python 2.4 is installed in */opt/python2.4*. For the
last two options to work, you would need to create the directories
*eggs* and *downloads* inside the *~/.buildout* directory.

.. _versions: http://dist.plone.org/release/3.2/versions.cfg
.. _zc.buildout 1.4.1: http://pypi.python.org/pypi/zc.buildout/1.4.1#specifying-extends-cache-and-offline-mode
