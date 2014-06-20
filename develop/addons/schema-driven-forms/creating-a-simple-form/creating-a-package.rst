Creating a package
====================

**Giving our forms a home**

For the purposes of this tutorial, we will create a simple package that
adds the necessary dependencies. If you have an existing package that
requires a form, you should be able to add the same dependencies. If you
have read the :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/index>`, most of this should be familiar.

For details about creating new packages, see
:doc:`Bootstrapping Plone add-on development </develop/addons/paste>`.

First, we create a new package:

.. code-block:: bash

    $ paster create -t plone example.dexterityforms

After answering the relevant questions, we edit *setup.py* to add
*plone.app.z3cform* and *plone.directives.form* as dependencies. This
will pull in the other pre-requisites, including *plone.z3cform* and
*z3c.form* itself. We have also removed the *ZopeSkel* local command
support, which we will not need, although there is no harm in keeping it
in. Finally, we have added a *tests* extra to pull in
*collective.testcaselayer* for our integration tests.

::

    from setuptools import setup, find_packages
    import os

    version = '1.0b1'

    setup(name='example.dexterityforms',
          version=version,
          description="Examples of forms using plone.directives.form",
          long_description=open("README.rst").read() + "\n" +
                           open(os.path.join("docs", "HISTORY.rst")).read(),
          # Get more strings from https://pypi.python.org/pypi?%3Aaction=list_classifiers
          classifiers=[
            "Framework :: Plone",
            "Programming Language :: Python",
            ],
          keywords='',
          author='Martin Aspeli',
          author_email='optilude@gmail.com',
          url='http://plone.org/products/dexterity/documentation/manual/schema-driven-forms',
          license='GPL',
          packages=find_packages(exclude=['ez_setup']),
          namespace_packages=['example'],
          include_package_data=True,
          zip_safe=False,
          install_requires=[
              'setuptools',
              'plone.app.z3cform',
              'plone.directives.form',
          ],
          extras_require={
            'tests': ['collective.testcaselayer',]
          },
          entry_points="""
          [z3c.autoinclude.plugin]
          target = plone
          """,
          )

Next, we edit *configure.zcml* to add some boilerplate:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:genericsetup="http://namespaces.zope.org/genericsetup"
        xmlns:grok="http://namespaces.zope.org/grok"
        i18n_domain="example.dexterityforms">

        <includeDependencies package="." />
        <grok:grok package="." />

        <genericsetup:registerProfile
            name="default"
            title="Example forms"
            directory="profiles/default"
            description="Example forms using plone.directives.forms"
            provides="Products.GenericSetup.interfaces.EXTENSION"
            />

    </configure>

This will:

-  Include the configuration of the packages we have listed in the
   *install\_requires* line in *setup.py*. This saves us from manually
   including them with individual ZCML *<include />* statements.
-  “Grok” the package, to configure the forms we will add. See the
   :doc:`five.grok manual</develop/addons/five-grok/index>` for more details.
-  Create an installation profile that will install this package and its
   dependencies.

The installation profile contains the instructions to install our
package’s dependencies into the Plone site. We create a
*profiles/default* directory, and add to it a *metadata.xml*:

.. code-block:: xml

    <metadata>
        <version>1</version>
        <dependencies>
            <dependency>profile-plone.app.z3cform:default</dependency>
        </dependencies>
    </metadata>


We need to install *plone.app.z3cform* to ensure that our forms have the
proper widgets and templates available.

Next, we add a *message factory* to allow the titles and descriptions in
our form to be translated. We’ll do this in a module *interfaces.py* at
the root of our package:

::

    import zope.i18nmessageid
    MessageFactory = zope.i18nmessageid.MessageFactory('example.dexterityforms')

The name of the factory should normally be the name of the package.

Finally, we add this package to our *buildout.cfg* and re-run
*bin/buildout*.

::

    [buildout]
    extends =
        http://dist.plone.org/release/4-latest/versions.cfg
    ...
    develop =
        src/example.dexterityforms

    eggs =
        example.dexteriyforms

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


