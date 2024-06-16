---
myst:
  html_meta:
    "description": "Contributing to Plone 6 Core"
    "property=og:description": "Contributing to Plone 6 Core"
    "property=og:title": "Contributing to Plone 6 Core"
    "keywords": "Plone, Plone Contributor Agreement, License, Code of Conduct"
---

# Contributing to Plone 6 core

This part describes the process of development in Plone core.
It's primarily a technical resource for setting up your development environment, fixing bugs, and writing Plone Improvement Proposals (PLIPs).

It expands upon {doc}`/contributing/index` and, where applicable, {doc}`/contributing/first-time`.

## Version support policy

If you are triaging or fixing bugs, keep in mind that Plone has a [version support policy](https://plone.org/download/release-schedule)

## Dependencies

```{include} ../../volto/contributing/install-operating-system.md
```

- {ref}`setup-build-installation-python-label` {SUPPORTED_PYTHON_VERSIONS}
- {ref}`setup-build-installation-gnu-make-label`
- [git](https://help.github.com/articles/set-up-git/)

The first step in fixing a bug is getting this [buildout](https://github.com/plone/buildout.coredev) running.
We recommend fixing the bug on the latest branch and then [backporting](http://en.wikipedia.org/wiki/Backporting) as necessary.
[GitHub](https://github.com/plone/buildout.coredev/) by default always points to the currently active branch.
Depending on the current development cycle there may exist a future branch.
I.e. at the moment 6.0 is the actively maintained stable branch and 6.1 is the future, currently unstable, active development branch.
More information on switching release branches is below.

To set up a plone 6 development environment:

```shell
cd ~/buildouts # or wherever you want to put things
git clone -b 6.1 https://github.com/plone/buildout.coredev ./plone6devel
cd ./plone6devel
./bootstrap.sh
```

If you run into issues in this process, please see {doc}`troubleshooting`.

This will run for a long time if it is your first pull (~20 mins).
Once that is done pulling down eggs,
you can start your new instance with::

```shell
./bin/instance fg
```

or as WSGI service with::

```shell
./bin/wsgi
```

The default username/password for a dev instance is **admin/admin**.

## Additional material

```{toctree}
:maxdepth: 1

package-dependencies
release
```
