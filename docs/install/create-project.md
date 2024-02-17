---
myst:
  html_meta:
    "description": "Create a Plone project"
    "property=og:description": "Create a Plone project"
    "property=og:title": "Create a Plone project"
    "keywords": "Plone, Plone 6, create, project, install, cookiecutter"
---


(create-a-project-label)=

# Create a project

This chapter describes how you can create a web application project using Plone, with full control over development and deployment.

If instead you want to contribute to a Plone package, see {doc}`/contributing/index`.


(install-packages-system-requirements-label)=

## System requirements

Plone 6 has both hardware requirements and software pre-requisites.


(install-packages-hardware-requirements-label)=

### Hardware requirements

The hardware requirements below give a rough estimate of the minimum hardware setup needed for a Plone server.

A single Plone installation is able to run many Plone sites.

-   Installation of the Plone backend and Classic UI frontend requires a minimum of 256 MB of RAM and 2GB of disk swap space.
-   Installation of the Volto frontend requires a minimum of 2GB of RAM.
-   After installation, running Plone requires a minimum of 256 MB RAM and 512 MB of disk swap space per Plone site.
    2 GB or more RAM per Plone site is recommended.
-   Minimum 512 MB hard disk space is required.
    40 GB or more hard disk space is recommended.


````{warning}
{term}`Add-on` products and caching solutions may also increase RAM and disk swap space requirements.
To avoid RAM and disk swap limitations, we recommend either temporarily resizing your remote machine to accommodate the build, or build your images locally and upload them to an image store, such as [Docker Hub](https://hub.docker.com/) or [GitHub Packages](https://github.com/features/packages).
```{seealso}
[How much RAM is required to build a Volto front end?](https://community.plone.org/t/how-much-ram-is-required-to-build-a-volto-front-end/17949) and [Dealing with heap exhaustion while building Volto 17 on limited-RAM host](https://community.plone.org/t/dealing-with-heap-exhaustion-while-building-volto-17-on-limited-ram-host/18078).
```
````


(install-packages-prerequisites-label)=

### Pre-requisites for installation

```{include} ../volto/contributing/install-operating-system.md
```

-   Python {SUPPORTED_PYTHON_VERSIONS}
-   {term}`pipx`
-   {term}`nvm`
-   {term}`Node.js` LTS 20.x
-   {term}`Yeoman`
-   {term}`Yarn`
-   {term}`git`
-   {term}`GNU make`
-   {term}`Docker`


(install-prerequisites-python-label)=

#### Python

Installing Python is beyond the scope of this documentation.
However, it is recommended to use a Python version manager, {term}`pyenv` that allows you to install multiple versions of Python on your development environment without destroying your system's Python.
Plone requires Python version {SUPPORTED_PYTHON_VERSIONS}.


(install-prerequisites-pipx-label)=

#### pipx

Install {term}`pipx`.

```shell
pip install pipx
```


(install-prerequisites-nvm-label)=

#### nvm

The following terminal session commands use `bash` for the shell.
Adapt them for your flavor of shell.

```{seealso}
See the [`nvm` install and update script documentation](https://github.com/nvm-sh/nvm#install--update-script).
For the `fish` shell, see [`nvm.fish`](https://github.com/jorgebucaran/nvm.fish).
```

1.  Create your shell profile, if it does not exist.

    ```shell
    touch ~/.bash_profile
    ```

2.  Download and run the `nvm` install and update script, and pipe it into `bash`.

    ```shell
    curl -o- https://raw.githubusercontent.com/creationix/nvm/v{NVM_VERSION}/install.sh | bash
    ```

3.  Source your profile.
    Alternatively close the session and open a new one.

    ```shell
    source ~/.bash_profile
    ```

4.  Verify that the `nvm` version is that which you just installed or updated:

    ```shell
    nvm --version
    ```


(install-prerequisites-nodejs-label)=

#### Node.js

```{include} ../volto/contributing/install-nodejs.md
```


(install-prerequisites-yeoman-label)=

#### Yeoman and the Volto boilerplate generator

Install {term}`Yeoman` and the Volto boilerplate generator

```shell
npm install -g yo @plone/generator-volto
```

(install-prerequisites-yarn-label)=

#### Yarn

1.  Open a terminal and type:

    ```shell
    corepack enable
    ```

From that moment on, `yarn` will be available for you to use in your system.
This is thanks that `yarn` is shipped with NodeJS since Node 16 (along with other common package managers).
The version shipped is v1 (classic `yarn`).
Volto makes sure that you are using the correct version of `yarn` at runtime.
This is because it's pinned in the Volto boilerplate to use the right version.
So from this moment on, you don't have to worry about the version of `yarn` you are using, it will adapt to the project's needs.

````important
These instructions will not work if you have used another package manager, such as Homebrew on macOS, to install Yarn.
You can verify where you installed Yarn and its version.
Make sure that you are using the yarn version provided by NodeJS by default
```shell
which yarn
```
```console
/opt/homebrew/bin/yarn
```
```shell
yarn -v
```
```console
3.2.3
```
If the console includes `homebrew` in the path, and the version of Yarn is not supported, then you must uninstall it.
```shell
brew uninstall yarn
```
Now the instructions should work.
````

(install-prerequisites-make-label)=

#### Make

```{include} ../volto/contributing/install-make.md
```


(install-prerequisites-docker-label)=

#### Install Docker

```{include} ../volto/contributing/install-docker.md
```


(install-packages-install-label)=

## Install Plone 6

We install Plone 6 with {term}`pipx`, {term}`Cookiecutter`, {term}`mxdev`, {term}`make`, and other developer tools.

```{note}
We do not maintain documentation for installing Plone 6 or later with `buildout`.
For Plone 5, `buildout` was the preferred installation method.
You can read the [documentation of how to install Plone 5 with `buildout`](https://5.docs.plone.org/manage/installing/installation_minimal_buildout.html), and adapt it to your needs for Plone 6.
```

Create a new directory to hold your project, and make it your current directory.

```shell
mkdir my_project
cd my_project
```

Issue the following command to install or update `cookiecutter`, then run it to create a Plone project skeleton using the Cookiecutter {term}`cookiecutter-plone-starter`.

```shell
pipx run cookiecutter gh:collective/cookiecutter-plone-starter
```

You will be presented with a series of prompts.
You can accept the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.
For ease of documentation, we will use the default values.

(avoid-plone-core-package-names)=

```{important}
For {guilabel}`Project Slug`, you must not use any of the Plone core package names listed in [`constraints.txt`](https://dist.plone.org/release/6.0-latest/constraints.txt).
Note that pip normalizes these names, so `plone.volto` and `plone-volto` are the same package.
```

```console
% pipx run cookiecutter gh:collective/cookiecutter-plone-starter


Cookiecutter Plone Starter
================================================================================

Sanity checks
--------------------------------------------------------------------------------
  [1/5] Python: ✓
  [2/5] Node: ✓
  [3/5] yo: ✓
  [4/5] Docker: ✓
  [5/5] git: ✓

Project details
--------------------------------------------------------------------------------

  [1/19] Project Title (Project Title): Plone Conference Website 2070
  [2/19] Project Description (A new project using Plone 6.):
  [3/19] Project Slug (Used for repository id) (plone-conference-website-2070):
  [4/19] Project URL (without protocol) (plone-conference-website-2070.example.com):
  [5/19] Author (Plone Foundation): Elli
  [6/19] Author E-mail (collective@plone.org): elli@plone.org
  [7/19] Python Package Name (plone_conference_website_2070):
  [8/19] Volto Addon Name (volto-plone-conference-website-2070):
  [9/19] Choose a Python Test Framework
    1 - pytest
    2 - unittest
    Choose from [1/2] (1):
  [10/19] Plone Version (6.0.8):
  [11/19] Should we use Volto Alpha Versions? (No): yes
  [12/19] Volto Version (18.0.0-alpha.1):
  [13/19] Volto Generator Version (8.0.0):
  [14/19] Language
    1 - English
    2 - Deutsch
    3 - Español
    4 - Português (Brasil)
    5 - Nederlands
    6 - Suomi
    Choose from [1/2/3/4/5/6] (1):
  [15/19] GitHub Username or Organization (collective): ellizurigo
  [16/19] Container Registry
    1 - GitHub Container Registry
    2 - Docker Hub
    Choose from [1/2] (1):
  [17/19] Should we setup a caching server?
    1 - Yes
    2 - No
    Choose from [1/2] (1): 2
  [18/19] Add Ansible playbooks?
    1 - Yes
    2 - No
    Choose from [1/2] (1):
  [19/19] Add GitHub Action to Deploy this project?
    1 - Yes
    2 - No
    Choose from [1/2] (1):

Plone Conference Website 2070 generation
--------------------------------------------------------------------------------

Summary:
  - Plone version: 6.0.8
  - Volto version: 18.0.0-alpha.1
  - Volto Generator version: 8.0.0
  - Output folder: /Users/katjasuss/Desktop/_temp/scratch_cookiecutter_plone/plone-conference-website-2070

Frontend codebase:
 - Installing required npm packages
 - Generate frontend application with @plone/volto 18.0.0-alpha.1

Backend codebase
 - Remove folder src/plone_conference_website_2070/src/plone_conference_website_2070/tests not used by pytest
 - Format generated code in the backend

================================================================================

Project "Plone Conference Website 2070" was generated
--------------------------------------------------------------------------------
Now, code it, create a git repository, push to your organization.

Sorry for the convenience,
The Plone Community.

================================================================================
```

Change to your project directory {file}`plone-conference-website-2070`.

```shell
cd plone-conference-website-2070
```

Next you switch to using `make`.
To see all available commands and their descriptions, enter the following command.

```shell
make help
```

To install both the Plone backend and frontend, use the following command.

```shell
make install
```

This will take a few minutes.
☕️
First the backend, then the frontend will be installed.

When the process completes successfully, it will exit with no message.

````{note}
If you used a Plone core package name, then `make install` will return an error message such as the following.

```console
ERROR: Cannot install plone-volto 1.0.0a1 (from /home/username/projects/volto/plone-volto/backend/src/plone_volto) because these package versions have conflicting dependencies.

The conflict is caused by:
    The user requested plone-volto 1.0.0a1 (from /home/username/projects/volto/plone-volto/backend/src/plone_volto)
    The user requested (constraint) plone-volto==4.2.0

To fix this you could try to:
1. loosen the range of package versions you've specified
2. remove package versions to allow pip attempt to solve the dependency conflict

ERROR: ResolutionImpossible: for help visit
make[2]: *** [Makefile:112: build-dev] Error 1
make[2]: Leaving directory '/home/username/projects/volto/plone-volto/backend'
make[1]: *** [Makefile:46: install-backend] Error 2
make[1]: Leaving directory '/home/username/projects/volto/plone-volto'
```

You must delete your project, {ref}`follow the important note <avoid-plone-core-package-names>`, and run the cookiecutter again.
````


(install-packages-start-plone-label)=

## Start Plone

Plone 6 has two servers: one for the frontend, and one for the backend.
As such, we need to maintain two active shell sessions, one for each server, to start your Plone site.


(install-packages-start-plone-backend-label)=

### Start Plone backend

In the currently open session, issue the following command.

```shell
make start-backend
```

The Plone backend server starts up and emits messages to the console.

```console
2022-09-24 01:30:17,799 WARNING [ZODB.FileStorage:411][MainThread] Ignoring index for /<path-to-project>/my_project/project-title/backend/instance/var/filestorage/Data.fs
2022-09-24 01:30:19,639 INFO    [chameleon.config:38][MainThread] directory cache: /<path-to-project>/my_project/project-title/backend/instance/var/cache.
2022-09-24 01:30:23,680 INFO    [plone.volto:22][MainThread] Aliasing collective.folderish classes to plone.volto classes.
2022-09-24 01:30:24,935 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 92714.
2022-09-24 01:30:24,940 INFO    [waitress:486][MainThread] Serving on http://[::1]:8080
2022-09-24 01:30:24,940 INFO    [waitress:486][MainThread] Serving on http://127.0.0.1:8080
```


(install-packages-start-plone-frontend-label)=

### Start Plone frontend

Create a second shell session in a new window.
Change your current working directory to {file}`project-title`.
Start the Plone frontend with the following command.

```shell
make start-frontend
```

The Plone frontend server starts up and emits messages to the console.

```console
 WAIT  Compiling...


✔ Client
  Compiled successfully in 864.83ms

✔ Server
  Compiled successfully in 9.62s

✅  Server-side HMR Enabled!
sswp> Handling Hot Module Reloading
Volto is running in SEAMLESS mode
Using internal proxy: http://localhost:3000 -> http://localhost:8080/Plone
🎭 Volto started at 0.0.0.0:3000 🚀
```

Note that the Plone frontend uses an internal proxy server to connect with the Plone backend.
Open a browser at the following URL to visit your Plone site.

http://localhost:3000

You will see a page similar to the following.

```{image} /_static/plone-home-page.png
:alt: Plone home page
:class: figure
```

Select the {guilabel}`Login` link to visit the login form, and enter the following credentials.

-   {guilabel}`Login name`: `admin`
-   {guilabel}`Password`: `admin`

```{image} /_static/plone-login-page.png
:alt: Plone login page
:class: figure
```

Now you can edit content or configure your Plone site.

You can stop the site with {kbd}`ctrl-c`.
