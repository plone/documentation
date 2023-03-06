---
myst:
  html_meta:
    "description": "Prerequisites for content types"
    "property=og:description": "Prerequisites for content types"
    "property=og:title": "Prerequisites for content types"
    "keywords": "Plone, content types, prerequisites"
---

# Prerequisites

This portion of the Dexterity documentation mainly intends to illuminate Dexterity features.
If you would like an in-depth, step-by-step approach, we recommend you work through the [Mastering Plone](https://training.plone.org/) training.


## Prepare a development environment

First get a working Plone installation.
If you don't already have one, the easiest way to do so is to use one of Plone's installers.
Note that for development purposes, you may use a standalone (non-ZEO), non-root install.

Second add our standard development tools.
If you've used one of our installers, developer tool configurations are in a separate file, `develop.cfg`.
Once your site is running, you may activate the development configuration by using the command:

```shell
bin/buildout -c develop.cfg
```

Rather than running `bin/buildout` without arguments.
The `develop.cfg` config file extends the existing `buildout.cfg`.

The key tools that you'll need, both supplied by `develop.cfg`, are:

1.  `mr.bob`, a Python package skeleton builder;
1.  `bobtemplates.plone`, `mr.bob` templates for Plone; and
1.  A test runner and code quality testing tools.

If you've created yor own `buildout.cfg` file rather than using one of the installers, you'll need to add an equivalent development configuration.
The easiest way to do so is to pick up a copy from the [Unified Installer's repository](https://github.com/plone/Installers-UnifiedInstaller/blob/master/base_skeleton/develop.cfg).
To pick up `mr.bob` and the Plone templates alone, just add a `mrbob` part to your buildout:

```ini
[mrbob]
recipe = zc.recipe.egg
eggs =
    mr.bob
    bobtemplates.plone
```

Don't forget to add `mrbob` to your parts list.


## Creating a package

```{note}
We're going to build a package named `example.conference`.
You may find a completed version of it in the [Collective repository](https://github.com/collective/example.conference).
```

Typically, our content types will live in a separate package from our theme and other customizations.

To create a new package, we can start with `mrbob` and the `dexterity` template.

```{note}
Nothing that we're doing actually requires `mrbob` or the `bobtemplates.plone` skeleton package.
It's just a quick way of getting started.
```

We run the following from the `src/` directory

```shell
../bin/mrbob bobtemplates.plone:addon -O example.conference
```

and specify your target version of Plone and Python.
This will create a directory named `example.conference` inside `./src` with the basic structure of a generic add-on.
Now ["refine"](https://github.com/plone/bobtemplates.plone#provided-subtemplates) it for the creation of a content type.

```shell
../bin/mrbob bobtemplates.plone:content_type -O example.conference
```

Specify `Program` for your content type name, and `Container` as the Dexterity base class (remember that Programs will contain Sessions).
Choose not to use XML Model for this example.

Now take a look at the `setup.py` file in your new package.
Edit the `author`, `author_email`, and `description` fields as you wish.
Note a couple of parts of the generated `setup.py` file:

```python
install_requires=[

    'plone.app.dexterity',

],

entry_points="""
# -*- Entry points: -*-
[z3c.autoinclude.plugin]
target = plone
""",
```

The addition of `plone.app.dexterity` to our install requirements assures that we'll have Dexterity loaded, even in older versions of Plone.
The specification of `plone` as a `z3c.autoinclude.plugin` entry point ensures that we won't need to separately specify our `zcml` in buildout.

Now let's take a look at `configure.zcml` in the `examples/conference` directory of our project.
Again, we want to note a few parts:

```xml
<configure>

  <i18n:registerTranslations directory="locales" />

  <includeDependencies package="." />

  <include package=".browser" />

  <genericsetup:registerProfile
      name="default"
      title="collective.foo"
      directory="profiles/default"
      description="Installs the collective.foo add-on."
      provides="Products.GenericSetup.interfaces.EXTENSION"
      post_handler=".setuphandlers.post_install"
      />

  <genericsetup:registerProfile
      name="uninstall"
      title="collective.foo (uninstall)"
      directory="profiles/uninstall"
      description="Uninstalls the collective.foo add-on."
      provides="Products.GenericSetup.interfaces.EXTENSION"
      post_handler=".setuphandlers.uninstall"
      />

</configure>
```

Here, with the `includeDependencies` tag, we automatically include the ZCML configuration for all packages listed under `install_requires` in `setup.py`.
The alternative would be to manually add a line, such as `<include package="plone.app.dexterity" />` for each dependency.

The `include package=".browser"` directive loads additional ZCML configuration from the `browser` subdirectory.
In turn, the `browser.resourceDirectory` command in that configuration file creates a directory for static resources that we want to make available through the web.

Finally, we register a `GenericSetup` profile to make the type installable, which we will build up over the next several sections.

When you've got your project tuned up, return to your `buildout/instance` directory and edit `buildout.cfg` to add `example.conference` to your eggs list, and `src/example.conference` to your `develop` sources list:

```ini
eggs =
    Plone

    example.conference


develop =

    src/example.conference
```

Run `bin/buildout -c develop.cfg` to add your new product to the configuration, or just `bin/buildout` if you don't have a separate `develop.cfg`.

The buildout should now configure Plone, Dexterity, and the `example.conference` package.

We are now ready to start adding types.
