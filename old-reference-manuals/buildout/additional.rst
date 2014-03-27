=======================
Additional information
=======================

.. admonition:: Description

   Further in-depth information about dealing with buildout
   in Plone context

.. contents:: :local:

Recipes
--------

Buildout consists of *recipes*. In use, a recipe consists of:

* a Python package published to in ``pypi.python.org``,
* a declaration in ``[buildout] parts=partname``, and
* a ``[partname]`` section with a ``recipe=`` assignment specifying the
  package name at ``pypi.python.org`` name

Recipes are automatically downloaded from pypi as Python eggs.

Making buildout faster
------------------------

``easy_install`` crawls unnecessary web pages when trying to install Python eggs.
You can limit this crawl by using ``allow-hosts`` to specify a whitelist:

.. code-block:: cfg

    allow-hosts =
        github.com
        *.python.org
        *.plone.org
        *.zope.org
        launchpad.net

Buildout folder structure
--------------------------

Plone buildouts have folders with predefined purposes:

``bin/`` 
    Contains Python scripts and shell scripts installed by various eggs,
    including the ``buildout`` command itself.  The default Plone start
    script ``bin/instance`` is here.

``parts/``
    The source tree constructed by buildout. This is wiped between buildout
    runs, so you should not change anything here (note: some broken recipes
    store things like pid files here). Generated configuration files are
    stored here: don't change them directly (changes will be wiped), change
    the corresponding buildout sections instead. 

``src/``
    source code you are developing yourself.

``eggs/``
    extracted Python eggs.

``downloads/``
    Python egg download cache (may be elsewhere depending on the system
    configuration).

``var/``
    Persistent data such as logfiles, pid files, and Zope's database
    consisting of filestorage files (e.g. ``Data.fs``) and blobstorage
    directories.

``bootstrap.py`` 
    Installs the ``buildout`` command.

``buildout.cfg``
    Basic buildout file. May extend other ``.cfg`` files. Sometimes there
    are many files and you need to pick one for ``buildout`` to use; e.g.::

        bin/buildout -c production.cfg

Running buildout on Windows
-----------------------------

The Windows Plone installer provides ``buildout.exe``.
This executable uses the system Python installation.
This installation is not necessarily the correct Python
version, if multiple Pythons are installed on the computer.

Many Windows Python software uses
wrapper ``.exe`` files which pick the Python interpreter
based on registry settings. One notable exe is ``buildout.exe``,
which is used to run buildout.

If you install multiple Pythons,
the latter installations might not become active in the registry automatically,
and your Python wrapper still rely on the old version. This leads to
version incompatibilities and you are unable to start the Python applications.

Since only one Python interpreter can be active at a time,
it is tricky to develop multi-version Python code on Windows, 
for example if you need to develop Plone 3 sites
(Python 2.4) and Plone 4 sites (Python 2.6) simultaneously.

Below is a script (``regpy.py``) which changes the active Python interpreter.
The orignal author is unknown, I picked up this code from some paste board
long time ago. Just run this code with your Python and the running
interpreter becomes active.

Example::

    C:\Plone\python\python.exe regpy.py

Code::

    import sys

    from _winreg import *

    # tweak as necessary
    version = sys.version[:3]
    installpath = sys.prefix

    regpath = "SOFTWARE\\Python\\Pythoncore\\%s\\" % (version)
    installkey = "InstallPath"
    pythonkey = "PythonPath"
    pythonpath = "%s;%s\\Lib\\;%s\\DLLs\\" % (
        installpath, installpath, installpath
    )

    def RegisterPy():
        try:
            reg = OpenKey(HKEY_LOCAL_MACHINE, regpath)
        except EnvironmentError:
            try:
                reg = CreateKey(HKEY_LOCAL_MACHINE, regpath)
                SetValue(reg, installkey, REG_SZ, installpath)
                SetValue(reg, pythonkey, REG_SZ, pythonpath)
                CloseKey(reg)
            except:
                print "*** Unable to register!"
                return
            print "--- Python", version, "is now registered!"
            return
        if (QueryValue(reg, installkey) == installpath and
            QueryValue(reg, pythonkey) == pythonpath):
            CloseKey(reg)
            print "=== Python", version, "is already registered!"
            return
        CloseKey(reg)
        print "*** Unable to register!"
        print "*** You probably have another Python installation!"

    if __name__ == "__main__":
        RegisterPy()

Example error when going from Plone 3 to Plone 4::

    Traceback (most recent call last):

      File "C:\xxx\bin\idelauncher.py", line 99, in ?

        exec(data, globals())

      File "<string>", line 419, in ?

      File "c:\xxx\buildout-cache\eggs\plone.recipe.zope2instance-4.0.3-py2.6.egg\plone\recipe\zope2instance\__init__.py", line 27, in ?

        from plone.recipe.zope2instance import make

      File "c:\xxx\buildout-cache\eggs\plone.recipe.zope2instance-4.0.3-py2.6.egg\plone\recipe\zope2instance\make.py", line 5, in ?

        from hashlib import sha1

    ImportError: No module named hashlib

More info

* http://blog.mfabrik.com/2011/02/22/changing-the-active-python-interpreter-on-windows/

Running buildout behind a proxy
---------------------------------

Buildout uses ``setuptools``, which uses ``urllib``,
which allows you to set a
proxy using the ``http_proxy`` (lowercase!) environment variable.

Example for UNIX shell (bash):

.. code-block:: console

    # Set proxy address as environment variable.
    # In this case we use Polipo server running on the same computer.
    http_proxy=http://localhost:8123/

    # This is Bash shell specific command to export environment variable
    # to processes started from the shell
    export http_proxy

    # Run buildout normally
    bin/buildout

You can also SSH tunnel the proxy from a remote server:

.. code-block:: console

    # Make Polipo proxy yourserver.com:8123
    # made to be available at local port 8123
    # through SSH tunnel
    ssh -L 8123:localhost:8123 yourserver.com


*!!Attention!!*

  In Plone 4.3 the System changed , and from now on you get special users with different privileges for buildout and run. Because of the sudo command you proxy environment variables aren't saved in the sudo env list. 
There are 3 ways to fix this in \*nix systems: 

Inline: Set the environment variable inline. 
 1) ``sudo -u plone_buildout http_proxy="http://myproxy:1234" ./bin/buildout`` 

Copy the environment from the currently logged in user. 
 2) ``sudo -E -u plone_buildout ./bin/buildout`` 

Setup sudoers 
 3)Maybe this article is interesting for setting up sudoers: http://ubuntuforums.org/showthread.php?t=1132821 



Buildout cache folder
----------------------

If you are running several buildouts as the same user you should
consider setting the cache folder. All downloaded eggs are cached here.

There are two ways to set the cache folder

* Use the ``PYTHON_EGG_CACHE`` environment variable;

* or set the ``download-cache`` variable in ``[buildout]``. 
  This is only recommended if the ``buildout.cfg``
  file is not shared between different configurations.

Example:

.. code-block:: console

    # Create a cache directory
    mkdir ~/python-egg-cache

    # Set buildout cache directory for this shell session
    export PYTHON_EGG_CACHE=~/python-egg-cache

Bauildout defaults
=================

You can set user-wide buildout settings in the following file::

    $HOME/.buildout/default.cfg

This is especially useful if you are running many Plone development buildouts on your computer
and you want them to share the same buildout egg cache settings.

Example settings how to setting shared egg cache across various buildouts on your computer::

	[buildout]
	eggs-directory = /Users/mikko/code/buildout-cache/eggs
	download-cache = /Users/mikko/code/buildout-cache/downloads
	extends-cache = /Users/mikko/code/buildout-cache/extends
	 
.. warning ::

	If you are sharing egg cache you might run into egg versioning problems especially
	with older Plone installs. If you are having mysterious VersionConflict etc. problems
	try disable buildout defaults and run buildout cleanly without shared eggs.

Manually picking downloaded and active component versions
----------------------------------------------------------

This is also known as *pinning* versions.
You can manually choose what Python egg versions
of each component are used. This is often needed to resolve version conflict issues.

* http://www.uwosh.edu/ploneprojects/documentation/how-tos/how-to-use-buildout-to-pin-product-versions

Migrating buildout to a different Python interpreter
-----------------------------------------------------

You can either:

* copy the whole buildout folder to a new computer (not recommended); or

* changing the Python interpreter on the same computer.

First you need to clear existing eggs as they might contain binary compilations
for wrong Python version or CPU architecture:

.. code-block:: console

    rm -rf eggs/*

Also clear the ``src/`` folder if you are developing any binary eggs.

Buildout can be made aware of a new Python interpreter by rerunning
``bootstrap.py``:

.. code-block:: console

    source ~/code/python/python-2.4/bin/activate
    python bootstrap.py

Then run buildout again and it will fetch all Python eggs for the new Python interpreter:

.. code-block:: console

    bin/buildout

Setting up a Plone site from ``buildout.cfg`` and ``Data.fs``
--------------------------------------------------------------

This is often needed when you are copying or moving a Plone site.
If the repeatable deployment strategy is done correctly, all that is
needed to establish a Plone site is:

* ``buildout.cfg`` (which describes the Plone site and its add-on products
  and how they are downloaded or checked out from version control)

* ``Data.fs`` (and blobstorage directories) which contains the site
  database.

Below is an example process.

Activate Python 2.6 for Plone (see :doc:`how to use virtualenv controlled non-system wide Python </getstarted/python>`):

.. code-block:: console

    source ~/code/python/python-2.6/bin/activate

Install ZopeSkel templates which contains a buildout and folder structure
template for Plone site (``plone3_buildout``
works also for Plone 4 as long as you type in the correct version when
paster template engine asks for it):

.. code-block:: console

    easy_install ZopeSkel # creates paster command under virtual bin/ folder and downloads Plone/Zope templates
    paster create -t plone3_buildout


    paster create -t plone3_buildout newprojectfoldername
    ...
    Selected and implied templates:
      ZopeSkel#plone3_buildout  A buildout for Plone 3 installation
    ...

    Expert Mode? (What question mode would you like? (easy/expert/all)?) ['easy']:
    Plone Version (Plone version # to install) ['3.3.4']: 4.0
    Zope2 Install Path (Path to Zope2 installation; leave blank to fetch one!) ['']:
    Plone Products Directory (Path to Plone products; leave blank to fetch [Plone 3.0/3.1 only]) ['']:
    Initial Zope Username (Username for Zope root admin user) ['admin']: admin
    Initial User Password (Password for Zope root admin user) ['']: admin
    HTTP Port (Port that Zope will use for serving HTTP) ['8080']:
    Debug Mode (Should debug mode be "on" or "off"?) ['off']: on
    Verbose Security? (Should verbose security be "on" or "off"?) ['off']: on

Then you can copy ``buildout.cfg`` from the existing site to your new
project:

.. code-block:: console

    copy buildout.cfg newproject # Copy the existing site configuration file to new project
    cd newproject
    python bootstrap.py # Creates bin/buildout command for buildout
    bin/buildout # Run buildout - will download and install necessary add-ons to run Plone site

Assuming buildout completes succesfully, test that the site starts (without
database):

.. code-block:: console

    bin/instance fg # Start Zope in foreground debug mode

Press CTRL+C to stop the instance.

Now copy the existing database to the buildout directory:

.. code-block:: console

    cp Data.fs var/filestorage/Data.fs # There should be existing Data.fs file here, created by site test launch

If you do not know the admin user account for the database,
you can create an additional admin user:

.. code-block:: console

    bin/instance adduser admin2 admin # create user admin2 with password admin

Look for the Zope start-up message, which mentions the port the instance is
running on (the default port is 8080)::

    2010-09-06 12:55:17 INFO ZServer HTTP server started at Mon Sep  6 12:55:17 2010
    Hostname: 0.0.0.0
    Port: 20001

Then log in to the Zope Management Interface using your browser::

    http://localhost:8080

.. _configuring-products-from-buildout:

Configuring plone products from buildout
----------------------------------------

In case add-on products require configuration which is not 
handled by buildout recipes, you can supply this configuration using the
``zope-conf-additional`` specification of the ``plone.recipe.zope2instance``
recipe:

.. code-block:: cfg

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    zope-conf-additional =
    <product-config foobar>
        spam eggs
    </product-config>

These configuration sections are added directly to your ``zope.conf`` file.

Any named product-config section is then available as a simple dictionary to any python product that cares to look for it.
The above example creates a ``foobar`` entry which is a dict with a 
``'spam': 'eggs'`` mapping.

Here is how you then access that from your code::

    from App.config import getConfiguration

    config = getConfiguration()
    configuration = config.product_config.get('foobar', dict())
    spamvalue = configuration.get('spam')

A similar method is used to configure the built-in Zope ClockServer enabling
you to trigger scripts:

.. code-block:: cfg

    zope-conf-additional =
        <clock-server>
            method /mysite/do_stuff
            period 60
            user admin
            password secret
            host www.mysite.com
        </clock-server>


Setting ``LD_LIBRARY_PATH``
----------------------------

``LD_LIBRARY_PATH`` is a UNIX environment variable which specifies 
from which folders to load native dynamic linked libraries (``.so`` files).
You might want to override your system-wide libraries, 
because operating systems may ship with old, incompatible, versions.

You can use ``environment-vars`` of the
`zope2instance <http://pypi.python.org/pypi/plone.recipe.zope2instance>`_ recipe.

Example in ``buildout.cfg``

.. code-block:: cfg

    [instance]
    # Use statically compiled libxml2
    environment-vars =
        LD_LIBRARY_PATH ${buildout:directory}/parts/lxml/libxml2/lib:${buildout:directory}/parts/lxml/libxslt/lib


Extending buildout section
-------------------------------

Buildout extensions can be extended in another buildout file.

* http://pypi.python.org/pypi/zc.buildout#extending-sections-macros


Overriding parts variables from command line
--------------------------------------------

Sometimes, you need a variable from one of your buildout parts to be different, but for just one run.

So, instead of modifying your .cfg file for just one run and remember to revert it back before pushing your changes back to the server, you can just do that from the command line.

The format is::

        ./bin/builodut partname:some_variable=new_value

Examples
=========

Need to create your site from scratch using the plonesite recipe::

	./bin/buildout plonesite:site-replace=true

Want to re-run buildout, but you don't want to mr.developer to update packages::

	./bin/buildout buildout:always-checkout=false

Want to do both examples at the same time::

	./bin/buildout plonesite:site-replace=true buildout:always-checkout=false


Troubleshooting
----------------

See :doc:`Buildout troubleshooting </troubleshooting/buildout>` chapter.

