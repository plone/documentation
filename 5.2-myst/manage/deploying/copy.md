# Copying A Plone Site

```{admonition} Description
Quick instructions on how to create a copy of a Plone installation.
```

## Introduction

These instructions tell you the basics of creating a duplicate of Plone site
for testing or back-up

## Prerequisites

- Ability to use file system manager to copy files from/to the remote server
- Ability to use the command line

## Plone Site Contents

In order to copy a Plone site the following must be copied

- `buildout.cfg` - defines your site package configuration
- `src folder` - all add-ons you have developed yourself
- `var/filestorage/Data.fs` - ZODB database of your site
- `var/blobstorage` folder which contains file-like objects of ZODB database (BLOBs)

Other folders (eggs, downloads, parts) etc. are generated by buildout command and may
be left empty.

## Copying And Bootstrapping A Plone Site

- Create a new site in the destination using Plone installer and make sure you can log-in to the site with temporary admin account
- Copy var/filestorage/Data.fs from the old system to the new system - note that admin password is stored in Data.fs and the password given during the creation of a new site is no longer effective after Data.fs copy
- Copy blobs from the old system to the new system by copying var/blobstorage/ folder
- Copy src/ folder from the old system if you have any custom development code there
- Copy buildout.cfg and other .cfg files
- Rerun buildout in order to automatically re-download and configure all Python packages needed to run the site
  : - python bootstrap.py to make the buildout use new local Python interpreter
    - Then bin/buildout to regenerate parts/ folder

## Copying Site Data In UNIX Environment

Below are example UNIX commands to copy a Plone site data from a computer to
another over SCP/SSH connection.

The actual \$USERNAME and folder locations depend on your system configuration.

```{note}
A copy of the Plone site configuration must already exist on the target computer.
```

These instructions are for copying or creating a backup of your site data.

This operation can be performed on a running system - Data.fs is append only file and you
will lose transactions which happened during the copying of the end of the file.

## Copy Local To Remote

Run this command in your buildout Plone installation.

Copy Data.fs database:

```shell
scp -C -o CompressionLevel=9 var/filestorage/Data.fs plone@server.com:/srv/plone/site/var/filestorage
```

## Copy BLOB Files Using Rsync

BLOB files contain file and image data uploaded to your site.

Since the file content rarely changes after upload, rsync can synchronize only changed
files using -a (archive) flag.

```shell
rsync -av --compress-level=9 var/blobstorage plone@server.com:/srv/plone/site/var
```

## Upgrading a Plone Site

To upgrade Plone, see {doc}`manage/upgrading`.