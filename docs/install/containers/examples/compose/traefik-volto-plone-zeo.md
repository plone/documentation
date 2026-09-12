---
myst:
  html_meta:
    "description": "Simple Plone 6 setup with Traefik and one or more backend instances accessing a ZEO server, with data persisted in a Docker volume."
    "property=og:description": "Simple Plone 6 setup with Traefik and one or more backend instances accessing a ZEO server, with data persisted in a Docker volume."
    "property=og:title": "Traefik, Frontend, Backend, ZEO container example"
    "keywords": "Plone 6, Container, Docker, Traefik, Frontend, Backend, ZEO"
---

# Traefik, Frontend, Backend, ZEO container example

This example is a simple setup with one or more backend instances accessing a ZEO server, with data persisted in a Docker volume.

In this example, {term}`Traefik Proxy` routes requests to the frontend and the backend.


## Setup

Create an empty project directory named {file}`traefik-volto-plone-zeo`.

```shell
mkdir traefik-volto-plone-zeo
```

Change into your project directory.

```shell
cd traefik-volto-plone-zeo
```


### Service configuration with Docker Compose

Create a {file}`docker-compose.yml` file with the following content.
Traefik reads its routing configuration from the labels of the `frontend` and `backend` services, so this example doesn't need a separate proxy configuration file.

```yaml
services:

  traefik:
    image: traefik:${STACK_TRAEFIK_TAG:?Set STACK_TRAEFIK_TAG}
    ports:
      - "80:80"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command:
      - --providers.docker
      - --providers.docker.exposedbydefault=false
      - --entrypoints.http.address=:80
      - --accesslog

  frontend:
    image: plone/plone-frontend:${STACK_FRONTEND_TAG:?Set STACK_FRONTEND_TAG}
    environment:
      RAZZLE_INTERNAL_API_PATH: http://backend:8080/Plone
    depends_on:
      - backend
    labels:
      - traefik.enable=true
      # Service
      - traefik.http.services.svc-frontend.loadbalancer.server.port=3000
      # Router
      - traefik.http.routers.rt-frontend.rule=Host(`plone.localhost`)
      - traefik.http.routers.rt-frontend.entrypoints=http
      - traefik.http.routers.rt-frontend.service=svc-frontend

  backend:
    image: plone/plone-backend:${STACK_BACKEND_TAG:?Set STACK_BACKEND_TAG}
    environment:
      SITE: Plone
      ZEO_ADDRESS: db:8100
      ZEO_SHARED_BLOB_DIR: on   # otherwise the backend will create its own blob storage
    volumes:
      - vol-site-data:/data     # the backend and database need access to the same volume
    depends_on:
      - db
    labels:
      - traefik.enable=true
      # Service
      - traefik.http.services.svc-backend.loadbalancer.server.port=8080
      # Middleware: Virtual Host Monster rewrite for /++api++/
      - "traefik.http.middlewares.mw-backend-vhm-api.replacepathregex.regex=^/\\+\\+api\\+\\+($$|/.*)"
      - "traefik.http.middlewares.mw-backend-vhm-api.replacepathregex.replacement=/VirtualHostBase/http/plone.localhost/Plone/++api++/VirtualHostRoot$$1"
      # Router
      - traefik.http.routers.rt-backend-api.rule=Host(`plone.localhost`) && PathPrefix(`/++api++`)
      - traefik.http.routers.rt-backend-api.entrypoints=http
      - traefik.http.routers.rt-backend-api.service=svc-backend
      - traefik.http.routers.rt-backend-api.middlewares=mw-backend-vhm-api

  db:
    image: plone/plone-zeo:${STACK_ZEO_TAG:?Set STACK_ZEO_TAG}
    restart: always
    volumes:
      - vol-site-data:/data

volumes:
  vol-site-data: {}
```

```{note}
Use `http://plone.localhost/` to access the website.
If `plone.localhost` doesn't resolve on your computer, add it to your {file}`/etc/hosts` file, pointing to the IP address of the Docker host.
```


### Environment variables

The {file}`docker-compose.yml` file reads the tags of its images from the following environment variables.
All of them are required, and `docker compose` stops with an error if one of them is missing.

| Variable | Description | Default value | Example |
| --- | --- | --- | --- |
| `STACK_FRONTEND_TAG` | Tag (version) of the image for the frontend | | {{PLONE_FRONTEND_VERSION}} |
| `STACK_BACKEND_TAG` | Tag (version) of the image for the backend | | {{PLONE_BACKEND_MINOR_VERSION}} |
| `STACK_ZEO_TAG` | Tag (version) of the image for the ZEO server | | {{PLONE_ZEO_VERSION}} |
| `STACK_TRAEFIK_TAG` | Tag (version) of the image for Traefik | | {{TRAEFIK_VERSION}} |

Create a {file}`.env` file in your project directory with your values.
Docker Compose reads it automatically when you run `docker compose` from that directory.

```shell
STACK_FRONTEND_TAG={PLONE_FRONTEND_VERSION}
STACK_BACKEND_TAG={PLONE_BACKEND_MINOR_VERSION}
STACK_ZEO_TAG={PLONE_ZEO_VERSION}
STACK_TRAEFIK_TAG={TRAEFIK_VERSION}
```


## Build the project

Start the stack with `docker compose`.

```shell
docker compose up -d
```

This pulls the needed images and starts Plone.


## Access Plone in a browser

After startup, go to `http://plone.localhost/` and you should see the site.


## Increase the number of backends

To use two containers for the backend, run `docker compose` with `--scale`.

```shell
docker compose up -d --scale backend=2
```

Traefik distributes the requests to the backend among both containers.


## Shutdown and cleanup

The command `docker compose down` removes the containers and default network, but preserves the Plone database.

The command `docker compose down --volumes` removes the containers, default network, and the Plone database.
