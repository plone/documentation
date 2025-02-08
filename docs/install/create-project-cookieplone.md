---
myst:
  html_meta:
    "description": "Install Plone with Cookieplone"
    "property=og:description": "Install Plone with Cookieplone"
    "property=og:title": "Install Plone with Cookieplone"
    "keywords": "Plone, Plone 6, Volto, create, project, install, Cookieplone"
---


(install-cookieplone-label)=

# Install Plone with Cookieplone

This chapter describes how you can create a web application using the {term}`Cookieplone` template.

This template is the recommended way to start a new Plone project using the Volto frontend.
It also includes tools for development and deployment.

```{seealso}
For other installation options, see {ref}`get-started-install-label`.
```

```{versionadded} Volto 18.0.0-alpha.43
{term}`Cookieplone` was added as the recommended template to create a Plone project with Volto starting in Volto 18.0.0-alpha.43 and above.
```


(create-project-cookieplone-system-requirements)=

## System requirements

Plone 6 has both hardware requirements and software prerequisites.


### Supported web browsers

```{include} /_inc/_install-browser-reqs-volto.md
```


(create-project-cookieplone-hardware-requirements-label)=

### Hardware requirements

```{include} /_inc/_hardware-requirements.md
```


(create-project-cookieplone-prerequisites-for-installation-label)=

### Prerequisites for installation

```{include} ../volto/_inc/_install-operating-system.md
```

-   Python {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}
-   {term}`pipx`
-   {term}`nvm`
-   {term}`Node.js` LTS 20.x
-   {term}`GNU make`
-   {term}`Git`


#### Python

```{include} /_inc/_install-python-plone61.md
```

Plone 6.1 requires Python version {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}.

```{warning}
Python 3.9 will reach [end of life in October 2025](https://devguide.python.org/versions/).
Do not create a new Plone project with Python 3.9.
```


#### pipx

```{include} /_inc/_install-pipx.md
```


#### nvm

```{include} ../volto/_inc/_install-nvm.md
```


#### Node.js

```{include} ../volto/_inc/_install-nodejs.md
```

3.  Enable {term}`corepack` so that Node.js will install {term}`pnpm` as a package manager.

    ```shell
    corepack enable
    ```


#### Make

```{include} ../volto/_inc/_install-make.md
```


#### Git

```{include} ../volto/_inc/_install-git.md
```


(create-project-cookieplone-generate-the-project-label)=

## Generate the project

After satisfying the prerequisites and having activated an LTS version of Node,
generate the project.

```shell
pipx run cookieplone project
```

You will be presented with a series of prompts.
You can accept the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.
For ease of documentation, we will use the default values.

```{tip}
See the cookiecutter's README for how to [Use options to avoid prompts](https://github.com/plone/cookieplone/?tab=readme-ov-file#use-options-to-avoid-prompts).
```

```{important}
For {guilabel}`Project Slug`, you must not use any of the Plone core package names listed in [`constraints.txt`](https://dist.plone.org/release/6-latest/constraints.txt).
Note that pip normalizes these names, so `plone.volto` and `plone-volto` are the same package.
```

```console
╭──────────────────────────────── cookieplone ────────────────────────────────╮
│                                                                             │
│                              .xxxxxxxxxxxxxx.                               │
│                          ;xxxxxxxxxxxxxxxxxxxxxx;                           │
│                       ;xxxxxxxxxxxxxxxxxxxxxxxxxxxx;                        │
│                     xxxxxxxxxx              xxxxxxxxxx                      │
│                   xxxxxxxx.                    .xxxxxxxx                    │
│                  xxxxxxx      xxxxxxx:            xxxxxxx                   │
│                :xxxxxx       xxxxxxxxxx             xxxxxx:                 │
│               :xxxxx+       xxxxxxxxxxx              +xxxxx:                │
│              .xxxxx.        :xxxxxxxxxx               .xxxxx.               │
│              xxxxx+          ;xxxxxxxx                 +xxxxx               │
│              xxxxx              +xx.                    xxxxx.              │
│             xxxxx:                      .xxxxxxxx       :xxxxx              │
│             xxxxx                      .xxxxxxxxxx       xxxxx              │
│             xxxxx                      xxxxxxxxxxx       xxxxx              │
│             xxxxx                      .xxxxxxxxxx       xxxxx              │
│             xxxxx:                      .xxxxxxxx       :xxxxx              │
│             .xxxxx              ;xx.       ...          xxxxx.              │
│              xxxxx+          :xxxxxxxx                 +xxxxx               │
│              .xxxxx.        :xxxxxxxxxx               .xxxxx.               │
│               :xxxxx+       xxxxxxxxxxx              ;xxxxx:                │
│                :xxxxxx       xxxxxxxxxx             xxxxxx:                 │
│                  xxxxxxx      xxxxxxx;            xxxxxxx                   │
│                   xxxxxxxx.                    .xxxxxxxx                    │
│                     xxxxxxxxxx              xxxxxxxxxx                      │
│                       ;xxxxxxxxxxxxxxxxxxxxxxxxxxxx+                        │
│                          ;xxxxxxxxxxxxxxxxxxxxxx;                           │
│                              .xxxxxxxxxxxxxx.                               │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯
You've downloaded /Users/stevepiercy/.cookiecutters/cookieplone-templates 
before. Is it okay to delete and re-download it? [y/n] (y): 
╭─────────────────────────────── Plone Project ───────────────────────────────╮
│                                                                             │
│ Creating a new Plone Project                                                │
│                                                                             │
│ Sanity check results:                                                       │
│                                                                             │
│   - Cookieplone: ✓                                                          │
│   - Python: ✓                                                               │
│   - Node: ✓                                                                 │
│   - git: ✓                                                                  │
│   - Docker (optional): ✓                                                    │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯
  [1/17] Project Title (Project Title): 
  [2/17] Project Description (A new project using Plone 6.): 
  [3/17] Project Slug (Used for repository id) (project-title): 
  [4/17] Project URL (without protocol) (project-title.example.com): 
  [5/17] Author (Plone Foundation): 
  [6/17] Author E-mail (collective@plone.org): 
  [7/17] Should we use prerelease versions? (No): 
  [8/17] Plone Version (6.1.0): 
  [9/17] Volto Version (18.8.1): 
  [10/17] Python Package Name (project.title): 
  [11/17] Volto Addon Name (volto-project-title): 
  [12/17] Language
    1 - English
    2 - Deutsch
    3 - Español
    4 - Português (Brasil)
    5 - Nederlands
    6 - Suomi
    Choose from [1/2/3/4/5/6] (1): 
  [13/17] GitHub or GitLab Username or Organization (collective): 
  [14/17] Container Registry
    1 - GitHub Container Registry
    2 - Docker Hub
    3 - GitLab
    Choose from [1/2/3] (1): 
  [15/17] Should we setup a caching server?
    1 - Yes
    2 - No
    Choose from [1/2] (1): 
  [16/17] Add Ansible playbooks?
    1 - Yes
    2 - No
    Choose from [1/2] (1): 
  [17/17] Add GitHub Action to Deploy this project?
    1 - Yes
    2 - No
    Choose from [1/2] (1): 
╭───────────────────────── Project Title generation ──────────────────────────╮
│                                                                             │
│ Summary:                                                                    │
│                                                                             │
│   - Plone version: 6.1.0                                                    │
│   - Volto version: 18.8.1                                                   │
│   - Output folder: <PATH_TO>/project-title                                  │
│                                                                             │
│                                                                             │
╰─────────────────────────────────────────────────────────────────────────────╯
 -> Initialize Git repository
 -> Setup Backend
 -> Setup Frontend
 -> Setup Cache
 -> Setup Project Settings
╭───────────────────────── New project was generated ─────────────────────────╮
│                                                                             │
│ Project Title                                                               │
│                                                                             │
│ Now, code it, create a git repository, push to your organization.           │
│                                                                             │
│ Sorry for the convenience,                                                  │
│ The Plone Community.                                                        │
│                                                                             │
│ https://plone.org/                                                          │
╰─────────────────────────────────────────────────────────────────────────────╯
```

## Install the project

To work on your project, you need to install both the frontend and backend.

Change your current working directory to {file}`project-title`.

```shell
cd project-title
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


## Start Plone

Plone 6 has two servers: one for the frontend, and one for the backend.
As such, we need to maintain two active shell sessions, one for each server, to start your Plone site.


### Start Plone backend

In the currently open session, issue the following command.

```shell
make backend-start
```

The Plone backend server starts up and emits messages to the console.

```console
2024-09-25 16:47:15,699 INFO    [chameleon.config:39][MainThread] directory cache: /<path-to-project>/backend/instance/var/cache.
2024-09-25 16:47:16,387 WARNING [ZODB.FileStorage:412][MainThread] Ignoring index for /<path-to-project>/backend/instance/var/filestorage/Data.fs
2024-09-25 16:47:16,508 INFO    [plone.restapi.patches:16][MainThread] PATCH: Disabled ZPublisher.HTTPRequest.ZopeFieldStorage.VALUE_LIMIT. This enables file uploads larger than 1MB.
2024-09-25 16:47:17,018 INFO    [plone.volto:23][MainThread] Aliasing collective.folderish classes to plone.volto classes.
2024-09-25 16:47:17,760 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 20912.
2024-09-25 16:47:17,772 INFO    [waitress:486][MainThread] Serving on http://[::1]:8080
2024-09-25 16:47:17,772 INFO    [waitress:486][MainThread] Serving on http://127.0.0.1:8080
```


### Start Plone frontend

Create a second shell session in a new window.
Change your current working directory to {file}`project-title`.
Start the Plone frontend with the following command.

```shell
make frontend-start
```

The Plone frontend server starts up and emits messages to the console, and should end with the following.

```console
webpack 5.90.1 compiled successfully in 11004 ms
sswp> Handling Hot Module Reloading
Using volto.config.js in: /<path-to-project>/frontend/volto.config.js
✅  Server-side HMR Enabled!
Volto is running in SEAMLESS mode
Proxying API requests from http://localhost:3000/++api++ to http://localhost:8080/Plone
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
