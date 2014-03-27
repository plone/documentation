Where's my Zope Instance?
=========================

Where your Zope instance lives depends on the Plone installer or
installation process you used.

Plone Version 3.1.2 onwards
---------------------------

Buildout
    In a Buildout based installation, you don't need to worry much about
    your Zope instance. If you really want to investigate you'll find
    the actual instance in [your buildout]/parts/instance. However most
    of the key bits (your Plone products, 3\ :sup:`rd` party products,
    your Data.fs) don't actually live there. They are all assembled
    together from various parts of your file system by the zope.conf
    file which is generated when you run buildout.

Plone Version 3.1.1 or lower
----------------------------

Plone Installer
    The Plone installers (apart from the Plone 3.1 Universal Installer)
    usually drop a Zope instance directory alongside the Zope and Python
    software directories. So, for example, a standard Windows
    installation, locates your Zope instance at c:\\Program Files\\Plone
    3\\Data. On a Mac, it will be called 'instance' and will probably
    live in a Plone folder in your applications folder.
    The Plone 3.1 Universal Installer, however, will have given you a
    buildout based installation.
Plone Product Package
    If you've installed Zope yourself, you'll have been prompted to
    create a Zope instance, so you should have a good idea of where that
    is on your system.

