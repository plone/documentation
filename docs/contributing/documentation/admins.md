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
-   [Plone Sphinx Theme `requirements-dev.txt`](https://github.com/plone/plone-sphinx-theme/blob/main/requirements-docs.txt) specifies the requirements to use Plone Sphinx Theme and build the docs.
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


### Search engine indexing

Many Plone projects currently self-host their official documentation at {doc}`/index`.
These projects get indexed by search engines.

For pull request previews, unsupported branches or versions, or other situations, you most likely do not want search engines to index your documentation.
Your options include the following.

-   Deactivate your build
-   Hide your build
-   Create a custom {file}`robots.txt` file to discourage, but not absolutely prevent, search engine indexing

For the last option, you can configure Sphinx to copy the {file}`robots.txt` file.
However, if you want to have two versions of a {file}`robots.txt` file—say one that allows indexing of your official documentation and another that discourages indexing—you can configure your automation to copy it into place with a command such as the following.

```shell
cp source-path/block-robots.txt docs-root-path/robots.txt
```

```{seealso}
-   [Automation rules](https://docs.readthedocs.io/en/stable/automation-rules.html)
-   [Versions](https://docs.readthedocs.io/en/stable/versions.html)
-   [Managing versions automatically](https://docs.readthedocs.io/en/stable/guides/automation-rules.html)
-   [`robots.txt` support](https://docs.readthedocs.io/en/stable/reference/robots.html)
```


### Cancel builds programmatically

You might want to cancel a build programmatically when certain conditions are met.
You can do this through your {file}`.readthedocs.yaml` file.
Read the Docs covers a few scenarios in its documentation, [Cancel build based on a condition](https://docs.readthedocs.io/en/stable/build-customization.html#cancel-build-based-on-a-condition).


#### Build only on changes

When there are no changes to documentation, it is not necessary to build it.
You can save time and energy by programmatically building documentation only when it changes.

In your {file}`.readthedocs.yaml` file, you could use the following example.

```yaml
version: 2
build:
  os: "ubuntu-22.04"
  tools:
    python: "3.12"
  jobs:
    post_checkout:
      # Cancel building pull requests when there aren't changes in the docs directory or YAML file.
      # You can add any other files or directories that you'd like here as well,
      # like your docs requirements file, or other files that will change your docs build.
      #
      # If there are no changes (git diff exits with 0) we force the command to return with 183.
      # This is a special exit code on Read the Docs that will cancel the build immediately.
      - |
        if [ "$READTHEDOCS_VERSION_TYPE" = "external" ] && git diff --quiet origin/main -- docs/ .readthedocs.yaml requirements-initial.txt requirements.txt;
        then
          exit 183;
        fi
```


#### Cancel builds on a branch

If you have pull request preview builds enabled, any pull request to any branch will trigger a build.
If you do not want to build documentation on a specific branch, you can cancel a build programmatically through your {file}`.readthedocs.yaml` file.

```yaml
version: 2
build:
  os: "ubuntu-22.04"
  tools:
    python: "3.12"
  jobs:
    post_checkout:
      # Cancel the Read the Docs build
      # https://docs.readthedocs.io/en/stable/build-customization.html#cancel-build-based-on-a-condition
      - exit 183;
```
