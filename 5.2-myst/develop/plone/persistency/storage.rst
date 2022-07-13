=======
Storage
=======

.. admonition:: Description

        What kind of different storages (storing backends) ZODB has and how to use them.


Introduction
------------

This page explains the details how data is stored in the ZODB.
The information here is important to understand Plone's database behavior and how to optimize your application.

Pickling
--------

ZODB is an object oriented database. All data in the ZODB are stored as `pickled Python objects <http://docs.python.org/library/pickle.html>`_.
Pickle is the object serialization module in Pythons standard library.

* Each time an object is read and it is not cached, object is read from the ZODB data storage and unpickled

* Each time an object is written, it is pickled and transaction machinery appends it to the ZODB data storage

Pickle format is a series of bytes. Here is an example what it looks like::

	>>> import pickle
	>>> data = { "key" : "value" }
	>>> pickled = pickle.dumps(data)
	>>> print pickled
	(dp0
	S'key'
	p1
	S'value'
	p2
	s.

It is not a very human readable format.

Even if you use SQL based `RelStorage <https://pypi.python.org/pypi/RelStorage/>`_ ZODB backends, the objects are still pickled to the database;
SQL does not support varying table schema per row and Python objects do not have fixed schema format.

Binary trees
------------

Data is usually organized to binary trees or `BTrees <http://wiki.zope.org/ZODB/guide/node6.html>`_ .
More specifically, data is usually stored as Object Oriented Binary Tree
`OOBtree <http://docs.zope.org/zope3/Code/BTrees/OOBTree/OOBTree/index.html>`_
which provides a Python object as key and Python object value mappings. Key is the object id in the parent container as a string, and value is any pickleable Python object or primitive you store in your database.

`ZODB data structure interfaces <https://github.com/zopefoundation/BTrees/blob/master/BTrees/Interfaces.py>`_.

`Using BTrees example from Zope Docs <http://www.zodb.org/en/latest/documentation/articles/ZODB2.html#using-btrees>`_.

Buckets
-------

BTree stores data in buckets (`OOBucket <http://docs.zope.org/zope3/Code/BTrees/OOBTree/OOBucket/index.html>`_).

A Bucket is the smallest unit of data which is written to the database once.
Buckets are loaded lazily: BTree only loads buckets storing values of keys being accessed.

BTree tries to put as much data as possible into one bucket.
When one value in a bucket is changed, the whole bucket must be rewritten to the disk.

`Default bucket size is 30 objects <https://github.com/zopefoundation/BTrees/blob/master/BTrees/_OOBTree.c#L27>`_.

Storing as attribute vs. storing in BTree
-----------------------------------------

Plone has two kinds of fundamental way to store data:

* Attribute storage (stores values directly in the pickled objects).

* Annotation storage (OOBTree based). Plone objects have attribute __annotations__ which is an OOBtree for storing objects in a name-conflict free way.

When objects are stored in the annotation storage, reading object values needs at least one extra database look up to load the first bucket of the OOBTree.

If the value is going to be used frequently, and especially if it is read when viewing the content object, storing it in an attribute is more efficient than storing it in an annotation.
This is because the __annotations__ BTree is a separate persistent object which has to be loaded into memory, and may push something else out of the ZODB cache.

If the attribute stores a large value, it will increase memory usage, as it will be loaded into memory each time the object is fetched from the ZODB.

BLOBs
-----

BLOBs are large binary objects like files or images.

BLOBs are supported since ZODB 3.8.x.

When you use BLOB interface to store and retrieve data, they are stored physically as files on your file systems.
A file system, as the name says, was designed to handle files and has far better performance on large binary data than sticking the data into ZODB.

BLOBs are streamable which means that you can start serving the file from the beginning of the file to HTTP wire without needing to buffer the whole data to the memory first (slow).

SQL values
----------

Plone's Archetypes subsystem supports storing individual Archetypes fields in SQL database.
This is mainly `an integration feature <http://plone.293351.n2.nabble.com/Work-with-Contents-in-SQL-database-td5868800.html>`_. Read more about this in `Archetypes manual <https://plone.org/products/archetypes/documentation/old/ArchetypesDeveloperGuide/index_html#advanced-storage-manual>`_.

Transaction sizes
-----------------

Discussion pointers

* http://www.mail-archive.com/zodb-dev@zope.org/msg03398.html

Analysing Data.fs content offline
-----------------------------------

* https://plone.org/documentation/kb/debug-zodb-bloat
