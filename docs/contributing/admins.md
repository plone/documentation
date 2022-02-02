---
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

To make it easier for other contributors to work with your project, update the following files, using `volto` as a model.
 
-   `Makefile` targets  `docs/my_package` and `deps`
-   The documentation section {ref}`contributing-editing-volto-documentation-label`

Commit and push your changes to a remote, and submit a pull request against [`plone/documentation@6-dev`](https://github.com/plone/documentation/compare).
