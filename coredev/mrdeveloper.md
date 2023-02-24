---
myst:
  html_meta:
    "description": "mr.developer"
    "property=og:description": "mr.developer"
    "property=og:title": "mr.developer"
    "keywords": "mr.developer"
---

# `mr.developer`

This buildout uses `mr.developer` to manage package development.
See https://pypi.org/project/mr.developer/ for more information, or run `bin/develop help` for a list of available commands.

The most common workflow to get all the latest updates is:

```shell
git pull
bin/develop rb
```

This will get you the latest `coredev` configuration, checkout and update all packages via git and Subversion in src, and run buildout to configure the whole thing.

From time to time you can check if some old cruft has accumulated:

```shell
bin/develop st
```

If this prints any lines with a question mark in front, you can cleanup by:

```shell
bin/develop purge
```

This will remove packages from {file}`src/` which are no longer needed, as they have been replaced by proper egg releases of these packages.
