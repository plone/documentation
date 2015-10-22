===================================
Styleguide for add-on documentation
===================================



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



