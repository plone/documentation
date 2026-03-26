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

For instructions of how to override a core Plone package, select the tab below according to your Python package manager.

```{tip}
Select the tab for uv if you have a project that was created using Cookieplone, and you have `managed = true` set in the `[tool.uv]` section of the file {file}`backend/pyproject.toml`.
Select the tab for pip if you have a project that was created using Cookieplone that does not have this setting.
```

`````{tab-set}

````{tab-item} uv

Edit `constraint-dependencies` in the file {file}`pyproject.toml`.
This example uses `plone.api`.

```
[tool.uv]
constraint-dependencies = [
    "plone.api==2.0.0a3",
]
```

Stop the backend with {kbd}`ctrl-c`.

To actually download and install the new package version, run the following command.

```shell
make backend-build
```

Now restart the backend.

```{seealso}
{doc}`run-plone`
```

````

````{tab-item} pip

Add a version override to the file {file}`mx.ini`.
This example uses `plone.api`.

```
[settings]
version-overrides =
    plone.api==2.0.0a3
```

```{seealso}
The {file}`mx.ini` file configures a tool called {term}`mxdev`.
For an explanation of why Plone uses `mxdev` for projects using pip as the Python package manager, see {ref}`manage-packages-mxdev-label`.
```

Stop the backend with {kbd}`ctrl-c`.

To actually download and install the new package version, run the following command.

```shell
make backend-build
```

Now restart the backend.

```{seealso}
{doc}`run-plone`
```

````

````{tab-item} Buildout

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
The version pins specified in the `[versions]` section will take precedence over the pins inherited from `https://dist.plone.org/release/6-latest/versions.cfg`.
```

To actually download and install the new package version, run the following command.

```shell
bin/buildout -N
```

Then restart your instance.

```{seealso}
{doc}`run-plone`
```

````

`````

## Install a core Plone package from source

A core Plone package can be installed from a source control system such as GitHub.

For instructions, select the tab below according to your Python package manager.

```{tip}
Select the tab for uv if you have a project that was created using Cookieplone, and you have `managed = true` set in the `[tool.uv]` section of the file {file}`backend/pyproject.toml`.
Select the tab for pip if you have a project that was created using Cookieplone that does not have this setting.
```

`````{tab-set}

````{tab-item} uv

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

Stop the backend with {kbd}`ctrl-c`.

Now restart the backend.

```{seealso}
{doc}`run-plone`
```

````

````{tab-item} pip

Add the Plone package you want to check out in the file {file}`mx.ini`.
This example uses `plone.restapi`.

```cfg
[plone.restapi]
url = git@github.com:plone/plone.restapi.git
branch = main
extras = test
```

```{seealso}
The {file}`mx.ini` file configures a tool called {term}`mxdev`.
For an explanation of why Plone uses `mxdev`, see {ref}`manage-packages-mxdev-label`.
```

Stop the backend with {kbd}`ctrl-c`.

To actually download and install the new package version, run the following command.

```shell
make backend-build
```

Now restart the backend.

```{seealso}
{doc}`run-plone`
```

````

````{tab-item} Buildout

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

````

`````
