---
myst:
  html_meta:
    "description": "Contributing to Plone"
    "property=og:description": "Contributing to Plone"
    "property=og:title": "Contributing to Plone"
    "keywords": "Plone, Plone Contributor Agreement, License, Code of Conduct"
---

(contributing-to-plone-index-label)=

# Contributing to Plone

This part of the documentation describes how to contribute to Plone, including all its projects and repositories under the Plone GitHub organization.

If instead you want to create a web application project using Plone, see {ref}`get-started-install-label`.

To contribute to any project in Plone, you must follow the policies of the [Plone Foundation](https://plone.org/foundation), [Plone GitHub organization](https://github.com/plone/) and the specific project.

This chapter covers policies that apply to all Plone projects.
Other chapters cover any variations and additional policies for each project.

(contributing-sign-and-return-the-plone-contributor-agreement-label)=

## Sign and return the Plone Contributor Agreement

You must give permission to the Plone Foundation to publish your contribution, according to the license we use.
Plone uses the [GNU General Public License, version 2](https://github.com/plone/Products.CMFPlone/blob/master/LICENSE) for most of its projects and for any new projects.
A few other projects use the [modified BSD license](https://opensource.org/license/bsd-3-clause/), [MIT License](https://opensource.org/license/mit/), or [Creative Commons Attribution-ShareAlike 4.0 International license](https://creativecommons.org/licenses/by-sa/4.0/).
You grant permission by signing and returning the Plone Contributor Agreement.

A volunteer member of the Plone Foundation will review your signed agreement.

If accepted, your GitHub account will be added to a team in the Plone GitHub organization with appropriate access, and you will simultaneously receive an email from GitHub for you to accept the invitation to join the team.

Allow up to one week for processing.
Contact the Plone Foundation at agreements@plone.org for further information, including the status of your request.

```{button-link} https://plone.org/foundation/contributors-agreement
:color: primary

Sign the Plone Contributor Agreement
```

```{seealso}
-   [Plone License FAQ](https://plone.org/foundation/copyright-licensing-logo/license-faq)
-   [Plone Framework Components Relicensing Policy, Framework Components Available Under a BSD License](https://plone.org/foundation/about/materials/foundation-resolutions/plone-framework-components-relicensing-policy#3b050ad2-361a-46de-b5c6-9b90f8947eb7)
```

(contributing-code-of-conduct-label)=

## Code of Conduct

The Plone Foundation has published a [Code of Conduct](https://plone.org/foundation/materials/foundation-resolutions/code-of-conduct).
All contributors to the Plone Documentation follow the Code of Conduct.


(contributing-first-time-contributors-label)=

## First-time contributors

First-time contributors should read and follow our guide {doc}`first-time`.


(report-bugs-and-feature-requests-label)=

## Report bugs and request features

When you experience a bug with, or want to request a feature for Plone, but you don't know in which package you should create the GitHub issue, you can create an issue in the primary Plone repository, [`Products.CMFPlone`](https://github.com/plone/Products.CMFPlone/).
Someone will help identify in which of the dozens of repositories that make up Plone the actual change and pull request should be made.


(contributing-continuous-integration-label)=

## Continuous integration

```{include} /_inc/_continuous-integration.md
```

(contributing-change-log-label)=

## Change log entry

Plone packages require that you include a change log entry or news item with your contribution.
This is enforced by continuous integration through GitHub Actions.

Plone uses [`towncrier`](https://github.com/collective/zestreleaser.towncrier) to manage change log entries and to automatically generate history or change log files from the entries.
The log file is usually named `CHANGES.rst`, `CHANGES.md`, or `CHANGELOG.md`, and is located at the root of the package.
When a package is released with a new version, the release manager runs `towncrier` as part of the release process.
Because the log file is automatically generated, you should not edit it directly, except to make corrections, such as broken links.


(contributing-create-a-news-item-file-label)=

### Create a news item file

To create a change log entry or news item, create a file in the `news` directory, located in the root of the package.

For Volto, its repository is in a monorepo structure, consisting of several packages in the `packages` folder.
Thus for Volto and its packages, change log entries should be created in `packages/PACKAGE_NAME/news/`, which is the root of the package.
When making a change to its documentation, set up, continuous integration, or other repository-wide items, place a change log entry in `packages/volto/news/` as a default.

The change log entry's format must be `###.type`, where `###` is the referenced GitHub issue or pull request number, `.` is the literal extension delimiter, and `type` is one of the following strings.

- `breaking` for breaking changes
- `bugfix` for bug fixes
- `documentation` for documentation
- `feature` for new features
- `internal` for internal changes

A package configures the types it allows in a file `towncrier.toml` located at the root of its package directory.


(write-a-good-change-log-entry-label)=

### Write a good change log entry

```{important}
These change log entries become narrative documentation.
```

The content of this file must include the following.

-   A brief message that summarizes the changes in your contribution.
-   An attribution to yourself, in the format of `@github_username`.

You can write a good change log entry with the following guidance.

-   Use a narrative format, in the past tense, proper English spelling and grammar, and inline markup as needed.
-   Write your change log entry for its appropriate audience.
    -   Most entries should address _users_ of the software.
    -   An entry for a change to a public API should address _developers_.
-   If you fix a bug, write what was broken and is now fixed.
    You should not write _how_ you fixed it.
-   If you add or change a feature or public API, write a summary of previous behavior, what it does now, and how to use it.
-   Refer to narrative documentation as needed.

The following text is an example of a good change log entry, placed inside {file}`/news/4470.documentation`.

```text
Changed a few broken links in `CHANGELOG.md` from URLs to inline literals to avoid errors when validating links. See https://6.docs.plone.org/volto/contributing/documentation.html#docs-linkcheckbroken for usage. @stevepiercy
```

The following would be a poor change log entry.

```text
Fix #123456 by chaning config of additionalToolbarComponents [did_not_read_this_guide]
```


(contributing-project-configuration-files-label)=

## Project configuration files

To standarize the developer experience across packages, a configuration tool is used.

See the [tool documentation](https://github.com/plone/meta) for more information.

(contributing-specific-contribution-policies-for-projects-label)=

## Specific contribution policies of projects

Each Plone project may have specific contribution policies and guidance.
This may include writing tests, developing add-ons, internationalization and localization, logging, and debugging.

The following is an abridged list of actively developed Plone projects with links to how to contribute to them.

`Products.CMFPlone`
:   The primary Plone project.
    See its [repository](https://github.com/plone/Products.CMFPlone).

Documentation
:   "If it's not documented, it's broken."
    See {doc}`documentation/index`.

Plone API
:   API methods for Plone functionality.
    See {doc}`../plone.api/contribute`.

Plone REST API
:   A RESTful API for Plone.
    See {doc}`/plone.restapi/docs/source/contributing/index`.

Volto
:   Plone 6 default frontend.
    See {doc}`../volto/contributing/index`.

(contributing-releases-label)=

## Releases

The Plone [Release Team](https://plone.org/community/teams/release-team) manages the release of new versions of Plone.

We use [`zest.releaser`](https://zestreleaser.readthedocs.io/en/latest/) for releasing the Python packages used in Plone, including [Plone core (`Products.CMFPlone`)](https://github.com/plone/Products.CMFPlone/), {doc}`/classic-ui/index`, {doc}`/plone.restapi/docs/source/index`, {doc}`/plone.api/index`, and {doc}`/backend/index`.

We use [`release-it`](https://github.com/release-it/release-it) for releasing the Node.js packages used in Plone, including {doc}`Volto </volto/index>` and the [Classic UI mockup](https://github.com/plone/mockup).

```{toctree}
---
caption: Contributing
maxdepth: 2
hidden: true
---

first-time
documentation/index
core/index
plone-api
plone-restapi
volto
github-administration
```
