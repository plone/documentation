.. -*- coding: utf-8 -*-

===============
Troubleshooting
===============

Buildout Issues
===============

Buildout can be frustrating for those unfamiliar with parsing through autistic robot language.

These errors are almost always a quick fix and a little bit of understanding goes a long ways.

Errors Running bootstrap.py
---------------------------
You may not even get to running buildout and then you will already have an error.
Let's take this one for example::

    ...
     File "/usr/local/lib/python2.6/site-packages/distribute-0.6.13-py2.6.egg/pkg_resources.py", line 556, in resolve
        raise VersionConflict(dist,req) # XXX put more info here
     pkg_resources.VersionConflict: (zc.buildout 1.5.1 (/usr/local/lib/python2.6/site-packages/zc.buildout-1.5.1-py2.6.egg), Requirement.parse('zc.buildout==1.5.2'))


Buildout has simply noticed that the version of buildout required by the bootstrap.py file you are trying to run
does not match the version of buildout in your python library.

In the error above, your system has buildout 1.5.1 installed and the bootstrap.py file wants to run with 1.5.2.

To fix, you have a couple options.

First, you can force buildout to run with the version you already have installed by invoking the version tag.

This tells your [Plone] bootstrap.py file to play nicely with the version that you already have installed.

In the case of the error pasted above, that would be::

   > python bootstrap.py --version=1.5.1

I personally know that versions 1.4.4, 1.5.1, and 1.5.2 all work this way.

The other option is to delete your current egg and force the upgrade.
In the case of the error above, all you need to do is delete the egg the system currently has. eg::

  > rm -rf /usr/local/lib/python2.6/site-packages/zc.buildout-1.5.1-py2.6.egg

When you rerun bootstrap, it will look for the buildout of the egg, note that there isn't one,
and then go fetch a new egg in the version that it wants for you.

Do one of those and re-run bootstrap.

One other thing of note is that running bootstrap effectively ties that python executable and all of its libraries to your buildout.
If you have several python installs and want to switch which python is tied to your buildout,
simply rerun bootstrap.py with the new python (and then rerun buildout).
You may get the same error above again but now that you know how to fix it,
you can spend that time drinking beer instead of smashing your keyboard.

Hooray!

When Mr. Developer is Unhappy
-----------------------------
``mr.developer`` is never unhappy, except when it is.
Although this technically isn't a buildout issue, it happens when running buildout so I'm putting it under buildout issues.

When working with the dev instance, especially with all the moving back and forth between GitHub and svn,
you may have an old copy of a src package.

The error looks like::

    mr.developer: Can't update package 'Products.CMFPlone' because its URL doesn't match.


As long as you don't have any pending commits, you just need to remove the package from :file:`src/` and
it will recheck it out for you when it updates.

You can also get such fun errors as::

    Link to http://sphinx.pocoo.org/ ***BLOCKED*** by --allow-hosts


These are ok to ignore IF and ONLY IF the lines following it say::

    Getting distribution for 'Sphinx==1.0.7'.
    Got Sphinx 1.0.7.


If buildout ends with warning you that some packages could not be downloaded, then chances are that package wasn't downloaded.
This is bad and could cause all sorts of whack out errors when you start or try to run things because it never actually downloaded the package.

There are two ways to get this error to go away. The first is to delete all instances of host filtering.
Go through all the files and delete any lines which say ``allow-hosts =`` and ``allow-hosts +=``.
In theory, by restricting which hosts you download from, buildout will go faster.

The point is that they are safely deletable.

The second option is to allow the host that it is pointing to by adding something like this to your .cfg::

    allow-hosts += sphinx.pocoo.org

Again, this is only necessary if the package wasn't found in the end.


mr.developer Path Errors
------------------------
``ERROR: You are not in a path which has mr.developer installed (:file:`.mr.developer.cfg` not found).``

When running any :command:`./bin/develop` command.

To fix, do::

  ln -s plips/.mr.developer.cfg



Other Random Issues
===================
.. TODO: These need to be revalidated

Dirty Packages
--------------

"ERROR: Can't update package '[Some package]', because it's dirty."

Fix
^^^
``mr.developer`` is complaining because a file has been changed/added, but not committed.

Use :command:`bin/develop update --force`.
Adding ``*.pyc *~.nib *.egg-info .installed.cfg *.pt.py *.cpt.py *.zpt.py *.html.py *.egg`` to your subversion config's global-ignores has been suggested as a more permanent solution.

No module named zope 2
----------------------
``ImportError: No module named Zope2" when building using a PLIP cfg file.``

Appears to not actually be the case.
Delete :file:`mkzopeinstance.py` from :file:`bin/` and rerun buildout to correct this if you're finding it irksome.

Can't open file '/Startup/run.py'
---------------------------------

Two possible fixes, you are using Python 2.4 by mistake, use 2.6 instead.
Or, you may need to make sure you run :command:`bin/buildout …` after :command:`bin/develop …`.
Try removing :file:`parts/*`, :file:`bin/*`, :file:`.installed.cfg`, then re-bootstrap and re-run buildout, develop, buildout.

Missing PIL
-----------
:file:`pil.cfg` is include within this buildout to aid in PIL installation.
Run :command:`bin/buildout -c pil.cfg` to install.
This method does not work on Windows, we're unable to run it by default.


Modified Egg Issues
-------------------
:command:`bin/develop status` is showing that the ``Products.CMFActionIcons`` egg has been modified,
but I haven't touched it.
And this is preventing bin/develop up from updating all the eggs.

Fix
^^^
Edit :file:`~/.subversion/config` and add eggtest*.egg to the list of global-ignores

