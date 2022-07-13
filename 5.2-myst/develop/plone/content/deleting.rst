========
Deleting
========

.. admonition:: Description

    Deleting content items in Plone programmatically.
    How link integrity checks work and how (and when!) to avoid them.


Introduction
============

This document explains how to programmatically delete objects in Plone.

Deleting content by id
======================

Deleting content objects is done by IObjectManager.

`IObjectManager definition <http://svn.zope.org/Zope/trunk/src/OFS/interfaces.py?rev=96262&view=auto>`_.

Example::

    # manage_delObjects takes list of ids as an argument
    folder.manage_delObjects(["list", "of", "ids", "to", "delete"])

Or::

    parent = context.aq_parent
    parent.manage_delObjects([context.getId()])

Permissions
-----------

The user must have Zope 2 *Delete objects* permission on the *content item* being
deleted. This is checked in ``Products.CMFPlone.PloneFolder.manage_delObjects()``.

Otherwise an ``Unauthorized`` exception is raised.

Example how to check for this permission::

    from Products.CMFCore import permissions

    hospital = self.portal.country.hospital
    item = hospital.patient1

    mt = getToolByName(self.portal, 'portal_membership')
    if mt.checkPermission(permissions.DeleteObjects, item):
        # Can delete
        raise AssertionError("Oooops. Deletion allowed")
    else:
        pass

Bypassing permissions
---------------------

This is handy if you work e.g. in a :doc:`debug shell </develop/plone/misc/commandline>`
and you are deleting badly behaved objects::

    from AccessControl.SecurityManagement import newSecurityManager
    admin = app.acl_users.getUserById("admin")
    app.folder_sits.sitsngta.manage_delObjects("examples")
    # Try harder:
    # app.folder_sits.sitsngta._delObject("examples", suppress_events=True)
    import transaction ; transaction.commit()

Bypassing link integrity check
------------------------------

Plone 5 handles deleting an item in its user interface only;
there's no longer need to bypass link integrity programmatically.

For more information check the documentation of `plone.app.linkintegrity <https://pypi.python.org/pypi/plone.app.linkintegrity/3.0>`_.

Deleting all content in a folder
================================

This can be a bit tricky. An example::

    ids = folder.objectIds() # Plone 3 or older
    ids = folder.keys()      # Plone 4 or newer

    if len(ids) > 0:
        # manage_delObject will mutate the list
        # so we cannot give it tuple returned by objectIds()
        ids = list(ids)
        folder.manage_delObjects(ids)

Fail safe deleting
===================

Sometimes deletion might fail because it dispatches
events which might raise exception due to bad broken objects
or badly behaving code.

`OFS.ObjectManager <http://svn.zope.org/Zope/trunk/src/OFS/ObjectManager.py?rev=115507&view=auto>`_, the base class for Zope folders,
provides an internal method to delete
objects from a folder without firing any events::

    # Delete object with id "broken-folder" without firing any delete events
    site._delObject("broken-folder", suppress_events=True)

The best way to clean up bad objects on your site is via a
:doc:`command line script </develop/plone/misc/commandline>`,
in which case remember to commit the transaction
after removing the broken objects.

Purging old content from site
=============================

This Management Interface script allows you to find content items of certain type and
delete them if they are created too long ago::

    # Delete FeedfeederItem content items which are more than three months old

    from StringIO import StringIO
    import DateTime

    buf = StringIO()

    # DateTime deltas are days as floating points
    end = DateTime.DateTime() - 30*3
    start = DateTime.DateTime(2000, 1,1)

    date_range_query = { 'query':(start,end), 'range': 'min:max'}

    items = context.portal_catalog.queryCatalog({
                "portal_type":"FeedFeederItem",
                "created" : date_range_query,
                "sort_on" : "created" })

    items = list(items)

    print >> buf, "Found %d items to be purged" % len(items)

    count = 0
    for b in items:
        count += 1
        obj = b.getObject()
        print >> buf, "Deleting:" + obj.absolute_url() + " " + str(obj.created())
        obj.aq_parent.manage_delObjects([obj.getId()])

    return buf.getvalue()

Below is an advanced version for old item-date-based deletion code
which is suitable for huge sites.
This snippet is from the ``Products.feedfeeder`` package.
It will look for ``Feedfeeder`` items
(automatically generated from RSS) which
are older than X days and delete them.

It's based on Zope 3 page registration (sidenote: I noticed that views do not
need to be based on BrowserView page class).

* Transaction thresholds make sure the code runs faster and does not
  run out of RAM

* Logging to Plone event log files

* Number of days to look into past is not hardcoded

* Manage rights needed to execute the code

You can call this view like::

    http://localhost:9999/plonecommunity/@@feed-mega-cleanup?days=90

Here is the view Python source code::

    import logging

    import transaction
    from zope import interface
    from zope import component
    import DateTime
    import zExceptions

    logger = logging.getLogger("feedfeeder")

    class MegaClean(object):
        """ Clean-up old feed items by deleting them on the site.

        This is intended to be called from cron weekly.
        """

        def __init__(self, context, request):
            self.context = context
            self.request = request

        def clean(self, days, transaction_threshold=100):
            """ Perform the clean-up by looking old objects and deleting them.

            Commit ZODB transaction for every N objects to that commit buffer does not grow
            too long (timewise, memory wise).

            @param days: if item has been created before than this many days ago it is deleted

            @param transaction_threshold: How often we commit - for every nth item
            """

            logger.info("Beginning feed clean up process")

            context = self.context.aq_inner
            count = 0


            # DateTime deltas are days as floating points
            end = DateTime.DateTime() - days
            start = DateTime.DateTime(2000, 1,1)

            date_range_query = {'query':(start,end), 'range': 'min:max'}

            items = context.portal_catalog.queryCatalog({
                        "portal_type": "FeedFeederItem",
                        "created": date_range_query,
                        "sort_on": "created" })

            items = list(items)

            logger.info("Found %d items to be purged" % len(items))

            for b in items:
                count += 1
                obj = b.getObject()
                logger.info("Deleting:" + obj.absolute_url() + " " + str(obj.created()))
                obj.aq_parent.manage_delObjects([obj.getId()])

                if count % transaction_threshold == 0:
                    # Prevent transaction becoming too large (memory buffer)
                    # by committing now and then
                    logger.info("Committing transaction")
                    transaction.commit()

            msg = "Total %d items removed" % count
            logger.info(msg)

            return msg

        def __call__(self):

            days = self.request.form.get("days", None)
            if not days:
                raise zExceptions.InternalError("Bad input. Please give days=60 as HTTP GET query parameter")

            days = int(days)

            return self.clean(days)

Then we have the view ZCML registration:

.. code-block:: xml

    <page
        name="feed-mega-cleanup"
        for="Products.CMFCore.interfaces.ISiteRoot"
        permission="cmf.ManagePortal"
        class=".feed.MegaClean"
        />
