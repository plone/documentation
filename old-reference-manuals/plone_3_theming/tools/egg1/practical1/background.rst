Python Eggs, Generic Setup and Zope 3
=====================================

Background notes on changes between Plone 2.5 and Plone 3.

Products, in Plone's parlance, are analogous to modules or extensions
for other applications. In the move from Plone 2.5 to Plone 3, several
important changes were made in the way Plone handles products. First,
some products began to be packaged as Python eggs, which made them
easier to manage, distribute and install. Second, products began to use
GenericSetup as a means for installation. And third, products
increasingly incorporated Zope 3 (Z3) technologies like browser views.

Python Eggs
~~~~~~~~~~~

A python egg is simply a bundle of files and directories which
constitute a python package. Eggs can either be compressed, in which
case they appear as a single \*.egg file, or uncompressed. Eggs are
similar in concept and function to Java's JAR files.

Eggs are installed via the setuptools framework, a side project of the
Python Enterprise Application Kit (PEAK), which provides for package
(and dependendency) management and distribution.

If you're using version control, you'll want to add \*.egg-info and
\*.pyc to the ignore patterns for your setup so that the egg metadata
and compiled python files aren't added to your repository.

`A Quick Guide to Python
Eggs <http://peak.telecommunity.com/DevCenter/PythonEggs>`_

    A good overview of eggs and setuptools from the folks at PEAK.

`Hatch Python Eggs with
SetupTools <http://www.ibm.com/developerworks/library/l-cppeak3.html>`_

    David Metz takes a look at the setuptools framework.

GenericSetup
~~~~~~~~~~~~

GenericSetup (GS) is a tool for managing site configuration in Plone
using xml files. GS makes it possible to export customizations from one
Plone site and import them into another. And to some extent, GS replaces
the Portal QuickInstaller (QI) post-Plone 2.5 in that GS can be used to
install products. In products which rely on GS, we find xml
configuration files; in products which use the older, venerable QI for
installation, by comparison, we find install methods written in python.

Keep in mind that GenericSetup does not currently allow you to undo the
profile applied during installation. You can uninstall your theme using
the QuickInstaller, however, assuming that an uninstall method is
present.

Because our skeleton theme product utilizes GenericSetup to install
itself, we will shortly be configuring several xml files needed by GS.

`Understanding and Using GenericSetup in
Plone <http://plone.org/documentation/tutorial/genericsetup>`_

    Now a bit dated, Rob Miller's tutorial on GS remains a useful
    resource for background on GS.

`GenericSetup
Improvements <http://theploneblog.org/blog/archive/2007/06/21/genericsetup-improvements>`_

    More information about GS from Rob Miller.

`Benefit NOW from Using GenericSetup and Z3
Technologies <http://plone.org/documentation/tutorial/benefit-now-from-using-genericsetup-and-zope-3-technologies/?searchterm=benefit%20NOW>`_

    Impress your colleagues by using GenericSetup and Zope 3 views
    efficiently and with minimal effort! This tutorial shows you how to
    add a new view, how to use it, how to add a new content type and how
    to hook it all up.

Zope 3 Technology
~~~~~~~~~~~~~~~~~

Despite any version number-induced miasma, remember that Plone 3 runs on
Zope 2. Zope 3 is a dramatic rewrite of Zope 2 and some Zope 3
functionality has been backported to work under Zope 2. (And yes, Plone
3.) For a full explanation of the Zope 3 technologies involved, consult
this tutorial:

`Customization for
developers <http://plone.org/documentation/how-to/how-to-create-a-plone-3-theme-product-on-the-filesystem/plone.org/documentation/tutorial/customization-for-developers>`_

    An overview of Plone 3 customization by Martin Aspeli.

