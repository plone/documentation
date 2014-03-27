=============================
 Packages, products and eggs
=============================

.. admonition:: Description

   Looking at the core concepts in more detail

Terminology
-----------

Before we begin, you should familiarize yourself with these terms:


-  `Software home`_
-  `Zope instance`_
-  `Python path`_
-  `Python package`_
-  `Zope product`_
-  `Python egg`_
-  `The Python Package Index`_
-  `easy\_install`_
-  `Namespace package`_

The magic Products namespace
-----------------------------

When Zope finds a "product", it will create an entry in
*Control\_Panel/Products* in the root of the ZMI, and run the
*initialize()* method, found in the product's root
*\_\_init\_\_.py* file, each time Zope starts up. Not every package
used in a Plone context needs to be a product, but "productness" is
required for:


-  GenericSetup profiles
-  Skin directories being installed as layers in the
   *portal\_skins* tool (but *not* for Zope 3-style browser views)

The easiest way to create a product is to use Paster/ZopeSkel to
create an egg-ready package in the *Products.\** namespace using
the *basic\_namespace* template:

::

    $ paster create -t basic_namespace Products.myproduct
    Selected and implied templates:
      ZopeSkel#basic_namespace  A project with a namespace package

    Variables:
      egg:      Products.myproduct
      package:  productsmyproduct
      project:  Products.myproduct
    Enter namespace_package (Namespace package (like plone)) ['plone']: Products
    Enter package (The package contained namespace package (like example)) ['example']: myproduct
    ... accept defaults to end

If you're using buildout, create your package in the
*src* directory, and add references to it in the develop and
instance/eggs sections of buildout.cfg:

::

    develop =
        src/Products.myproduct
    ...
    [instance]
    ...
    eggs =
        ${buildout:eggs}
        ${plone:eggs}
        Products.myproduct

Run bin/buildout and you'll be set up to develop your egg-ready
product in the *src* directory. Turn it into a distribution egg when
complete.

It is possible to use packages (including egg-distributed ones)
outside the *Products* namespace/directory as Zope 2 products. Many
developers prefer this approach, feeling it is unnatural to keep
everything in a single, "flat" namespace.

Extra steps are required for this. Prior to Zope 2.10.4, this is
also required for products in the *Products* namespace

We must add a line like the following to the package's
*configure.zcml*:

::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five">

      <five:registerPackage package="." initialize=".initialize" />

    </configure>



Secondly, it is important to realize that packages outside the
*Products* namespace are not automatically detected when Zope starts
up. If they contain *configure.zcml* files (as most packages will
do), this must be explicitly included from somewhere. This may be:


-  Another package's configure.zcml file.
-  Zope's site.zcml, the root of all ZCML files, which is found in
   the *etc* directory in the instance home.
-  A ZCML :term:`Slug`, a one-liner created in the zope instance's
   *etc/package-includes* directory, with a name like
   *my.package-configure.zcml*.

In all cases, the syntax is the same:

::

    <include package="my.package" file="configure.zcml" />

If you have *meta.zcml* or *overrides.zcml* files, you can add
*<include />* directives for these as well. If you are using slugs,
it must be named accordingly, e.g. *my.package-meta.zcml* or
*my.package-overrides.zcml*. A :term:`Slug` can not contain more than one
line.

Later in this tutorial, we will show how buildout can manage slugs
for us automatically.

.. _Software home: http://plone.org/documentation/glossary/software-home
.. _Zope instance: http://plone.org/documentation/glossary/zope-instance
.. _Python path: http://plone.org/documentation/glossary/python-path
.. _Python package: http://plone.org/documentation/glossary/python-package
.. _Zope product: http://plone.org/documentation/glossary/zope-product
.. _Python egg: http://plone.org/documentation/glossary/python-egg
.. _The Python Package Index: http://plone.org/documentation/glossary/python-package-index
.. _easy\_install: http://plone.org/documentation/glossary/easy_install
.. _Namespace package: http://plone.org/documentation/glossary/namespace-package
