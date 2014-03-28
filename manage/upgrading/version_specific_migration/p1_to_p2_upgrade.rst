===============================
Upgrading from Plone 1.0 to 2.0
===============================

.. admonition:: Description

   Version-specific procedures and tips for migrating Plone 1.0 to 2.0.

.. contents:: :local:

The changes made to Plone between 1.0 to 2.0 are fairly complex.
Before migrating you can read this document to understand the potential impact migrating will have on your website.
We suggest to follow standard practices: backup your Products and Data.fs file(s), do the actual migration on a test instance., etc.
Another note is that Plone's migration are probably not perfect - this is hard to guarantee, since we can't predict just how you have changed your system.

If you have a big site running Plone and want a painless transition to the much-improved version 2.0, we suggest that you hire a company that can do the migration properly for you.
Send a mail to the Plone Developer mailing list, and we can recommend a company in your area if needed.

The migration tool handles most cases, but your mileage may vary.
Heavily customized sites should factor in some time to do the transition.

Side Effects Moving to 2.0
==========================

* Plone CSS has radically changed.
* Plone Templates have radically changed.
* Plone 2.0 Tools Tools for Plone have changed
* Plone 2.0 Group User Folder the User Folder for Plone has changed
* See the What's New in Plone 2.0 Guide for more information about what has changed.

Template/CSS Changes
====================

The templates and CSS have been refactored and reorganized to be leaner, more efficient and more logically laid out.
The CSS class names have been changed to be consistent and to provide easier customization.
Therefore, if your site customized the templates or CSS, you will have to examine how your changes are affected by the new templates and CSS.

* ploneDeprecated.css
* About the tableless layout
* base_properties vs. stylesheet_properties
* Form changes: New Forms Style and How to Convert from the Plone 1.0 forms format
* CSS Nameageddon - the CSS class names have changed from Plone 1 to Plone 2

base_properties
===============

Plone 1 shipped with a property sheet called 'stylesheet_properties', that enabled you to change your site in a quick and easy way.

In Plone 2, we have stripped this down a bit, and changed its name to 'base_properties' to better reflect what it's for.

The reason for this was that the 'stylesheet_properties' was kind of a half-way mix of color properties and CSS, and you could do much more than simple color changes with it.
This complicated things for the CSS people, and thus we decided to keep the separation cleaner, and have only base properties in the variables.

It's not possible to do a perfect 1:1 mapping between the two, and you might have to resort to a few simple CSS rules to replicate what you had in Plone 1.
The good news is that it's much more flexible and powerful this way.

The best approach to converting to the new scheme is to start with the existing 'base_properties', and move your color and border values over one by one until you have something that resembles your old layout.

Lexicons
========

lexicon in portal_catalog is set as plone_lexicon.
Look at your ZCTextIndex indexes to see what lexicon they are looking for. On plone.org, we needed to rename the lexicon to zc_lexicon (or we could have recreated the ZCTextIndexes and specified whatever lexicon you have.)
Even if your ZCTextIndex indexes are looking for the right index, you may benefit from re-indexing those fields.

Special Note about the Windows Installer
========================================

You have to uninstall previous Plone versions and delete the Plone service before you can install Plone 2 successfully on Windows XP.
The service doesn't delete by itself when you uninstall.
