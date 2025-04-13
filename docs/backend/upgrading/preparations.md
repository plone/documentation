---
myst:
  html_meta:
    "description": "Plone upgrade preparations"
    "property=og:description": "Plone upgrade preparations"
    "property=og:title": "Plone upgrade preparations"
    "keywords": "Plone, upgrade, preparations, ZODB, collective.recipe.backup, buildout, backup, restore"
---


(upgrade-preparations-label)=

# Preparations

This chapter describes things to do before you migrate Plone.


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

This back up guide assumes the following.

-   You back up your Plone site.
-   You back up your buildout and its caches.
-   You back up your persistent data storage using a strategy that maintains data integrity without taking down your Plone site, that is performed periodically with adequate frequency, and that stores sufficient versions of your data.
-   You've tested the restore process.


### Where's my data?

Your Plone instance installation contains a directory {file}`./var`.
This directory is located in the same directory as the file {file}`buildout.cfg`.
It holds the frequently changing data files for the instance.
{file}`./var` contains the instance's log, process ID, and socket files.

The following directories contain your instance's content.


#### {file}`./var/filestorage`
 
The Zope Object Database ({term}`ZODB`) file storage is maintained in the directory {file}`./var/filestorage`.
The default file name is {file}`Data.fs`, although you could have multiple files or renamed it.
It's typically a large file which contains everything except {term}`blob`s.

The other files in this directory with the file extensions of `.index`, `.lock`, `.old`, or `.tmp` are ephemeral, and will be recreated by Zope if they're absent.


#### {file}`./var/blobstorage`

The directory {file}`./var/blobstorage` contains a deeply nested directory hierarchy that contains the blobs of your database.
These files may include PDFs, images, videos, office automation files, and other binary objects.

`filestorage` and `blobstorage` are maintained synchronously.
`filestorage` has references to blobs in `blobstorage`.
If the two storages are not synchronized, you'll get errors whenever their data is accessed.


### `collective.recipe.backup`

[`collective.recipe.backup`](https://pypi.org/project/collective.recipe.backup/) is a well-maintained buildout recipe that maintains data integrity for a live Plone database.

See its `README.md`'s section [Introduction](https://github.com/collective/collective.recipe.backup?tab=readme-ov-file#introduction) for its buildout recipe configuration.

The recipe supports several options, all of which are documented its `README.md`'s section [Supported options](https://github.com/collective/collective.recipe.backup/blob/master/README.rst#supported-options).

Perhaps the most useful option is `location`, which sets the destination for backup files.
Its default value is `var/backups`, inside the buildout directory.
The backup destination, may be any attached location, including another partition, drive, or network storage.


#### Operation

After running buildout to configure `collective.recipe.backup`, you'll find {file}`bin/backup` and {file}`bin/restore` scripts in your buildout directory.
Since all options are set via buildout, there are few command-line options, and operation is generally through bare commands.

{file}`bin/restore` will accept a date-time argument, if you keep multiple backups.
For restore operations, stop Plone before starting your restore, and restart after the restore is complete.

{file}`bin/backup` is commonly included in a cron table for regular operation.
You can run backup operations without stopping Plone.
Make sure you test your backup and restore process before you need it.


### Incremental backups

`collective.recipe.backup` offers both incremental and full backups, and will maintain multiple versions of backups.
Tune these to meet your needs.

When you enable incremental backups, the database packing operation will automatically cause the next backup to be a full backup.

If your backup continuity need is critical, then your incremental backup schedule may need to be frequent.
Some Plone sites require incremental backups every few minutes.


(upgrade-setup-a-test-environment-to-rehearse-the-upgrade-label)=

## Set up a test environment to rehearse the upgrade

```{danger}
Never work directly on your live site until you know that the upgrade was successful.
```

Always create a test environment to rehearse the upgrade.
Copy your instance into a new environment and upgrade the copy.
This is a good way of working through your third-party products and dependencies in preparation for the final upgrade of the live site.
