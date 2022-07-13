================================
Backing up your Plone deployment
================================

.. admonition:: Description

   Strategies for backing up operating Plone installations.


A guide to determining what to back up and how to back it up and restore it
safely.

Introduction
============

The key rules of backing up a working system are probably:

* Back up everything

* Maintain multiple generations of backup

* Test restoring your backups

.. warning::

    This guide assumes that you are already doing this for your system as a
    whole, and will only cover the considerations specific to Plone. When we
    say we are assuming you're already doing this for the system as a whole,
    what we mean is that your system backup mechanisms - rsync, bacula,
    whatever - are already backing up the directories into which you've
    installed Plone.

Your buildout and buildout caches are already backed up, and you've tested
the restore process.

Your remaining consideration is making sure that
Plone's database files are adequately backed up and recoverable.

Objects in motion
-----------------

Objects in motion tend to remain in motion. Objects that are in motion are
difficult or impossible to back up accurately.

Translation: Plone is a long-lived process that is constantly changing its
content database. The largest of these files, the Data.fs filestorage which
contains everything except Binary Large OBjects (BLOBs), is always open for
writing. The BLOB storage, a potentially complex file hierarchy, is
constantly changing and must be referentially synchronized to the filestorage.

This means that most system backup schemes are incapable of making useful
backups of the content database while it's in use. We assume you don't want
to stop your Plone site to backup, so you need to add procedures to
make sure you have useful backups of Plone's data. (We assume that you know
that the same thing is true of your relational database storage.)

Where's my data?
----------------

Your Plone instance installation will contain a ``./var`` directory (in the same
directory as buildout.cfg) that contains the frequently changing data files
for the instance. Much of what's in ./var, though, is not your actual content
database. Rather, it's log, process id, and socket files.

The directories that actually contain content data are:

Filestorage
~~~~~~~~~~~

``./var/filestorage``:

This is where Zope Object Database filestorage is maintained. Unless
you've multiple storages or have changed the name, the key file is
Data.fs. It's typically a large file and contains everything except BLOBS.

The other files in filestorage, with extensions like .index, .lock,
.old, .tmp are ephemeral, and will be recreated by Zope if they're absent.

Blobstorage
~~~~~~~~~~~

``./var/blobstorage``:

This directory contains a deeply nested directory hierarchy that,
in turn, contains the BLOBs of your database: PDFs, image files, office
automation files and such.

The key thing to know about filestorage and blobstorage is that they are
maintained synchronously. The filestorage has references to BLOBs in the
blobstorage.
If the two storages are not synchronized, you'll get errors.

collective.recipe.backup
========================

`collective.recipe.backup <https://pypi.python.org/pypi/collective.recipe.backup>`_
is a well-maintained and well-supported recipe for solving the "objects in
motion" problem for a live Plone database. It makes it easy to both back up
and restore the object database. The recipe is basically a sophisticated
wrapper around ``repozo``, a Zope database backup tool, and ``rsync``, the
common file synchronization tool.

.. note::

    Big thanks to Reinout van Rees, Maurits van Rees and community helpers for
    creating and maintaining collective.recipe.backup.

If you're using any of Plone's installation kits, collective.recipe.backup is
included in your install. If not, you may add it to your buildout by adding
a ``backup`` part:

.. code-block:: ini

    [buildout]
    parts =
        ...
        backup
        ...

    [backup]
    recipe = collective.recipe.backup

There are several useful option settings for the recipe, all set by adding
configuration information. All are documented on `the PyPI page
<https://pypi.python.org/pypi/collective.recipe.backup>`_. Perhaps the most
useful is the ``location`` option, which sets the destination for backup
files:

.. code-block:: ini

    [backup]
    recipe = collective.recipe.backup
    location = /path/to/reliably/attached/storage/filestorage
    blobbackuplocation =  /path/to/reliably/attached/storage/blobstorage

If this is unspecified, the backup destination is the buildout var directory.
The backup destination, though, may be any reliably attached location -
including another partition, drive or network storage.

Operation
---------

Once you've run buildout, you'll have ``bin/backup`` and ``bin/restore``
scripts in your buildout. Since all options are set via buildout, there are
few command-line options, and operation is generally as simple as using the
bare commands. ``bin/restore`` will accept a date-time argument if you're
keeping multiple backups. See the docs for details.

Backup operations may be run without stopping Plone. Restore operations
require that you stop Plone, then restart after the restore is complete.

``bin/backup`` is commonly included in a cron table for regular operation.
Make sure you test backup/restore before relying on it.

Incremental backups
-------------------

collective.recipe.backup offers both incremental and full backup and will
maintain multiple generations of backups. Tune these to meet your needs.

When incremental backup is enabled, doing a database packing operation will
automatically cause the next backup to be a full backup.

If your backup continuity needs are extreme, your incremental backup may be
equally extreme.
There are Plone installations where incremental backups are run every few minutes.
