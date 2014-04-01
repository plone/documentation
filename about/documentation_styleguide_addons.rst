=====================================
Documentation Styleguide for Add ons
=====================================

.. admonition:: Description

    A guide to write Documentation for Plone Add-ons

.. contents:: :local:

Introduction
============

Having a 'best practices' approach for writing your documentation will benefit the users of your add-on, and the community at large.

Even better: when there is a clear structure and style for your documentation, the chances that other people will help improve the documentation increase!

Further advantages of following this guide:

* The documentation can be included on `docs.plone.org <http://docs.plone.org>`_
* It will be in optimal format to be translated with tools like `Transifex <https://www.transifex.com/>`_.
* Unicorns will come and play in your garden. No, *really*.



Best practices
===============

For including documentation into docs.plone.org, **please** follow these guidelines:

* Please do not link files from outsite your '/docs/source' directory. Linking *the other way around* is fine. So, if you create a README.rst, do it in the /docs/source directory, and make a symlink to it from the root of your repository. Github will display that one just fine.
* Please do not use 'autodoc' to include comments of your code.
* Please follow this :doc:`ReST styleguide <styleguide>` and use **semantic linefeeds**. Do **not** break your sentences into half with newlines because you somehow think you should follow PEP8.

*Your documentation is not code.*

Let's repeat that, shall we?

**Your documentation is not code.**

It needs to be translatable. No, not into PHP, but into Chinese, Catalan, Klingon, ...

Think about it this way: each sentence in the documentation can be turned into a .po string.
Breaking sentences with linebreaks would mean a translator will only see part of the sentence, making it impossible to translate.






Styleguide
==========

* All documentation should be written in **valid** `ReStructuredText <http://docutils.sourceforge.net/rst.html>`_
* All documentation should be in the folder */docs/source*
* It's good practice to have a README.rst and a CHANGES.rst file in the top level of your package. If you want that information to also be available in the documentation on docs.plone.org, you should move those files into the /docs/source directory, and then make a symlink in the root of your package. Don't forget to update setup.py if you're using these files as long_description!!
* that README.rst should just contain a **short** description of your package, what it does, and the requirements. Do **not** put your entire documentation in it.
* The documentation goes into /docs/source/\*.rst. Make sure the starting page of your doc is called index.rst. Create multiple pages if it makes your documentation clearer.
* If you want to include images (*Yes! We love you! But do remember, .png or .jpg, no .gif please*), you should place them into /docs/_images
* You should use `Sphinx <http://sphinx-doc.org/>`_

Directory Structure
=====================

* You should configure Sphinx in that way that you have a seperate */source* directory for your documentation .rst files

.. code-block:: rst

    source
    $YOUR_PROJECT/docs/source

* /docs could contain your Makefile and conf.py

* /docs/_images should *only* contain images

* /docs/source should *only* contain your documentation written in rst. Use .rst as the file extension.

* use relative links for internal links within your /docs/source directory, to include images for instance.

* make sure all .rst files are referenced with a Table of Contents directive, like this example:

.. code-block:: rst

   .. toctree::
      :maxdepth: 2

      quickstart
      working_examples
      absolutely_all_options_explained
      how_to_contribute



