=================================
Upgrading a Plone 2.5 site to 3.0
=================================

.. admonition:: Description

   Tips and issues when upgrading your site from Plone 2.5 to 3.0

.. contents:: :local:

* To migrate from Plone 2.5 to 3.0, please follow the steps outlined in the :doc:`General approach to upgrading. </manage/upgrading/non_buildout_based_upgrade>`
* One thing to make sure you have right is that Plone is now not only files in the *Products directory*, but also modules inside *lib/python* in your instance.
  If you're using the installers, this is taken care of for you, but if you're doing it manually, make sure the lib/python components are in the right location.

Third party products
====================

If you have installed and depend on a lot of third-party products produced by developers outside the Plone Team, it's hard to say something definite - make sure the products you depend on are certified to work with Plone 3.
GroupUserFolder is NOT supported!
(NOTE: It may not be possible to upgrade a site using GRUF with external user folders such as LDAPUserFolder.
In those cases it is advised to create a new site and move the content over manually.)

If you have a big site running Plone and want a painless transition to the much-improved version 3, we suggest that you hire a company that can do the migration properly for you.
Send a mail to the Plone Developer mailing list, and we can recommend a company in your area if needed.

Notes on Zope migration
=======================

Migration from Zope 2.8.7 or 2.9.5 to Zope 2.10.x is mandatory but Plone 3 does not run natively on Zope 3.
If you are upgrading from Zope 2.8.7 and you have a separate Five product you need to delete the Five product from your product directory before your upgrade.
Zope 2.10.x requires Python 2.4.3+ (Python 2.4.2 is still acceptable).
Also mandatory is Python Imaging Library 1.1.5 or newer, Python ElementTree.

Caching
=======

* Caching related changes required (or maybe none!)
