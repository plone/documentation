=================
Customizing Plone
=================

Introduction
============

Plone can be customized in two different ways,
depending on which kind of component you are trying to change:

* Through-the-web.

* By add-on products.

You should never edit files directly in an egg folder.
Instead you usually create a customized version of the
item you wish to modify and then configure Plone to use your customized
version instead of the stock one.

Through-the-web changes
=======================

Minor configuration changes can be done through the web. These
changes are effective immediately and don't require you to write
any code or restart Zope application server. The downside is that
since through-the-web changes don't have a source code "recipe" for
what you did,
the changes are not automatically repeatable.
If you need to do the same changes
for another site again, or you need heavily modify your site, you
need go through manual steps to achieve the same customization.

Possible through-the-web changes are:

* Site settings: E.g. adding/removing :doc:`content rules </working-with-content/managing-content/contentrules>`

* Showing and hiding viewlets (parts of the page) using ``@@manage-viewlets``

* Exporting and importing parts of the site configuration in ``portal_setup``

* Customizing viewlet templates in ``portal_view_customization``

* Customize ``portal_skins`` layer theme files in portal_skins

* Uploading JavaScript files, CSS files and images through Zope management
  interface and registering using ``portal_css`` and ``portal_javascripts``

Through the code changes
========================

To expand Plone using Python, you have to create your own add-on product.
Add-on products are distributed as packaged Python modules called `eggs <http://docs.plone.org/4/en/old-reference-manuals/buildout/index.html>`_.

The recommended way is to use the :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>` command to generate an add-on product skeleton which you can use as a starting point for your development.


