---
myst:
  html_meta:
    "description": "Plone 6 Classic UI stack for Docker Swarm with Traefik and a backend that stores its data in a Docker volume."
    "property=og:description": "Plone 6 Classic UI stack for Docker Swarm with Traefik and a backend that stores its data in a Docker volume."
    "property=og:title": "Docker Swarm: Traefik, Plone Classic example"
    "keywords": "Plone 6, Container, Docker, Docker Swarm, Traefik, Plone Classic"
---

# Docker Swarm: Traefik, Plone Classic example

This example deploys a Plone 6 site with the Classic UI as a stack on a Docker Swarm cluster.
The stack runs the following services.

`traefik`
:   {term}`Traefik Proxy` routes requests to the backend, and gets TLS certificates from Let's Encrypt.

`socket-proxy`
:   Gives Traefik access to the parts of the Docker API it needs, instead of the Docker socket itself.

`backend`
:   The Plone backend with the Classic UI, with its data persisted in a Docker volume.


## Prerequisites

-   A Docker Swarm cluster.
    To create a cluster with a single node, run `docker swarm init` on that node.
-   DNS records that point the host names of `STACK_HOSTNAME`, `STACK_HOSTNAME_REDIRECT`, and `TRAEFIK_HOSTNAME` to your cluster.
-   Ports 80 and 443 open to the internet, so Let's Encrypt can validate your host names.


## Setup

Create an empty project directory named {file}`swarm-traefik-plone`.

```shell
mkdir swarm-traefik-plone
```

Change into your project directory.

```shell
cd swarm-traefik-plone
```


### Create the public network

Traefik and the services it routes requests to share an overlay network named `nw-public`.
Create it once on a manager node, before you deploy the stack.

```shell
docker network create --driver overlay nw-public
```


### Stack file

Create a {file}`stack.yml` file with the following content.

```yaml
services:

  socket-proxy:
    image: tecnativa/docker-socket-proxy
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      NODES: 1
      SERVICES: 1
      TASKS: 1
      NETWORKS: 1
    networks:
      - nw-traefik
    deploy:
      placement:
        constraints:
          - node.role == manager

  traefik:
    image: traefik:${STACK_TRAEFIK_TAG:?Set STACK_TRAEFIK_TAG}
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - vol-traefik-certs:/certificates
    command:
      - --providers.swarm
      - --providers.swarm.endpoint=tcp://socket-proxy:2375
      - --providers.swarm.exposedbydefault=false
      - --providers.swarm.network=nw-public
      - --providers.swarm.constraints=Label(`traefik.constraint-label`, `public`)
      - --entrypoints.http.address=:80
      - --entrypoints.https.address=:443
      - --certificatesresolvers.le.acme.email=${TRAEFIK_EMAIL:?Set TRAEFIK_EMAIL}
      - --certificatesresolvers.le.acme.storage=/certificates/acme.json
      - --certificatesresolvers.le.acme.tlschallenge=true
      - --accesslog
      - --accesslog.format=json
      - --log.level=INFO
      - --log.format=json
      - --api
    networks:
      - nw-public
      - nw-traefik
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        - traefik.http.services.traefik-public.loadbalancer.server.port=8000

        # Dashboard
        - traefik.http.middlewares.admin-auth.basicauth.users=${TRAEFIK_BASIC_AUTH:?Set TRAEFIK_BASIC_AUTH}
        - traefik.http.routers.traefik-dashboard.rule=Host(`${TRAEFIK_HOSTNAME:?Set TRAEFIK_HOSTNAME}`)
        - traefik.http.routers.traefik-dashboard.entrypoints=https
        - traefik.http.routers.traefik-dashboard.tls=true
        - traefik.http.routers.traefik-dashboard.tls.certresolver=le
        - traefik.http.routers.traefik-dashboard.service=api@internal
        - traefik.http.routers.traefik-dashboard.middlewares=admin-auth

        # Generic middlewares
        - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
        - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
        - traefik.http.middlewares.gzip.compress=true
        - traefik.http.middlewares.gzip.compress.excludedcontenttypes=image/png, image/jpeg, font/woff2

        # Redirect every HTTP request to HTTPS
        - traefik.http.routers.generic-https-redirect.entrypoints=http
        - traefik.http.routers.generic-https-redirect.rule=HostRegexp(`^.+$$`)
        - traefik.http.routers.generic-https-redirect.priority=1
        - traefik.http.routers.generic-https-redirect.middlewares=https-redirect

  backend:
    image: plone/plone-backend:${STACK_BACKEND_TAG:?Set STACK_BACKEND_TAG}
    environment:
      SITE: Plone
      TYPE: classic
    volumes:
      - vol-site-data:/data
    networks:
      - nw-public
    deploy:
      replicas: 1
      update_config:
        parallelism: 1
        delay: 5s
        order: stop-first   # only one process can open the database
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        # Service
        - traefik.http.services.svc-${STACK_NAME:?Set STACK_NAME}-backend.loadbalancer.server.port=8080

        # Middlewares
        ## Redirect
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.permanent=true
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.regex=^https://${STACK_HOSTNAME_REDIRECT:?Set STACK_HOSTNAME_REDIRECT}/(.*)
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.replacement=https://${STACK_HOSTNAME:?Set STACK_HOSTNAME}/$${1}
        ## Virtual Host Monster rewrite for the site
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm.replacepathregex.regex=^/(.*)"
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm.replacepathregex.replacement=/VirtualHostBase/https/${STACK_HOSTNAME}/Plone/VirtualHostRoot/$$1"

        # Routers
        ## Redirect
        - traefik.http.routers.rt-${STACK_NAME}-backend-redirect.rule=Host(`${STACK_HOSTNAME_REDIRECT}`)
        - traefik.http.routers.rt-${STACK_NAME}-backend-redirect.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-backend-redirect.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-backend-redirect.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-backend-redirect.middlewares=mw-${STACK_NAME}-redirect
        ## /
        - traefik.http.routers.rt-${STACK_NAME}-backend.rule=Host(`${STACK_HOSTNAME}`)
        - traefik.http.routers.rt-${STACK_NAME}-backend.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-backend.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-backend.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-backend.service=svc-${STACK_NAME}-backend
        - traefik.http.routers.rt-${STACK_NAME}-backend.middlewares=gzip,mw-${STACK_NAME}-backend-vhm

volumes:
  vol-traefik-certs: {}
  vol-site-data: {}

networks:
  nw-public:
    external: true
  nw-traefik:
    driver: overlay
    internal: true
```

```{warning}
The backend stores its data in a Docker volume, and only one backend process can open that data at a time.
Keep the `backend` service at one replica.

Docker volumes are also local to the node where they're created.
In a cluster with more than one node, add a placement constraint to the `backend` service, so it always runs on the node that holds its data.
```


### Environment variables

The stack reads its configuration from the following environment variables.
All of them are required, and `docker stack deploy` stops with an error if one of them is missing.

| Variable | Description | Default value | Example |
| --- | --- | --- | --- |
| `STACK_NAME` | Name of the stack, which must match the name you pass to `docker stack deploy`. Traefik uses it to name routers, services, and middleware. | | `plone` |
| `STACK_HOSTNAME` | Public host name of the site | | `www.example.com` |
| `STACK_HOSTNAME_REDIRECT` | Host name that permanently redirects to `STACK_HOSTNAME` | | `example.com` |
| `STACK_BACKEND_TAG` | Tag (version) of the image for the backend | | {{PLONE_BACKEND_MINOR_VERSION}} |
| `STACK_TRAEFIK_TAG` | Tag (version) of the image for Traefik | | {{TRAEFIK_VERSION}} |
| `TRAEFIK_HOSTNAME` | Host name of the Traefik dashboard | | `traefik.example.com` |
| `TRAEFIK_EMAIL` | Email address of your Let's Encrypt account | | `admin@example.com` |
| `TRAEFIK_BASIC_AUTH` | User name and password hash for the Traefik dashboard, in the format `user:hash` | | `admin:$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0` |

To create a password hash, run the following command, with your password instead of `secret`.

```shell
openssl passwd -apr1 secret
```

Create a {file}`.env` file with your values.
Wrap values that contain a dollar sign, such as password hashes, in single quotes.

```shell
STACK_NAME=plone
STACK_HOSTNAME=www.example.com
STACK_HOSTNAME_REDIRECT=example.com
STACK_BACKEND_TAG={PLONE_BACKEND_MINOR_VERSION}
STACK_TRAEFIK_TAG={TRAEFIK_VERSION}
TRAEFIK_HOSTNAME=traefik.example.com
TRAEFIK_EMAIL=admin@example.com
TRAEFIK_BASIC_AUTH='admin:$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0'
```

`docker stack deploy` doesn't read {file}`.env` files.
Load the variables into your shell before you deploy.

```shell
set -a
. ./.env
set +a
```


## Deploy the stack

Deploy the stack with the name from `STACK_NAME`.

```shell
docker stack deploy -c stack.yml "$STACK_NAME"
```

This pulls the needed images and starts Plone.


## Access Plone

After startup, go to `https://www.example.com`, using your value of `STACK_HOSTNAME`, and you should see the site.

Unlike the {doc}`Docker Compose example <../compose/traefik-plone>`, this stack doesn't publish port 8080 of the backend, so the page to create more Plone sites isn't reachable.

The Traefik dashboard is available at the host name from `TRAEFIK_HOSTNAME`, behind the user name and password from `TRAEFIK_BASIC_AUTH`.


## Shutdown and cleanup

The command `docker stack rm "$STACK_NAME"` removes the services and the stack networks, but preserves the Plone database and the TLS certificates in their volumes.
