---
myst:
  html_meta:
    "description": "Install Plone 6"
    "property=og:description": "Install Plone 6"
    "property=og:title": "Install Plone 6"
    "keywords": "Plone 6, install, overview"
---

(install-index-label)=

# Install

In this part of the documentation, you can find how to try Plone and how to choose an installation method if you want to develop in Plone.


(install-index-getting-started-label)=

## Getting started

::::{grid} 1 2 2 2
:gutter: 1 1 1 2

:::{grid-item-card} {octicon}`browser;1.5em;sd-mr-1` Try a demo

Choose a version.

-   [Plone 6 with Volto frontend](https://demo.plone.org/)
-   [Plone 6 Classic UI (nightly build)](https://classic.demo.plone.org/login?came_from=/en)
:::

:::{grid-item-card} {octicon}`download;1.5em;sd-mr-1` Install

Developers may choose to install Plone from either [the official container images](containers/index) or [packages](install-from-packages).
+++
Help me [choose an installation method](install-index-choose-installation-method-label).
:::

::::


(install-index-choose-installation-method-label)=

## Choose an installation method

Developers may choose to install Plone from either [the official container images](containers/index) or [packages](install-from-packages).


### Containers

The Plone 6 container images are compliant with the [Open Container Initiative (OCI)](https://opencontainers.org/).
They should work with any OCI-compliant container engine for developing, managing, and running Plone 6 images.
Two popular options include [podman](https://podman.io/) and [Docker](https://www.docker.com/products/docker-desktop/).

The Plone 6 images have all the system requirements, pre-requisites, and Plone 6 already installed, except those requirements needed for running the container engine itself.

This option is the quickest method to install and develop for Plone 6 and its packages.

:::{card}
:link: containers/index
:link-type: any
{octicon}`container;1.5em;sd-mr-1` [Use containers to install Plone](containers/index)
:::


### Packages

There may be some cases where using a Plone 6 image and containers is not practical or desired.

-   You use an SQL database that is not PostgreSQL.
-   You develop custom applications, themes, and add-ons for Plone.
-   You use a deployment workflow that has specific requirements.

For these situations, Plone 6 may be installed from its packages.

It might be a challenge if you bump up against system requirements, or need to resolve conflicts between required packages.

This method takes longer than using containers.

:::{card}
:link: install-from-packages
:link-type: any
{octicon}`package;1.5em;sd-mr-1` [Install Plone from its packages](install-from-packages)
:::


(install-index-system-requirements-label)=

## System Requirements

System requirements depend upon your choice of installation method.

-   [Container system requirements](install-containers-index-system-requirements-label)
-   [Packages system requirements](install-packages-system-requirements-label)


```{toctree}
:maxdepth: 2
:hidden: true

containers/index
install-from-packages
manage-add-ons-packages
```
