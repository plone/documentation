---
html_meta:
  "description": "Install Plone 6 from source"
  "property=og:description": "Install Plone 6 from source"
  "property=og:title": "Install Plone 6 from source"
  "keywords": "Plone 6, install, buildout, pip, Docker, source"
---


(install-source-1-label)=

# Install from source for development

As an overview, you will perform the following steps in order.

1.  Install the Plone backend (which includes the Classic UI) with either [buildout](install-source-install-backend-label) or [pip](install-source-install-backend-pip-label).
1.  Create the Plone Site in a web browser, choosing either the new Volto or the Classic UI for a frontend.
1.  Install the Plone frontend (Volto) with node.


(install-source-system-requirements-label)=

## System requirements

To install Plone 6, you must satisfy system requirements.

```{todo}
Add any missing requirements, including disk space.
```

-   2GB if using a container image, 4GB RAM if installing manually.
-   Disk space (TBD).
-   Either a UNIX-like operating system—such as Linux, Ubuntu, macOS—or Windows.
    For Windows, it is a good idea to use [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/).
    We strongly recommend using a recent version of your operating system released within the last 3 years.
    Older systems might not be supported.
-   Python 3.7, 3.8, or 3.9.
-   [Other?]


(install-source-2-label)=

## Backend source / frontend source explanation


(install-source-3-label)=

## Pip install  / cookiecutter


(install-source-4-label)=

## Mxdev


(install-source-5-label)=

## Tox


(install-source-5-label)=

## Deprecated installation methods


(install-source-5-a-label)=

### Buildout


(install-source-5-b-label)=

### Universal installer? (based on buildout) -> container




```{todo}
Move parts of the subsequent content into their appropriate section headings above.
```

(install-source-install-backend-label)=

### Install the Plone backend

You can install the Plone backend with either [buildout](install-source-install-backend-label) or [pip](install-source-install-backend-pip-label).


(install-source-install-backend-buildout-label)=

#### Install backend with buildout

Create a new directory to hold your project, make it your current directory, and create a new file inside it called `buildout.cfg`.
This file will refer to the latest version of Plone, and the `user` value that will be used in the next step to create a Plone site.
Paste the following configuration information into it.

```ini
[buildout]
extends = https://dist.plone.org/release/6.0.0a6/versions.cfg
parts = instance

[instance]
recipe = plone.recipe.zope2instance
eggs =
    Plone
user = admin:admin
```

Install Plone with the following shell commands.

```shell
# Create a Python virtual environment in the current directory
python3.9 -m venv .
# Install the latest Plone 6 requirements with pip
bin/pip install -r https://dist.plone.org/release/6.0.0a6/requirements.txt
# Run buildout to install Plone 6
bin/buildout
# Start the Plone instance
bin/instance fg
```


(install-source-install-backend-pip-label)=

#### Install backend with pip

Create a new directory to hold your project, make it your current directory, then issue the following commands in a shell session.

```shell
# Create a Python virtual environment in the current directory
python3.9 -m venv .
# Update Python package management tools
bin/pip install -U pip setuptools wheel
# Install Plone 6 with constrained requirements with pip
bin/pip install Plone -c https://dist.plone.org/release/6.0.0a6/constraints.txt
# Create a Plone 6 site with the given username and password in the current directory
bin/mkwsgiinstance -u admin:admin -d .
# Initialize Zope
bin/runwsgi -v etc/zope.ini
```

```{warning}
You might need to edit `etc/zope.conf` to add a `blobstorage` node with a `blob-dir` entry.
See [issue 3345](https://github.com/plone/Products.CMFPlone/issues/3345#issuecomment-953700024).
```


(install-source-create-plone-site-label)=

## Create a Plone site

After you have installed the backend with buildout or pip, open a browser and visit http://localhost:8080/.

Choose either Volto or Classic UI for the frontend.

-   For a new Volto frontend, click {guilabel}`Create a new Plone site` to prepare a Plone site and its backend.

    ```{note}
    If this button is not available, then you did not install `plone.volto` with buildout or pip.
    ```

    ```{attention}
    For Volto, make sure the `Path` identifier is `Plone`.
    You can change this, but then you need to change some Volto frontend configuration as well.
    ```

-   For a Plone Classic UI frontend, click {guilabel}`Create Classic Plone site`.

Submit the form and your backend is ready.

If you created a Plone site with a Classic UI frontend, then you have completed installation.

If a created a Plone site with a Volto frontend, continue with the next steps.


(install-source-volto-frontend-node-label)=

## Volto frontend with node

We recommend that you read the chapter {ref}`frontend-getting-started-installing-volto-label` for details.


(install-source-nvm-node-version-manager-label)=

### `nvm`, the Node Version Manager

We recommend that you install [`nvm`, or Node Version Manager](https://github.com/nvm-sh/nvm).
This makes it possible to switch to any version of [`node` (Node.JS)](https://nodejs.org/en/) and [`npm` (Node Package Manager)](https://www.npmjs.com/) for any project on which you might work.

-   On Linux: `apt-get install nvm`
-   On Mac: `brew install nvm`
-   Or use the installation procedure detailed in the [nvm documentation](https://github.com/nvm-sh/nvm)

With `nvm` installed, you can use it to install and use a supported version of `node` and `npm` using the following shell commands.

```shell
nvm install 16
nvm use 16
```


(install-source-install-yarn-label)=

## Install Yarn

Volto requires [Yarn Classic](https://classic.yarnpkg.com/lang/en/), a dependency manager for JavaScript code.
Install Yarn with the following command.

```shell
npm install --global yarn
```


(install-source-create-volto-project-label)=

### Create a Volto project

Create a Volto project using the following shell command.

```shell
npm init yo @plone/volto
```

This will take some time ☕️.
Toward the end of the process, it will ask you for a project name.
Enter the name of your project, using only lowercase letters.
It will create a directory with this name.
Go to that directory and start the frontend with the following command.

```shell
yarn start
```

In your browser, visit [http://localhost:3000](http://localhost:3000/).

Congratulations!
You have completed the installation of Plone 6 with Volto for its frontend.
Welcome to Plone 6!


(install-source-additional-references-label)=

## Additional references

-   [Installation instructions from the Mastering Plone 6 training](https://training.plone.org/5/mastering-plone/installation.html)
-   {ref}`frontend-getting-started-installing-volto-label`
-   [Community post](https://community.plone.org/t/our-pip-based-development-workflow-for-plone/14562) on work in progress with [`plone-kickstarter`](https://github.com/bluedynamics/plone-kickstarter) and [`mxdev`](https://github.com/bluedynamics/mxdev).
