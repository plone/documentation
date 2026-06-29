---
myst:
  html_meta:
    "description": "Override core Plone packages"
    "property=og:description": "Override core Plone packages"
    "property=og:title": "Override core Plone packages"
    "keywords": "Plone 6, core, package, version, override, Cookieplone, Buildout"
---

(override-core-plone-packages-label)=

# Override core Plone packages

Plone includes a few hundred Python packages.
Sometimes you will need to override one or more package versions to fix a bug.

## Override the version of a core Plone package

Plone's Python package dependencies are pinned to specific versions at the time a Plone release is created.
This section describes how to override the version of one of these packages, in case you need a newer one.

```{caution}
When you override package versions, the combination of packages isn't tested by the Plone development team.
Use at your own risk!
```

### Configure package installation

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

In the file {file}`pyproject.toml`, under the table `[tool.uv]`, edit `constraint-dependencies`.
This example uses `plone.api`.

```
[tool.uv]
constraint-dependencies = [
    "plone.api==2.0.0a3",
]
```
````

````{tab-item} pip
:sync: pip

In the file {file}`backend/mx.ini`, under the `[settings]` section, add `version-overrides` setting.
This example uses `plone.api`.

```
[settings]
version-overrides =
    plone.api==2.0.0a3
```

```{seealso}
The {file}`mx.ini` file configures a tool called {term}`mxdev`.
For an explanation of why Plone uses mxdev, see {ref}`manage-packages-mxdev-label`.
```
````

````{tab-item} Buildout
:sync: buildout

Update the file {file}`buildout.cfg`.
This example uses `plone.api`.

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

[versions]
plone.api = 2.0.0a3
```

```{note}
The version pins specified in the `[versions]` section will take precedence over the pins inherited from https://dist.plone.org/release/6-latest/versions.cfg.
```
````
`````

### Install the package

```{include} /_inc/_build-and-restart.md
```

## Install a core Plone package from source

A core Plone package can be installed from a source control system such as GitHub.
This is useful for developing and testing changes in core Plone packages.

### Configure package installation

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

This example uses `plone.restapi`.

Clone the repository into a local directory.

```shell
git clone git@github.com:plone/plone.restapi.git
```

Add the local directory to your uv project as an editable package.

```shell
cd backend
uv add --editable ../plone.restapi
```
````

````{tab-item} pip
:sync: pip

Add the Plone package you want to check out in the file {file}`backend/mx.ini`.
This example uses `plone.restapi`.

```cfg
[plone.restapi]
url = git@github.com:plone/plone.restapi.git
branch = main
extras = test
```

```{seealso}
The {file}`mx.ini` file configures a tool called {term}`mxdev`.
For an explanation of why Plone uses mxdev, see {ref}`manage-packages-mxdev-label`.
```
````

````{tab-item} Buildout
:sync: buildout

Update the file {file}`buildout.cfg`.
This example uses `plone.restapi`.

```cfg
[buildout]
extends =
    https://dist.plone.org/release/6-latest/versions.cfg
extensions = mr.developer
auto-checkout =
    plone.restapi

parts =
    instance

[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
http-address = 8080
eggs =
    Plone

[sources]
plone.restapi = git https://github.com/plone/plone.restapi.git

[versions]
plone.restapi =
```

```{tip}
Setting an empty version ensures that the copy of `plone.restapi` from source control will be used, instead of the version pin inherited from https://dist.plone.org/release/6-latest/versions.cfg.
```

```{seealso}
This approach uses the [`mr.developer`](https://pypi.org/project/mr.developer/) Buildout extension.
```
````
`````

### Install the package

```{include} /_inc/_build-and-restart.md
```
