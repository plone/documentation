---
myst:
  html_meta:
    "description": "Contributing to Plone Core Code"
    "property=og:description": "Contributing to Plone Core Code"
    "property=og:title": "Contributing to Plone Core Code"
    "keywords": "Plone, Plone Contributor Agreement, License, Code of Conduct, core, code"
---

(contributing-to-plone-core-code-index-label)=

# Contributing to Plone core code

This part of the documentation describes how to contribute to Plone core code, including all its packages and repositories under the Plone GitHub organization.

To contribute to any package in Plone, you must follow the policies of the [Plone Foundation](https://plone.org/foundation), [Plone GitHub organization](https://github.com/plone/) and the specific package.

This chapter covers policies that apply to all Plone packages.
Other chapters cover any variations and additional policies for each package.


(contributing-sign-and-return-the-plone-contributor-agreement-label)=

## Sign and return the Plone Contributor Agreement

You must give permission to the Plone Foundation to publish your contribution, according to the license we use.
Plone uses the [GNU General Public License, version 2](https://github.com/plone/Products.CMFPlone/blob/master/LICENSE).
You grant permission by signing and returning the Plone Contributor Agreement.

```{button-link} https://plone.org/foundation/contributors-agreement
:color: primary

Sign the Plone Contributor Agreement
```

After a member of the Plone Foundation reviews and accepts your signed agreement, your GitHub account will be added to a team in the Plone GitHub organization with appropriate access.
This process may take a few business days.

```{seealso}
[Plone License FAQ](https://plone.org/foundation/copyright-licensing-logo/license-faq)
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
-   An attribution to yourself, either in the format of `@github_username` or `[github_username]`.

The following text is an example change log entry, placed inside {file}`/news/4569.documentation`.

```text
Fix broken links for ReactJS.org. @stevepiercy
```


(contributing-plone-packages-label)=

## Plone core packages

Each Plone core package may have specific policies and guidance.
This may include writing tests, developing add-ons, internationalization and localization, logging, and debugging.

The following is an abridged list of actively developed Plone core packages with links to how to contribute to them.

`Products.CMFPlone`
:   The primary Plone package.
    See its [repository](https://github.com/plone/Products.CMFPlone).

Documentation
:   "If it's not documented, it's broken."
    See {doc}`documentation/index`.

Plone API
:    API methods for Plone functionality.
    See {doc}`../plone.api/contribute/index`.

Plone REST API
:   A RESTful API for Plone.
    See {doc}`plone.restapi/docs/source/contributing/index`.

Volto
:   Plone 6 default frontend.
    See {doc}`../volto/developer-guidelines/contributing`.

`plone.app.contentlisting`
:   Facilitates working with Plone content objects.
    See https://github.com/plone/plone.app.contenttypes

`plone.app.contenttypes`
:   Provides default content types for Plone.
    See https://github.com/plone/plone.app.contenttypes

`plone.app.event`
:   A calendar framework for Plone.
    See https://github.com/plone/plone.app.event

`plone.app.multilingual`
:   The default solution to create multilingual content in a Plone site.
    See https://github.com/plone/plone.app.multilingual

```{todo}
Add other important Plone packages to both the above list and the `toctree`.
```


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
../volto/developer-guidelines/contributing
```
