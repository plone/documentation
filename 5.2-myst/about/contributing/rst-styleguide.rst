==========================
General Writing Guidelines
==========================

.. topic:: Description

   This page explains reST writing guidelines for the Plone documentation.

   Use your best judgment, and feel free to propose changes to this document in a pull request.


Overview
========

- All pages should be in ReStructured Text, and have a .rst extension.

- Images should be in .png, or .jpg format.

- Please, don't use .gif, because the PDF-generating software has issues with that.


Document Page Format
====================

Here are some Sphinx coding conventions used in the documentation.


Table Of Contents
-----------------

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


Page Structure
--------------

Each page should contain, in this order:

* The main heading. This will be visible in the table of contents:

.. code-block:: rst

   ==================================
   Writing And Updating This Document
   ==================================

* A single paragraph of text consisting of 1-3 sentences is recommended, so that the same text fits into the search engine results:

.. code-block:: rst

   .. topic:: Description

      This text will go to Plone's pages description field.


A number of paragraphs: The actual content of the document page:

.. code-block:: rst

   Introduction
   ============

   Below is the list of documentation and references.

Section Structure
-----------------

Each section (folder) must contain

* :file:`index.rst` with:

* Section heading: This will be visible in the table of contents

* A single paragraph summarizing what this section is all about. This will be mapped to Plone folder description.

* Sphinx `toctree <http://www.sphinx-doc.org/en/stable/markup/toctree.html>`_  directive, maxdepth 2. Each ``.rst`` file in the folder should
  be linked to this toctree.

.. code-block:: rst

   .. toctree::
      :maxdepth: 2

      chapter1
      chapter2
      chapter3

Headings
========

Readers use the table of contents or scan through the headings to find the required content.
Therefore, headings must reflect the information that the readers search.

For having consistent heading styles in all files it is recommended to follow strictly the rules stated in the `Sphinx manual <http://sphinx-doc.org/rest.html#sections>`_.

As individual files do not have so called "parts" or "chapters", the headings would be underlined like this:

.. code-block:: rst

   ===
   One
   ===

   Two
   ===

   Three
   -----

   Four
   ~~~~

   Five
   ^^^^


Links
=====

Sphinx can use two link styles, inline and via a link at the end of the page.

Please **do not** separate the link and the target definition, please **only** use inline links like this:

.. code-block:: rst

   `Example <https://example.com>`_

otherwise the URL is not attached to the context it is used in, and that makes it harder for translators to use the right expressions.


Syntax Highlighting
===================

Sphinx does syntax highlighting using the `Pygments <http://pygments.org/>`_ library.

You can specify the language used for syntax highlighting by using the ``code-block`` directive:

Python
------

.. code-block:: rst

   .. code-block:: python

       if "foo" == "bar":
           # This is Python code
           pass

Interactive Python
------------------

.. code-block:: rst

   .. code-block:: pycon

      >>> class Foo:
      ...     bar = 100
      ...
      >>> f = Foo()
      >>> f.bar
      100
      >>> f.bar / 0
      Traceback (most recent call last):
        File "<stdin>", line 1, in <module>
      ZeroDivisionError: integer division or modulo by zero

XML
---

.. code-block:: rst

   .. code-block:: xml

       <somesnippet>Some XML</somesnippet>

UNIX Shell
----------

.. code-block:: rst

   .. code-block:: shell

      bin/plonectl fg

INI Files
---------

.. code-block:: rst

   .. code-block:: ini

      [some-part]
      # A random part in the buildout
      recipe = collective.recipe.foo
      option = value


JavaScript
----------

.. code-block:: rst

    .. code-block:: javascript

       var $el = $('<div/>');
       var value = '<script>alert("hi")</script>';
       $el.text(value);
       $('body').append($el);


If syntax highlighting is not enabled for your code block, you probably have a syntax error and `Pygments <http://pygments.org>`_ will fail silently.

Images
======

reST supports an image directive:

.. code-block:: rst

  .. image:: ../_static/plone_donut.png
     :alt: Picture of Plone Donut

When used within Sphinx, the file name given (here plone_donut.png) must either be relative to the source file,
or absolute which means that they are relative to the top source directory.

For example, the file sketch/spam.rst could refer to the image _static/plone_donut.png as ../_static/plone_donut.png or /_static/plone_donut.png.


Other Sphinx And ReStructured Text Source Snippets
==================================================

Italics:

.. code-block:: rst

   This *word* is italics.

Strong:

.. code-block:: rst

   This **word** is in bold text.

Labels for graphical user interfaces (GUI), including buttons, menu items, form controls, and links.

.. code-block:: rst

    Click the :guilabel:`Submit` button.

The above reStructuredText renders as follows.

Click the :guilabel:`Submit` button.

Inline code highlighting:

.. code-block:: rst

   This is :func:`aFunction`, this is the :mod:`some.module` that contains the :class:`some.module.MyClass`

.. note::

   These Python objects are rendered as hyperlinks if the symbol is mentioned in a relevant directive.

   See http://sphinx-doc.org/domains.html and http://sphinx-doc.org/ext/autodoc.html

Making an external link (note the underscore at the end):

.. code-block:: rst

   `This is an external link to <http://opensourcehacker.com>`_

Making an internal link:

.. code-block:: rst

   :doc:`This is a link to </introduction/writing.txt>`
   ...
   See also :ref:`somewhere` (assuming that a line containing only
   ``.. _somewhere:`` exists above a heading in any file of this
   documentation) ...
   And a link to the term :term:`foo` assuming that ``foo`` is defined in the glossary.

Glossary:

.. code-block:: rst

    .. glossary:: :sorted:

Bullet list:

.. code-block:: rst

   * First bullet
   * Second bullet with `a link <http://opensourcehacker.com>`_

Warning:

.. code-block:: rst

   .. warning::

      This is a warning box (yellow)

.. warning::

   This is a warning box (yellow)

.. code-block:: rst

   .. error::

      This is an error box (red)

.. error::

   This is an error box (red)

Note:

.. code-block:: rst

   .. note::

      This is a note box (blue)

.. note::

   This is a note box (blue)

.. code-block:: rst

   .. TODO::

      This is a TODO item

.. TODO::

   This is a TODO item

You can find a brief introduction to reStructuredText (reST) on http://www.sphinx-doc.org/en/stable/rest.html

Including Gists
----------------

Sometimes it is handy to include `gists <https://help.github.com/articles/about-gists/>`_.
This can be useful if you want to include for example a configuration file.

For including gists just use the *gist* directive

.. code-block:: rst

    .. gist:: https://gist.github.com/shomah4a/5149412

.. note::

    Since this documentation serves as source for various versions (html, PDF, others), please **always** include a link to the gist under the gist directive.
