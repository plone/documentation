============================================
Upgrading Non-Buildout-based Plone Instances
============================================

.. admonition:: Description

   How to upgrade versions of Plone that predate the use of buildout-based installers.

**This document applies only to older Plone installations that do not use buildout.  Generally, this means Plone 1 - Plone 3.x, although some custom installations of Plone 3 can be buildout-based.  If you are using Plone 4, please see ":doc:`General procedure for Plone 4.x minor version upgrades with buildout. </manage/upgrading/plone4_minor_upgrade.rst>`"**

When upgrading to a newer release of Plone, it is important to run the content migration procedure, since internal structures in Plone might have changed since the last version. This is the general procedure for upgrading.

Before you start upgrading anything, make sure you have a backup.
=================================================================

The basic manual procedure is detailed below. If you are using the installers, you can skip the part about moving away directories and replacing them with the new ones (step 3-4) - it should be handled by the installer for you.

#. Back up your entire Plone directory. If you're using WebDAV, make sure all objects are unlocked in Control Panel → WebDAV Lock Manager.
#. Shut down your Plone server instance.
#. Remove the Product directories you want to replace (ie. the ones in the package you downloaded).
#. Put in the new Product directories.
#. Start Plone again - your site may be inaccessible until we have performed the next steps - don't panic :)
#. Go to http://yoursite/manage (aka. the ZMI) and click portal_migrations
#. Make sure you are on the Upgrade tab (in older versions, this tab is called Migrate) — it will state something like::

         Instance version: 2.5.3
         File system version: 3.1.1

#. This means that you have to run the upgrade procedure to be updated to 3.1.1.
#. Click the Upgrade button.
   If you want to see what steps the upgrade would go through without making the actual changes, you can check the Dry Run option - this will do the exact same steps as a normal upgrade/migration will do, but not write anything to the database.
#. The site will now be updated, this may take a while, depending on which versions you upgrade from/to. For example, the upgrade from Plone 2.0 to Plone 2.1 involves conversion and re-cataloging of all content in your site, so if you have a big site, this may take a while. Be patient.

For those of you who wonder why we don't do this automatically, the reason is that we don't want to modify your data, and you should have the opportunity to back up the data before doing the upgrade.

**For advanced/enterprise users:** It is normally possible to upgrade in-place (at least between minor versions) without any site downtime if you run ZEO and multiple load-balanced instances. See the ZEO documentation for more information if you need this.

