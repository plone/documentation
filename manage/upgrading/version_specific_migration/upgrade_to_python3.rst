===============================
Migrating Plone 5.2 to Python 3
===============================


.. admonition:: Description

   Instructions and tips for porting Plone projects to Python 3


Make Custom Packages Python 3 Ready
===================================

Principles
----------

* You should support Python 2 and 3 with the same codebase to allow it to be used in existing versions of Plone.
* Plone 5.2 supports Python 2.7, Python 3.6, and Python 3.7.
* We use `six <https://six.readthedocs.io>`_ and `modernize <https://pypi.python.org/pypi/modernize>`_ to do the first steps towards Python 3.

In general you should follow these steps to port add-ons:

#. Prepare ``buildout`` for the add-on to be ported.
#. Update code with `python-modernize <https://python-modernize.readthedocs.io/en/latest/>`_.
#. Use `plone.recipe.precompiler <https://github.com/plone/plone.recipe.precompiler>`_ (also called ``precompiler`` for brevity) to find syntax errors.
#. Start the instance and find more errors.
#. Test functionality manually.
#. Run and fix all tests.
#. Update package information.


1 Preparation
-------------

In the GitHub repository of the add-on:

* Open a ticket with the title "Add support for Python 3".
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
Add your package as in the following example.
Exchange ``collective.package`` with the name of the add-on you want to port.

.. note::

    This example expects a branch with the name ``python3`` to exist for the package.
    Adapt it for your use case.

.. code-block:: ini

    [buildout]
    extends = buildout.cfg

    always-checkout = true
    allow-picked-versions = true

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

.. note::

    You can also add some development-tools like ``Products.PDBDebugMode`` and ``plone.reload`` to your buildout.
    For some you currently need a source checkout though.

    .. code-block:: ini

        custom-eggs +=
            collective.package
            Products.PDBDebugMode
            Products.PrintingMailHost
            plone.reload

        test-eggs +=
            collective.package [test]

        auto-checkout +=
            collective.package
            Products.PDBDebugMode

        [sources]
        Products.PDBDebugMode = git ${remotes:collective}/Products.PDBDebugMode.git pushurl=${remotes:collective_push}/Products.PDBDebugMode.git branch=master

        [versions]
        Products.PrintingMailHost = 1.1.1

.. code-block:: shell

    ./bin/buildout -c local.cfg

Now everything is prepared to work on the migration of the package.

For small packages or packages that have few dependencies, it is a good idea to try starting your instance now.

.. code-block:: shell

    ./bin/instance fg

If it does not start up, you should continue with the next steps instead of trying to fix each issue as it appears.


2 Automated Fixing With Modernize
---------------------------------

``python-modernize`` is a utility that automatically prepares Python 2 code for porting to Python 3.
After running ``python-modernize``, there is manual work ahead.
There are some problems that ``python-modernize`` can not fix on its own.
It also can make changes that are not really needed.
You need to closely review all changes after you run this tool.

``python-modernize`` will warn you, when it is not sure what to do with a possible problem.
Check this `Cheat Sheet <http://python-future.org/compatible_idioms.html>`_  with idioms for writing Python 2/3 compatible code.

``python-modernize`` adds an import of the compatibility library ``six`` if needed.
The import is added as the last import, therefore it is often necessary to reorder the imports.
The easiest way is to use `isort <https://pypi.python.org/pypi/isort>`_, which does this for you automatically.
Check the `Python style guide for Plone <https://docs.plone.org/develop/styleguide/python.html#grouping-and-sorting>`_ for information about the order of imports and an example configuration for ``isort``.

If ``six`` is used in the code, make sure that ``six`` is added to the ``install_requires`` list in the ``setup.py`` of the package.

Installation
~~~~~~~~~~~~

Install ``modernize`` into your Python 3 environment with ``pip``.

.. code-block:: shell

    ./bin/pip install modernize

Install ``isort`` into your Python 3 environment with ``pip``.

.. code-block:: shell

    ./bin/pip install isort


Usage
~~~~~

The following command runs an import fixer on all Python files.

.. code-block:: shell

    ./bin/python-modernize -x libmodernize.fixes.fix_import  src/collective.package

.. note::

    The ``-x`` option is used to exclude certain fixers.
    The one that adds ``from __future__ import absolute_import`` should not be used.
    See ``./bin/python-modernize -l`` for a complete list of fixers and the `fixers documentation <https://python-modernize.readthedocs.io/en/latest/fixers.html>`_.

The following command applies all fixes to the files:

.. code-block:: shell

    ./bin/python-modernize -wn -x libmodernize.fixes.fix_import  src/collective.package

You can use ``isort`` to fix the order of imports:

.. code-block:: shell

    ./bin/isort src/collective.package

After you run the command above, you can fix what ``modernizer`` did not get right.

3 Use ``precompiler``
---------------------

You can make use of ``plone.recipe.precompiler`` to identify syntax errors quickly.
This recipe compiles all Python code already at buildout-time, not at run-time.
You will see right away when there is some illegal syntax.

Add the following line to the section ``[buildout]`` in ``local.cfg``.
Then run ``./bin/buildout -c local.cfg`` to enable and use ``precompiler``.

.. code-block:: ini

    parts += precompiler

``precompile`` will be run every time you run buildout.
If you want to avoid running the complete buildout every time, you can use the ``install`` keyword of buildout like this as a shortcut:

.. code-block:: shell

    ./bin/buildout -c local.cfg  install precompiler


4 Start The Instance
---------------------

As a next step we recommend that you try to start the instance with your add-on.
This will fail on all import errors (e.g., relative imports that are not allowed in Python 3).
If it works then you can try to install the add-on.

You need to fix all issues that appear before you can do manual testing to check for big, obvious issues.


Common Issues during startup
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following issues will abort your startup.
You need to fix them before you are able to test the functionality by hand or run tests.


A - Class Advice
^^^^^^^^^^^^^^^^

This kind of error message:

.. code-block:: shell

    TypeError: Class advice impossible in Python3.  Use the @implementer class decorator instead.

tells you that there is a class that is using an ``implements`` statement which needs to be replaced by the ``@implementer`` decorator.

For example, code that is written as follows:

.. code-block:: python

    from zope.interface import implements

    class Group(form.BaseForm):
        implements(interface.IGroup)

needs to be replaced with:

.. code-block:: python

    from zope.interface import implementer

    @implementer(interfaces.IGroup)
    class Group(form.BaseForm):

The same is the case for ``provides(IFoo)`` and some other Class advices.
These need to be replaced with their respective decorators like ``@provider``.


B - Relative Imports
^^^^^^^^^^^^^^^^^^^^

Relative imports like ``import permissions`` are no longer permitted.
Use ``from collective.package import permissions`` or ``from . import permissions`` (not recommended).


C - Syntax Error On Importing Async
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

In Python 3.7 you can no longer have a module called ``async`` (see https://github.com/celery/celery/issues/4849).
You need to rename all such files, folders or packages (like ``zc.async`` and ``plone.app.async``).


5 Test functionality manually
-----------------------------

Now that the instance is running you should do the following and fix all errors as they appear.

* Install the add-on.
* Test basic functionality (e.g., adding and editing content-types and views).
* Uninstall the add-on.

For this step you should have ``Products.PDBDebugMode`` installed.
It will make fixing any issues much easier.


6 Run Tests
------------

.. code-block:: shell

    $ ./bin/test --all -s collective.package

Remember that you can run ``./bin/test -s collective.package -D`` to enter a pdb session when an error occurs.

With some luck, there will not be too many issues left with the code at this point.

It you are unlucky then you have to fix Doctests.
These should be changed so that Python 3 is the default.
For example, string types (or text) should be represented as ``'foo'``, not ``u'foo'``, and bytes types (or data) should be represented as ``b'bar'``, not ``'bar'``.
Search for examples of ``Py23DocChecker`` in Plone's packages to find a pattern which allows updated doctests to pass in Python 2.

*   Test your code against `buildout.coredev on Jenkins <https://jenkins.plone.org/view/Add-ons/>`_.
*   Note there are jobs set up for Plone 4.3, 5.1, and 5.2 on Python 2, and two jobs that run tests for Plone 5.2 on Python 3.6 and Python 3.7.
*   Log in to the Jenkins website (top right) and click on the job you want to run.
*   Choose the link "Build with parameters" in the left menu on the left-hand side.
*   Fill the fields "ADDON_URL" and "ADDON_BRANCH" with your repository's URL and the branch name ("python3" if you followed these instructions).
*   Start the build with the "Build" button.


7 Update Add On Information
---------------------------

Add the following three entries of the classifiers list in setup.py:

.. code-block:: python

    "Framework :: Plone :: 5.2",
    # ...
    "Programming Language :: Python :: 3.6",
    "Programming Language :: Python :: 3.7",

Make an entry in the ``CHANGES.rst`` file.


8 Create A Test Setup That Tests In Python 2 And Python 3
----------------------------------------------------------

TBD: Run tests with ``tox`` on Travis for Python 2.7, 3.6, and 3.7.

An example for a ``tox`` setup can be found in https://github.com/collective/collective.ifttt/pull/82.


9 Frequent Issues
-----------------

Text and Bytes
~~~~~~~~~~~~~~

This is by far the biggest issue when porting to Python 3.
Read https://portingguide.readthedocs.io/en/latest/strings.html to be prepared.

As a rule of thumb, you can assume that in Python 3 everything should be text.
Only in very rare cases you need to handle bytes.

``python-modernize`` will **not** fix all your text/bytes issues.
It only replaces all cases of ``unicode`` with ``six.text_type``.
You need to make sure that the code you are porting will remain unchanged in Python 2 and (at least in most cases) use text in Python 3.

Try to modify the code in such a way that when dropping support for Python 2 you will be able to delete while lines.
For example:

.. code-block:: python

   if six.PY2 and isinstance(value, six.text_type):
       value = value.encode('utf8')
   do_something(value)

You can use the helper methods ``safe_text`` and ``safe_bytes`` (``safe_unicode`` and ``safe_encode`` in Plone 5.1).

``python-modernize`` also does not touch the import statement ``from StringIO import StringIO`` even though this works only in Python 2.
You have to check whether you are dealing with text or binary data and use the appropriate import statement from ``six`` (https://pythonhosted.org/six/#six.StringIO).

.. code-block:: python

    # For textual data
    from six import StringIO
    # For binary data
    from six import BytesIO

.. seealso::

    Here is a list of helpful references on the topic of porting Python 2 to Python 3.

    - https://portingguide.readthedocs.io/en/latest/index.html
    - https://eev.ee/blog/2016/07/31/python-faq-how-do-i-port-to-python-3/
    - http://getpython3.com/diveintopython3/
    - https://docs.djangoproject.com/en/1.11/topics/python3/
    - https://docs.ansible.com/ansible/latest/dev_guide/developing_python_3.html
    - https://docs.python.org/2/library/doctest.html#debugging


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

ZODB itself is compatible with Python 3 but a DB created in Python 2.7 cannot be used in Python 3 without modifying it before.
(See `Why do I have to migrate my database?`_ for technical background).


Database Upgrade Procedure
--------------------------

TODO: provided sections for these steps that explain them in more detail.


* Upgrade your site to Plone 5.2 running on Python 2 first
  (see :doc:`upgrade_to_52`)

* Backup your database!

* Run scripts to prepare the content for migration
  `https://github.com/plone/Products.CMFPlone/issues/2575 <https://github.com/plone/Products.CMFPlone/issues/2575>`_


* Migrate your database using zodbupdate

  - Add script to buildout

  - Run it



* Testing / Debugging



Why Do I Have To Migrate My Database
-------------------------------------

To understand the problem that arises when migrating a ZODB from Python2 to Python3,
this `introduction <https://blog.gocept.com/2018/06/07/migrate-a-zope-zodb-data-fs-to-python-3/>`_ and the following example will help.


When pickling an object the datatypes and values are stored.

Python2 strings get STRING, and Unicode gets UNICODE

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


Python3 will wrongly interpret a pickle created with Python2 that contains non-ascii characters in a field declared with OPTCODE `STRING`.
In that case we may end up with a UnicodeDecodeError for this pickle in ZODB.serialize


.. code-block:: bash

    $ python3
    >>> b'\xc3\x9cml\xc3\xa4ut'.decode('ascii')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 0: ordinal not in range(128)


Or when UTF-8 encoded byte-strings are interpreted as Unicode we do not get an error but mangled non-ascii characters

.. code-block:: bash

    $ python3
    >>> print('\xdcml\xe4ut')
    Ümläut
    >>> print('\xc3\x9cml\xc3\xa4ut')
    ÃmlÃ¤ut



Migrate Database using zodbupdate
---------------------------------

Use the 'convert-in-py3' branch of zodbupdate.
The 'convert-in-py3' branch is already implemented in buildout.coredev.

The Database Migration is run in the Python3 installation of Plone5.2 after the Database is copied there.

Example assuming Python2 installation in folder py2 and Python3 installation in folder py3.

.. code-block:: bash

    rm -rf py3/var/*storage
    cp -r py2/var/*storage py3/var/
    py3/bin/zodbupdate --convert-py3 --file py3/var/filestorage/Data.fs --encoding=utf8



Downtime
--------

When running the Database Migration in Python3 on the target installation there is no Downtime.



Custom Content Types
--------------------

When running the Database Migration in Python3 there is most certainly no need to provide additional mappings for zodbupdate.



Test Migration
--------------

You can use the following command to check, that all records in the database can be successfully loaded.

.. code-block:: bash

    bin/instance verifydb

The output should look like this::

    ...
    INFO:zodbverify:Scanning ZODB...
    INFO:zodbverify:Done! Scanned 5999 records. Found 0 records that could not be loaded.



Running zodbupdate in Python2 installation
------------------------------------------

In an older Version of zodbupdate the Database Migration is run in Python2 installation of Plone5.2.

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



Prepare zodbupdate in Python2 installation
------------------------------------------


TODO: Not yet sure if custom types need to provide additional mappings for zodbupdate.


If you have custom content types and add-ons, it is a good idea to first test the migration on a staging server.


Here is an example Pull Request that adds them: `https://github.com/zopefoundation/Products.PythonScripts/pull/19 <https://github.com/zopefoundation/Products.PythonScripts/pull/19>`_


Analyze existing objects in the ZODB and list classes with missing `[zodbupdate.decode]` mapping for attributes containing string values that could possibly break when converted to python3.
workflow: analyze, read sourcecode, add pdb to see which values are passed to attribute to decide whether to use bytes or utf-8

.. code-block:: bash

    bin/zodb-py3migrate-analyze py2/var/filestorage/Data.fs -b py2/var/blobstorage -v
    # this might be possible with zodbupdate (https://github.com/zopefoundation/zodbupdate/issues/10)



Downtime in Python2 installation
--------------------------------

This step actually requires to take your site offline or into read-only mode.


Some thoughts on doing upgrades w/o downtime that came up in a hangout during a coding sprint in October 2018:


- jim mentions downtime. would try to leverage the zrs replication protocol, secondary server with converted data.
  It would probably be a trivial change to zrs.
- for relstorage jim mentions a zrs equivalent for relstorage: http://www.newtdb.org/en/latest/topics/following.html
- david thought out loud about taking down downtime: do conversion at read time....
