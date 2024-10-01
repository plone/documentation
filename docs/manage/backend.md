---
myst:
  html_meta:
    "description": "Manage Plone backend"
    "property=og:description": "Manage Plone backend"
    "property=og:title": "Manage Plone backend"
    "keywords": "Plone 6, manage, backend, add-ons, packages, mxdev"
---

(manage-plone-backend-label)=

# Manage Plone backend

This part of the documentation describes how to perform common management tasks in the Plone backend.
This chapter assumes you have previously followed {doc}`/install/create-project`.


## Manage add-ons and packages

Plone uses `mxdev` to manage packages and constraints.

```{seealso}
For an explanation of why Plone uses `mxdev`, see {ref}`manage-backend-python-packages-label`.
```


(mxdev-usage-overview-label)=

### `mxdev` usage overview

The default set of files for `mxdev` is shown below.
They are located in the `backend` directory of your project.

{file}`requirements.txt`

```ini
-c constraints.txt
-e src/project_title

zope.testrunner

# Add required add-ons
# collective.easyform
```

{file}`constraints.txt`

```ini
-c https://dist.plone.org/release/{PLONE_BACKEND_PATCH_VERSION}/constraints.txt
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

You can edit these three files in your project as you need.
Then you can generate package requirements and constraints files, and then install those packages, with one command.

```shell
make build-backend
```

`make build-backend` invokes `mxdev`, which generates the files {file}`requirements-mxdev.txt` and {file}`constraints-mxdev.txt`.
It then invokes `pip` to install packages with the new requirements file.

To reload the packages, stop your Plone site with {kbd}`ctrl-c`, and start it with the following command.

```shell
make start-backend
```

```{seealso}
See the [documentation of `mxdev` in its README.md](https://github.com/mxstack/mxdev/blob/main/README.md) for complete information.
```


(manage-add-an-add-on)=

### Add an add-on

Add a line with the name of your add-on in `requirements.txt`.
This example uses [`collective.easyform`](https://pypi.org/project/collective.easyform/).

```
collective.easyform
```

Add it to {file}`instance.yaml` to let Zope know that this add-on should be loaded:

```yaml
default_context:
    zcml_package_includes: project_title, collective.easyform
```

Stop the backend with {kbd}`ctrl-c`.
Then apply your changes and start the backend.
You do not need to stop the frontend.

```shell
make build-backend
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.

Then click the {guilabel}`Install` button next to your add-on to complete installation of the add-on.

Some add-ons have configuration options.
To configure such add-ons, return to the {guilabel}`Site Setup` control panel.
At the bottom of the page, you should see the heading {guilabel}`Add-on Configuration`, and a control panel to configure the add-on that you just installed.


(manage-pin-the-version-of-an-add-on)=

### Pin the version of an add-on

Pin the version in {file}`constraints.txt`.

```
collective.easyform==3.1.0
```

Add the add-on to {file}`requirements.txt`:

```
collective.easyform
```

Add it to {file}`instance.yaml` to let Zope know that this add-on should be loaded:

```yaml
default_context:
    zcml_package_includes: project_title, collective.easyform
```

Stop the backend with {kbd}`ctrl-c`.
Then apply your changes and start the backend.

```shell
make build-backend
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.
An upgrade step might need to be performed in the Plone control panel.
Follow the upgrade information, if present.
Else click the {guilabel}`Install` button to complete installation of the add-on.


(manage-check-out-an-add-on)=

### Check out an add-on

Add the add-on in {file}`requirements.txt`:

```
collective.easyform
```

In {file}`mx.ini`, specify the information to check out the add-on:

```ini
[collective.easyform]
url=git@github.com:collective/collective.easyform.git
branch=dev-branch-name
extras=test
```

Add it to {file}`instance.yaml` to let Zope know that this add-on should be loaded:

```yaml
default_context:
    zcml_package_includes: project_title, collective.easyform
```

Stop the backend with {kbd}`ctrl-c`.
Then apply your changes and start the backend.

```shell
make build-backend
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.
An upgrade step might need to be performed in the Plone control panel.
Follow the upgrade information, if present.
Else click the {guilabel}`Install` button to complete installation of the add-on.


(manage-pin-the-version-of-a-plone-package-against-constraints-label)=

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

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.
An upgrade step might need to be performed in the Plone control panel.
Follow the upgrade information, if present.


(manage-checkout-a-plone-package-label)=

### Check out a Plone package

This section covers how to check out a Plone Core package for development.

Add the Plone package you want to check out in {file}`mx.ini`.

```ini
[plone.restapi]
url = git@github.com:plone/plone.restapi.git
branch = main
extras = test
```

Stop the backend with {kbd}`ctrl-c`.
Then apply your changes and start the backend.

```shell
make build-backend
make start-backend
```

In your web browser, and assuming you are currently logged in as `admin`, visit the URL http://localhost:8080/Plone/prefs_install_products_form.
An upgrade step might need to be performed in the Plone control panel.
Follow the upgrade information, if present.


(manage-build-and-start-your-instance-label)=

### Build and start your instance

Whenever you make changes to your backend configuration—for example, install an add-on, or override a Plone core package—then a build and restart is needed.
First stop your Zope instance/Plone site with {kbd}`ctrl-c`.
Then build and run the Plone backend.

```shell
make build-backend
make start-backend
```

In a web browser, visit http://localhost:8080/ to see that Plone is running.

Your instance is running in the foreground.

```{seealso}
For an explanation of the command `make build-backend`, see {doc}`/conceptual-guides/make-build-backend-walk-through`.
```