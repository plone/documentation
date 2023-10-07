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

## Importing external docs and converting to MyST

This section describes how to import external projects and convert their docs to MyST.
We did this for `plone.app.dexterity` and several other projects.

1.  Create a new branch using the name of the project.
1.  Install [rst-to-myst](https://pypi.org/project/rst-to-myst/).

    ```shell
    bin/pip install "rst-to-myst[sphinx]"
    ```

1.  Clone the project repository to the root of `plone/documentation`.
1.  Delete any non-documentation files from the clone.
1.  Move the documentation files and subfolders to the root of the clone, retaining the documentation structure.
1.  Convert the reStructuredText documentation files to MyST.
    The example commands below assume that there are files at the root of the clone and in one sub-level of nested directories.
    For deeper nesting, insert globbing syntax for each sub-level as `**/`

    ```shell
    bin/rst2myst convert -R project/*.rst
    bin/rst2myst convert -R project/**/*.rst
    ```

1.  Add HTML meta data to the converted files.

    ```shell
    cd project
    ../bin/python ../docs/addMetaData.py
    ```

1.  Optionally clean up any MyST syntax.
1.  Commit and push your branch to GitHub and create a pull request.


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
