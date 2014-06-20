=======================
Updating 2.5.3 to 3.0.3
=======================

.. admonition:: Description

   Specific steps (for review) on updating a Plone 2.5.3 site to 3.0.3 on Linux using the Universal Installer package.

Migration Procedure
===================

These steps assume a previous 2.5.3 installation in the folder */var/plone/*, which should be modified if necessary to suit your environment.

#. Download and un-archive the Plone 3 universal installer package for Linux.
#. Modify the install.sh script to point the **PLONE_HOME** variable to */var/plone/*
#. In the existing Plone site, take note of any non-Plone products that need to be moved to the upgraded instance.

    It is advisable to un-install any non-essential third-party products before migrating to a new version. In most cases, products are the biggest obstacle to migrating a site, and weeding out unnecessary products can save a great deal of time and frustration. These products can be re-installed as new packages after migration.

    It also seems necessary in some cases to remove installed caching objects (CacheFu), uninstall the caching products, and install new versions of the products and create new caching tools after migrating.

#. As the root user (or with "sudo"), shut down the existing Plone/Zope/Zeo cluster::

    /var/plone/zeocluster/bin/shutdowncluster.sh

#. Move */var/plone/* to a backup folder, such as */var/plone253/*
#. Run the Plone 3 install.sh script with the "zeo" cluster option::

    ./install.sh zeo

#. Start the new cluster::

    /var/plone/zeocluster/bin/startcluster.sh

   This can take some time, as a new Plone site is now created as part of the process.
#. Log into the ZMI as the "admin" user, using the password specified in */var/plone/zeocluster/adminPassword.txt:*
   http://localhost:8080/manage/

   Once logged in, you may want to change the admin password to something more memorable (yet still secure) for future use:
   http://localhost:8080/acl_users/users/manage_users?user_id=admin&passwd=1
#. Stop the new cluster::

   /var/plone/zeocluster/bin/shutdowncluster.sh

#. In */var/plone/zeocluster/server/var/*, create a backup/ folder, and move all existing contents to this new folder::

    cd /var/plone/zeocluster/server/var/
    mkdir backup
    mv Data.fs* backup/

    .. note::

    Note that this step isn't completely necessary: you could just delete the existing files, but it's nice to back-up a working configuration in case things go wrong later.

#. Copy Data.fs from the old instance to the new installation, and ensure the permissions are correct::

    cp /var/plone253/zeocluster/server/var/Data.fs .
    chown plone:plone Data.fs

#. Start the new cluster::

    /var/plone/zeocluster/bin/startcluster.sh

#. Log into the ZMI as the "admin" user:
   http://localhost:8080/manage/

#. .. note::

      Note: this step is here presently only for the purpose of a full procedure review: it may be bug-related and should not be performed as part of a base migration. Try this only if all else fails.

   In the ZMI, at the Plone site root, delete the following objects:
   * **content_type_registry**
   * **mimetypes_registry**
   * **portal_transforms**

#. .. note::

      Note: this step is here presently only for the purpose of a full procedure review: it may be bug-related and should not be performed as part of a base migration. Try this only if all else fails.

   At the site root, using the Add pull-down, add new versions of the **Content Types Registry**, **MimetypesRegistry Tool**, and **PortalTransforms Tool** (in that order).
#. At the site root, click **portal_migration**, and in the **Upgrade** tab, click the **Upgrade** button.
#. After upgrading the site, click the **View** tab to test the main page.
#. Click **Site Setup**, and then click **Add/Remove Products**.
#. Under **Installed Products**, click the **Migrate** button to re-install any necessary existing products (in my case, this was **CMFPlacefulWorkflow** and **Marshall**).
#. Download and un-archive any required products to /var/plone/zeocluster/Products
   Make sure the product directories are complete, and that all contents have the proper owner ("plone").
#. Re-start the cluster.
#. In **Site Setup** on the Plone site, in **Add/Remove Products**, install the new products.

