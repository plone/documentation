===
SQL
===

.. admonition:: Description

        Using SQL databases (MySQL, PostgreSQL, others) in Plone


Introduction
============

If you are building the codebase Plone behaves as any other Python application.

* Write your SQL related code using known available Python SQL libraries and frameworks

* Plug your code to Plone HTML pages through :doc:`views </develop/plone/views/browserviews>`

Example Python SQL libraries

* http://www.sqlalchemy.org/

ZSQL
====

ZSQL is something probably written before you knew what SQL is.
Never ever use ZSQL in new code. It's not following any modern best practices
and has history of 1990s code. You have been warned. Stay away. The grue is near.


