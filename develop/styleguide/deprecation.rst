==========================
Deprecation Best Prcatices
==========================


Why Deprecation
===============

While refactoring code moving modules, functions, classes and methods is often needed.
To not break third party code imports from the old place or usage of old functions or methods must work for while.
Deprecated methods are usually removed with the next major release of Plone.
Following the `semantic versioning guideline <http://semver.org>`_ is recommended.


Enable Deprecation Warnings
===========================

Using ``plone.recipe.zope2instance`` add the option ``deprecation-warnings = on`` to the buildouts ``[instance]`` section.


Vanilla Deprecation Messages
============================

Python offers a built-in ``DeprecationWarning`` which can be issued using standard libraries ``warnings`` module.

For details read `the official documentation <https://docs.python.org/2/library/warnings.html>`_.

In short it works like so

   .. sourcecode:: python

       import warnings
       warnings.warn('deprecated', DeprecationWarning)


Moving Whole Modules
====================

Given a package ``old.pkg`` with a module ``foo.py`` need to be moved to a package ``new.pkg`` as ``bar.py``.

`zope.deprecation <http://docs.zope.org/zope.deprecation/api.html#moving-modules>`_ offers a helper.

1. Copy the ``foo.py`` as ``bar.py`` to the ``new.pkg``.
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




