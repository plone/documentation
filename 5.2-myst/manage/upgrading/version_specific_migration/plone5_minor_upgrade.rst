=====================================
Upgrading Plone 5 Within 5.x.x Series
=====================================

.. admonition:: Description

   Steps for minor upgrades within the Plone 5 Major Release.



.. warning::

   Before performing any Plone upgrade, you should always have a complete backup of your site.
   See the :doc:`Preparations </manage/upgrading/preparations>` section of this manual for more details.

   In addition, you should check the :doc:`Version-specific migration tips </manage/upgrading/version_specific_migration/index>`
   section of this manual for any notes that may apply to the specific version upgrade you're about to perform.

Buildout
========

Out of the box, Plone's Unified Installer includes a ``buildout.cfg`` (typically located at your-plone-directory/zinstance/buildout.cfg) file that contains the following parameter.

.. code-block:: shell

    extends =
    base.cfg
    versions.cfg
    # http://dist.plone.org/release/5.1-latest/versions.cfg

This tells buildout to get all of its package versions from the included versions.cfg file.
Notice that there is another line, commented out, that points to dist.plone.org.  This location will always contain the
most recent versions that comprise the latest release in the Plone 5.1 series.
(You can also replace 5.1-latest with 5.0-latest or 5.2-latest, or another other existing minor release in the 5.x series.)

To upgrade your buildout to use the latest Plone 5.1.x release, comment out versions.cfg and
uncomment the line pointing to dist.plone.org, so it looks like this:

.. code-block:: shell

    extends =
    base.cfg
    # versions.cfg
    http://dist.plone.org/release/5.1-latest/versions.cfg

Save your changes.


Upgrading
---------

Stop your Plone instance:

.. code-block:: console

    bin/plonectl stop

Rerun buildout:

.. code-block:: console

    bin/buildout

This may take a some time, as Plone downloads new releases.

When buildout finishes running, restart your Plone instance:

.. code-block:: console

     bin/plonectl start

Migration
=========

Visit your Management Interface (http://yoursite:8080).
You will see a message prompting you to run Plone's migration script for each site in your instance:

``This site configuration is outdated and needs to be upgraded.``

Click :guilabel:`Upgrade` button next to the site and the upgrade will run.

Check :guilabel:`Dry Run` if you want to test the migration before you execute it.
