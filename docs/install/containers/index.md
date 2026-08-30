---
myst:
  html_meta:
    "description": "Using Plone 6 with containers"
    "property=og:description": "Using Plone 6 with containers"
    "property=og:title": "Containers"
    "keywords": "Plone 6, install, installation, Docker, containers"
---

(install-containers-label)=

# Containers

## Introduction

The Plone 6 images have all the system requirements, prerequisites, and Plone 6 already installed, except those requirements needed for running the container engine itself.

Using containers is the easiest way to deploy Plone 6.
You may also use containers when {doc}`creating a Plone project </install/create-project-cookieplone>`.

The Plone 6 container images are compliant with the [Open Container Initiative (OCI)](https://opencontainers.org/).
They should work with any OCI-compliant container engine for developing, managing, and running Plone 6 images.
Two popular options include [podman](https://podman.io/) and [Docker](https://www.docker.com/products/docker-desktop/).

## Resources

The community provides {doc}`images/index` that you can use for standalone Plone installations.
These images support a variety of installation options.
You can choose from Volto or Classic UI for a frontend, or specialized databases using ZEO or a relational database.

The {doc}`examples/index` and {doc}`recipes/index` provide configuration for proxy servers, load balancers, and caching services.

```{toctree}
:maxdepth: 2
:hidden:

getting-started
images/index
examples/index
recipes/index
```

For step-by-step instructions on getting started with containers, see {doc}`getting-started`.
