---
html_meta:
  "description": "Install Plone 6 from scratch – the installer"
  "property=og:description": "Install Plone 6 from scratch – the installer"
  "property=og:title": "Install Plone from scratch"
  "keywords": "Plone, Plone 6, install, pip, scratch, source, buildout"
---


(install-source-1-label)=

# Install Plone from Scratch

Installation from scratch is for development and it is reasonable for deployment with full control.

As an overview, you will perform the following steps in order.

1. [Install the Plone backend](install-source-install-backend-pip-label).
1. [Create a Plone instance](install-source-create-plone-site-label).
  Choose between an instance configured either for the Plone frontend or the Plone Classic UI.
1. [Install the Plone frontend](install-source-volto-frontend-label).


(install-source-components)=

## Short explanation of components and processes running

There are three processes continuously running when you have a working Plone 6 website:

1. A frontend web application running in your browser (JavaScript)
1. A Node.js server process that delivers the JavaScript to the client and does
   Server Side Rendering (SSR) of your pages on first request (JavaScript, the
   Razzle package is used for SSR)
1. A Plone server process that stores and delivers all content through a REST API (Python)

In case you decide for Plone Classic UI, you waive to the first two components and restrict to Plone which provides the Plone Classic frontend.


(install-source-backend-components-label)=

## Short explanation of Plone backend components

```{todo}
short explanation of backend components and how they interact
- {term}`Zope` instance
- Plone instance
- {term}`WSGI`
- REST API

Application server {term}`Zope` is working hard. {term}`Plone` provides the CMS stuff. {term}`WSGI` fills the gap between Python app Zope and web server. {term}`REST API` is the interface to request the Plone backend from thin air. The frontend {term}`Volto` does request this interface. Voilà.
```


(install-source-install-backend-pip-label)=

## Installation backend

We install the Plone backend with {term}`pip`, {term}`mxdev` and other fancy helpers.

You are probably familiar with a `buildout` Plone installation. The installation with `zc.buildout` was the way to go for Plone 5. Plone 6 prefers to be installed with {term}`pip`.


(install-source-system-requirements-label)=

### System requirements

- Raspberry Pi or more disk and CPU


(install-source-prerequisites-label)=

### Pre-requisites for the installation 

- Python 3.7, 3.8, 3.9 or 3.10.
- [Discord](https://discord.com/channels/786421998426521600/786421998426521603) account to say "Hello Plonistas! I installed Plone with pip, cookiecutter-zope-instance and mxdev. And I like it."



(install-source-installation-jump-label)=

### Installation – jump in and enfold the beauty

```{important}
There will be one single cookiecutter template to install both backend and frontend.
By now the chapter {ref}`install-source-stepbystep-start-label` is for you.
It explains the installation of the backend with `pip`.
```

<!-- TODO Add installation steps for future cookiecutter template 'cookiecutter-plone-starter' https://github.com/collective/cookiecutter-plone-starter/

Create a new directory to hold your project, make it your current directory, then issue the following commands in a shell session.

Create a Python virtual environment in the current directory.

```shell
python3.9 -m venv venv
source venv/bin/activate
```

Update Python package management tools.

```shell
pip install -U pip wheel
```

Install {term}`cookiecutter`:

```shell
pip install cookiecutter
```

You can now run `cookiecutter` to create a Zope instance sceleton with configuraton with the following command.


```shell
cookiecutter https://github.com/bluedynamics/plone-kickstarter
```

```{todo}
- Documentation driven implementation: plone-kickstarter: configure with mxmake [on top of] / [enhancing with scripts like test and check and you name it] mxdev.
- Move bluedynamics/plone-kickstarter to plone/plone-kickstarter in Plone repo?
- See mxmake in action:  https://github.com/rohberg/Plone_mxmake_example  for ONE single Makefile, ONE single requirements, ONE single constraints
```

Answer the prompts with:

```ini

project_name [acme.foo]: 
project_directory [acme.foo]: acme_foo
Select mode:
1 - standalone
2 - addon
Choose from 1, 2 [1]: 1
requirements_out [requirements-mxdev.txt]: 
admin_user [admin]: 
admin_password []: admin
plone_version [6.0.0a2]: 6.0.0a4
listen [localhost:8080]: 
```

Change to your project directory {file}`acme_foo`.

We are now working with `make`. All available commands are listed with
`make help`.

We could now build and run Zope / Plone with one command `make run`.\
Instead we customize the setting with additional add-ons and constraints of a Plone package and a checkout of a Plone package. -->


(install-source-tweak-backend-installation-label)=

### Tasks on your backend installation from scratch

You have installed Plone with `pip` like explained above or in {ref}`install-source-stepbystep-start-label`.

Add an add-on
: Add a line with the name of your add-on to `requirements.txt` and add it to {ref}`instance.yaml<install-source-cookiecutter-zope-instance-presets-label>`, then install with pip and apply cookiecutter:

  {file}`requirements.txt`:

  ```
  collective.easyform
  ```

  {file}`instance.yml`:

  ```yaml
  default_context:
      load_zcml:
          package_includes: ['collective.easyform']
  ```

  ```shell
  cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
  mxdev -c mx.ini
  pip install -r requirements-mxdev.txt
  ```

Pin the version of an add-on
: Pin the version in {file}`constraints.txt`:

  ```
  collective.easyform==3.1.0
  ```

  Add the add-on to {file}`requirements.txt`:

  ```
  collective.easyform
  ```

  Add it to {file}`instance.yml` to let Zope know that this add-on should be loaded:

  ```yaml
  default_context:
      load_zcml:
          package_includes: ['collective.easyform']
  ```

  Apply your changes and install:

  ```shell
  cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
  mxdev -c mx.ini
  pip install -r requirements-mxdev.txt
  ```


Checkout an add-on
: Add the add-on to {file}`requirements.txt`:

  ```
  collective.bookmarks
  ```

  Checkout with {file}`mx.ini`:

  ```ini
  [collective.bookmarks]
  url=git@github.com:collective/collective.bookmarks.git
  branch=master
  extras = test
  mxmake-test-path = src
  ```

  Add it to {file}`instance.yml` to let Zope know that this add-on should be loaded:

  ```yaml
  default_context:
      load_zcml:
          package_includes: ['collective.bookmarks']
  ```

  Apply your changes and install:

  ```shell
  cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
  mxdev -c mx.ini
  pip install -r requirements-mxdev.txt
  ```



Pin the version of a Plone package / constraints
: A version can **not** be pinned in constraints.txt if the package is mentionend in the constraints of Plone.
  Any other package version could be pinned in constraints.txt.
  A summary of section {ref}`install-source-checkout-and-pin` for a clean and well documented set up of your Zope/Plone installation:

  Pin the version of a Plone package in {file}`mx.ini`:

  ```ini
  [settings]
  # constraints of Plone packages
  version-overrides =
      plone.api>=2.0.0a3
  ```

  Apply the changes and install the package with the modified version by running `mxdev` and `pip`:

  ```shell
  mxdev -c mx.ini
  pip install -r requirements-mxdev.txt
  ```


Checkout a Plone package
: If you want to checkout a Plone Core package for development, this section is for you.

  Add the Plone package you want to check out in {file}`mx.ini`.

  ```ini
  [plone.restapi]
  url = git@github.com:plone/plone.restapi.git
  branch = master
  extras = test
  ```

  Apply the changes and install the package with the modified version with:

  ```shell
  mxdev -c mx.ini
  pip install -r requirements-mxdev.txt
  ```

  Restart Zope with

  ```shell
  runwsgi instance/etc/zope.ini
  ```


Build and start your instance
: Build and run Zope / Plone with one command:

  ```shell
  runwsgi instance/etc/zope.ini
  ```

  Head over to http://localhost:8080/ and see that Plone is running.

  Your instance is running in foreground. For a deamon, see section {ref}`install-source-process-manger`.


(install-source-deprecated-label)=

## Deprecated backend installation methods


(install-source-install-backend-buildout-label)=

````{admonition} Install backend with buildout (deprecated)
:class: toggle

Create a new directory to hold your project, make it your current directory, and create a new file inside it called `buildout.cfg`.
This file will refer to the latest version of Plone, and the `user` value that will be used in the next step to create a Plone site.
Paste the following configuration information into it.

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

Install Plone with the following shell commands.

```shell
# Create a Python virtual environment in the current directory
python3.9 -m venv .
# Install the latest Plone 6 requirements with pip
bin/pip install -r https://dist.plone.org/release/6.0.0a4/requirements.txt
# Run buildout to install Plone 6
bin/buildout
# Start the Plone instance
bin/instance fg
```

Then [create a Plone instance](install-source-create-plone-site-label).
````


(install-source-create-plone-site-label)=

## Create a Plone instance

After you have installed the backend ({ref}`install-source-install-backend-pip-label`), open a browser and visit http://localhost:8080/ to create a Plone instance.

Choose either Volto or Classic UI for the frontend.

- For a new Volto frontend, click {guilabel}`Create a new Plone site` to prepare a Plone sites backend.  
For Volto, make sure the `Path` identifier is `Plone`.
You can change this, but then you need to change some Volto frontend configuration as well.

- For a Plone Classic UI frontend, click {guilabel}`Create Classic Plone site`.

Submit the form and your backend is ready.

- If you created a Plone site with a Classic UI frontend, then you have completed the installation. Nearly. Enable your add-ons [^enable-add-ons].

- If you created a Plone site with a Volto frontend, continue with the next steps in section {ref}`install-source-volto-frontend-label`.


(install-source-volto-frontend-label)=

## Volto frontend

Now that you installed your backend and decided to go with the ReactJS frontend, the next steps explain how to generate a Volto project.

Instead navigate to {doc}`/classic-ui/index` if you do not want a ReactJs based frontend, but prefer to go with a Plone Classic frontend.

<!-- TODO strip all down to official Plone 6 frontend installation (from scratch. no docker) (https://6.dev-docs.plone.org/volto/getting-started/install.html#installing-volto) -->


(install-source-nvm-node-version-manager-label)=

### Install nvm (NodeJS version manager)

If you have a working Node JavaScript development already set up on your machine or you prefer
another management tool to install/maintain node this step is not needed. If you have less
experience with setting up JavaScript, it's a good idea to integrate nvm for development, as
it provides easy access to any NodeJS released version.

1.  Open a terminal console and type:

    ```bash
    touch ~/.bash_profile
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.39.1/install.sh | bash
    ```

    (Please check the latest available version of nvm on the [main README](https://github.com/nvm-sh/nvm)

1.  Close the terminal and open a new one or execute:

    ```bash
    source ~/.bash_profile
    ```

1.  Test it:

    ```bash
    nvm version
    ```

1.  Install any active LTS version of NodeJS (https://nodejs.org/en/about/releases/):

    ```{note}
    :class: margin
    Volto supports currently active NodeJS LTS versions based on [NodeJS
    Releases page](https://nodejs.org/en/about/releases/), starting with Node 14 LTS.
    ```

    ```bash
    nvm install 16
    nvm use 16
    ```

1.  Test NodeJS:

    ```bash
    node -v
    ```


(install-source-install-yarn-label)=

### Install Yarn (NodeJS package manager)

Install the Yarn Classic version (not the 2.x one!), of the popular node package manager.

```{tip}
:class: margin
As alternative, you can install `yarn` using several approaches too, depending on the
platform you are on. Take a look at the original `yarn`
[documentation](https://classic.yarnpkg.com/lang/en/) for a list of them.
```

1. Open a terminal and type:

    ```bash
    curl -o- -L https://yarnpkg.com/install.sh | bash
    ```

1. Test it, running:

    ```bash
    yarn -v
    ```


(install-source-create-volto-project-label)=

### Create a Volto project

Use the project generator helper utility.

1.  Open a terminal and execute:

    ```bash
    $ npm install -g yo @plone/generator-volto
    $ yo @plone/volto
    ```

    ````{tip}
    :class: margin
    You can run the generator with parameters to tailor your requirements.

    ```bash
    yo @plone/volto --help
    ```

    or take a look at the [README](https://github.com/plone/volto/blob/master/packages/generator-volto/README.md) for more information.
    ````

1.  Answer to the prompted questions and provide the name of the new app (folder) to be created. For the sake of this documentation, provide `myvoltoproject` as project name then.

1.  Change directory to the newly created folder `myvoltoapp` (or the one you've chosen):
    ```bash
    cd myvoltoapp
    ```

    Then start Volto with:

    ```bash
    yarn start
    ```

    This command will build an in-memory bundle and execute Volto in development mode.

Visit [http://localhost:3000](http://localhost:3000/) in your browser to see your new Plone 6 website.

Congratulations!
You have completed the installation of Plone 6 with Volto frontend.
Welcome to Plone 6!


<!-- TODO I have now my local environment with add-ons. How do I deploy? -->


(install-source-process-manger)=

## Process manager (he/she/you)

Run, stop, restart your backend and frontend and more with one command. In the background, for production. Get to know process manager {term}`pm2`!


Create an overall process configuration file {file}`pm2.config.js`:

```js
let apps = [
    {
      name   : "plone_backend_tutorial",
      script: 'runwsgi instance/etc/zope.ini',
      cwd: 'backend'
    },
    {
      name   : "plone_frontend_tutorial",
      script: 'yarn build && yarn start:prod',
      cwd: 'frontend'
    }
  ];

module.exports = { apps: apps };

```

Start all with:

```shell
pm2 start pm2.config.js
```

See processes managed by `pm2` (running and not running):

```shell
pm2 l
```

![List processes with 'pm2 l'](/_static/illustration/pm2.png)

Restart e.g. the backend process with:

```shell
pm2 start plone_backend_tutorial
```

Stop e.g. the backend process with:

```shell
pm2 stop plone_backend_tutorial
```



(install-source-tools-label)=

## Tools

- {term}`pip`
- {term}`mxdev`
% Future cookiecutter template for backend and frontend
% - {term}`cookiecutter-plone-starter`
- {term}`Yarn`

<!-- TODO Update used tools -->


## Footnotes

[^enable-add-ons]: enable add-ons (non-Plone-core packages) in {guilabel}`Site Setup` [http://localhost:8080/Plone/prefs_install_products_form](http://localhost:8080/Plone/prefs_install_products_form).
