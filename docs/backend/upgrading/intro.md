---
myst:
  html_meta:
    "description": "Introduction to upgrading Plone"
    "property=og:description": "Introduction to upgrading Plone"
    "property=og:title": "Introduction to upgrading Plone"
    "keywords": "Introduction, Upgrading, Plone, migration, version"
---

(introduction-label)=

# Introduction

This part of the documentation describes how to upgrade an existing Plone installation.
For most people, this means upgrading Plone to a newer release, for example, from 5.2.9 to 6.0.0.
This guide applies to all modern versions of Plone.
For unsupported versions from the year 2009 and before, see older versions of this documentation.

Upgrading Plone includes the Plone application and its add-ons, as well as migration of its content.

A *migration* is the process of taking a component in your Plone site, and moving it from its current version to a newer one.
Migration is necessary because the internals of Plone sometimes change to support new functionality.
When that's the case, the content that is stored in your Plone instance may not align with the requirements of the new version.
To handle this situation, Plone has a built-in tool that migrates existing content to the new structure.

Before migrating you should read this entire document, as well as {ref}`introduction-version-specific-upgrade-guides-label`, to understand the potential impact migrating will have on your Plone site.
It is also wise to read the {doc}`troubleshooting` chapter, in case you run into any issues.


(introduction-versioning-policy-and-numbering-label)=

## Versioning policy and numbering

Plone follows [semantic versioning](https://semver.org/) to communicate what users and developers can expect from a release regarding breaking changes, new features, and bug fixes.
We use a three-digit version scheme (e.g., `6.0.0`), following the `major.minor.patch` scheme.

(introduction-versioning-policy-breaking-or-major-release-label)=

### Breaking (major) release

A _breaking_ release indicates a change that might break an application or third-party add-on that relies on Plone.
The version numbering would increase as in the following example.

````
5.2.3 -> 6.0.0
````

For every breaking release, details of what breaks and how to mitigate it must be documented in the change and release notes.


(introduction-versioning-policy-feature-minor-release-label)=

### Feature (minor) release

A _feature_ release indicates that a new feature has been added to Plone in a non-breaking fashion.
The version numbering would increase as in the following example.

````
5.1.7 -> 5.2.0
````

You do not have to expect any breaking changes from such a release.
It is possible that the user interface changes, due to a new feature that has been added.


(introduction-versioning-policy-bugfix-patch-release-label)=

### Bugfix (patch) release

A _bugfix_ release indicates one or more bugs in Plone have been fixed.
The version numbering would increase as in the following example.

````
5.2.8 -> 5.2.9
````

There should be no breaking or UX/UI changes from such a release.
It just fixed a bug.

```{seealso}
A post on the Community forum, [Rules for Plone 6 development during the beta stage](https://community.plone.org/t/rules-for-plone-6-development-during-the-beta-stage/15432), discusses alpha and beta versioning.
```


(introduction-version-specific-upgrade-guides-label)=

## Version-specific upgrade guides

In addition to the general upgrade procedure, there are {doc}`version-specific migration guides <version-specific-migration/index>`.
These guides contain specific instructions and valuable information that has been collected from real-life migration cases.

This approach is recommended for all upgrades of minor versions, and can work fine for most major upgrades.
When dealing with major changes in Plone, or with very large or complex installations, an {ref}`export-import based migration <introduction-upgrade-strategies-export-import-migrations-label>` is often the better solution.

(introduction-upgrade-strategies-label)=

## Upgrade strategies


(introduction-upgrade-strategies-in-place-migrations-label)=

### In-place migrations

An in-place migration means the content and settings of a Plone installation are being updated while Plone is running.
These upgrades use a built-in tool.
They run upgrade steps that are collected in [plone.app.upgrade](https://github.com/plone/plone.app.upgrade/).

This approach is recommended for all upgrades of feature (minor) versions.
This usually works fine for most breaking (major) upgrades as well.

When dealing with major changes in Plone, or with very large or complex installations, an {ref}`export-import <introduction-upgrade-strategies-export-import-migrations-label>` based migration is often the better solution.

During in-place migrations, it is advisable **not to skip over** breaking (major) version numbers.

Going from Plone 5.2 to Plone 6.0 is fine.

If you are at Plone 2.5 and want to upgrade to the latest Plone 6, you should approach this in several steps:

-   First upgrade from Plone 2.5 to the latest Plone 3 version (3.3.6).
-   Then upgrade from Plone 3 to the latest Plone 4 version (4.3.20).
-   Then upgrade from Plone 4 to the latest Plone 5 version (5.2.15).
-   Then upgrade from Plone 5 to the latest Plone 6 version ({PLONE_BACKEND_PATCH_VERSION}).


(introduction-upgrade-strategies-export-import-migrations-label)=

### Export-import migrations

Export all content and settings that you want to keep from an old site and import it into a fresh site.

This approach allows you to migrate from Plone 4 to 6, from Python 2 to 3, and from Archetypes to Dexterity, in one migration step.
It is recommended for large and complex migrations.

The recommended tool for this is [`collective.exportimport`](https://github.com/collective/collective.exportimport).
An alternative is `transmogrifier` (see the training {ref}`training-2022:transmogrifier-label`).


(introduction-major-changes-label)=

## Major Changes

The following major changes in the history of Plone require special attention when migrating.


(introduction-plone-5.0-dexterity-replaces-archetypes-label)=

### Plone 5.0: Dexterity replaces Archetypes

With Plone 5.0 the default framework for content types switched from Archetypes to Dexterity.

Up through Plone 5.2.x, there is a built-in migration from Archetypes to Dexterity, but it only supports Python 2.
See [Migration](https://github.com/plone/plone.app.contenttypes/blob/2.2.3/docs/README.rst#migration) in the 2.2.3 release of `plone.app.contenttypes` for details on the migration of custom and default content types to Dexterity.

Using [collective.exportimport](https://pypi.org/project/collective.exportimport/) you can export Archetypes content and import it as Dexterity content.


(introduction-plone-5.2-support-for-python-3-label)=

### Plone 5.2: Support for Python 3

Plone 5.2 added support for Python 3, while Plone 6.0 dropped support for Python 2.
This means that you can use Plone 5.2 to upgrade to Python 3.

This requires that you run Plone in Python 3 and only use code that supports Python 3.
It also requires that you migrate the database in a separate step from Python 2 to 3 while Plone is not running.

See the chapters {doc}`version-specific-migration/upgrade-to-python3` and {doc}`version-specific-migration/upgrade-zodb-to-python3` for detailed information on these steps.

Using [collective.exportimport](https://pypi.org/project/collective.exportimport/), you can export content from Python 2 and import it in Python 3.


(introduction-plone-6.0-volto-as-new-frontend-label)=

### Plone 6.0: Volto as new frontend

Plone 6.0 comes with a new default frontend called {term}`Volto`.
It is written in React, and expects some subtle but important changes.

See {ref}`backend-migrate-to-volto-label` for the specific migration steps.
