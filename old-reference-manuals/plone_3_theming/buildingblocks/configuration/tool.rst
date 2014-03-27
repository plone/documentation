The Generic Setup Tool
======================

The Generic Setup tool is used to apply your profiles to your site.

You can find the Generic Setup tool here

-  Site Setup > Zope Management Interface > portal\_setup

You can run the tool manually, but for theme purposes, if you have
created a product using the plone3\_theme paster template, Generic Setup
will be triggered automatically when you install your theme in your
site.

You'll find more extensive information about the Generic Setup Tool in
this tutorial:

-  `Understanding and Using Generic Setup on
   plone.org <http://plone.org/tutorial/genericsetup/exports-snapshots-and-comparisons>`_

However, there are two useful facts to know about it.

No Undo
-------

Although you can uninstall your theme using portal\_quickinstaller, at
present, you can't undo the profiles Generic Setup applied during
installation. For the most part, this isn't a problem, but it can get
confusing - if, for instance, you are experimenting with the order of
your viewlets and have tried several versions of viewlets.xml in
successive installations. In this case, exporting a profile (explained
below) can help you make sense of what you've done.

Exporting Profiles
------------------

You can export the current configuration of your site as a set of XML
files. This can be helpful if you're not quite sure what you've done, if
you're searching for a profile to base your own configuration on, or if
you just want the Generic Setup Tool to write out a configuration for
you.

-  Site Setup > Zope Management Interface > portal\_setup
-  Click the Export tab
-  Select the steps you wish to export
-  Click the Export Selected Steps button
-  You'll be given a zip file with the relevant XML files

It isn't always obvious which export step you need to get the exact
configuration you want, you may need to experiment.
