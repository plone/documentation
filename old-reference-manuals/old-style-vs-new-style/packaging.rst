Packaging
=========

To understand Plone's packaging story you must first understand **both** the
historic Zope2 add-on packaging story **and** the present day Python packaging
story. It also doesn't hurt to understand the future of Python packaging.

Zope2 products
--------------

*Old style*

Zope2 introduces the concept of "products" which are bundles of Python source
code that live in a special "products" directory; Zope2 looks for these on
startup and then registers them if they meet a certain set of criteria.

The *specialized* creation and use of products in Zope2 has generally fallen
out of favor, and given way to the use of *generic* Python packages, which are
widely used by the rest of the Python community.

Python packages
---------------

*New style*

The Setuptools add-on module for Python introduces the concept of
Python packages, called "eggs" (although recently, they are more and more
being referred to as just packages to avoid any "cuteness" getting in the
way of the concept.)

.. Note::

    If the packaging story were over now, things would be simple; but life is
    never simple. What follows is an explanation of Setuptools vs. Distribute.
    Or if you will, old style (Setuptools) vs. new style (Distribute) within the
    new style of packaging (eggs).

Setuptools
----------

*Old style within new style*

There are several important things you should know about Setuptools:

* It's built on top of a core module called Distutils, but it itself is
  not part of the Python core.

* It was forked in 2009 into the Distribute project (based on a
  disagreement over frequency of releases, among other things).

* It continues to exist.

Based on the above criteria, and what follows below about Distribute, you may
sometimes (perhaps less frequently then in the case of products vs. packages)
hear Setuptools referred to as "old style" and Distribute referred to as "new style".
And even if you don't, being aware of the distinction will certainly help you
understand "new style" packaging better.

Distribute
----------

*New style within new style*

Distribute is a fork of Setuptools. It is intended to "get us through" to the
point where a better solution can be implemented within the Python core in
the Distutils2 module which is currently in development (as of early 2011). 

Distribute is actively maintained, has frequent bug fixes and releases, and
is the self-proclaimed "new hotness".

And the "new hotness" part is no false promise. Using Distribute means you are using
the newest Python packaging technology short of Distutils2. One of the promises of
Distribute is using it will prepare you as gently as possible for the arrival of
Distutils2.
