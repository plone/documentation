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

images/index
examples/index
recipes/index
```

## Getting started

```{note}
Although there are many container engine tools for developing, managing, and running containers, we will use {term}`Docker` in this documentation.
```


(install-containers-index-system-requirements-label)=

### System requirements

The system requirements include those required by Docker itself.

-   [Linux](https://docs.docker.com/desktop/setup/install/linux/)
-   [macOS](https://docs.docker.com/desktop/setup/install/mac-install/)
-   [Windows](https://docs.docker.com/desktop/setup/install/windows-install/)

Plone 6 itself requires memory and disk space in addition to those of Docker alone.
See its {ref}`create-project-cookieplone-hardware-requirements-label`.


### Install Docker

Install [Docker Desktop](https://docs.docker.com/get-started/get-docker/) for your operating system.

Docker Desktop includes all Docker tools.
{term}`Docker Compose` is one of the Docker tools that will be used in much of this documentation.


### Start Plone

First start the Plone Backend, naming it `plone6-backend` and creating a site with its default configuration, using the following command.

```shell
docker run --name plone6-backend -e SITE=Plone -d -p 8080:8080 plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
```

Now start the Plone Frontend, linking it to the `plone6-backend`:

```shell
docker run --name plone6-frontend --link plone6-backend:backend -e RAZZLE_DEV_PROXY_API_PATH=http://backend:8080/Plone -d -p 3000:3000 plone/plone-frontend:latest
```


## Access your Plone site

Point your browser to `http://localhost:3000` and you should see the new Plone site.

```{note}
The default user is `admin` and the password is `admin`.
```


## Shutdown and cleanup

To stop and clean up the containers use the following commands.

```shell
docker stop plone6-frontend && docker rm plone6-frontend
docker stop plone6-backend && docker rm plone6-backend
```


## Next steps

Get to know the [Official Images](images/index) maintained by the Plone community.

Also see some [examples](examples/index) of how to use the Official Images to bootstrap your projects.
