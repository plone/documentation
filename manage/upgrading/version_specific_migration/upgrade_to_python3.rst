===============================
Migrating Plone 5.2 to Python 3
===============================


.. admonition:: Description

   Instructions and tips for porting Plone projects to Python 3

.. note::

   If you want to upgrade add-ons to Python 3, the list of all Plone packages that still need to be ported can be found on the  GitHub project board `Python 3 porting state for Plone add-ons <https://github.com/orgs/collective/projects/1>`_.


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

.. warning::

    The following section is valid until the final release of Plone 5.2.
    Upon the final release of Plone 5.2, something else will take its place.

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

    You can also add development tools like `Products.PDBDebugMode <https://pypi.org/project/Products.PDBDebugMode/>`_, `plone.reload <https://pypi.org/project/plone.reload/>`_ and `Products.PrintingMailHost <https://pypi.org/project/Products.PrintingMailHost/>`_ to your buildout.

    Especially ``Products.PDBDebugMode`` will help a lot with issues during porting to Python 3.

    .. code-block:: ini

        custom-eggs +=
            collective.package
            Products.PDBDebugMode
            plone.reload
            Products.PrintingMailHost

        test-eggs +=
            collective.package [test]

        auto-checkout +=
            collective.package

        [versions]
        Products.PrintingMailHost = 1.1.1
        Products.PDBDebugMode = 1.4

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

    ./bin/isort -rc src/collective.package

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
Instead use fully qualified import paths such as ``from collective.package import permissions``.


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

For this step it is recommended that you have installed ``Products.PDBDebugMode`` to help debug and fix issues.


6 Run Tests
------------

.. code-block:: shell

    $ ./bin/test --all -s collective.package

Remember that you can run ``./bin/test -s collective.package -D`` to enter a ``pdb`` session when an error occurs.

With some luck, there will not be too many issues left with the code at this point.

It you are unlucky then you have to fix Doctests.
These should be changed so that Python 3 is the default.
For example, string types (or text) should be represented as ``'foo'``, not ``u'foo'``, and bytes types (or data) should be represented as ``b'bar'``, not ``'bar'``.
Search for examples of ``Py23DocChecker`` in Plone's packages to find a pattern which allows updated doctests to pass in Python 2.

*   To test your code against ``buildout.coredev``, start by browsing to `Add-ons [Jenkins] <https://jenkins.plone.org/view/Add-ons/>`_.
*   Note there are jobs set up for Plone 4.3, 5.1, and 5.2 on Python 2, and two jobs that run tests for Plone 5.2 on Python 3.6 and Python 3.7.
*   Click the link :guilabel:`log in` on Jenkins website (top right). For the first login, you must authorize Jenkins to have access to your GitHub account to authenticate.
*   Click the link for the job you want to run, for example, :guilabel:`Test add-on against Plone 5.2 on Python3.7`.
*   Choose the link :guilabel:`Build with parameters` in the menu on the left-hand side.
*   Fill the fields :guilabel:`ADDON_URL` and :guilabel:`ADDON_BRANCH` with your repository's URL and the branch name ("python3" if you followed these instructions).
*   Start the build with the :guilabel:`Build` button.


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
Read the `Conservative Python 3 Porting Guide, Strings <https://portingguide.readthedocs.io/en/latest/strings.html>`_ to be prepared.

.. note::

    As a rule of thumb, you can assume that in Python 3 everything should be text.
    Only in very rare cases will you need to handle bytes.

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
For new projects you can start with a Python 3 with a fresh database.
To use an existing project in Python 3 though, you need to migrate your existing database first.
This section explains how to do that.

ZODB itself is compatible with Python 3 but a DB created in Python 2.7 cannot be used in Python 3 without modifying it before.
(See `Why do I have to migrate my database?`_ for technical background).


Database Upgrade Procedure
--------------------------

In short you need to follow these steps to migrate your database:

#. Upgrade your site to Plone 5.2 running on Python 2 first.
   (see :doc:`upgrade_to_52`)
#. Make sure your code and all add-ons that you use work in Python 3.
   (see the section above)
#. Backup your database!
#. Prepare your buildout for migrating the database to Python 3.
#. Migrate your database using :py:mod:`zodbupdate`



Why Do I Have To Migrate My Database
-------------------------------------

To understand the problem that arises when migrating a ZODB from Python2 to Python3,
this `introduction <https://blog.gocept.com/2018/06/07/migrate-a-zope-zodb-data-fs-to-python-3/>`_ and the following example will help.

When pickling an object the datatypes and values are stored.

In Python 2 strings get STRING, and Unicode gets UNICODE

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

Python 3 does not allow non-ascii characters in bytes and the pickle declares the byte string as SHORT_BINBYTES and the string (py2 unicode) as BINUNICODE

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


Python 3 will wrongly interpret a pickle created with Python 2 that contains non-ascii characters in a field declared with OPTCODE `STRING`.
In that case we may end up with a `UnicodeDecodeError` for this pickle in `ZODB.serialize`


.. code-block:: bash

    $ python3
    >>> b'\xc3\x9cml\xc3\xa4ut'.decode('ascii')
    Traceback (most recent call last):
      File "<stdin>", line 1, in <module>
    UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 0: ordinal not in range(128)

Or when UTF-8 encoded byte-strings are interpreted as Unicode we do not get an error but mangled non-ascii characters:

.. code-block:: bash

    $ python3
    >>> print('\xdcml\xe4ut')
    Ümläut
    >>> print('\xc3\x9cml\xc3\xa4ut')
    ÃmlÃ¤ut


TODO: Add some info on how `zodbupdate` changes these pickles during the migration and how and in which cases the default-encoding is used.


Prepare Your Buildout For Migrating The Database To Python 3
------------------------------------------------------------

You need to add the package :py:mod:`zodbupdate` to your buildout.

Depending on your buildout this could look like this:

.. code-block:: ini

    [buildout]

    parts =+
        zodbupdate

    auto-checkout +=
        zodbupdate

    [zodbupdate]
    recipe = zc.recipe.egg
    eggs =
        zodbupdate
        ${buildout:eggs}

    [sources]
    zodbupdate = git https://github.com/zopefoundation/zodbupdate.git pushurl=git@github.com:zopefoundation/zodbupdate.git branch=convert-in-py3


This adds a new buildout-part `zodbupdate` and uses a checkout of the branch `convert-in-py3` of :py:mod:`zodbupdate`.
The branch is necessary until https://github.com/zopefoundation/zodbupdate/pull/14 is merged. The coredev also uses this branch.

After re-running buildout you will now have a new executable `./bin/zodbupdate`.

.. warning::

    Do not try to start Plone in Python 3 with the old database before migrating it!
    Trying to that will result in a traceback like this:

    .. code-block::

        Traceback (most recent call last):
          File "/Users/pbauer/workspace/projectx/parts/instance/bin/interpreter", line 279, in <module>
            exec(compile(__file__f.read(), __file__, "exec"))
          File "/Users/pbauer/.cache/buildout/eggs/Zope-4.0b8-py3.7.egg/Zope2/Startup/serve.py", line 219, in <module>
            sys.exit(main() or 0)

          [...]

          File "/Users/pbauer/.cache/buildout/eggs/ZODB-5.5.1-py3.7.egg/ZODB/FileStorage/FileStorage.py", line 1619, in read_index
            raise FileStorageFormatError(name)
        ZODB.FileStorage.FileStorage.FileStorageFormatError: /Users/pbauer/workspace/projectx/var/filestorage/Data.fs


Migrate Database using zodbupdate
---------------------------------

Make sure you use the branch `convert-in-py3` of :py:mod:`zodbupdate`.

The migration of the database is run on Plone 5.2 in Python 3.
It is expected to work equally in Python 3.6 and 3.7.

Run the migration by passing the operation to undertake (`convert-py3`), the location of the database and the fallback-encoding.

.. code-block:: console

    ./bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs --encoding=utf8

Depending on the size of you database this can take a while.

Ideally the output is similar to this:

.. code-block:: console

    $ ./bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs --encoding=utf8
    Updating magic marker for var/filestorage/Data.fs
    Ignoring index for /Users/pbauer/workspace/projectx/var/filestorage/Data.fs
    Loaded 2 decode rules from AccessControl:decodes
    Loaded 12 decode rules from OFS:decodes
    Loaded 2 decode rules from Products.PythonScripts:decodes
    Loaded 1 decode rules from Products.ZopeVersionControl:decodes
    Committing changes (#1).

Afterwards you can start your instance in Python 3 and test if everything works as expected.

.. note::

    The blobstorage (holding binary data of files and images) will not be changed or even be read during the migration since the blobs only contain the raw binary data of the file/image.

.. note::

    The fallback-encoding should always be `utf8` and will be used when porting database-entries of classes where no encoding is specified in a `[zodbupdate.decode]` mapping in the package that holds the base-class.


Test Migration
--------------

You can use the following command to check if all records in the database can be successfully loaded:

.. code-block:: bash

    bin/instance verifydb

The output should look like this:

.. code-block:: bash

        $ ./bin/instance verifydb

        INFO:Zope:Ready to handle requests
        INFO:zodbverify:Scanning ZODB...
        INFO:zodbverify:Done! Scanned 7781 records. Found 0 records that could not be loaded.

Most likely you will have additional log-messages, warnings and even errors.

.. note::

    You can use the debug-mode with `./bin/instance verifydb -D` which will drop you in a pdb each time a database-entry cannnot be unpickled so you can inspect it and figure out if that is a real issue or not.

    Before you start debugging you should read the following section on Troubleshooting because in many cases you can ignore the warnings.


Troubleshooting
---------------


ModuleNotFoundError: No module named 'PloneLanguageTool'
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

There were cases when the migration aborted with a import-error like this::

    An error occured
    Traceback (most recent call last):
      File "/Users/pbauer/.cache/buildout/eggs/plone.app.upgrade-2.0.22-py3.7.egg/plone/app/upgrade/__init__.py", line 120, in <module>
        from Products.PloneLanguageTool import interfaces  # noqa F811
    ModuleNotFoundError: No module named 'PloneLanguageTool'

    During handling of the above exception, another exception occurred:

    Traceback (most recent call last):
      File "/Users/pbauer/workspace/stiftung_py3/src-mrd/zodbupdate/src/zodbupdate/main.py", line 201, in main
        updater()
      File "/Users/pbauer/workspace/stiftung_py3/src-mrd/zodbupdate/src/zodbupdate/update.py", line 82, in __call__
        new = self.processor.rename(current)
      File "/Users/pbauer/workspace/stiftung_py3/src-mrd/zodbupdate/src/zodbupdate/serialize.py", line 333, in rename
        data = unpickler.load()
      File "/Users/pbauer/workspace/stiftung_py3/src-mrd/zodbupdate/src/zodbupdate/serialize.py", line 199, in __find_global
        return find_global(*self.__update_symb(klass_info), Broken=ZODBBroken)
      File "/Users/pbauer/workspace/stiftung_py3/src-mrd/zodbupdate/src/zodbupdate/serialize.py", line 177, in __update_symb
        symb = find_global(*symb_info, Broken=ZODBBroken)
      File "/Users/pbauer/.cache/buildout/eggs/ZODB-5.5.1-py3.7.egg/ZODB/broken.py", line 204, in find_global
        __import__(modulename)
      File "/Users/pbauer/.cache/buildout/eggs/plone.app.upgrade-2.0.22-py3.7.egg/plone/app/upgrade/__init__.py", line 127, in <module>
        'Products.PloneLanguageTool.LanguageTool',
    AttributeError: type object 'LanguageTool' has no attribute 'LanguageTool'
    Stopped processing, due to: type object 'LanguageTool' has no attribute 'LanguageTool'
    Traceback (most recent call last):
      File "/Users/pbauer/.cache/buildout/eggs/plone.app.upgrade-2.0.22-py3.7.egg/plone/app/upgrade/__init__.py", line 120, in <module>
        from Products.PloneLanguageTool import interfaces  # noqa F811
    ModuleNotFoundError: No module named 'PloneLanguageTool'

To work around this comment out the lines offending lines in `plone/app/upgrade/__init__.py` (do not forget to uncomment them after the migration!)

.. code-block:: python

    # try:
    #     from Products.PloneLanguageTool import interfaces  # noqa F811
    # except ImportError:
    #     alias_module('Products.PloneLanguageTool.interfaces', bbb)
    #     alias_module('Products.PloneLanguageTool', bbbd)
    #     __import__(
    #         'Products.PloneLanguageTool.LanguageTool',
    #     ).PloneLanguageTool.LanguageTool = __import__(
    #         'Products.PloneLanguageTool.LanguageTool',
    #     ).PloneLanguageTool.LanguageTool.LanguageTool



Migration Logs Errors And Warnings
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If there are log-messages during the migration or during verifydb that does not necessarily mean that the migration did not work or that your database is broken. 
For example if you migrated from Plone 4 to Plone 5 and then from Archetypes to Dexterity it is very likely that items in the database cannot be loaded because packages like `Products.Archetypes`, `plone.app.blob` or `plone.app.imaging` are not available.
These items are most likely remains that were not removed properly but are not used.
If your site otherwise works fine you can choose to ignore these issues.

Here is the output of a migration start started in Plone 4 with Archetypes.
The site still works nicely in Plone 5.2 on Python 3.7 despite the warnings and errors::

    Updating magic marker for var/filestorage/Data.fs
    Loaded 2 decode rules from AccessControl:decodes
    Loaded 12 decode rules from OFS:decodes
    Loaded 2 decode rules from Products.PythonScripts:decodes
    Loaded 1 decode rules from Products.ZopeVersionControl:decodes
    Warning: Missing factory for App.Product ProductFolder
    Warning: Missing factory for Products.Archetypes.ReferenceEngine ReferenceCatalog
    Warning: Missing factory for Products.Archetypes.ArchetypeTool ArchetypeTool
    Warning: Missing factory for Products.PloneLanguageTool.LanguageTool LanguageTool
    Warning: Missing factory for Products.Archetypes.UIDCatalog UIDCatalog
    Warning: Missing factory for Products.CMFPlone.MetadataTool MetadataTool
    Warning: Missing factory for Products.CMFDefault.MetadataTool MetadataSchema
    Warning: Missing factory for Products.Archetypes.ReferenceEngine ReferenceBaseCatalog
    Warning: Missing factory for Products.ATContentTypes.tool.atct ATCTTool
    Warning: Missing factory for Products.ATContentTypes.tool.topic TopicIndex
    Warning: Missing factory for Products.ResourceRegistries.tools.CSSRegistry CSSRegistryTool
    Warning: Missing factory for Products.ResourceRegistries.tools.CSSRegistry Stylesheet
    Warning: Missing factory for Products.PasswordResetTool.PasswordResetTool PasswordResetTool
    New implicit rule detected copy_reg _reconstructor to copyreg _reconstructor
    New implicit rule detected __builtin__ object to builtins object
    Warning: Missing factory for Products.CMFPlone.CalendarTool CalendarTool
    Warning: Missing factory for Products.CMFPlone.InterfaceTool InterfaceTool
    Warning: Missing factory for Products.CMFPlone.ActionIconsTool ActionIconsTool
    Warning: Missing factory for Products.CMFActionIcons.ActionIconsTool ActionIcon
    Warning: Missing factory for Products.Archetypes.UIDCatalog UIDBaseCatalog
    Warning: Missing factory for Products.CMFPlone.UndoTool UndoTool
    Warning: Missing factory for Products.TinyMCE.utility TinyMCE
    Warning: Missing factory for Products.ResourceRegistries.tools.JSRegistry JSRegistryTool
    Warning: Missing factory for Products.ResourceRegistries.tools.JSRegistry JavaScript
    Warning: Missing factory for Products.CMFPlone.FactoryTool FactoryTool
    New implicit rule detected copy_reg __newobj__ to copyreg __newobj__
    Warning: Missing factory for Products.ATContentTypes.tool.metadata MetadataTool
    Warning: Missing factory for Products.ATContentTypes.interfaces.interfaces IATCTTool
    New implicit rule detected Products.CMFPlone.DiscussionTool DiscussionTool to OFS.SimpleItem SimpleItem
    Warning: Missing factory for Products.CMFDefault.MetadataTool ElementSpec
    Warning: Missing factory for Products.CMFDefault.MetadataTool MetadataElementPolicy
    New implicit rule detected plone.app.folder.nogopip GopipIndex to plone.folder.nogopip GopipIndex
    Warning: Missing factory for Products.ATContentTypes.content.folder ATFolder
    Warning: Missing factory for Products.Archetypes.BaseUnit BaseUnit
    Warning: Missing factory for Products.ATContentTypes.content.document ATDocument
    Warning: Missing factory for plone.app.blob.content ATBlob
    Warning: Missing factory for plone.app.blob.interfaces IATBlobImage
    Warning: Missing factory for Products.ATContentTypes.interfaces.image IATImage
    Warning: Missing factory for Products.ATContentTypes.interfaces.image IImageContent
    Warning: Missing factory for plone.app.blob.field BlobWrapper
    Warning: Missing factory for plonetheme.stiftung.portlets.news Assignment
    Warning: Missing factory for plonetheme.stiftung.portlets.linkportlet Assignment
    New implicit rule detected plone.app.portlets.portlets.events Assignment to plone.app.event.portlets.portlet_events Assignment
    Warning: Missing factory for Products.Archetypes.ReferenceEngine Reference
    Warning: Missing factory for Products.ATContentTypes.content.link ATLink
    Warning: Missing factory for Products.ATContentTypes.content.newsitem ATNewsItem
    Warning: Missing factory for Products.Archetypes.Field Image
    Warning: Missing factory for plone.app.imaging.scale ImageScale
    Warning: Missing factory for webdav.LockItem LockItem
    Warning: Missing factory for plone.app.blob.interfaces IATBlobFile
    Warning: Missing factory for Products.ATContentTypes.interfaces.file IATFile
    Warning: Missing factory for Products.ATContentTypes.interfaces.file IFileContent
    Error: cannot pickle modified record: Can't pickle <class 'Products.ResourceRegistries.tools.JSRegistry.JavaScript'>: attribute lookup Products.ResourceRegistries.tools.JSRegistry.JavaScript failed
    Warning: Missing factory for plone.app.collection.collection Collection
    Warning: Missing factory for collective.flowplayer.media VideoInfo
    Error: cannot pickle modified record: Can't pickle <class 'Products.ResourceRegistries.tools.CSSRegistry.Stylesheet'>: attribute lookup Products.ResourceRegistries.tools.CSSRegistry.Stylesheet failed
    Warning: Missing factory for Products.ResourceRegistries.interfaces.settings IResourceRegistriesSettings
    Warning: Missing factory for collective.js.jqueryui.controlpanel IJQueryUICSS
    Warning: Missing factory for collective.js.jqueryui.controlpanel IJQueryUIPlugins
    Warning: Missing factory for wildcard.media.content Video
    Committing changes (#1).

    Found new rules: {
     'Products.CMFPlone.DiscussionTool DiscussionTool': 'OFS.SimpleItem SimpleItem',
     '__builtin__ object': 'builtins object',
     'copy_reg __newobj__': 'copyreg __newobj__',
     'copy_reg _reconstructor': 'copyreg _reconstructor',
     'plone.app.folder.nogopip GopipIndex': 'plone.folder.nogopip GopipIndex',
     'plone.app.portlets.portlets.events Assignment': 'plone.app.event.portlets.portlet_events Assignment',
    }


Broken Values In ZCTextIndex
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some indexes of the type `ZCTextIndex` may hold invalid data which results in a traceback like this::

    2019-03-11 17:06:37,622 ERROR   [portlets:38][waitress] Error while determining renderer availability of portlet ('context' '/Plone' 'events'): cannot use a string pattern on a bytes-like object
    Traceback (most recent call last):
      File "/Users/pbauer/.cache/buildout/eggs/plone.portlets-2.3.1-py3.7.egg/plone/portlets/manager.py", line 119, in _lazyLoadPortlets
        isAvailable = renderer.available
      File "/Users/pbauer/.cache/buildout/eggs/plone.app.event-3.2.2-py3.7.egg/plone/app/event/portlets/portlet_events.py", line 141, in available
        return self.data.count > 0 and len(self.events)
      File "/Users/pbauer/.cache/buildout/eggs/plone.app.event-3.2.2-py3.7.egg/plone/app/event/portlets/portlet_events.py", line 189, in events
        expand=True, limit=data.count, **query
      File "/Users/pbauer/.cache/buildout/eggs/plone.app.event-3.2.2-py3.7.egg/plone/app/event/base.py", line 151, in get_events
        sort, sort_reverse)
      File "/Users/pbauer/.cache/buildout/eggs/plone.app.event-3.2.2-py3.7.egg/plone/app/event/base.py", line 220, in filter_and_resort
        idx = catalog.getIndexDataForRID(brain.getRID())
      File "/Users/pbauer/.cache/buildout/eggs/Products.ZCatalog-4.2-py3.7.egg/Products/ZCatalog/ZCatalog.py", line 556, in getIndexDataForRID
        return self._catalog.getIndexDataForRID(rid)
      File "/Users/pbauer/.cache/buildout/eggs/Products.ZCatalog-4.2-py3.7.egg/Products/ZCatalog/Catalog.py", line 469, in getIndexDataForRID
        result[name] = self.getIndex(name).getEntryForObject(rid, "")
      File "/Users/pbauer/.cache/buildout/eggs/Products.ZCatalog-4.2-py3.7.egg/Products/ZCTextIndex/ZCTextIndex.py", line 214, in getEntryForObject
        word_ids = self.index.get_words(documentId)
      File "/Users/pbauer/.cache/buildout/eggs/Products.ZCatalog-4.2-py3.7.egg/Products/ZCTextIndex/BaseIndex.py", line 106, in get_words
        return WidCode.decode(self._docwords[docid])
      File "/Users/pbauer/.cache/buildout/eggs/Products.ZCatalog-4.2-py3.7.egg/Products/ZCTextIndex/WidCode.py", line 93, in decode
        return [get(p) or _decode(p) for p in _prog.findall(code)]
    TypeError: cannot use a string pattern on a bytes-like object

Updating the catalog will update the index and make the error go away.


Running Zodbupdate In Python 2
------------------------------

If the approach to run :py:mod:`zodbupdate` in Python 3 does not work you could try the older approach to migrate the database in Python 2.7.

Prepare Buildout
~~~~~~~~~~~~~~~~

To do so add zodbupdate to buildout eggs without using the branch `convert-in-py3`:

.. code-block:: ini

    [buildout]

    parts =+
        zodbupdate

    auto-checkout +=
        zodbupdate

    [zodbupdate]
    recipe = zc.recipe.egg
    eggs =
        zodbupdate
        zodb.py3migrate
        ${buildout:eggs}

    scripts =
        zodb-py3migrate-analyze
        zodbupdate

    [sources]
    zodbupdate = git https://github.com/zopefoundation/zodbupdate.git pushurl=git@github.com:zopefoundation/zodbupdate.git branch=convert-in-py3


Prepare Zodbupdate In Python 2 Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Before migrating you need to analyze the existing objects in the ZODB and list classes with missing `[zodbupdate.decode]` mapping for attributes containing string values that could possibly break when converted to python3.

Workflow: analyze, read sourcecode, add pdb to see which values are passed to attribute to decide whether to use bytes or utf-8

.. code-block:: bash

    ./bin/zodb-py3migrate-analyze py2/var/filestorage/Data.fs -b py2/var/blobstorage -v
    # this might be possible with zodbupdate (https://github.com/zopefoundation/zodbupdate/issues/10)

If you need to add additional mappings to packages here is an example Pull Request that adds them: `https://github.com/zopefoundation/Products.PythonScripts/pull/19 <https://github.com/zopefoundation/Products.PythonScripts/pull/19>`_

Migrate
~~~~~~~

Then you can migrate the database as described above with the exception that you cannot specify a default-encoding:

.. code-block:: bash

    ./bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs


Downtime
--------

Some thoughts on doing upgrades without downtime that came up in a Hangout during a coding sprint in October 2018:

- You can try to leverage the zrs replication protocol, where the secondary server has the converted data. It would probably be a trivial change to zrs to get this to work.
- For relstorage there is a zrs equivalent for relstorage: http://www.newtdb.org/en/latest/topics/following.html
