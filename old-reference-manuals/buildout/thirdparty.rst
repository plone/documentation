================================
Installing a third party product
================================

.. admonition:: Description

  How to install a new package using these tools


How to install a new third-party products will depend on whether it
is packaged as an egg, or a traditional Zope 2 product.

Installing eggs
---------------

So long as an egg has a release in the
`PyPi <http://pypi.python.org/pypi>`_ or elsewhere, buildout can
download and install it, including any explicitly specified
dependencies. Simply list the egg, and optionally a version
(otherwise, you get the latest available), in the *eggs* option.

::

    [buildout]
    ...
    eggs = 
        elementtree
        borg.project>=1.0b1,<2.0dev

If you want buildout to search an index other than PyPi's, you can
add a URL to *find-links* that contains download links for the
eggs. In fact, we have already seen an example of this:
*elementtree* is found at *http://effbot.org/downloads*, not in PyPi
directly. Thus, we have:

::

    [buildout]
    ...
    
    find-links =
        http://dist.plone.org
        http://download.zope.org/ppix/
        http://download.zope.org/distribution/
        http://effbot.org/downloads
    
    eggs =
        elementtree

We have also listed some of the download locations for Zope and
Plone eggs.

Again - re-run buildout for the changes to take effect:

::

    $ ./bin/buildout

Development eggs
~~~~~~~~~~~~~~~~

If there is not a release for your egg, or you want to track an egg
in Subversion, check it out to the *src/* directory. Make sure you
get the full egg, including the top-level *setup.py* file. For
example, to get the *plone.portlets* trunk development, egg do:

::

    $ cd src
    $ git clone git://github.com/plone/plone.portlets.git

Then, add the following to *buildout.cfg*:

::

    [buildout]
    ...
    eggs =
        ...
        plone.portlets
    
    develop =
        src/plone.portlets

Note that:


-  The *develop*option contains a relative path to where the source
   egg is installed. Buildout will expect to find a suitable
   *setup.py* in this directory.
-  Development eggs always take precedence over regular eggs.
-  You still need to list the egg name in the *eggs* option for it
   to be installed.
-  If you are overriding an egg that ships with Plone, you may need
   to list it in the eggs section of the *[plone]* part instead:

::

    [buildout]
    ...
    develop =
        src/plone.portlets
    
    ...
    
    [plone]
    recipe = plone.recipe.plone
    eggs = 
        plone.portlets

This is because *plone.recipe.plone* is very explicit about which
versions of its various eggs to use, to ensure Plone keeps running
as it was released.

Buildout recipes (such as *plone.recipe.plone*) are distributed as
eggs. You can use a development egg of a recipe by listing it under
the *develop* option. There is no need to explicitly list it under
the *eggs* option, since it is referenced by the *recipe* option of
the relevant part.

Installing a traditional Zope 2 product
---------------------------------------

The easiest way to try out a traditional Zope 2 product is to
extract it into the *products*/ folder inside the buildout. If you
see documentation referring to the *Products/* folder in a Zope
instance, this is the same thing.

However, this approach makes it harder to redistribute your project
and share it with other developers. It is often more predictable to
let buildout download and install the package for you. You can do
this with the *[productdistros]* section of *buildout.cfg*. For
example, here is how you might install a product named
*ExampleProduct* and a set of products named
*ExampleProductBundle*:

::

    [productdistros]
    recipe = plone.recipe.distros
    urls =
        http://example.com/dist/ExampleProduct-1.0.tgz
        http://example.com/dist/ExampleProductBundle-1.0.tgz
    nested-packages =
        ExampleProductBundle-1.0.tgz
    version-suffix-packages =

Note that our fictional *ExampleProductBundle* is distributed as a
single directory containing a number of products in
sub-directories, so we list it under *nested-packages*.

As always, if you change *buildout.cfg*, you must re-run buildout:

::

    $ ./bin/buildout

Managing ZCML files
-------------------

It is important to realize that Zope will not load *configure.zcml*
files automatically for packages that are not in the *Products.\**
namespace and lack support for *z3c.autoinclude* (see next page for
more on using *z3c.autoinclude*). Instead, you must explicitly
reference the package. Buildout can create such a reference (known
as a ZCML **slug**) with the *zcml*option under the *[instance]*
part. Here is how to ensure that *borg.project* is available to
Zope:

::

    [buildout]
    ...
    eggs =
        elementtree
        borg.project
    
    ...
    
    [instance]
    ...
    zcml = 
        borg.project

Should you need to load an *overrides.zcml* or a *meta.zcml*, you
can use a syntax like:

::

    zcml =
        some.package
        some.package-overrides
        some.package-meta

Policy products
---------------

Many developers prefer to create a single "policy product" (also
known as a "deployment product") that orchestrates various
dependencies. If you have such a product, you may want to include
various dependencies directly from the policy product's
*configure.zcml* file, with lines such as:

::

    <configure xmlns="http://namespace.zope.org/zope">
    
        <include package="borg.project" />
    
    </configure>

In this case, you may still need one slug (using the *zcml* option
as above) for the policy product.


