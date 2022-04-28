---
html_meta:
  "description": "Install Plone 6"
  "property=og:description": "Install Plone 6"
  "property=og:title": "Install Plone 6"
  "keywords": "installation, installing, buildout, pip, docker"
---

(backend-installation-label)=

# Installation

Some documentation about installation:

* [Installation instructions from the Mastering Plone 6 training](https://training.plone.org/5/mastering-plone/installation.html)
* {ref}`frontend-getting-started-installing-volto-label`
* [Community post](https://community.plone.org/t/our-pip-based-development-workflow-for-plone/14562) on work in progress with [`plone-kickstarter`](https://github.com/bluedynamics/plone-kickstarter) and [`mxdev`](https://github.com/bluedynamics/mxdev).

If you use Docker, we have some images:

* `plone/plone-backend` (5.2 and 6.0)
* `plone/plone-frontend` (Volto)
* `plone/plone-haproxy`

If you don't do Docker, you will have to do the backend by hand.
The links above should give you information on how to install the prerequisites, like Python, also on Windows.
Here, we will focus on Unix-like systems (Linux, Mac OSX), but Windows should work as well.
The steps are:

* Install the Plone (Classic) backend with buildout or pip.
* Create the Plone Site in the browser.
* Install the Plone frontend (Volto) with node.

Below we will install Plone 6.0.0a4.
You should use the latest from the Plone 6.0 series.
We install it with Python 3.9.
Python 3.7 and 3.8 are also supported.
Please use the most recent version supported by your platform.


(installation-backend-buildout-label)=

## Install backend with buildout

Change to a new directory and put a file `buildout.cfg` in it:

```ini
[buildout]
extends = https://dist.plone.org/release/6.0.0a4/versions.cfg
parts = instance

[instance]
recipe = plone.recipe.zope2instance
eggs =
    Plone
user = admin:admin
```

Install it with:

```shell
python3.9 -m venv .
bin/pip install -r https://dist.plone.org/release/6.0.0a4/requirements.txt
bin/buildout
bin/instance fg
```


(installation-backend-pip-label)=

## Install backend with pip

If you do not want to use buildout, you can install the Plone Python packages with `pip`.
Change to a new directory and then:

```shell
python3.9 -m venv .
bin/pip install -U pip setuptools wheel
bin/pip install Plone -c https://dist.plone.org/release/6.0.0a4/constraints.txt
bin/mkwsgiinstance -u admin:admin -d .
bin/runwsgi -v etc/zope.ini
```

Note: you may need to edit `etc/zope.conf` to add a `blob-dir`.
See [issue 3345](https://github.com/plone/Products.CMFPlone/issues/3345#issuecomment-953700024).


(installation-create-plone-backend-label)=

## Create Plone backend

After you have installed the backend with buildout or pip, open a browser and go to http://localhost:8080/.
Click 'Create a new Plone site' to prepare for the new Volto frontend.
If you want Plone Classic instead, click 'Create Classic Plone site'.
(If this button is not available, then you did not install `plone.volto` with buildout or pip. 'Create a new Plone site' will create a Classic site then.)

Note: For Volto, make sure the Path identifier is Plone. You can change this, but then you need to change some Volto frontend configuration as well.

Submit the form and your backend is ready.
If you want Classic Plone, you are done.
If you want the full Plone 6 with Volto, read on.


(installation-frontend-node-label)=

## Frontend with node

You should probably read the chapter on {ref}`frontend-getting-started-installing-volto-label`.
But the following gives you the general idea.

First you may want to install `nvm`, the Node Version Manager:

* On Linux: `apt-get install nvm`
* On Mac: `brew install nvm`
* Or use the installation procedure detailed in the [nvm documentation](https://github.com/nvm-sh/nvm)

You use `nvm` to install recent `node/npm/yarn` versions:

```shell
nvm install --lts
npm install --global yarn
```

Create a Volto project:

```shell
npm init yo @plone/volto
```

This will take long, and then ask for a project name.
It will create a directory with this name.
Go to that directory and start the frontend:

```shell
yarn start
```

In your browser go to [http://localhost:3000](http://localhost:3000/).

You are done. Welcome to Plone 6!
