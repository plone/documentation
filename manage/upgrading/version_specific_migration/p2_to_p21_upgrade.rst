===============================
Upgrading from Plone 2.0 to 2.1
===============================

.. admonition:: Description

   Procedures and tips to migrate your site from Plone 2.0 to 2.1.

.. contents:: :local:

A note about migration and version numbering
============================================

Plone has changed significantly infrastructure-wise with the jump from Plone 2.0 to 2.1. Plone 2.1 represents 18 months of active development and improvements, and is a much more scalable and powerful platform with the 2.1 release.

Some people are confused by the low version number increase, and mistakenly assume that it is a minor upgrade.
It is not, far from it.

Up until Plone 2.1, the policy was that each of our major releases would be incremented 0.1, like a standard framework policy.
We understand that this is somewhat confusing, and have since changed this policy.
The Plone Team aims to release a new version roughly every 6 months, so we have moved to a policy that increases the version number by 0.5 on every significant release.

We have done this to better reflect the enormous amount of work that goes into each release, and to better illustrate what you can expect from a release.

The main point here is that even if an upgrade from 2.0 to 2.1 sounds minor, in this particular case it is not.
The entire content type infrastructure has been rewritten, and all your content needs to be transferred to the new types, so there will most likely be some pain involved on some level &mdash; be it third-party products, templates that need to be re-customized, or actual bugs in the migration machinery (which have mostly been ironed out with the 2.1 and 2.1.1 releases).

About the migration
===================

Please note that it is difficult to predict how well migration will work, since we can't know just how you have changed your system. Plone is a very flexible system, but when migrating this will affect the outcome based on what you changes you have made to your system.

* If you have a standard Plone site with simple customizations, it will likely work very well.
* If you have installed and depend on a lot of third-party products produced by developers outside the Plone Team, it's hard to say something definite - make sure the products you depend on are certified to work with Plone 2.1.x.
  **Special note about SpeedPack:** You should uninstall this product, as most of the improvements done in this product are now part of Plone, and as a result, it's no longer necessary (and it doesn't work on Zope 2.8).
* If you have a big site running Plone and want a painless transition to the much-improved version 2.1, we suggest that you hire a company that can do the migration properly for you.
  Send a mail to the "Plone Developer mailing list":/contact#developers, and we can recommend a company in your area if needed.

The migration tool handles most cases, but your mileage may vary.
Heavily customized sites should factor in some time to do the transition.

For Plone 2.5 (our next upcoming release), there are substantial improvements to the architecture that will ease migration in the future, as well as providing good tools for exporting and importing content and configurations.

Plone 2.1.2 and later releases also includes significant improvements to the migration machinery based on feedback we got from people doing migrations, so if migrating your site using the Plone 2.1 or 2.1.1 release didn't work out for you, please give the new version a try.

Performing the migration
========================

Before you start the migration, you should decide what approach you want to use. There are two common ways of migrating:

#. Migrating your site content, products and customizations in-place.
#. Exporting your content, creating a fresh Plone 2.1 site, importing your content.

The in-place migration is more comprehensive, and hence more error-prone, especially if you have misbehaving third-party products or very old Plone instances.
If your content is the most important thing for you, and you don't mind applying your configuration settings and simple customizations again, exporting all your content folders followed by an import into a clean instance might be a better approach for you.
This procedure is described in the "importing Plone 2.0 content into 2.1 FAQ":/documentation/faq/importing-2.0-content-into-2.1.
Please note that this should only be done if you are experiencing problems and as a last resort (or simply want to start with a clean site but keep your content) &mdash; for most people, in-place migration is the way to go.

The in-place procedure is the usual one for Plone migrations, a quick overview of the steps:

#. If you want to upgrade from Zope 2.7 to Zope 2.8 in this transition, we advice you to **stay with Zope 2.7 until you have completed the Plone part of the migration**, *then* upgrade to 2.8.
   Zope 2.8 includes major changes and improvements, and trying to upgrade both Zope and Plone in the same operation is not recommended.
   Both Zope 2.7 and Zope 2.8 are supported platforms for Plone 2.1.x, though.
   As a rule of thumb, always start at the top with upgrades, and work your way down &mdash; upgrade Products, then Plone, then Zope, then Python.
#. Make sure the third-party products you use have been updated or verified to work on Plone 2.1. Upgrading to 2.1 if the products you are using do not support it is a frustrating experience.
#. Install the new Plone version in a clean location, you should stick with the same major version of Zope (e.g. going from Zope 2.7.3 to 2.7.5 is OK, going from 2.7.x to 2.8.x is not recommended until the Plone part of the migration is done).
#. Move over your 'Data.fs' and any Products / External Methods to the new instance.
#. Start the new Zope/Plone
#. Log in to the ZMI as a 'Manager' user.
#. Go to 'portal_migration'
#. Click the migrate button and wait for the output from the migration process.
   This can take a considerable amount of time depending on your site, since all content is being re-created with the new content types, and re-cataloged.

Common problems and issues
==========================

* Several "new" tabs will appear at the top of the site.
  This is due to a policy change in how Plone constructs navigation.
  Plone 2.1 and up will automatically make tabs from the folders in the root, and doesn't require you to manually create them in the portal_actions tool anymore.
  To fix this, you can either:

  * Go in and delete your portal_actions entries to only use the root folders (the folders also have individual visibility settings in the Properties tab of each item).
    This is the recommended approach unless you have global tabs leading deep inside the site, or:
  * Turn off the automatic tab generation in the 'Site Setup' &rarr; 'Navigation Settings'.
    This will make the global tabs behave the way they did in 2.0.

* All the content items and folders **that you have the permissions to view** now show up in the nav tree - if you want the old behavior from Plone 2.0 back, where only folders show up &mdash; and only those who are published &mdash; you can now control the navigation setup in 'Site Setup' &rarr; 'Navigation Settings'.
* If you have an item with the short name 'events' or 'news' in the root of your site, they should be renamed before starting the migration - since this can cause problems with the migration to the new Smart Folders that list these.
* If you get 'AttributeError: referencebrowser_startupDirectory', you are unpacking the Plone tarball with WinZip, which mangles long file names and has a lot of other problems.
  Get a proper unpacking tool like WinRAR instead.
* One of the problems that people run into during migration is third-party products they have installed that didn't clean up after themselves, or that left behind "dead" content when uninstalled.
  This can trip up the migration process.
  Here is a simple script that can list content with no associated product, so you can remove the defunct objects.
  To use it, create a 'Script (Python)' from the ZMI add menu in the root of your Plone site, paste in the code from this file, click 'Save' and then click the 'Test' tab to run the script.
  It should list dead object locations, so you can go and delete them manually if needed::

     portal_types = context.portal_types.objectIds()

     print "Dead Content Type Inspector"
     print

     for i in context.portal_catalog.uniqueValuesFor('portal_type'):
         if i in portal_types: continue
         print i
         results = context.portal_catalog(portal_type=i)
     for i in results:
         print i.getURL()
         print
     print

     return printed

* Another error that was often encountered in Plone 2.1 and 2.1.1 was that some objects weren't converted to the new Archetypes-based types.
  If you get: "maximum recursion depth exceeded" on viewing your site after the migration, the folders/objects are most likely still CMF objects, not Archetypes objects.
  Plone 2.1.2 includes a fix that tries to work around this problem.
  (The reason this exists in the first place seems to be bad behaviour introduced in the Plone 2.0 Release Candidates and subsequently fixed before the 2.0 final release, but some people still have content created with the Release Candidates.)
  Also note that this error message can show up if you customized a 2.0 'document_view' template and are trying to use it with Plone 2.1.
* If all (or some of) the migrated content are owned by the person doing the migration instead of the original author, that means that Plone was unable to look up the owner info while migrating.
  The cause of this is normally that your users are stored in LDAP and you haven't set up the connection before doing the migration. Another possibility is that your users are defined outside the Plone site.
* If you don't get any images in the image views or thumbnails in the summary listings: PIL is now a dependency, and you will not get image scaling if it is not installed.
  Also, you need to make sure zlib (for PNG support) and libjpeg is installed before you install PIL.
  More information "can be found here":/documentation/error/no-image-resizing.
* If your content column is missing on all pages, one of the portlets you have set up is broken.
  Some versions of Plone (including the RCs of 2.1.2) had a bug where it would just stop rendering the content column instead of giving you an error if one of your portlets break.
* Some people are also confused about the behavior of security in 2.0 vs. 2.1:
  A bug in Plone 2.0 made it so that it **seemed** to be the case that if any folder along the path to an item was private, that item could not be viewed, regardless of its state.
  Workflows in Plone behave in a different way, though - allowing you to have a folder that is private, and have a published item inside it that is accessible (but the folder will be inaccessible).
  If you want your permissions to inherit down the path, you'll have to make some changes to the workflow, "documented here":/documentation/how-to/make-permission-settings-inherit.
  The reason this seemed to work in Plone 2.0 was a bug in the breadcrumb handling code, and the object wasn't protected there either, but erroneously seemed to be.
* If you get the error 'AttributeError: _length', you are upgrading to Zope 2.8, and you will need to call 'manage_convertIndexes' on all catalogs that are not in the root (CMFCollector catalogs etc).
  Third-party products sometimes have their own catalogs, check with the product maintainer about this.
  See the section "Upgrading from Earlier Versions of Zope" in the file 'Zope-2.8.4-final/doc/FAQ.txt'.
* If LiveSearch doesn't work or you have other symptoms that looks like the catalog isn't working properly, check out the "FAQ on disappearing catalogs":/documentation/faq/catalog-disappears
* If you get 'AttributeError: toPortalTime' from a third-party product, it needs to update itself to use 'toLocalizedTime' instead.
  'toPortalTime' was deprecated in Plone 2.0, and is removed in Plone 2.1.
* If for some reason some of the original tools are corrupted or not working properly, you can copy in fresh instances from a newly-created Plone site.
  I will show an example where the 'portal_form_controller' tool is not present in the migrated site.
  Typically you would get AttributeError: portal_form_controller as an error message.
  In this example, {Zope} represents the Zope root (for example, localhost:8080)and {Plone} represents your Plone site:

  #. Go to 'http://{Zope}/manage_main' and log in with a Manager user.
  #. Add Plone Site from the pulldown menu
  #. Call it 'TempPlone'
  #. Once the Plone site is created, go to 'http://{Zope}/TempPlone/manage_main
  #. Check the box next to 'portal_form_controller', and click 'Cut' at the bottom of the page.
  #. Go to http://{Zope}/{Plone}/manage_main
  #. Make sure there is no 'portal_form_controller' in the list. If there is, delete it.
  #. Click the 'Paste' button at the bottom of the form.
  #. Your site now has a fresh 'portal_form_controller' from a new Plone 2.1 site, and should work properly. You can now delete the 'TempPlone' instance.

Additional notes
================

If you still have problems, create an issue in the "issue tracker":/collector - make sure you use the Upgrade / Migration topic, and remember to search before submitting an issue to minimize duplicates. Make sure you provide as much detail as possible on your configuration and setup, so we can better help you.

Tip: How to re-customize your templates
=======================================

If you have done significant changes to the Plone 2.0 templates (functionally, that is - the CSS classes are mostly the same as in 2.0), you may have to re-apply these customizations to the 2.1 templates. The best way to do this is:

* Have one directory with the original Plone 2.0 templates
* Compare your customized templates with the original Plone 2.0 ones (a visual diff tool is useful for this - we recommend Meld for Linux, FileMerge (included in XCode) for Mac OS X, and WinMerge for Windows)
* Apply those changes to the 2.1 templates. Of course, your customizations should not touch the original Plone 2.1 files, so make sure you place your customized templates in a file system Product, or in the 'custom' directory in 'portal_skins'.

Postscript
==========

This document was written as an attempt to collect all the relevant information about migrating from 2.0 to 2.1 in one location.
It would be impossible without all the hard-working people in the Plone Team writing the migration code (which is a boring and complex task) in the first place, and the helpful people on the "Plone Setup":/contact#setup list, who have helped a lot of people migrate successfully.
You all rock!
