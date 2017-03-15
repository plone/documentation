====================================
Importing content from other sources
====================================

.. admonition:: Description

	There are various tools to help you import content from other systems into Plone



Introduction
============

Rarely does a new website start all from scratch.
Most of the time, you will have to import content from other systems. These may include:

- other CMS systems, sometimes based on PHP/MySQL
- legacy sites in plain HTML
- resources that exist on a filesystem, such as files and images
- other Plone sites, including older and unmaintained versions

While Plone even comes with an FTP service, that can serve as a last-ditch effort to get some pictures in, there are far more sophisticated tools available.


Transmogrify
============

By far the most flexible tool available is something called **collective.transmogrifier**.

.. note::

	A transmogrifier is fictional device used for transforming one object into another object. The term was coined by Bill Waterson of Calvin and Hobbes fame.

In principle, what it does is to allow you to lay a 'pipeline', whereby an object (a piece of content) is transported. At each part of the pipeline, you can perform various operations on it: extract, change, add metadata, etcetera. These operations are in the form of so-called 'blueprints'.

In short: an object is gathered from a source you define. Then, it goes to one or more segments of the pipeline to let the various blueprints work on it, and in the end you use a 'constructor' to turn it into a Plone content object.

That's the basics, but by combining all your options you have an incredibly flexible and powerful tool at hand.

collective.transmogrifier
=========================

See the extensive documentation:

.. toctree::
   :maxdepth: 1

   /external/collective.transmogrifier/docs/source/index


Transmogrify helpers
====================

Various add-ons exist to make working with transmogrify easier:

- `mr.migrator <https://pypi.python.org/pypi/mr.migrator>`_ is a way to lay pipelines
- `funnelweb <https://pypi.python.org/pypi/funnelweb>`_ helps to parse static sites, and crawl external sites
- `parse2plone <https://pypi.python.org/pypi/parse2plone>`_ is meant to get HTML content from the file system into Plone

And a wide array of extra 'blueprints' exist, like

- `quintagroup.transmogrifier <https://pypi.python.org/pypi/quintagroup.transmogrifier>`_
- `transmogrify.sqlalchemy <https://pypi.python.org/pypi/transmogrify.sqlalchemy/1.0.1>`_ to get content out of just about any SQL database you can think of
- `collective.jsonmigrator <https://pypi.python.org/pypi/collective.jsonmigrator>`_ is good at migrating data via JSON format from very old Plone versions, going back all the way to 2.x

Note this is only a selection, do a search on pypi to find more. NB searching both on `transmogrify <https://pypi.python.org/pypi?%3Aaction=search&term=transmogrify&submit=search>`_ and `transmogrifier <https://pypi.python.org/pypi?%3Aaction=search&term=transmogrifier&submit=search>`_ gives more results!
