---
html_meta:
  "description": "How to set up the Plone Documentation locally"
  "property=og:description": "How to set up the Plone Documentation locally"
  "property=og:title": "Building and Checking the Quality of Documentation"
  "keywords": "setup, build, documentation, quality, development, spellcheck, linkcheck"
---

(setup-build-label)=

# Building and Checking the Quality of Documentation

This document covers how to build the Plone Documentation and check it for quality.


(setup-build-installation-label)=

## Installation

Install [Enchant](https://abiword.github.io/enchant/) to check spelling.

**macOS**

```shell
brew install enchant
```

**Ubuntu**

```shell
sudo apt-get install enchant
```

Clone the Plone Documentation repository, and change your working directory into the cloned project.
Then with a single command using `Makefile`, create a Python virtual environment, install project dependencies, pull in Volto documentation as a git submodule, build the docs, and view the results in a web browser by opening `/_build/html/index.html`.

```shell
git clone https://github.com/plone/documentation.git
cd documentation
make html
```

```{note}
If you are using an M1 Mac to build the documentation, there is currently an issue with pyenchant that throws an error that the enchant library can't be found. This happens for example if you installed your Python with pyenv. 
A workaround until pyenchant is fixed is to run `export PYENCHANT_LIBRARY_PATH=/opt/homebrew/lib/libenchant-2.dylib` in the terminal session before you execute `make html`.
in the terminal session before you execute `make html`.
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


### `spellcheck`

`spellcheck` checks the spelling of words.
See {ref}`authors-english-label` for configuration.

```shell
make spellcheck
```

Open `/_build/spellcheck/` for misspellings.


### `html_meta`

`html_meta` adds a meta data section to each chapter if missing.
See {ref}`authors-html-meta-data-label` for more info.

```shell
make html_meta
```
