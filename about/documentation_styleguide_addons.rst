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

* Do not link files from outsite your '/docs/source' directory, this will break the build
* Please do not use 'autodoc' to include comments for your Code, this will break too !
* Please follow our :doc:`styleguide </styleguide>` and use **semantic linefeeds**

.. todo:
    finish this and link to our mr.gutenberg
    - we do not link to files outsite
    - do not use autodoc, please
    - follow the writng and style guide [syantec lines]
    - if youinclude images have one folder for example _images, you may have robot test in the future
