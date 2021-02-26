=================
Python styleguide
=================


Introduction
============

We've modeled the following rules and recommendations based on the following documents:

* `PEP8 <http://www.python.org/dev/peps/pep-0008>`__
* `PEP257 <http://www.python.org/dev/peps/pep-0257>`_
* `Rope project <https://github.com/python-rope/rope/blob/master/docs/overview.rst>`_
* `Google Style Guide <https://google.github.io/styleguide/pyguide.html>`_
* `Pylons Coding Style <https://pylonsproject.org/community-coding-style-standards.html>`_
* `Tim Pope on Git commit messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`__


Line length
===========

All Python code in this package should be PEP8 valid.
This includes adhering to the 80-char line length.
If you absolutely need to break this rule, append ``  # noqa: E501`` to the offending line to skip it in syntax checks.

.. note::
    Configuring your editor to display a line at 79th column helps a lot here and saves time.

.. note::
    The line length rule also applies to non-Python source files, such as ``.zcml`` files, but is a bit more relaxed there.

.. note::
    The rule explicitly **does not apply to documentation** ``.rst`` files.
    For ``.rst`` files including the package documentation but also ``README.rst``, ``CHANGES.rst``, and doctests, add a line break after each sentence.
    See the :doc:` documentation styleguide </about/contributing/documentation_styleguide>` for more information.


Breaking lines
--------------

Based on code we love to look at (Pyramid, Requests, etc.), we allow the following two styles for breaking long lines into blocks:

1. Break into next line with one additional indent block.

   .. sourcecode:: python

       foo = do_something(
           very_long_argument='foo',
           another_very_long_argument='bar',
       )

       # For functions the ): needs to be placed on the following line
       def some_func(
           very_long_argument='foo',
           another_very_long_argument='bar',
       ):

2. If this still doesn't fit the 80-char limit, break into multiple lines.

   .. sourcecode:: python

       foo = dict(
           very_long_argument='foo',
           another_very_long_argument='bar',
       )

       a_long_list = [
           "a_fairly_long_string",
           "quite_a_long_string_indeed",
           "an_exceptionally_long_string_of_characters",
       ]

* Arguments on first line, directly after the opening parenthesis are forbidden when breaking lines.

* The last argument line needs to have a trailing comma (to be nice to the next developer coming in to add something as an argument and minimize VCS diffs in these cases).

* The closing parenthesis or bracket needs to have the same indentation level as the first line.

* Each line can only contain a single argument.

* The same style applies to dicts, lists, return calls, etc.


autopep8
--------

Making old code pep8 compliant can be a lot of work.
There is a tool that can automatically do some of this work for you: `autopep8 <https://pypi.python.org/pypi/autopep8>`_.
This fixes various issues, for example fixing indentation to be a multiple of four.
Just install it with pip and call it like this::

    pip install autopep8
    autopep8 -i filename.py
    autopep8 -i -r directory

It is best to first run autopep8 in the default non aggressive mode, which means it only does whitespace changes.
To run this recursively on the current directory, changing files in place::

    autopep8 -i -r .

Quickly check the changes and then commit them.

WARNING: be *very* careful when running this in a skins directory, if you run it there at all.
It will make changes to the top of the file like this, which completely breaks the skin script::

    -##parameters=policy_in=''
    +# parameters=policy_in=''

With those safe changes out of the way, you can move on to a second, more aggresive round::

    autopep8 -i --aggressive -r .

Check these changes more thoroughly.
At the very least check if Plone can still start in the foreground and that there are no failures or errors in the tests.

Not all changes are always safe.
You can ignore some checks::

    autopep8 -i --ignore W690,E711,E721 --aggressive -r .

This skips the following changes:

- W690: Fix various deprecated code (via lib2to3). (Can be bad for
  Python 2.4.)

- E721: Use `isinstance()` instead of comparing types directly.
  (There are uses of this in for example GenericSetup and plone.api that must not be fixed.)

- E711: Fix comparison with None.  (This can break SQLAlchemy code.)

You can check what would be changed by one specific code::

    autopep8 --diff --select E309 -r .


Indentation
===========

For Python files, we stick with the `PEP 8 recommondation <http://www.python.org/dev/peps/pep-0008/#indentation>`_: Use 4 spaces per indentation level.

For ZCML and XML (GenericSetup) files, we recommend the `Zope Toolkit's coding style on ZCML <http://docs.zope.org/zopetoolkit/codingstyle/zcml-style.html>`_::

  Indentation of 2 characters to show nesting, 4 characters to list attributes on separate lines.
  This distinction makes it easier to see the difference between attributes and nested elements.


Quoting
=======

For strings and such prefer using single quotes over double quotes.
The reason is that sometimes you do need to write a bit of HTML in your python code, and HTML feels more natural with double quotes so you wrap HTML string into single quotes.
And if you are using single quotes for this reason, then be consistent and use them everywhere.

There are two exceptions to this rule:

* docstrings should always use double quotes (as per PEP-257).

* if you want to use single quotes in your string, double quotes might make more sense so you don't have to escape those single quotes.

.. sourcecode:: python

    # GOOD
    print 'short'
    print 'A longer string, but still using single quotes.'

    # BAD
    print "short"
    print "A long string."

    # EXCEPTIONS
    print "I want to use a 'single quote' in my string."
    """This is a docstring."""


Docstrings style
================

Read and follow http://www.python.org/dev/peps/pep-0257/.
There is one exception though: We reject BDFL's recommendation about inserting a blank line between the last paragraph in a multi-line docstring and its closing quotes as it's Emacs specific and two Emacs users here on the Beer & Wine Sprint both support our way.

The content of the docstring must be written in the active first-person form, e.g.
"Calculate X from Y" or "Determine the exact foo of bar".

.. sourcecode:: python

    def foo():
        """Single line docstring."""

    def bar():
        """Multi-line docstring.

        With the additional lines indented with the beginning quote and a
        newline preceding the ending quote.
        """

If you wanna be extra nice, you are encouraged to document your method's parameters and their return values in a `reST field list syntax <http://docutils.sourceforge.net/docs/ref/rst/restructuredtext.html#field-lists>`_.

.. sourcecode:: rest

    :param foo: blah blah
    :type foo: string
    :param bar: blah blah
    :type bar: int
    :returns: something

Check out the `plone.api source <https://github.com/plone/plone.api/tree/master/src/plone/api>`_ for more usage examples.
Also, see the following for examples on how to write good *Sphinxy* docstrings: http://stackoverflow.com/questions/4547849/good-examples-of-python-docstrings-for-sphinx.


Unit tests style
================

Read http://www.voidspace.org.uk/python/articles/unittest2.shtml to learn what is new in :mod:`unittest2` and use it.

This is not true for in-line documentation tests.
Those still use old unittest test-cases, so you cannot use ``assertIn`` and similar.


String formatting
=================

As per http://docs.python.org/2/library/stdtypes.html#str.format, we should prefer the new style string formatting (``.format()``) over the old one (``% ()``).

Also use numbering or keyword arguments, like so:

.. sourcecode:: python

    # GOOD
    print "{0} is not {1}".format(1, 2)
    print "{bar} is not {foo}".format(foo=1, bar=2)


and *not* like this:

.. sourcecode:: python

    # BAD
    print "{} is not {}".format(1, 2)
    print "%s is not %s" % (1, 2)


because Python 2.6 supports only explicitly numbered placeholders.


About imports
=============

1. Don't use ``*`` to import *everything* from a module, because if you do, pyflakes cannot detect undefined names (W404).

2. Don't use commas to import multiple things on a single line.
   Some developers use IDEs (like `Eclipse <http://pydev.org/>`_) or tools (such as `mr.igor <http://pypi.python.org/pypi/mr.igor>`_) that expect one import per line.
   Let's be nice to them.

3. Don't use relative paths, again to be nice to people using certain IDEs and tools.
   Also `Google Python Style Guide` recommends against it.

   .. sourcecode:: python

       # GOOD
       from plone.app.testing import something
       from zope.component import getMultiAdapter
       from zope.component import getSiteManager

   instead of

   .. sourcecode:: python

       # BAD
       from plone.app.testing import *
       from zope.component import getMultiAdapter, getSiteManager

4. Don't catch ``ImportError`` to detect whether a package is available or not, as it might hide circular import errors.
   Instead, use ``pkg_resources.get_distribution`` and catch ``DistributionNotFound``.
   More background at http://do3.cc/blog/2010/08/20/do-not-catch-import-errors,-use-pkg_resources/.

   .. sourcecode:: python

       # GOOD
       import pkg_resources

       try:
           pkg_resources.get_distribution('plone.dexterity')
       except pkg_resources.DistributionNotFound:
           HAS_DEXTERITY = False
       else:
           HAS_DEXTERITY = True

   instead of

   .. sourcecode:: python

       # BAD
       try:
           import plone.dexterity
           HAVE_DEXTERITY = True
       except ImportError:
           HAVE_DEXTERITY = False


Grouping and sorting
--------------------

Since Plone has such a huge code base, we don't want to lose developer time figuring out into which group some import goes (standard lib?, external package?, etc.).
We sort everything alphabetically case insensitive and insert one blank line between ``from foo import bar`` and ``import baz`` blocks.
Conditional imports come last.
Don't use multi-line imports but import each identifier from a module in a separate line.
Again, we *do not* distinguish between what is standard lib, external package or internal package in order to save time and avoid the hassle of explaining which is which.

.. sourcecode:: python

    # GOOD
    from __future__ import division
    from Acquisition import aq_inner
    from datetime import datetime
    from datetime import timedelta
    from plone.api import portal
    from plone.api.exc import MissingParameterError
    from Products.CMFCore.interfaces import ISiteRoot
    from Products.CMFCore.WorkflowCore import WorkflowException

    import pkg_resources
    import random

    try:
        pkg_resources.get_distribution('plone.dexterity')
    except pkg_resources.DistributionNotFound:
        HAS_DEXTERITY = False
    else:
        HAS_DEXTERITY = True

`isort <http://pypi.python.org/pypi/isort>`_, a python tool to sort imports can be configured to sort exactly as described above.

Add the following::

    [settings]
    force_alphabetical_sort = True
    force_single_line = True
    lines_after_imports = 2
    line_length = 200
    not_skip = __init__.py

To either ``.isort.cfg`` or changing the header from ``[settings]`` to ``[isort]`` and putting it on ``setup.cfg``.

You can also use `plone.recipe.codeanalysis <http://pypi.python.org/pypi/plone.recipe.codeanalysis>`_ with the `flake8-isort <https://pypi.python.org/pypi/flake8-isort>`_ plugin enabled to check for it.


Declaring dependencies
======================

All direct dependencies should be declared in ``install_requires`` or ``extras_require`` sections in ``setup.py``.
Dependencies, which are not needed for a production environment (like "develop" or "test" dependencies) or are optional (like "Archetypes" or "Dexterity" flavors of the same package) should go in ``extras_require``.
Remember to document how to enable specific features (and think of using ``zcml:condition`` statements, if you have such optional features).

Generally all direct dependencies (packages directly imported or used in ZCML) should be declared, even if they would already be pulled in by other dependencies.
This explicitness reduces possible runtime errors and gives a good overview on the complexity of a package.

For example, if you depend on ``Products.CMFPlone`` and use ``getToolByName`` from ``Products.CMFCore``, you should also declare the ``CMFCore`` dependency explicitly, even though it's pulled in by Plone itself.
If you use namespace packages from the Zope distribution like ``Products.Five`` you should explicitly declare ``Zope`` as dependency.

Inside each group of dependencies, lines should be sorted alphabetically.


Versioning scheme
=================

For software versions, use a sequence-based versioning scheme, which is `compatible with setuptools <http://pythonhosted.org/setuptools/setuptools.html#specifying-your-project-s-version>`_::

    MAJOR.MINOR[.MICRO][.STATUS]

The way, setuptools interprets versions is intuitive::

    1.0 < 1.1.dev < 1.1.a1 < 1.1.a2 < 1.1.b < 1.1.rc1 < 1.1 < 1.1.1

You can test it with setuptools::

    >>> from pkg_resources import parse_version
    >>> parse_version('1.0') < parse_version('1.1.dev')
    ... < parse_version('1.1.a1') < parse_version('1.1.a2')
    ... < parse_version('1.1.b') < parse_version('1.1.rc1')
    ... < parse_version('1.1') < parse_version('1.1.1')
    True

``dev`` and ``dev0`` are treated as the same::

    >>> parse_version('1.1.dev') == parse_version('1.1.dev0')
    True

Setuptools recommends to separate parts with a dot.
The website about `semantic versioning <http://semver.org/>`_ is also worth a read.


Concrete Rules
==============

- Do not use tabs in Python code!
  Use spaces as indenting, 4 spaces for each level.
  We don't **"require"** `PEP8 <http://www.python.org/dev/peps/pep-0008/>`_, but most people use it and it's good for you.

- Indent properly, even in HTML.

- Never use a bare except.
  Anything like ``except: pass`` will likely be reverted instantly.

- Avoid ``tal:on-error``, since this swallows exceptions.

- Don't use ``hasattr()`` - this swallows exceptions, use ``getattr(foo, 'bar', None)`` instead.
  The problem with swallowed exceptions is not just poor error reporting.
  This can also mask ``ConflictErrors``, which indicate that something has gone wrong at the `ZODB level <http://developer.plone.org/troubleshooting/transactions.html#conflicterror>`_!

- Never put any HTML in Python code and return it as a string.
  There are exceptions, though.

- Do not acquire anything unless absolutely necessary, especially tools.
  For example, instead of using ``context.plone_utils``, use::

    from Products.CMFCore.utils import getToolByName
    plone_utils = getToolByName(context, 'plone_utils')

- Do not put too much logic in ZPT (use `Views <http://developer.plone.org/views/index.html>`_ instead!)

- Remember to add `i18n <http://developer.plone.org/i18n/index.html>`_ tags in ZPTs and Python code.
