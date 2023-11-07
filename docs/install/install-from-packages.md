---
myst:
  html_meta:
    "description": "How to install Plone 6 from its packages."
    "property=og:description": "How to install Plone 6 from its packages."
    "property=og:title": "Install Plone from its packages"
    "keywords": "Plone, Plone 6, install, pip, packages, source, cookiecutter"
---


(install-packages-1-label)=

# Install Plone from its packages
 
When you want full control over development or deployment, installing Plone from its packages is a good option.


(install-packages-system-requirements-label)=

## System requirements

Plone 6 has both hardware requirements and software pre-requisites.


(install-packages-hardware-requirements-label)=

### Hardware requirements

The hardware requirements below give a rough estimate of the minimum hardware setup needed for a Plone server.

A single Plone installation is able to run many Plone sites.

- Installation of the Plone backend and Classic UI frontend requires a minimum of 256 MB of RAM and 2GB of disk swap space.
- Installation of the Volto frontend requires a minimum of 2GB of RAM.
- After installation, running Plone requires a minimum of 256 MB RAM and 512 MB of disk swap space per Plone site.
    2 GB or more RAM per Plone site is recommended.
- Minimum 512 MB hard disk space is required.
    40 GB or more hard disk space is recommended.
- `Add-on` products and caching solutions may also increase RAM and disk swap space requirements.


(install-packages-prerequisites-label)=

### Pre-requisites for installation

-   An operating system that runs all the requirements mentioned above.
    Most UNIX-based operating systems are supported, including many Linux distributions, macOS, or {term}`Windows Subsystem for Linux` (WSL) on Windows.
    A UNIX-based operating system is recommended.

    ```{important}
    Windows alone is not recommended because it does not support {term}`GNU make`.
    If you get Plone to run on Windows alone, please feel free to document and share your process.
    ```

-   [Python](https://www.python.org/downloads/) 3.8, 3.9, 3.10 or 3.11 at the time of writing. Verify with the [Release notes](https://plone.org/download/releases/).
-   {pipx}`pipx`
-   {term}`Cookiecutter`
-   {term}`nvm`
-   {term}`Node.js` LTS
-   {term}`Yeoman`
-   {term}`Yarn`
-   {term}`GNU make`


(install-prerequisites-python-label)=

#### Python

Installing Python is beyond the scope of this documentation.
However, it is recommended to use a Python version manager, [`pyenv`](https://github.com/pyenv/pyenv) that allows you to install multiple versions of Python on your development environment without destroying your system's Python.

Install {pipx}`pipx`.

```shell
pip install pipx
```

(install-prerequisites-cookiecutter-label)=

#### Cookiecutter

Installation and upgrade is done below in {ref}`install-packages-install-label`.


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

1.  Install or update the supported LTS version of Node.js.
    This command also activates that version.

    ```shell
    nvm install --lts
    ```

2.  Verify that the supported version of Node.js is activated.

    ```shell
    node -v
    ```


(install-prerequisites-yeoman-label)=

#### Yeoman

Install {term}`Yeoman`.

```shell
npm install -g yo
```


(install-prerequisites-yarn-label)=

#### Yarn 3

Install the latest Yarn 3 version (not the Classic 1.x one) using `npm`.

1.  Open a terminal and type:

    ```shell
    npm install yarn@3
    ```

2.  Verify that Yarn v3.x.x is installed and activated.

    ```shell
    yarn -v
    ```
    ```console
    3.2.3
    ```
    
    If you do not see a version of Yarn 3, then try the following to set the active version.
    
    ```shell
    yarn set version 3.x
    ```


(install-prerequisites-make-label)=

#### Make

{term}`Make` comes installed on most Linux distributions.
On macOS, you must first [install Xcode](https://developer.apple.com/xcode/resources/), then install its command line tools.
On Windows, it is strongly recommended to [Install Linux on Windows with WSL](https://learn.microsoft.com/en-us/windows/wsl/install), which will include `make`.

Finally, it is a good idea to update your system's version of `make`, because some distributions, especially macOS, have an outdated version.
Use your favorite search engine or trusted online resource for how to update `make`.


(install-packages-install-label)=

## Install Plone 6

We install Plone 6 with {term}`pip` or {term}`pipx`, {term}`Cookiecutter`, {term}`mxdev`, {term}`make`, and other developer tools.

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

Run `cookiecutter` to create a Plone project skeleton using the Cookiecutter {term}`cookiecutter-plone-starter` with the following command.
This also updates cookiecutter.

```shell
pipx run cookiecutter gh:collective/cookiecutter-plone-starter
```

You will be presented with a series of prompts.
You can accept the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.
For ease of documentation, we will use the default values.

```console
You've downloaded <path-to-cookiecutter>/cookiecutter-plone-starter before. Is it okay to delete and re-download it? [yes]: 
project_title [Project Title]: 
project_slug [project-title]: 
description [A new project using Plone 6.]: 
author [Plone Foundation]: 
email [collective@plone.org]: 
python_package_name [project_title]: 
plone_version [6.0.0]: 
volto_version [16.5.0]: 
volto_generator_version [6.2.0]: 
Select language_code:
1 - en
2 - de
3 - es
4 - pt-br
Choose from 1, 2, 3, 4 [1]: 
github_organization [collective]: 
Select container_registry:
1 - Docker Hub
2 - GitHub
Choose from 1, 2 [1]: 
================================================================================
Project Title generation
================================================================================
Running sanity checks
  - Python: ✓
  - Node: ✓
  - yo: ✓
  - Docker: ✓
  - git: ✓

Summary:
  - Plone version: 6.0.0
  - Volto version: 16.5.0
  - Volto Generator version: 6.2.0
  - Output folder: <path-to-project>/project-title

Frontend codebase:
 - Installing @plone/generator-volto@6.2.0
 - Generate frontend application with @plone/volto 16.5.0

Backend codebase
 - Format generated code in the backend
================================================================================

Project "Project Title" was generated

Now, code it, create a git repository, push to your organization.

Sorry for the convenience,
The Plone Community.

================================================================================
```

Change to your project directory {file}`project-title`.

```shell
cd project-title
```

Next we switch to using `make`.
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
At the start of the frontend installation part, you might see a prompt.

```console
Need to install the following packages:
  mrs-developer
Ok to proceed? (y)
``` 

Hit the {kbd}`Enter` key to proceed and install `mrs-developer`.

When the process completes successfully, it will exit with a message similar to the following.

```console
✨  Done in 98.97s.
```


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

Enjoy!
