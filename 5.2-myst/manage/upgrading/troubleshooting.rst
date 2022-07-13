===============
Troubleshooting
===============

.. admonition:: Description

   What to do when a problem occurs during a Plone upgrade.


When a problem occurs during the migration we recommend that you take the following steps.

Check the log files
===================

When a site error occurs, or Zope fails to start, there's probably an informative error message in Zope's log files.
Locate `these log files <https://plone.org/documentation/faq/plone-logs>`_ and inspect instance.log.
Ignore irrelevant warnings and search for words such as error, exception and traceback (case-insensitive).

When Zope doesn't start and there's no useful information in the log file, you can start Zope interactively and watch for error messages in the output:::

    bin/instance fg

You may be able to find more information on the error messages in:

* the :doc:`Version-specific migration tips </manage/upgrading/version_specific_migration/index>` for your version of Plone
* the :doc:`Error References </appendices/error-reference>`

Test without customizations
===========================

When you have customized page templates or Python scripts, your changes may interfere with changes in the new version of Plone.
It's important to rule out this possibility, since your customizations are unique to your site and no one on the planet will be able to help you solve it.

Temporarily remove your customizations, for example by removing your layers from portal_skins, or by removing files from these layers on the file system.
If the problem disappears, you'll need to double-check your customizations.
It's usually best to copy the original files of the new version of Plone to your skin, and re-customize those.

Test without products
=====================

Bugs or compatibility problems in products that you have installed may cause problems in Plone.
Go to Site Setup > Add/Remove Products and remove (uninstall) all product that are not distributed with Plone.
Remove the uninstalled products from the Products directory of your Zope instance.

If the problem disappears, you'll need to doublecheck the offending product:

* Does it support the new version of Plone, Zope and Python?
  Check the product's README.txt or other informational files or pages.
* Does the product require any additional migration procedures?
  Check the product's INSTALL.txt, UPGRADE.txt or other informational files or pages.
* Does the product install properly? Re-install it and check the install log.

Test with a fresh Plone instance
================================

Create a new Plone site with your new version of Plone.
You don't need a new Zope instance, since you can add another Plone site in the root of Zope.
If the problem does not occur in a fresh site, the cause of your problem is most likely a customization, an installed product or content that was not migrated properly.

Make the problem reproducible
=============================

Before you go out and :doc:`ask for help </askforhelp>`, you should be able to describe your problem in such a way that others can reproduce it in their environment.

Reduce the problem to the smallest possible domain.
Eliminate products and customizations that are not part of the problem.
This makes it easier for others to reproduce the problem and it increases your chances of meeting others with the same problem or even a solution.
The more complex your story is, the more likely that it is unique to your situation and in-penetrable to others.

Ask for help
============

:doc:`Ask for help </askforhelp>` in the `Plone support channels <https://plone.org/support>`_. Be sure to:

* Provide relevant source code for your customizations that are part of the problem.
* Describe the exact configuration, software versions, migration history, error messages and so on.

Report a bug
============

Once you have investigated, analyzed, identified and confirmed the cause of your problem and you are convinced it's a bug (rather than an X-file), go to the appropriate bug tracker and report it:

* Products: the README usually tells how to report bugs
* `Plone Issue Tracker <https://github.com/plone/Products.CMFPlone/issues>`_

Do not use the bug trackers to ask for help.
First analyze your problem and assert that it's a bug before you report it.

