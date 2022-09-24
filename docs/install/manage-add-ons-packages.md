---
myst:
  html_meta:
    "description": "Manage add-ons, packages, and processes"
    "property=og:description": "Manage add-ons, packages, and processes"
    "property=og:title": "Manage add-ons, packages, and processes"
    "keywords": "Plone 6, manage, backend, add-ons, packages, processes, cookiecutter, Zope"
---


(manage-add-ons-packages-and-processes-label)=

# Manage add-ons and packages

This chapter assumes you have previously {doc}`installed Plone from its packages <install-from-packages>`.
In this section, we discuss details of the installation process so that you can customize your Plone installation.
It also covers routine management tasks that a developer might perform.


(manage-installation-details-with-cookiecutter-label)=

## Installation details with Cookiecutter

{term}`Cookiecutter` creates projects from project templates.
The cookiecutter [`cookiecutter-plone-starter`](https://github.com/collective/cookiecutter-plone-starter/) creates a Plone project that you can install using {term}`Make`.
It generates files for installing and configuring both the frontend and backend.
For the backend, it uses [`cookiecutter-zope-instance`](https://github.com/plone/cookiecutter-zope-instance) to generate configuration files for a Zope WSGI instance.


(manage-configuration-with-cookiecutter-zope-instance-label)=

## Configuration with `cookiecutter-zope-instance`

You can configure your instance's options, including the following.

-   persistent storage: blobs, direct filestorage, relational database, ZEO, and so on
-   ports
-   threads
-   cache
-   debugging and profiling for development

```{seealso}
For a complete list of features, usage, and options, read [`cookiecutter-zope-instance`'s `README.rst`](https://github.com/plone/cookiecutter-zope-instance#readme).
```


(manage-plone-backend-packages-with-mxdev-label)=

## Manage Plone backend packages with `mxdev`

This section describes how to manage packages for the Plone backend with `mxdev`.

For developing add-ons for the Plone frontend, Volto, see {doc}`volto/addons/index`.


(manage-the-problem-with-pip-label)=

### The problem with `pip`

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

`mxdev` resolves Plone constraints according to your needs for version pinning or source checkouts.
It reads its configuration file {file}`mx.ini`, and your {file}`requirements.txt` and {file}`constraints.txt` files.
Then it fetches the requirements and constraints of Plone.
Finally, it writes new combined requirements in {file}`requirements-mxdev.txt` and new constraints in {file}`constraints-mxdev.txt`.
Together these two files contain the combined requirements and constraints, but modified according to the configuration in {file}`mx.ini`.
The generated files indicate from where the constraints were fetched, and comments are added when a modification was necessary.

`mxdev` does not run `pip` or install packages.
You must perform that step.


(manage-mxdev-example-files-label)=

### `mxdev` example files

A minimal example set of files for `mxdev` would look like the following.
{ref}`manage-common-management-tasks-label` customize your `Plone` instance.

{file}`requirements.txt`

```ini
-c constraints.txt
-e src/project_title

zope.testrunner

# Add required add-ons
collective.easyform
```

{file}`constraints.txt`

```ini
-c https://dist.plone.org/release/{PLONE_BACKEND_VERSION}/constraints.txt
```

{file}`mx.ini`

```ini
; This is a mxdev configuration file
; it can be used to override versions of packages already defined in the
; constraints files and to add new packages from VCS like git.
; to learn more about mxdev visit https://pypi.org/project/mxdev/

[settings]
; example how to override a package version
; version-overrides =
;     example.package==2.1.0a2

; example section to use packages from git
; [example.contenttype]
; url = https://github.com/collective/example.contenttype.git
; pushurl = git@github.com:collective/example.contenttype.git
; extras = test
; branch = feature-7
```

With these three files in your project, you can generate package requirements and constraints files, and then install those packages.

```shell
make build-backend
```

The `make` target invokes `mxdev`, which generates the files {file}`requirements-mxdev.txt` and {file}`constraints-mxdev.txt`.
It then invokes `pip` to install packages with the new requirements file.
Finally, to reload the packages, restart your Zope instance/Plone site with the following command.

```shell
make start-backend
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

Apply your changes and restart backend:

```shell
make build-backend
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

Then click the {guilabel}`Install` button to complete installation of `collective.easyform`.

Return to the {guilabel}`Site Setup` control panel.
At the bottom of the page, you should see the heading {guilabel}`Add-on Configuration`, and a panel {guilabel}`easyform` to configure the add-on that we just installed.

While visiting the home page, you can add a new `easyform` object.


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

Apply your changes and restart backend:

```shell
make build-backend
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

At the top of the page, you should see an upgrade information. Update your add-on.


(manage-backend-check-out-an-add-on)=

### Check out an add-on

Add the add-on to {file}`requirements.txt`:

```
collective.easyform
```

Check out with {file}`mx.ini`:

```ini
[collective.easyform]
url=git@github.com:collective/collective.easyform.git
branch=dev-branch-name
extras = test
```

Add it to {file}`instance.yml` to let Zope know that this add-on should be loaded:

```yaml
default_context:
  load_zcml:
      package_includes: ['collective.easyform']
```

Apply your changes and restart backend:

```shell
make build-backend
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

Then click the {guilabel}`Install` button to complete installation of `collective.easyform`.


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

Apply your changes and restart backend:

```shell
make build-backend
make start-backend
```

Depending on the package whose version you are overriding, an upgrade step needs to be done in Plone control panel.
In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.
Follow the upgrade information.
Not every Plone core package needs and provides upgrade steps.

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

Apply your changes and restart backend:

```shell
make build-backend
make start-backend
```

Depending on the package whose version you are overriding, an upgrade step needs to be done in Plone control panel.
In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.
Follow the upgrade information.
Not every Plone core package needs and provides upgrade steps.


(manage-backend-build-and-start-your-instance-label)=

### Build and start your instance

Build and run Plone backend.

```shell
make build-backend
make start-backend
```

In a web browser, visit http://localhost:8080/ to see that Plone is running.

Your instance is running in the foreground.


(manage-backend-installation-details-label)=

## Backend installation details

Inside your project, open `backend/Makefile`.

```makefile
bin/pip:
  @echo "$(GREEN)==> Setup Virtual Env$(RESET)"
  python -m venv .
  bin/pip install -U "pip" "wheel" "cookiecutter" "mxdev"

instance/etc/zope.ini:  bin/pip
  @echo "$(GREEN)==> Install Plone and create instance$(RESET)"
  bin/cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
  mkdir -p var/{filestorage,blobstorage,cache,log}

build-dev: instance/etc/zope.ini ## pip install Plone packages
  @echo "$(GREEN)==> Setup Build$(RESET)"
  bin/mxdev -c mx.ini
  bin/pip install -r requirements-mxdev.txt
```

/ `make build-backend`

-   Creates a `Python` virtual environment if one does not exist, then upgrades Python package management tools.
-   Creates or updates the Zope configuration from its `instance.yaml` file using `cookiecutter-zope-instance`.
-   Creates specified directories, if they do not exist.
-   Installs Plone core packages and add-ons according `mx.ini`, `requirements.txt` and `constraint.txt`

You can configure your Zope instance as described in section {ref}`manage-common-management-tasks-label`.


````{todo}
configuration frontend:

- add an add-on
- checkout an add-on for development with mrs.developer

Add info here or link to respective frontend chapter.
localhost:8050/volto/addons/index.html#configuring-a-volto-project-to-use-an-addon

run
```
make install-frontend
make start-frontend
```

not: `make build-frontend`. Unfortunatly `build` means different things in frontend and backend. `build frontend` means production build. `build backend` means: apply changed configuration.
````
