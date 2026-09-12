---
myst:
  html_meta:
    "description": "Plone container images"
    "property=og:description": "Plone container images"
    "property=og:title": "Plone container images"
    "keywords": "Plone 6, install, installation, docker, containers, Official Images"
---

# Plone container images

## Official images for Plone 6

The Plone community maintains the following official images:

| Image           | Description                                                       |
|-----------------|-------------------------------------------------------------------|
| {doc}`aurora`   | Aurora, the future React frontend of Plone. Requires a Plone backend |
| {doc}`backend`  | Plone backend. Could be used standalone or as a headless CMS      |
| {doc}`frontend` | Plone default frontend written in React. Requires a Plone backend |
| {doc}`zeo`      | ZEO server, a specialized database to be used with Plone backend  |


## Other container images

These images are for historical versions of Plone.
They aren't supported or actively maintained.
Don't use them in production.

| Image           | Description                                                       |
|-----------------|-------------------------------------------------------------------|
| {doc}`historical` | Images for Plone releases from 1.0 to 5.2, for migration and content extraction |

```{toctree}
:maxdepth: 2
:hidden: true

aurora
backend
frontend
zeo
historical
```
