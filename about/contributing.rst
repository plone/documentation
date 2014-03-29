==========================
 Documentation Styleguide
==========================

.. admonition:: Description

   How to write and submit content for the Plone Documentation.

.. contents:: :local:

Introduction
============

This chapter explains the basics of editing, updating and contributing to
the *Plone Documentation*.

Reaching documentation team
=============================

Plone community runs a documentation team which is responsible
for keeping Plone documentation coherent.
To reach this team for any questions please contact

* `Documentation team mailing list <https://plone.org/support/forums/docs>`_

* *#plone-docs* IRC channel on irc.freenode.net

Contributing
============

The Plone Documentation by `Plone Foundation <http://plone.org>`_ is licensed under a `Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.

If you want to contribute to this documentation, you can do so directly by making a pull request, if you have filled out a `Contributor Agreement <http://plone.org/foundation/contributors-agreement>`_.

If you haven't filled in a Contributor Agreement, you can still contribute. Contact the Documentation team, for instance via the `mailinglist <http://sourceforge.net/p/plone/mailman/plone-docs/>`_ or directly send a mail to plone-docs@lists.sourceforge.net

Git workflow / branching model
==============================

It is important that you **NEVER** commit to master directly. Even for the smallest and most trivial fix. **ALWAYS** open a pull request and ask somebody else to merge your code. **NEVER** merge it yourself.

If you don't get feedback on your pull request in a day please come to #plone-docs and ask.

The main goal of this process is not to boss developers around and make their lives harder, but to bring greater quality to the documentation.

Pull request checklist
======================

Checklist of things that every person accepting pull request should follow.

* The title and description of a pull request MUST be descriptive and need to reflect the changes. Please review, line by line, and comment if the code change was not mentioned in the description of the pull request.


Editing documentation using git
=================================

This is the recommended method of editing the documentation for
advanced users. Please do not be afraid to commit.

* Learn about `Sphinx <http://sphinx.pocoo.org/>`_ and `restructured text
  <http://sphinx.pocoo.org/rest.html>`_.

* `Fork <https://help.github.com/articles/fork-a-repo>`_ the documentation source files into your own repository

* Edit the file(s) which you want to update.

* Check that you do not have any syntax errors or typos

* Commit changes your changes and `create <https://help.github.com/articles/creating-a-pull-request>`_ and open `pull <https://help.github.com/articles/using-pull-requests>`_ request.

For more information about writing documentation please read the :doc:`styleguide </about/styleguide>` and also :doc:`this </about/helper_tools>`.
