====================================================================
 How to update and maintain collective.developermanual
====================================================================

.. admonition:: Description

        This document explains how collective.developermanual
        package is maintained and how changes are pushed.

.. contents :: :local:

.. highlight:: console

Introduction
==============

This document concerns those who:

* wish to generate a HTML version of Plone Developer Documentation

* need to edit templates or styles of Plone Developer Documentation, or
  otherwise customize Sphinx process

collective.developermanual
==========================

collective.developermanual_ is open-for-anyone-to-edit documentation for
Plone development in `Sphinx documentation format <http://sphinx.pocoo.org/>`_, living on 
`Github <https://github.com/collective/collective.developermanual>`_.
Anyone can provide patches through Github through-the-web editor and Pull request
mechanisms.

The ``collective.developermanual`` *git clone* contains buildout to:

* Install Sphinx 

* Install and clone necessary Plone packages referred by documentation (API docs)

* Compile the documentation to HTML

Setting up software for manual compilation
=======================================================

First you need to install Git for your operating system to be able to
retrieve the necessary source code::

    sudo apt-get install git # Debian-based Linux
         
or::

    sudo port install git-core # Mac, using MacPorts

.. note::

    You must not have Sphinx installed in your Python environment (this will
    be the case if you installed it using ``easy_install``, for example).
    Remove it, as it will clash with the version created by buildout.  Use
    ``virtualenv`` if you need to have Sphinx around for other projects.

Then clone ``collective.developermanual`` from GitHub::

    git clone git://github.com/collective/collective.developermanual.git

Run buildout to install Sphinx.
First step: bootstrap::

    python2.7 bootstrap.py
    ./bin/buildout

This will always report an error, but the ``bin/`` folder is created and
populated with the required scripts.  Now you need to checkout all the
source code using the *mr.developer* tool::

    ./bin/develop co ""

Run buildout again::

    ./bin/buildout

Analytics
---------

developer.plone.org pages have the Google Analytics script installed.
Please ask on the #plone.org IRC channel for data access.

Building static HTML with Sphinx
=================================

This creates the ``docs/html`` folder from the source documents in the
``source`` folder, by compiling all the ``collective.developermanual``
pages, using the ``sphinx-build`` command from buildout::

    ./bin/sphinx-build source build

If you want to build everything from the scratch, to see all warnings::

    rm -rf build
    ./bin/sphinx-build                                     

.. What about the Makefile? The above commands could also be e.g. 
   ``make html``. Is the Makefile being deprecated?

Editing CSS styles
---------------------

When ``sphinx-build`` is run it copies stylesheets from *sources* to
*build*.

For live editing of CSS styles you might want to do::

    cp source/_static/plone.css build/_static

Then copy back::

    cp build/_static/plone.css source/_static    

.. note ::

    Firefox does not follow symlinks on file:// protocol, and cannot load
    CSS files from them.

More info

* http://sphinx.pocoo.org/templating.html

* https://bitbucket.org/birkenfeld/sphinx/src/65e4c29a24e4/sphinx/themes/basic


Compiling the HTML manual
--------------------------

Use the Sphinx makefile::

    make html

.. Should this be changed? To the following:
    ./bin/sphinx-build source build


Setting up CSS for http://plone.org
-----------------------------------

An example ``sphinx.css`` is provided with ``collective.developermanual``.

* It sets up CSS for default Sphinx styles (notices, warning, other
  admonition).  
* It sets up CSS for syntax highlighting.  
* It resolves some CSS class conflicts between Sphinx and the plone.org
  theme.

``sphinx.css`` assumes that a special Sphinx ``page.html`` template is used.
This template is modified to wrap everything which Sphinx outputs in the
``sphinx-content`` CSS class, so we can nicely separate them from standard
Plone styles.

``page.html`` can be found at ``sources/_templates/page.html``.


