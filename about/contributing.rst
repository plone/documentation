==============
 Contributing
==============

.. admonition:: Description

   How to write and submit content for the Plone Documentation.

.. contents:: :local:

Introduction
============

This chapter explains the basics of editing, updating and contributing to
the *Plone Documentation*.

Reaching the documentation team
===============================

Plone community runs a documentation team which is responsible for keeping the Plone documentation coherent.
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

The documentation is hosted on github. And there are tools hooked directly into it: 

* there are branches for the different versions of Plone

* translation hooks with Transifex are in place

* some external documentation is pulled in, to collect all the documentation in one place.

For these reasons, it is important we keep the documentation coherent. 
Therefore, we follow a simple workflow, which we ask all contributors to respect:


Please  **DO NOT** commit to master directly. Even for the smallest and most trivial fix. **ALWAYS** open a pull request and ask somebody else to merge your code. **NEVER** merge it yourself.

Your pull requests may be checked for spelling, and clarity. So don't hesitate to contribute also if English is not your first language, we will try to be helpful in corrections without being annoying.

If you don't get feedback on your pull request in a day please come to #plone-docs and ask.

The main goal of this process is not to annoy you. On the contrary, we **love** your contributions. 

But the documentation team also wants to keep the documentation in good shape.


Pull request checklist
======================

Making a good pull request makes life easier for everybody: 

* The title and description of a pull request MUST be descriptive and need to reflect the changes. So please say "grammar fixes on the intro page" or "new page: feature x explained as a user story"

If you can state for which versions of Plone your submissions are valid, that would be awesome.

Editing the documentation using git
===================================

This is the recommended method of editing the documentation for
advanced users. 

* Learn about `Sphinx <http://sphinx.pocoo.org/>`_ and `restructured text
  <http://sphinx.pocoo.org/rest.html>`_.

* `Fork <https://help.github.com/articles/fork-a-repo>`_ the documentation source files into your own repository

* Edit the file(s) which you want to update.

* Check that you do not have any syntax errors or typos

* Commit changes your changes and `create <https://help.github.com/articles/creating-a-pull-request>`_ and open `pull <https://help.github.com/articles/using-pull-requests>`_ request.

For more information about writing documentation please read the :doc:`styleguide </about/styleguide>` and also :doc:`this </about/helper_tools>`.
