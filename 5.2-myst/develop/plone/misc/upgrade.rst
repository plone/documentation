============
Upgrade tips
============

.. admonition:: Description

        Advanced tips for upgrading Plone.

        Some of the information on this page is for Plone 4, which used the Archetypes content type framework. Plone 5.x uses the Dexterity content type framework.

General Tips
============

This guide contains some tips for Plone upgrades. For more information, see
also the `official Plone upgrade guide <http://docs.plone.org/manage/upgrading/index.html>`_


Recommended setup
-----------------

* Test the upgrade on your local development computer first.

* Create two buildouts: one for the old Plone version (your existing buildout)
  and one for the new version.

* Prepare the migration in the old buildout. After all preparations are done, copy
  the Data.fs and blobstorage to the new buildout and run plone_migration tool there.


Fix persistent utilities
------------------------

You might need to clean up some leftovers from uninstalled add-ons which have
not cleanly uninstalled.

Use this utility:

* https://pypi.python.org/pypi/wildcard.fixpersistentutilities

.. note:: Perform this against old buildout


Content Upgrades
================

For content migrations, `Products.contentmigration
<https://pypi.python.org/pypi/Products.contentmigration/>`_  can help you.
Documentation on how to use it can be found on `plone.org
<https://plone.org/documentation/kb/migrate-custom-types-with-products.contentmigration>`_.


Migration from non-folderish to folderish Archetypes based content types
------------------------------------------------------------------------

Non-folderish content types are missing some BTree attributes, which folderish
content types have (See ``Products.BtreeFolder2.BTreeFolder2Base._initBtrees``
).

plone.app.folder provides an upgrade view to migrate pre-plone.app.folder (or
non-folderish) types to the new BTree based implementation (defined in:
``plone.app.folder.migration.BTreeMigrationView``).

To upgrade your non-folderish content types to folderish ones, just call
``@@migrate-btrees`` on your Plone site root, and you're done.

This applies to Archetypes based content types.


Upgrading theme
===============

Make sure that your site them works on Plone 4.
Official upgrade guide has tips how the theme codebase should
be upgraded.


Theme fixing and portal_skins
-----------------------------

Your theme might be messed up after upgrade.

Try playing around setting in *portal_skins* *Properties* tab.
You can enable, disable and reorder skins layer applied in the theme.

Upgrade may change the default theme and you might want to restore
custom theme in *portal_skins*.


Upgrade tips for plone.app.discussion
=====================================

Enabling plone.app.discussion after Plone 4.1 upgrade
-----------------------------------------------------

After migration from an earlier version of Plone, you will may notice that you
do not have a *Discussion* control panel for ``plone.app.discussion``, the new
commenting infrastructure which now ships as part of new Plone installs beyond
version 4.1.  If a check of your *Site Setup* page reveals that you do not have
the *Discussion* control panel, implement the following.


Install plone.app.discussion manually
-------------------------------------

#. Log into your Plone site as a user with Manager access
#. Browse to the following URL to manually install ``plone.app.discussion``::

    http://<your-plone-url>:<port>/<plone-instance>/portal_setup/manage_importSteps

#. In the *Select Profile or Snapshot* drop-down menu, select
   ``Plone Discussions``.
#. Click the ``Import all steps`` button at the bottom of the page.
#. Confirm that *Discussion* is now present as a control panel in your
   *Site Setup*


Migrate existing comments
-------------------------

Follow the instructions regarding `How to migrate comments to
plone.app.discussion
<https://plone.org/products/plone.app.discussion/documentation/how-to/how-to-migrate-comments-to-plone.app.discussion>`_
to migrate existing Plone comments.


Fixing Creator details on existing comments
-------------------------------------------

You may notice that some of your site's comments have the user's ID as their
Creator property.  At time of writing (for ``plone.app.discussion==2.0.10``),
the Creator field should refer to the user's full name and not their user ID.
You'll likely notice that a number of other fields, including
``author_username``, ``author_name`` and ``author_email`` are not present on
some of your migrated comments.  Reasons why comments get migrated but
unsuccessfully are being investigated.

This may change for future versions of ``plone.app.discussion``.  For now,
though, having the user ID left as the Creator is less than helpful and means
aspects like the username, name, and email not present affect usability of
comments.

If a site has many comments with this issue, it is possible to step through all
of them and correct them.  Using a script like the following will process each
of the affected comments accordingly:

.. code-block:: python

    from Products.CMFPlone.utils import getToolByName
    from zope.app.component import hooks
    from plone import api

    context = hooks.getSite()

    catalog = api.portal.get_tool(name='portal_catalog')
    mtool = api.portal.get_tool(name='portal_membership')

    brains = catalog.searchResults(object_provides='plone.app.discussion.interfaces.IComment')
    for brain in brains:
        member = api.user.get(username=brain.Creator')
        comment = brain.getObject()

        if member and not comment.author_username and not comment.author_name and not comment.author_email:
            fullname = member.getProperty('fullname')
            email = member.getProperty('email')
            if fullname and email:
                comment.author_username = brain.Creator #our borked user ID
                comment.creator = fullname
                comment.author_name = fullname
                comment.author_email = email
                comment.reindexObject()
                print 'Fixed and reindexed %s' % comment
            else:
                print 'Could not find properties for author of %s' % comment

This can be run anywhere an Acquisition ``context`` object is available, such
as running your Zope instance in ``debug`` mode, an ipython prompt, or some
other function on the filesystem.  The ``getSite()`` function call can (and may
need to) be replaced with some other pre-existing context object if that is
more suitable.

Keep in mind that this script was successfully used in a situation where no
possible collisions existed between correctly-migrated comments Creators' full
names and user IDs (the code looks up the Creator in the hope of finding a
valid Plone member).  If you had a situation where you had some correctly
migrated comments written by a user with ID ``david`` and full name of
``Administrator``, and also had a user with the ID of ``Administrator``, then
this script may not be suitable.  In the test situation, the three attributes
of ``author_username``, ``author_name``, and ``author_email`` were observed as
all being ``None``, so in checking for this too, this may avoid problems.  Test
the code first with something like a ``print`` statement to ensure all comments
will get modified correctly.
