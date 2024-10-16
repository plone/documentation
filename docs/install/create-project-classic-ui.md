---
myst:
  html_meta:
    "description": "Create a Plone project with Classic UI (stable release)"
    "property=og:description": "Create a Plone project with Classic UI (stable release)"
    "property=og:title": "Create a Plone project with Classic UI (stable release)"
    "keywords": "Plone, Plone 6, Classic UI, create, project, install, cookiecutter, Cookieplone"
---


(create-a-project-classic-ui-label)=

# Create a project with Classic UI (stable release)

This chapter describes how you can create a web application using the current **stable release** version of Plone with **Classic UI** for the frontend, while having full control over its development and deployment.

```{seealso}
For other installation options, see {doc}`/install/index`.
```


## System requirements

Plone 6 has both hardware requirements and software prerequisites.


### Hardware requirements

```{include} /_inc/_hardware-requirements.md
```

### Prerequisites for installation

```{include} ../volto/contributing/install-operating-system.md
```

-   Python {SUPPORTED_PYTHON_VERSIONS}
-   {term}`pipx`
-   {term}`GNU make`
-   {term}`Git`


#### Python

```{include} /_inc/_install-python.md
```


#### pipx

Install {term}`pipx`.

```shell
pip install pipx
```


#### Make

```{include} ../volto/contributing/install-make.md
```


#### Git

```{include} ../volto/contributing/install-git.md
```


## Generate the project

After satisfying the prerequisites, generate the project.

```shell
pipx run cookieplone backend_addon
```

You will be presented with a series of prompts.
You can accept the default values in square brackets (`[default-option]`) by hitting the {kbd}`Enter` key, or enter your preferred values.
For ease of documentation, we will use the default values.

```{tip}
See the cookiecutter's README for how to [Use options to avoid prompts](https://github.com/collective/cookiecutter-plone-starter/?tab=readme-ov-file#use-options-to-avoid-prompts).
```

```{important}
For {guilabel}`Project Slug`, you must not use any of the Plone core package names listed in [`constraints.txt`](https://dist.plone.org/release/6.0-latest/constraints.txt).
Note that pip normalizes these names, so `plone.volto` and `plone-volto` are the same package.
```

```console
% pipx run cookieplone backend_addon
╭─────────────────────────────────── cookieplone ────────────────────────────────────╮
│                                                                                    │
│                                  .xxxxxxxxxxxxxx.                                  │
│                              ;xxxxxxxxxxxxxxxxxxxxxx;                              │
│                           ;xxxxxxxxxxxxxxxxxxxxxxxxxxxx;                           │
│                         xxxxxxxxxx              xxxxxxxxxx                         │
│                       xxxxxxxx.                    .xxxxxxxx                       │
│                      xxxxxxx      xxxxxxx:            xxxxxxx                      │
│                    :xxxxxx       xxxxxxxxxx             xxxxxx:                    │
│                   :xxxxx+       xxxxxxxxxxx              +xxxxx:                   │
│                  .xxxxx.        :xxxxxxxxxx               .xxxxx.                  │
│                  xxxxx+          ;xxxxxxxx                 +xxxxx                  │
│                  xxxxx              +xx.                    xxxxx.                 │
│                 xxxxx:                      .xxxxxxxx       :xxxxx                 │
│                 xxxxx                      .xxxxxxxxxx       xxxxx                 │
│                 xxxxx                      xxxxxxxxxxx       xxxxx                 │
│                 xxxxx                      .xxxxxxxxxx       xxxxx                 │
│                 xxxxx:                      .xxxxxxxx       :xxxxx                 │
│                 .xxxxx              ;xx.       ...          xxxxx.                 │
│                  xxxxx+          :xxxxxxxx                 +xxxxx                  │
│                  .xxxxx.        :xxxxxxxxxx               .xxxxx.                  │
│                   :xxxxx+       xxxxxxxxxxx              ;xxxxx:                   │
│                    :xxxxxx       xxxxxxxxxx             xxxxxx:                    │
│                      xxxxxxx      xxxxxxx;            xxxxxxx                      │
│                       xxxxxxxx.                    .xxxxxxxx                       │
│                         xxxxxxxxxx              xxxxxxxxxx                         │
│                           ;xxxxxxxxxxxxxxxxxxxxxxxxxxxx+                           │
│                              ;xxxxxxxxxxxxxxxxxxxxxx;                              │
│                                  .xxxxxxxxxxxxxx.                                  │
│                                                                                    │
╰────────────────────────────────────────────────────────────────────────────────────╯
╭─────────────────────────────────── Plone Addon ────────────────────────────────────╮
│ Creating a new Plone Addon                                                         │
╰────────────────────────────────────────────────────────────────────────────────────╯
  [1/7] Addon Title (Addon): 
  [2/7] A short description of your addon (A new addon for Plone): 
  [3/7] Author (Plone Community): 
  [4/7] Author E-mail (collective@plone.org): 
  [5/7] GitHub Username or Organization (collective): 
  [6/7] Python package name (collective.addon): 
  [7/7] Support headless Plone?
    1 - Yes
    2 - No
    Choose from [1/2] (1): 
 -> Initialize Git repository
╭───────────────────────────── New addon was generated ──────────────────────────────╮
│                                                                                    │
│ Addon                                                                              │
│                                                                                    │
│ Now, enter the repository run the code formatter with:                             │
│                                                                                    │
│ make format                                                                        │
│                                                                                    │
│ start coding, and push to your organization.                                       │
│                                                                                    │
│ Sorry for the convenience,                                                         │
│ The Plone Community.                                                               │
│                                                                                    │
│ https://plone.org/                                                                 │
╰────────────────────────────────────────────────────────────────────────────────────╯
```


## Install the project

Change to your project directory.

```shell
cd collective.addon
```

To install the project's dependencies, use the following command.

```shell
make install
```

This will take a few minutes.
☕️

When the process completes successfully, it will exit with no message.

```{include} /_inc/_install-pillow.md
```


## Start Plone

To start Plone, issue the following command.

```shell
make start
```

The Plone backend server starts up and emits messages to the console.

```console
2024-09-25 16:47:15,699 INFO    [chameleon.config:39][MainThread] directory cache: /<path-to-project>/instance/var/cache.
2024-09-25 16:47:16,387 WARNING [ZODB.FileStorage:412][MainThread] Ignoring index for /<path-to-project>/instance/var/filestorage/Data.fs
2024-09-25 16:47:16,508 INFO    [plone.restapi.patches:16][MainThread] PATCH: Disabled ZPublisher.HTTPRequest.ZopeFieldStorage.VALUE_LIMIT. This enables file uploads larger than 1MB.
2024-09-25 16:47:17,018 INFO    [plone.volto:23][MainThread] Aliasing collective.folderish classes to plone.volto classes.
2024-09-25 16:47:17,760 INFO    [Zope:42][MainThread] Ready to handle requests
Starting server in PID 20912.
2024-09-25 16:47:17,772 INFO    [waitress:486][MainThread] Serving on http://[::1]:8080
2024-09-25 16:47:17,772 INFO    [waitress:486][MainThread] Serving on http://127.0.0.1:8080
```

You can stop the site with {kbd}`ctrl-c`.


## Create Classic UI Plone site

While the Plone backend server is running, open a browser and visit the following URL.

http://localhost:8080

```{image} /_static/plone-classic-ui-landing-page.png
:class: figure
:alt: Plone Classic UI landing page
```

Click the button {guilabel}`Create Classic UI Plone site` to do exactly that.

Use the username and password of `admin` to authenticate.
You will be redirected to the Create a Plone site page.

```{image} /_static/plone-classic-ui-site-page.png
:class: figure
:alt: Plone Classic UI site page
```

Enter values for {guilabel}`Path identifier`, {guilabel}`Title`, {guilabel}`Language`, and {guilabel}`Default timezone`.
The default values are usually good.

Click the button {guilabel}`Create Plone site`.

You will be redirected to the Plone site you just created.
