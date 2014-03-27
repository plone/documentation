Background: Third Party Theme Products
======================================

In this section, we will look at how to install a Plone theme that you
have downloaded from Plone.org/products, PyPi, etc. We will also show
how you can distinguish between an old-style 2.5 product and a new
egg-based one.

There are two kinds of theme products: newer **egg-based products**, and
older theme products that are in the **"magical Products namespace"**.
The type of theme product you are working with determines the steps you
must take to install your theme. We'll now see how to tell the
difference between the two.

Is the Theme Product Egg-Based or in the Product's Namespace?
-------------------------------------------------------------

First, we need to understand what egg-based means. If the theme, when
unzipped, is named plonetheme.whatever, or you generate a new theme
using the `Paster <http://plone.org/how-to/use-paster>`_ recipe and
answer "yes" to the "is this a Zope2 product", then your theme product
is egg-based. On an even simpler note, if the root folder contains
setup.py, it's an egg. In a typical egg-based theme product, setup.py
would look something like this, where the highlighted text is the name
of the egg.

::

    from setuptools import setup, find_packages

    version = '1.1'

    setup(name='webcouturier.icompany.theme',

    [...]

If the product looks like it was created using DIYPloneStyle 3.x (now
outdated), it lives in the Products namespace. You can also tell that
you are working with a theme in the Products namespace because there is
no setup.py file in the root.

Installing an Egg-based Product
-------------------------------

We recommend using buildout to install an egg-based product. You can
decide whether you want to download the package yourself or leave
buildout to do it for you. If the former, then follow the instructions
in the previous section. If you want to leave the download up to
buildout, then buildout configuration is simpler:

 

[configuration here]

Dependencies
~~~~~~~~~~~~

If another package depends on the theme egg or includes its ZCML
directly, you do not need to specify anything in the buildout
configuration; buildout will detect this automatically. This is
considered a more advanced topic. Similarly, if the theme egg depends on
another product, then buildout will take care of this too.

Installing a Product if it is in the 2.x Products namespace
-----------------------------------------------------------

Assuming the theme product is an older 3.x theme and that it is in the
Products namespace, all you have to do is place the theme product in
your buildout's "products/" directory and restart your Zope instance.
There is no need to rerun your buildout, because we have not changed any
ZCML code.

Then, after your Zope has restarted, go to the 'Site Setup' page in the
Plone interface and click on the 'Add/Remove Products' link. The 'Site
Setup' area is also known as plone\_control\_panel, as this is the URL
used to get to 'Site Setup'.

Choose the product by selecting the checkbox next to it and click the
'Install' button.

Older themes in the Products namespace may show up twice in the
portal\_quickinstaller, but this is a bug that is fixed in a more recent
version of ZopeSkel. You can either ignore the bug or resolve it by
removing this line from your theme product's configure.zcml file and
restarting your Zope instance:

::

    <five:registerPackage package="." initialize=".initialize" />

Note: You may have to empty your browser cache to see the effects of the
product installation.
