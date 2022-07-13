==========================================
 Database and transactions troubleshooting
==========================================

.. admonition:: Description

    How to debug and fix ZODB database problems in Plone


Introduction
=============

This document contains information to fix and debug ZODB databases with Plone.

BLOBs and POSKeyErrors
======================

The `Plone CMS <https://plone.org>`_ from version 4.x onwards
stores files and images uploaded to the `ZODB <http://www.zodb.org/>`_
as blob.
They exist in a ``var/blobstorage`` folder structure on the file system,
files being named after (opaque) persistent object ids.
When using the default backend, the objects themselves,
without file payload,
are stored in an append-only database file called
*filestorage* and usually the name of this file is ``Data.fs``.

If you copy the Plone site database object data (``Data.fs``) and
forget to copy the ``blobstorage`` folder(s),
or if data gets out of the sync during the copy,
various problems appear on the Plone site:

* You cannot access a content item for which the a corresponding blob file
  is missing from the file system;

* you cannot rebuild the ``portal_catalog`` indexes;

* database packing may fail.

Instead, you'll see something like this - an evil ``POSKeyError`` exception
(POS referring to Persistent Object Storage)::

    Traceback (most recent call last):
      File "/fast/xxx/eggs/ZODB3-3.10.3-py2.6-macosx-10.6-i386.egg/ZODB/Connection.py", line 860, in setstate
        self._setstate(obj)
      File "/fast/xxx/eggs/ZODB3-3.10.3-py2.6-macosx-10.6-i386.egg/ZODB/Connection.py", line 922, in _setstate
        obj._p_blob_committed = self._storage.loadBlob(obj._p_oid, serial)
      File "/fast/xxx/eggs/ZODB3-3.10.3-py2.6-macosx-10.6-i386.egg/ZODB/blob.py", line 644, in loadBlob
        raise POSKeyError("No blob file", oid, serial)
    POSKeyError: 'No blob file'

The proper solution to this problem is to:

* Re-copy ``blobstorage`` folder;

* restart Plone twice in foreground mode
  (sometimes a freshly copied blobstorage folder does not get picked up -
  some kind of timestamp issue?).
  Restarting ZEO clients once seems to be enough.

* :doc:`Copy a Plone site </manage/deploying/copy>`

However you may have failed.
You may have damaged or lost your ``blobstorage`` forever.
To get the Plone site to a working state,
all content with bad BLOB data must be deleted
(which usually entails losing some site images and uploaded files).

Below is Python code for a :doc:`BrowserView </develop/plone/views/browserviews>` which you can drop in to your own Plone.
It creates an admin view which you can call directly via an URL.
This code will walk through all the content on your Plone site and try to
delete bad content items with BLOBs missing.

The code handles both Archetypes and Dexterity subsystems' content types.

.. note::

    Fixing Dexterity blobs with this code has never been tested -
    please feel free to update the following code example
    if you find it not working properly.


The code, ``fixblobs.py``::

    """

        A Zope command line script to delete content with missing BLOB in Plone, causing
        POSKeyErrors when content is being accessed or during portal_catalog rebuild.

        Tested on Plone 4.1 + Dexterity 1.1.

        http://stackoverflow.com/questions/8655675/cleaning-up-poskeyerror-no-blob-file-content-from-plone-site

        Also see:

        https://pypi.python.org/pypi/experimental.gracefulblobmissing/

    """

    # Zope imports
    from ZODB.POSException import POSKeyError
    from zope.component import queryUtility
    from Products.CMFCore.interfaces import IPropertiesTool
    from Products.CMFCore.interfaces import IFolderish

    # Plone imports
    from Products.Five import BrowserView
    from Products.Archetypes.Field import FileField
    from Products.Archetypes.interfaces import IBaseContent
    from plone.namedfile.interfaces import INamedFile
    from plone.dexterity.content import DexterityContent


    def check_at_blobs(context):
        """ Archetypes content checker.

        Return True if purge needed
        """

        if IBaseContent.providedBy(context):

            schema = context.Schema()
            for field in schema.fields():
                id = field.getName()
                if isinstance(field, FileField):
                    try:
                        field.get_size(context)
                    except POSKeyError:
                        print "Found damaged AT FileField %s on %s" % (id, context.absolute_url())
                        return True

        return False


    def check_dexterity_blobs(context):
        """ Check Dexterity content for damaged blob fields

        XXX: NOT TESTED - THEORETICAL, GUIDELINING, IMPLEMENTATION

        Return True if purge needed
        """

        # Assume dexterity contennt inherits from Item
        if isinstance(context, DexterityContent):

            # Iterate through all Python object attributes
            # XXX: Might be smarter to use zope.schema introspection here?
            for key, value in context.__dict__.items():
                # Ignore non-contentish attributes to speed up us a bit
                if not key.startswith("_"):
                    if INamedFile.providedBy(value):
                        try:
                            value.getSize()
                        except POSKeyError:
                            print "Found damaged Dexterity plone.app.NamedFile %s on %s" % (key, context.absolute_url())
                            return True
        return False


    def fix_blobs(context):
        """
        Iterate through the object variables and see if they are blob fields
        and if the field loading fails then poof
        """

        if check_at_blobs(context) or check_dexterity_blobs(context):
            print "Bad blobs found on %s" % context.absolute_url() + " -> deleting"
            parent = context.aq_parent
            parent.manage_delObjects([context.getId()])


    def recurse(tree):
        """ Walk through all the content on a Plone site """
        for id, child in tree.contentItems():

            fix_blobs(child)

            if IFolderish.providedBy(child):
                recurse(child)


    class FixBlobs(BrowserView):
        """
        A management view to clean up content with damaged BLOB files

        You can call this view by

        1) Starting Plone in debug mode (console output available)

        2) Visit site.com/@@fix-blobs URL

        """
        def disable_integrity_check(self):
            """  Content HTML may have references to this broken image - we cannot fix that HTML
            but link integrity check will yell if we try to delete the bad image.


            """
            ptool = queryUtility(IPropertiesTool)
            props = getattr(ptool, 'site_properties', None)
            self.old_check = props.getProperty('enable_link_integrity_checks', False)
            props.enable_link_integrity_checks = False

        def enable_integrity_check(self):
            """ """
            ptool = queryUtility(IPropertiesTool)
            props = getattr(ptool, 'site_properties', None)
            props.enable_link_integrity_checks = self.old_check

        def render(self):
            #plone = getMultiAdapter((self.context, self.request), name="plone_portal_state")
            print "Checking blobs"
            portal = self.context
            self.disable_integrity_check()
            recurse(portal)
            self.enable_integrity_check()
            print "All done"
            return "OK - check console for status messages"

Registering the view in ZCML:

.. code-block:: xml

    <browser:view
            for="Products.CMFPlone.interfaces.IPloneSiteRoot"
            name="fix-blobs"
            class=".fixblobs.FixBlobs"
            permission="cmf.ManagePortal"
            />


More info

* http://stackoverflow.com/questions/8655675/cleaning-up-poskeyerror-no-blob-file-content-from-plone-site

* https://pypi.python.org/pypi/experimental.gracefulblobmissing/


Transactions
================

Transactions are usually problematic only when many
ZEO front-end clients are used.

ConflictError
---------------

When the site gets more load, ``ConflictError``\s start to occur.
Zope tries to solve the situation by replaying HTTP requests
for ``ConflictError``\s and has a default threshold (3) of
how many times the request is replayed.

More info

* https://www.andreas-jung.com/contents/on-zodb-conflict-resolution

How to debug which object causes ``ConflictError``\s
-----------------------------------------------------

``ConflictError``\s are caused by concurrent transactions trying to write to the same object(s) -
usually ``portal_catalog``.
They are harmless, but slow down badly coded sites.
Plone will retry the HTTP request and transaction three times before giving up.

The OID is visible in the ConflictError traceback.

You can turn OID back to the corresponding Python object,
as mentioned by A. Jung::

        from ZODB.utils import p64
        app._p_jar[p64(oid)]

If every transaction appears as write transaction
--------------------------------------------------

If you are not careful, you may accidentally write code
which turns all transactions to write transactions.
This typically happens when you call some method without realizing that
that method eventually modifies a persistent object,
causing a database write.

Symptoms:

* Your Undo tab in the Management Interface will be full of entries, one added per
  page request.

* If you run the server in single Zope server mode, it is slow.

* If you run the server in ZEO mode you get the exceptions like one below.
  It may happen even with one user.
  This is because each page load requres more than one HTTP request:
  HTML load, image load, CSS load and so on. Browser makes many requests
  per page and those transactions are conflicting, because they are
  all write transactions.

Traceback example::

        * Module ZPublisher.Publish, line 202, in publish_module_standard
        * Module ZPublisher.Publish, line 170, in publish
        * Module ZPublisher.Publish, line 170, in publish
        * Module ZPublisher.Publish, line 170, in publish
        * Module ZPublisher.Publish, line 157, in publish
        * Module plone.app.linkintegrity.monkey, line 15, in zpublisher_exception_hook_wrapper
        * Module ZPublisher.Publish, line 125, in publish
        * Module Zope2.App.startup, line 238, in commit
        * Module transaction._manager, line 96, in commit
        * Module transaction._transaction, line 395, in commit
        * Module transaction._transaction, line 495, in _commitResources
        * Module ZODB.Connection, line 510, in commit
        * Module ZODB.Connection, line 547, in _commit

    ConflictError: database conflict error (oid 0x2b92, class Products.CMFPlone.PropertiesTool.SimpleItemWithProperties)

How to debug it
`````````````````

Zope 2 doesn't have many well-documented ZODB debugging tools.
Below is one snippet to examine the contents of the last transactions
of an offline ``Data.fs`` file.
It is an evolved version of
`this original script <http://www.mail-archive.com/zodb-dev@zope.org/msg04387.html>`_.

* Do something on a badly behaving site.

* Stop Zope instance.

* Run the script below (``debug.py``) on the ``Data.fs`` file to see what
  objects have been changed.

* Guess the badly behaving code from the object class name.

Example how to run the script for the last 30 transaction under a Zope egg
environment using the ``zopepy`` script::

    bin/zopepy debug.py -n 30 Data.fs

.. Warning::
    The following is obsolete with current Zope. FileIterator does not
    take a ``pos`` argument any more.

Code for debug.py::

    ##############################################################################
    #
    # Copyright (c) 2001, 2002 Zope Corporation and Contributors.
    # All Rights Reserved.
    #
    # This software is subject to the provisions of the Zope Public License,
    # Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
    # THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
    # WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
    # WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
    # FOR A PARTICULAR PURPOSE
    #
    ##############################################################################
    """Tool to dump the last few transactions from a FileStorage."""

    from ZODB.fstools import prev_txn
    from ZODB.serialize import ObjectReader, get_refs
    from persistent.TimeStamp import TimeStamp
    from ZODB.FileStorage.FileStorage import FileIterator
    import cStringIO, cPickle
    import optparse, getopt
    import sys

    class Nonce(object): pass

    class Reader(ObjectReader):

        def __init__(self):
            self.identity = None

        def _get_unpickler(self, pickle):
            file = cStringIO.StringIO(pickle)
            unpickler = cPickle.Unpickler(file)
            unpickler.persistent_load = self._persistent_load

            def find_global(modulename, name):
                self.identity ="%s.%s"%(modulename, name)
                return Nonce

            unpickler.find_global = find_global

            return unpickler

        def getIdentity(self, pickle ):
            self.identity = None
            unpickler = self._get_unpickler( pickle )
            unpickler.load()
            return self.identity

        def getObject(self, pickle):
            unpickler = self._get_unpickler( pickle )
            ob = unpickler.load()
            return ob

    def pretty_size( size ):
        if size < 1024:
            return "%sB"%(size)
        kb = size / 1024.0
        if kb < 1024.0:
            return '%0.1fKb'%kb
        else:
            mb = kb/1024.0
            return '%0.1fMb'%mb

    def run(path, ntxn):
        f = open(path, "rb")
        f.seek(0, 2)

        th = prev_txn(f)
        for i in range(ntxn):
            th = th.prev_txn()
        f.close()
        reader = Reader()
        iterator = FileIterator(path, pos=th._pos)
        for i in iterator:
            print "Transaction ", TimeStamp(i.tid), i.user, i.description
            object_types = {}
            for o in i:
                ot = reader.getIdentity(o.data)
                if ot in object_types:
                    size, count = object_types[ot]
                    object_types[ot] = (size+len(o.data), count+1)
                else:
                    object_types[ot] = (len(o.data),1)


                ob = cPickle.loads(o.data)

                print "Object data for :" + str(o)

                # Not sure why some objects are stored as tuple (object, ())
                if type(ob) == tuple and len(ob) == 2:
                    ob = ob[0]

                if hasattr(ob, "__dict__"):
                    for i in ob.__dict__.items():
                        if not callable(i[1]):
                            print i
                else:
                    print "can't extract:" + str(ob)

                print "-------------------------------------------------------"

            keys = object_types.keys()
            keys.sort()
            for k in keys:
                # count, class, size (aggregate)
                print " - ", object_types[k][1], k, pretty_size(object_types[k][0])


    def main():
        ntxn = 20
        opts, args = getopt.getopt(sys.argv[1:], "n:")
        path, = args
        for k, v in opts:
            if k == '-n':
                ntxn = int(v)
        run(path, ntxn)


    if __name__ == "__main__":
        main()


zeostorage Client has seen newer transactions than server
---------------------------------------------------------

If you get::

    ClientStorageError: zeostorage Client has seen newer transactions than server!

, you can fix it by removing ``cache-data.zec`` from ``parts/instace/var/``.


Updating objects created by older code
======================================

In the course of development, classes may be renamed or moved.
When an object is read from the ZODB,
the class required to unpickle the serialized object is named in the pickle data.
If this name cannot be imported, you have a broken object on your hands.

In the Zope event log that will show up as, for example::

    2014-06-19 11:04:04 WARNING OFS.Uninstalled Could not import class 'ATSimpleStringCriterion' from module 'Products.ATContentTypes.types.criteria.ATSimpleStringCriterion'

To make the object usable again,
the reference needs to be updated to refer to a class that can instantiate this object.
One tool that can help you with this is
`zodbupdate <https://pypi.python.org/pypi/zodbupdate>`_

In this case, the ``ATSimpleStringCriterion`` class in question has moved from
``Products.ATContentTypes.types.criteria.ATSimpleStringCriterion`` to
``Products.ATContentTypes.criteria.simplestring``.

To make ``zodbupdate`` handle this, add a ``zodbupdate`` entry point to
``ATContentTypes``. Depending on your configuration, that may look like
this:

.. code-block:: console

    $ cat .../buildout-cache/eggs/Products.ATContentTypes-2.1.13-py2.7.egg/EGG-INFO/entry_points.txt
    [zodbupdate]
    renames=Products.ATContentTypes:rename_dict

Next, define ``rename_dict`` in the ``__init__.py`` of the named package, e.g.::

    .../buildout-cache/eggs/Products.ATContentTypes-2.1.13-py2.7.egg/Products/ATContentTypes/__init__.py

 In this case, our ``rename_dict`` will look like this:

.. code-block:: python

    rename_dict = {
        'Products.ATContentTypes.types.criteria.ATSimpleStringCriterion ATSimpleStringCriterion':
        'Products.ATContentTypes.criteria.simplestring ATSimpleStringCriterion'}

.. note:: As always, work on a copy of your data first, before working on the live site.
