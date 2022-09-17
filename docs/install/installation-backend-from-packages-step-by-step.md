---
myst:
  html_meta:
    "description": "Install Plone 6 backend from its packages for the one who wants to look under the hood"
    "property=og:description": "Install Plone 6 backend from its packages for the one who wants to look under the hood"
    "property=og:title": "Install Plone backend from its Packages – Step-by-step"
    "keywords": "Plone, Plone 6, install, backend, pip, mxdev, cookiecutter, packages, source, Zope, buildout"
---


(installation-backend-from-packages-step-by-step-start-label)=

# Install Plone backend from its Packages – Step-by-step

For system requirements and pre-requisites for the installation see {ref}`install-source-system-requirements-label`.

We install the Plone backend with `pip`, `cookiecutter-zope-instance`, `mxdev` and other developer tools.

```{note}
There will be one single cookiecutter template to install both backend and frontend from its packages.
You will find the instructions on {ref}`install-source-installation-jump-label`.
That chapter is for you if you want to develop and want to jump in with all steps prepared by an overall cookiecutter.
The subsequent sections explain the installation of the backend step-by-step.
You will learn the details of the installation included in the future overall cookiecutter.
```


(installation-backend-from-packages-installation-steps-label)=

## Installation steps

Create a new directory to hold your project and make it your current directory.
Next issue the following commands in a shell session to create a Python virtual environment in the current directory.

```shell
python -m venv venv
source venv/bin/activate
```

Update Python package management tools.

```shell
pip install -U pip wheel
```

````{admonition} packages tree
:class: margin toggle
The Plone packages and dependencies are installed in trees.

```
venv/lib/python3.x/site-packages
│
…
├── plone
│   ├── …
│   ├── app/
│       ├── caching/
│       ├── content/
│       └── …
…   
├── zope/
│   ├── …
```
````

Install Plone 6 with constrained requirements using `pip`.

```shell
pip install Plone -c https://dist.plone.org/release/{PLONE_BACKEND_VERSION}/constraints.txt
```

:::{admonition} <span>`mkwsgiinstance` creates a home with a minimal configuration for a Zope instance.</span>
:class: margin toggle

```
┌── etc/
│   ├── site.zcml
│   ├── zope.conf
│   └── zope.ini
├── inituser
└── var/
    ├── cache/
    ├── log/
    └── REAMDME.txt/
```
:::

(installation-backend-from-packages-step-by-step-mkwsgiinstance)=

Create a Zope instance with the given username and password in the current directory.

(install-source-mkwsgiinstance)=

```shell
mkwsgiinstance -u admin:admin -d .
```

````{admonition} All commands so far
:class: margin

```shell
python -m venv venv
source venv/bin/activate
pip install -U pip wheel
pip install Plone -c https://dist.plone.org/release/{PLONE_BACKEND_VERSION}/constraints.txt
mkwsgiinstance -u admin:admin -d .
```
````

Start the Zope instance.

```shell
runwsgi ./etc/zope.ini
```

It will take a few seconds to start the Zope instance.
You can stop the instance later with {kbd}`ctrl-esc`.

Before creating a Plone site on http://localhost:8080/, we configure our Zope instance for blobs, configure add-ons, and so on.

For the configuration, you have two options:
1. *manual* configuration by editing {file}`site.zcml` and {file}`zope.conf` (^[Configuring and Running Zope](https://zope.readthedocs.io/en/latest/operation.html))
2. *generate* configuration by applying `cookiecutter-zope-instance`

(install-source-cookiecutter-zope-instance-label)=

### Generate Plone / Zope configuration with cookiecutter

{term}`Cookiecutter` creates projects from project templates.
{term}`cookiecutter-zope-instance` is such a template that allows to create a complete Zope configuration. 
Zope configuration means:

- type of storage: direct filestorage/blobs, relational database, ZEO, you name it
- ports
- threads/caches
- debugging/profiling options

Install cookiecutter:

```shell
pip install cookiecutter
```

You could now run `cookiecutter` to create a Zope instance sceleton including configuration with the following command. It prompts you for parameter values.

```shell
cookiecutter https://github.com/plone/cookiecutter-zope-instance
```

(install-source-cookiecutter-zope-instance-presets-label)=

Instead we prepare a configuration file {file}`instance.yaml` with the parameters we want to set. 
In this section we will learn how to configure our `Zope` / `Plone` installation via `instance.yaml`.
A minimal example with one add-on configured:

```{note}
:class: margin
Reference of configuration options of [`cookiecutter-zope-instance`](https://github.com/plone/cookiecutter-zope-instance#options).
```

```yaml
default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'

    load_zcml:
        package_includes: ['collective.easyform']

    db_storage: direct
```

Add-ons are listed here to be loaded by `Zope` app. As python packages they also need to be installed with pip.
The documented installation of add-ons with pip is achieved via a {file}`requirements.txt` file.
We list an add-on like for example `collective.easyform` in\
`requirements.txt`:

```
collective.easyform
```

Install your requirements:

```shell
pip install -r requirements.txt
```

You have done two things so far: You installed your add-on packages and you have prepared an initializing file to roll out a Zope / Plone project, configured to load your installed add-on packages.

You are now ready to apply `cookiecutter` to generate the Zope configuration:

```shell
cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
```

```{list-table} Cookiecutter options used here
:header-rows: 1

* - Option
  - Effect
* - -f, --overwrite-if-exists
  - Overwrite the contents of the output directory if it already exists. Data in var stays untouched.
* - --no-input
  - Do not prompt for parameters and only use cookiecutter.json file content
* - --config-file instance.yaml
  - User configuration file
```

````{admonition} Summed up tasks and commands
:class: margin

Summed up tasks and commands after creating a Zope instance with {ref}`mkwsgiinstance <install-source-mkwsgiinstance>`:

- Create an {ref}`instance.yaml<install-source-cookiecutter-zope-instance-presets-label>` for presets.
- Create a `requirements.txt` for the installation of python packages.
- Install add-ons and generate Zope skeleton with configuration (apply cookiecutter)

  ```shell
  pip install -r requirements.txt
  cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
  ```
````

`cookiecutter` creates a new directory {file}`instance` with your Zope and Plone configuration. This directory will also comprise file storage, blob storage, etc..

It's time to start the new Zope instance.

```shell
runwsgi -v instance/etc/zope.ini
```

Head over to http://localhost:8080/ and see that Plone is running.
You could now create a Plone instance {ref}`install-source-create-plone-site-label` and enable the add-on `collective.easyform` in {guilabel}`Site Setup` [http://localhost:8080/Plone/prefs_install_products_form](http://localhost:8080/Plone/prefs_install_products_form).

If you want to run Plone with some add-ons, you are ready with the installation of the backend.\
If you decided to go with the Plone Classic UI this is also your frontend.\
If you decided to go with the Plone Volto frontend, then section {ref}`install-source-volto-frontend-label` explains your next steps.

If you want to develop a Plone package, then the subsequent section is for you.


(install-source-checkout-and-pin)=

### Checkout or version pinning of a Plone package

If you want to checkout a Plone Core package for development or just want to override the constraints of Plone, then a first attempt would be to define constraints with a {file}`constraints.txt` to tell pip to install a different version of a Plone package.

```
# constraints.txt with unresolvable version conflict
-c https://dist.plone.org/release/{PLONE_BACKEND_VERSION}/constraints.txt
plone.api>=2.0.0a3
```

Unfortunatly pip does not allow this way of overwriting constraints. 

`mxdev` is made for assembling Plone constraints with your needs of version pinning or source checkouts.\
It reads your {file}`requirements.txt` and so your {file}`constraints.txt`, fetches the requirements/constraints of Plone and writes the files {file}`requirements-mxdev.txt` and {file}`constraints-mxdev.txt`. 
Both are containing the combined requirements and constraints, but modified according to the configuration in {file}`mx.ini`. 
The generated files are transparent about where constraints were fetched from and comments are added when a modification was necessary.

In summary, mxdev operates on three files to tell pip which packages to install with which version.
A minimal example set of files would look like the following.

{file}`requirements.txt`

```ini
-c constraints.txt

Plone

# List of add-ons that are needed.
collective.easyform
```

{file}`constraints.txt`

```ini
-c https://dist.plone.org/release/{PLONE_BACKEND_VERSION}/constraints.txt

# constraints of add-ons
collective.easyform==3.4.5
```

{file}`mx.ini`

```ini
[settings]
# constraints of Plone packages
version-overrides =
    plone.api>=2.0.0a3

[plone.restapi]
url = git@github.com:plone/plone.restapi.git
branch = master
extras = test
```

A run of mxdev reads {file}`requirements.txt`, {file}`constraints.txt` and {file}`mx.ini`, and writes new combined requirements in {file}`requirements-mxdev.txt` and writes new constraints in {file}`constraints-mxdev.txt` according to {file}`mx.ini`:

- 'version-overrides' in section [settings]
- checkout settings in [packagename] sections


````{admonition} checkout packages or define constraints
:class: margin

Summed up tasks and commands to checkout packages or define constraints:

Create

  - {file}`requirements.txt`
  - {file}`constraints.txt`
  - {file}`mx.ini`

  ```shell
  pip install mxdev
  mxdev -c mx.ini
  pip install -r requirements-mxdev.txt
  runwsgi instance/etc/zope.ini
  ```
````

So with the three files above, install and run `mxdev` with:

```shell
pip install mxdev
mxdev -c mx.ini
```

You are now ready to install your packages with `pip` and the new requirements file:

```shell
pip install -r requirements-mxdev.txt
```

Et voilà. Zope can be restarted:

```shell
runwsgi instance/etc/zope.ini
```

```{note}
You have seen how `mxdev` helps with versions and checkouts. It can do a lot more for you. See [mxdev](https://github.com/mxstack/mxdev) for more information.
```

You can now continue with chapter {ref}`install-source-create-plone-site-label`.
