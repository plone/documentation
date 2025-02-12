---
myst:
  html_meta:
    "description": "Install Plone with cookiecutter-plone-starter (deprecated)"
    "property=og:description": "Install Plone with cookiecutter-plone-starter (deprecated)"
    "property=og:title": "Install Plone with cookiecutter-plone-starter (deprecated)"
    "keywords": "Plone, Plone 6, Volto, create, project, install, cookiecutter"
---


(create-a-project-label)=

# Install Plone with `cookiecutter-plone-starter` (deprecated)

```{deprecated} Plone 6.1 and Volto 18
This method to install Plone is now deprecated.
It was the recommended way to start a new Plone project with Plone 6.0 and Volto 17 or earlier.
For other installation options, see {ref}`get-started-install-label`.
```

This chapter describes how you can create a web application using the {term}`cookiecutter-plone-starter` template.

This template creates a web application using Plone with the Volto frontend, along with tools for development and deployment.


(install-packages-system-requirements-label)=

## System requirements

Plone 6.0 has both hardware requirements and software prerequisites.


### Supported web browsers

```{include} /_inc/_install-browser-reqs-volto.md
```

```{include} /_inc/_install-browser-reqs-classic-ui.md
```


(install-packages-hardware-requirements-label)=

### Hardware requirements

```{include} /_inc/_hardware-requirements.md
```


(install-packages-prerequisites-label)=

### Prerequisites for installation

```{include} ../volto/_inc/_install-operating-system.md
```

-   Python {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}
-   {term}`pipx`
-   {term}`nvm`
-   {term}`Node.js` LTS 20.x
-   {term}`Yeoman`
-   {term}`Yarn`
-   {term}`GNU make`
-   {term}`Docker`
-   {term}`Git`


(install-prerequisites-python-label)=

#### Python

```{include} /_inc/_install-python-plone60.md
```


(install-prerequisites-pipx-label)=

#### pipx

```{include} /_inc/_install-pipx.md
```


(install-prerequisites-nvm-label)=

#### nvm

```{include} ../volto/_inc/_install-nvm.md
```


(install-prerequisites-nodejs-label)=

#### Node.js

```{include} ../volto/_inc/_install-nodejs.md
```


(install-prerequisites-yeoman-label)=

#### Yeoman and the Volto boilerplate generator

Install {term}`Yeoman` and the Volto boilerplate generator.

```shell
npm install -g yo @plone/generator-volto
```


(install-prerequisites-yarn-label)=

#### Yarn

Use {term}`Corepack` to enable Yarn, which was already installed with the {ref}`supported version of Node.js <install-packages-prerequisites-label>`.

1.  Open a terminal and type:

    ```shell
    corepack enable
    ```

````{important}
The preceding instructions will not work if you have used another package manager, such as Homebrew on macOS, to install Yarn.
You can verify where you installed Yarn.

```shell
which yarn
# /opt/homebrew/bin/yarn
```

If the console includes `homebrew` in the path, then you must uninstall it.

```shell
brew uninstall yarn
```

Now the instructions to install Yarn should work.
````


(install-prerequisites-make-label)=

#### Make

```{include} ../volto/_inc/_install-make.md
```


(install-prerequisites-docker-label)=

#### Docker

```{include} ../volto/_inc/_install-docker.md
```


(install-prerequisites-git-label)=

#### Git

```{include} ../volto/_inc/_install-git.md
```


(install-packages-install-label)=

## Install Plone 6.0

We install Plone 6.0 with {term}`pipx`, {term}`Cookiecutter`, {term}`mxdev`, {term}`make`, and other developer tools.

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

```{tip}
See the cookiecutter's README for how to [Use options to avoid prompts](https://github.com/collective/cookiecutter-plone-starter/?tab=readme-ov-file#use-options-to-avoid-prompts).
```

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

```{include} /_inc/_install-pillow.md
```

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
