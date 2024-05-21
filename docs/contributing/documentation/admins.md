---
myst:
  html_meta:
    "description": "Administrators' guide to writing Plone Documentation. It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation."
    "property=og:description": "Administrators' guide to writing Plone Documentation. It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation."
    "property=og:title": "Administrators Guide"
    "keywords": "Plone, Documentation, automated deployments, hosting, automated testing, importing external packages, preview, build, pull request"
---

(administrators-guide-label)=

# Administrators Guide

This guide is for administrators of Plone Documentation.
It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation.


(administrators-import-docs-and-converting-to-myst-label)=

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

Commit and push your changes to a remote, and submit a pull request against [`plone/documentation@6.0`](https://github.com/plone/documentation/compare).


## Pull request preview builds

To preview pull request builds of documentation or Storybooks on Read the Docs, you need to configure your project's repository and import it into Read the Docs.
You also need an account on Read the Docs and have write access to the repository.


### Configuration files

The following are example files that you can use to configure your project for pull request previews on Read the Docs.

-   [Plone Sphinx Theme `Makefile`](https://github.com/plone/plone-sphinx-theme/blob/main/Makefile), specifically the `rtd-pr-preview` section.
    This is the command to use to build documentation previews on Read the Docs.
-   [Plone Sphinx Theme `requirements-initial.txt`](https://github.com/plone/plone-sphinx-theme/blob/main/requirements-initial.txt) specifies the initial Python packaging tool requirements to set up a virtual environment.
-   [Plone Sphinx Theme `requirements-docs.txt`](https://github.com/plone/plone-sphinx-theme/blob/main/requirements-docs.txt) specifies the requirements to use Plone Sphinx Theme and build the docs.
-   [Plone Sphinx Theme `conf.py`](https://github.com/plone/plone-sphinx-theme/blob/main/docs/conf.py) the Sphinx configuration file to build the docs.
-   [Plone Sphinx Theme `.readthedocs.yaml`](https://github.com/plone/plone-sphinx-theme/blob/main/.readthedocs.yaml) specifies the configuration and command to build the docs.
-   [Plone Sphinx Theme `.github/workflows/rtd-pr-preview.yml`](https://github.com/plone/plone-sphinx-theme/blob/main/.github/workflows/rtd-pr-preview.yml) specifies when to build the docs, specifically only when a pull request is opened against the `main` branch and there are changes to documentation files.
    You might need to adjust the branch name, paths, and files to check for changes.


### Import your project

After logging in to your Read the Docs account, you can import your project.

1.  Click {guilabel}`Add project`.
1.  For {guilabel}`Repository name`, enter the GitHub organization, a forward slash, and the repository to import, for example, `plone/volto`.
1.  Click {guilabel}`Continue`.
1.  In the {guilabel}`Add project` screen, you can configure basic project settings, including its {guilabel}`Name`, {guilabel}`Repository URL`, {guilabel}`Default branch`, and {guilabel}`Language`.
    The defaults are usually accurate.
1.  Click {guilabel}`Next`.
1.  A sample `.readthedocs.yaml` file is suggested, if you have not already added one.
1.  Click {guilabel}`Finish`.
    Read the Docs will redirect you to the project details, and start building the docs.

For most Plone projects, you will not want to Read the Docs to publish the `latest` or other specific versions.
Plone projects currently self-host their official documentation.

1.  For the version that you want to deactivate, click its {guilabel}`…` icon, and select {guilabel}`Configure version`.
1.  Toggle the {guilabel}`Active` option off, and click {guilabel}`Update version`.
