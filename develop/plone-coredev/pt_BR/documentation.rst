Writing documentation
=====================

Documentation of Plone
----------------------

As a community, Plone maintains several types of documentation:

* *Curated* documents. This is a limited set of documentation that is intended to be carefully managed and regularly updated.

  * `User Manual <http://plone.org/documentation/manual/plone-4-user-manual>`_
  * `Installing Plone <http://plone.org/documentation/manual/installing-plone>`_
  * `Theme Reference <http://plone.org/documentation/manual/theme-reference>`_
  * `Developer Manual <http://plone.org/documentation/manual/developer-manual>`_

  Improvements to the curated documents can be discussed on the `plone-docs mailing list <https://lists.sourceforge.net/lists/listinfo/plone-docs>`_.

* *Community-edited* documents. These are open for contributions by anyone. This leads to a wealth of information that is of more widely ranging quality.

  * `Knowledgebase on plone.org <http://plone.org/documentation/kb>`_. Anyone with a plone.org account is free to edit.
  * `Collective Plone developer documentation <http://collective-docs.readthedocs.org/en/latest/index.html>`_. Anyone may `contribute <http://collective-docs.readthedocs.org/en/latest/introduction/developermanual.html>`_.

Documenting a package
---------------------

The basics
~~~~~~~~~~

At the very least, your package should include the following forms of documentation:

  ``README.rst``
    The readme is the first entry point for most people to your package. It will be included on the PyPI page for your egg, and on the front page of its github repository. It should be formatted using `reStructuredText (reST) <http://docutils.sourceforge.net/rst.html>`_ in order to get formatted properly by those systems.

    ``README.rst`` should include:

    * A brief description of the package's purpose
    * Installation information (How do I get it working?)
    * Compatibility information (what versions of Plone does it work with?)
    * Links to other sources of documentation
    * Links to issue trackers, mailing lists, and other ways to get help.

  The manual (a.k.a. narrative documentation)

    The manual goes into further depth for people who want to know all about how to use the package.

    It includes topics like:

    * What the features are
    * How to use them (in English—not doctests!)
    * Information about architecture
    * Common gotchas

    The manual should consider various audiences who may need different types of information:

    * End users who use Plone for content editing but don't manage the site.
    * Site administrators who install and configure the package.
    * Integrators who need to extend the functionality of the package in code.
    * Sysadmins who need to maintain the server running the software.

    Simple packages with limited functionality can get by with a single page of narrative documentation. In this case it's simplest to include it in an extended ``README.rst``. Some excellent examples of a single-page readme are http://pypi.python.org/pypi/plone.outputfilters and https://github.com/plone/plone.app.caching

    If your project is moderately complex, you may want to set up your documentation with multiple pages. The best way to do this is to add Sphinx to your project and host your docs on readthedocs.org so that it rebuilds the documentation whenever you push to github. If you do this, your ``README.rst`` must link off site to the documentation.

  Reference (a.k.a. API documentation)

    An API reference provides information about the package's public API (that is, the code that the package exposes for use from external code.) It is meant for random access to remind the reader of how a particular class or method works, rather than for reading in its entirety.

    If the codebase is written with docstrings, API documentation can be automatically generated using Sphinx.

  ``CHANGES.txt``
    The changelog is a record of all the changes made to the package and who made them, with the most recent changes at the top. This is maintained separately from the git commit history to give a chance for more user-friendly messages and to and record when releases were made.

    A changelog looks something like::

      Changelog
      =========

      1.0 (2012-03-25)
      ----------------

      * Documented changelogs.
        [davisagli]

    See https://raw.github.com/plone/plone.app.caching/master/CHANGES.rst for a full example.

    If a change was related to a bug in the issue tracker, the changelog entry should include a link to that issue.

  Licenses
    Information about the open source license used for the package should be placed within the ``docs`` directory.

    For Plone core packages, this includes ``LICENSE.txt`` and ``LICENSE.GPL``.


Using Sphinx
~~~~~~~~~~~~

reST References:
 * `Plone Oriented Shpinx Documentation <http://collective-docs.plone.org/en/latest/introduction/writing.html>`_
 * `Sphinx reST Primer <http://sphinx.pocoo.org/rest.html>`_ 

To add Sphinx to your package...
