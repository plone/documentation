=============================================================================
General advice on updating from a non-buildout to buildout-based installation
=============================================================================

.. admonition:: Description

   Some hints for those stepping onto the buildout bandwagon.

Beginning with Plone 3.2, we're no longer distributing Plone in the traditional tarballs (archive files) of Zope products. Instead, Plone is distributed as a set of Python Packages. These packages bear information about dependencies, and they generally provide us with a much better way of managing a complex web of Python, Zope and Plone components.

Buildout, a sophisticated configuration management system from the creator of Zope, is now the recommended way for managing Plone installations. This poses a one-time challenge for folks upgrading from old to new-style installs. It should, though, make future updates much easier.

The :doc:`Managing projects with Buildout </old-reference-manuals/buildout/index>` tutorial provides a great introduction to buildout and its use. Here, we'll just offer a few hints on making your move to buildout as painless as possible.

#. Give up any idea of doing an in-place update. Many of us got into the habit with earlier versions of Plone of simply unpacking the tarball for a new version into the "Products" directory of the old install. That was never a good idea for a major version update, and it's just not feasible while trying to switch to buildout. The internal layout of the files has just changed too much. Changing to buildout will make it much easier, though, to upgrade in place in the future.
#. Install a new, buildout-based Plone version to a different place than your old installation. Different path, different drive, different server, different hosting facility — whichever you need.
#. Use a current Plone installer if available (all installers for 3.2+ are buildout-based):

   * If you're using Linux/FreeBSD/\*nix, please strongly consider using the Unified Installer. If you didn't like something about the way it worked for 2.x, please take a look again. It's a lot more versatile. It includes options to change target directory, do ZEO or stand-alone installs, and to use an already installed Python.
   * If you're using Darwin on a production server, it's a good idea to install the XCode tools and use the Unified Installer. You'll want the versatility.
   * If you're using OS X on a workstation, it's fine to use the OS X installer, which is meant to be convenient.
   * If you're on Windows, use the Windows installer or prepare to learn a lot.

#. If you don't want to use an installer, that's OK, but protect your system Python. Learn to use `virtualenv <http://pypi.python.org/pypi/virtualenv>`_, which will allow you to create isolated Python sandboxes. Install virtualenv first, create a sandbox, then use easy_install in the sandbox to install ZopeSkel. Follow the buildout tutorial's instructions for creating your buildout.
#. Fire up your new installation and make sure it's working. Try it out with an empty database. If you're using it on the same server, you should adjust the ports first to make sure you're not trying to use the same TCP/IP ports. This is a common error. Look for the "http-address" address in your buildout.cfg file. If you've used the Unified or OS X installers, it's even easier as the ports settings are in the top of the file.
#. Evaluate your add-on product list. Enumerate all the add-on Zope and Plone products installed on your own server. Divide the list into those that have egg (Python Package) updates available and those that don't.
#. Copy the add-on products that don't have egg versions from the "Products" directory of the old install into the "products" directory (note the small "p") of your new install. Check ownership and permissions of the copied files (failure to do this is another common error).
#. Add the names of new, egg-based products to the "[eggs]" section of your buildout.cfg. Check the install instructions to see if they also need a ZCML slug specification. Re-run buildout to fetch and install the new eggs.
#. Start your new install in foreground mode (bin/plonectl fg or bin/instance fg) to watch product loading and discover errors. Fix product problems until you have a clean start.
#. Copy the Data.fs file from your old install's var directory to the new one's var/filestorage directory. Check ownership and permissions!
#. Do the foreground start dance again. Solve problems.
#. Go live.

A word on warnings
==================

Whenever you run buildout and load new packages that have skin layers, you're likely to receive warnings indicating "'return' outside function." Ignore them, they're harmless. The warnings are produced when Python attempts to compile skin-layer Python scripts, which do indeed contain 'return' outside of function, but run in a context in which this is OK.
