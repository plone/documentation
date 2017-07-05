=================================
Contributing To The Documentation
=================================

.. topic:: Description

   This document describes what documentation contributors should follow to ensure consistency throughout all publications.

.. note::

   Don't hesitate to contribute also if English is not your first language !

Overview
========

The documentation is hosted on `GitHub <https://github.com/plone/documentation>`_.

* There are branches for the different versions of Plone, see :ref:`plone-versions`.

* Some external documentation is pulled in, to collect all the documentation in one place.



General Guidelines
==================

Please follow these general guidelines.

- **DO NOT** commit to master directly. Even for the smallest and most trivial fix.

- **ALWAYS** open a pull request and ask somebody else to merge your contribution.

- **NEVER** merge it yourself.

- If you work on a `ticket <https://github.com/plone/documentation/issues>`_, assign yourself to it.

- Create 'small' pull requests, one per each file, these are easier and faster to review, think *quality over quantity* ! 


Editing On GitHub
=================

This is the recommended way for smaller changes, and for people who are not familiar with Git.

- Go to `Plone Documentation <https://github.com/plone/documentation>`_ on  GitHub.
- Press the :guilabel:`Fork` button. This will create your own personal copy of the documentation.
- **Edit** files using GitHub's text editor in your web browser
- Fill in the :guilabel:`Commit changes`-textbox at the end of the page telling why you did the changes. Press the :guilabel:`Commit changes`-button next to it when done.
- Then head to the green :guilabel:`New pull request`-button (e.g. by navigating to your fork's root and clicking :guilabel:`Pull requests` on the right menu-bar, or directly via https://github.com/yourGitHubUserName/documentation/pulls), you won't need to fill in any additional text.
  Press :guilabel:`New pull request`-button, finally click :guilabel:`Send pull request`.
- Your changes are now queued for review under project's `Pull requests <https://github.com/plone/documentation/pulls>`_ tab on GitHub.
- For more information about writing documentation please read the :doc:`styleguide </about/documentation_styleguide>` and also :doc:`this </about/helper_tools>`.
- You will receive a message when your request has been integrated into the documentation. At that moment, feel free to delete the copy of the documentation you created under your account on GitHub. Next time you contribute, just fork again. That way you'll always have a fresh copy of the documentation to work on.


Before You Make A Pull Request
==============================

* Check for typos. Again, do not let this discourage you if English is not your first language, but simple typing errors can usually be found with spellcheckers
* Make sure that all links you put in are valid.
* Check that you are using valid restructured text.


Pull Request Checklist
======================

Making a good pull request makes life easier for everybody:

* The title and description of a pull request **MUST** be descriptive and need to reflect the changes. So please say "grammar fixes on the intro page" or "new page: feature x explained as a user story"

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


Editing The Documentation Using Git
===================================

This is the recommended method of editing the documentation for
advanced users.

If you are already a member of the Plone organisation on GitHub, create a branch in the `documentation repository <gttps://github.com/plone/documentation>`_.

If you are not a member you can also create a `fork <https://help.github.com/articles/fork-a-repo>`_ of the documentation repository into your own repository.

* Learn about `Sphinx <http://sphinx-doc.org/>`_ and `restructured text
  <http://sphinx-doc.org/rest.html>`_.

* Edit the file(s) which you want to update.

* Check that you do not have any syntax errors or typos

* Commit your changes and `create <https://help.github.com/articles/creating-a-pull-request>`_ and open `pull <https://help.github.com/articles/using-pull-requests>`_ request.

For more information about writing documentation please read the :doc:`styleguide </about/documentation_styleguide>` and also :doc:`this </about/helper_tools>`.


