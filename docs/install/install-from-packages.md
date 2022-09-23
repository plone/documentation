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

The hardware requirements below give a rough estimate of the minimum hardware setup needed for a Plone server.

Add-on products and caching solutions may increase RAM requirements.

A single Plone installation is able to run many Plone sites.
You may host multiple Plone sites on the same server.

-   Almost any modern operating system, including Linux, macOS, and Windows, but a UNIX-based operating system is recommended.
-   Minimum 256 MB RAM and 512 MB of swap space per Plone site is required.
    2 GB or more RAM per Plone site is recommended.
-   Minimum 512 MB hard disk space is required.
    40 GB or more hard disk space is recommended.


(install-packages-prerequisites-label)=

### Pre-requisites for installation

-   Python 3.8, 3.9, or 3.10.
-   Cookiecutter
-   Node.JS
-   nvm
-   Yarn
-   ```{todo}
    List any system libraries, such as `make`, `Xcode`, and so on.
    ```

Installing Python is beyond the scope of this documentation.
However, it is recommended to use a Python version manager, [`pyenv`](https://github.com/pyenv/pyenv) that allows you to install multiple versions of Python on your development environment without destroying your system's Python.

Install or upgrade {term}`Cookiecutter` and {term}`mxdev` in your user's Python:

```shell
pip install --user --upgrade cookiecutter
```

{ref}`Install nvm and Node.js documentation <frontend-getting-started-install-nvm-label>`.

{ref}`Install Yarn documentation <frontend-getting-started-yarn-label>`.


(install-packages-install-label)=

## Install Plone 6

We install Plone 6 with {term}`pip`, {term}`Cookiecutter`, {term}`make`, and other developer tools.

```{note}
We do not maintain documentation for installing Plone 6 or later with `buildout`.
For Plone 5, `buildout` was the preferred installation method.
You can read the [documentation of how to install Plone 5 with `buildout`](https://docs.plone.org/manage/installing/installation_minimal_buildout.html), and adapt it to your needs for Plone 6.
```

Create a new directory to hold your project, and make it your current directory.

```shell
mkdir my_project
cd my_project
```

Run `cookiecutter` to create a Plone project skeleton using the cookiecutter {term}`cookiecutter-plone-starter` with the following command.

````{todo}
When the feature branch is merged, the following command should be replaced with:

```
cookiecutter https://github.com/collective/cookiecutter-plone-starter/
```
````

```shell
cookiecutter https://github.com/collective/cookiecutter-plone-starter.git --checkout feature-4
```

You will be presented with a series of prompts.
You can accept the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.
For ease of documentation, we will use the default values.

```console
You've downloaded /<path-to-cookiecutter>/cookiecutter-plone-starter before.
  Is it okay to delete and re-download it? [yes]: 
project_title [Project Title]: 
project_slug [project-title]: 
description [A new project using Plone 6.]: 
author [Plone Foundation]: 
email [collective@plone.org]: 
python_package_name [project_title]: 
plone_version [6.0.0b2]: 
volto_version [16.0.0-alpha.35]: 
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
  - Plone version: 6.0.0b2
  - Volto version: 16.0.0-alpha.35
  - Output folder: /Users/stevepiercy/projects/Plone/documentation/ainstall/project-title

Frontend codebase:
 - Install latest @plone/generator-volto
 - Generate frontend application with @plone/volto 16.0.0-alpha.35

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
Starting application
2022-09-18 23:14:27,119 INFO    [chameleon.config:38][MainThread] directory cache: /path-to/my_project/project-title/backend/instance/var/cache.
2022-09-18 23:14:30,812 INFO    [plone.volto:22][MainThread] Aliasing collective.folderish classes to plone.volto classes.
2022-09-18 23:14:31,889 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 53838.
2022-09-18 23:14:31,893 INFO    [waitress:486][MainThread] Serving on http://[::1]:8080
2022-09-18 23:14:31,893 INFO    [waitress:486][MainThread] Serving on http://127.0.0.1:8080
```

At this point, you could visit the Plone Classic UI interface at the URL http://localhost:8080.
However it is strongly recommended to use the new Plone frontend, Volto, to gain many advantages, including easier content editing and development of components.
Continue to the next section to do so.


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
yarn run v1.22.19
$ razzle start
 WAIT  Compiling...


✔ Client
  Compiled successfully in 864.83ms

✔ Server
  Compiled successfully in 9.62s

✅  Server-side HMR Enabled!
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

You can stop the site with {kbd}`ctrl-esc`.

Enjoy!
