==================================
 Contributing to the documentation
==================================

.. admonition:: Description

   How to write and submit content for the Plone Documentation.

.. contents:: :local:



Reaching the documentation team
===============================

The Plone community runs a documentation team which is responsible for keeping the Plone documentation coherent.
To reach this team for any questions please contact

* `Documentation team mailing list <https://plone.org/support/forums/docs>`_

* *#plone-docs* IRC channel on irc.freenode.net


License
=======

The Plone Documentation by `Plone Foundation <http://plone.org>`_ is licensed under a `Creative Commons Attribution 4.0 International License <http://creativecommons.org/licenses/by/4.0/>`_.

If you want to contribute to this documentation, you can do so directly by making a pull request, if you have filled out a `Contributor Agreement <http://plone.org/foundation/contributors-agreement>`_.

If you haven't filled in a Contributor Agreement, you can still contribute. Contact the Documentation team, for instance via the `mailinglist <http://sourceforge.net/p/plone/mailman/plone-docs/>`_ or directly send a mail to plone-docs@lists.sourceforge.net
Basically, all we need is your written confirmation that you are agreeing your contribution can be under Creative Commons. You can also add in a comment with your pull request "I, <full name>, agree to have this published under Creative Commons 4.0 International BY".


Workflow
========

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


Editing the documentation on GitHub
===================================

This is the recommended way for smaller changes, and for people who are not familiar with Git.

- Go to `Plone Documentation <https://github.com/plone/documentation>`_ on  GitHub.
- Press the **Fork** button. This will create your own personal copy of the documentation.
- **Edit** files using GitHub's text editor in your web browser
- Fill in the **Commit changes**-textbox at the end of the page telling why you did the changes. Press the **Commit changes**-button next to it when done.
- Then head to the green *New pull request*-button (e.g. by navigating to your fork's root and clicking "Pull requests" on the right menu-bar, or directly via https://github.com/yourGitHubUserName/documentation/pulls), you won't need to fill in any additional text. Just press **New pull request** button, finally click "Send pull request".
- Your changes are now queued for review under project's `Pull requests <https://github.com/plone/documentation/pulls>`_ tab on Github.
- For more information about writing documentation please read the :doc:`styleguide </about/styleguide>` and also :doc:`this </about/helper_tools>`.
- You will receive a message when your request has been integrated into the documentation. At that moment, feel free to delete the copy of the documentation you created under your account on github. Next time you contribute, just fork again. That way you'll always have a fresh copy of the documentation to work on.



Pull request checklist
======================

Making a good pull request makes life easier for everybody:

* The title and description of a pull request MUST be descriptive and need to reflect the changes. So please say "grammar fixes on the intro page" or "new page: feature x explained as a user story"

If you can state for which versions of Plone your submissions are valid, that would be awesome.

Editing the documentation using git
===================================

This is the recommended method of editing the documentation for
advanced users.

* Learn about `Sphinx <http://sphinx-doc.org/>`_ and `restructured text
  <http://sphinx-doc.org/rest.html>`_.

* `Fork <https://help.github.com/articles/fork-a-repo>`_ the documentation source files into your own repository

* Edit the file(s) which you want to update.

* Check that you do not have any syntax errors or typos

* Commit your changes and `create <https://help.github.com/articles/creating-a-pull-request>`_ and open `pull <https://help.github.com/articles/using-pull-requests>`_ request.

For more information about writing documentation please read the :doc:`styleguide </about/styleguide>` and also :doc:`this </about/helper_tools>`.

Translation
===========

We use `Transifex <https://www.transifex.com/>`_ for translation.
Thanks to that it is really easy to contribute to translation.

Quick start:
------------

* Browse to: https://www.transifex.com/projects/p/plone-doc/ and choose your language.

* Click on the right *Join Team*


Getting started
---------------

* Go to: https://www.transifex.com/signin/

* Go to: https://www.transifex.com/projects/p/plone-doc/

* Click on: `HELP TRANSLATE PLONE DOCUMENTATION <https://www.transifex.com/signup/?join_project=plone-doc>`_

* Choose your language

* Click on the right *Join Team*




