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


## Cookieplone

Use the following instructions if you installed Plone with Cookieplone.


### Override a core Plone package

Add a version override to the file {file}`mx.ini`.
This example uses `plone.api`.

```
[settings]
version-overrides =
    plone.api==2.0.0a3
```

```{seealso}
The {file}`mx.ini` file configures a tool called {term}`mxdev`.
For an explanation of why Plone uses `mxdev`, see {ref}`manage-backend-python-packages-label`.
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


### Install a core Plone package from source

You can also use `mxdev` to install core Plone packages from a source control system such as GitHub.

Add the Plone package you want to check out in the file {file}`mx.ini`.
This example uses `plone.restapi`.

```cfg
[plone.restapi]
url = git@github.com:plone/plone.restapi.git
branch = main
extras = test
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


## Buildout

Use the following instructions if you installed Plone with Buildout.

### Override a core Plone package

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
bin/buildout
```

Then restart your instance.

```{seealso}
{doc}`run-plone`
```


### Install a core Plone package from source

A core Plone package can be installed from a source control system such as GitHub.

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
