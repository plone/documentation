---
html_meta:
  "description": "Install Plone 6"
  "property=og:description": "Install Plone 6"
  "property=og:title": "Install Plone 6"
  "keywords": "Plone 6, install, overview"
---

(install-index-label)=

# Install Plone 6


(install-index-getting-started-label)=

## Getting started

What do you want to do?

-   [Try a demo now](https://6.demo.plone.org/).
-   Run Plone in containers (why use containers here..)
-   Develop Plone add-ons or contribute to Plone packages → Install Plone from source


(install-index-system-requirements-label)=

## System Requirements

To install Plone 6, you must satisfy system requirements.

```{todo}
Add any missing requirements, including disk space.
```

-   2GB if using a container image, 4GB RAM if installing manually.
-   Disk space (TBD).
-   Either a UNIX-like operating system—such as Linux, Ubuntu, macOS—or Windows.
    For Windows, it is a good idea to use [Windows Subsystem for Linux (WSL)](https://docs.microsoft.com/en-us/windows/wsl/).
    We strongly recommend using a recent version of your operating system released within the last 3 years.
    Older systems might not be supported.
-   Python 3.7, 3.8, or 3.9.

Additional requirements might be needed depending on your choice of installation method.


(install-index-choose-installation-method-label)=

### Choose an installation method

Developers may choose to install Plone from either [the official container images](containers/index) or [source](source).

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


```{toctree}
:maxdepth: 2
:hidden: true

containers/index
source
```
