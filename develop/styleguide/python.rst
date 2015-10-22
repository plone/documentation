=================
Python styleguide
=================


Introduction
==============

We've modeled the following rules and recommendations based on the following
documents:

 * `PEP8 <http://www.python.org/dev/peps/pep-0008>`__
 * `PEP257 <http://www.python.org/dev/peps/pep-0257>`_
 * `Rope project <http://rope.sourceforge.net/overview.html>`_
 * `Google Style Guide <http://google-styleguide.googlecode.com/svn/trunk/pyguide.html>`_
 * `Pylons Coding Style <http://docs.pylonsproject.org/en/latest/community/codestyle.html>`_
 * `Tim Pope on Git commit messages <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`__

Line length
===========

All Python code in this package should be PEP8 valid.
This includes adhering to the 80-char line length.
If you absolutely need to break this rule, append ``# noPEP8`` to the offending line to skip it in syntax checks.

.. note::
    Configuring your editor to display a line at 79th column helps a lot
    here and saves time.

.. note::
    The line length rule also applies to non-python source files, such as ``.zcml`` files,
    but is a bit more relaxed there.
    It explicitly **does not** aply to documentation ``.rst`` files.
    For rst files, use *semantic* linebreaks.
    See `the Plone rst styleguide <http://docs.plone.org/about/rst-styleguide.html#line-length-translations>`_ for the reasoning behind it.

Breaking lines
--------------

Based on code we love to look at (Pyramid, Requests, etc.), we allow the following two styles for breaking long lines into blocks:

1. Break into next line with one additional indent block.

   .. sourcecode:: python

       foo = do_something(
           very_long_argument='foo', another_very_long_argument='bar')

       # For functions the ): needs to be placed on the following line
       def some_func(
           very_long_argument='foo', another_very_long_argument='bar'
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

- E721: Use `isinstance()` instead of comparing types directly. (There
  are uses of this in for example GenericSetup and plone.api that must
  not be fixed.)

- E711: Fix comparison with None.  (This can break SQLAlchemy code.)

You can check what would be changed by one specific code::

    autopep8 --diff --select E309 -r .

Indentation
===========

For Python files, we stick with the `PEP 8 recommondation
<http://www.python.org/dev/peps/pep-0008/#indentation>`_: Use 4 spaces per
indentation level.

For ZCML and XML (GenericSetup) files, we recommend the `Zope Toolkit's coding
style on ZCML <http://docs.zope.org/zopetoolkit/codingstyle/zcml-style.html>`_
::

  Indentation of 2 characters to show nesting, 4 characters to list attributes
  on separate lines. This distinction makes it easier to see the difference
  between attributes and nested elements.
