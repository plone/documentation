---
myst:
  html_meta:
    "description": "Manage add-ons, packages, and processes"
    "property=og:description": "Manage add-ons, packages, and processes"
    "property=og:title": "Manage add-ons, packages, and processes"
    "keywords": "Plone 6, manage, backend, add-ons, packages, processes, cookiecutter, pm2, Zope"
---


(manage-add-ons-packages-and-processes-label)=

# Manage add-ons, packages, and processes

This chapter assumes you have previously {doc}`installed Plone from its packages <install-from-packages>`.
That documented process is a streamlined version.
In this section, we discuss details of the installation process, so that you can customize your Plone installation.
It also covers routine management tasks that a developer might perform.


(install-packages-installation-details-label)=

## Installation details

The cookiecutter [`cookiecutter-plone-starter`](https://github.com/collective/cookiecutter-plone-starter/) creates a project template.
Behind the scenes, it uses [`cookiecutter-zope-instance`](https://github.com/plone/cookiecutter-zope-instance) to configure a Zope WSGI instance.  

Inside your project, open `backend/Makefile`.
The `make` target `instance/etc/zope.ini` performs several tasks.

```makefile
bin/pip:
	@echo "$(GREEN)==> Setup Virtual Env$(RESET)"
	python3 -m venv .
	bin/pip install -U "pip" "wheel" "cookiecutter"

instance/etc/zope.ini:	bin/pip
	@echo "$(GREEN)==> Install Plone and create instance$(RESET)"
	bin/pip install Plone -c https://dist.plone.org/release/$(PLONE_VERSION)/constraints.txt
	bin/cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
	mkdir -p var/{filestorage,blobstorage,cache,log}
```

-   Creates a virtual environment if one does not exist, then upgrades Python package management tools.
-   Installs Plone using a given `constraints.txt` file for a specific version using `pip`.
-   Creates or updates the Zope configuration from its `instance.yaml` file using `cookiecutter-zope-instance`.
-   Creates specified directories, if they do not exist.

As you may surmise, you can configure your Zope instance.
You have two options for configuration.

1.  *Generate* configuration by using `cookiecutter-zope-instance`.
    This chapter covers this option.
2.  *Manual* configuration by editing {file}`site.zcml` and {file}`zope.conf`.
    This option is detailed in Zope's documentation in [Configuring and Running Zope](https://zope.readthedocs.io/en/latest/operation.html).
    

(install-packages-cookiecutter-zope-instance-label)=

## Zope configuration with `cookiecutter-zope-instance`

You can configure your Zope instance's options, including the following.

-   persistent storage: blobs, direct filestorage, relational database, ZEO
-   ports
-   threads
-   cache
-   debugging and profiling for development

```{seealso}
For a complete list of features, usage, and options, read [`cookiecutter-zope-instance`'s `README.rst`](https://github.com/plone/cookiecutter-zope-instance#readme).
```

As an example, we will add the add-on `collective.easyform` to our Zope instance.

Zope is configured through the file {file}`instance.yaml` in your project.
Modify the file as indicated.

```{code-block} yaml
:emphasize-lines: 6-9

default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'

    load_zcml:
        package_includes: [
            'project_title',
            'collective.easyform',
        ]

    db_storage: direct
```

Add-ons are listed here under the `package_includes` key to be loaded by `Zope`.
As Python packages, they also need to be installed with `pip`.
`pip` can install Python packages by specifying them in a {file}`requirements.txt` file, one line per package, such as the following.

```{code-block} text
:emphasize-lines: 3

-r requirements/unreleased.txt
src/project_title
collective.easyform
```

```{seealso}
Documentation of Python [Requirements File Format](https://pip.pypa.io/en/stable/reference/requirements-file-format/).
```

Then after specifying requirements, you can install them with the following command.

```shell
pip install -r requirements.txt
```

Finally, you are now ready to use `cookiecutter` to generate the Zope configuration files.

```shell
cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
```

Let's break down that command.

```{list-table} Table of Cookiecutter arguments
:header-rows: 1

* - Option
  - Effect
* - `-f`, `--overwrite-if-exists`
  - Overwrite the contents of the output directory if it already exists.
    Data in `var` stays untouched.
* - `--no-input`
  - Do not prompt for parameters and only use `cookiecutter.json` file content.
* - `--config-file instance.yaml`
  - User configuration file.
```

As we mentioned in {ref}`install-packages-installation-details-label`, `cookiecutter-zope-instance` creates a directory {file}`instance` that contains your Zope and Plone instance configuration.
This directory also contains persistent storage objects.

When we ran the command `make start-backend`, the `Makefile` target ran the following command to start the Zope instance.

```shell
runwsgi -v instance/etc/zope.ini
```





(manage-backend-add-an-add-on)=

## Add an add-on

Add a line with the name of your add-on to `requirements.txt`

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


(manage-backend-pin-the-version-of-an-add-on)=

## Pin the version of an add-on

Pin the version in {file}`constraints.txt`.

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


(manage-backend-check-out-an-add-on)=

## Check out an add-on

Add the add-on to {file}`requirements.txt`:

```
collective.bookmarks
```

Check out with {file}`mx.ini`:

```ini
[collective.bookmarks]
url=git@github.com:collective/collective.bookmarks.git
branch=master
extras = test
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



(manage-backend-pin-the-version-of-a-plone-package-against-constraints-label)=

## Pin the version of a Plone package against constraints

A version can **not** be pinned in `constraints.txt` when the package is mentioned in the constraints of Plone.
Any other package version could be pinned in `constraints.txt`.
 
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

```{seealso}
{ref}`install-source-checkout-and-pin`.
```


(manage-backend-checkout-a-plone-package-label)=

## Check out a Plone package

This section covers how to check out a Plone Core package for development.

Add the Plone package you want to check out in {file}`mx.ini`.

```ini
[plone.restapi]
url = git@github.com:plone/plone.restapi.git
branch = master
extras = test
```

Apply the changes and install the package with the modified version with the following.

```shell
mxdev -c mx.ini
pip install -r requirements-mxdev.txt
```

Restart Zope with the following command.

```shell
runwsgi instance/etc/zope.ini
```


(manage-backend-build-and-start-your-instance-label)=

## Build and start your instance

Build and run Plone with one command.

```shell
runwsgi instance/etc/zope.ini
```

In a web browser, visit http://localhost:8080/ to see that Plone is running.

Your instance is running in the foreground.
For a daemonized process, see the section {ref}`manage-backend-process-manager`.


(manage-backend-process-manager)=

## Process manager

You can run, stop, or restart your backend and frontend, and more, with one command.
{term}`pm2` is a daemon process manager, suitable for production environments.

Create an overall process configuration file {file}`pm2.config.js` in the root of your project:

```js
let apps = [
  {
    name: "plone_backend_tutorial",
    script: 'runwsgi instance/etc/zope.ini',
    cwd: 'backend'
  },
  {
    name: "plone_frontend_tutorial",
    script: 'yarn build && yarn start:prod',
    cwd: 'frontend'
  }
];
module.exports = { apps: apps };
```

Start these processes with the following command.

```shell
pm2 start pm2.config.js
```

See processes managed by `pm2` (running and not running) with the following command.

```shell
pm2 l
```

![List processes with 'pm2 l'](/_static/illustration/pm2.png)

Restart a named process with the following command.

```shell
pm2 start plone_backend_tutorial
```

Stop a named process with the following command.

```shell
pm2 stop plone_backend_tutorial
```
