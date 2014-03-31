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
* It will be in optimal format to be translated with tools like Transifex.
* Unicorns will come and play in your garden. No, *really*.

Styleguide
----------

* All documentation should be written in **valid** `ReStructuredText <http://docutils.sourceforge.net/rst.html>`_
* All documentation should be in the folder */docs/source*
* If you want to include images, you should place them into /docs/_images
* You should use `Sphinx <http://sphinx-doc.org/>`_

Structure
---------

* You should configure Sphinx in that way that you have a seperate */source* directory for your documentation .rst files

.. code-block:: rst

    source
    $YOUR_PROJECT/docs/source

* /docs could contain your Makefile and conf.py

* /docs/_images should *only* contain images

* /source should *only* contain your documentation written in rst

Best practices
--------------

For including documentation into docs.plone.org, **please** follow these guidelines:

* Please do not link files from outsite your '/docs/source' directory. Linking *the other way around* is fine. So, if you create a README.rst, do it in the /docs/source directory, and make a symlink to it from the root of your repository. Github will display that one just fine.
* Please do not use 'autodoc' to include comments of your code.
* Please follow this :doc:`ReST styleguide <styleguide>` and use **semantic linefeeds**. Do **not** break your sentences into half with newlines because you think you should follow PEP8.

*Your documentation is not code.* It needs to be translatable. No, not in PHP, but in Chinese, Catalan, Klingon, ...

