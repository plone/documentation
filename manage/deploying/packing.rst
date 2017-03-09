================
Database packing
================

.. admonition:: Packing is a vital regular maintenance procedure

    The Plone database does not automatically prune deleted content.
    You must periodically pack the database to reclaim space.

Zope's object database does not immediately remove objects when they are deleted.
Instead, they are just marked inactive.
This has advantages: it supplies a knowledgeable administrator with the ability to undo transactions
on an emergency basis.
However, this means that the disk space consumed by your object database will grow with every transaction.

*Packing* the database reclaims the space previously consumed by deleted objects.
You *must* periodically pack your database, or it will eventually consume all available disk space.

It also may be done while the system is live.

Setting up packing
==================

On a development or testing installation, packing will be an infrequent need.

You may initiate a packing operation via the Management Interface.

It will allow you to set the number of days of transactions you wish to keep in the undo stack.

On a production system, you should pack the database via a ``bin/zeopack`` in your buildout directory.

*zeopack* is installed automatically by the `plone.recipe.zeoserver <https://pypi.python.org/pypi/plone.recipe.zeoserver/>`_
recipe that generates the zeoserver (database server component).

You may set packing options for zeopack by setting attributes in the zeoserver part of your buildout:

.. code-block:: shell

    [zeoserver]
    recipe = plone.recipe.zeoserver
    ...
    pack-days = 3

Will (after buildout is run), cause bin/zeopack to conserve three days of undo history during the pack operation.

Other options include:

pack-gc

    Can be set to false to disable garbage collection as part of the pack.
    Defaults to true.

pack-keep-old

    Can be set to false to disable the creation of \*.fs.old files before
    the pack is run. Defaults to true.

pack-user

    If the ZEO server uses authentication, this is the username used by the
    zeopack script to connect to the ZEO server.

pack-password

    If the ZEO server uses authentication, this is the password used by the
    zeopack script to connect to the ZEO server.

Packing
=======

Expect the packing operation to be time-consuming and for the time to grow on a linear basis with the size of your object database.

Disk-space
----------

The packing operation will (unless you force this off) copy the existing database before it begins packing.

This means that a packing operation will consume up-to twice the space currently occupied by your object database.
(Pre-existing .old files get overwritten.)

Regular scheduling
------------------

Database packing is typically run as an automated (cron) job.

The cron job may be set up in the system cron table, or in the Plone users.

Disk packing is an extremely disk-intensive operation.
It is best to schedule it to occur when your monitoring indicates that disk usage is usually low.
