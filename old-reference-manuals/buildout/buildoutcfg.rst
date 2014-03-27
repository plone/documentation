=============================
Understanding buildout.cfg
=============================

.. admonition:: Description

  How to manage the main buildout configuration file


**Important note:** This document applies to Plone 3.2 onwards. In
Plone versions prior to 3.2 the vanilla buildout.cfg file was
significatively different because Plone wasn't fully eggified.

*buildout.cfg* is the most important file in your new buildout
environment. Here is how it looks:

.. code-block:: cfg

    [buildout]
    parts =
        zope2
        productdistros
        instance
        zopepy
    
    # Change the number here, and in find-links below, to change the version of
    # Plone being used
    extends = http://dist.plone.org/release/3.3.5/versions.cfg
    versions = versions
    
    # Add additional egg download sources here. dist.plone.org contains archives
    # of Plone packages.
    find-links =
        http://dist.plone.org/release/3.3.5
        http://dist.plone.org/thirdparty
    
    # Add additional eggs here
    eggs =
        
    # Reference any eggs you are developing here, one per line
    # e.g.: develop = src/my.package
    develop =
    
    [zope2]
    recipe = plone.recipe.zope2install
    url = ${versions:zope2-url}
    
    # Use this section to download additional old-style products.
    # List any number of URLs for product tarballs under URLs (separate
    # with whitespace, or break over several lines, with subsequent lines
    # indented). If any archives contain several products inside a top-level
    # directory, list the archive file name (i.e. the last part of the URL, 
    # normally with a .tar.gz suffix or similar) under 'nested-packages'.
    # If any archives extract to a product directory with a version suffix, list
    # the archive name under 'version-suffix-packages'.
    [productdistros]
    recipe = plone.recipe.distros
    urls =
    nested-packages =
    version-suffix-packages = 
    
    [instance]
    recipe = plone.recipe.zope2instance
    zope2-location = ${zope2:location}
    user = admin:admin
    http-address = 8080
    # comment the following two options in production sites
    debug-mode = on
    verbose-security = on
    
    # If you want Zope to know about any additional eggs, list them here.
    # This should include any development eggs you listed in develop-eggs above,
    # e.g. eggs = Plone my.package
    eggs =
        Plone
        ${buildout:eggs}
    
    # If you want to register ZCML slugs for any packages, list them here.
    # e.g. zcml = my.package my.other.package
    zcml = 
    
    products =
        ${buildout:directory}/products
        ${productdistros:location}
    
    [zopepy]
    recipe = zc.recipe.egg
    eggs = ${instance:eggs}
    interpreter = zopepy
    extra-paths = ${zope2:location}/lib/python
    scripts = zopepy

Let us walk through this file step-by-step:

The main [buildout] section
~~~~~~~~~~~~~~~~~~~~~~~~~~~

The *[buildout]* section is the starting point for the file. It
lists a number of "parts", which are configured in separate
sections later in the file. Each *part* has an associated *recipe*,
which is the name of an egg that knows how to perform a particular
task, e.g. build Zope or create a Zope instance. A recipe typically
takes a few configuration options.

Our global settings are as follows:

.. code-block:: cfg

    [buildout]
    parts =
        zope2
        productdistros
        instance
        zopepy
    
    find-links =
        http://dist.plone.org/release/3.3.5
        http://dist.plone.org/thirdparty
    
    eggs =
        
    develop =

This specifies that the parts *zope2*, *productdistros*,
*instance* and *zopepy* will be run, in that order. Then, we tell
buildout that it can search one of a number of URLs when it is
looking for eggs to download. In addition, it will always search
the Cheese Shop.

Note that configuration entries are commonly split into multiple
lines. For this to work, all lines after the first must begin with
**at least 4 spaces**.

Next, we can list any eggs that buildout should download and
install for us. This may include version specifications. For
example, if you want sqlalchemy 0.3, but not 0.4, you could list;

.. code-block:: cfg

    eggs = 
        sqlalchemy>=0.3,<0.4dev

Please note that you will need the Python Imaging Library (PIL) for
Plone to work. This example assumes that you have this library
already installed and available from your Python interpreter, but
otherwise you can install a slightly modified (to workaround some
common problems) version from the "thirdparty" Plone repository in
your buildout adding its name to the eggs list:

.. code-block:: cfg

    eggs = PILwoTk

And the full path to the package in the find-links, e.g.:

.. code-block:: cfg

    find-links = http://dist.plone.org/thirdparty/PILwoTk-1.1.6.4.tar.gz

Finally, we can list development eggs, by specifying a directory
where the egg is extracted in source format. For example:

.. code-block:: cfg

    eggs =
        my.package
    
    develop = 
        src/my.package

This presumes that there is an egg called *my.package* in the
*src/* directory. We will learn how to create such eggs a little
later in this tutorial. Notice how we must also list my.package as
an actual egg dependency: development eggs are not automatically
added to the "working set" of eggs that are installed for Zope.

The *extends* and *versions* lines
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This part was introduced with Plone 3.2. It references a remote
file where the version of each needed package is specified. Check
that remote file to see yourself how these dependencies are
specified.

.. code-block:: cfg

    # Change the number here, and in find-links below, to change the version of
    # Plone being used
    extends = http://dist.plone.org/release/3.3.5/versions.cfg
    versions = versions

If you want to use a local file instead of a remote one to be able
to work offline, download it to your buildout directory and
reference it like this:

.. code-block:: cfg

    extends = versions.cfg

The [zope2] section
~~~~~~~~~~~~~~~~~~~

This part builds Zope 2, using
`plone.recipe.zope2install <http://cheeseshop.python.org/pypi/plone.recipe.zope2install>`_.
If you specified an existing Zope installation, you will not have
this part. Otherwise, it looks like this:

.. code-block:: cfg

    [zope2]
    recipe = plone.recipe.zope2install
    url = ${versions:zope2-url}

Here, we reference the download location for Zope as present in the
versions file. This ensures that we always get the recommended
version of Zope. You could specify a download URL manually instead,
if you wanted to use a different version of Zope.

When the recipe is run, Zope 2 is installed in *parts/zope2*. The
Zope software home becomes *parts/zope2/lib/python*.

The [productdistros] section
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This uses the
`plone.recipe.distros <http://cheeseshop.python.org/pypi/plone.recipe.distros>`_ recipe,
which is able to download distributions (archives) of Zope 2 style
products and make them available to Zope. It is empty to begin
with:

.. code-block:: cfg

    [productdistros]
    recipe = plone.recipe.distros
    urls =
    nested-packages =
    version-suffix-packages =

However, you can list any number of downloads. The recipe is also
able to deal with archives that contain a single top-level
directory that contains a bundle of actual product directories
(*nested-packages*), or packages that have a version number in the
directory name and thus need to be renamed to get the actual
product directory (*version-suffix-packages*).

Consider the following distributions:

::

    # A typical distribution 
    ExampleProduct-1.0.tgz
     |
     |- ExampleProduct
         |
         |- __init__.py
         |- (product code)
    
    # A version suffix distribution
    AnotherExampleProduct-2.0.tgz
     |
     |- AnotherExampleProduct-2.0
         |
         |- __init__.py
         |- (product code)
    
    # A nested package distribution
    ExampleProductBundle-1.0.tgz
     |
     |- ExampleProductBundle
         |
         |- ProductOne
         |   |- __init__.py
         |   |- (product code)
         | 
         |- ProductTwo
             |- __init__.py
             |- (product code)

Here is what the part would look like if we try to install the
three distributions above:

.. code-block:: cfg

    [productdistros]
    recipe = plone.recipe.distros
    urls =
        http://example.com/dist/ExampleProduct-1.0.tgz
        http://example.com/dist/AnotherExampleProduct-2.0.tgz
        http://example.com/dist/ExampleProductBundle-1.0.tgz
    nested-packages = ExampleProductBundle-1.0.tgz
    version-suffix-packages = AnotherExampleProduct-2.0.tgz

You can specify multiple downloads on separate lines. When the
recipe is run, the product directories for downloaded products are
found in *parts/productdistros*.

The [instance] section
~~~~~~~~~~~~~~~~~~~~~~

The instance section pulls it all together: It configures a Zope
instance using the
`plone.recipe.zope2instance <http://cheeseshop.python.org/pypi/plone.recipe.zope2instance>`_ script.
Here is how it looks:

.. code-block:: cfg

    [instance]
    recipe = plone.recipe.zope2instance
    zope2-location = ${zope2:location}
    user = admin:admin
    http-address = 8080
    # comment the following two options in production sites
    debug-mode = on
    verbose-security = on
    
    eggs =
        Plone
        ${buildout:eggs}
    
    zcml = 
    
    products =
        ${buildout:directory}/products
        ${productdistros:location}

Here, we reference the Zope 2 installation from the *[zope2]* part
- if you specified a location yourself when creating the buildout,
you would see that one here. Then, we specify the initial admin
user and password used only when creating the initial database, and
the port that Zope will be bound to. We also turn on debug mode and
verbose security. They are useful for development, but remember to
turn them off in production sites since they can compromise the
security of your site. These options are used to generate an
appropriate *zope.conf* file for this instance. See the
`recipe page in the Cheese Shop <http://cheeseshop.python.org/pypi/plone.recipe.zope2instance>`_
for more details on the options available.

Next, we specify which eggs that will be made available to Zope.
This references the "global" eggs from the *[buildout]* section, as
well as Plone itself. You could add additional eggs here, though it
is generally easier to specify these at the top of the file, so
that they get included in the *${buildout:eggs}* working set.

Zope 3 *configure.zcml* files are not automatically loaded for eggs
or packages that lack *z3c.autoinclude* support and are not in the
*Products* namespace. To load ZCML files for a regular package, we
can make buildout create a ZCML slug by listing the package under
the *zcml* option:

.. code-block:: cfg

    zcml =
        my.package
        my.package-overrides

This assumes that *my.package* was previously referenced in the
buildout. This would load both the main *configure.zcml*and the
*overrides.zcml* file from this package. Over time, the need for
these entries should diminish, as *z3c.autoinclude* support becomes
widespread.

Finally, we list the various directories that contain Zope 2 style
products - akin to the *Products/* directory in a traditional
instance. Notice how the *products/* directory in the main buildout
directory comes first, followed by the products downloaded with the
*[productdistros]* part.

When the recipe is run, the Zope instance home will be
*parts/instance*, and a control script is created in
*./bin/instance*.

The [zopepy] section
~~~~~~~~~~~~~~~~~~~~

This final section creates a Python interpreter that has all the
eggs and packages (but not Zope 2 style products) that Zope would
have during startup. This can be useful for testing purposes.

.. code-block:: cfg

    [zopepy]
    recipe = zc.recipe.egg
    eggs = ${instance:eggs}
    interpreter = zopepy
    extra-paths = ${zope2:location}/lib/python
    scripts = zopepy

Here, we copy the eggs from the *[instance]* section, and include
in the pythonpath the Zope instance home.

When the recipe is run, the script will be created in
*./bin/zopepy*.
