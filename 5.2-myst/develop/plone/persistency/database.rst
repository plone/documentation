=============
ZODB Database
=============

.. admonition:: Description

    Plone uses the ZODB object database to store its data.  The ZODB can act
    independently in-process, clustered over network or over another database
    engine, like SQL.


Introduction
============

Plone uses the ZODB database.  The ZODB happily stores any Python object with
any attributes |---| there is no need to write database schema or table
descriptions as there is
with SQL-based systems. If data models are described somehow
the descriptions are written in Python, usually using
``zope.schema`` package.

This chapter is about the basics of the ZODB, working with the ZODB database
directly, like tuning database settings.

More information about ZODB

* http://www.zodb.org/

* `Documentation <http://zodb.readthedocs.org/>`_

* `API documentation <http://zodb.readthedocs.org/en/latest/api.html>`_

Database files
==============

Usually Plone's database is configured to file ``var/filestorage/Data.fs``
and uploaded files can be found as BLOBs in ``var/blobstorage``.


Object database features
========================

The ZODB is an object database.  It makes very easy to store different kinds of
contentish data in a graph, supporting subclassing (something which SQL often
does poorly).

Since the database stores objects, and the objects are defined in Python code,
you always need the corresponding Python source code to instantiate the objects
stored inside the ZODB.  This might feel awkward at first, but you need to have
MySQL running to read what's inside MySQL files stored on your disk and so on ...

.. warning::

    The ZODB database is not usable without the Python source code used to
    create the data. The data is not readable using any SQL-based tools, and
    there exist little tools to deal with the raw data. The way to access Plone
    data is running Plone itself and performing queries through it.

.. warning::

    Since correct source code is needed to read ZODB data, this poses a problem
    for versioning. Even if you use the correct add-on product with proper
    source code, if the source code version is wrong, it might not work.  Data
    model attributes might be added, modified or deleted between source code
    revisions, making data operations on the existing database fail by raising
    Python exceptions (``AttributeError``, ``KeyError``).

To work around the ZODB interoperability problems, products like
*ore.contentmirror* exist to duplicate Plone content data to read-only SQL
database.

Query and searching
-------------------

ZODB does not provide query services as is
i.e. there is no SELECT statement.

Plone provides :doc:`cataloging </develop/plone/searching_and_indexing/catalog>`
service for this purpose.

This gives some benefits

* You define yourself how data is indexed

* The backend to perform queries is flexible - you
  can plug-in custom indexes

* portal_catalog default catalog is used for all content items
  to provide basic CMS functionality

* You can have optimized catalogs for specialized data (e.g. reference look-ups
  using reference_catalog)

Data model
----------

There is no hardwired way for describe
data in ZODB database.

Subclasses of ZODB ``persistent.Persistent``
class will have all their attributes and referred objects
written to the database using Python pickle mechanism.
Lists and dictionaries will be automatically
converted to persistent versions.

There are currently three primary ways to define data models in Plone

* Using zope.schema package (modern way) to describe Python object properties

* Using Archetypes content type subsystem (all Plone 3 content)

* Not defining the model, but relying on ad hoc object attributes

Read about :doc:`zope.schema </develop/plone/forms/schemas>`
how to define a model for the data to be stored
in ZODB database.

Transactions and committing
---------------------------

`This in-depth SO answer <http://stackoverflow.com/questions/11254384/when-to-commit-data-in-zodb/>`_
explains how committing works in ZODB.

* Savepoints and optimism regarding them

* PersistentList and list differences when saving data


Browsing
========

You can explore ZODB with-in Plone using `ZODBBrowser <https://plone.org/products/zodbbrowser>`_.

Packing database
================

As ZODB is append-only database it remembers all its history unless packed. Packing will erase undo history.

* `Why you need to regularly pack ZODB database to keep the performance up <http://www.sixfeetup.com/blog/optimize-your-plone-development-by-packing-the-zodb>`_

* `Packing is similar to VACUUM in PostgreSQL <http://stackoverflow.com/questions/11254384/when-to-commit-data-in-zodb/>`_

Packing through-the-web
-----------------------

Manual packing can be executed through Zope Control Panel (not Plone control panel)
in Zope application server root (not Plone site root) in the Management Interface.

Packing from command line
-------------------------

`plone.recipe.zeoserver <https://github.com/plone/plone.recipe.zeoserver/>`_ buildout recipe provides command called ``bin/zeopack``
inside buildout.
It allows you to trigger packing from the command line when Zope is clustered ZEO configuration.
``zeopack`` command runs against an on-line site.

This command is useful to run in cron to keep your Data.fs file growing forever.
You can control the number of days of history to be kept, etc., using buildout recipe variables.

More info

* https://github.com/plone/plone.recipe.zeoserver

Packing the database offline
----------------------------

`See this blog post <http://blog.twinapex.fi/2009/09/01/packing-and-copying-data-fs-from-production-server-for-local-development/>`_.

Example how to pack a copy of Data.fs in offline using Python snippet::

    import time
    import ZODB.FileStorage
    import ZODB.serialize

    storage=ZODB.FileStorage.FileStorage('/tmp/Data.fs.copy')
    storage.pack(time.time(),ZODB.serialize.referencesf)

As this depends on ZODB egg, the easiest way to run the snippet is to ``zopepy``
script from your ``buildout/bin`` folder::

    bin/zopepy pack.py

For more information, see :doc:`command-line scripts </develop/plone/misc/commandline>`.

Visualizing object graphs
=========================

* http://glicksoftware.com/blog/visualizing-the-zodb-with-graphviz

Cache size
==========

* `Understanding ZODB cache size option <https://mail.zope.org/pipermail/zodb-dev/2010-March/013199.html>`_

Integrity checks
================

Especially when you back-up a Data.fs file, it is useful to run integrity checks for the transferred files.

ZODB provides scripts ``fstest`` and ``fsrefs`` to check if Data.fs data is intact
and there are no problems due to low level disk corruption or bit flip.

* http://wiki.zope.org/ZODB/FileStorageBackup

.. note::

        It is recommended best practice to run integrity against your Data.fs regularly.
        This is the only way to detect corruption which would otherwise go unnoticed
        for a long time.

Restart and cache warm-up
=========================

Discussion why Plone is slow after restart

* https://mail.zope.org/pipermail/zodb-dev/2013-March/014935.html

Recovering old data
===================

Instructions for undoing deleted data and fixing broken databases.

* http://www.zopatista.com/plone/2008/12/18/saving-the-day-recovering-lost-objects


.. |---| unicode:: U+02014 .. em dash
