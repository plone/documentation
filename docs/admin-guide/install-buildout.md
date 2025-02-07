---
myst:
  html_meta:
    "description": "Install Plone with Buildout"
    "property=og:description": "Install Plone with Buildout"
    "property=og:title": "Install Plone with Buildout"
    "keywords": "Plone 6, install, Classic UI, Buildout"
---

(install-buildout-label)=

# Install Plone with Buildout

This chapter describes how you can install Plone using {term}`Buildout`.

This is one way to install Plone with the Classic UI.
Using Buildout will be the most familiar approach for administrators who have experience with Plone 3, 4, or 5.

```{seealso}
For other installation options, see {ref}`get-started-install-label`.
```

(install-buildout-prerequisites)=


## Supported web browsers

```{include} /_inc/_install-browser-reqs-classic-ui.md
```


## Prerequisites for installation

-   For Plone 6.1, Python {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}


### Python

```{include} /_inc/_install-python-plone61.md
```


## Installation

Select a directory of your choice, and change it to your working directory.

```shell
mkdir -p <my_projects>/plone
cd <my_projects>/plone
```

Create a Python virtual environment.

```shell
python3 -m venv venv
```

Install the minimal Python packages needed in order to run Buildout.

```shell
venv/bin/pip install -r https://dist.plone.org/release/6-latest/requirements.txt
```



Create a {file}`buildout.cfg` file in your directory with the following contents.

```cfg
[buildout]
extends =
    https://dist.plone.org/release/6-latest/versions.cfg

parts =
    instance

[instance]
recipe = plone.recipe.zope2instance
# user = username:password - Use a secure token in a production environment.
user = admin:admin
http-address = 8080
eggs =
    Plone
```

Use Buildout's [`bootstrap` command](https://www.buildout.org/en/latest/topics/bootstrapping.html) to install a local `buildout` script in the {file}`bin` directory.

```shell
venv/bin/buildout bootstrap
```

Run Buildout.

```shell
bin/buildout
```

This may take a few minutes.

Whenever you change the Buildout configuration, run `./bin/buildout` again.

## Start Plone in foreground mode

Start the instance for a quick test in foreground mode:

```shell
bin/instance fg
```

```{include} /_inc/_create-classic-ui-instance.md
```


## Start Plone as a background service

Start the instance.

```shell
bin/instance start
```


## Stop Plone as a background service

Stop the instance.

```shell
bin/instance stop
```
