========================
Buildout troubleshooting
========================

.. admonition:: Description

    How to solve problems related to running buildout and some common    exceptions you might encounter when running buildout for Plone.

Introduction
============

This document tells how to resolve buildout problems.

Network errors and timeouts
===========================

The usual reason for download error or timeout is that either

* ``pypi.python.org`` server is down, or
* one of ``plone.org`` servers is down, or
* other Python package source server is down.

Here are instructions how to deal with community servers down situations

* http://jacobian.org/writing/when-pypi-goes-down/

Mirrors

* http://www.pypi-mirrors.org/


Individual package failing outside PyPI
---------------------------------------

To figure out which file buildout tries to download, usually the only way is to use ``buildout -D`` pdb debug mode and step up in stack frames to see what is going on.


parts/instance/etc/zope.conf: [Errno 2] No such file or directory
===================================================================


You see this error when trying to start Plone.
This means that buildout did not complete correctly and did not generate configuration files.

Rerun buildout and fix errors in ``buildout.cfg`` based on buildout command output.

Buildout and SyntaxErrors
=========================

You may see ``SyntaxError`` exceptions when running buildout::

    SyntaxError: ("'return' outside function", ('/usr/local/Plone/buildout-cache/eggs/tmpzTKrEI/Products.ATExtensions-1.1a3-py2.6.egg/Products/ATExtensions/skins/at_extensions/getDisplayView.py', 11, None, 'return value\n'))

They are harmless.

The reason: Buildout uses a Python tool called ``setuptools`` internally to install the packages.
Setuptools scans all ``.py`` files inside the Python package and assumes they are Python modules.
However, Plone has something called :doc:`RestrictedPython </develop/plone/security/sandboxing>`.
RestrictedPython allows untrusted users to execute Python code in Plone (Python Scripts in the Management Interface).
RestrictedPython scripts use slightly modified Python syntax compared to plain Python modules.

Setuptools does not know which files are normal ``.py`` and which files are RestrictedPython and tries to interpret them all using standard Python
syntax rules.
Then it fails.
However, setuptools only tries to scan files (`in order to see if they are zip-safe <https://pythonhosted.org/setuptools/easy_install.html#compressed-installation>`__) but still installs them correctly.
No harm done.


Version conflicts
=================

Buildout gives you an error if there is a dependency shared by two components, and one of the components wants to have a different version of this dependency.

Example::

      Installing.
      Getting section zeoserver.
      Initializing part zeoserver.
    Error: There is a version conflict.
    We already have: zope.component 3.8.0
    but five.localsitemanager 1.1 requires 'zope.component<3.6dev'.

If your buildout is fetching strange versions:

* try running buildout in verbose mode: ``bin/buildout -vvv``
* Use ``show-picked-versions`` (see below)
* Manually pin down version in the ``[versions]`` section of your buildout.

Further reading:

* http://maurits.vanrees.org/weblog/archive/2010/08/fake-version-pinning

* http://www.uwosh.edu/ploneprojects/documentation/how-tos/how-to-use-buildout-to-pin-product-versions

Show picked versions
--------------------

In order to show which versions were picked by buildout -
or in other words, versions were not pinned anywhere -
use this feature.

Buildout will show automatically picked Python egg versions at the end of the output.
The output may be copy pasted in your versions section.

Add to your ``buildout.cfg``:

.. code-block:: cfg

    [buildout]
    show-picked-versions = true


Extracting version numbers from instance script
=================================================

Example::

    cat bin/instance | \
        grep eggs | \
        sed -r 's#.*eggs/(.*)-py2.[0-9].*#\1#g' | \
        sed -r 's#-# = #g' | \
        sed -r 's#_#-#g' | \
        grep -E ' = [0-9\.]' | \
        xargs -0 echo -e "[versions]\n" | \
        sed -r 's#^\s+##g' > versions-extracted.cfg; cat versions-extracted.cfg

More info

* http://davidjb.com/blog/2011/06/extracting-a-buildout-versions-cfg-from-a-zope-instance-script/

Plone 3.1
=========

Plone 3.1 and earlier are not eggified.
Below are links how to keep Plone 3.1 and earlier buildouts running.

See:

* http://www.netsight.co.uk/blog/resurrecting-old-plone-3-buildouts





Getting distribution for ``distribute``
========================================

You try to run buildout, but it is stuck in a loop::

    Getting distribution for 'distribute'.
    Getting distribution for 'distribute'.
    ....
    Getting distribution for 'distribute'.
    Getting distribution for 'distribute'.
    Getting distribution for 'distribute'.

Your system-wide Distribute version is older than the latest release.
Buildout tries to update it, but since system wide site-packages version
overrides anything buildout can do, it is stuck in a loop.

Fix: update Distribute in system-wide Python::

    easy_install -U Distribute
    Searching for Distribute
    Reading https://pypi.python.org/simple/Distribute/
    Reading http://packages.python.org/distribute
    Best match: distribute 0.6.12
    Downloading https://pypi.python.org/packages/source/d/distribute/distribute-0.6.12.tar.gz#md5=5a52e961f8d8799d243fe8220f9d760e
    Processing distribute-0.6.12.tar.gz
    Running distribute-0.6.12/setup.py -q bdist_egg --dist-dir /tmp/easy_install-jlL3e7/distribute-0.6.12/egg-dist-tmp-IV9SiQ
    Before install bootstrap.
    Scanning installed packages
    Setuptools installation detected at /home/moo/py24/lib/python2.4/site-packages
    Non-egg installation
    Removing elements out of the way...
    Already patched.
    /home/moo/py24/lib/python2.4/site-packages/setuptools-0.6c11-py2.4.egg-info already patched.
    After install bootstrap.
    /home/moo/py24/lib/python2.4/site-packages/setuptools-0.6c11-py2.4.egg-info already exists
    Removing distribute 0.6.10 from easy-install.pth file
    Adding distribute 0.6.12 to easy-install.pth file
    Installing easy_install script to /home/moo/py24/bin
    Installing easy_install-2.4 script to /home/moo/py24/bin


UnknownExtra: zope.i18n 0.0 has no such extra feature 'zcml'
============================================================

You get the following traceback when running buildout::

      File "/home/moo/rtv/eggs/plone.recipe.zope2instance-2.7-py2.4.egg/plone/recipe/zope2instance/__init__.py", line 93, in update
        requirements, ws = self.egg.working_set()
      File "/home/moo/rtv/eggs/zc.recipe.egg-1.1.0-py2.4.egg/zc/recipe/egg/egg.py", line 93, in working_set
        allow_hosts=self.allow_hosts,
      File "/tmp/tmpGFbvPP/zc.buildout-1.5.0b2-py2.4.egg/zc/buildout/easy_install.py", line 800, in install
      File "/tmp/tmpGFbvPP/zc.buildout-1.5.0b2-py2.4.egg/zc/buildout/easy_install.py", line 660, in install
      File "/home/moo/py24/lib/python2.4/site-packages/distribute-0.6.10-py2.4.egg/pkg_resources.py", line 551, in resolve
        requirements.extend(dist.requires(req.extras)[::-1])
      File "/home/moo/py24/lib/python2.4/site-packages/distribute-0.6.10-py2.4.egg/pkg_resources.py", line 2164, in requires
        raise UnknownExtra(
    UnknownExtra: zope.i18n 0.0 has no such extra feature 'zcml'

You might be using an add-on meant for Plone 4 with Plone 3. Check if
``setup.py`` contains *Zope2* as a dependency. If it does, then you need to
use earlier version of the add-on for your Plone 3 site.

More info:

* http://groups.google.com/group/singing-dancing/browse_thread/thread/331cdfe78cf371ed


We already have: zope.interface 4.0.3
========================================

Example::

    Getting distribution for 'zope.testing==3.9.7'.
    warning: no files found matching 'sampletests' under directory 'src'
    Got zope.testing 3.9.7.
    While:
      Installing.
      Getting section test.
      Initializing section test.
      Installing recipe zc.recipe.testrunner.
    Error: There is a version conflict.
    We already have: zope.interface 4.0.3

Your system Python or virtualenv'd Python already has ``zope.interface`` library installed.
A lot of Python software uses this library.
However, the system version is wrong and cannot be overridden.

Solutions.

For virtualenv: ``rm -rf ~/code/plone-venv/lib/python2.7/site-packages/zope.interface-4.0.3-py2.7-macosx-10.8-x86_64.egg``

For system Python: You need to create a virtualenv'd Python and to use it to drive buildout, so that there is no conflict with ``zope.interface`` versions.

We already have: zope.location 3.4.0
====================================

When running buildout, Plone 3.3.5::

    While:
      Installing.
      Getting section zopepy.
      Initializing section zopepy.
      Getting option zopepy:eggs.
      Getting section client1.
      Initializing section client1.
      Getting option client1:zeo-address.
      Getting section zeo.
      Initializing part zeo.
    Error: There is a version conflict.
    We already have: zope.location 3.4.0
    but zope.traversing 3.13 requires 'zope.location>=3.7.0'.

Solution:

.. code-block:: console

    rm -rf fake-eggs/*
    bin/buildout install zope2
    bin/buildout


ImportError: No module named lxml
=================================

``lxml`` as a PyPi package dependency fails even though it is clearly
installed.

Example traceback when running buildout::

    ...
    Processing openxmllib-1.0.6.tar.gz
    <snip Unpacking... >
    Running openxmllib-1.0.6/setup.py bdist_egg --dist-dir /tmp/easy_install-Urh6x4/openxmllib-1.0.6/egg-dist-tmp-ju0TuT
    Traceback (most recent call last):
    <snip Traceback... >
      File "setup.py", line 5, in <module>
      File "/tmp/easy_install-Urh6x4/openxmllib-1.0.6/openxmllib/__init__.py", line 17, in <module>
      File "/tmp/easy_install-Urh6x4/openxmllib-1.0.6/openxmllib/wordprocessing.py", line 5, in <module>
      File "/tmp/easy_install-Urh6x4/openxmllib-1.0.6/openxmllib/document.py", line 14, in <module>
    ImportError: No module named lxml
    An error occurred when trying to install openxmllib 1.0.6. Look above this message for any errors that were output by easy_install.
    While:
      Installing plone-core-addons.
      Getting distribution for 'openxmllib>=1.0.6'.
    Error: Couldn't install: openxmllib 1.0.6

Solution: ensure lxml compilation happens before openxmllib is being compiled.

For instance, if you are installing something like ``Products.OpenXml``, you will have likely included this egg under your Plone ``[instance]`` section of your buildout.
You should consider using something like ``collective.recipe.staticlxml`` to build lxml and to do this *before* this egg's installation is invoked.
Like so in your ``buildout.cfg``:

.. code-block:: cfg

    [buildout]
    parts =
        lxml
        ...
        instance
    ...

    [lxml]
    recipe = z3c.recipe.staticlxml
    egg = lxml

More information:

* http://www.niteoweb.com/blog/order-of-parts-when-compiling-lxml

* http://plone.293351.n2.nabble.com/lxml-installs-but-Products-OpenXml-openxmllib-can-t-see-it-tp5565184p5565184.html


Can't run ``bootstrap.py`` - VersionConflict for ``zc.buildout``
================================================================

Traceback when running ``python bootstrap.py``::

    Traceback (most recent call last):
      File "/Users/moo/code/collective.buildout.python/parts/opt/lib/python2.6/pdb.py", line 1283, in main
        pdb._runscript(mainpyfile)
      File "/Users/moo/code/collective.buildout.python/parts/opt/lib/python2.6/pdb.py", line 1202, in _runscript
        self.run(statement)
      File "/Users/moo/code/collective.buildout.python/parts/opt/lib/python2.6/bdb.py", line 368, in run
        exec cmd in globals, locals
      File "<string>", line 1, in <module>
      File "bootstrap.py", line 256, in <module>
        ws.require(requirement)
      File "/Users/moo/code/collective.buildout.python/python-2.6/lib/python2.6/site-packages/distribute-0.6.8-py2.6.egg/pkg_resources.py", line 633, in require
        needed = self.resolve(parse_requirements(requirements))
      File "/Users/moo/code/collective.buildout.python/python-2.6/lib/python2.6/site-packages/distribute-0.6.8-py2.6.egg/pkg_resources.py", line 535, in resolve
        raise VersionConflict(dist,req) # XXX put more info here
    VersionConflict: (zc.buildout 1.5.0b2 (/Users/moo/code/collective.buildout.python/python-2.6/lib/python2.6/site-packages/zc.buildout-1.5.0b2-py2.6.egg), Requirement.parse('zc.buildout==1.5.2'))

Solution: update the ``zc.buildout`` installed in your system Python:

.. code-block:: console

    easy_install -U zc.buildout

An error occurred when trying to install lxml - error: Setup script exited with error: command 'gcc' failed with exit status 1
==============================================================================================================================

Traceback when running buildout::

    ...
    src/lxml/lxml.etree.c:143652: error: ‘__pyx_v_4lxml_5etree_XSLT_DOC_DEFAULT_LOADER’ undeclared (first use in this function)
    src/lxml/lxml.etree.c:143652: error: ‘xsltDocDefaultLoader’ undeclared (first use in this function)
    src/lxml/lxml.etree.c:143661: error: ‘__pyx_f_4lxml_5etree__xslt_doc_loader’ undeclared (first use in this function)
    error: Setup script exited with error: command 'gcc' failed with exit status 1
    An error occurred when trying to install lxml 2.2.8. Look above this message for any errors that were output by easy_install.
    While:
      Installing instance.
      Getting distribution for 'lxml==2.2.8'.
    Error: Couldn't install: lxml 2.2.8

Solution: install the ``libxml`` and ``libxslt`` development headers.

On Ubuntu/Debian you could do this as follows:

.. code-block:: console

    sudo apt-get install libxml2-dev libxslt-dev


VersionConflict: distribute 0.6.19
==================================

When running buildout you see something like this::

      File "/home/danieltordable.es/buildout-cache/eggs/zc.buildout-1.4.4-py2.6.egg/zc/buildout/easy_install.py", line 606, in _maybe_add_setuptools
        if ws.find(requirement) is None:
      File "/home/danieltordable.es/buildout-cache/eggs/distribute-0.6.19-py2.6.egg/pkg_resources.py", line 474, in find
        raise VersionConflict(dist,req)     # XXX add more info
    VersionConflict: (distribute 0.6.19 (/home/danieltordable.es/buildout-cache/eggs/distribute-0.6.19-py2.6.egg), Requirement.parse('distribute==0.6.15'))

Buildout uses the system-wide Distribute installation (``python-distribute``
or similar package, depends on your OS).  To fix this, you need to update
system-wide distribution.

.. note:: It is preferred to do your Python + buildout
   installation in a :term:`virtualenv`, in order not to break your OS

Update Distribute (Plone universal installer, using supplied
``easy_install`` script):

.. code-block:: console

        python/bin/easy_install -U Distribute

Update Distribute (OSX/Ubuntu/Linux):

.. code-block:: console

        easy_install -U Distribute


argparse 1.2.1
==============

If you get::

    While:
      Installing.
      Loading extensions.
    Error: There is a version conflict.
    We already have: argparse 1.2.1

Rerun ``bootstrap.py`` with the correct Python interpreter.


Error: Picked: <some.package> = <some.version>
==============================================

If you get something like this::

    We have the distribution that satisfies 'zc.recipe.testrunner==1.2.1'.
    Installing 'collective.recipe.backup'.
    Picked: collective.recipe.backup = 2.4
    Could't load zc.buildout entry point default
    from collective.recipe.backup:
    Picked: collective.recipe.backup = 2.4.
    While:
      Installing.
      Getting section backup.
      Initializing section backup.
      Installing recipe collective.recipe.backup.
      Getting distribution for 'collective.recipe.backup'.
    Error: Picked: collective.recipe.backup = 2.4

This means that your buildout has "allow picked versions" set to false.
You need to pin the version for the picked version (or turn on "allow picked versions").

Buildout error: Not a recognized archive type
=================================================

If you run across an error like this when running buildout::

    ...
    Installing instance.
    Getting distribution for 'collective.spaces'.
    error: Not a recognized archive type: /home/plone/.buildout/downloads/dist/collective.spaces-1.0.zip

the error is likely stemming from an incorrect download of this egg.
Check the given file to ensure that the file is correct (for instance, it is a non-zero length file or verifying the content using something like ``md5sum``) before delving deep into your Python install's workings.
This error makes it look as if your Python install doesn't have support for this type of archive, but in fact it can be caused by a corrupt download.


Distribute / setuptools tries to mess with system Python and Permission denied
==============================================================================

When running ``bootstrap.py`` your buildout files
because it tries to write to system-wide Python installation.

Example::

    Getting distribution for 'distribute==0.6.24'.
    Before install bootstrap.
    Scanning installed packages
    No setuptools distribution found
    warning: no files found matching 'Makefile' under directory 'docs'
    warning: no files found matching 'indexsidebar.html' under directory 'docs'
    After install bootstrap.
    Creating /srv/plone/python/python-2.7/lib/python2.7/site-packages/setuptools-0.6c11-py2.7.egg-info
    error: /srv/plone/python/python-2.7/lib/python2.7/site-packages/setuptools-0.6c11-py2.7.egg-info: Permission denied
    An error occurred when trying to install distribute 0.6.24. Look above this message for any errors that were output by easy_install.
    While:
      Bootstrapping.
      Getting distribution for 'distribute==0.6.24'.
    Error: Couldn't install: distribute 0.6.24

Solution:

`This bug has been fixed in Distribute 0.6.27 <https://pypi.python.org/pypi/distribute/0.6.27#id2>`_ - make sure your system-wide Python
uses this version or above::

       sudo /srv/plone/python/python-2.7/bin/easy_install -U Distribute



UnboundLocalError: local variable 'clients' referenced before assignment
==========================================================================

Example traceback when running buildout::

    Traceback (most recent call last):
      File "/srv/plone/x/eggs/zc.buildout-1.4.4-py2.7.egg/zc/buildout/buildout.py", line 1683, in main
        getattr(buildout, command)(args)
      File "/srv/plone/x/eggs/zc.buildout-1.4.4-py2.7.egg/zc/buildout/buildout.py", line 555, in install
        installed_files = self[part]._call(recipe.install)
      File "/srv/plone/x/eggs/zc.buildout-1.4.4-py2.7.egg/zc/buildout/buildout.py", line 1227, in _call
        return f()
      File "/srv/plone/x/eggs/plone.recipe.unifiedinstaller-4.3.1-py2.7.egg/plone/recipe/unifiedinstaller/__init__.py", line 65, in install
        for part in clients
    UnboundLocalError: local variable 'clients' referenced before assignment

Solution: Your buildout contains leftovers from the past. Remove ``clients`` variable in ``[unifiedinstaller]`` section.



error: None
============

This means .tar.gz is corrupted::

    error: None
    An error occurred when trying to install lxml 2.3.6. Look above this message for any errors that were output by easy_install.
    While:
      Installing instance.
      Getting distribution for 'lxml==2.3.6'.
    Error: Couldn't install: lxml 2.3.6

Buildout download cache is corrupted. Run ``bin/buildout -vvv`` for more info. Then do something like this::

      # Corrupted .tar.gz download
      rm /Users/mikko/code/buildout-cache/downloads/dist/lxml-2.3.6.tar.gz


Mac OS X Error: Couldn't install: lxml 3.4.4
============================================

If you got the error ``Couldn't install: lxml 3.4.4`` while using the Plone 5.0 unified installer on Mac OS X 10.11.1 El Capitan, you should `update your Xcode command line tools <http://stackoverflow.com/questions/19548011/cannot-install-lxml-on-mac-os-x-10-9>`_::

    xcode-select --install

then re-run ``bin/buildout``.
