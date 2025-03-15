---
myst:
  html_meta:
    "description": "Contributing to Plone 6 Documentation"
    "property=og:description": "Contributing to Plone 6 Documentation"
    "property=og:title": "Contributing to Plone 6 Documentation"
    "keywords": "Plone, Plone Contributor Agreement, License, Code of Conduct"
---

(contributing-documentation-index-label)=

# Contribute to documentation

This part of the documentation describes how to contribute to Plone Documentation.
Contributions to Plone Documentation are welcome.

```{contents} On this page
:local:
```

## Choose your path

{doc}`/contributing/first-time`
:   First-time contributors to Plone and its documentation should read this first.
    Fixing typographical errors and writing documentation is a relatively easy way to learn how to contribute to Plone.

{doc}`setup-build`
:   Start here if you have previously contributed to Plone.
    This guide shows you how to set up and build your environment to contribute to documentation.

{doc}`authors`
:   This guide shows you how to run a live preview of documentation while you edit it, perform quality checks, choose a code syntax highlighting lexer, improve search engine results, and follow structure, organization, and styles in Plone Documentation.

{doc}`myst-reference`
:   This reference guide provides frequently used MyST markup code snippets that you can use while you write documentation.

{doc}`themes-and-extensions`
:   This reference guide describes the themes and extensions used in Plone Documentation, with links to their documentation and usage.

{doc}`admins`
:   This guide covers automated deployments, hosting, automated testing, previewing, and importing and converting external package documentation into Plone Documentation.


(contributing-permission-to-publish-label)=

## Granting permission to publish

Before you contribute documentation, you must give permission to publish your contribution according to the license we use.
You may give that permission in two ways.

- Sign the [Plone Contributor Agreement](https://plone.org/foundation/contributors-agreement).
  This method also covers contributions to Plone code.
  It is a one-time only process.
- In every pull request or commit message, include the following statement.

  > I, [full name], agree to have this contribution published under Creative Commons 4.0 International License (CC BY 4.0), with attribution to the Plone Foundation.

The Plone Documentation is licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/).
A copy of the license is included in the root of this repository.


(documentation-repositories-label)=

## Documentation repositories

Plone documentation consists of several repositories.

-   [`documentation`](https://github.com/plone/documentation)
-   [`plone.api`](https://github.com/plone/plone.api)
-   [`plone.restapi`](https://github.com/plone/plone.restapi)
-   [`volto`](https://github.com/plone/volto)

[`documentation`](https://github.com/plone/documentation) is the primary repository.
When you {doc}`setup and build <setup-build>` the documentation, it will automatically pull in the other repositories via git submodules.

```{important}
We currently use the branches `plone/documentation@6.0`, `plone/plone.api@main`, `plone/plone.restapi@main`, and `plone/volto@main` as the default branches for developing Plone 6 Documentation.
```


(contributing-documentation-github-menu-label)=

## GitHub menu

In the upper right of the documentation, you will see the GitHub Octocat icon. 

```{image} /_static/contributing/github-navigation.png
:alt: GitHub navigation menu
```

You can use this menu to quickly navigate to the `documentation` source repository or open an issue.
You can also browse open issues and pull requests to see what has already been reported, or work started on, to improve Plone Documentation.
You can also give a reaction of a thumbs up 👍 on an issue or pull request to express that it is valuable to work on.

```{tip}
Working on documentation or on issues labeled with either `33 needs: docs` or `41 lvl: easy` are the two best ways for first-timers to contribute.
This is because first-timers have a fresh perspective that might be overlooked by old-timers.
```


(contributing-quick-edits-label)=

## Edit via GitHub's website

You can make small edits for minor issues, such as typographical errors, misspellings, and English grammar and syntax, through the GitHub website.

1.  Navigate to the repository as noted in {ref}`documentation-repositories-label`.
1.  Navigate into the `docs` directory to find the source file to edit.
1.  Click the {guilabel}`pencil icon` to edit the file in the browser.

    ```{image} /_static/edit-pencil-icon.png
    :alt: GitHub Edit this file
    ```
1.  Make edits, add a commit message, select {guilabel}`Create a new branch for this commit and start a pull request`, then click {guilabel}`Propose changes`.
1.  Make your pull request against the default branch of the repository.
1.  Members who subscribe to the repository will receive a notification and review your request.
1.  Request a review from other team members.


(contributing-large-edits-label)=

## Edit in your local editor

For large edits in your local editor, first follow the instructions in {doc}`setup-build`.

Once you have your environment set up, then you can follow the standard practice for making a pull request.
This practice differs according to the repository's files that you edit.

You can then edit the documentation of either Plone in the primary repository or any of the other projects in their folder inside the {file}`/submodules` folder.


### Git submodules

```{danger}
Every time you commit a git submodule, your deity kills a kitten.
```

```{image} /_static/contributing/git-commit-submodule.jpg
:alt: Two furry brown brick characters with stubby arms and legs and razor sharp teeth chase an adorable kitten across a lush green lawn to its ultimate demise.
```

Please save teh kittehs!
Never commit a git submodule.

If you mistakenly ~~kill a kitten~~ commit a git submodule, then you can ~~time travel~~ revert the commit, depending on whether it was the most recent commit or earlier.
Use one of the following processes for what works best in your situation.

If it was in your most recent commit, use the following.
This command will also revert all other changes in the commit.

```shell
git reset --hard HEAD~1
```

If it was an earlier commit, use the following process.
Check out only the submodule folder to a specific commit or remote branch where the folder's changes are not committed.

```shell
git fetch
git checkout <remote>/<branch> -- <submodule-folder>
```

Alternatively, use the log to copy the commit hash, and use that to check out that hash for your submodule folder.

```shell
git log
git checkout <commit-hash> -- <submodule-folder>
```

Finally, to force your cloned repository to use the same submodule as the upstream, pull the changes from upstream, then push to your cloned repository branch.

```shell
git pull upstream main
git push
```

```{seealso}
[How to undo a committed submodule command](https://stackoverflow.com/questions/46500441/how-to-undo-a-committed-submodule-command/46500544#46500544).
```


(contributing-documentation-only-label)=

### Working with only the `plone/documentation` repository

This section describes how to make contributions to files in the `plone/documentation` repository only, and excludes files in `submodules/plone.api/docs`, `submodules/plone.restapi/docs` and `submodules/volto/docs`.

1.  From the project root directory, sync your local `6.0` branch with its remote.
    You might need to resolve conflicts.

    ```shell
    git checkout 6.0
    git pull
    ```

1.  Create a new branch from `6.0`.

    ```shell
    git switch -c <new_branch>
    ```

1.  Edit files, save, preview, and test.
    You must run and pass the builds `html` and `linkcheck` without causing new errors.

    ```shell
    # Optionally clean the builds to avoid cache issues
    make clean
    make html
    make linkcheckbroken
    ```

    ```{note}
    Currently there are some errors on the `html` build, mostly due to empty `meta` HTML tags.
    You are welcome to fix as many errors as you like.
    You are only responsible to fix errors that you create.
    ```

    ```{note}
    Eventually the `vale` build will be required, but not at this time.
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

1.  Visit the GitHub `documentation` repository, and [create a pull request](https://github.com/plone/documentation/compare) against the branch `6.0`.
1.  Members who subscribe to the repository will receive a notification and review your request.
1.  Request a review from other team members.


(contributing-editing-external-package-documentation-label)=

### Editing external package documentation

To edit documentation of imported external packages, including `plone/plone.api`, `plone/plone.restapi`, and `plone/volto`, the process is slightly different.
Plone Documentation uses git submodules to manage multiple repositories.
You already imported the external repositories into the `plone/documentation` repository as described in {doc}`setup-build`.

1.  Change your working directory to the imported package's directory under `submodules/`.

    ```shell
    # Choose one.
    cd submodules/plone.api/docs
    cd submodules/plone.restapi/docs/source
    cd submodules/volto/docs/source
    ```

1.  Sync your local development branch with its remote.
    You might need to resolve conflicts.

    ```shell
    git checkout main
    
    # pull in the latest changes
    git pull
    ```

1.  Create a new branch from the development branch.

    ```shell
    git switch -c <new_branch>
    ```

1.  Make edits to files in `submodules/<external_package>/<path-to-docs>` using your favorite editor, and save, preview, and test.
    You must run and pass the builds `livehtml` and `linkcheckbroken` without causing new errors.

    ```shell
    # Optionally clean the builds to avoid cache issues.
    # For the external packages' documentation only, you must use
    # "docs-" as a prefix for `make` targets. This convention avoids
    # conflicts with the `make` targets of source code.
    make docs-clean
    make docs-livehtml
    make docs-linkcheckbroken
    ```

1.  Commit and push your changes to the remote.

    ```shell
    git add <files>
    git commit -m "My commit message"
    git push
    ```

1.  Visit the GitHub `plone/<external_package>` repository, and create a pull request against the development branch.
1.  Members who subscribe to the `plone/<external_package>` repository will receive a notification and review your request.
1.  Request a review from other team members.


## More ways to contribute to documentation

-   Discuss during sprints, conferences, trainings, and other Plone events.
-   Ask on the [Plone Community Forum, Documentation topic](https://community.plone.org/c/documentation/13).
-   Ask in the [Plone Documentation chat on Discord](https://discord.com/invite/d9dZcA4Ezw).


(contributing-documentation-code-of-conduct-label)=

## Code of Conduct

See {ref}`contributing-code-of-conduct-label`.


```{toctree}
---
caption: Contribute to Documentation
maxdepth: 2
hidden: true
---

setup-build
authors
myst-reference
themes-and-extensions
admins
```
