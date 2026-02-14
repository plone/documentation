---
myst:
  html_meta:
    "description": "Reference for plone/plone-zeo image environment variables"
    "property=og:description": "Reference for plone/plone-zeo image environment variables"
    "property=og:title": "Plone ZEO image - Environment Variables Reference"
    "keywords": "Plone 6, install, installation, docker, containers, plone/plone-zeo, reference, environment variables"
---

# `plone/plone-zeo` - Environment Variables Reference

This reference document covers all environment variables available for the ZEO Server [Docker](https://www.docker.com/) image.

For usage instructions and examples, see {doc}`zeo`.


## Main variables

| Environment variable | ZEO option | Default value |
| --- | --- | --- |
| `ZEO_PORT` | `address` | `8100` |
| `ZEO_READ_ONLY` | `read-only` | `false` |
| `ZEO_INVALIDATION_QUEUE_SIZE` | `invalidation-queue-size` | `100` |
| `ZEO_PACK_KEEP_OLD` | `pack-keep-old` | `true` |

