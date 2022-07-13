==========================================
Migrate a ZODB from Python 2.7 to Python 3
==========================================

.. note::

   The process described here was successfully applied to several projects with its databases.
   Anyway, this is still work in progress.
   Any help to make this document better is appreciated.
   To continue with documenting the process or help improve the involved scripts/tools please have a look at the following resources:

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
==========================

In short you need to follow these steps to migrate your database:

#. Upgrade your site to Plone 5.2 running on Python 2 first.
   (see :doc:`upgrade_to_52`)
#. Make sure your code and all add-ons that you use work in Python 3.
   (see :doc:`upgrade_to_python3`)
#. Backup your database!
#. **Pack** your database to **0 days** (``zodbupdate`` will not update your database history and will leave old objects in place and you will not be able to pack your database in the future).
#. In your old buildout under Python 2, verify your database integrity using :py:mod:`zodbverify`.
   Solve integrity problems, if there are any.
#. Prepare your buildout for migrating the database to Python 3
#. Do **not** start the instance.
#. Migrate your database using :py:mod:`zodbupdate`
#. Verify your database integrity using :py:mod:`zodbverify`
   If there are any problems, solve them and redo the migration.
#. Start the instance.
#. Manually check if all works as expected



Why Do I Have To Migrate My Database?
=====================================

To understand the problem that arises when migrating a ZODB from Python 2 to Python 3,
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

How zodbupdate solves the problem
=================================

:py:mod:`zodbupdate` loads the ZODB and iterates on a low-level without actually loading the pickle over all pickle-data.

It does:

- Update magic marker to indicate the new format of the database.
- Rename classes and modules with different locations.
- Convert bytes to string or keep binary (according to rule-mappings).
- Handle encoding-problems while doing bytes to string conversion and provide fallbacks for mixed encodings in DB.


Prepare Your Buildout For Migrating The Database To Python 3
============================================================

You need to add :py:mod:`zodbverify` to your Python 2 buildouts ``eggs = `` variable in the ``[instance]`` section.

You need to add the package :py:mod:`zodbupdate` and :py:mod:`zodbverify` to your Python 3 buildout.

Depending on your buildout this could look like this:

.. code-block:: ini

    [buildout]

    parts +=
        zodbupdate

    auto-checkout +=
        zodbupdate

    [instance]
    eggs +=
        zodbverify

    [zodbupdate]
    recipe = zc.recipe.egg
    eggs =
        zodbupdate
        ${buildout:eggs}

    [sources]
    zodbupdate = git https://github.com/zopefoundation/zodbupdate.git pushurl=git@github.com:zopefoundation/zodbupdate.git branch=master


This adds a new buildout-part ``zodbupdate``.
The coredev-buildout already has this part.

After re-running buildout you will now have a new executable ``./bin/zodbupdate``.

.. warning::

    Do not try to start Plone in Python 3 with the old database before migrating it!
    Trying to that will destroy the database and result in a traceback like this:

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

Verify The Integrity of the Database in Python 2
================================================

The preflight verification of the database is run on Plone 5.2 in Python 2.
First check if all Python-pickles in the database can be loaded.
In older and grown projects it is possible to have pickles in there pointing to classes long gone in code.
Those may cause problems later.

Call ``./bin/instance zodbverify`` in your Python 2.7 setup.
If a problem pops up there is a debug mode with additional parameter ``-D``, resulting in PDB with the pickle-data and a decompiled pickle in place to gather information about the source of the problem.
This enables solving the problem by either adding a stub class in the code or by deleting the object in the ZODB.


Migrate Database using zodbupdate
=================================

The migration of the database is run on Plone 5.2 in Python 3.
It is expected to work equally in Python 3.6 and 3.7.

Run the migration by

- passing the operation to undertake (`convert-py3`),
- the location of the database,
- the encoding expected and
- optional, encoding fallbacks if the database contains mixed encodings.

.. code-block:: console

    ./bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs --encoding utf8 --encoding-fallback latin1

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

.. note::

    The blobstorage (holding binary data of files and images) will not be changed or even be read during the migration since the blobs only contain the raw binary data of the file/image.

.. note::

    The encoding should always be `utf8` and will be used when porting database-entries of classes where no encoding is specified in a `[zodbupdate.decode]` mapping in the package that holds the base-class.

.. note::

    The encoding fallback is optional and should not be provided by default.
    If a ``UnicodeDecodeError`` occur, try to find out if the instance was configured with encodings different from `utf8`.
    Provides those as encodings as fallback.
    If in doubt try `latin1` since this was in former times of Zope the default encoding.


Test Migration
==============

You can use the following command to check if all records in the database can be successfully loaded:

.. code-block:: bash

    bin/instance zodbverify

The output should look like this:

.. code-block:: bash

        $ ./bin/instance zodbverify

        INFO:Zope:Ready to handle requests
        INFO:zodbverify:Scanning ZODB...
        INFO:zodbverify:Done! Scanned 7781 records. Found 0 records that could not be loaded.

Most likely you will have additional log-messages, warnings and even errors.

.. note::

    You can use the debug-mode with `./bin/instance zodbverify -D` which will drop you in a pdb each time a database-entry cannnot be unpickled so you can inspect it and figure out if that is a real issue or not.

    Before you start debugging you should read the following section on Troubleshooting because in many cases you can ignore the warnings.


Troubleshooting
===============

Data.fs.index broken
~~~~~~~~~~~~~~~~~~~~

Delete `Data.fs.index` before migrating or you will get this error during migrating:

.. code-block:: bash

    $ ./bin/zodbupdate --convert-py3 --file=var/filestorage/Data.fs --encoding=utf8
    Updating magic marker for var/filestorage/Data.fs
    loading index
    Traceback (most recent call last):
      File "/home/erral/downloads/eggs/ZODB-5.5.1-py3.6.egg/ZODB/FileStorage/FileStorage.py", line 465, in _restore_index
        info = fsIndex.load(index_name)
      File "/home/erral/downloads/eggs/ZODB-5.5.1-py3.6.egg/ZODB/fsIndex.py", line 134, in load
        v = unpickler.load()
    UnicodeDecodeError: 'ascii' codec can't decode byte 0x80 in position 249: ordinal not in range(128)

This error can be safely ignored.

Search/ Catalog raises errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If searches are failing and are raising errors, go to the ZMI of your Plone Site root.
Select the ``portal_catalog`` and click on the ``Advanced`` tab.
Select ``Clear and Rebuild``.
This may take a while!


ModuleNotFoundError: No module named PloneLanguageTool
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

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

If there are log-messages during the migration or during ``zodbverify`` that does not necessarily mean that the migration did not work or that your database is broken.
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


Downtime
========

Some thoughts on doing upgrades without downtime that came up in a Hangout during a coding sprint in October 2018:

- You can try to leverage the ZRS replication protocol, where the secondary server has the converted data.
  It would probably be a trivial change to ZRS to get this to work.
- For Relstorage there is a ZRS equivalent for Relstorage: http://www.newtdb.org/en/latest/topics/following.html

Further Reading
===============

The Zope Documentation contains a `section about ZODB migration <https://zope.readthedocs.io/en/latest/zope4/migration/zodb.html>`_
