---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(backend-zodb-label)=

# ZODB

The ZODB (Zope Object Database) is a Python-native, object-oriented database designed for direct persistence of Python objects.
Unlike traditional relational databases that rely on tables and SQL queries, ZODB allows developers to work directly with Python objects, persisting them without the need for object-relational mapping (ORM).


## Core Features of ZODB

- Transparent Persistence: Objects stored in ZODB automatically persist.
  In a Plone request/response cycle they do not require an explicit save or commit operation, since this is done automatically when the response is ready but before it is delivered.
- No schema constraints: Unlike relational databases, ZODB does not require predefined schemas, allowing for flexible and dynamic data structures.
  The attributes of the Python objects themselves are stored.
- ACID Compliance: ZODB ensures data consistency through transactions that support Atomicity, Consistency, Isolation, and Durability.
- Automatic Conflict Resolution: With its multi-version concurrency control (MVCC), ZODB can handle concurrent access efficiently.
- Built-in Versioning and Undo: The database allows versioning, enabling rollback to previous states if needed.
- Scalability: ZODB can be used in standalone applications or scaled with ZEO (ZODB Extension Objects) for distributed storage.
  Additionally, ZODB supports the RelStorage adapter, which allows it to use relational databases like PostgreSQL, MySQL, or Oracle as a backend, providing flexibility for integration with existing database infrastructures.

## How ZODB Works

At its core, ZODB operates as an object store, maintaining pickled Python objects with some metadata in a hierarchical structure.

- Storage: Handles how objects are stored.
  The default storage is FileStorage, which writes data to `.fs` files Filestorage does not scale, as only one process can work with it.
  ZEO (Zope Enterprise Objects) storage is used for distributed multi-client access to the same database, introducing scalability.
  Another highly scalable option is RelStorage, which allows ZODB to use relational databases like PostgreSQL, MySQL, or Oracle as backend storage, combining object persistence with traditional database infrastructure.
  RelStorage is used often in containerized deployment environment.

- Connection: Acts as the interface between Python applications and the database.
  With ZEO for each active Zope thread one connection is established.
  Connection are pooled and re-used.

- Transaction Manager: Manages transactional operations, ensuring data integrity.
  A transaction normally start with the requests and ends with the response.
  However, in long running requests with lots of database writes, the programmer can decide to commit actively in between.

- Append only behavior:
  The ZODB in general appends new transactions and keeps the old version of the object.
  Even on delete only the reference to the object is removed, the object itself is not touched.
  Exception here is RelStorage in history free mode, where actual data is overridden.

- Binary Large Objects (BLOBs) are files, images or similar larger objects.
  Those are handled special in ZODB.
  Either those are stored in a own tree of folders or in the database.
  Latter is recommended only for RelStorage, since FileStorage gets bloated and slow with many large objects.
  If the blobs are stored in the filesystem and ZEO is used, each ZEO client needs to mount the blob-storage folder-tree as a shared folder.
  There is an option to not configure ZEO with shared folders, but it is not recommended because of performance reasons.

- Any object that inherits from `Persistent` can be stored.
  Python objects are stored as a whole.
  To not store one large object they need to be divided.
  If an objet has an attribute which itself inherits from `Persistent` it is stored as a separate object in the ZODB.
  To divide lists and dicts into an objet for each value, there are `PersistentDict` and `PersistentList` classes.
  For larger structures the `BTree` package with its different optimized tree- and set-classes is generally used.
  Blobs are handled separately

- Low Level Indexing and Caching: Optimizes read and write operations for better performance.
  Tuning the ZODB-cache sizes to hardware-environment and the kind of data stored may help to speed up the application.

- Packing is the process of removing old versions of an object.
  This includes deleted objects.
  So even with the above mentioned history free RelStorage packing is needed to get rid of the deleted objects.
  The packing process needs to be started actively, either using the web interface (ZMI) or by starting a pack script.
  Usually this is done as a cron job.

## Further reading

More information can be found at the official [ZODB website](https://zodb.org)
