---
myst:
  html_meta:
    "description": "Administrators guide to writing Plone Documentation. It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation."
    "property=og:description": "Administrators guide to writing Plone Documentation. It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation."
    "property=og:title": "Administrators guide"
    "keywords": "Plone, Documentation, automated deployments, hosting, automated testing, importing external packages, preview, build, pull request"
---

(administrators-guide-label)=

# Administrators guide

This guide is for administrators of Plone Documentation.
It covers automated deployments, hosting, automated testing, previewing, and importing external package documentation into Plone Documentation.


## Deployments and hosting

Plone Documentation is automatically deployed through GitHub Workflows.
The Plone Admin and Infrastructure Team maintains the processes and the servers where this documentation is hosted.
Some individual projects may also host their projects on Read the Docs.


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
We did this with `volto`, `plone.api`, and `plone.restapi` documentation.
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
-   [Plone Sphinx Theme `requirements-docs.txt`](https://github.com/plone/plone-sphinx-theme/blob/main/requirements-docs.txt) specifies the requirements to use Plone Sphinx Theme and build the docs.
-   [Plone Sphinx Theme `conf.py`](https://github.com/plone/plone-sphinx-theme/blob/main/docs/conf.py) the Sphinx configuration file to build the docs.
-   [Plone Sphinx Theme `.readthedocs.yaml`](https://github.com/plone/plone-sphinx-theme/blob/main/.readthedocs.yaml) specifies the configuration and Makefile command that Read the Docs uses to build the docs.
-   [Plone Sphinx Theme `.github/workflows/rtd-pr-preview.yml`](https://github.com/plone/plone-sphinx-theme/blob/main/.github/workflows/rtd-pr-preview.yml) specifies when to build the docs, specifically only when a pull request is opened and there are changes to the documentation files.
    You might need to adjust the `paths` and `project-slug` for your documentation.


### Import your project

After logging in to your Read the Docs account, you can import your project.

1.  Click {guilabel}`Add project`.
1.  For {guilabel}`Repository name`, enter the GitHub organization, a forward slash, and the repository to import, for example, `plone/volto`.
1.  Click {guilabel}`Continue`.
1.  In the {guilabel}`Add project` screen, you can configure basic project settings, including its {guilabel}`Name`, {guilabel}`Repository URL`, {guilabel}`Default branch`, and {guilabel}`Language`.
    The defaults are usually accurate.
1.  Click {guilabel}`Next`.
    Read the Docs will redirect you to the project details, and start building the docs, but you don't need to wait.
1.  Click the {guilabel}`Settings` button.
1.  Scroll to the end of the page and check the box for {guilabel}`Build pull requests for this project`.
1.  Click {guilabel}`Save` to save the new setting.


### Prevent search engine indexing

Many Plone projects currently self-host their official documentation at {doc}`/index`.
These projects get indexed by search engines.

For pull request previews, unsupported branches or versions, or other situations, you most likely do not want search engines to index your documentation.

You can create a branch that serves as a landing page for your documentation.
Using `sphinx-reredirects`, you can configure this page to redirect to your official documentation.

In Plone 6 Documentation, the branch `rtd-redirect` consists of a single landing page that redirects visitors to https://6.docs.plone.org/.
You can use this branch as a minimal example for your documentation.

This branch also includes a custom {file}`robots.txt` file to discourage, but not absolutely prevent, search engine indexing.
It also includes a 404 not found page that directs visitors the correct site.

In addition, you should consider configure Read the Docs for the following.

-   Deactivate your build
-   Hide your build
-   Set your default branch from your default to the home page branch, such as `rtd-redirect`.

With this configuration and setup, you will also continue to have pull request preview builds.

```{seealso}
-   [`robots.txt` support](https://docs.readthedocs.io/en/stable/reference/robots.html)
-   [Automation rules](https://docs.readthedocs.io/en/stable/automation-rules.html)
-   [Versions](https://docs.readthedocs.io/en/stable/versions.html)
-   [Managing versions automatically](https://docs.readthedocs.io/en/stable/guides/automation-rules.html)
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


## Update git submodules

Only members of the Plone Documentation Team should update git submodules from the primary repository `documentation`.

1.  Update all branches to pull in the latest changes to their primary branches.
    Start from the root of the `documentation` project directory.

    ```shell
    # documentation
    git checkout 6.0
    git pull
    # plone.api
    cd submodules/plone.api
    git checkout main
    git pull
    # plone.restapi
    cd ../../submodules/plone.restapi
    git checkout main
    git pull
    # plone.api
    cd ../../submodules/volto
    git checkout main
    git pull
    ```

1.  Get the status of the submodules to determine whether you need to update the git submodules.
    
    ```shell
    cd ../..
    git status
    ```

    If you see any of the submodules listed to add, then proceed to the next step, else you have nothing more to do.

1.  Update the submodule to point to the latest commit, and push your changes to the remote repository.
    You can combine multiple submodules in a single command.

    ```shell
    cd ../..

    # for plone.api
    git add submodules/plone.api
    git commit -m "Update tip submodules/plone.api"

    # for plone.restapi
    git add submodules/plone.restapi
    git commit -m "Update tip submodules/plone.restapi"

    # for Volto
    git add submodules/volto
    git commit -m "Update tip submodules/volto"
    
    ## for all submodules
    git add submodules/plone.api submodules/plone.restapi submodules/volto
    git commit -m "Update tips submodules/plone.api submodules/plone.restapi submodules/volto"

    # finally push your changes
    git push
    ```


## Welcome bot

[Welcome](https://github.com/apps/welcome) bot automatically makes comments in issues and pull requests when a person creates their first issue, pull request, or merged pull request.
It is configured as a GitHub app.
Its configuration file is located at {file}`.github/config.yml`.
