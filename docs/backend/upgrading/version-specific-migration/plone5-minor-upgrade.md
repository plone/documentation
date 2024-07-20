---
myst:
  html_meta:
    "description": "Upgrading Plone 5 within 5.x.x series"
    "property=og:description": "Upgrading Plone 5 within 5.x.x series"
    "property=og:title": "Upgrading Plone 5 within 5.x.x series"
    "keywords": "Upgrading, Plone 5"
---

(upgrading-plone-5-within-5.x.x-series-label)=

# Upgrading Plone 5 within 5.x.x series

This chapter outlines steps for minor upgrades within the Plone 5 major release.


```{warning}
Before performing any Plone upgrade, you should always have a complete backup of your site.
See the {doc}`../preparations` chapter of this documentation for more details.

In addition, you should check the {doc}`../version-specific-migration/index` chapter of this documentation for any notes that may apply to the specific version upgrade that you are about to perform.
```

## Buildout

Out of the box, Plone's Unified Installer includes a {file}`buildout.cfg` (typically located at `your-plone-directory/zinstance/buildout.cfg`) file that contains the following parameter.

```cfg
extends =
    base.cfg
    versions.cfg
    # https://dist.plone.org/release/5.1-latest/versions.cfg
```

This tells buildout to get all of its package versions from the included {file}`versions.cfg` file.
Notice that there is another line, commented out, that points to `dist.plone.org`.
This location will always contain the most recent versions that comprise the latest release in the Plone 5.1 series.
You can also replace `5.1-latest` with `5.0-latest` or `5.2-latest`, or another existing minor release in the 5.x series.

To upgrade your buildout to use the latest Plone 5.1.x release, comment out `versions.cfg` and uncomment the line pointing to `dist.plone.org`, so it looks like this:

```cfg
extends =
    base.cfg
    # versions.cfg
    https://dist.plone.org/release/5.1-latest/versions.cfg
```

Save your changes.


### Upgrading

Stop your Plone instance:

```console
bin/plonectl stop
```

Rerun buildout:

```console
bin/buildout
```

This may take a some time, as Plone downloads new releases.

When buildout finishes running, restart your Plone instance:

```console
bin/plonectl start
```


## Migration

Visit your Management Interface (http://yoursite:8080).
You will see a message prompting you to run Plone's migration script for each site in your instance:

{guilabel}`This site configuration is outdated and needs to be upgraded.`

Click the {guilabel}`Upgrade` button next to the site and the upgrade will run.

Check {guilabel}`Dry Run` if you want to test the migration before you execute it.
