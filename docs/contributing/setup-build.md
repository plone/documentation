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

Clone the Plone Documentation repository, then create and activate a virtual environment, and install project dependencies.

```shell
git clone https://github.com/plone/documentation.git
cd documentation
python -m venv .
source bin/activate
pip install -r requirements.txt
```


(setup-build-available-documentation-builds-label)=

## Available documentation builds

All build and check documentation commands use the file `Makefile`.

To see all available builds:

```shell
make
```


### `html`

`html` is the long narrative version used for the online documentation and by the trainer.

```shell
make html
```

Open `/_build/html/index.html` in a web browser.


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

Open `/_build/spellcheck/` for each training's misspellings.


### `html_meta`

`html_meta` adds a meta data section to each chapter if missing.
See {ref}`authors-html-meta-data-label` for more info.

```shell
make html_meta
```
