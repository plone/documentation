---
myst:
  html_meta:
    "description": "Standardize project configuration in Plone with plone/meta"
    "property=og:description": "Standardize project configuration in Plone with plone/meta"
    "property=og:title": "Standardize project configuration in Plone with plone/meta"
    "keywords": "Plone 6, standardize, project, configuration, development, plone/meta"
---

# Standardize Python project configuration

This part of the documentation describes how to standardize Python project configuration in Plone.
It does not cover the following.

-   Volto or any other JavaScript-based project, which has its own ecosystem.
-   Monorepos, such as [Cookieplone](https://github.com/plone/cookieplone).
    Repositories must have a single Python package at the top level.
-   Project that support multiple versions of Plone in the same branch.

Plone consists of hundreds of projects.
To lessen the effort of configuring a new project in the Plone GitHub organization, and to keep these projects current with latest configuration practices, the Plone community agreed upon a trusted set of configuration items.
The Plone community manages these configuration items using the [`plone/meta`](https://github.com/plone/meta) project.

You can follow these practices in your own projects, or suggest new or alternative configuration items through the `plone/meta` repository, sharing them with the rest of the Plone community.


## `plone/meta` basic usage

`plone/meta` has a rich set of features.
This section describes the most common use cases.

```{seealso}
See a description of all of [`plone/meta`'s features](https://github.com/plone/meta/blob/main/config/README.md#quick-start).
```


### Setup

Clone `plone/meta` to any machine, then change your current working directory into `meta/config`, create a Python virtual environment, and install `plone/meta`'s requirements.

```shell
git clone https://github.com/plone/meta.git
cd meta/config
python3 -m venv venv
venv/bin/pip install -r requirements.txt
```


### `config-package.py` script

The {file}`config-package.py` Python script from `plone/meta` creates or overwrites configuration files for your project.
See a current list of [configuration files](https://github.com/plone/meta/blob/main/config/README.md#configuration-files) that it will create or overwrite.

This script has several [command line options](https://github.com/plone/meta/blob/main/config/README.md#cli-arguments) that you can use to override the default options.

When you run this script, it automatically goes through the following steps.

1.  It creates a new git branch from the current branch in your project.
1.  If the file {file}`.meta.toml` is not present in the project, then it creates this and the other new configuration files from `plone/meta`'s Jinja2 templates.
    Otherwise, it reads the file {file}`.meta.toml` for regenerating the configuration files.
1.  It writes the configuration files.
1.  It creates a change log entry.
1.  By default, it commits changes.
1.  It optionally adds packages, pushes commits, or runs tox from the configuration files. 

```{tip}
If you prefer to name the new git branch instead of letting the script name it using its default naming scheme, then either create a new branch `my-new-branch`, switch to it, and use the `--branch current` option, or do all that in one step with the `--branch my-new-branch` option.
```

```{tip}
If you prefer to review changes before committing them, then use the `--no-commit` option.
```

For help for the script, use the following command.

```shell
venv/bin/python config-package.py --help
```


### Generate configuration files

Now you can run the Python script {file}`config-package.py` to generate configuration files from Jinja2 template files to manage your project.

```shell
venv/bin/python config-package.py [OPTIONS] PATH/TO/PACKAGE
```


### Manage configuration files

For each of the configuration files, you should edit its [corresponding stanza](https://github.com/plone/meta/blob/main/config/README.md#applying-a-customized-configuration) in the file {file}`.meta.toml`.

```{warning}
Do not directly edit the configuration files that `plone/meta` manages.
Anytime someone runs the Python script {file}`config-package.py`, any changes made in these files will get clobbered.
```

Then run the Python script {file}`config-package.py` to regenerate configuration files from your project's {file}`.meta.toml`.

```shell
venv/bin/python config-package.py [OPTIONS] PATH/TO/PACKAGE
```
