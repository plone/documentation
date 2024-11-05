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

## Prerequisites for installation

-   For Plone 6.0, Python {SUPPORTED_PYTHON_VERSIONS_PLONE60}
% TODO: These instructions install Plone 6.0.x. Uncomment next line and change the subsequent include when Plone 6.1 is released and "latest". 
% -   For Plone 6.1, Python {SUPPORTED_PYTHON_VERSIONS_PLONE61}


### Python

```{include} /_inc/_install-python-plone60.md
```


## Installation

Select a directory of your choice, and change it to your working directory.

```shell
mkdir -p <my_projects>/plone
cd <my_projects>/plone
```

Create a Python virtual environment.

```shell
python3 -m venv .
```

Install the minimal Python packages needed in order to run Buildout.

```shell
bin/pip install -r https://dist.plone.org/release/6-latest/requirements.txt
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

Run Buildout.

```shell
bin/buildout
```

This may take a few minutes.


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
