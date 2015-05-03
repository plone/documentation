======================================
Helper tools for writing Documentation
======================================

.. admonition:: Description

   Tools and Plugins which will help to write documentation.

.. contents:: :local:





Online tools:
-------------

- `rst.ninjs.org <http://rst.ninjs.org/>`_ and a fork with more Sphinx support at `livesphinx.herokuapp.com <http://livesphinx.herokuapp.com/>`_
- `notex.ch <https://notex.ch/>`_


Offline tools:
---------------

**ReText** is a handy editor for **.rst** and **.md** formats.
On Ubuntu and Debian-based systems all you have to do is

.. code-block:: rst

   apt-get install retext


**Pandoc** If you have existing documentation, you may want to check out `pandoc <http://johnmacfarlane.net/pandoc/>`_ , the "swiss army knife" of document conversions. For instance, it can create valid rst files from Markdown and quite a number of other formats.
On Ubuntu you can install it via apt

.. code-block:: rst

    apt-get install pandoc

There is also a `online version <http://johnmacfarlane.net/pandoc/try/>`_.


**Sublime Text** has a number of plugins for rst highlighting and snippets, install via the Sublime package installer.

One  particular which is really good for getting a impression how it will looks
like in html is `OmniMarkupPreviewer <https://sublime.wbond.net/packages/OmniMarkupPreviewer>`_ a live
previewer/exporter for markup files (markdown, rst, creole, textile...).

**Emacs** has a nice `rst-mode <http://docutils.sourceforge.net/docs/user/emacs.html>`_.
This mode comes with some Emacs distros. Try ``M-x rst-mode`` in your Emacs and enjoy syntax coloration, underlining a heading with ``^C ^A``

Another nice tool for Emacs is `Flycheck <https://flycheck.readthedocs.org/en/latest/index.html>`_.

**Eclipse** users can install **ReST Editor** through the Eclipse
Marketplace.

**Vim** does syntax highlighting for RST files.
There is a nice plugin called `vim-markdown <https://github.com/plasticboy/vim-markdown>`.

If you prefer a more *advanced* plugin with enhanced functionalities you could use `Riv <https://github.com/Rykka/riv.vim>`_.

**restview** `ReStructuredText viewer <https://pypi.python.org/pypi/restview>`_
A viewer for ReStructuredText documents that renders them on the fly.

.. code-block:: rst

    pip install restview

Language tools:
---------------

These tools can help you to check for grammatical mistakes and typos, you should always use a spell checker anyway!

**LanguageTool** is an Open Source proofreading software for English, French, German, Polish and more than 20 other languages.
See `www.languagetool.org <https://www.languagetool.org/>`_.

**After the Deadline** `is a language checker for the web <http://www.afterthedeadline.com/>`_.
This handy tool is also available in your Plone sites, by the way, see the :doc:`conent quality </working-with-content/content-quality/index>` section

