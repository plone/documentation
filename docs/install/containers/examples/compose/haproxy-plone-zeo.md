---
myst:
  html_meta:
    "description": "Simple Plone 6 setup with scalable backend and data being persisted in a ZEO volume."
    "property=og:description": "Simple Plone 6 setup with scalable backend and data being persisted in a ZEO volume."
    "property=og:title": "HAProxy, Backend, ZEO container example"
    "keywords": "Plone 6, Container, Docker, HAProxy, ZEO"
---

# HAProxy, Backend, ZEO container example

This example is a very simple setup with one or more backend instances accessing a ZEO server and data being persisted in a Docker volume.

{term}`HAProxy` is used for load balancing in this example.
We will use the image [`plone/plone-haproxy`](https://github.com/plone/plone-haproxy).


## Setup

Create a directory for your project, and inside it create a {file}`docker-compose.yml` file that starts your Plone instance and the ZEO instance with volume mounts for data persistence.

```yaml
services:

  lb:
    image: plone/plone-haproxy
    depends_on:
    - backend
    ports:
    - "8080:8080"
    - "1936:1936"
    environment:
      FRONTEND_PORT: "8080"
      BACKENDS: "backend"
      BACKENDS_PORT: "8080"
      DNS_ENABLED: "True"
      HTTPCHK: "GET /"
      INTER: "5s"
      LOG_LEVEL: "info"

  backend:
    image: plone/plone-backend:${STACK_BACKEND_TAG:?Set STACK_BACKEND_TAG}
    restart: always
    environment:
      ZEO_ADDRESS: zeo:8100
    ports:
    - "8080"
    depends_on:
      - zeo

  zeo:
    image: plone/plone-zeo:${STACK_ZEO_TAG:?Set STACK_ZEO_TAG}
    restart: always
    volumes:
      - vol-site-data:/data

volumes:
  vol-site-data: {}
```


### Environment variables

The {file}`docker-compose.yml` file reads the tags of its images from the following environment variables.
All of them are required, and `docker compose` stops with an error if one of them is missing.

| Variable | Description | Default value | Example |
| --- | --- | --- | --- |
| `STACK_BACKEND_TAG` | Tag (version) of the image for the backend | | {{PLONE_BACKEND_MINOR_VERSION}} |
| `STACK_ZEO_TAG` | Tag (version) of the image for the ZEO server | | {{PLONE_ZEO_VERSION}} |

Create a {file}`.env` file in your project directory with your values.
Docker Compose reads it automatically when you run `docker compose` from that directory.

```shell
STACK_BACKEND_TAG={PLONE_BACKEND_MINOR_VERSION}
STACK_ZEO_TAG={PLONE_ZEO_VERSION}
```


## Build the project with multiple backends

Run `docker compose up -d --scale backend=4` from your project directory.


## Access Plone via Browser

Point your browser at `http://localhost:8080`.
Login using the username and password combination of `admin` and `admin`.
You should see the default Plone site creation page.


## Access HAProxy Stats Page via Browser

Point your browser at `http://localhost:1936`.
Login using the username and password combination of `admin` and `admin`.
You should see HAProxy statistics for your Plone cluster.


## Shutdown and cleanup

The command `docker compose down` removes the containers and default network, but preserves the Plone database.

The command `docker compose down --volumes` removes the containers, default network, and the Plone database.
