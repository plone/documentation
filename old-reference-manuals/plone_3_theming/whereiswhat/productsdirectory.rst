Where's my Products Directory?
==============================

How to track down your products directory. It'll differ according to the
Plone installer or installation process you used.

The products directory is where old-style 2.5 products live. To track
this down, you'll need to know where your Zope Instance or your Buildout
is first.

For theming purposes, the main reason you'll need to investigate the
products directory is to locate Plone Default theme files - as parts of
Plone are still in old-style product form.

Plone version 3.1.2 onwards
---------------------------

In a Buildout based installation, you'll find products in various
directories.

Core Plone products (such as CMFPlone)
    For these, have a look in

    -  [your buildout]/parts/plone.

Products you download yourself
    These should go in

    -  [your buildout]/products.

    If you find you haven't got a products directory there, then it is
    OK to create one yourself.
Products you asked buildout to download
    If you asked buildout to go and fetch some old-style products, then
    these will have been dropped into

    -  [your buildout]/parts/[directory name].

    (Buildout will also have created the directory and will have called
    it something like "productdistros").

Plone version 3.1.1 or lower
----------------------------

Plone Installer and Plone Product Package
    It should be easy to locate all your products (those belonging to
    the core Plone installation and those you've downloaded yourself) in

    -  [your zope instance]/products

    However, if you used the Plone 3.1 Universal Installer your
    installation will be buildout based.

