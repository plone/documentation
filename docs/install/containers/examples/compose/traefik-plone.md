---
myst:
  html_meta:
    "description": "Simple Plone 6 Classic UI setup with Traefik and one backend, with data persisted in a Docker volume."
    "property=og:description": "Simple Plone 6 Classic UI setup with Traefik and one backend, with data persisted in a Docker volume."
    "property=og:title": "Traefik, Plone Classic container example"
    "keywords": "Plone 6, Container, Docker, Traefik, Plone Classic"
---

# Traefik, Plone Classic container example

This example is a simple setup with one backend, with data persisted in a Docker volume.

In this example, {term}`Traefik Proxy` routes requests to the backend.


## Setup

Create an empty project directory named `traefik-plone`.

```shell
mkdir traefik-plone
```

Change into your project directory.

```shell
cd traefik-plone
```


### Service configuration with Docker Compose

Create a `docker-compose.yml` file with the following content.
Traefik reads its routing configuration from the labels of the `backend` service, so this example doesn't need a separate proxy configuration file.

```yaml
services:

  traefik:
    image: traefik:{TRAEFIK_VERSION}
    ports:
      - "80:80"
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
    command:
      - --providers.docker
      - --providers.docker.exposedbydefault=false
      - --entrypoints.http.address=:80
      - --accesslog

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
    environment:
      SITE: Plone
      TYPE: classic
    volumes:
      - vol-site-data:/data
    ports:
      - "8080:8080"
    labels:
      - traefik.enable=true
      # Service
      - traefik.http.services.svc-backend.loadbalancer.server.port=8080
      # Middleware: Virtual Host Monster rewrite for the site
      - "traefik.http.middlewares.mw-backend-vhm.replacepathregex.regex=^/(.*)"
      - "traefik.http.middlewares.mw-backend-vhm.replacepathregex.replacement=/VirtualHostBase/http/plone.localhost/Plone/VirtualHostRoot/$$1"
      # Router
      - traefik.http.routers.rt-backend.rule=Host(`plone.localhost`)
      - traefik.http.routers.rt-backend.entrypoints=http
      - traefik.http.routers.rt-backend.service=svc-backend
      - traefik.http.routers.rt-backend.middlewares=mw-backend-vhm

volumes:
  vol-site-data: {}
```

```{note}
Use `http://plone.localhost/` to access the website.
If `plone.localhost` doesn't resolve on your computer, add it to your `/etc/hosts` file, pointing to the IP address of the Docker host.
```


## Build the project

Start the stack with `docker compose`.

```shell
docker compose up -d
```

This pulls the needed images and starts Plone.


## Access Plone in a browser

After startup, go to `http://plone.localhost/` and you should see the site.
You can also open the main Plone control page, where you can create more Plone sites, at `http://localhost:8080`.


## Shutdown and cleanup

The command `docker compose down` removes the containers and default network, but preserves the Plone database.

The command `docker compose down --volumes` removes the containers, default network, and the Plone database.
