# Creating A Package

**Giving our forms a home**

For the purposes of this tutorial, we will create a simple package that adds the necessary dependencies.

If you have an existing package that requires a form, you should be able to add the same dependencies.

For details about creating new packages, see
{doc}`Bootstrapping Plone add-on development </develop/addons/bobtemplates.plone/README>`.

```{note}
Using paster is deprecated instead you should use {doc}`bobtemplates.plone </develop/addons/bobtemplates.plone/README>`
```

~~~{deprecated} may_2015 Use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>` instead
~~~

First, we create a new package in src:

```shell
../bin/mrbob -O example.form bobtemplates:plone_addon
```

We create a package from the *Basic* template for Plone *5.0-latest*.

We will add example.form later as development egg to our buildout. Before we use the
autogenerated buildout of the package itself.

Take a look at buildout.cfg at the top level of our newly created package.
You will find there various useful things:

> - instance with your package added to the eggs
> - code analysis
> - a test runner
> - even a robot test runner
> - and a releaser

That is everything you need for development. Let us use this buildout.

```shell
cd example.form/
python bootstrap-buildout.py
bin/buildout
```

Let us test it!

```shell
bin/test -s example.form
bin/test -s example.form -t test_example.robot --all
```

Our package shall add a form to our Plone site. We use plone.app.z3cform to develop the form.

That is why we add it to install_requires in setup.py

```py
# -*- coding: utf-8 -*-
"""Installer for the example.form package."""

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
    name='example.form',
    version='0.1',
    description="An add-on for Plone",
    long_description=long_description,
    # Get more from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        "Environment :: Web Environment",
        "Framework :: Plone",
        "Framework :: Plone :: 5.0-latest",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
    ],
    keywords='Python Plone',
    author='John Doe',
    author_email='john@doe.org',
    url='http://pypi.python.org/pypi/example.form',
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
        'plone.app.z3cform',
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
```

and add plone.app.z3cform's import step to our profile's metadata.xml for an automated installation.

```xml
<metadata>
    <version>1000</version>
    <dependencies>
        <dependency>profile-plone.app.z3cform:default</dependency>
    </dependencies>
</metadata>
```

We have omitted large parts of the buildout configuration here.

The important things to note are:

- We have created a plone 5 add-on using mr.bob.
- We have tested the egg in a Plone test environment using the
  autogenerated buildout.cfg of our package.
- We have added dependencies to the egg.