============
Preparations
============

.. admonition:: Description

   Things to do before you migrate Plone.


Gather Information
==================

- Read the "What's new in..." for your relevant Plone version, and read the release notes.

  - You'll find these in the CMFPlone directory of the distribution of the new version of Plone.

- Make sure to check installed add-ons, if you **do not** need certain add-ons anymore, please deactivate and deinstall.

- Check for dependencies

  - Read the release notes for the Plone release you are upgrading to, in particular:
  - What version of Python is required?
  - What version of Zope is required?
  - Do you need any new Python libraries?
  - Make sure all the add-on products you are using have updated to support the version of Plone you are upgrading to.

  - Start with the third-party products that are in use on your site.

    - Verify that they have been updated or verified to work on the new version, and get them upgraded in your existing instance before you start the Plone/Zope/Python upgrade if possible.
  - If Zope depends on a newer version of Python, install the new version of Python first.
  - If the newer version of Plone depends on a newer version of Zope, you will need to install that before proceeding with the Plone upgrade.


.. note::

    Zope has its own migration guidelines, which you will find in the release notes of the version you are migrating to.

    If Plone is being upgraded at the same time as a Zope version, Plone will usually handle the Zope upgrade with its own migration script.

- Read the following files in the CMFPlone directory of the distribution of the new version of Plone you want to update to:

  - README.txt
  - INSTALL.txt
  - UPGRADE.txt (although this usually contains only the general procedure outlined above)

    - These files are important because they may contain important last minute information and might be more specific than the relevant sections of this reference manual.

Back Up Your Plone Site
=======================

.. note::

    It's important to back up your Plone site.

You will find a :doc:`how-to on backing up your Plone site here </manage/deploying/backup>`.

Setup A Test Environment To Rehearse The Upgrade
================================================

.. note::

    Never work directly on your live site until you know that the upgrade was successful.

Instead, create a test environment to rehearse the upgrade.
Copy your instance into a new environment and upgrade the copy.
This is a good way of working out your third party products and dependencies in preparation for the final upgrade of the live site!
