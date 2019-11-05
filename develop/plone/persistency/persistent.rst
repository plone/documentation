==================
Persistent objects
==================

.. admonition:: Description

        This document tells how to save objects to Plone/Zope database.
        Persistent objects are automatically read and written from ZODB database in Plone
        and they appear as normal Python objects in your code. This document clarifies
        some of special properties, like with containers, when you deal with persistent
        objects programmatically.


Introduction
------------

**Q: How do I save() object in Plone**

**A: You don't**

Plone does this automatically for you. You just assign the file data
as an attribute of some persistent object. When the HTTP request
completes, Zope transaction manager will automatically update all
changed persistent objects to the database. There is no "save" as such in Zope world -
it all is transparent to the developer. If the
transaction fails in any point, no data is being written and you do
not need to worry about the partial data being written to the
database.

* Changed objects will be automatically saved (if they are attached to the
  traversing graph)

* Save will not occur if an exception is raised

If your data class inherits from higher level Plone base classes
(all go up to persistent.Persitent class). persistency is handled transparently for you.
Plone also handles
transaction automatically for each HTTP request. Unless you wish
to do manual transactions there is no need to call transaction.commit().

If you want to do your own persistent classes please read the following

* `Writing a persistent class <http://www.zodb.org/documentation/guide/prog-zodb.html#writing-a-persistent-class>`_

* `About persistent objects <http://www.zope.org/Documentation/Books/ZDG/current/Persistence.stx>`_

* `Persistent interface description <http://apidoc.zope.org/++apidoc++/Interface/persistent.interfaces.IPersistent/index.html>`_.

* `ZODB tips and tricks <https://plone.org/events/regional/nola05/collateral/Chris%20McDonough-ZODB%20Tips%20and%20Tricks.pdf>`_

Lists and dictionaries
----------------------

If you modify objects inside persistent lists and dictionaries, the change is not automatically
reflected to the parent container.

* `Modifying mutable objects <http://zodb.readthedocs.org/en/latest/working.html#handling-changes-to-mutable-objects>`_

PersistentList vs. normal Python list
-------------------------------------

All items in normal Python list are stored as one write and loaded on one write.
PersistentList is slower, but allows individual objects picked from the list without loading the whole list.

For more information, see

* https://mail.zope.org/pipermail/zodb-dev/2009-December/013011.html


Persistent, modifications, __setattr__ and transactions
--------------------------------------------------------

When Persitent object is modified, via attribute set or __setattr__() call,
the current transaction is converted to a write transaction.
Write transactions are usually undoable (visible on Zope's Undo tab).

If you are using Python property mutator and even if it does not write to the object it
still will trigger the object rewrite.

More info

* https://mail.zope.org/pipermail/zodb-dev/2009-December/013047.html

Up-to-date reads
----------------

Normally, ZODB only assures that objects read are consistent, but not necessarily up to date.
Checking whether an object is up to date is important when information read from one object
is used to update another.

The following will force the object to use the most up-to-date version in the transaction::

        self._p_jar.readCurrent(ob)

A conflict error will be raised if the version of ob read by the transaction isn't
current when the transaction is committed.

.. note::

        ZODB versions older than 3.10.0b5 do not support this feature.

More information

* https://pypi.python.org/pypi/ZODB3/3.10.0b5#b5-2010-09-02

Accessing broken objects
------------------------

ZODB is object database.
By default, it cannot load object from the database if the code (Python class)
is not present.

You can still access data in the objects by creating Python code "stubs" which
fake the non-existing classes in the run-time environment.

More info

* http://mockit.blogspot.com/2010/11/getting-broken-objects-out-of-zodb.html

Fixing damaged objects
------------------------

If your BTrees have been damaged, you can use ``dm.historical`` tool
to inspect the object history and rewind it to a working state.

* http://plone.293351.n2.nabble.com/Cleaning-up-damaged-BTree-can-t-delete-folder-tp5761780p5773269.html

* https://pypi.python.org/pypi/dm.historical/

See also

* :doc:`Deleting broken objects </develop/plone/content/deleting>`

Volatile references
--------------------

Volatile attributes are attributes on persistent objects which never get stored.
ZODB assumes variable is volatile if it has _v_ prefix.

Volatiles are useful when framework expects the object to conform certain interface,
like form frameworks. However, your persistent object edited by form cannot
have persistent attributes for all variables the form expects to see.

Example::

    from persistent import Persistent
    from zope.annotation import IAnnotations

    class VolatileContext(object):
        """ Mix-in class to provide context variable to persistent classes which is not persistent.

        Some subsystems (e.g. forms) expect objects to have a reference to parent/site/whatever.
        However, it might not be a wise idea to have circular persistent references.

        This helper class creates a context property which is volatile (never persistent),
        but can be still set on the object after creation or after database load.
        """

        def _set_context(self, context):
            self._v_context = context

        def _get_context(self):
            return self._v_context

    class MobileBehaviorStorage(VolatileContext, Persistent):
        """Set mobile specific field properties on the context object and return the context object itself.#

        This allows to use attribute storage with schema input validation.
        """

        mobileFolderListing = FieldPropertyDelegate(IMobileBehavior["mobileFolderListing"])


    KEY = "mobile"

    def manufacture_mobile_behavior(context):

        annotations = IAnnotations(context)
        if not KEY in annotations:
            annotations[KEY] = MobileBehaviorStorage()

        object = annotations[KEY]

        # Set volatile context
        object.context = context

        return object

Correct use of volatile variables in functions
================================================

**WRONG**::

    if hasattr(self, '_v_image'):
        return self._v_image

**RIGHT**::

    marker = []
    value = getattr(self, "_v_image", marker)
    if value is not marker:
        return value

**RIGHT**::

    try:
        return self._v_image
    except AttributeError:

**WRONG**::

    self._v_image=expensive_calculation()
    return self._v_image

**RIGHT**::

    image=expensive_calculation()
    self._v_image=image
    return image

For more information, see

* https://mail.zope.org/pipermail/zodb-dev/2010-May/013437.html


Measuring persistent object sizes
---------------------------------

Get the size of the pickled object in the database.

Something like::

        pickle, serial = obj._p_jar._storage.load(obj._p_oid, obj._p_jar._version)

See also

* http://blog.hannosch.eu/2009/05/visualizing-persistent-structure-of.html

* https://plone.org/documentation/kb/debug-zodb-bloat

* treeanalyze.py will give you the total size of a traverse graph http://svn.erp5.org/erp5/trunk/utils/treenalyser.py?view=markup&pathrev=24405


