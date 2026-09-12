---
myst:
  html_meta:
    "description": "Examples of Plone 6 setup with containers"
    "property=og:description": "Examples of Plone 6 setup with containers"
    "property=og:title": "Examples of Plone 6 using containers"
    "keywords": "Plone 6, install, installation, docker, containers"
---

# Examples of Plone 6 using containers

```{toctree}
:maxdepth: 2
:hidden: true

compose/index
swarm/index
```

## Docker Compose

Examples of projects running Plone using `docker compose`.

### Traefik

| Project example | Description |
| --- | --- |
| [`traefik-volto-plone`](compose/traefik-volto-plone) | Stack with Traefik, Frontend, and Backend |
| [`traefik-volto-plone-zeo`](compose/traefik-volto-plone-zeo) | Stack with Traefik, Frontend, Backend, and ZEO server |
| [`traefik-volto-plone-postgresql`](compose/traefik-volto-plone-postgresql) | Stack with Traefik, Frontend, Backend, and PostgreSQL DB |
| [`traefik-plone`](compose/traefik-plone) | Stack with Traefik and Backend (Plone Classic) |
| [`traefik-volto-plone-varnish`](compose/traefik-volto-plone-varnish) | Stack with Traefik, Frontend, Backend, ZEO server, and Varnish |

### nginx

| Project example | Description |
| --- | --- |
| [`nginx-volto-plone`](compose/nginx-volto-plone) | Stack with nginx, Frontend, and Backend |
| [`nginx-volto-plone-zeo`](compose/nginx-volto-plone-zeo) | Stack with nginx, Frontend, Backend, and ZEO server |
| [`nginx-volto-plone-postgresql`](compose/nginx-volto-plone-postgresql) | Stack with nginx, Frontend, Backend, and PostgreSQL DB |
| [`nginx-plone`](compose/nginx-plone) | Stack with nginx and Backend (Plone Classic) |

### HAProxy

| Project example | Description |
| --- | --- |
| [`haproxy-plone-zeo`](compose/haproxy-plone-zeo) | Stack with HAProxy, Backend, and ZEO server |


## Docker Swarm

Examples of stacks running Plone on a Docker Swarm cluster.

| Stack example | Description |
| --- | --- |
| [`traefik-volto-plone`](swarm/traefik-volto-plone) | Stack with Traefik, Frontend, and Backend |
| [`traefik-volto-plone-zeo`](swarm/traefik-volto-plone-zeo) | Stack with Traefik, Frontend, Backend, and ZEO server |
| [`traefik-volto-plone-postgresql`](swarm/traefik-volto-plone-postgresql) | Stack with Traefik, Frontend, Backend, and PostgreSQL DB |
| [`traefik-plone`](swarm/traefik-plone) | Stack with Traefik and Backend (Plone Classic) |
| [`traefik-volto-plone-varnish`](swarm/traefik-volto-plone-varnish) | Stack with Traefik, Frontend, Backend, ZEO server, and Varnish |
