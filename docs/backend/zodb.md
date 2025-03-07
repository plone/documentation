---
myst:
  html_meta:
    "description": "Zope Object Database (ZODB)"
    "property=og:description": "Zope Object Database (ZODB)"
    "property=og:title": "Zope Object Database (ZODB)"
    "keywords": "Plone, ZODB, Zope Object Database, RelStorage, ZEO, ZODB Extension Objects"
---

% TODO: Diátaxis conceptual guide

(backend-zodb-label)=

# Zope Object Database (ZODB)

The {term}`Zope Object Database` (ZODB) is a Python native, object-oriented database designed for direct persistence of Python objects.
Unlike traditional relational databases that rely on tables and SQL queries, ZODB allows developers to work directly with Python objects, persisting them without the need for object-relational mapping (ORM).


## Core features of ZODB

Transparent persistence
: Objects stored in ZODB automatically persist.
  In a Plone request/response cycle, they do not require an explicit save or commit operation, since this is done automatically.

No schema constraints
: Unlike relational databases, ZODB does not require predefined schemas, allowing for flexible and dynamic data structures.
  The attributes of the Python objects themselves are stored.

ACID compliance
: ZODB ensures data consistency through transactions that support atomicity, consistency, isolation, and durability (ACID).

Automatic conflict resolution
: With its multi-version concurrency control (MVCC), ZODB can handle concurrent access efficiently.

Built-in versioning and undo
: The database allows versioning, enabling rollback to previous states if needed.

Scalability
: ZODB can be used in standalone applications or scaled with {term}`ZODB Extension Objects` (ZEO) for distributed storage.
  Additionally, ZODB supports the {term}`RelStorage` adapter, which allows it to use relational databases, including PostgreSQL, MySQL, or Oracle, as a backend, providing flexibility for integration with existing database infrastructures.


## How ZODB works

At its core, ZODB operates as an object store, maintaining serialized Python objects with some metadata in a hierarchical structure.

Storage
: Handles how objects are stored on disk or in-memory.

  The default storage is {term}`FileStorage`, which writes data to `.fs` files. `FileStorage` does not scale, as only one process can work with it.

  {term}`ZEO` storage is used for distributed multi-client access to the same database, introducing scalability.

  {term}`RelStorage` is another highly scalable option.
  It allows ZODB to use relational databases like PostgreSQL, MySQL, or Oracle as backend storage, combining object persistence with traditional database infrastructure.
  RelStorage is used often in a containerized deployment environment.

Connection
: Acts as the interface between Python applications and the database.
  With ZEO for each active Zope thread, one connection is established.
  Connections are pooled and re-used.

Transaction manager
: Manages transactional operations, ensuring data integrity.
  A transaction normally starts with the request, and ends with the response.
  However, in long-running requests with lots of database writes, transactions can be committed in between.

Indexing and caching
: Optimizes read and write operations for better performance.
  Tuning the ZODB cache sizes to hardware environment and the kind of data stored may help to speed up the application.


## Further reading

More information can be found at the official [ZODB website](https://zodb.org/en/latest/).
