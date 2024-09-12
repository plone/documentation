---
myst:
  html_meta:
    "description": "Installation notes for Plone Classic UI"
    "property=og:description": "Installation notes for Plone Classic UI"
    "property=og:title": "Installation notes for pip and buildout based installation paths"
    "keywords": "Plone, Classic UI, classic-ui, installation, pip, buildout"
---

(classic-ui-installation-label)=

# Installation

This sections describes how to install Plone 6 Classic UI.
Examples include the following.

- pip based install method
- buildout based install method

(classic-ui-installation-pip-label)=

## Quickstart pip based installation

install notes for linux

requirements:

- python3.10 or greater
- python venv module

in our example we use python3.12

On debian based systems you can install python with following command

```bash
sudo apt install python3.12 python3.12-dev python3.12-venv
```

Select a directory of your choice

```bash
mkdir -p /tmp/plone && cd /tmp/plone
```

Create a virtual environment

```bash
python3 -m venv ./venv
```

Activate the virtual environment

```bash
source ./venv/bin/activate
```

Install Plone and a helper package

```bash
pip install Plone cookiecutter
```

```bash
cookiecutter -f --no-input --config-file ./instance.yaml https://github.com/plone/cookiecutter-zope-instance
```

Deactivate the virtual environment

```bash
deactivate
```

minimal content for the `instance.yaml` file

```yaml
# please change the password to a secrue token!
default_context:
  initial_user_name: "admin"
  initial_user_password: "admin"
  wsgi_listen: "localhost:8080"
  debug_mode: false
  verbose_security: false
  db_storage: "direct"
  environment: {
    "zope_i18n_compile_mo_files": true,
  }
```

Start the instance for quick test

```bash
./venv/bin/runwsgi -v instance/etc/zope.ini
```

Your instance starts in foreground mode, which is only advisable for troubleshooting or for local demonstration purposes,

Now you can call the url `http://localhost:8080` in your browser and you can add a **Classic UI Plone site**

Let's have fun with Plone!

```{todo}
add an example to create a zeo installation
```

```{todo}
add an example to start the instance via for systemd
```

(classic-ui-installation-buildout-label)=

## Quickstart buildout based installation

install notes for linux

requirements:

- python3.10 or greater
- python venv module

in our example we use python3.12

On debian based systems you can install python with following command

```bash
sudo apt install python3.12 python3.12-dev python3.12-venv
```

Select a directory of your choice

```bash
mkdir -p /tmp/plone && cd /tmp/plone
```

Create a virtual environment

```bash
python3 -m venv .
```

Activate the virtual environment

```bash
source ./bin/activate
```

install requirements

```bash
pip install -r https://dist.plone.org/release/6-latest/requirements.txt
```

add a minimal `buildout.cfg` file to your directory

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
```

run buildout

```bash
buildout
```

Start the instance for quick test in foreground mode

```bash
./bin/instance fg
```

Start the instance normal

```bash
./bin/instance start
```

Stop the instance

```bash
./bin/instance stop
```

Your instance starts in foreground mode, which is only advisable for troubleshooting or for local demonstration purposes,

Now you can call the url `http://localhost:8080` in your browser and you can add a **Classic UI Plone site**

Let's have fun with Plone!
