=========================================================
Upgrading from 3.2 to 3.3.x
=========================================================


.. admonition:: Description

   Steps for minor upgrades from Plone 3.2 to Plone 3.3.x.

.. contents:: :local:


**For most situations, this upgrade will be an easy one.**

Upgrading from 3.2 to 3.3 is quick and easy. If you're upgrading from an earlier version, you should carefully read the upgrade instructions for the intervening versions. **If you are upgrading to buildout for the first time,** be sure to read :doc:`General advice on updating from a non-buildout to buildout-based installation. </manage/upgrading/non_buildout_to_buildout_upgrade>`


Upgrade Steps
================

**Back up your entire installation.** Stop the Zope/Plone process.

**Edit your buildout.cfg** file to use the 3.3 versions.cfg file::

    extends = http://dist.plone.org/release/3.3.5/versions.cfg

* check http://plone.org/products/plone to see whether a more recent release is advised
* we have at least 3.3.5.

If you're using a buildout.cfg that reads versions.cfg from a file instead of a URL, you'll need to add this line and comment out the existing extends = versions.cfg line. Alternatively, you may download a new versions.cfg file from the URL above and point to that instead - if you prefer having the setup locally.

Make sure your *[zope2]* section (or equivalent using *plone.recipe.zope2install*) is pointing to the Zope version indicated in the previous *versions.cfg*::

    [zope2]
    recipe = plone.recipe.zope2install
    url = ${versions:zope2-url}

**Run buildout** to download the updated packages and rebuild your startup commands. Change to the directory containing buildout.cfg and run::

    bin/buildout

Windows users will use a backslash in place of the slash.

**Restart Plone.**

In the Zope Management Interface, **visit portal_migration and use the upgrade button** to update your database.