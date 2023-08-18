---
myst:
  html_meta:
    "description": "How to set up the Plone Documentation locally"
    "property=og:description": "How to set up the Plone Documentation locally"
    "property=og:title": "Building and Checking the Quality of Documentation"
    "keywords": "setup, build, documentation, quality, development, Vale, spell, grammar, style, check, linkcheck"
---

(setup-build-label)=

# Building and checking the quality of documentation

This document covers how to build the Plone Documentation and check it for quality.


(setup-build-installation-label)=

## Installation

Installation of Plone 6 Documentation includes pre-requisites and the repository itself.


(setup-build-installation-python-label)=

### Python

Python 3.8 or later is required.
A more recent Python is preferred.
Use your system's package manager or [pyenv](https://github.com/pyenv/pyenv) to install an appropriate version of Python.


(setup-build-installation-vale-label)=

### Vale

Vale is a linter for narrative text.
It checks spelling, English grammar, and style guides.
Plone documentation uses a custom spelling dictionary, with accepted and rejected spellings in `styles/Vocab/Plone`.

Use your operating system's package manager to [install Vale](https://vale.sh/docs/vale-cli/installation/).

Vale also has [integrations](https://vale.sh/docs/integrations/guide/) with various IDEs.

-   [JetBrains](https://vale.sh/docs/integrations/jetbrains/)
-   [Vim](https://github.com/dense-analysis/ale)
-   [VS Code](https://github.com/errata-ai/vale-vscode)

Plone documentation uses a file located at the root of the repository, `.vale.ini`, to configure Vale.
This file allows overriding rules or changing their severity.

The Plone Documentation Team selected the [Microsoft Writing Style Guide](https://learn.microsoft.com/en-us/style-guide/welcome/) for its ease of use—especially for non-native English readers and writers—and attention to non-technical audiences. 

```{note}
More corrections to spellings and Vale's configuration are welcome by submitting a pull request.
This is an easy way to become a contributor to Plone.
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

Clone the Plone Documentation repository, and change your working directory into the cloned project.
Then with a single command using `Makefile`, create a Python virtual environment, install project dependencies, pull in Volto documentation as a git submodule, build the docs, and view the results in a web browser by opening `/_build/html/index.html`.

```shell
git clone https://github.com/plone/documentation.git
cd documentation
make html
```

(setup-build-available-documentation-builds-label)=

## Available documentation builds

All build and check documentation commands use the file `Makefile`.

To see the most frequently used builds, use the following command.

```shell
make help
```

Else you can open `Makefile` to see other build formats, including PDF.


### `html`

`html` is the HTML version of the documentation.

```shell
make html
```

Open `/_build/html/index.html` in a web browser.


### `livehtml`

`livehtml` rebuilds Sphinx documentation on changes, with live-reload in the browser.

```shell
make livehtml
```

Open http://0.0.0.0:8000/ in a web browser.


### `linkcheck`

`linkcheck` checks all links.
See {ref}`authors-linkcheck-label` for configuration.

```shell
make linkcheck
```

Open `/_build/linkcheck/output.txt` for a list of broken links.


### `vale`

`vale` checks for American English spelling, grammar, syntax, and the Microsoft Developer Style Guide.
See {ref}`authors-english-label` for configuration.

```shell
make vale
```

See the output on the console for suggestions.


### `html_meta`

`html_meta` adds a meta data section to each chapter if missing.
See {ref}`authors-html-meta-data-label` for more info.

```shell
make html_meta
```
