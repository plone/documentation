---
myst:
  html_meta:
    "description": "Export and import Plone site data with plone.exportimport"
    "property=og:description": "Export and import Plone site data with plone.exportimport"
    "property=og:title": "Export and import Plone site data with plone.exportimport"
    "keywords": "Plone 6, plone.exportimport, export, import, site, data, Content, Principals, Relations, Translations, Discussions, Redirects"
---

(exportimport)=

# Export and import site data

The `plone.exportimport` package provides support to export and import all kinds of data from and to Plone sites using an intermediate JSON format.

Most features use {doc}`plone.restapi <../plone.restapi/docs/source/index>` to serialize and deserialize data.


## Command line utilities

This package provides two command line utilities, `plone-exporter` and `plone-importer`.

### `plone-exporter`

Export content from a Plone site to a directory in the file system.
You can call `plone-exporter` as shown.

```shell
plone-exporter [--include-revisions] <path-to-zopeconf> <site-id> <path-to-export-data>
```

The following command shows typical usage.

```shell
plone-exporter instance/etc/zope.conf Plone /tmp/plone_data/
```

By default, the revisions history (older versions of each content item) are not exported.
If you do want them, add `--include-revisions` on the command line.


### `plone-importer`

Import content from a file system directory into an existing Plone site.

You can call `plone-importer` as shown.

```shell
plone-importer <path-to-zopeconf> <site-id> <path-to-import-data>
```

The following command shows typical usage.

```shell
plone-importer instance/etc/zope.conf Plone /tmp/plone_data/
```


## Supported data

-   Content (Dexterity content items)
    -   Ordering
    -   Local roles
    -   Versions (when using the `--include-revisions` command line option)
    -   Default pages
-   Principals (members and groups)
-   Relations (relationships between content items)
-   Translations (translation groups)
-   Discussions (content comments)
-   Redirects (redirect information)


## Exported data structure

Some goals of the new data structure are to:

-   support diff of exported data, and
-   have blob files near the content item that uses it.

After exporting content, at the top level directory, the following objects exist.

| Name | Description |
| --- | --- |
| `content` | Directory containing content item information exported from the site |
| `discussions.json` | JSON File with discussions (comments) exported from the site |
| `principals.json` | JSON File with members and groups exported from the site |
| `redirects.json` | JSON File with redirect information exported from the site |
| `relations.json` |  JSON File with content relations exported from the site  |
| `translations.json` | JSON File with translation groups exported from the site  |


### Content directory structure

The {file}`content` directory contains all content items exported from the site.
Each content item has its own subdirectory, named with the UID of the content, including the serialized data and all blob files related to this content.

One special case is the directory for the `Plone Site` object, which is named `plone_site_root`.

| Name | Description |
| --- | --- |
| `content/__metadata__.json` | JSON File with metadata information about the exported content |
| `content/<content uid>` | Directory with serialization for a content item |
| `content/plone_site_root` | Directory with serialization for the Plone Site Root |


#### Content item directory structure

Consider a File content item with UID `3e0dd7c4b2714eafa1d6fc6a1493f953` and a PDF file named {file}`plone.pdf` (added in the `file` field), the exported directory will have the following structure.

| Name | Description |
| --- | --- |
| `content/3e0dd7c4b2714eafa1d6fc6a1493f953/data.json` | JSON File with serialized representation of a content item |
| `content/3e0dd7c4b2714eafa1d6fc6a1493f953/file/plone.pdf` | Blob file stored in the `file` field in the content item |
