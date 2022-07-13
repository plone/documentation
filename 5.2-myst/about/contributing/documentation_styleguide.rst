========================
Documentation Styleguide
========================

.. topic:: Description

   A guide on how to write Documentation for Plone and for Plone Add-ons


Introduction
============

Having a "best practices" approach for writing your documentation will benefit the users and the community at large.

Even better: when there is a clear structure and style for your documentation, the chances that other people will help improve the documentation increase!

Further advantages of following this guide:

* The documentation can be included on `docs.plone.org <http://docs.plone.org>`_
* It will be in optimal format to be translated with tools like `Transifex <https://www.transifex.com/>`_.

Tone
----

Guides should be informational, but friendly.

Use the active voice whenever possible.
Pronouns are acceptable (in particular, the use of "you" in regards to the reader).

Avoid contractions, and spell out the words.
For example, use "do not" instead of "don't".
See also :doc:`/about/contributing/word_choice`.

Use common sense – if a term is related to a high-level concept that fewer people would know, then take a sentence or two to explain it.

Avoid using "we" users are more engaged with documentation when you use second person (that is, you address the user as "you").

Writing in second person has the following advantages:

- Second person promotes a friendly tone by addressing users directly.

- Using second person with the imperative mood (in which the subject you is understood) and active voice helps to eliminate wordiness and confusion about who or what initiates an action, especially in procedural steps.

Line Length
-----------

- Please do not follow `PEP8 <https://www.python.org/dev/peps/pep-0008/#maximum-line-length>`_ maximum line length standard.
  Documentation is narrative text and images, not Python code.

- One sentence per line.

- Keep sentences short and understandable.

- Keep in mind that your sentences will become .po strings for translation.

This will greatly improve the editing and maintenance of your documentation.

Take this example paragraph::

    Patterns can take options in two ways: from the DOM or via the jQuery interface.
    It is highly recommended to use the DOM interface, since it offers a lot more flexibility compared to the jQuery approach.

    Also if you wish to use the automatic binding and rebinding functionality, the DOM approach is more straightforward and hassle-free.


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
-----------------------

* All documentation should be written in **valid** `reStructuredText <http://docutils.sourceforge.net/rst.html>`_.
  There are some :doc:`helper_tools` available.

* The top level of your package should contain the following documentation-related files:

  - ``README.rst`` — This should be a **short** description of your add-on, not the entire documentation!
    See the :ref:`styleguide-readme-example`.

  - ``CHANGES.rst`` — This should track the feature changes in your add-on.
    See :doc:`changelog-example`.

  - ``CONTRIBUTORS.rst`` — This should list the people writing, translating, and otherwise contributing to your package.

* All of your (longer) end-user documentation should go into the ``/docs/`` subdirectory.
  Feel free to split your documentation into separate files, or even further subdirectories, if it helps clarity.

* Make **absolutely** sure there is a start page called ``index.rst``.
  It is also a *really* good idea to have that include a Table of Contents.
  See :ref:`styleguide-toc-example`.

* Use relative links for internal links within your ``/docs/`` directory when referencing images, for instance.

* If you want to include images and screenshots, you should place them into ``/docs/resources/``, along with other resources, such as PDFs, audio, video, and so on.

* Please do not symlink to, or use the ``include`` directive on, files that live outside your ``/docs/`` directory.

* Please do not use ``autodoc`` to include comments of your code.

* The ``/docs/`` directory should contain content **only** related to documentation.
  Please do **not** put the license here.
  A ``LICENSE.rst`` with a short description of the license, and ``LICENSE.GPL`` for the legalese should go into the top level of your package next to your ``README.rst``.

* Usage of `Sphinx <http://sphinx-doc.org/>`_ within your project is optional, but if you want your add-on to (also) be documented, for instance on `Read The Docs <https://readthedocs.org/>`_, it is highly recommended.
  Put the associated ``Makefile`` and ``conf.py`` into the ``/docs/`` directory.


.. note::

   If you use `bobtemplates.plone <https://github.com/plone/bobtemplates.plone>`_ to generate the layout of your add-on, the recommended files will already be there, and in the right place.
   You will still have to write the content, though.


.. _styleguide-toc-example:


