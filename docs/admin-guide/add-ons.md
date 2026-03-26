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

(install-an-add-on-from-pypi-label)=

## Install an add-on from PyPI

This section describes how to install an add-on that is released on {term}`PyPI`.


(configure-add-on-installation-pypi-label)=

### Configure add-on installation

First, configure your project according to the instructions in the tabbed interface below.
Select the tab according to the method you used to create your project.

`````{tab-set}
````{tab-item} Cookieplone
:sync: cookieplone

Add the name of your add-on in the file {file}`backend/pyproject.toml` in the section `dependencies`.
This example adds [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```{code-block} toml
:emphasize-lines: 6
dependencies = [
    "Products.CMFPlone==6.1.4",
    "plone.api",
    "plone.classicui",
    "plone.app.caching",
    "collective.easyform==4.5.1",
]
```

To configure the add-on to load, in the file {file}`backend/instance.yaml`, under the key `default_context`, for the key `zcml_package_includes`, set its value to the add-on's name.

```yaml
default_context:
    zcml_package_includes: project_title, collective.easyform
```
````

````{tab-item} Buildout
:sync: buildout

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
collective.easyform = 4.5.1
```
````
`````

```{tip}
You can control which version of an add-on to install through "version pinning."

-   Specify the add-on version to avoid its unintentional upgrade.
-   Leave it off to always install the latest version.
```


(install-the-add-on-pypi-label)=

### Install the add-on

```{include} /_inc/_build-and-restart.md
```

In your web browser, and assuming you are currently logged in as an administrator, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

Then click the {guilabel}`Install` button next to your add-on to complete installation of the add-on.

Some add-ons have configuration options.
To configure such add-ons, return to the {guilabel}`Site Setup` control panel.
At the bottom of the page, you should see the heading {guilabel}`Add-on Configuration`, and a control panel to configure the add-on that you just installed.


## Install an add-on from source

This section describes how to install an unreleased add-on from a source control system, such as GitHub.


(configure-add-on-installation-source-label)=

### Configure add-on installation

First, configure your project according to the instructions in the tabbed interface below.
Select the tab according to your Python package manager.

```{tip}
For projects created with Cookieplone, select the tab labeled:

-   {guilabel}`pip` if your project has the file {file}`backend/mx.ini`
-   {guilabel}`uv` if your project doesn't have this file
```

`````{tab-set}
````{tab-item} uv
:sync: uv

Clone the repository into a local directory.
This example uses [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```shell
git clone git@github.com:collective/collective.easyform.git
```

Add the local directory to your uv project as an editable package.

```shell
cd backend
uv add --editable ../collective.easyform
```

To configure the add-on to load, in the file {file}`backend/instance.yaml`, under the key `default_context`, for the key `zcml_package_includes`, set its value to the add-on's name.

```yaml
default_context:
    zcml_package_includes: project_title, collective.easyform
```
````

````{tab-item} pip
:sync: pip

Add the name of your add-on in the file {file}`backend/pyproject.toml` in the section `dependencies`.
This example adds [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```{code-block} toml
:emphasize-lines: 6
dependencies = [
    "Products.CMFPlone==6.1.4",
    "plone.api",
    "plone.classicui",
    "plone.app.caching",
    "collective.easyform",
]
```

To configure the add-on to load, in the file {file}`backend/instance.yaml`, under the key `default_context`, for the key `zcml_package_includes`, set its value to the add-on's name.

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
For an explanation of why Plone uses `mxdev`, see {ref}`manage-packages-mxdev-label`.
```
````

````{tab-item} Buildout
:sync: buildout

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

```{seealso}
This approach uses the [`mr.developer`](https://pypi.org/project/mr.developer/) Buildout extension.
```

````
`````

```{tip}
When installing an add-on from source, it's best not to pin a version.
This way you always get the version that's currently available in the source control system.
```


(install-the-add-on-source-label)=

### Install the add-on

```{include} /_inc/_build-and-restart.md
```

In your web browser, and assuming you are currently logged in as an administrator, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

Then click the {guilabel}`Install` button next to your add-on to complete installation of the add-on.

Some add-ons have configuration options.
To configure such add-ons, return to the {guilabel}`Site Setup` control panel.
At the bottom of the page, you should see the heading {guilabel}`Add-on Configuration`, and a control panel to configure the add-on that you just installed.
