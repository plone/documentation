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

This chapter describes how you can create a web application using {term}`Cookieplone`.
Cookieplone is the recommended way to create a Plone project.
It also includes tools for development and deployment.

```{seealso}
For other installation options, see {ref}`get-started-install-label`.
```

```{versionadded} Volto 18.0.0-alpha.43
{term}`Cookieplone` was added as the recommended tool to create a Plone project with the Volto frontend starting in Volto 18.0.0-alpha.43 and above.
Subsequently, support for the Classic UI frontend was added in https://github.com/plone/cookieplone-templates/pull/240.
```


(create-project-cookieplone-choose-a-user-interface)=

## Choose a user interface

With Cookieplone, you can create projects that use either {term}`Volto` or {term}`Classic UI` as a frontend.
It is a good idea to choose a Plone frontend, or user interface before creating a project.
You can read {doc}`/conceptual-guides/choose-user-interface` to help inform your choice between Volto and Classic UI.
You can also create one {term}`Volto` and one {term}`Classic UI` project to test both variants locally before making a final decision.


(create-project-cookieplone-system-requirements)=

## System requirements

Plone has both hardware requirements and software prerequisites.


(create-project-cookieplone-hardware-requirements-label)=

### Hardware requirements

```{include} /volto/_inc/_hardware-requirements.md
```


### Supported web browsers

```{include} /volto/_inc/_install-browser-reqs-volto.md
```

```{include} /_inc/_install-browser-reqs-classic-ui.md
```


(create-project-cookieplone-prerequisites-for-installation-label)=

### Prerequisites for installation

```{include} ../volto/_inc/_install-operating-system.md
```

-   {term}`uv`
-   {term}`nvm` (required only for Volto projects)
-   {term}`Node.js` (required only for Volto projects)
-   {term}`GNU make`
-   {term}`Git`


(prerequisites-for-installation-uv-label)=

#### uv

```{include} ../volto/_inc/_install-uv.md
```


(prerequisites-for-installation-nvm-label)=

#### nvm

nvm is required only for Volto projects and not for Classic UI projects.

```{include} ../volto/_inc/_install-nvm.md
```


(prerequisites-for-installation-nodejs-label)=

#### Node.js

Node.js is required only for Volto projects and not for Classic UI projects.

```{include} ../volto/_inc/_install-nodejs.md
```


(prerequisites-for-installation-make-label)=

#### Make

```{include} ../volto/_inc/_install-make.md
```


(prerequisites-for-installation-git-label)=

#### Git

```{include} ../volto/_inc/_install-git.md
```


(create-project-cookieplone-create-volto-project-label)=

## Create a Plone project

After satisfying the prerequisites, generate a Plone project.

```shell
uvx cookieplone project
```

You will be presented with a series of prompts.
You can accept the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.

For ease of documentation, we will use the default values and thus create a project using the Volto frontend. 

To create a project using the ClassicUI frontend instead answer `No` when asked `Use Volto as frontend (Yes/no)`.

```{tip}
See Cookieplone's README for how to [Use options to avoid prompts](https://github.com/plone/cookieplone/?tab=readme-ov-file#use-options-to-avoid-prompts).
```

```{important}
For {guilabel}`Project Slug`, you must not use any of the Plone core package names listed in [`constraints.txt`](https://dist.plone.org/release/6-latest/constraints.txt).
Note that pip normalizes these names, so `plone.volto` and `plone-volto` are the same package.
```

```console
╭──────────────────────────── cookieplone (2.0.0a3) ─────────────────────────────╮
│                                                                                │
│                                    *******                                     │
│                                ***************                                 │
│                              ***             ***                               │
│                            ***    ***          ***                             │
│                           ***    *****          ***                            │
│                          ***      ***            ***                           │
│                          ***               ***   ***                           │
│                          ***              *****  ***                           │
│                          ***      ***      ***   ***                           │
│                           ***    *****          ***                            │
│                            ***    ***          ***                             │
│                              ***             ***                               │
│                                ***************                                 │
│                                    *******                                     │
│                                                                                │
╰───────────────────── Made with ❤️ by the Plone Community ──────────────────────╯
```

```
  [1/20] Project Title (Project Title)
  [2/20] Project Description (A new project using Plone 6.):
  [3/20] Project Slug (Used for repository id) (project-title):
  [4/20] Project URL (without protocol) (project-title.example.com):
  [5/20] Author (Plone Foundation):
  [6/20] Author E-mail (collective@plone.org):
  [7/20] Python Package Name (project.title):
  [8/20] Should we use prerelease versions? (yes/No):
  [9/20] Plone Version (6.2.0):
```
The next questions will determine if you will create a Volto or ClassicUI project.  
```
  [10/20] Use Volto as frontend (Yes/no): 
```
These two questions are only asked if you choose to create a project using Volto:
```
  [11/20] Volto Version (19.1.0): 
  [12/20] Volto Addon Name (volto-project-title):
```
For the remaining questions again we choose the default answer.
```
  [13/20] Language
    1 - English
    2 - Deutsch
    3 - Español
    4 - Português (Brasil)
    5 - Nederlands
    6 - Suomi
    7 - Italiano
    8 - Svenska
    Choose from [1/2/3/4/5/6/7/8] (1):
  [14/20] GitHub or GitLab username or organization slug from URL (collective):
  [15/20] Container Registry
    1 - GitHub Container Registry
    2 - Docker Hub
    3 - GitLab
    Choose from [1/2/3] (1):
  [16/20] Which persistent storage to use in the deployment stack?
    1 - RelStorage with PostgreSQL (recommended)
    2 - ZEO with FileStorage
    3 - Local FileStorage, implies a single backend
    Choose from [1/2/3] (1):
  [17/20] Should we setup a caching server? (Yes/no)
  [18/20] Add Ansible playbooks? (Yes/no)
  [19/20] Add GitHub Action to Deploy this project? (Yes/no)
  [20/20] Would you like to add a documentation scaffold to your project? (Yes/no)

╭─ Review your answers ──────────────────────────────────────────────────────────╮
│                                                                                │
│   Container Registry                     GitHub Container Registry             │
│   Should we use prerelease versions?     No                                    │
│   Language                               English                               │
│   Python Package Name                    project.title                         │
│   Which persistent storage to use in     RelStorage with PostgreSQL            │
│   the deployment stack?                  (recommended)                         │
│   Author E-mail                          <your@email>                          │
│   GitHub or GitLab username or           collective                            │
│   organization slug from URL                                                   │
│   Project Title                          Project Title                         │
│   Use Volto as frontend?                 Yes                                   │
│   Add Ansible playbooks?                 Yes                                   │
│   Volto Addon Name                       volto-project-title                   │
│   Volto Version                          19.1.1                                │
│   Author                                 <Your Name>                           │
│   Should we setup a caching server?      Yes                                   │
│   Plone Version                          6.2.0                                 │
│   Project Description                    A new project using Plone 6.          │
│   Project URL (without protocol)         project-title.example.com             │
│   Project Slug (Used for repository      project-title                         │
│   id)                                                                          │
│   Add GitHub Action to Deploy this       Yes                                   │
│   project?                                                                     │
│   Would you like to add a                Yes                                   │
│   documentation scaffold to your                                               │
│   project?                                                                     │
│                                                                                │
╰────────────────────────────────────────────────────────────────────────────────╯
Proceed? [Y/n]:

 -> Setup Backend
 -> Setup Frontend
 -> Generate documentation scaffold
 -> Setup Cache
 -> Setup Project Settings
 -> Setup VSCode configuration
 -> Setup GitHub CI
 -> Ignoring (Remove unneeded documentation files)
 -> Ignoring (Remove unneeded cache files)
 -> Ignoring (Remove unneeded deploy files)
 -> Ignoring (Remove frontend files for Classic UI)
 -> Backend final cleanup
 -> Format backend code
  -> Format frontend code
 -> Ignoring (Remove Ansible files)
 -> Ignoring (Remove GitHub Actions deployment files)
 -> Organize documentation files
 -> Ignoring (Remove unneeded documentation files)
 -> Initialize Git repository
╭─────────────────────────── New project was generated ───────────────────────────╮
│                                                                                 │
│ Project Title                                                                   │
│                                                                                 │
│ Now, code it, create a git repository, push to your organization.               │
│                                                                                 │
│ Sorry for the convenience,                                                      │
│ The Plone Community.                                                            │
│                                                                                 │
│ https://plone.org/                                                              │
╰─────────────────────────────────────────────────────────────────────────────────╯
```


### Install the project

To work on your project, you need to install both the backend and frontend.

Change your current working directory to {file}`project-title`.

```shell
cd project-title
```

To install both the Plone backend and Volto as frontend, use the following command.

```shell
make install
```

This will take a few minutes if you run it for the first time.
☕️
First the backend, then Volto as the frontend will be installed.

When the process completes successfully, it will exit with no message.

```{include} /_inc/_install-pillow.md
```


### Start Plone backend and Volto frontend

Plone with Volto for its frontend has two servers: one each for the backend and frontend.
As such, we need to maintain two active shell sessions, one for each server, to start your Plone site.


#### Start Plone backend

In the currently open session, issue the following command.

```shell
make backend-start
```

The Plone backend server starts up and emits messages to the console similar to the following.

```console
2026-05-29 11:48:31,825 INFO    [chameleon.config:40][MainThread] directory cache: /Users/username/PATH_TO/project-title/backend/instance/var/cache.
2026-05-29 11:48:32,337 WARNING [ZODB.FileStorage:409][MainThread] Ignoring index for /Users/username/PATH_TO/project-title/backend/instance/var/filestorage/Data.fs
2026-05-29 11:48:32,475 INFO    [plone.restapi.patches:15][MainThread] PATCH: Disabled ZPublisher.HTTPRequest.ZopeFieldStorage.VALUE_LIMIT. This enables file uploads larger than 1MB.
2026-05-29 11:48:32,757 INFO    [plone.app.event:17][MainThread] icalendar has been set up to use pytz instead of zoneinfo.
2026-05-29 11:48:33,781 INFO    [plone.volto:22][MainThread] Aliasing collective.folderish classes to plone.volto classes.
2026-05-29 11:48:34,311 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 93865.
2026-05-29 11:48:34,315 INFO    [waitress:449][MainThread] Serving on http://[::1]:8080
2026-05-29 11:48:34,315 INFO    [waitress:449][MainThread] Serving on http://127.0.0.1:8080
```


#### Start Volto frontend

Create a second shell session in a new window.
Change your current working directory to {file}`project-title`.
Start the Volto frontend with the following command.

```shell
make frontend-start
```

The Volto frontend server starts up and emits messages to the console, and should end with output similar to the following.

```console
webpack 5.90.1 compiled successfully in 14898 ms
sswp> Handling Hot Module Reloading
✅  Server-side HMR Enabled!
API server (API_PATH) is set to: http://localhost:3000
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


(install-cookieplone-generate-classic-project-label)=

## Create a Classic UI project

This section describes how to install Plone by creating a project with Classic UI as the frontend.

To create a ClassicUI project run the same command as in the section {ref}`create-project-cookieplone-create-volto-project-label`.: 

```shell
uvx cookieplone project
```

Only when asked `Use Volto as frontend (Yes/no)` you answer `No`!

### Install the project

To work on your project, you need to install it.

Change your current working directory to {file}`project-title`.

```shell
cd project-title
```

To install Plone with Classic UI for the frontend, use the following command.

```shell
make install
```

This will take a few minutes.
☕️
When the process completes successfully, it will exit with no message.

```{include} /_inc/_install-pillow.md
```


### Start Plone

In the currently open session, issue the following command.

```shell
make backend-start
```

The Plone server starts up and emits messages to the console.

```console
🐎 This Python uses horse-with-no-namespace to make pkg_resources namespace packages compatible with PEP 420 namespace packages.
2025-05-30 00:31:48,278 INFO    [chameleon.config:39][MainThread] directory cache: <PATH_TO>/project-title/backend/instance/var/cache.
2025-05-30 00:31:48,991 WARNING [ZODB.FileStorage:409][MainThread] Ignoring index for <PATH_TO>/project-title/backend/instance/var/filestorage/Data.fs
2025-05-30 00:31:49,106 INFO    [plone.restapi.patches:16][MainThread] PATCH: Disabled ZPublisher.HTTPRequest.ZopeFieldStorage.VALUE_LIMIT. This enables file uploads larger than 1MB.
2025-05-30 00:31:49,443 INFO    [plone.app.event:18][MainThread] icalendar has been set up to use pytz instead of zoneinfo.
2025-05-30 00:31:50,363 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 35793.
2025-05-30 00:31:50,365 INFO    [waitress:449][MainThread] Serving on http://[::1]:8080
2025-05-30 00:31:50,366 INFO    [waitress:449][MainThread] Serving on http://127.0.0.1:8080
```

Open a browser at the following URL to visit your Plone site.

http://localhost:8080/Plone

You will see a page similar to the following.

```{image} /_static/plone-classic-ui-home-page.png
:alt: Plone Classic UI home page
:class: figure
```

Select the {guilabel}`Login` link to visit the login form, and enter the following credentials.

-   {guilabel}`Login name`: `admin`
-   {guilabel}`Password`: `admin`

```{image} /_static/plone-classic-ui-login-page.png
:alt: Plone Classic UI login page
:class: figure
```

Now you can edit content or configure your Plone site.

You can stop the site with {kbd}`ctrl-c`.
