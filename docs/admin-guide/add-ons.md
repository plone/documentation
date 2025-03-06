---
myst:
  html_meta:
    "description": "Install Plone add-ons"
    "property=og:description": "Install Plone add-ons"
    "property=og:title": "Install Plone add-ons"
    "keywords": "Plone 6, add-on, package, plugin, extension, install"
---

(install-plone-add-ons-label)=

# Install Plone add-ons

This chapter explains how to install {term}`add-ons <add-on>` as Python packages to extend the functionality of the Plone backend or Classic UI.

```{note}
The Volto frontend has its own system of add-ons using Node.js packages.
See {doc}`/volto/development/add-ons/index`.
```


## Cookieplone

Use the following instructions if you installed Plone with Cookieplone.


### Install an add-on

Add a line with the name of your add-on in the file {file}`backend/requirements.txt`.
This example uses [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```
collective.easyform==4.2.1
```

```{tip}
Including the add-on version, or "pinning a version", ensures that it won't unintentionally get upgraded in the future.
```

Also add the add-on to `zcml_package_includes` in the file {file}`backend/instance.yaml` to make sure its configuration will be loaded.

```yaml
default_context:
    zcml_package_includes: project_title, collective.easyform
```

Stop the backend with {kbd}`ctrl-c`.

To actually download and install the new add-on, run the following command.

```shell
make backend-build
```

Now restart the backend.

```{seealso}
{doc}`run-plone`
```

In your web browser, and assuming you are currently logged in as an administrator, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

Then click the {guilabel}`Install` button next to your add-on to complete installation of the add-on.

Some add-ons have configuration options.
To configure such add-ons, return to the {guilabel}`Site Setup` control panel.
At the bottom of the page, you should see the heading {guilabel}`Add-on Configuration`, and a control panel to configure the add-on that you just installed.


### Install an add-on from source

An add-on can be installed from a source control system such as GitHub.

Add a line with the name of your add-on in the file {file}`backend/requirements.txt`.
This example uses [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```
collective.easyform
```

```{note}
When installing an add-on from source, it's best not to pin a version.
This way you always get the version that's currently available in the source control system.
```

Next add the add-on to `zcml_package_includes` in the file {file}`backend/instance.yaml` so that its configuration will load.

```yaml
default_context:
    zcml_package_includes: project_title, collective.easyform
```

Finally, add the package's source to the file {file}`mx.ini`.

```cfg
[collective.easyform]
url=git@github.com:collective/collective.easyform.git
branch=dev-branch-name
extras=test
```

```{seealso}
The {file}`mx.ini` file configures a tool called {term}`mxdev`.
See the [documentation of `mxdev` in its README.md](https://github.com/mxstack/mxdev/blob/main/README.md) for complete information.
```

Stop the backend with {kbd}`ctrl-c`.

To actually download and install the new add-on, run the following command.

```shell
make backend-build
```

Now restart the backend.

```{seealso}
{doc}`run-plone`
```

In your web browser, and assuming you are currently logged in as an administrator, visit the URL http://localhost:8080/Plone/prefs_install_products_form.
An upgrade step might need to be performed in the Plone control panel.
Follow the upgrade information, if present.
Else click the {guilabel}`Install` button to complete installation of the add-on.


## Buildout

Use the following instructions if you installed Plone with Buildout.

### Install an add-on

Update the file {file}`buildout.cfg`.
This example uses [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```cfg
[buildout]
extends =
    https://dist.plone.org/release/6-latest/versions.cfg

parts =
    instance

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
http-address = 8080
eggs =
    Plone
    collective.easyform

[versions]
collective.easyform = 4.2.1
```

```{tip}
Including the add-on version, or "pinning a version", ensures that it won't unintentionally get upgraded in the future.
```

To actually download and install the new add-on, run the following command.

```shell
bin/buildout
```

Then restart your instance.

```{seealso}
{doc}`run-plone`
```


### Install an add-on from source

You can install an add-on from a source control system such as GitHub.

Update the file {file}`buildout.cfg`.
This example uses [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```cfg
[buildout]
extends =
    https://dist.plone.org/release/6-latest/versions.cfg
extensions = mr.developer
auto-checkout =
    collective.easyform

parts =
    instance

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
http-address = 8080
eggs =
    Plone
    collective.easyform

[sources]
collective.easyform = git https://github.com/collective/collective.easyform.git
```

To actually download and install the new add-on, run the following command.

```shell
bin/buildout
```

Then restart your instance.

```{seealso}
{doc}`run-plone`
```

```{seealso}
This approach uses the [`mr.developer`](https://pypi.org/project/mr.developer/) Buildout extension.
```
