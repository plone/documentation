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

- Transparent Persistence: Objects stored in ZODB automatically persist. In a Ploe request/respone cycle they do not require an explicit save or commit operation, since this is done automatically.
- No Schema Constraints: Unlike relational databases, ZODB does not require predefined schemas, allowing for flexible and dynamic data structures.
  The attributes of the Python objects themselves are stored.
- ACID Compliance: ZODB ensures data consistency through transactions that support Atomicity, Consistency, Isolation, and Durability.
- Automatic Conflict Resolution: With its multi-version concurrency control (MVCC), ZODB can handle concurrent access efficiently.
- Built-in Versioning and Undo: The database allows versioning, enabling rollback to previous states if needed.
- Scalability: ZODB can be used in standalone applications or scaled with ZEO (ZODB Extension Objects) for distributed storage.
  Additionally, ZODB supports the RelStorage adapter, which allows it to use relational databases like PostgreSQL, MySQL, or Oracle as a backend, providing flexibility for integration with existing database infrastructures.

## How ZODB Works

At its core, ZODB operates as an object store, maintaining pickled Python objects with some metadata in a hierarchical structure.

- Storage: Handles how objects are stored on disk or in-memory.
  The default storage is FileStorage, which writes data to `.fs` files Filestorage does not scale, as only one process can work with it.
  ZEO (ZODB Extension Objects) storage is used for distributed multi-client access to the same database, introducing scalability.
  Another highly scalable option is RelStorage, which allows ZODB to use relational databases like PostgreSQL, MySQL, or Oracle as backend storage, combining object persistence with traditional database infrastructure.
  RelStorage is used often in containerized deployment environment.

- Connection: Acts as the interface between Python applications and the database.
  With ZEO for each active Zope thread one connection is established.
  Connection are pooled and re-used.

- Transaction Manager: Manages transactional operations, ensuring data integrity.
  A transaction normally start with the requests and ends with the respsonse.
  However, in long running requests with lots of database writes, transactions can be committed in between.

- Indexing and Caching: Optimizes read and write operations for better performance.
  Tuning the ZODB-cache sizes to hardware-environment and the kind of data stored may help to speed up the application.

## Further reading

More information can be found at the official [ZODB.org] website (https://zodb.org)