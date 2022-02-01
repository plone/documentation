---
html_meta:
  "description": "Contributing to Plone Documentation."
  "keywords": "Plone, Plone Contributor Agreement, License, Code of Conduct"
---

(contributing-index-label)=

# Contributing to Plone Documentation

This document describes how to contribute to Plone Documentation.

Contributions to the Plone Documentation are welcome.


(contributing-permission-to-publish-label)=

## Granting permission to publish

Before you contribute, you must give permission to publish your contribution according to the license we use.
You may give that permission in two ways.

- Sign the [Plone Contributor Agreement](https://plone.org/foundation/contributors-agreement).
  This method also covers contributions to Plone code.
  It is a one-time only process.
- In every pull request or commit message, include the following statement.

  > I, [full name], agree to have this contribution published under Creative Commons 4.0 International License (CC BY 4.0), with attribution to the Plone Foundation.

The Plone Documentation is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
A copy of the license is included in the root of this repository.


(contributing-roles-label)=

## Contributor Roles

Contributors to the Plone Documentation may perform one or many roles.

- **Plone users and developers** use this documentation because it is accurate and actively maintained.
  People in these roles typically contribute minor corrections.
  They should read {doc}`setup-build` and {doc}`writing-docs-guide`.
- **Authors** create Plone Documentation.
  They should read {doc}`setup-build` and {doc}`writing-docs-guide`.
  They should also read {doc}`authors` for guidance and tips for writing good technical documentation.


(contributing-quality-requirements-label)=

## Documentation quality requirements

We use GitHub Actions with every pull request to enforce Plone Documentation quality.
We recommend that you build the documentation locally to catch errors and warnings early on.
See {doc}`setup-build` for instructions for how to set up and build the documentation and to run quality checks.


(contributing-manage-on-github-label)=

## Making contributions on GitHub

Contributions are managed through git repositories on GitHub.

- [documentation](https://github.com/plone/documentation)
- [volto](https://github.com/plone/volto)

First discuss whether you should perform any work.
Any method below is acceptable, but are listed in order of most likely to get a response.

- Search for open issues in [`documentation`](https://github.com/plone/documentation/issues) or [`volto`](https://github.com/plone/volto/issues) and comment on them.
- Create a new issue in [`documentation`](https://github.com/plone/documentation/issues) or [`volto`](https://github.com/plone/volto/issues).
- Discuss during conferences, trainings, and other Plone events.
- Ask on the [Plone Community Forum, Documentation topic](https://community.plone.org/c/documentation/13).
- Ask in the [Plone chat on Discord](https://discord.com/invite/zFY3EBbjaj).

As a convenience, at the top right of every page, there is a GitHub navigation menu.
Tap, click, or hover over the GitHub Octocat icon for options.

```{image} /_static/github-navigation.png
:alt: GitHub navigation menu 
```

You can use this menu to quickly navigate to the `documentation` source repository, open an issue, or suggest an edit to the current document.
Note that this navigation convenience is provided only for the `documentation` repository.


(contributing-quick-edits-label)=

### Quick edits

Quick edits for minor issues, such as typographical errors, misspellings, and English grammar and syntax, can be made through the GitHub user interface.

1.  Navigate to the repository as noted in {ref}`contributing-manage-on-github-label`.
1.  Navigate with the `docs` directory to find the source file to edit.
1.  Click the {guilabel}`pencil icon` to edit the file in the browser.

    ```{image} /_static/edit-pencil-icon.png
    :alt: GitHub Edit this file
    ```
1.  Make edits, add a commit message, select {guilabel}`Create a **new branch** for this commit and start a pull request`, then click {guilabel}`Propose changes`.
1.  Make your pull request against the branch `6-dev`.
1.  Members who subscribe to the repository will receive a notification and review your request.


(contributing-large-edits-label)=

### Large edits

For large edits, first follow the instructions in {doc}`setup-build`.

Once you have your environment set up, then you can follow the standard practice for making a pull request.
This practice differs depending on whether you are making contributions to only the core `documentation` files or `volto` files as well.


(contributing-documentation-only-label)=

### Working with only the `documentation` repository

This section describes how to make contributions to files in the `documentation` repository only, and excludes `volto` files.

1.  From the project root directory, synch your local `6-dev` branch with its remote.
    You might need to resolve conflicts.

    ```shell
    git checkout 6-dev
    git pull
    ```

1.  Create a new branch from `6-dev`.

    ```shell
    git checkout -b <new_branch>
    ```

1.  Edit files, save, preview, and test.
    You must run and pass the builds `html` and `linkcheck` without causing new errors.

    ```shell
    # Optionally clean the builds to avoid cache issues
    make clean
    make html
    make linkcheck
    ```

    ```{note}
    Currently there are some errors on the `html` build, mostly due to empty `meta` HTML tags.
    You are welcome to fix as many errors as you like.
    You are only responsible to fix errors that you create.
    ```

    ```{note}
    Eventually the `spellcheck` build will be required, but not at this time.
    We welcome improvements to the dictionary.
    ```

    ```{seealso}
    {ref}`setup-build-available-documentation-builds-label`.
    ```

1.  After the builds pass, commit changes to your branch, and push it to the remote repository on GitHub.
    The remote repository may be either a branch in your fork of the project or a branch in the `plone/documentation` upstream repository.

    ```shell
    git commit -m "My descriptive commit message"
    git push
    ```

1.  Visit the GitHub `documentation` repository, and [create a pull request](https://github.com/plone/documentation/compare) against the branch `6-dev`.
1.  Members who subscribe to the repository will receive a notification and review your request.


(contributing-documentation-and-volto-label)=

### Working with both the `documentation` and `volto` repositories

When you want to edit files within the `docs/volto` subdirectory, the process is slightly different.
We use git submodules to manage multiple repositories.
We imported the `volto` repository into the `documentation` repository as described in {doc}`setup-build`.

```{important}
We currently use the branches `plone/documentation@6-dev` and `plone/volto@plone6-docs` as the main branches for developing Plnoe 6 Documentation.
These branches may change as we get closer to a production release.
```

1.  From the project root directory, synch your local `6-dev` branch with its remote.
    You might need to resolve conflicts.

    ```shell
    git checkout 6-dev
    git pull
    ```

1.  Change your working directory from the project root directory to `submodules/volto`.

    ```shell
    cd submodules/volto
    ```

1.  Update the submodule, and synch your local `plone6-docs` branch with its remote.
    You might need to resolve conflicts.

    ```shell
    git submodule update
    git checkout plone6-docs
    git pull
    ```

1.  Create a new branch from `volto/plone6-docs`.

    ```shell
    git checkout -b <new_branch>
    ```

1.  Make edits to files in `docs/volto` using your favorite editor, and save, preview, and test.
    You must run and pass the builds `html` and `linkcheck` without causing new errors.

    ```shell
    # Optionally clean the builds to avoid cache issues
    make clean
    make html
    make linkcheck
    ```

1.  Back in `submodules/volto`, commit and push your changes to the remote.

    ```shell
    git add <files>
    git commit -m "My commit message"
    git push
    ```

1.  Now return to the project root directory, and update the submodule to point to the commit you just made, and push your changes to the remote repository.

    ```shell
    cd ../..
    git add submodules/volto
    git commit -m "Update submodules/volto tip"
    git push
    ```

1.  Visit the GitHub `volto` repository, and [create a pull request](https://github.com/plone/volto/compare) against the branch `plone6-docs`.
1.  Members who subscribe to the repository will receive a notification and review your request.



(contributing-code-of-conduct-label)=

## Code of Conduct

The Plone Foundation has published a [Code of Conduct](https://plone.org/foundation/materials/foundation-resolutions/code-of-conduct).
All contributors to the Plone Documentation follow the Code of Conduct.


```{toctree}
---
caption: Contributing
maxdepth: 2
hidden: true
---

setup-build
writing-docs-guide
authors
```
