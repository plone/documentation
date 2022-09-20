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


(manage-installation-details-label)=

## Installation details

{term}`Cookiecutter` creates projects from project templates.
The cookiecutter [`cookiecutter-plone-starter`](https://github.com/collective/cookiecutter-plone-starter/) creates a Plone project that you can install using {term}`Make`.
It generates files for installing and configuring both the frontend and backend.
For the backend, it uses [`cookiecutter-zope-instance`](https://github.com/plone/cookiecutter-zope-instance) to generate configuration files for a Zope WSGI instance.


(manage-backend-installation-details-label)=

## Backend installation details

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
    The next section in this chapter, {ref}`manage-zope-configuration-with-cookiecutter-zope-instance-label`, covers this option.
2.  *Manual* configuration by editing {file}`site.zcml` and {file}`zope.conf`.
    This option is detailed in Zope's documentation in [Configuring and Running Zope](https://zope.readthedocs.io/en/latest/operation.html).
    

(manage-zope-configuration-with-cookiecutter-zope-instance-label)=

## Zope configuration with `cookiecutter-zope-instance`

You can configure your Zope instance's options, including the following.

-   persistent storage: blobs, direct filestorage, relational database, ZEO, and so on
-   ports
-   threads
-   cache
-   debugging and profiling for development

```{seealso}
For a complete list of features, usage, and options, read [`cookiecutter-zope-instance`'s `README.rst`](https://github.com/plone/cookiecutter-zope-instance#readme).
```

As an example of how to configure Zope, we will add the add-on `collective.easyform` to our Zope instance.

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
`pip` can install Python packages by specifying them in a requirements file.
In your Plone project directory, open and edit the file {file}`backend/requirements.txt` as indicated.

```{code-block} text
:emphasize-lines: 3

-r requirements/unreleased.txt
src/project_title
collective.easyform
```

```{seealso}
Documentation of Python [Requirements File Format](https://pip.pypa.io/en/stable/reference/requirements-file-format/).
```

```{todo}
There should be a new make target that does not require this dance of changing the working directory.
```

Then after specifying requirements, you can install them by changing your working directory to `backend`, and using the following command.

```shell
cd backend
bin/pip install -r requirements.txt
```

Next you can use `cookiecutter` to generate the Zope configuration files.

```shell
bin/cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
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

As we mentioned earlier in {ref}`manage-installation-details-label`, `cookiecutter-zope-instance` creates a directory {file}`instance` that contains your Zope and Plone instance configuration.
This directory also contains persistent storage objects. During {doc}`install-from-packages`, when we ran the command `make start-backend`, the `Makefile` target ran the following command.

```shell
runwsgi -v instance/etc/zope.ini
```

That command loaded that instance's configuration, and started the Zope instance and our Plone site.
However, if your site is still running in the backend shell session, the changes will not show up until you restart the Plone backend.
If needed, stop your Plone backend with {kbd}`ctrl-c`.
Then start the backend with the following command.

```shell
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

Then click the {guilabel}`Install` button to complete installation of `collective.easyform`.

Return to the {guilabel}`Site Setup` control panel.
At the bottom of the page, you should see the heading {guilabel}`Add-on Configuration`, and a panel {guilabel}`easyform` to configure the add-on that we just installed.

While visiting the home page, you can add a new `easyform` object.


(manage-develop-packages-with-mxdev-label)=

## Develop Plone backend packages with `mxdev`

This section describes how to develop packages for Plone backend with `mxdev`.

For developing add-ons for the Plone frontend, Volto, see {doc}`volto/addons/index`.


(manage-the-problem-with-pip-label)=

### The problem with pip

If you want to check out a Plone core package for development, or want to override the constraints of Plone, normally you would define constraints with a file {file}`constraints.txt` to tell `pip` to install a different version of a Plone package.

```
# constraints.txt with unresolvable version conflict
-c https://dist.plone.org/release/{PLONE_BACKEND_VERSION}/constraints.txt
plone.api>=2.0.0a3
```

Unfortunately `pip` does not allow overriding constraints this way. 
{term}`mxdev` solves this issue.


(manage-mxdev-to-the-rescue-label)=

### `mxdev` to the rescue!

`mxdev` resolves Plone constraints with your needs for version pinning or source checkouts.
It reads its configuration file {file}`mx.ini`, and your {file}`requirements.txt` and {file}`constraints.txt` files.
Then it fetches the requirements and constraints of Plone
Finally it writes new combined requirements in {file}`requirements-mxdev.txt` and new constraints in {file}`constraints-mxdev.txt`.
Together these two files contain the combined requirements and constraints, but modified according to the configuration in {file}`mx.ini`.
The generated files indicate from where the constraints were fetched, and comments are added when a modification was necessary.

`mxdev` does not run `pip` or install packages.
You must perform that step.


(manage-mxdev-example-files-label)=

### `mxdev` example files

A minimal example set of files for `mxdev` would look like the following.

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

With these three files in your project, install and run `mxdev` with the following commands.

```shell
pip install mxdev
mxdev -c mx.ini
```

`mxdev` generates the files {file}`requirements-mxdev.txt` and {file}`constraints-mxdev.txt`.
Now you can install your packages with `pip` and the new requirements file:

```shell
pip install -r requirements-mxdev.txt
```

Finally, to reload the packages, restart your Zope instance/Plone site with the following command.

```shell
runwsgi instance/etc/zope.ini
```

```{seealso}
This was a brief overview of how `mxdev` helps with versions and checkouts.
It can do a lot more.
See the [documentation of `mxdev` in its README.rst](https://github.com/mxstack/mxdev/blob/main/README.rst) for complete information.
```


(manage-common-management-tasks-label)=

## Common management tasks

This section provides examples of common management tasks.


(manage-add-an-add-on)=

### Add an add-on

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

### Pin the version of an add-on

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

### Check out an add-on

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

### Pin the version of a Plone package against constraints

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

### Check out a Plone package

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

### Build and start your instance

Build and run Plone with one command.

```shell
runwsgi instance/etc/zope.ini
```

In a web browser, visit http://localhost:8080/ to see that Plone is running.

Your instance is running in the foreground.
For a daemonized process, see the section {ref}`manage-backend-process-manager`.


(manage-backend-process-manager)=

### Process manager

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
