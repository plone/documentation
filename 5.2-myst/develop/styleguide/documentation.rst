============================
Styleguide for documentation
============================


General style guides on documentation
=====================================

For general information on how to write documentation, see the :doc:`documentation styleguide </about/documentation_styleguide>`.
Information on our Restructured Text style guide can be found in the: :doc:`REST styleguide </about/rst-styleguide>`.


Restructured Text versus Plain Text
===================================

Use the Restructured Text (``.rst`` file extension) format instead of plain text
files (``.txt`` file extension) for all documentation, including doctest files.
This way you get nice syntax highlighting and formating in recent text editors,
on GitHub and with Sphinx.


Tracking changes
================

Feature-level changes to code are tracked inside ``CHANGES.rst``. The title
of the ``CHANGES.rst`` file should be ``Changelog``. Example:

.. sourcecode:: rst

    Changelog
    =========

    1.0.0-dev (Unreleased)
    ----------------------

    - Added feature Z.
      [github_userid1]

    - Removed Y.
      [github_userid2]


    1.0.0-alpha.1 (2012-12-12)
    --------------------------

    - Fixed Bug X.
      [github_userid1]


Add an entry every time you add/remove a feature, fix a bug, etc. on top of the
current development changes block.


.. _git_commit_message_style_guide:

Git commit message style guide
==============================

`Tim Pope's post on Git commit message style <http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html>`_
is widely considered the gold standard:

::

    Capitalized, short (50 chars or less) summary

    More detailed explanatory text, if necessary.  Wrap it to about 72
    characters or so.  In some contexts, the first line is treated as the
    subject of an email and the rest of the text as the body.  The blank
    line separating the summary from the body is critical (unless you omit
    the body entirely); tools like rebase can get confused if you run the
    two together.

    Write your commit message in the imperative: "Fix bug" and not "Fixed bug"
    or "Fixes bug."  This convention matches up with commit messages generated
    by commands like git merge and git revert.

    Further paragraphs come after blank lines.

    - Bullet points are okay, too
    - Typically a hyphen or asterisk is used for the bullet, preceded by a
      single space, with blank lines in between, but conventions vary here
    - Use a hanging indent

`GitHub flavored markdown <http://github.github.com/github-flavored-markdown/>`_ is also useful in commit messages.

