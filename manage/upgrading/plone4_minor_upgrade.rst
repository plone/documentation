
=========================================================
Upgrading Plone 4 within 4.x.x series dot minor releases
=========================================================

*Plone 4 uses buildout, which makes minor version upgrades very simple.*

Plone 4.0 and above use buildout in its packaged installers.
Among the many benefits of buildout is the fact that it makes minor Plone version
upgrades extremely simple. Here is the general procedure, which is based on the
buildout shipped with the Plone Unified Installer.


.. warning::

   Before performing any Plone upgrade, you should always have a complete backup of your site.
   See the :doc:`Preparations </manage/upgrading/preparations>` section of this manual for more details.

   In addition, you should check the :doc:`Version-specific migration tips </manage/upgrading/version_specific_migration/index>`
   section of this manual for any notes that may apply to the specific version upgrade you're about to perform.

**1) Edit your buildout.cfg file**

Out of the box, Plone's Unified Installer includes a buildout.cfg (typically located at your-plone-directory/zinstance/buildout.cfg) file that contains the following parameter::

    extends = 
    base.cfg
    versions.cfg
    # http://dist.plone.org/release/4.1-latest/versions.cfg

This tells buildout to get all of its package versions from the included versions.cfg file.  Notice that there is another line, commented out, that points to dist.plone.org.  This location will always contain the most recent versions that comprise the latest release in the Plone 4.1 series.  (You can also replace 4.1-latest with 4.0-latest or 4.2-latest, or another other existing minor release in the 4.x series.)

To upgrade your buildout to use the latest Plone 4.1.x release, comment out versions.cfg and uncomment the line pointing to dist.plone.org, so it looks like this::

    extends = 
    base.cfg
    # versions.cfg
    http://dist.plone.org/release/4.1-latest/versions.cfg

Save your changes.

**2) Stop Plone, Rerun Buildout, Restart Plone**

Now that you've edited your buildout file, stop Plone (*bin/plonectl stop*), rerun buildout with the command::

    > bin/buildout

This may take a few minutes as Plone downloads new releases. When buildout finishes running, restart your Plone instance (*bin/plonectl start*).

**3) Run Migration Script**

Visit your Zope instance's ZMI (http://yoursite:8080). You will likely see a message prompting you to run Plone's migration script for each site in your instance, e.g.

                                   ``This site configuration is outdated and needs to be upgraded.``

Click **Upgrade** button next to the site and the upgrade will run. Check the *Dry Run* checkbox if you want to test the migration before you execute it.

Voila! You've successfully upgraded your Plone site. Plone on!
