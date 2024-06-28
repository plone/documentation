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

```{important}
Although Plone core includes Volto—the React based, default frontend for Plone 6—this guide does not apply to Volto and its packages.
To contribute to Volto, see {doc}`../volto`.
```

This guide assumes that you have basic knowledge of how to use git and GitHub.
If you have never contributed to Plone, or you lack basic knowledge of how to use git and GitHub, you should first read {doc}`/contributing/first-time` for more information.

```{important}
You must {ref}`contributing-sign-and-return-the-plone-contributor-agreement-label` before your contribution can be accepted.
```


## Version support policy

Before you contribute to Plone core, check the [version support policy](https://plone.org/download/release-schedule) to see which versions of Plone are currently supported.


## Pre-requisites

It is beyond the scope of this documentation to provide installation instructions for all pre-requisites for your operating system.
However, the following links and sections below may be helpful.

```{include} ../../volto/contributing/install-operating-system.md
```

-   Python {SUPPORTED_PYTHON_VERSIONS}
-   {term}`GNU make`
-   {term}`Git`
-   A C compiler


### Python

Installing Python is beyond the scope of this documentation.
However, it is recommended to use a Python version manager, {term}`pyenv` that allows you to install multiple versions of Python on your development environment without destroying your system's Python.
Plone requires Python version {SUPPORTED_PYTHON_VERSIONS}.


### Make

```{include} ../../volto/contributing/install-make.md
```


### Git

```{include} ../../volto/contributing/install-git.md
```

### C compiler

You need a C compiler on your system to compile some of the Python libraries that Plone uses.

On macOS, Developer Tools provides Clang for a C compiler.

On Linux, [GNU Compiler Collection (GCC)](https://gcc.gnu.org/) is a common option.



## Install Plone core for development

The tool that installs Plone core is `buildout.coredev`.

The current default and development branch of `buildout.coredev` is `6.1`
Older versions are named according to their `major.minor` version.
Its versions align with Plone's `major.minor` versions.

Use a separate directory for each version of Plone to which you want to contribute.
This will avoid switching between git branches, then re-running buildout, which can cause dependency conflicts between versions of Plone.

To set up a Plone 6 development environment, change your working directory to wherever you place your projects, and clone https://github.com/plone/buildout.coredev.
You can specify the branch that you want to check out with the `-b` option.

```shell
cd [MY_PROJECTS]
# clone a specific major.minor version branch
git clone -b 6.1 https://github.com/plone/buildout.coredev
cd buildout.coredev
```

````{important}
If you want to use a Python version that is not 3.11, follow these instructions.

Open the file {file}`bootstrap.sh` at the root of the repository.
Notice that the script expects Python 3.11 to be installed on your system and in your user's `PATH`.

```shell
#/bin/sh
`which python3.11` -m venv .
```

Edit it according to the Python version you want to use, then save and close the file.
After you have run the script, you should undo the change, otherwise you have a local change in git that you might accidentally commit.
````

Now run the script to install Plone 6.

```shell
./bootstrap.sh
```

If you run into issues in this process, see {doc}`troubleshoot`.

This will run for a long time if it's your first pull (approximately 10-20 minutes, depending on network speed and your hardware).

Once that's done, you can start an instance of Plone with the following command.

```shell
./bin/instance fg
```

To visit your Plone instance, you can open the link http://0.0.0.0:8080 in a web browser.

You will be presented with several options.
Click the button {guilabel}`Create Classic UI Plone site`.

Enter values in the form, and click the button {guilabel}`Create Plone Site`.

You will be redirected to your new Classic UI Plone site.

```{warning}
Ignore the warning about accessing the Plone backend through its Classic UI frontend.

Do not follow the instructions to install Volto.
They will not work with buildout.
To contribute to Volto, you will need to start over, and follow {doc}`../volto`.
```

To login, the default credentials are the following.

-   username: `admin`
-   password: `admin`


## Work with git

```{important}
This section applies to members of the GitHub `plone/developers` team, who have write access to repositories under the Plone GitHub organization.

Members of the `plone/contributors` team do not have write access, and instead must follow the process to set up their remote upstream and origin branches as described in {ref}`set-up-your-environment-label`.
```

Always begin by checking out the git branch on which you want to work.
This is the base branch to which you will create a pull request.

If you just cloned `https://github.com/plone/buildout.coredev`, then the `6.1` branch is checked out and current, and you can skip the rest of this section and continue on the next, {ref}`contributing-core-edit-packages-label`.

```shell
git checkout 6.1
```

Next pull down and merge any recent changes from the remote tracked repository with a single command.

```shell
git pull
```


(contributing-core-edit-packages-label)=

## Edit packages

First identify the names of the Plone packages you want to work on.
If you do not know, you can ask in the [Plone Community Forum](https://community.plone.org/).
Only a few packages are in {file}`src/` by default.

Next create a new file {file}`buildout.local.cfg`, and add the names of packages that you want to develop under the `auto-checkout` list.

```ini
[buildout]
extends =
  buildout.cfg

auto-checkout =
    # Add packages that you want to develop
    plone.app.event
    icalendar
    # others
    ...
```

When you make changes in your package, then rerun buildout with the following command, specifying your new buildout configuration file with the `-c` option.
You can add the `-N` flag to save time by not checking PyPI to see if there are updates to packages that were already installed.

```shell
./bin/buildout -c buildout.local.cfg -N
```

```{seealso}
`mr.developer` checks out additional repositories using the `auto-checkout` option.
For more information, see {doc}`mrdeveloper`.
```

````{tip}
To avoid conflicts with `buildout.coredev` files, you can configure git for your user.
Either create or edit a file at {file}`~/.gitconfig`.
Then add the following stanza to it.

```cfg
[core]
    excludesfile = ~/.gitignore_global
```

Then add any standard `.gitignore` syntax to exclude files from getting committed and pushed to a remote repository.
````

Next create a new development branch on which you want to work from the current branch, tracking the upstream Plone repository, and check it out.
It's a good idea to use a branch name that includes the issue number and is descriptive of what it resolves.

```shell
git switch -c 123-thing-i-fixed
```

Now you can edit your code without affecting the original branch.


(contributing-core-test-locally-label)=

## Test locally

If you change the expected behavior of a feature in a package, you should write a test to cover the change.

To run a test for the specific package that you modified, use the `-m` option followed by the package name, as shown in the following example.

```shell
./bin/test -m plone.app.event
```

If any test fails, do not commit and push the changes.
Instead write a test that passes.

After the package level tests pass with your change, you can {ref}`contributing-core-create-a-pull-request-label` and let CI run and ask Jenkins to run the full test suite.

However, if CI or Jenkins report a test failure that you want to troubleshoot locally, you can run the full unit test suite to ensure other packages aren't affected by the change.
It takes 5-10 minutes to run the full unit test suite.

```shell
# Run unit tests
./bin/test
```

If you run acceptance tests with the `--all` option, it will repeatedly launch and close browser windows that gain focus, disrupting you from doing any other work.
This takes 30-40 minutes to run.
If you can't afford this disruption, you can defer it to Jenkins.

```shell
# Run acceptance tests
./bin/test --all
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


## Jenkins and mr.roboto

Plone has a continuous integration ({term}`CI`) setup and follows CI rules.

When you push a change to a Plone package, there may be GitHub workflows that run automatically.
The CI package [mr.roboto](https://github.com/plone/mr.roboto) will perform some checks and suggest that you run Jenkins after all other CI runs.

See {doc}`continuous-integration` for more information.


## Additional material

```{toctree}
:maxdepth: 1

documentation
continuous-integration
mrdeveloper
troubleshoot
plips
plip-review
package-dependencies
release
```
