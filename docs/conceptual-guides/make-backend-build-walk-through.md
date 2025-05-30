---
myst:
  html_meta:
    "description": "make backend-build in Plone."
    "property=og:description": "make backend-build in Plone."
    "property=og:title": "make backend-build"
    "keywords": "Plone 6, make, backend-build, install"
---

(make-backend-build-label)=

# `make backend-build`

This chapter assumes you have previously followed {doc}`/install/create-project-cookieplone`.

The `Makefile` at the root of your project invokes commands in `backend/Makefile`.

The command `make backend-build` performs the following tasks.

-   Invokes the target `install` in `backend/Makefile`.
-   `install` has the two dependencies `$(VENV_FOLDER)` and `config`.
-   `$(VENV_FOLDER)` creates and populates a virtual Python environment with uv from a {file}`constraints.txt` file generated using mxdev.
-   `config` creates the Zope and Plone configuration files using cookiecutter-zope-instance.

You can configure your Zope instance as described in the section {doc}`/admin-guide/configure-zope`.
