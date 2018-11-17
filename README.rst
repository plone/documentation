=====================
Plone 6 Documentation
=====================

   Note: This is a complete rewrite of the whole Plone documentation.

Dependencies
============

- `Docker <https://docker.com>`_ (local building and testing)


Building
========

Local
-----

   Note: Please **do not** install, setup and run `Sphinx <http://www.sphinx-doc.org/en/master/>`_ via your OS package manager, buildout, pip or something else for this repository.

   **Please follow the docs below.**

Please make sure that you have `Docker <https://docker.com>`_ installed.

For building a HTML version, please run ``make html`` from within the top/root of this repository.

This will create the HTML files under *source/_build/html*.

Notes
=====

Be aware that for the time being (till we official announce and publish this branch) we use a
custom *robots.txt* to disallow crawling.

Support
=======

If you are having issues, please let us know.

We have a community space at: `community.plone.org/c/documentation <https://community.plone.org/c/documentation>`_.

License
=======

The *content* of the documentation is licensed under the
`Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_ by the `Plone Foundation <https://plone.org>`_.

The software project to *generate* the docs is licensed under the GPLv2.

Maintained by the Plone Docs-Team.
