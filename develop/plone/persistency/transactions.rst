============
Transactions
============


Introduction
============

Plone uses the
`ZODB database <http://en.wikipedia.org/wiki/Zope_Object_database>`_ which
implements `Multiversion concurrency control
<http://en.wikipedia.org/wiki/Multiversion_concurrency_control>`_.

Plone will complete either *all* database modifications that occur during a
request, or *none* of them. It will never write incomplete data to the
database.

Plone and the underlying Zope handles transactions transparently.

.. note::

    Every transaction is a *read* transaction until any of the objects
    participating in the transaction are mutated (object attribute set),
    turning the transaction to a *write* transaction.

.. note::

    Old examples might refer to the ``get_transaction()`` function. This has
    been replaced by ``transaction.get()`` in the later Zope versions.

Please read this
`Zope transaction tutorial <http://www.zope.org/Members/mcdonc/HowTos/transaction>`_
to get started how to use transactions with your code.

* https://bugs.launchpad.net/zope2/+bug/143584

Using transactions
==================

Normally transactions are managed by Plone and the developer should not be
interested in them.

Special cases where one would want to manage transaction life-cycle may
include:

* Batch creation or editing of many items once.

Example code:

* `transaction source code <http://svn.zope.org/transaction/trunk/transaction/?rev=104430>`_.

* http://www.zope.org/Members/mcdonc/HowTos/transaction

* https://bugs.launchpad.net/zope3/+bug/98382


Subtransactions
----------------

Normally, a Zope transaction keeps a list of objects modified within the
transaction in a structure in RAM.

This list of objects can grow quite large when there is a lot of work done
across a lot of objects in the context of a transaction. *Subtransactions*
write portions of this object list out to disk, freeing the RAM required by
the transaction list. Using subtransactions can allow you to build
transactions involving objects whose combined size is larger than available
RAM.

Example::

    import transaction
    ...

    done = 0
    for brain in all_images:
        done += 1
        ...
        # Since this is HUGE operation (think resizing 2 GB images)
        # it is not nice idea to buffer the transaction (all changed data)
        # in the memory (Zope default transaction behavior).
        # Using subtransactions we hint Zope when it would be a good time to
        # flush the changes to the disk.
        if done % 10 == 0:
            # Commit subtransaction for every 10th processed item
            transaction.get().commit(True)

Failsafe crawling and committing in batches
==============================================

In the case you need to access many objects in coherent and efficient manner.

* https://bitbucket.org/gocept/gocept.linkchecker/src/80a127405ac06d2054e61dd62fcd643d864357a0/src/gocept/linkchecker/scripts/crawl-site.py?at=default

Transaction boundary events
============================

It is possible to perform actions before and after transaction is written to
the database.

See transaction documentation about
`before commit hooks <http://zodb.readthedocs.org/en/latest/transactions.html#before-commit-hook>`_ and
`after commit hooks <http://zodb.readthedocs.org/en/latest/transactions.html#after-commit-hooks>`_.


Viewing transaction content and debugging transactions
=======================================================

Please see :doc:`Transaction troubleshooting </manage/troubleshooting/transactions>`

Undoing transactions
=======================

Everything that has happened on Plone site can be undoed through the *Undo*
tab in the Management Interface, in the site root.
By default you can undo latest 20 transactions.

If you need to raise this limit just replace all numbers of ``20``
with higher value in file ``App/Undo.py``, restart site and now you can undo more transactions.

