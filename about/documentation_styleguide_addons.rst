=====================================
Documentation Styleguide for Add ons
=====================================

.. admonition:: Description

    A guide to write Documentation for Add ons

.. contents:: :local:

Introduction
============

We want to have a 'unified documentation' reasons for that are

* reason1
* reason2
* reason3

Styleguide
----------

* All documentation should be written in **valid** `rest <http://docutils.sourceforge.net/rst.html>`_
* All documentation should be in the folder */docs/source*
* If you want to include images, you should place them into _images
* You should use `Sphinx <http://sphinx-doc.org/>`_

Structure
---------

* You should configure Sphinx in that way that you have a seperate */source* directory for your documentation .rst files

.. code-block:: rst

    source
    $YOUR_PROJECT/docs/source

    /docs could contain your Makefile and conf.py

    /docs/_images should *only* contain images

    /source should *only* contain your documentation written in rst

Best practices
--------------

For including documentation into docs.plone.org, **please** follow these guidelines:

* Please do not link files from outsite your '/docs/source' directory !
* Please do not use 'autodoc' to include comments of your Code !
* Please follow our :doc:`styleguide </styleguide>` and use **semantic linefeeds**

