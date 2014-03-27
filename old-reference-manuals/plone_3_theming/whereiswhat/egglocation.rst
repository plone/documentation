Where's my Egg Location?
========================

It is easy enough for Zope to find your eggs, harder for humans.

Plone version 3.1.2 onwards
---------------------------

Core Plone Default Products
    For core products used in the Plone Default Theme, buildout has an
    eggs directory

    -  [your buildout]/eggs

    which is where eggs are automatically dropped when Plone is
    installed.
Your own theme product
    Because your own theme product will be under development, this will
    go in a separate place in your buildout

    -  [your buildout]/[zinstance\|zeocluster\|]/src

(note that to share eggs between buildouts you can specify a different
location for this in a buildout defaults file, check the `buildout
tutorial on
plone.org <http://plone.org/documentation/tutorial/buildout/creating-a-buildout-defaults-file>`_
for more information).

Using Omelette to get at your eggs quickly
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

It is a bit of a drag navigating your way around all the eggs used by
Plone. David Glick's Omelette recipe creates a unified directory
structure of all namespace packages, symlinking to the actual contents,
via buildout. Full instructions and documentation on this can be found
here:

`http://pypi.python.org/pypi/collective.recipe.omelette <http://pypi.python.org/pypi/collective.recipe.omelette>`_

Once you've re-run buildout with the omelette recipe, you'll find that
you have a new section here:

-  [your buildout]/[zinstance\|zeocluster]/parts/omelette

and eggs such as plone.app.layout can be found in:

-  [your
   buildout]/[zinstance\|zeocluster]/parts/omelette/plone/app/layout

Plone version 3.1.1 or lower
----------------------------

Plone Installer
    If you have installed Plone with an installer, then the eggs will
    probably have been dropped into

    -  [your plone installation]/Python/Lib/site-packages.

    However, if you've used the Plone 3.1 universal installer, then you
    will have a buildout based installation.
The Plone Product Package
    If you used the product package (i.e. installed from source), then
    you may well find them in

    -  [your Zope instance]/lib/python.


