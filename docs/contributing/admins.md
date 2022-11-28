---
myst:
  html_meta:
    "description": "Administrators' guide to writing Plone Documentation. It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation."
    "property=og:description": "Administrators' guide to writing Plone Documentation. It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation."
    "property=og:title": "Administrators Guide"
    "keywords": "Plone, Documentation, automated deployments, hosting, automated testing, importing external packages"
---

(administrators-guide-label)=

# Administrators Guide

This guide is for administrators of Plone Documentation.
It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation.


(administrators-import-docs-submodule-label)=

## Importing external docs with submodules

To add an external package to Plone Documentation, we use git submodules.
We did this with Volto documentation.
Your package must be available under the Plone GitHub organization.

Inside the repository `plone/documentation`, add a git submodule that points to your project.

```shell
git submodule add git@github.com:plone/my_package.git submodules/my_package
```

Add a target `docs/my_package` in `Makefile`, then add `docs/my_package` to the `deps` target, following `volto` as a pattern.
You might need to adjust the paths to your package's documentation after it is cloned.

To complete setup, generate a symlink to your project's docs, and build the docs, use a single command.

```shell
make html
```

To make it easier for other contributors to work with your project, update the following files, using `volto` as a model.
 
-   Add it to the documentation section {ref}`contributing-editing-external-package-documentation-label`.
-   Add the symlink `docs/my_package` to `.gitignore`.
-   Optionally set a branch to work on in `.gitmodules`.

Commit and push your changes to a remote, and submit a pull request against [`plone/documentation@6-dev`](https://github.com/plone/documentation/compare).
