============================
ReStructuredText Style Guide
============================

.. admonition:: Description

   How to write content for the Plone Documentation.


Introduction
============

This chapter explains the basics of editing, and updating to the *Plone Documentation*.


.. note::

  All pages should be in ReStructured Text, and have a .rst extension.
  Images should be in .png, or .jpg format.
  Please, don't use .gif, because the PDF-generating software has issues with that.


Line Length & Translations
==========================

Documentation is not code. Repeat after us: **Documentation is not code.**

Documentation should **not** follow `PEP8 <https://www.python.org/dev/peps/pep-0008/>`_ or other arbitrary conventions.

.. note::

  **Remember :** This documentation is set up so it is fully translatable by using standard tools like transifex.

  Your sentences will become .po strings, to be translated.

  Now, think about how translations would work if the translator can only see an arbitrary part of a sentence. Translating is hard enough without creating additional problems...

If you want to keep short lines:

Use `semantic linefeeds <http://rhodesmill.org/brandon/2012/one-sentence-per-line/>`_
when you are editing restructured text (or any other interpreted rich text format) because it will greatly improve the editing and maintenance of your documents.

Take this example paragraph::

    Patterns can take options in two ways:
    from the DOM or via the jQuery interface.
    It is highly recommended to use the DOM interface,
    since it offers a lot more flexibility compared to the jQuery approach.
    Also,
    if you wish to use the automatic binding and rebinding functionality,
    the DOM approach is more straightforward and hassle-free.

Notice how it's easier to just reshuffle sentences and add stuff if, instead of using your editor "autowrap" feature,
you manually insert line breaks after full stops, commas, or upon "grammatical" boundaries (and not merely word ones).

Do not be afraid to use more than 80 characters.


Document Page Format
====================

Here are some Sphinx coding conventions used in the documentation.

Tab Policy
----------

* Indentation 4 spaces

* No hard tabs

* No trailing whitespaces

Headings And Filenames
----------------------

* For the headings, capitalize the first letter only

* For the filenames, use_underscore_naming_style

Page Structure
--------------

Each page should contain, in this order:

* The main heading. This will be visible in the table of contents:

.. code-block:: rst

   ==================================
   Writing and updating this document
   ==================================

* The description of the page, which will appear in Plone's *Description* Dublin Core metadata field.
  This created using the reST *admonition* directive. A single paragraph of text consisting of 1-3 sentences is recommended, so that the same text fits into the search engine results (Google):

.. code-block:: rst

   .. admonition:: Description

      This text will go to Plone's pages description field. It will appear in the search engine listings for the page.


Introduction paragraph: A brief overview:

.. code-block:: rst

   Introduction
   ------------

   This chapter will describe the basics of how to contribute to this document.

A number of paragraphs: The actual content of the document page:

.. code-block:: rst

   Contributions needed
   --------------------

   Below is the list of documentation and references we'd like to see

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

reStructuredText and Sphinx enable any style you would prefer for the various heading level you would need.
For example, underlining level 1 headings with ``.``, level 2 headings with ``#`` and level 3 headings with ``|`` is perfectly valid as far as ``docutils`` is concerned.

Unfortunately this is not the same for a human documentation maintainer.

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

Sphinx can use two link styles, inline and via a link at the end of the page. Please **do not** separate the link and the target definition, please **only** use inline links like this:

.. code-block:: rst

   `Example <https://example.com>`_

otherwise the URL is not attached to the context it is used in, and that makes it harder for translators to use the right expressions.


Topic
=====

A topic is like a block quote with a title, or a self-contained section with no subsections.

Use the "topic" directive to indicate a self-contained idea that is separate from the flow of the document. Topics may occur anywhere a section or transition may occur. Body elements and topics may not contain nested topics.

The directive's sole argument is interpreted as the topic title; the next line must be blank.

All subsequent lines make up the topic body, interpreted as body elements. For example:

.. code-block:: rst

    .. topic:: Topic Title

        Subsequent indented lines comprise
        the body of the topic, and are
        interpreted as body elements.

Syntax Highlighting
===================

Sphinx does syntax highlighting using the `Pygments <http://pygments.org/>`_ library.

You can specify different highlighting for a code block using the following syntax::

    With two colons you start a code block using the default highlighter::

        # Some Python code here
        # The language defaults to Python, we don't need to set it
        if 1 == 2:
            pass


You can specify the language used for syntax highlighting by using the ``code-block`` directive:

.. code-block:: rst

   .. code-block:: python

       if "foo" == "bar":
           # This is Python code
           pass

For example, to specify XML:

.. code-block:: rst

   .. code-block:: xml

       <somesnippet>Some XML</somesnippet>

... or UNIX shell:

.. code-block:: rst

   .. code-block:: shell

      # Start Plone in foreground mode for a test run
      cd ~/Plone/zinstance
      bin/plonectl fg

... or a buildout.cfg:

.. code-block:: rst

   .. code-block:: ini

      [some-part]
      # A random part in the buildout
      recipe = collective.recipe.foo
      option = value

... or interactive Python:

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

... or JavaScript:

.. code-block:: javascript

    .. code-block:: javascript

    var $el = $('<div/>');
    var value = '<script>alert("hi")</script>';
    $el.text(value);
    $('body').append($el);

Setting the highlighting mode for the whole document:

.. code-block:: rst

   .. highlight:: shell

   All code blocks in this doc use console highlighting by default::

      some shell commands

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

Inline code highlighting:

.. code-block:: rst

   This is :func:`aFunction`, this is the :mod:`some.module` that contains the :class:`some.module.MyClass`

.. note::

   These Python objects are rendered as hyperlinks if the symbol is mentioned in a relevant directive.
   See
   http://sphinx-doc.org/domains.html and
   http://sphinx-doc.org/ext/autodoc.html

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
