---
myst:
  html_meta:
    "description": "make backend-build in Plone."
    "property=og:description": "make backend-build in Plone."
    "property=og:title": "make backend-build details"
    "keywords": "Plone 6, make, backend-build, install"
---

(make-backend-build-details-label)=

# `make backend-build` details

This chapter assumes you have previously followed {doc}`/install/create-project-cookieplone`.

The `Makefile` at the root of your project invokes commands in `backend/Makefile`.

The command `make backend-build`:

-   Invokes the target `install` in `backend/Makefile`.
-   `install` has the two dependencies `$(VENV_FOLDER)` and `config`.
-   `$(VENV_FOLDER)` creates and populates a virtual Python environment with `uv` from a `constraints.txt` file generated using `mxdev`.
-   `config`: Creates the Zope/Plone configuration files using `cookiecutter-zope-instance`.

You can configure your Zope instance as described in the section {doc}`/admin-guide/configure-zope`.
