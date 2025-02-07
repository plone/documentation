---
myst:
  html_meta:
    "description": "Install Plone with pip"
    "property=og:description": "Install Plone with pip"
    "property=og:title": "Install Plone with pip"
    "keywords": "Plone 6, install, Classic UI, pip"
---

(install-pip-label)=

# Install Plone with pip

This chapter describes how you can install Plone using {term}`pip`.

This is one way to install Plone with the Classic UI.
It provides a basic installation without many additional tools to help with development.

```{seealso}
For other installation options, see {ref}`get-started-install-label`.
```


## Supported web browsers

```{include} /_inc/_install-browser-reqs-classic-ui.md
```


(install-pip-prerequisites)=

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

Install Plone and a helper package, {term}`pipx`.

```shell
venv/bin/pip install -c https://dist.plone.org/release/6.1-latest/constraints.txt Plone pipx
```


## Create a Zope instance

Create a file {file}`instance.yaml` in your directory with the following contents.

```yaml
default_context:
  initial_user_name: "admin"
# Use a secure token for the password in a production environment.
  initial_user_password: "admin"
  wsgi_listen: "localhost:8080"
  debug_mode: false
  verbose_security: false
  db_storage: "direct"
  environment: {
    "zope_i18n_compile_mo_files": true,
  }
```

Now run the {term}`cookiecutter` tool to create configuration for a Zope instance.

```
bin/pipx run cookiecutter -f --no-input --config-file instance.yaml gh:plone/cookiecutter-zope-instance
```


## Start Plone in foreground mode

Start the instance for a quick test.

```shell
bin/runwsgi -v instance/etc/zope.ini
```

```{include} /_inc/_create-classic-ui-instance.md
```
