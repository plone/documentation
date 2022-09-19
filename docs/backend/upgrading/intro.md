---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(upgrading-plone-label)=

# Upgrading Plone

This document covers the procedures and issues involved in upgrading an existing Plone installation.

This involves both the upgrading of the program set, and migration of the site itself.

Generally, you will often see the word *migration* used as the word we use to describe the process of getting your Plone site
from one version of a given component to a newer version.

For most people, this means upgrading Plone to a newer release, for example from 5.2.x to 6.0.x.

Migration is necessary because the internals of Plone sometimes change to support new functionality.
When that's the case, the content which is stored in your Plone instance may not match what the new version of the software expects.

Plone has a builtin tool that migrates existing content to the new structure.

This guide describes migration in Plone, specifically how you upgrade between different versions.

Before migrating you should read this entire document to understand the potential impact migrating will have on your Plone site.

It is also wise to have read the {doc}`troubleshooting <troubleshooting>` section, in case you may need to employ one of the techniques there.

The guide applies to all contemporary versions of Plone.

For unsupported versions from the year 2009 and before, see older versions of this documentation.

## Version Numbering And Terminology

Plone has a policy that increases the version number to a .0 on every major release.

This means that when we say a *major release*, we are referring to a x.0 release, whereas a minor release has the version numbering 4.3.14 or 5.1.0

In addition to the general procedure there are {doc}`version-specific migration guides </manage/upgrading/version_specific_migration/index>`.

These guides contain more specific instructions and valuable information that has been collected from real-life migration cases.

## Upgrade Strategies

### Inplace Migrations

A inplace migration means the content and settings of a Plone installation are being updated while Plone is running.
These upgrades use a builtin tool and basically run upgrade-steps that are collected in [plone.app.upgrade](https://github.com/plone/plone.app.upgrade/).

This approach is recommended for all upgrades of minor version and can work fine for most mayor upgrades.
When dealing with mayor changes in Plone or with very large or complex installations a export-import based migration (see below) is often the better solution.

During in-place migrations it is advisable to **not make large leaps** in version numbers.
A single upgrade should not try to bridge multiple major version numbers.

Going from Plone 4.0 to Plone 5.1 is fine.

If you are at Plone 2.5 and want to upgrade to the latest Plone 5, you should approach this in several steps:

- First upgrade from Plone 2.5 to the latest Plone 3 version (3.3.6).
- Then upgrade from Plone 3 to the latest Plone 4 version.
- Then upgrade from Plone 4 to the latest Plone 5 version.


### Export-import Migrations

Export all content and settings that you want to keep from an old site and import it to a fresh site.

This approach allows you to migrate from Plone 4 to 6, from Python 2 to 3 and from Archetypes to Dexterity in one migration-step and is recommended for large and complex migrations.

The recommended tool for this is https://github.com/collective/collective.exportimport. An alternative is transmogrifier (see the training {ref}`training:transmogrifier-label`)

## Mayor Changes

The following mayor changes in the history of Plone require special attention when migrating:

### Plone 5.0: Dexterity replaces Archetypes

With Plone 5.0 the default framework for content-types switched from Archetypes to Dexterity.

Until Plone 5.2.x (in Python 2 only!) there is a builtin migration from Archetypes to Dexterity.
See https://pypi.org/project/plone.app.contenttypes/2.2.3/#migration for details on the migration of custom and default content-types to Dexterity.

Using [collective.exportimport](https://pypi.org/project/collective.exportimport/) you can export Archetypes content and import it as Dexterity content.


### Plone 5.2: Support for Python 3

Plone 5.2 added support for Python 3 while Plone 6.0 dropped support for Python 2.
This means that you can use Plone 5.2 to upgrade to Python 3.

This requires that you run Plone in Python 3 and only use code that supports Python 3. It also requires that you migrate the database in a separate step from Python 2 to 3 while Plone is not running.

See the chapters {ref}`migrating-52-to-python3-label` and {ref}`migrate-zodb-to-python3-label` for detailed info on these steps.

Using [collective.exportimport](https://pypi.org/project/collective.exportimport/) you can export content in Python 2 and import it in Python 3.

### Plone 6.0: Volto as new frontend

Plone 6.0 comes with a new default frontend called {term}`Volto` which is written in React and expects some subtle but important changes.

See {ref}`backend-migrate-to-volto-label` for these specialized migration-steps.
