==================
Naming conventions
==================


Naming Conventions
==================
Above all else,
be consistent with any code you are modifying!
Historically the code is all camel case,
but new code should written following the PEP8 convention.

Class names should be written in ``CamelCase`` and
function and method names all lowercase with a underscrore seperating words (e.g. ``my_method``).


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

The former is obviously much easier to read,
less redundant and generally more aesthetically pleasing.


Versioning scheme
=================

For software versions, use a sequence-based versioning scheme, which is
`compatible with setuptools <http://pythonhosted.org/setuptools/setuptools.html#specifying-your-project-s-version>`_::

    MAJOR.MINOR[.MICRO][STATUS]

The way, setuptools interprets versions is intuitive::

    1.0 < 1.1dev < 1.1a1 < 1.1a2 < 1.1b < 1.1rc1 < 1.1 < 1.1.1

You can test it with setuptools::

    >>> from pkg_resources import parse_version
    >>> parse_version('1.0') < parse_version('1.1.dev')
    ... < parse_version('1.1.a1') < parse_version('1.1.a2')
    ... < parse_version('1.1.b') < parse_version('1.1.rc1')
    ... < parse_version('1.1') < parse_version('1.1.1')

Setuptools recommends to seperate parts with a dot. The website about `semantic
versioning <http://semver.org/>`_ is also worth a read.
