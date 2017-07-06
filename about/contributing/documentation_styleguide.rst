========================
Documentation Styleguide
========================

.. topic:: Description

   A guide to write Documentation for Plone and for Plone Add-ons


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

**Your documentation is not code.**

It needs to be translatable. No, not into PHP, but into Chinese, Catalan, Klingon, ...

Think about it this way:

Each sentence in the documentation can be turned into a .po string.

Breaking sentences with linebreaks would mean a translator will only see part of the sentence, making it impossible to translate.

Documentation Structure & Styleguide
====================================

For including documentation into docs.plone.org, **please** follow these guidelines:


* All documentation should be written in **valid** `ReStructuredText <http://docutils.sourceforge.net/rst.html>`_  There are some :doc:`helper_tools` available.

* The top level of your package should contain the following documentation-related files:

  - README.rst   This should be a **short** description of your add-on, not the entire documentation!
    See the :ref:`styleguide-readme-example`

  - CHANGES.rst  This should track the feature changes in your add-on, see :ref:`styleguide-changes-example`

  - CONTRIBUTORS.rst  This should list the people writing, translating and otherwise contributing

* All of your (longer) end-user documentation should go into the /docs subdirectory. Feel free to split your documentation into separate files, or even further subdirectories if it helps clarity.

* Make **absolutely** sure there is a start page called index.rst.
  It is also usually a *really* good idea to have that include a Table of Content, see :ref:`styleguide-toc-example`

* use relative links for internal links within your /docs/ directory, to include images for instance.

* If you want to include images and screenshots, you should place them into /docs/resources/ , along with other resources like PDF's, audio, video, etcetera.
  (*Yes! Make more screenshots, we love you! But do remember, .png or .jpg as file formats, no .gif please*)

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

   If you use `bobtemplates.plone <https://github.com/plone/bobtemplates.plone>`_ to generate the layout of your add-on, the recommended files will already be there, and in the right place. You'll still have to write the content, though.


.. _styleguide-toc-example:

Table Of Contents For Your Documentation
========================================

Make sure all .rst files are referenced with a Table of Contents directive, like this example:

.. code-block:: rst

   .. toctree::
      :maxdepth: 2

      quickstart
      working_examples
      absolutely_all_options_explained
      how_to_contribute


.. note::

   The files themselves will have an extension of .rst, but you don't specify that extension in the toctree directive.
