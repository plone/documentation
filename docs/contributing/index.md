---
html_meta:
  "description": "Contributing to Plone Documentation."
  "keywords": "Plone, Plone Contributor Agreement, License, Code of Conduct"
---

(contributing-index-label)=

# Contributing to Plone Documentation

This document describes how to contribute to the Plone Documentation.

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


(contributing-manage-on-github-label)=

## Managing contributions on GitHub

Contributions are managed through the [Documentation repository on GitHub](https://github.com/plone/documentation).

First discuss whether you should perform any work.
Any method below is acceptable, but are listed in order of most likely to get a response.

- [Search for open issues](https://github.com/plone/documentation/issues) and comment on them.
- [Create a new issue](https://github.com/plone/documentation/issues/new/choose).
- Discuss during conferences, trainings, and other Plone events.
- Ask on the [Plone Community Forum, Documentation topic](https://community.plone.org/c/documentation/13).
- Ask in the [Plone chat on Discord](https://discord.com/invite/zFY3EBbjaj).

As a convenience, at the top right of every page, there is a GitHub navigation menu.
Tap, click, or hover over the GitHub Octocat icon for options.

```{image} /_static/github-navigation.png
:alt: GitHub navigation menu 
```

You can use this menu to quickly navigate to the source repository, open an issue, or suggest an edit to the current document.
Of course, you can use whichever tools you like.

Next edit files, commit your changes, push them to the remote repository, and submit a pull request to resolve the issue.

Members who subscribe to the repository will receive a notification and review your request.


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
