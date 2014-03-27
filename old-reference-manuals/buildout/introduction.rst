============
Introduction
============

.. admonition:: Description

   Or: "What's wrong with a plain old Zope instance"?

This tutorial shows how to install Plone 3 into a *buildout*, and
how to use that buildout when working on a software project that
extends Plone. A buildout is a self-contained environment where you
can manage the dependencies (including Zope and Plone and any
third-party products or libraries you need) and custom code for
your project. Even if you are not planning on writing any custom
code, the buildout approach is an easy way to install Plone in a
robust, well-tested manner.  As of Plone 3.2, all of the installers
are now buildout based.

Prior to Plone 3.0, most developers and users who did not use a GUI
installer, would set up a Zope instance, drop in a few products
into the *Products* folder, and be done with it. Unfortunately, this
approach has a few problems:


-  Plain old Zope instances are not very well equipped to deal with
   packages distributed as python *eggs* or using setuptools
   *namespace packages*. Many new packages in Plone 3 are made in this
   way, and more and more third party modules will be as well.
-  Without access to the metadata that is held in eggs, developers
   may find it too time-consuming or confusing to factor their work
   into multiple packages that are more re-usable, preferring
   monolithic products that are impossible to re-use outside Zope.
-  Without any further tools, it is cumbersome to repeat a setup
   across different environments.

As eggs become more important, developers should look to employ
more appropriate tools for managing their code. **zc.buildout**,
hereafter referred to only as "buildout" is one such tool. This
tutorial shows how to use buildout for day-to-day development as
well as deployment.

More buildout documentation and background
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Buildout was created by Jim Fulton of Zope Corporation, and is
documented in depth at: `http://buildout.org/`_

.. _`http://buildout.org/`: http://buildout.org/
