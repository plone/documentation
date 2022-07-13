================
Renaming content
================

.. admonition:: Description

        How to programmatically rename Plone content items


Introduction
------------

This page tells how to rename Plone content objects and change their ids.

* This only concerns URL path ids

* Archetypes' Unique ID (UID) is not affected by the rename operation

* Title can be changed using ``setTitle()`` (Archetypes) or related mutator

Renaming objects
----------------

OFS interface has facilities to rename objects

* http://svn.zope.org/Zope/trunk/src/OFS/interfaces.py?rev=105745&view=auto

* ``manage_renameObject(oldid, newid)`` for one item

* ``manage_renameObject([oldid, oldid2], [newid, newid2])`` for rename many items

* Products.CMFPlone.PloneFolder overrides manage_renameObject() to have hooks
  to reindex the new object path


.. warning::

        Security warning: "Copy or Move" permission is needed on the object by
        the logged in user.

.. warning::

        New id must be a 8-bit string, not unicode.
        The system might accept values in invalid format.

Example how to rename object *lc* to have *-old* suffix::

        id = lc.getId()
        if not lc.cb
        parent = lc.aq_parent
        parent.manage_renameObject(id, id + "-old")




These checks performed before rename by the manage_renameObject()::

        if not lc.cb_userHasCopyOrMovePermission():
            print "Does not have needed permission"
            return

        if not lc.cb_isMoveable():
            # This makes sanity checks whether the object is
            # properly connected to the database
            print "Object problem"
            return

.. warning::

        Testing warning: Rename mechanism relies of Persistent attribute called _p_jar to be present
        on the content object. By default, this is not the case on unit tests. You need to call
        transaction.savepoint() to make _p_jar appear on persistent objects.

        If you don't do this, you'll receive a "CopyError" when calling manage_renameObjects
        that the operation is not supported.


Unit testing example::

        import transaction


        self.portal.invokeFactory("Document", doc")
        doc = self.portal.doc

        # Make sure all persistent objects have _p_jar attribute
        transaction.savepoint(optimistic=True)

        # Call manage_renameCode()...

