---
myst:
  html_meta:
    "description": "How to Back up and restore a Plone site that was installed using buildout"
    "property=og:description": "How to Back up and restore a Plone site that was installed using buildout"
    "property=og:title": "Back up and restore a Plone site"
    "keywords": "Plone 6, admin, install, configuration, upgrade, buildout"
---

(back-up-and-restore-a-plone-buildout-label)=

# Back up and restore a Plone buildout

This chapter explains how to back up and restore a Plone site that was installed using buildout.

(backup-your-plone-site-label)=

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

## Related content

-   {doc}`/admin-guide/export-import`
-   {doc}`/admin-guide/install-buildout`