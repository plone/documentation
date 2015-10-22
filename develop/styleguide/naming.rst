==================
Naming conventions
==================



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