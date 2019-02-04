===============================
Migrating Plone 5.2 to Python 3
===============================


.. admonition:: Description

   Instructions and tips for running Plone 5.2 with Python 3


Make custom packages Python 3 ready
===================================

Principles
----------

* You should support Python 2 and 3 with the same codebase to allow it to be used in existing versions of Plone.
* Plone 5.2 supports Python 2.7, Python 3.6 and Python 3.7
* We use `six <https://six.readthedocs.io>`_ and
  `modernize <https://pypi.python.org/pypi/modernize>`_ to do the first steps towards Python 3.

First steps of add-ons
----------------------

#. Prepare add-on to be ported, i.e. add it to a buildout running Plone 5.2 on Python 3
#. Install modernize and run it on the code
#. Use precompile to find syntax errors
#. Start the instance and find more errors like import errors
#. Run and fix all tests
#. Update package information

1. Preparation
--------------

In the GitHub repo of the add-on:

* Open a ticket with the title "Add support for Python 3" .
* Create a new branch named ``python3``.

Until Plone 5.2 is released, you can use the coredev buildout setup.
It contains everything for porting an add-on to Python 3.
Follow these steps:

.. code-block:: shell

    # Clone coredev and use branch 5.2:
    git clone git@github.com:plone/buildout.coredev.git coredev_py3
    cd coredev_py3
    git checkout 5.2
    # Create a py3 virtual environment with either Python 3.6 or 3.7 (they are very similar):
    python3.7 -m venv .
    # Install buildout:
    ./bin/pip install -r requirements.txt


Next create a file called ``local.cfg`` in the root of the buildout.
This file will be used to add your add-on to the buildout.
Add your package like in the following example.
Exchange ``collective.package`` with the name of the add-on you want to port.

.. note::

    This example expects a branch with the name ``python3`` to exist for the package.
    Adapt it for your use case.

.. code-block:: ini

    [buildout]
    extends = buildout.cfg

    always-checkout = true

    custom-eggs +=
        collective.package

    test-eggs +=
        collective.package [test]

    auto-checkout +=
        collective.package

    [sources]
    collective.package = git git@github.com:collective/collective.package.git branch=python3

With the file in place, run buildout.
Then the source of the add-on package will be checked out into the ``src`` folder.

.. code-block:: shell

    ./bin/buildout -c local.cfg

Now everything is prepared to work on the migration of the package.

2. Automated fixing with modernize
----------------------------------

``python-modernize`` is a utility that automatically prepares Python 2 code for porting to Python 3.
After running ``python-modernize``, there is manual work ahead.
There are some problems that ``python-modernize`` can not fix on its own.
It also might make changes that are not really needed.
You need to closely review all changes after you run this tool.

``python-modernize`` will warn you,
when it is not sure what to do with a possible problem.
Check this `Cheat Sheet <http://python-future.org/compatible_idioms.html>`_  with idioms
for writing Python 2-3 compatible code.

``python-modernize`` adds an import of the compatibility library ``six`` if needed.
The import is added as the last import,
therefore it is often necessary to reorder the imports.
The easiest way is to use ``isort``.
Check the `Python Styleguide for Plone <https://docs.plone.org/develop/styleguide/python.html#grouping-and-sorting>`_
for information about the order of imports and an example config for ``isort``.


Installation
~~~~~~~~~~~~

Install `modernize <https://pypi.python.org/pypi/modernize>`_ into your Python 3 environment with ``pip``.

.. code-block:: shell

    ./bin/pip install modernize

Usage
~~~~~

The following command runs an import fixer on all Python files.

.. code-block:: shell

    ./bin/python-modernize -x libmodernize.fixes.fix_import  src/collective.package

.. note::

    The ``-x`` option is used to exclude certain fixers.
    The one that adds ``from __future__ import absolute_import`` should not be used.
    See ``./bin/python-modernize -l`` for a complete list of fixers and
    the `Documentation <https://python-modernize.readthedocs.io/en/latest/fixers.html>`_ about them.

The following commands applies all fixes to the files:

.. code-block:: shell

    ./bin/python-modernize -wn -x libmodernize.fixes.fix_import  src/collective.package

You can use ``isort`` to fix the order of imports:

.. code-block:: shell

    ./bin/isort src/collective.package

After you run the command above, you can fix what ``modernizer`` did not get right.

3. Use precompile
-----------------

You can make use of `plone.recipe.precompiler <https://github.com/plone/plone.recipe.precompiler>`_ to identify syntax errors quickly.
This recipe compiles all Python code already at buildout-time, not at run-time.
You will see right away when there is some illegal syntax.

Add the following line to the section ``[buildout]`` in ``local.cfg``.
Then run ``./bin/buildout -c local.cfg`` to enable and use ``precompile``.

.. code-block:: ini

    parts += precompiler

4. Start the instance
---------------------

As a next step we recommend that you try to start the instance with your add-on.
This will fail on all import errors (e.g. relative imports that are not allowed in Python 3).
If it works you can try to install the add-on.
You need to fix all issues that appear and do some preliminary manual testing to check for big, obvious issues.

5. Run tests
------------

.. code-block:: shell

    $ ./bin/test --all -s collective.package

Hopefully there are not many issues with the code left at this point.

TBD: Document the most frequent issues when porting to Python 3


.. seealso::

    Here is a list of helpful references on the topic of porting Python 2 to Python 3.

    - https://portingguide.readthedocs.io/en/latest/index.html
    - https://eev.ee/blog/2016/07/31/python-faq-how-do-i-port-to-python-3/
    - http://getpython3.com/diveintopython3/
    - https://docs.djangoproject.com/en/1.11/topics/python3/
    - https://docs.ansible.com/ansible/latest/dev_guide/developing_python_3.html
    - https://docs.python.org/2/library/doctest.html#debugging


6. Update add-on information
----------------------------

Add the following three entries of the classifiers list in setup.py:

.. code-block:: python

    "Framework :: Plone :: 5.2",
    ...
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",

Make an entry on the CHANGES.rst file.


7. Create a test-setup that tests in Python 2 and Python 3
----------------------------------------------------------

TBD: Run tests on with `tox` on travis for Python 2.7, 3.6 and 3.7

A example for a tox-setup can be found in https://github.com/collective/collective.ifttt/pull/82


Database Migration
==================

.. note::

   This is work in progress. To continue with documenting the process or help improve the involved scripts/tools
   please have a look at the following resources:

   * Provide Migration-Story for ZODB with Plone from Python 2 to 3: https://github.com/plone/Products.CMFPlone/issues/2525

   * Documentation on setting up an environment to test the migration:
     https://github.com/frisi/coredev52multipy/tree/zodbupdate

Plone 5.2 can be run on Python 2 and Python 3.
To use an existing project in Python 3, you need to `migrate your database <https://github.com/zopefoundation/zodbupdate/issues/11>`_ first.

ZODB itself is compatible with Python 3 but a DB created in Python 2.7 cannot be used in Python 3 without being modified before.
(See `Why do I have to migrate my database?`_ for technical background).


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
--------

This step actually requires to take your site offline or into read-only mode.


Some thoughts on doing upgrades w/o downtime that came up in a hangout during a coding sprint in October 2018:


- jim mentions downtime. would try to leverage the zrs replication protocol, secondary server with converted data.
  It would probably be a trivial change to zrs.
- for relstorage jim mentions a zrs equivalent for relstorage: http://www.newtdb.org/en/latest/topics/following.html
- david thought out loud about taking down downtime: do conversion at read time....



Prepare the migration
---------------------

If you have custom content types and add-ons, it is a good idea to first test the migration on a staging server.


Analyze existing objects in the ZODB and list classes with missing `[zodbupdate.decode]` mapping for attributes containing string values that could possibly break when converted to python3.

.. code-block:: bash

    bin/zodb-py3migrate-analyze py2/var/filestorage/Data.fs -b py2/var/blobstorage -v
    # this might be possible with zodbupdate (https://github.com/zopefoundation/zodbupdate/issues/10)



Test Migration
--------------

You can use the following command to check, that all records in the database can be successfully loaded.

.. code-block:: bash

    bin/instance verifydb

The output should look like this::

    ...
    INFO:zodbverify:Scanning ZODB...
    INFO:zodbverify:Done! Scanned 5999 records. Found 0 records that could not be loaded.
