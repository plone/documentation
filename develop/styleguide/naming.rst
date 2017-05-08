==================
Naming Conventions
==================

Above all else, be consistent with any code you are modifying!

Historically the code is all camel case, but new code should written following the PEP8 convention.

Class names should be written in ``CamelCase`` and function and method names all lowercase with a underscrore separating words (e.g. ``my_method``).


File Conventions
================

In Zope 2 file names used to be MixedCase.
In Python and Plone we prefer all-lowercase filenames.

This has the advantage that you can instantly see if you refer to a module / file or a class::

  from zope.pagetemplate.pagetemplate import PageTemplate

compare that to::

  from Products.PageTemplates.PageTemplate import PageTemplate

Filenames should be short and descriptive.

Think about how an import would read::

  from Products.CMFPlone.utils import safe_hasattr

compare that to::

  from Products.CMFPlone.PloneUtilities import safe_hasattr

The former is better to read, less redundant and generally more aesthetically pleasing.
