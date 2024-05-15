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


## Add a project to Read the Docs

To add a new site to Read the Docs to preview documentation or storybooks in pull requests, you need to configure your project's repository and import it into Read the Docs.
You also need an account on Read the Docs and have write access to the repository.


### Configuration files

The following are example files that you can use to configure your project for Read the Docs pull request previews.

-   [Plone Sphinx Theme `Makefile`](https://github.com/plone/plone-sphinx-theme/blob/main/Makefile), specifically the `rtd-pr-preview` section.
    This is the command to use to build documentation previews on Read the Docs.
-   [Plone Sphinx Theme `requirements-initial.txt`](https://github.com/plone/plone-sphinx-theme/blob/main/requirements-initial.txt) specifies the initial Python packaging tool requirements to set up a virtual environment.
-   [Plone Sphinx Theme `requirements-docs.txt`](https://github.com/plone/plone-sphinx-theme/blob/main/requirements-docs.txt) specifies the requirements to use Plone Sphinx Theme and build the docs.
-   [Plone Sphinx Theme `.readthedocs.yaml`](https://github.com/plone/plone-sphinx-theme/blob/main/readthedocs.yaml) specifies the configuration and command to build the docs.
-   [Plone Sphinx Theme `.github/workflows/rtd-pr-preview.yml`](https://github.com/plone/plone-sphinx-theme/blob/main/.github/workflows/rtd-pr-preview.yml) specifies when to build the docs, specifically only when a pull request is opened against the `main` branch and there are changes to documentation files.
    You might need to adjust the branch name, paths, and files to check for changes.


### Read the Docs administration

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

Plone uses an organization on Read the Docs.
The main project is Plone Documentation.
All other Plone projects with documentation should be configured as subprojects.

```{todo}
Add how to set up a subproject.
```

For most Plone projects, you will not want to Read the Docs to publish the `latest` or other specific versions.
Plone projects currently self-host their official documentation.

1.  For the version that you want to deactivate, click its {guilabel}`…` icon, and select {guilabel}`Configure version`.
1.  Toggle the {guilabel}`Active` option off, and click {guilabel}`Update version`.


## Add a project to Netlify

To add a new site to Netlify to preview built documentation or storybooks, you need to add a new site to Netlify.

1.  Visit [Team Overview](https://app.netlify.com/teams/plone/overview).
1.  Click {guilabel}`Add a new site` and select {guilabel}`Import an existing project`.
1.  Click {guilabel}`Deploy with GitHub`.
1.  Select {guilabel}`plone` for the GitHub organization.
1.  Click {guilabel}`Configure Netlify on GitHub`.
1.  Select the organization to where you want to install Netlify.
1.  Click {guilabel}`Select repositories` and select the repository that you want to add.
1.  Click {guilabel}`Update access`.
1.  Netlify sends an email to members of the email group `admins` at `plone.org`, who need to review and approve the request.
    However the email doesn't specify the repository, and admins will not know what to do.
    You must send email to that group, including in your request the organization and repository, such as `plone/volto`.
1.  The admin must login to GitHub as an organization owner, then navigate to the requested repository's {guilabel}`Settings`. [What else Admin person?]
1.  The admin replies to the requestor, letting them know the request was approved.

From here you need to update your repository to work with Netlify.
For an example, see the following files.

-   [Volto `Makefile`](https://github.com/plone/volto/blob/main/Makefile), specifically the `netlify` section.
    This will become the command used to build docs on Netlify.
-   [Volto `requirements-docs.txt`](https://github.com/plone/volto/blob/main/requirements-docs.txt) specifies the requirements to build the docs.
-   [Volto `netlify.toml`](https://github.com/plone/volto/blob/main/netlify.toml) specifies when to build the docs, specifically only when there are changes to documentation files.

Finally you need to configure your site in Netlify.
You may have done some of these steps earlier, but you might need to refine them.
The critical pieces are the following.

1.  From the dashboard, select the site to edit it.
1.  Click {guilabel}`Site configuration`.
1.  One time only, under {guilabel}`General > Site details` click {guilabel}`Change site name`.
    A modal dialog appears.
    Enter the site name using the pattern `ORGANIZATION_NAME-REPOSITORY_NAME`.
    For example, `plone-components`.
    Click {guilabel}`Save`.
1.  Under {guilabel}`Build & deploy > Continuous deployment`, scroll to {guilabel}`Build settings`, and click {guilabel}`Configure`, then enter the following values.
    -   {guilabel}`Base directory`: `/`
    -   {guilabel}`Package directory`: `/`
    -   {guilabel}`Build command`: `make netlify`.
        This is the command you would define in your `Makefile`.
    -   {guilabel}`Publish directory`: `_build/html`.
        This is where the `make` command will output files.
    -   Finally click {guilabel}`Save`.
1.  Under {guilabel}`Build & deploy > Continuous deployment`, scroll to {guilabel}`Branches and deploy contexts`, and click {guilabel}`Configure`, then enter appropriate values.
