=======================
Creating a new package
=======================

.. admonition:: Description

  Adding a new custom package is not much different from installing a
  third-party one.


Creating a traditional Zope 2 product
-------------------------------------

To create a traditional Zope 2 product, put it in the top-level
*products/* directory and re-start Zope. Nothing more should be
required. As explained previously, products placed here will be
found automatically at start-up, and their *configure.zcml* files
will be executed automatically.

Creating an egg
---------------

Of course, if you are using products, you cannot benefit from the
additional features of eggs, including automatic dependency
management, distribution via the Cheese Shop and nested
namespaces.

The easiest way to create a new egg is to use the *paster*command,
which we already used to create the buildout. To create a new basic
package, with a top-level namespace (e.g. your company name) and a
specific name, go to the *src/* directory and run:

::

    $ cd src
    $ paster create -t plone myorg.mypackage

You will be asked a series of questions. Make sure that the
namespace package and package name correspond to the name of the
egg. In this case, the namespace package is *myorg* and the package
name is *mypackage*. In general, answer *False* to the question on
whether your package if "zip safe". Enter other metadata as
requested.

You will now have:


-  A *setup.py* which contains the metadata you entered
-  A package in *myorg.mypackage/myorg/mypackage*. Your source code
   goes here.
-  A skeleton *configure.zcml*, tests.py and a few other useful
   starting points.
-  Some generic documentation in *myorg.mypackage/docs*.

Of course, you must also add this package to the buildout. In
*buildout.cfg*, you might have:

::

    [buildout]
    ...
    eggs =
        ...
        myorg.mypackage
    
    develop =
        src/myorg.mypackage

Unless you plan to include this package from another one (or use
automatic ZCML loading, explained below), you probably also need a
ZCML slug:

::

    [instance]
    ...
    zcml =
        myorg.mypackage

Do not forget to re-run buildout after making the change:

::

    $ ./bin/buildout

Automate ZCML loading for your package
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you're not including your package from another one, you can
still avoid having to include a ZCML slug in *buildout.cfg* for it.
This is particulary useful to avoid unneccessary repetition of
package names in *buildout.cfg*, which beginner integrators might
easily overlook. From Plone 3.3 on, you can make your packages
signal that their ZCML should be included by adding:

::

    setup(...
      entry_points="""
      [z3c.autoinclude.plugin]
      target = plone
      """

to their *setup.py* file. For further information, see the
`setuptools documentation about dynamic discovery of services and plugins <http://peak.telecommunity.com/DevCenter/setuptools#dynamic-discovery-of-services-and-plugins>`_.` <http://peak.telecommunity.com/DevCenter/setuptools#id19>`_

Specifying dependencies
~~~~~~~~~~~~~~~~~~~~~~~

If your new package has explicit dependencies, you can list them in
*setup.py*. That way, buildout will be able to download and install
these as well. Dependencies are listed in the *install\_requires*
argument to the *setup()* method, By default, *setuptools*is listed
here, since we need this to support namespace packages. To add
*sqlalchemy*0.3 (but not 0.4), and the *MySQL-Python* driver, you
could amend this to read:

::

    install_requires=[
              'setuptools',
              'sqlalchemy>=0.3,<0.4dev',
              'MySQL-Python',
          ],

Uploading your egg to the Cheese Shop
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to share your package with the rest of the Python
community and make it easy to install using tools like buildout and
*easy\_install*, you can upload the package to the Cheese Shop.

Before doing so, you should:


-  Commit your latest changes and tag the release in Subversion, if
   applicable.
-  Make sure the version number in *setup.py* is correct. This
   should use common conventions such as "1.0b2" for the second beta
   of version 1.0, or "2.1.3rc1" for the first release candidate of
   version 2.1.3.
-  If you are using Mac OS X, run
   export COPY\_EXTENDED\_ATTRIBUTES\_DISABLE=true on the shell first
   - otherwise, the egg will contain Mac OS X resource forks which
   cause problems if your egg is used on Windows.

When you are ready, run the following command from your package's
directory (e.g. *src/myorg.mypackage*):

::

    $ python setup.py egg_info -RDb "" sdist register upload

This will ask you to create a Cheese Shop account if you do not
have one already. You can run this command as often as you'd like
to release a new version (probably with a new version number).


Creating development releases
------------------------------
When working on a project, you might want to generate development
releases of a project to push to a staging server. Instead of
increasing the version number in the ``setup.py`` file each time, you
can use the ``egg_info`` command to name the release appropiately.

For a complete list of the available options, run::

    $ python setup.py --help egg_info

If you're using subversion for version control, you can use the
revision numbers. For example, this will generate a targz package in
the ``dist`` folder named ``your.package-rXXXX``, where ``XXXX`` is a
revision number::

   $ python setup.py sdist egg_info -r

If you do nightly releases, tagging with the date is a good option::

   $ python setup.py sdist egg_info -d

If you don't want to enter the full command everytime you make a
release, you can use the setup.cfg file to set the defaults. For example:

.. code-block:: cfg

   [egg_info]
   tag_date = true
