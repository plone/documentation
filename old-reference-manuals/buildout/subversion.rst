====================================
Installing products from Subversion
====================================

.. admonition:: Description

  Sometimes Plone products are not eggified, but available only in
  Subversion version control repository. This how to tells how such
  product can be automatically installed in buildout installations.


A few buildout recipes provide direct version control checkout
functionality:


-  `plone.recipe.bundlecheckout`_ - recipe provides Subversion (and
   CVS) downloads. Always does checkout - not suitable if you change
   files.
-  `mr.developer`_ -  a zc.buildout extension which makes it easier
   to work with buildouts containing lots of packages of which you
   only want to develop some.

-  `infrae.subversion`_ - can do SVN update

In this example we use the later.

Step by step
------------

Add the *infrae.buildout* recipe to your *buildout.cfg*. Adding a
recipe means adding a new line to
[*buildout] parts=...myrecipename* at the beginning of the file and
then later a corresponding *[mypartname] recipe = xxx.yyy*
section.

::

    [buildout]

    parts =

        plone
        zope2
        productdistros
        svnproducts
        instance
        zopepy
        zopeskel

List all the URLs of the products you want in *svnproducts*
section. In the example below we checkout TickingMachine product.

::

    # Get TickingMachine directly from SVN since it's not eggified

    [svnproducts]
    recipe = infrae.subversion

    urls =
        http://tickingmachine.googlecode.com/svn/trunk TickingMachine

In the case you're installing an old product (not eggified) you
will also need to register it in the *[products]* section so that
they get added to your Python path:

::

    products =
        ${buildout:directory}/products
        ${productdistros:location}
        ${plone:products}
        ${svnproducts:location

After rerunning buildout, TickingMachine will be found under
parts/development-products folder.

Further information
-------------------


-  `infrae.subversion: a recipe against disaster`_
-  Note that pointing to trunk is only a good practice for active
   development. Anyone else that needs to use this technique should
   point to a tag or branch URL.

Certification errors and passwords
----------------------------------

Self-signed certificates are often used with Subversion
repositories. Since *infrae.subversion* is made for automatization,
it cannot accept security decisions for the user. So if you are
receiving certification validation errors and password prompts,
please access the Subversion repository first manually using svn
command. Accept the choice and the svn client will remember this in
your user account home folder. It is recommended not to use your
commit account for this, since storing passwords is insecure.

Here's an example about how to access a SVN repository using the
*svn ls* command and accepting the security decisions for the svn
client to remember them permanently:

::

     svn ls   https://svn.plone.org/svn/collective/collective.easytemplate/trunk
    Error validating server certificate for 'https://svn.plone.org:443':
     - The certificate is not issued by a trusted authority. Use the
       fingerprint to validate the certificate manually!
    Certificate information:
     - Hostname: *.plone.org
     - Valid: from Mon, 14 Jan 2008 08:35:24 GMT until Wed, 13 Jan 2010 08:35:24 GMT
     - Issuer: Plone Foundation, Houston, Texas, US
     - Fingerprint: 39:6e:42:08:44:65:aa:7b:cb:55:85:9a:0c:0c:13:95:16:aa:38:48

    (R)eject, accept (t)emporarily or accept (p)ermanently? p


.. _plone.recipe.bundlecheckout: https://pypi.python.org/pypi/plone.recipe.bundlecheckout
.. _mr.developer: https://pypi.python.org/pypi/mr.developer
.. _infrae.subversion: https://pypi.python.org/pypi/infrae.subversion
.. _`infrae.subversion: a recipe against disaster`: http://danielnouri.org/blog/devel/zope/infrae-subversion.html
