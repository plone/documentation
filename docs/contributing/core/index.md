---
myst:
  html_meta:
    "description": "Contribute to Plone 6 Core"
    "property=og:description": "Contribute to Plone 6 Core"
    "property=og:title": "Contribute to Plone 6 Core"
    "keywords": "Plone, Plone Contributor Agreement, License"
---

# Contribute to Plone 6 core

This guide describes the process of how to contribute to, and develop in, Plone core.
It expands upon {doc}`/contributing/index`.

Although Plone core includes Volto—the React based, default frontend for Plone 6—this guide does not apply to Volto and its packages.
To contribute to Volto, see {doc}`../volto`.

This guide assumes that you have basic knowledge of how to use Git and GitHub.
If you have never contributed to Plone, or you lack basic knowledge of how to use Git and GitHub, you should first read {doc}`/contributing/first-time` for more information.

```{important}
You must {ref}`contributing-sign-and-return-the-plone-contributor-agreement-label` before your contribution can be accepted.
```


## Version support policy

Before you contribute to Plone core, check the [version support policy](https://plone.org/download/release-schedule) to see which versions of Plone are currently supported.


(plone-prerequisites-label)=

## Prerequisites

It is beyond the scope of this documentation to provide installation instructions for all prerequisites for your operating system.
However, the following links and sections below may be helpful.

```{include} ../../volto/_inc/_install-operating-system.md
```

-   Python {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}
-   {term}`GNU make`
-   {term}`Git`
-   A C compiler


### Python

Installing Python is beyond the scope of this documentation.
However, it is recommended to use a Python version manager, {term}`pyenv` that allows you to install multiple versions of Python on your development environment without destroying your system's Python.
Plone requires Python version {{SUPPORTED_PYTHON_VERSIONS_PLONE61}}.


### Make

```{include} ../../volto/_inc/_install-make.md
```


### Git

```{include} ../../volto/_inc/_install-git.md
```

### C compiler

You need a C compiler on your system to compile some of the Python libraries that Plone uses.

On macOS, Developer Tools provides Clang for a C compiler.

On Linux, [GNU Compiler Collection (GCC)](https://gcc.gnu.org/) is a common option.


(contributing-core)=
## Install Plone core for development

The tool that installs Plone core is `buildout.coredev`.

The current default and development branch of `buildout.coredev` is `{PLONE_BACKEND_MINOR_VERSION}`.
Older versions are named according to their `major.minor` version.
Its versions align with Plone's `major.minor` versions.

Use a separate directory for each version of Plone to which you want to contribute.
This will avoid switching between Git branches, which can cause dependency conflicts between versions of Plone.

To set up a Plone 6 development environment, clone https://github.com/plone/buildout.coredev.

```shell
git clone https://github.com/plone/buildout.coredev
cd buildout.coredev
```

Use the following command to install Plone and run it.

```shell
make run
```

To create and visit a new Plone site, visit http://localhost:8080, select the Classic UI distribution, and fill out and submit the form, ensuring you create a site with sample content against which you can test.

Stop Plone with the keyboard shortcut {kbd}`ctrl-c`.

```{seealso}
For more Make targets, see documentation in [`buildout.coredev`'s `README-make.md` file](https://github.com/plone/buildout.coredev/blob/{PLONE_BACKEND_MINOR_VERSION}/README-make.md).
The most relevant section is [How to use the `Makefile`](https://github.com/plone/buildout.coredev/blob/{PLONE_BACKEND_MINOR_VERSION}/README-make.md#how-to-use-the-makefile).
```


(contributing-core-work-with-git-label)=

## Work with Git

```{important}
This section applies to members of the GitHub `plone/developers` team, who have write access to repositories under the Plone GitHub organization.

Members of the `plone/contributors` team do not have write access, and instead must follow the process to set up their remote upstream and origin branches as described in {ref}`set-up-your-environment-label`.
```

Always begin by checking out the Git branch on which you want to work.
This is the base branch to which you will create a pull request.

If you just cloned `https://github.com/plone/buildout.coredev`, then the `{PLONE_BACKEND_MINOR_VERSION}` branch is checked out and current, and you can skip the rest of this section and continue on the next, {ref}`contributing-core-edit-packages-label`.

```shell
git checkout {PLONE_BACKEND_MINOR_VERSION}
```

Next pull down and merge any recent changes from the remote tracked repository with a single command.

```shell
git pull
```


(contributing-core-edit-packages-label)=

## Edit packages

First identify the names of the Plone packages you want to work on.
If you do not know, you can open an issue in the Plone GitHub repository for [`Products.CMFPlone`](https://github.com/plone/Products.CMFPlone/issues/), and someone might identify the source within a few days.
You can also read the conceptual guide {doc}`/conceptual-guides/package-dependencies` to get a mental model of the structure of Plone.
You can also ask in the [Plone Community Forum](https://community.plone.org/).

Only a few packages are in {file}`src/` by default.

Next, edit the file {file}`mxcheckouts.ini` at the root of your checkout, adding the name of the package that you want to develop as a new section.
The following example adds `plone.app.multilingual`.

```ini
[plone.app.multilingual]
use = true
```

You can now check out the package and start your instance with the checked out package using the following commands.

```shell
make sources-dirty
make run
```

Next create a new development branch on which you want to work from the current branch, tracking the upstream Plone repository, and check it out.
It's a good idea to use a branch name that includes the issue number and is descriptive of what it resolves.

```shell
git switch -c 123-thing-i-fixed
```

Now you can edit your code without affecting the original branch.


(contributing-core-test-locally-label)=

## Test locally

If you change the expected behavior of a feature in a package, you should write a unit or acceptance test, as appropriate, to cover the change.

Plone uses [Playwright](https://playwright.dev/) to run acceptance tests.
`plone.app.robotframework` provides a script to install Playwright browsers.

```shell
.venv/bin/rfbrowser init
```

To run tests for the specific package that you modified, use `.venv/bin/pytest` followed by the package name, as shown in the following example.

```shell
.venv/bin/pytest src/plone.app.multilingual
```

If any test fails, do not commit and push the changes.
Instead write a test that passes.

Following [How to invoke pytest](https://docs.pytest.org/en/stable/how-to/usage.html), you can run tests for the package you're developing.
Using the pytest keyword option `-k`, followed by a string expression in double quotes, you can select only unit tests or only acceptance tests to run as shown below.
With no options, pytest will run all tests.

```shell
.venv/bin/pytest src/plone.app.multilingual -v -k "not robot" 
```

```shell
.venv/bin/pytest src/plone.app.multilingual -v -k "robot" 
```

After the package level tests pass with your change, you can {ref}`contributing-core-create-a-pull-request-label`, which will start the CI checks.
After all CI checks pass, then you can ask Jenkins to run the full test suite.

If either CI or Jenkins report a test failure, and you want to troubleshoot it locally, then you can run the full test suite to ensure other packages aren't affected by the change.
It takes about 15-20 minutes to run the full unit test suite.

```shell
.venv/bin/pytest
```


(contributing-core-change-log-label)=

## Change log

All changes require a change log entry.

For packages that use [towncrier](https://pypi.org/project/towncrier/) to produce change logs, see {ref}`contributing-change-log-label`.
A package that uses towncrier has a `news` directory at its repository or package root.

For packages that don't use towncrier, edit either {file}`CHANGES.rst`, {file}`CHANGES.txt`, or {file}`HISTORY.txt` in each package you have modified, adding a summary of the change.
New change log entries should be added at the top of {file}`CHANGES.rst`.


(contributing-core-create-a-pull-request-label)=

## Create a pull request

After you have completed all the foregoing steps, push your changes to a remote branch and create a pull request in GitHub.
If you are working from an issue, include "Fixes #ISSUE-NUMBER" in the description.
This enables automatic closing of the related issue when the pull request is merged.
This also creates a hyperlink to the original issue for easy reference.


## Continuous integration

```{include} /_inc/_continuous-integration.md
```


## Additional material

```{toctree}
:maxdepth: 1

documentation
continuous-integration
mrdeveloper
plips
plip-review
package-dependencies
release
```
