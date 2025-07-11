---
myst:
  html_meta:
    "description": "How to set up, build, and check quality of Plone Documentation locally"
    "property=og:description": "How to set up, build, and check quality of Plone Documentation locally"
    "property=og:title": "Set up, build, and check the quality of documentation"
    "keywords": "setup, build, documentation, quality, development, Vale, spell, grammar, style, check, linkcheck"
---

(setup-build-label)=

# Set up, build, and check the quality of documentation

This document covers how to set up and build the Plone Documentation and check it for quality.


(setup-build-installation-label)=

## Installation

Installation of Plone 6 Documentation includes prerequisites and the repository itself.

```{include} ../../volto/_inc/_install-operating-system.md
```
-   {ref}`setup-build-installation-python-label` {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}
-   {ref}`setup-build-installation-gnu-make-label`
-   {ref}`setup-build-installation-graphviz-label`


(setup-build-installation-python-label)=

### Python

```{include} /_inc/_install-python-plone61.md
```

(setup-build-installation-gnu-make-label)=

### GNU make

```{include} ../../volto/_inc/_install-make.md
```


(setup-build-installation-graphviz-label)=

### Graphviz

Install [Graphviz](https://graphviz.org/download/) for graph visualization.

`````{tab-set}
````{tab-item} macOS
```shell
brew install graphviz
```
````

````{tab-item} Ubuntu
```shell
sudo apt-get install graphviz
```
````
`````


(setup-build-installation-clone-plone-documentation-label)=

### Clone `plone/documentation`

In a terminal session, clone the Plone Documentation repository, and change your working directory into the cloned project.
Then with a single `make` command, create a Python virtual environment, install project dependencies, pull in documentation from remote repositories as a git submodule, build the documentation, and preview the results in a web browser.

```shell
git clone https://github.com/plone/documentation.git
cd documentation
make livehtml
```

(setup-build-available-documentation-builds-label)=

## Available documentation builds

All build and check commands use the file `Makefile`.
To see descriptions of the builds and checks, use the following command.

```shell
make help
```

Else you can open the {file}`Makefile` file to see other build formats.

The following sections describe the most frequently used `make` commands while in the primary `documentation` folder.

All `make` commands that build documentation will

-   create a Python virtual environment,
-   install requirements,
-   initialize or update the `volto`, `plone.restapi`, and `plone.api` submodules, and
-   finally create symlinks to the source files.

````{tip}
If you want to build documentation for only one of the subprojects, navigate to the root of the project in the `/submodules` folder, then use any of the following commands, but with the prefix of `docs-`.

```shell
cd submodules/volto
make docs-livehtml
```
````


### `livehtml`

`livehtml` rebuilds documentation as you edit its files, with live reload in the browser.

```shell
make livehtml
```

The console will give you the URL to open in a web browser.
The URL may vary, according to its configuration in the repository's {file}`Makefile`.

```console
[sphinx-autobuild] Serving on http://127.0.0.1:8050
```


### `linkcheckbroken`

`linkcheckbroken` checks all links, returning a list of only broken links.
See {ref}`authors-linkcheck-label` for configuration.

```shell
make linkcheckbroken
```

Open `/_build/linkcheck/output.txt` for the entire list of links that were checked and their result.


### `vale`

`vale` checks for American English spelling, grammar, and syntax, and follows the Microsoft Writing Style Guide.
See {ref}`authors-english-label` for configuration.

```shell
make vale
```

See the output on the console for suggestions.


### `clean`

`clean` removes all builds and cached files of the documentation.
Use this command before a build to troubleshoot issues with edits not showing up and to ensure that cached files do not hide errors in the documentation.

```shell
make clean
```


### `distclean`

`distclean` cleans the documentation build directory, Python virtual environment, and symlinks.
Use this command when packages that you have installed in your virtual environment yield unexpected results.

```shell
make distclean
```
