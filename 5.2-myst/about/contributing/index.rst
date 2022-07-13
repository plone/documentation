=================================
Contributing To The Documentation
=================================

.. topic:: Description

   This document describes what documentation contributors should follow to ensure consistency throughout all publications.

.. note::

   Contributing to the docs is a excellent way to get involved, meet the community and to improve Plone !

   Don't hesitate to contribute also if English is not your first language !


Overview
========

The documentation is hosted on `GitHub <https://github.com/plone/documentation>`_.

* Different branches for the different :doc:`versions <versions>` of Plone.

* Some external documentation is pulled in, to collect all the documentation in one place.



General Guidelines
==================

Please follow these general guidelines.

- **DO NOT** commit to master directly. Even for the smallest and most trivial fix.

- **ALWAYS** open a pull request and ask somebody else to merge your contribution.

- **NEVER** merge it yourself.

- If you work on a `ticket <https://github.com/plone/documentation/issues>`_, assign yourself to it.

- Create 'small' pull requests, one per each file, these are easier and faster to review, think *quality over quantity* !


Edit In The Cloud
=================

Head over to the `documentation repository <https://github.com/plone/documentation>`_.

You can then click the :guilabel:`Fork` button in the upper-right area of the screen to create a copy of our site in your GitHub account called a fork.


Make any changes you want in your fork, and when you are ready to send those changes to us, go to the index page for your fork and click New Pull Request to let us know about it.

#. Fill in the text-box :guilabel:`Commit changes` at the end of the page telling why you did the changes.
#. Press the button :guilabel:`Commit changes` next to it when you are done.
#. Head to the green :guilabel:`New pull request` button (e.g., by navigating to your fork's root and clicking :guilabel:`Pull requests` on the right menu-bar.
#. Click :guilabel:`Send pull request`.

This is the recommended way for smaller changes, and for people who are not familiar with Git.

Your changes are now queued for review under project's `Pull requests <https://github.com/plone/documentation/pulls>`_ tab on GitHub.

For more information about writing documentation please read the :doc:`styleguide <documentation_styleguide>` and also :doc:`our docs about helper tools <helper_tools>`.

You will receive a message when your request has been integrated into the documentation.

At that moment, feel free to delete the copy of the documentation you created under your account on GitHub.

Next time you contribute, fork again.
That way you'll always have a fresh copy of the documentation to work on.


Before You Make A Pull Request
==============================

* Before you commit your changes, it’s a good idea to run a spell check.
* Make sure that all links you put in are valid.
* Check that you are using valid restructured text.



Pull Request Checklist
======================

Making a good pull request makes life easier for everybody:

* The title and description of a pull request should be descriptive and need to reflect the changes.

If you can state for which versions of Plone your submissions are valid, that would be awesome.

We use a template which creates a default form for pull requests

.. image:: /_static/pr-template.png
   :align: center
   :alt: Picture of Pull request template

If possible please make sure to fill in the missing bits, for example

.. code-block:: shell

    Fixes #1234

    Improves:

    -  Style-guide about reST syntax

    Changes proposed in this pull request: Unified usage of '..code-block:: shell' as best practices


Editing The Docs Using Git
==========================

This is the recommended method of editing the documentation for
advanced users.

If you are already a member of the Plone organization on GitHub, create a branch in the `documentation repository <gttps://github.com/plone/documentation>`_.

If you are not a member you can also create a `fork <https://help.github.com/articles/fork-a-repo>`_ of the documentation repository into your own repository.

* Learn about `Sphinx <http://www.sphinx-doc.org/en/stable/>`_ and `reStructuredText <http://www.sphinx-doc.org/en/stable/rest.html>`_.

* Edit the file(s) which you want to update.

* Check that you do not have any syntax errors or typos

* Commit your changes and `create <https://help.github.com/articles/creating-a-pull-request>`_ and open a `pull <https://help.github.com/articles/using-pull-requests>`_ request.

For more information about writing documentation please read the :doc:`styleguide <documentation_styleguide>` and the docs about :doc:`Helper tools <helper_tools>`.

.. toctree::
   :hidden:

   documentation_styleguide
   rst-styleguide
   helper_tools
   versions
   word_choice
   readme-example
   changelog-example
   cherrypicking
   issues
   translation
