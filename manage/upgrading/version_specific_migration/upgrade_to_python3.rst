===============================
Migrating Plone 5.2 to Python 3
===============================


.. admonition:: Description

   Instructions and tips for running Plone 5.2 with Python 3

.. note::

   This is work in progress. To continue with documenting the process or help improve the involved scripts/tools
   please have a look at the following resources:

   * https://github.com/plone/Products.CMFPlone/issues/2525

   * documentation on setting up an environment to test the migration:
     https://github.com/frisi/coredev52multipy/tree/zodbupdate


Plone 5.2 can be ran on Python 2 and Python 3. To use Python 3 you need to `migrate your database <https://github.com/zopefoundation/zodbupdate/issues/11>`_ first.



Make custom packages Python 3 ready
===================================

XXX @pbauer has some documentation on this in google docs




Database Migration
==================


ZODB itself is compatible with Python 3 but a DB created in Python 2.7 cannot be used in Python 3 without being modified before.
(See `Why do i have to migrate my database?`_ for technical background).


Database Upgrade procedure
--------------------------

TODO: provided sections for these steps that explain them in more detail.


* Upgrade your site to Plone 5.2 running on Python 2 first
  (see :doc:`upgrade_to_52`)

* Backup your database!

* Run scripts to prepare the content for migration
  `https://github.com/plone/Products.CMFPlone/issues/2575 <https://github.com/plone/Products.CMFPlone/issues/2575>`_


* Migrate your database using zodbupdate

  - add script to buildout

  - run it



* Testing / Debugging




Why do i have to migrate my database?
-------------------------------------

To understand the problem that arises when migrating a zodb from python2 to python3,
this `introduction <https://blog.gocept.com/2018/06/07/migrate-a-zope-zodb-data-fs-to-python-3/>`_ and the following example will help.


When pickling an object the datatypes and values are stored.

Python2 strings get STRING, and unicode gets UNICODE

::

    $ python2
    Python 2.7.14 (default, Sep 23 2017, 22:06:14)
    >>> di=dict(int=23,str='Ümläut',unicode=u'Ümläut')
    >>> di
    {'int': 23, 'unicode': u'\xdcml\xe4ut', 'str': '\xc3\x9cml\xc3\xa4ut'}
    >>> import pickle
    >>> import pickletools
    >>> pickletools.dis(pickle.dumps(di))
        0: (    MARK
        1: d        DICT       (MARK at 0)
        2: p    PUT        0
        5: S    STRING     'int'
       12: p    PUT        1
       15: I    INT        23
       19: s    SETITEM
       20: S    STRING     'unicode'
       31: p    PUT        2
       34: V    UNICODE    u'\xdcml\xe4ut'
       42: p    PUT        3
       45: s    SETITEM
       46: S    STRING     'str'
       53: p    PUT        4
       56: S    STRING     '\xc3\x9cml\xc3\xa4ut'
       80: p    PUT        5
       83: s    SETITEM
       84: .    STOP
    highest protocol among opcodes = 0

Python3 does not allow non-ascii characters in bytes and the pickle declares
the byte string as SHORT_BINBYTES and the string (py2 unicode) as BINUNICODE

::

    $ python3
    Python 3.6.3 (default, Oct  3 2017, 21:45:48)
    >>> di=dict(int=23,str=b'Ümläut',unicode='Ümläut')
      File "<stdin>", line 1
    SyntaxError: bytes can only contain ASCII literal characters.
    >>> di=dict(int=23,str=b'Umlaut',unicode='Ümläut')
    >>> di
    {'int': 23, 'str': b'Umlaut', 'unicode': 'Ümläut'}
    >>> import pickle
    >>> import pickletools
    >>> pickletools.dis(pickle.dumps(di))
        0: \x80 PROTO      3
        2: }    EMPTY_DICT
        3: q    BINPUT     0
        5: (    MARK
        6: X        BINUNICODE 'int'
       14: q        BINPUT     1
       16: K        BININT1    23
       18: X        BINUNICODE 'str'
       26: q        BINPUT     2
       28: C        SHORT_BINBYTES b'Umlaut'
       36: q        BINPUT     3
       38: X        BINUNICODE 'unicode'
       50: q        BINPUT     4
       52: X        BINUNICODE 'Ümläut'
       65: q        BINPUT     5
       67: u        SETITEMS   (MARK at 5)
       68: .    STOP
    highest protocol among opcodes = 3


When reading a pickle created with python2 with python3 that contains non-ascii
characters in a field declared with OPTCODE `STRING` python3 is trying to interpret it as python3 string (py2 unicode)
and we might end up getting a UnicodeDecodeError for this pickle in ZODB.serialize


.. code-block:: bash

    $ python3
    >>> b'\xc3\x9cml\xc3\xa4ut'.decode('ascii')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 0: ordinal not in range(128)


Or when utf-8 encoded byte-strings are interpreted as unicode we do not get an error but mangled non-ascii characters

.. code-block:: bash

    $ python3
    >>> print('\xdcml\xe4ut')
    Ümläut
    >>> print('\xc3\x9cml\xc3\xa4ut')
    ÃmlÃ¤ut




Custom Content Types
--------------------

TODO: Not yet sure if custom types need to provide additional mappings for zodbupdate.

Here is an example Pull Request that adds them: `https://github.com/zopefoundation/Products.PythonScripts/pull/19 <https://github.com/zopefoundation/Products.PythonScripts/pull/19>`_

workflow: analyze, read sourcecode, add pdb to see which values are passed to attribute to decide whether to use bytes or utf-8

.. code-block:: bash

    bin/zodb-py3migrate-analyze py2/var/filestorage/Data.fs -b py2/var/blobstorage -v



Migrate Database using zodbupdate
---------------------------------

add zodbupdate to buildout eggs::

    [zodbupdate]
    recipe = zc.recipe.egg
    eggs =
        ${buildout:eggs}
        zodbupdate
        zodb.py3migrate

    scripts =
        zodb-py3migrate-analyze
        zodbupdate



Migrate database so it can be read using Python 3.

.. warning::

    This migrates our database in place. Make sure to make a backup before!

.. code-block:: bash

    cd $BUILDOUT
    bin/instance stop
    cp var/filestorage/Data.fs var/filestorage/Data.fs-back
    bin/zodbupdate --pack --convert-py3 --file var/filestorage/Data.fs



Downtime
''''''''

This step actually requires to take your site offline or into read-only mode.


Some thoughts on doing upgrades w/o downtime that came up in a hangout during a coding sprint in October 2018:


- jim mentions downtime. would try to leverage the zrs replication protocol, secondary server with converted data.
  It would probably be a trivial change to zrs.
- for relstorage jim mentions a zrs equivalent for relstorage: http://www.newtdb.org/en/latest/topics/following.html
- david thought out loud about taking down downtime: do conversion at read time....



Prepare the migration
---------------------

If you have custom content types and addons, it is a good idea to first test the migration on a staging server.


Analyze existing objects in the ZODB and list classes with missing `[zodbupdate.decode]` mapping for attributes containing string values that could possibly break when converted to python3

.. code-block:: bash

    bin/zodb-py3migrate-analyze py2/var/filestorage/Data.fs -b py2/var/blobstorage -v
    # this might be possible with zodbupdate (https://github.com/zopefoundation/zodbupdate/issues/10)



Test Migration
--------------

- analyze the database to make sure all records can be opened when running python 3
