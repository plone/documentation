---
myst:
  html_meta:
    "description": "Plone 6 stack for Docker Swarm with Traefik, a scalable frontend and backend, and a PostgreSQL database."
    "property=og:description": "Plone 6 stack for Docker Swarm with Traefik, a scalable frontend and backend, and a PostgreSQL database."
    "property=og:title": "Docker Swarm: Traefik, Frontend, Backend, PostgreSQL example"
    "keywords": "Plone 6, Container, Docker, Docker Swarm, Traefik, Frontend, Backend, PostgreSQL"
---

# Docker Swarm: Traefik, Frontend, Backend, PostgreSQL example

This example deploys Plone 6 as a stack on a Docker Swarm cluster.
The stack runs the following services.

`traefik`
:   {term}`Traefik Proxy` routes requests to the other services, and gets TLS certificates from Let's Encrypt.

`socket-proxy`
:   Gives Traefik access to the parts of the Docker API it needs, instead of the Docker socket itself.

`frontend`
:   The Plone frontend, with two replicas by default.

`backend`
:   The Plone backend, with two replicas by default, which stores its data in PostgreSQL.

`db`
:   The PostgreSQL database, with its data persisted in a Docker volume.


## Prerequisites

-   A Docker Swarm cluster.
    To create a cluster with a single node, run `docker swarm init` on that node.
-   DNS records that point the host names of `STACK_HOSTNAME`, `STACK_HOSTNAME_REDIRECT`, and `TRAEFIK_HOSTNAME` to your cluster.
-   Ports 80 and 443 open to the internet, so Let's Encrypt can validate your host names.


## Setup

Create an empty project directory named {file}`swarm-traefik-volto-plone-postgresql`.

```shell
mkdir swarm-traefik-volto-plone-postgresql
```

Change into your project directory.

```shell
cd swarm-traefik-volto-plone-postgresql
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

  frontend:
    image: plone/plone-frontend:${STACK_FRONTEND_TAG:?Set STACK_FRONTEND_TAG}
    environment:
      RAZZLE_INTERNAL_API_PATH: http://${STACK_NAME:?Set STACK_NAME}_backend:8080/Plone
      RAZZLE_API_PATH: https://${STACK_HOSTNAME:?Set STACK_HOSTNAME}
    networks:
      - nw-public
      - nw-internal
    deploy:
      replicas: ${STACK_FRONTEND_REPLICAS:-2}
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        # Service
        - traefik.http.services.svc-${STACK_NAME}-frontend.loadbalancer.server.port=3000

        # Middleware
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.permanent=true
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.regex=^https://${STACK_HOSTNAME_REDIRECT:?Set STACK_HOSTNAME_REDIRECT}/(.*)
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.replacement=https://${STACK_HOSTNAME}/$${1}

        # Routers
        ## Redirect
        - traefik.http.routers.rt-${STACK_NAME}-frontend-redirect.rule=Host(`${STACK_HOSTNAME_REDIRECT}`)
        - traefik.http.routers.rt-${STACK_NAME}-frontend-redirect.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-frontend-redirect.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-frontend-redirect.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-frontend-redirect.middlewares=mw-${STACK_NAME}-redirect
        ## /
        - traefik.http.routers.rt-${STACK_NAME}-frontend.rule=Host(`${STACK_HOSTNAME}`)
        - traefik.http.routers.rt-${STACK_NAME}-frontend.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-frontend.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-frontend.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-frontend.service=svc-${STACK_NAME}-frontend
        - traefik.http.routers.rt-${STACK_NAME}-frontend.middlewares=gzip

  backend:
    image: plone/plone-backend:${STACK_BACKEND_TAG:?Set STACK_BACKEND_TAG}
    environment:
      SITE: Plone
      RELSTORAGE_DSN: "dbname='${DB_NAME:-plone}' user='${DB_USER:-plone}' host='${STACK_NAME}_db' password='${DB_PASSWORD:?Set DB_PASSWORD}'"
    networks:
      - nw-public
      - nw-internal
    deploy:
      replicas: ${STACK_BACKEND_REPLICAS:-2}
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        # Service
        - traefik.http.services.svc-${STACK_NAME}-backend.loadbalancer.server.port=8080

        # Middlewares
        ## Virtual Host Monster rewrite for /++api++/
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-api.replacepathregex.regex=^/\\+\\+api\\+\\+($$|/.*)"
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-api.replacepathregex.replacement=/VirtualHostBase/https/${STACK_HOSTNAME}/Plone/++api++/VirtualHostRoot$$1"
        ## Virtual Host Monster rewrite for /ClassicUI/
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-classic.replacepathregex.regex=^/ClassicUI($$|/.*)"
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-classic.replacepathregex.replacement=/VirtualHostBase/https/${STACK_HOSTNAME}/Plone/VirtualHostRoot/_vh_ClassicUI$$1"
        ## Basic authentication for /ClassicUI/
        - traefik.http.middlewares.mw-${STACK_NAME}-backend-auth.basicauth.users=${BASIC_AUTH_USER:?Set BASIC_AUTH_USER}:${BASIC_AUTH_PASSWORD_HASH:?Set BASIC_AUTH_PASSWORD_HASH}

        # Routers
        ## /++api++
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.rule=Host(`${STACK_HOSTNAME}`) && PathPrefix(`/++api++`)
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.service=svc-${STACK_NAME}-backend
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.middlewares=gzip,mw-${STACK_NAME}-backend-vhm-api
        ## /ClassicUI
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.rule=Host(`${STACK_HOSTNAME}`) && PathPrefix(`/ClassicUI`)
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.service=svc-${STACK_NAME}-backend
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.middlewares=gzip,mw-${STACK_NAME}-backend-auth,mw-${STACK_NAME}-backend-vhm-classic

  db:
    image: postgres:${STACK_POSTGRES_TAG:?Set STACK_POSTGRES_TAG}
    environment:
      POSTGRES_USER: ${DB_USER:-plone}
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_DB: ${DB_NAME:-plone}
    volumes:
      - vol-site-data:/var/lib/postgresql
    networks:
      - nw-internal
    deploy:
      replicas: 1
      update_config:
        parallelism: 1
        delay: 1s
        order: stop-first

volumes:
  vol-traefik-certs: {}
  vol-site-data: {}

networks:
  nw-public:
    external: true
  nw-traefik:
    driver: overlay
    internal: true
  nw-internal:
    driver: overlay
    internal: true
```

```{warning}
Docker volumes are local to the node where they're created.
In a cluster with more than one node, add a placement constraint to the `db` service, so the database always runs on the node that holds its data.
```


### Environment variables

The stack reads its configuration from the following environment variables.
Variables without a default value are required, and `docker stack deploy` stops with an error if one of them is missing.

| Variable | Description | Default value | Example |
| --- | --- | --- | --- |
| `STACK_NAME` | Name of the stack, which must match the name you pass to `docker stack deploy`. The services use it to reach each other, and Traefik uses it to name routers, services, and middleware. | | `plone` |
| `STACK_HOSTNAME` | Public host name of the site | | `www.example.com` |
| `STACK_HOSTNAME_REDIRECT` | Host name that permanently redirects to `STACK_HOSTNAME` | | `example.com` |
| `STACK_FRONTEND_REPLICAS` | Number of frontend replicas | `2` | `3` |
| `STACK_BACKEND_REPLICAS` | Number of backend replicas | `2` | `4` |
| `STACK_FRONTEND_TAG` | Tag (version) of the image for the frontend | | {{PLONE_FRONTEND_VERSION}} |
| `STACK_BACKEND_TAG` | Tag (version) of the image for the backend | | {{PLONE_BACKEND_MINOR_VERSION}} |
| `STACK_POSTGRES_TAG` | Tag (version) of the image for PostgreSQL | | {{POSTGRES_VERSION}} |
| `STACK_TRAEFIK_TAG` | Tag (version) of the image for Traefik | | {{TRAEFIK_VERSION}} |
| `TRAEFIK_HOSTNAME` | Host name of the Traefik dashboard | | `traefik.example.com` |
| `TRAEFIK_EMAIL` | Email address of your Let's Encrypt account | | `admin@example.com` |
| `TRAEFIK_BASIC_AUTH` | User name and password hash for the Traefik dashboard, in the format `user:hash` | | `admin:$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0` |
| `BASIC_AUTH_USER` | User name for the Classic UI at `/ClassicUI` | | `admin` |
| `BASIC_AUTH_PASSWORD_HASH` | Password hash for the Classic UI at `/ClassicUI` | | `$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0` |
| `DB_NAME` | Name of the PostgreSQL database | `plone` | `plone` |
| `DB_USER` | Name of the PostgreSQL user | `plone` | `plone` |
| `DB_PASSWORD` | Password of the PostgreSQL user | | `Correct-Horse-Battery-Staple` |

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
STACK_FRONTEND_TAG={PLONE_FRONTEND_VERSION}
STACK_BACKEND_TAG={PLONE_BACKEND_MINOR_VERSION}
STACK_POSTGRES_TAG={POSTGRES_VERSION}
STACK_TRAEFIK_TAG={TRAEFIK_VERSION}
TRAEFIK_HOSTNAME=traefik.example.com
TRAEFIK_EMAIL=admin@example.com
TRAEFIK_BASIC_AUTH='admin:$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0'
BASIC_AUTH_USER=admin
BASIC_AUTH_PASSWORD_HASH='$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0'
DB_PASSWORD=Correct-Horse-Battery-Staple
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

The Classic UI is available at `https://www.example.com/ClassicUI`, behind the user name and password from `BASIC_AUTH_USER` and `BASIC_AUTH_PASSWORD_HASH`.

The Traefik dashboard is available at the host name from `TRAEFIK_HOSTNAME`, behind the user name and password from `TRAEFIK_BASIC_AUTH`.


## Increase the number of backends

To run four backend replicas, scale the backend service.

```shell
docker service scale "${STACK_NAME}_backend=4"
```

The next `docker stack deploy` sets the number of replicas back to the value of `STACK_BACKEND_REPLICAS`.


## Shutdown and cleanup

The command `docker stack rm "$STACK_NAME"` removes the services and the stack networks, but preserves the Plone database and the TLS certificates in their volumes.
