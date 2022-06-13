---
html_meta:
  "description": "Install Plone 6 from source for the one who wants to look under the hood"
  "property=og:description": "Install Plone 6 from source for the one who wants to look under the hood"
  "property=og:title": "Install Plone 6 from source step by step"
  "keywords": "Plone 6, install, buildout, pip, mxdev, mxmake, cookiecutter, source, Zope"
---


(install-source-stepbystep-start-label)=

# Install Plone Backend from Source – Step by Step

For system requirements and Pre-requisites for the installation see {ref}`install-source-system-requirements-label`.

We install the Plone backend with `pip`, `cookiecutter-zope-instance`, `mxstack` and other fancy helpers.


(install-source-installation-steps-label)=

### Installation steps

```{admonition} Jump in!
:class: margin
Go to {ref}`install-source-installation-jump-label` if you want to develop and want to jump in with all steps prepared by an overall cookiecutter.
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

````{admonition} packages tree
:class: margin toggle
The Plone packages and dependencies are installed in trees.

% TODO Why in trees?

```
venv/lib/Python3.x/
site-packages/
┌── plone/
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
pip install Plone -c https://dist.plone.org/release/6.0.0a4/constraints.txt
```

````{admonition} mkwsgiinstance's minimal Zope configuration
:class: margin toggle
`mkwsgiinstance` creates a home with a minimal configuration for a Zope instance.
No blob storage, etc. is defined so far.

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
````

Create a Zope instance with the given username and password in the current directory.

(install-source-mkwsgiinstance)=

```shell
mkwsgiinstance -u admin:admin -d .
```

````{admonition} All commands so far
:class: margin

```shell
python3.9 -m venv venv
source venv/bin/activate
pip install -U pip wheel
pip install Plone -c https://dist.plone.org/release/6.0.0a4/constraints.txt
mkwsgiinstance -u admin:admin -d .
```
````

Start the Zope instance.

```shell
runwsgi ./etc/zope.ini
```

You can stop the instance later with {kbd}`ctrl-esc`.

% TODO How to start the Zope instance in background.

If you now open the browser with http://localhost:8080/, you see that you already can create a Plone instance.
Before doing this, we configure our Zope instance for blobs, configure add-ons, etc..
For the configuration, you have two options:
- manual configuration of site.zcml and zope.conf
- use of helper `cookiecutter-zope-instance`

(install-source-cookiecutter-zope-instance-label)=

#### Cookiecutter Zope instance

`Cookiecutter` creates projects from project templates. `cookiecutter-zope-instance` is such a template that allows to create a complete Zope configuration. Zope configuration means: blob storage, type of file storage (Zope style or relational database), ZEO, you name it.

Install cookiecutter:

```shell
pip install cookiecutter
```

You could now run `cookiecutter` to create a Zope instance sceleton with configuraton with the following command, which would prompt you for parameter values.

```shell
cookiecutter https://github.com/plone/cookiecutter-zope-instance
```

(install-source-cookiecutter-zope-instance-presets-label)=

Instead we prepare a file {file}`instance.yaml` with the parameters we want to set. 
A minimal example is (add options as needed):

```yaml
default_context:
    initial_user_name: 'admin'
    initial_user_password: 'admin'

    load_zcml:
        package_includes: ['my.awesome.addon']

    db_storage: direct
```

Find more [options of cookiecutter `cookiecutter-zope-instance`](https://github.com/plone/cookiecutter-zope-instance#options).

The file {file}`instance.yaml` allows to set some presets.
Add-ons are listed here, but need to be installed with pip.
The documented installation of add-ons with pip is achieved via a {file}`requirements.txt` file.
An add-on like for example `my.awesome.addon` is listed in\
`requirements.txt`:

```
my.awesome.addon
```

Install your requirements:

```shell
pip install -r requirements.txt
```

You have done two things so far: You installed your add-on packages and you have prepared an initializing file to roll out a Zope / Plone project, configured to load your installed add-on packages.

You are now ready to apply your cookiecutter:

```shell
cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
```

```{list-table} Cookiecutter options
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
runwsgi instance/etc/zope.ini
```

Head over to http://localhost:8080/ and see that Plone is running.
You could now create a Plone instance {ref}`install-source-create-plone-site-label` and enable the add-on `my.awesome.addon` in {guilabel}`Site Setup` [http://localhost:8080/Plone/prefs_install_products_form](http://localhost:8080/Plone/prefs_install_products_form).

If you want to run Plone with some add-ons, you are ready with the installation of the backend.\
If you decided to go with the Plone Classic UI this is also your frontend.\
If you decided to go with the Plone Volto frontend, then section {ref}`install-source-volto-frontend-label` shows your next steps.

If you want to develop a Plone package, then the subsequent section is for you.


(install-source-checkout-and-pin)=

#### Checkout or version pinning of a Plone package

If you want to checkout a Plone package (not add-on) for development or just want to override the constraints of Plone, then a first attempt would be to define constraints with a {file}`constraints.txt` to tell pip to install a different version of a Plone package.

```
# constraints.txt with unresolvable version conflict
-c https://dist.plone.org/release/6.0.0a4/constraints.txt
plone.api>=2.0.0a3
```

Unfortunatly pip does not allow this way of overwriting constraints. 

`mxdev` is made for assembling Plone constraints with your needs of version pinning or source checkouts.\
It reads your {file}`constraints.txt`, fetches the constraints of Plone and writes a {file}`constraints-mxdev.txt` which combines the constraints. Comments on which Plone constraint is modified asure the readability.
% TODO language: 'readability'?

mxdev operates on three files to tell pip which packages to install with which version.

{file}`requirements.txt`

```ini
-c constraints.txt

Plone

# List of add-ons that are needed.
collective.easyform
```

{file}`constraints.txt`

```ini
-c https://dist.plone.org/release/6.0.0a4/constraints.txt

# constraints of add-ons
collective.easyform==3.4.5
```

{file}`sources.ini`

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

A run of mxdev reads {file}`requirements.txt` and {file}`sources.ini`, and writes new combined requirements in {file}`constraints-mxdev.txt` and writes new constraints in {file}`constraints-mxdev.txt` according to {file}`source.ini`:

- 'version-overrides' in [settings]
- checkout settings in [packagename] sections


````{admonition} checkout packages or define constraints
:class: margin

Summed up tasks and commands to checkout packages or define constraints:

Create

  - {file}`requirements.txt`
  - {file}`constraints.txt`
  - {file}`sources.ini`

  ```shell
  pip install mxdev
  mxdev -c sources.ini
  pip install -r requirements-mxdev.txt
  runwsgi instance/etc/zope.ini
  ```
````

So with the three files above, run `mxdev` with:

```shell
mxdev -c sources.ini
```

You are now ready to install your packages with `pip` and the new constraints file:

```shell
pip install -r requirements-mxdev.txt
```

Et voilà. Zope can be restarted:

```shell
runwsgi instance/etc/zope.ini
```

```{note}
You have seen how `mxdev` helps with versions and checkouts. It can do a lot more for you. See {ref}`install-source-tools-label` for more information.
```

You can now continue with {ref}`install-source-create-plone-site-label`.


(install-source-tweak-backend-installation-label)=

### Tasks on your installation from source

Adding an add-on
: Add a line with the name of your add-on to `requirements.txt` and add it to {ref}`instance.yaml<install-source-cookiecutter-zope-instance-presets-label>`, then install with pip and apply cookiecutter:

  ```shell
  pip install -r requirements.txt
  cookiecutter -f --no-input --config-file instance.yaml https://github.com/plone/cookiecutter-zope-instance
  ```

version pinning / constraints
: A version can **not** be pinned in requirements.txt if the package is mentionend in the constraints of Plone.
  Any other package version could be pinned in requirements.txt. Instead see section {ref}`install-source-checkout-and-pin` for a clean and well documented set up of your Zope/Plone installation.
