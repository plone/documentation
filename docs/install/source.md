---
html_meta:
  "description": "Install Plone 6 from source"
  "property=og:description": "Install Plone 6 from source"
  "property=og:title": "Install Plone 6 from source"
  "keywords": "Plone 6, install, buildout, pip, Docker, source"
---


(install-source-1-label)=

# Install Plone from Source

Installation from source is for development and it is reasonable for deployment with full control.

As an overview, you will perform the following steps in order.

1.  [Install](install-source-install-backend-pip-label) the Plone backend.
1.  [Create](install-source-create-plone-site-label) a Plone instance, choosing between an instance, configured either for the Plone frontend or the Plone Classic UI.
1.  [Install the Plone frontend](install-source-volto-frontend-label).


(install-source-2-label)=

## Short explanation of backend components

Skip to {ref}`install-source-install-backend-pip-label` if you know it.

```{todo}
short explanation of backend components:
- Zope instance
- Plone instance
- wsgi
```

(install-source-install-backend-pip-label)=

## Installation backend

We install the Plone backend with `pip`, `cookiecutter-zope-instance`, `mxstack` and other fancy helpers.

You are maybe familiar with a `buildout` Plone installation. The installation with `zc.buildout` was the way to go for Plone 5. Plone 6 prefers to be installed with `pip`.


(install-source-system-requirements-label)=

### System requirements

-   Python 3.7, 3.8, 3.9 or 3.10.
-   Raspi or more disk and CPU


(install-source-prerequisites-label)=

### Pre-requisites for the installation 

- Python
- [Discord](https://discord.com/channels/786421998426521600/786421998426521603) account to say "Hello Plonistas! I installed Plone with pip, cookiecutter-zope-instance and mxstack. And I like it."



(install-source-installation-jump-label)=

### Installation – jump in and enfold the beauty

```{admonition} Under the hood
:class: margin

Go to {ref}`install-source-stepbystep-start-label` if you want to develop and want to know the details.
```

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
Instead we customize the setting with additional add-ons and constraints of a Plone package and a checkout of a Plone package.

First, a look on the generated directory content:

`instance.yaml`
: Load add-ons, configure the storage, etc..

`requirements.txt`
: List your add-ons to be installed with `pip`.

`mx.ini`
: Constraints and checkouts of Plone packages. Configure scripts like `test` to be generated.

`constraints.txt`
: Basic constraints of Plone, constraints of add-ons

### Add add-ons

% TODO describe how to add add-ons

Two steps are needed: pip install the code and configure Zope / Plone to use the Python package code of the add-ons.

Add the add-ons you want to use to {file}`instance.yaml`. This configures Zope / Plone to load the configuration of your add-ons.

```yaml

    load_zcml:
        package_includes: ['my.awesome.addon']
```

Add the add-on you want to use to your `requirements.txt` and pip install it.

`requirements.txt`:

```ini
my.awesome.addon
```

Run:

```shell
pip install -r requirements.txt
```

We could now build and run Zope / Plone with one command `make run`.


### Checkout add-on

TODO checkout an add-on for development


### Pin a Plone package to a higher version

% TODO describe how to modify constraints of Plone

If you  want to override the constraints of Plone, this section is for you.

Pin the version of a Plone package in {file}`mx.ini`:

```ini
[settings]
# constraints of Plone packages
version-overrides =
    plone.api>=2.0.0a3
```

Apply the changes and install the package with the modified version with:

```shell
make install
```

Under the hood happens a creation of a new constraints file and an installation with pip. See the step-by-step chapter for more info: {ref}`install-source-checkout-and-pin`.

Et voilà. Zope can be restarted with `make run`.


### Checkout a Plone package

% TODO describe how to checkout packages (Plone package or add-on)

If you want to checkout a Plone package (not add-on) for development, this section is for you.

Add the Plone package you want to checkout in {file}`mx.ini`.

```ini
[plone.restapi]
url = git@github.com:plone/plone.restapi.git
branch = master
extras = test
```

Apply the changes and install the package with the modified version with:

```shell
make install
```

Under the hood happens a creation of a new constraints file and an installation with pip. See the step-by-step chapter for more info: {ref}`install-source-checkout-and-pin`.

Et voilà. Zope can be restarted with `make run`.


### Build and start your instance

We can now build and run Zope / Plone with one command:

```shell
make run
```

Head over to http://localhost:8080/ and see that Plone is running.\
You can now [create a Plone instance](install-source-create-plone-site-label) and enable the add-on `my.awesome.addon` in {guilabel}`Site Setup` [http://localhost:8080/Plone/prefs_install_products_form](http://localhost:8080/Plone/prefs_install_products_form).



(install-source-deprecated-label)=

## Deprecated installation methods


(install-source-install-backend-buildout-label)=

````{admonition} Install backend with buildout (deprecated)
:class: toggle

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






```{todo}
TODO I have now my local environment with add-ons. How do I deploy?
```






(install-source-volto-frontend-label)=

## Volto frontend

We recommend that you read the chapter {ref}`frontend-getting-started-installing-volto-label` for details.

% TODO strip all to official Plone 6 frontend installation ()

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

### Install Yarn

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

## References

% TODO clean up references

- [Installation instructions from the Mastering Plone 6 training](https://training.plone.org/5/mastering-plone/installation.html)
- {ref}`frontend-getting-started-installing-volto-label`
- [Community post](https://community.plone.org/t/our-pip-based-development-workflow-for-plone/14562) on work in progress with [`plone-kickstarter`](https://github.com/bluedynamics/plone-kickstarter) and [`mxdev`](https://github.com/bluedynamics/mxdev).


(install-source-tools-label)=

## Tools

- {term}`mxdev`
- {term}`mxmake`
- {term}`cookiecutter`
- {term}`cookiecutter-zope-instance`


## Footnotes

[^enable-add-ons]: enable add-ons (non-Plone-core packages) in {guilabel}`Site Setup` [http://localhost:8080/Plone/prefs_install_products_form](http://localhost:8080/Plone/prefs_install_products_form).
