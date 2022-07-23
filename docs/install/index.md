---
html_meta:
  "description": "Install Plone 6"
  "property=og:description": "Install Plone 6"
  "property=og:title": "Install Plone 6"
  "keywords": "Plone 6, install, overview"
---

(install-index-label)=

# Install


(install-index-getting-started-label)=

## Getting started

What do you want to do?

-   Try a demo now.
    -   [Plone 6 with Volto frontend](https://6.demo.plone.org/)
    -   [Plone 5.2.x with Barceloneta frontend](https://demo.plone.org/)
-   [Run Plone in containers](containers/index) (why use containers here.)
-   {doc}`installation-from-packages` (contribute to Plone packages, develop add-ons, or install Plone with full control)


(install-index-choose-installation-method-label)=

## Choose an installation method

```{todo}
Add an explanation for choosing an installation method: container versus installation from packages.
Is there a combination for backend and frontend using a cookiecutter?
```

Developers may choose to install Plone from either [the official container images](containers/index) or [packages](installation-from-packages).

The Plone 6 container images are compliant with the [Open Container Initiative (OCI)](https://opencontainers.org/).
They should work with any OCI-compliant container engine for developing, managing, and running Plone 6 images.
Two popular options include [podman](https://podman.io/) and [Docker](https://www.docker.com/products/docker-desktop/).
The Plone 6 images have all the system requirements, pre-requisites, and Plone 6 already installed, except those requirements needed for running the container engine itself.
This option is the quickest method to install and develop for Plone 6 and its packages.

There may be some cases where using a Plone 6 image is not practical or desired.
You might want to use an SQL database that is not PostgreSQL, or you might use a deployment workflow that has specific requirements.
For these situations, Plone 6 may be installed manually.
This method takes longer.
It might be a challenge if you bump up against system requirements, or need to resolve conflicts between required packages.

```{todo}
Perhaps merge the subsequent section into this section?
```


(install-index-caveat-label)=

## Caveat that Plone is a large project and source installs are non-trivial


(install-index-system-requirements-label)=

## System Requirements

System requirements depend upon your choice of installation method:

-   [Use container images](containers/index)
-   {doc}`installation-from-packages`


```{toctree}
:maxdepth: 2
:hidden: true

containers/index
installation-from-packages
installation-backend-from-packages-step-by-step
```
