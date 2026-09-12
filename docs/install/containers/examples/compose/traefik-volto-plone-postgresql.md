---
myst:
  html_meta:
    "description": "Simple Plone 6 setup with Traefik and one or more backend instances accessing a PostgreSQL server, with data persisted in a Docker volume."
    "property=og:description": "Simple Plone 6 setup with Traefik and one or more backend instances accessing a PostgreSQL server, with data persisted in a Docker volume."
    "property=og:title": "Traefik, Frontend, Backend, PostgreSQL container example"
    "keywords": "Plone 6, Container, Docker, Traefik, Frontend, Backend, PostgreSQL"
---

# Traefik, Frontend, Backend, PostgreSQL container example

This example is a simple setup with one or more backend instances accessing a PostgreSQL server, with data persisted in a Docker volume.

In this example, {term}`Traefik Proxy` routes requests to the frontend and the backend.


## Setup

Create an empty project directory named `traefik-volto-plone-postgresql`.

```shell
mkdir traefik-volto-plone-postgresql
```

Change into your project directory.

```shell
cd traefik-volto-plone-postgresql
```


### Service configuration with Docker Compose

Create a `docker-compose.yml` file with the following content.
Traefik reads its routing configuration from the labels of the `frontend` and `backend` services, so this example doesn't need a separate proxy configuration file.

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

  frontend:
    image: plone/plone-frontend:{PLONE_FRONTEND_VERSION}
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
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
    environment:
      SITE: Plone
      RELSTORAGE_DSN: "dbname='plone' user='plone' host='db' password='plone'"
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
    image: postgres:{POSTGRES_VERSION}
    environment:
      POSTGRES_USER: plone
      POSTGRES_PASSWORD: plone
      POSTGRES_DB: plone
    volumes:
      - vol-site-data:/var/lib/postgresql

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


## Increase the number of backends

To use two containers for the backend, run `docker compose` with `--scale`.

```shell
docker compose up -d --scale backend=2
```

Traefik distributes the requests to the backend among both containers.


## Shutdown and cleanup

The command `docker compose down` removes the containers and default network, but preserves the Plone database.

The command `docker compose down --volumes` removes the containers, default network, and the Plone database.
