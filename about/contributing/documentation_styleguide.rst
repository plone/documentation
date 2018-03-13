========================
Documentation Styleguide
========================

.. topic:: Description

   A guide on how to write Documentation for Plone and for Plone Add-ons


Introduction
============

Having a 'best practices' approach for writing your documentation will benefit the users and the community at large.

Even better: when there is a clear structure and style for your documentation, the chances that other people will help improve the documentation increase!

Further advantages of following this guide:

* The documentation can be included on `docs.plone.org <http://docs.plone.org>`_
* It will be in optimal format to be translated with tools like `Transifex <https://www.transifex.com/>`_.

Tone
----

Guides should be informational, but friendly.

Use the active voice whenever possible, and contractions and pronouns are acceptable (in particular, the use of you in regards to the reader).

Use common sense – if a term is related to a high-level concept that fewer people would know, then take a sentence or two to explain it.

Avoid using "we" users are more engaged with documentation when you use second person (that is, you address the user as “you”).

Writing in second person has the following advantages:

- Second person promotes a friendly tone by addressing users directly.

- Using second person with the imperative mood (in which the subject you is understood) and active voice helps to eliminate wordiness and confusion about who or what initiates an action, especially in procedural steps.

Line Length
-----------

- Please do not follow `PEP8 <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_ maximum line length standard.

- Keep sentences short and sentences and understandable .

- Use `semantic linefeeds <http://rhodesmill.org/brandon/2012/one-sentence-per-line/>`_ when you are editing.

- Keep in mind that your sentences will become .po strings, for translation.

- One sentence per line.


This will greatly improve the editing and maintenance of your documents.

Take this example paragraph::

    Patterns can take options in two ways:
    from the DOM or via the jQuery interface.
    It is highly recommended to use the DOM interface,
    since it offers a lot more flexibility compared to the jQuery approach.

    Also, if you wish to use the automatic binding and rebinding functionality,
    the DOM approach is more straightforward and hassle-free.

Please do not follow `PEP8 <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_ maximum line length standard.

Limiting lines to a maximum of 130 characters.

Tab Policy
----------

* Indentation 4 spaces

* No hard tabs

* No trailing whitespaces

Headings And Filenames
----------------------

* Start capitals – capitalization of all words, regardless of the part of speech.

* For the filenames, use-dash-naming-style

Documentation Structure
=======================

For including documentation into docs.plone.org, **please** follow these guidelines:


* All documentation should be written in **valid** `ReStructuredText <http://docutils.sourceforge.net/rst.html>`_  There are some :doc:`helper_tools` available.

* The top level of your package should contain the following documentation-related files:

  - README.rst   This should be a **short** description of your add-on, not the entire documentation!
    See the :ref:`styleguide-readme-example`

  - CHANGES.rst  This should track the feature changes in your add-on, see :doc:`changelog-example`

  - CONTRIBUTORS.rst  This should list the people writing, translating and otherwise contributing

* All of your (longer) end-user documentation should go into the /docs subdirectory. Feel free to split your documentation into separate files, or even further subdirectories if it helps clarity.

* Make **absolutely** sure there is a start page called index.rst.
  It is also usually a *really* good idea to have that include a Table of Content, see :ref:`styleguide-toc-example`

* use relative links for internal links within your /docs/ directory, to include images for instance.

* If you want to include images and screenshots, you should place them into /docs/resources/ , along with other resources like PDF's, audio, video, etcetera.

* Please do not symlink to, or use the *include* directive on files that live outside your '/docs' directory.

* Please do not use 'autodoc' to include comments of your code.

* The '/docs' directory should contain **only** content related to documentation, please do **not** put the license here.
  A LICENSE.rst with a short description of the license, and LICENSE.GPL for the legalese should go into the top level of your package next to your README.rst

* Please follow this :doc:`rst-styleguide` and use **semantic linefeeds**.
  Do **not** break your sentences into half with newlines because you somehow think you should follow PEP8.
  PEP8 is for Python files, not for ReStructuredText.

* Please follow our :doc:`word_choice`.

* Usage of `Sphinx <http://sphinx-doc.org/>`_ within your project is optional, but if you want your add-on to (also) be documented for instance on `Read The Docs <https://readthedocs.org/>`_ it is highly recommended.
Put the associated Makefile and conf.py into the /docs directory.


.. note::

   If you use `bobtemplates.plone <https://github.com/plone/bobtemplates.plone>`_ to generate the layout of your add-on,
   the recommended files will already be there, and in the right place.

   You'll still have to write the content, though.


.. _styleguide-toc-example:


