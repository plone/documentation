======================================
Helper Tools For Writing Documentation
======================================

.. admonition:: Description

   Tools and Plugins which will help to write documentation.


Online Tools
============

- `rst.ninjs.org <http://rst.ninjs.org/>`_ and a fork with more Sphinx support at `livesphinx.herokuapp.com <http://livesphinx.herokuapp.com/>`_
- `notex.ch <https://www.notex.ch/>`_


Offline Tools
=============

**ReText** is an editor for **.rst** and **.md** formats.
On Ubuntu and Debian-based systems all you have to do is

.. code-block:: console

   apt-get install retext


**Pandoc** If you have existing documentation, you may want to check out `pandoc <http://johnmacfarlane.net/pandoc/>`_ , the "swiss army knife" of document conversions. For instance, it can create valid rst files from Markdown and many other formats.
On Ubuntu you can install it via apt

.. code-block:: console

    apt-get install pandoc

See also the `online version <http://johnmacfarlane.net/pandoc/try/>`_.


**Sublime Text** has a number of plugins for rst highlighting and snippets, install via the Sublime package installer.

`Restructured Text Snippets <https://packagecontrol.io/packages/Restructured%20Text%20(RST)%20Snippets>`_, which has automated header creation, html preview and more.

The *SublimeLinter* framework also comes with two plugins: `sublimelinter-rst <https://packagecontrol.io/packages/SublimeLinter-rst>`_ will error check RST files, and `write good <https://packagecontrol.io/packages/SublimeLinter-contrib-write-good>`_ checks your English for writing style.

When not using the Snippets, but you still want to check how the html would look, `OmniMarkupPreviewer <https://sublime.wbond.net/packages/OmniMarkupPreviewer>`_  is a live previewer/exporter for markup files (markdown, rst, creole, textile...).

Watch `the video <https://www.youtube.com/watch?v=3fWLuqyc3Oc>`_ on YouTube.

**Emacs** has a `rst-mode <http://docutils.sourceforge.net/docs/user/emacs.html>`_.
This mode comes with some Emacs distros. Try ``M-x rst-mode`` in your Emacs and enjoy syntax coloration, underlining a heading with ``^C ^A``

Another tool for Emacs is `Flycheck <https://flycheck.readthedocs.org/en/latest/index.html>`_.

**Eclipse** users can install **ReST Editor** through the Eclipse
Marketplace.

**Vim** does syntax highlighting for RST files.
There is a plugin called `vim-markdown <https://github.com/plasticboy/vim-markdown>`_.

If you prefer a more *advanced* plugin with enhanced functionalities you could use `Riv <https://github.com/Rykka/riv.vim>`_.

**Restview** `ReStructuredText viewer <https://pypi.python.org/pypi/restview>`_
A viewer for ReStructuredText documents that renders them on the fly.

.. code-block:: console

    pip install restview

Language Tools
==============

These tools can help you to check for grammatical mistakes and typos, you should always use a spell checker anyway!

**LanguageTool** is an Open Source proofreading software for English, French, German, Polish and more than 20 other languages.
See `www.languagetool.org <https://www.languagetool.org/>`_.

**After the Deadline** `is a language checker for the web <http://www.afterthedeadline.com/>`_.
This tool is also available in your Plone sites, see the :doc:`content quality </working-with-content/content-quality/index>` section
