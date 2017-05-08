=======================
Plone Deprecation Guide
=======================

------------
Introduction
------------

This document describes rationales, configuration and best practices of deprecations in Plone, Zope and Python.
It is meant as a styleguide on how to apply deprecations in Plone core packages.
It also has a value as a general overview on how to deprecate in Python.


Why Deprecation
===============

At some point we

- need to get rid of old code,
- want to unify api style (consistent api),
- fix typos in namings,
- move code around (inside package or to another package).

While refactoring code, moving modules, functions, classes and methods is often needed.
To not break third party code imports from the old place or usage of old functions/ methods must work for while.
Deprecated methods are usually removed with the next major release of Plone.
Following the `semantic versioning guideline <http://semver.org>`_ is recommended.


Help Programmers, No annoyance
==============================

Deprecation has to support the consumers of the code - the programmers using it.
From their point of view, Plone core code is an API to them.
Any change is annoying to them anyway, but they feel better if deprecation warnings are telling them what to do.

Deprecations must always log at level *warning* and have to answers the question:

**"Why is the code gone from the old place? What to do instead?"**

A short message is enough., i.e.:

- "Replaced by new API xyz, found at abc.cde".,
- "Moved to xyz, because of abc.",
- "Name had a typo, new name is "xyz".

All logging has to be done once, i.e. on first usage or first import.
It must not flood the logs.


Use Cases
=========

Renaming
    We may want to rename classes, methods, functions or global or class variables in order to get a more consistent api or because of a typo, etc.
    We never just rename, we always provide a deprecated version logging a verbose deprecation warning with information where to
    import from in future.

Moving a module, class, function, etc to another place
    For some reason, i.e. merging packages, consistent api or resolving cirular import problems, we need to move code around.
    When imported from the old place it logs a verbose deprecation warning with information where to import from in future.

Deprecation of a whole package
    A whole package (folder with ``__init__.py``)

    - all imports still working, logging deprecation warnings on first import
    - ZCML still exists, but is empty (or includes the zcml from the new place if theres no auto import (i.e. for meta.zcml).

Deprecation of a whole python egg
    We will provide a last major release with no 'real' code, only backward compatible (bbb) imports of public API are provided.
    This will be done the way described above for a whole package.
    The README clearly states why it was moved and where to find the code now.

Deprecation of a GenericSetup profile
    They may got renamed for consistency or are superfluos after an update.
    Code does not need to break to support this.


---------------------------
Enable Deprecation Warnings
---------------------------

Zope
====

Zope does configure logging and warnings, so the steps below (under section Python) are not needed.

Using ``plone.recipe.zope2instance`` add the option ``deprecation-warnings = on`` to the buildouts ``[instance]`` section.

.. code-block:: ini

    [buildout]
    parts = instance

    [instance]
    recipe = plone.recipe.zope2instance
    ...
    deprecation-warnings = on
    ...


This just sets a configuration option in ``zope.conf``.

Without the recipe this can be set manually as well:
In ``zope.conf`` custom filters for warnings can be defined.

.. code-block:: xml

    ...
    <warnfilter>
        action always
        category exceptions.DeprecationWarning
    </warnfilter>
    ...


Python
======

Enable Warnings
    Warnings are written to ``stderr`` by default, but ``DeprecationWarning`` output is surpressed by default.

    Output can be enabled by starting the Python interpreter with the `-W [all|module|once] <https://docs.python.org/2/using/cmdline.html#cmdoption-W>`_ option.

    It is possible to enable output in code too:

    .. code-block:: python

        import warnings
        warnings.simplefilter("module")

Configure Logging
    Once output is enabled it is possible to `redirect warnings to the logger <https://docs.python.org/2/library/logging.html#logging.captureWarnings>`_:

    .. code-block:: python

        import logging
        logging.captureWarnings(True)


Running tests
=============

In Plone tests deprecation warnings are not shown by default.
The ``zope.conf`` setting is not taken into account.

In order to enable deprecation warnings,
the Python way with the ``-W`` command option must to be used.

Given youre using a modern buildout with virtualenv as recommended,
the call looks like so:

.. code-block:: bash

    ./bin/python -W module ./bin/test


-------------------------
Deprecation Best Practice
-------------------------

Vanilla Deprecation Messages
============================

Python offers a built-in ``DeprecationWarning`` which can be issued using standard libraries ``warnings`` module.

For details read the `official documentation about warnings <https://docs.python.org/2/library/warnings.html>`_.

In short it works like so

.. sourcecode:: python

       import warnings
       warnings.warn('deprecated', DeprecationWarning)


Moving Whole Modules
====================

Given a package ``old.pkg`` with a module ``foo.py`` need to be moved to a package ``new.pkg`` as ``bar.py``.

`zope.deprecation Moving modules <http://docs.zope.org/zope.deprecation/api.html#moving-modules>`_ offers a helper.

1. Move the ``foo.py`` as ``bar.py`` to the ``new.pkg``.
2. At the old place create a new ``foo.py`` and add to it

.. sourcecode:: python

    from zope.deprecation import moved
    moved('new.pkg.bar', 'Version 2.0')

Now you can still import the namespace from ``bar`` at the old place, but get a deprecation warning:

    DeprecationWarning: old.pkg.foo has moved to new.pkg.bar.
    Import of old.pkg.foo will become unsupported in Version 2.0


Moving Whole Packages
=====================

This is the same as moving a module, just create for each module a file.


Deprecating methods and properties
==================================

You can use the ``@deprecate`` decorator from `zope.deprecation Deprecating methods and properties <http://docs.zope.org/zope.deprecation/api.html#deprecating-methods-and-properties>`_ to deprecate methods in a module:


.. sourcecode:: python

    from zope.deprecation import deprecate

    @deprecate('Old method is no longer supported, use new_method instead.')
    def old_method():
        return 'some value'

The ``deprecated`` wrapper method is for deprecating properties:

.. sourcecode:: python

    from zope.deprecation import deprecated

    foo = None
    foo = deprecated(foo, 'foo is no more, use bar instead')


Moving functions and classes
============================

Given we have a Python file at ``old/foo/bar.py`` and want to move some classes or functions to ``new/baz/baaz.py``.

Here ``zope.deferredimport`` offers a deprecation helper.
It also avoids circular imports on initialization time.

.. code-block:: python

    import zope.deferredimport
    zope.deferredimport.initialize()

    zope.deferredimport.deprecated(
        "Import from new.baz.baaz instead",
        SomeOldClass='new.baz:baaz.SomeMovedClass',
        some_old_function='new.baz:baaz.some_moved_function',
    )

    def some_function_which_is_not_touched_at_all():
        pass


Deprecating a GenericSetup profile
==================================

Starting with GenericSetup 1.8.2 (part of Plone > 5.0.2) the ``post_handler`` attribute in ZCML can be used to call a function after the profile was applied.
We use this feature to issue a warning.

First we register the same profile twice. Under the new name and under the old name:

.. sourcecode:: xml

    <genericsetup:registerProfile
        name="default"
        title="My Fance Package"
        directory="profiles/default"
        description="..."
        provides="Products.GenericSetup.interfaces.EXTENSION"
        />

    <genericsetup:registerProfile
        name="some_confusing_name"
        title="My Fance Package (deprecated)"
        directory="profiles/some_confusing_name"
        description="... (use profile default instaed)"
        provides="Products.GenericSetup.interfaces.EXTENSION"
        post_handler=".setuphandlers.deprecate_profile_some_confusing_name"
        />

And in ``setuphandlers.py`` add a function:

.. sourcecode:: python

    import warnings

    def deprecate_profile_some_confusing_name(tool):
        warnings.warn(
            'The profile with id "some_confusing_name" was renamed to "default".',
            DeprecationWarning
        )
