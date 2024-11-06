---
myst:
  html_meta:
    "description": "mr.developer"
    "property=og:description": "mr.developer"
    "property=og:title": "mr.developer"
    "keywords": "Plone, buildout, mr.developer"
---

# `mr.developer`

Plone core uses `mr.developer` to manage package development.
See [`mr.developer` on PyPI](https://pypi.org/project/mr.developer/) for more information, or run `bin/develop help` for a list of available commands.

To get all the latest updates, use the following commands.

```shell
git pull
bin/develop rebuild
```

This will get you the latest `coredev` configuration, check out and update all packages via git in {file}`src`, and run buildout to configure the whole thing.

From time to time you can check if some old cruft has accumulated.

```shell
bin/develop status
```

If this prints any lines with a question mark (`?`) in front, you can clean the cruft with the following command.

```shell
bin/develop purge
```

This will remove packages from {file}`src/` which are no longer needed, as they have been replaced by proper egg releases of these packages.
