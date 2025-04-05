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

### Introduction

The key rules for backing up a working system are:

- Back up everything
- Maintain multiple generations of backup
- Test restoring your backups

```{note}
This guide assumes you are already backing up your system as a whole. 
It only covers considerations specific to Plone. 
When we say we are assuming you’re already doing this for the system as a whole, what we mean is that your system backup mechanisms - rsync, bacula, whatever - are already backing up the directories into which you’ve installed Plone.
```

Your buildout and buildout caches are already backed up, and you’ve tested the restore process. 
Your remaining consideration is making sure that Plone’s database files are adequately backed up and recoverable.

### Objects in motion

Objects in motion tend to remain in motion. 
Objects that are in motion are difficult or impossible to back up accurately.

In other words, Plone is a long-lived process that constantly changes its content database. 
The largest of these files, the Data.fs filestorage which contains everything except Binary Large OBjects (BLOBs), is always open for writing. 
The BLOB storage, a potentially complex file hierarchy, is constantly changing and must be referentially synchronized to the filestorage.

This means that most system backup schemes are incapable of making useful backups of the content database while it’s in use. 
We assume you don’t want to stop your Plone site to backup, so you need to add procedures to make sure you have useful backups of Plone’s data. 
(We assume that you know that the same thing is true of your relational database storage.)

### Where’s my data?

Your Plone instance installation contains a `./var` directory. 
This directory is located in the same directory as `buildout.cfg`. 
It holds the frequently changing data files for the instance. 
Much of what’s in `./var`, though, is not your actual content database. 
Rather, it’s log, process id, and socket files.

The directories containing content data are:

#### Filestorage
`./var/filestorage`:

This is where Zope Object Database filestorage is maintained. 
Unless you’ve multiple storages or have changed the name, the key file is Data.fs. 
It’s typically a large file and contains everything except BLOBS.

The other files in filestorage, with extensions like .index, .lock, .old, .tmp are ephemeral, and will be recreated by Zope if they’re absent.

#### Blobstorage
`./var/blobstorage`:

This directory contains a deeply nested directory hierarchy that, in turn, contains the BLOBs of your database: PDFs, image files, office automation files and such.

The key thing to know about filestorage and blobstorage is that they are maintained synchronously. 
The filestorage has references to BLOBs in the blobstorage. 
If the two storages are not synchronized, you’ll get errors.

### collective.recipe.backup

[collective.recipe.backup](https://pypi.python.org/pypi/collective.recipe.backup) is a well-maintained recipe that solves the “objects in motion” problem for a live Plone database. 
It makes it easy to both back up and restore the object database. 
The recipe is basically a sophisticated wrapper around `repozo`, a Zope database backup tool, and `rsync`, the common file synchronization tool.

If you’re using any of Plone’s installation kits, `collective.recipe.backup` is included in your install. 
If not, you may add it to your buildout by adding a `backup` part:

```
[buildout]
parts =
    ...
    backup
    ...
[backup]
recipe = collective.recipe.backup
```

There are several useful option settings for the recipe, all set by adding configuration information. 
All are documented on [the PyPI page](https://pypi.python.org/pypi/collective.recipe.backup). 
Perhaps the most useful is the `location` option, which sets the destination for backup files:

```
[backup]
recipe = collective.recipe.backup
location = /path/to/reliably/attached/storage/filestorage
blobbackuplocation =  /path/to/reliably/attached/storage/blobstorage
```

If this is unspecified, the backup destination is the buildout var directory. 
The backup destination, though, may be any reliably attached location - including another partition, drive or network storage.

### Operation

After running buildout, you’ll find `bin/backup` and `bin/restore` scripts in your buildout directory. 
Since all options are set via buildout, there are few command-line options, and operation is generally as simple as using the bare commands. 
`bin/restore` will accept a date-time argument if you’re keeping multiple backups. 
See the docs for details.

You can run backup operations without stopping Plone. 
For restore operations, stop Plone before starting and restart after the restore is complete.

`bin/backup` is commonly included in a cron table for regular operation. 
Make sure you test backup/restore before relying on it.

### Incremental backups

`collective.recipe.backup` offers both incremental and full backup and will maintain multiple generations of backups. 
Tune these to meet your needs.

When incremental backup is enabled, doing a database packing operation will automatically cause the next backup to be a full backup.

If your backup continuity needs are critical, your incremental backup schedule may need to be frequent. 
There are Plone installations where incremental backups are run every few minutes.

(upgrade-setup-a-test-environment-to-rehearse-the-upgrade-label)=

## Setup a test environment to rehearse the upgrade

```{danger}
Never work directly on your live site until you know that the upgrade was successful.
```

Always create a test environment to rehearse the upgrade.
Copy your instance into a new environment and upgrade the copy.
This is a good way of working through your third-party products and dependencies in preparation for the final upgrade of the live site.
