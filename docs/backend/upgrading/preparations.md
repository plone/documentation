---
myst:
  html_meta:
    "description": "Plone upgrade preparations"
    "property=og:description": "Plone upgrade preparations"
    "property=og:title": "Plone upgrade preparations"
    "keywords": "Plone, upgrade, preparations"
---


(upgrade-preparations-label)=

# Preparations

This chapter lists things to do before you migrate Plone.


(upgrade-gather-informationlabel)=

## Gather information

-   Read the "What's new in..." for your relevant Plone version, and read the release notes.
    You will find these in the [online directory of released versions on `dist.plone.org`](https://dist.plone.org/release/).
    As an example, you can find the file [`RELEASE-NOTES.md` for 6.0.0b2](https://dist.plone.org/release/6.0.0b2/RELEASE-NOTES.md).
-   Check for dependencies.

    -   Read the release notes of the Plone release to which you are upgrading, in particular:

        -   What version of Python is required?
        -   What version of Zope is required?
        -   Do you need any new Python libraries?

    -   Make sure all the add-on products you are using have been updated to support the version of Plone to which you are upgrading.
    -   Start with the third-party products that are in use on your site.
        Verify that they have been updated or verified to work on the new version, and get them upgraded in your existing instance before you start the Plone/Zope/Python upgrade, if possible.
    -   If Zope depends on a newer version of Python, install the new version of Python first.
    -   If the newer version of Plone depends on a newer version of Zope, you will need to install that before proceeding with the Plone upgrade.

```{seealso}
Zope has its own documentation of migration guidelines.
Of most interest for migration are the following documents.

-   [What's new](https://zope.readthedocs.io/en/latest/news.html) at a high level.
-   [Migrating between Zope versions](https://zope.readthedocs.io/en/latest/migrations/index.html).
-   [Detailed changelog](https://zope.readthedocs.io/en/latest/changes.html).

If Plone is being upgraded at the same time as a Zope version, Plone will usually handle the Zope upgrade with its own migration script.
```


(upgrade-back-up-your-Plone-site-label)=

## Back up your Plone site

```{danger}
Always back up your Plone site before upgrading.
```

```{seealso}
See Plone 5.2 documentation, [Backing up your Plone deployment](https://5.docs.plone.org/manage/deploying/backup.html).
```

```{todo}
Migrate the Plone 5.2 docs for Backing up your Plone deployment into Plone 6 docs.
```


(upgrade-setup-a-test-environment-to-rehearse-the-upgrade-label)=

## Setup a test environment to rehearse the upgrade

```{danger}
Never work directly on your live site until you know that the upgrade was successful.
```

Always create a test environment to rehearse the upgrade.
Copy your instance into a new environment and upgrade the copy.
This is a good way of working through your third-party products and dependencies in preparation for the final upgrade of the live site.
