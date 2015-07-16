Creating a package
====================

**Giving our forms a home**

For the purposes of this tutorial, we will create a simple package that
adds the necessary dependencies. If you have an existing package that
requires a form, you should be able to add the same dependencies. If you
have read the :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/index>`, most of this should be familiar.

For details about creating new packages, see
:doc:`Bootstrapping Plone add-on development </develop/addons/bobtemplates.plone/README>`.

.. note:: 

    Using paster is deprecated instead you should use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>`


First, we create a new package. When asked what kind of package needs to be
created, answer *Basic*.

.. code-block:: bash

    $ mrbob -O example.dexterityforms bobtemplates:plone_addon

After answering the relevant questions, we edit *setup.py* to add
*plone.app.z3cform* and *plone.directives.form* as dependencies. This
will pull in the other pre-requisites, including *plone.z3cform* and
*z3c.form* itself.

::

    # -*- coding: utf-8 -*-
    """Installer for the example.dexterityforms package."""

    from setuptools import find_packages
    from setuptools import setup


    long_description = (
        open('README.rst').read()
        + '\n' +
        'Contributors\n'
        '============\n'
        + '\n' +
        open('CONTRIBUTORS.rst').read()
        + '\n' +
        open('CHANGES.rst').read()
        + '\n')


    setup(
        name='example.dexterityforms',
        version='0.1',
        description="An add-on for Plone",
        long_description=long_description,
        # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        classifiers=[
            "Environment :: Web Environment",
            "Framework :: Plone",
            "Framework :: Plone :: 4.3.6",
            "Programming Language :: Python",
            "Programming Language :: Python :: 2.7",
        ],
        keywords='Python Plone',
        author='John Smith',
        author_email='john@plone.org',
        url='http://pypi.python.org/pypi/example.dexterityforms',
        license='GPL',
        packages=find_packages('src', exclude=['ez_setup']),
        namespace_packages=['example'],
        package_dir={'': 'src'},
        include_package_data=True,
        zip_safe=False,
        install_requires=[
            'plone.api',
            'setuptools',
            'z3c.jbot',
            # Extra dependencies for z3c forms
            'plone.app.z3cform',
            'plone.directives.form',
        ],
        extras_require={
            'test': [
                'plone.app.testing',
                'plone.app.contenttypes',
                'plone.app.robotframework[debug]',
            ],
        },
        entry_points="""
        [z3c.autoinclude.plugin]
        target = plone
        """,
    )


The installation profile contains the instructions to install our
package’s dependencies into the Plone site. Edit *metadata.xml*
in the *profiles/default* directory, and add the depencency:

.. code-block:: xml

    <?xml version="1.0"?>
    <metadata>
      <version>1000</version>
      <dependencies>
        <dependency>profile-plone.app.z3cform:default</dependency>
      </dependencies>
    </metadata>

We need to install *plone.app.z3cform* to ensure that our forms have the
proper widgets and templates available.

There are two options to continue working on the package. The easiest option
is to run the buildout from the *example.dexterityforms*. This allows you to
directly work on this package without an extra buildout. In this package a
buildout is included, for details on how to run buildout see
`docs on writing your own add-ons. <http://training.plone.org/5/eggs1.html`_

The second option is to add the package to an existing buildout. Add this
package to our *buildout.cfg* and re-run *bin/buildout*.

::

    [buildout]
    extends =
        http://dist.plone.org/release/4-latest/versions.cfg
    ...
    develop =
        src/example.dexterityforms

    eggs =
        example.dexterityforms

    ...

    [tests]
    recipe = zc.recipe.testrunner
    eggs =
        example.dexterityforms [tests]

Obviously, we have omitted large parts of the buildout configuration
here. The important things to note are:

-  We have included the known good set (KGS) of package versions for
   the latest 4.x release of Plone.
-  We list the new egg as a develop egg, and make sure it is in an eggs
   list that gets used for the Zope instance.
-  We use the [*tests]* extra when listing the testable eggs in the
   tests section. This ensures that *collective.testcaselayer* is
   installed for the testrunner.


