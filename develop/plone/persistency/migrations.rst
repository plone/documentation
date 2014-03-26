=================
 Migrations
=================

Database migrations are needed if your internal data storage format
changes between versions.

ZODB does not require you to set object format explicitly,
like in SQL you need to create table schema. However,
your code will naturally fail if the data format of the object
is unexpected.

* `Changing instance attributes <http://www.zodb.org/documentation/guide/prog-zodb.html#changing-instance-attributes>`_
