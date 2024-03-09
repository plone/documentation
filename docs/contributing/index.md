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

To contribute to any project in Plone, you must follow the policies of the [Plone Foundation](https://plone.org/foundation), [Plone GitHub organization](https://github.com/plone/) and the specific project.

This chapter covers policies that apply to all Plone projects.
Other chapters cover any variations and additional policies for each project.


(contributing-sign-and-return-the-plone-contributor-agreement-label)=

## Sign and return the Plone Contributor Agreement

You must give permission to the Plone Foundation to publish your contribution, according to the license we use.
Plone uses the [GNU General Public License, version 2](https://github.com/plone/Products.CMFPlone/blob/master/LICENSE) for most of its projects and for any new projects.
A few other projects use the [modified BSD license](https://opensource.org/license/bsd-3-clause/).
You grant permission by signing and returning the Plone Contributor Agreement.

```{button-link} https://plone.org/foundation/contributors-agreement
:color: primary

Sign the Plone Contributor Agreement
```

After a member of the Plone Foundation reviews and accepts your signed agreement, your GitHub account will be added to a team in the Plone GitHub organization with appropriate access.
This process may take a few business days.

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


(contributing-continuous-integration-label)=

## Continuous integration

Plone project repositories use continuous integration (CI) to run tests, ensure code quality, or provide previews for every contribution.
Plone uses GitHub Actions, Jenkins, Cypress, Netlify, and other services for CI.
All of a project's CI jobs must pass before a contribution may be accepted.


(contributing-change-log-label)=

## Change log entry

Plone projects require that you include a change log entry or news item with your contribution.
This is enforced by continuous integration through GitHub Actions.

Plone uses [`towncrier`](https://github.com/collective/zestreleaser.towncrier) to manage change log entries and to automatically generate history or change log files from the entries.
The log file is usually named `CHANGES.rst`, `CHANGES.md`, or `CHANGELOG.md`, and is located at the root of the project.
When a project is released with a new version, the release manager runs `towncrier` as part of the release process.
Because the log file is automatically generated, you should not edit it directly, except to make corrections, such as broken links.

To create a change log entry or news item, create a file that is placed in the root of the repository directory at `/news`.
Its format must be `###.type`, where `###` is the referenced GitHub issue or pull request number, `.` is the literal extension delimiter, and `type` is one of the following strings.

-   `breaking` for breaking changes
-   `bugfix` for bug fixes
-   `documentation` for documentation
-   `feature` for new features
-   `internal` for internal changes

A project configures the types it allows in a file `towncrier.toml` located at the root of its repository.

The content of this file must include the following.

-   A brief message that summarizes the changes in your contribution.
-   An attribution to yourself, in the format of `@github_username`.

The following text is an example change log entry, placed inside {file}`/news/4569.documentation`.

```text
Fix broken links for ReactJS.org. @stevepiercy
```


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
    See {doc}`../plone.api/contribute/index`.

Plone REST API
:   A RESTful API for Plone.
    See {doc}`plone.restapi/docs/source/contributing/index`.

Volto
:   Plone 6 default frontend.
    See {doc}`../volto/contributing/index`.


```{toctree}
---
caption: Contributing
maxdepth: 2
hidden: true
---

first-time
documentation/index
../plone.api/contribute/index
../plone.restapi/docs/source/contributing/index
../volto/contributing/index
```
