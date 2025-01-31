---
myst:
  html_meta:
    "description": "Examples of Plone setup with containers"
    "property=og:description": "Examples of Plone setup with containers"
    "property=og:title": "Examples of Plone using containers"
    "keywords": "Plone, install, installation, docker, containers"
---

# Examples of Plone using containers

```{toctree}
:maxdepth: 2
:hidden: true

nginx-volto-plone
nginx-volto-plone-zeo
nginx-volto-plone-postgresql
nginx-plone
haproxy-plone-zeo
traefik-volto-plone-varnish
```

Examples of projects running Plone using `docker compose`.

| Project example | Description |
| --- | --- |
| [nginx-volto-plone](nginx-volto-plone) | Stack with nginx, Frontend, and Backend |
| [nginx-volto-plone-zeo](nginx-volto-plone-zeo) | Stack with nginx, Frontend, Backend, and ZEO server |
| [nginx-volto-plone-postgresql](nginx-volto-plone-postgresql) | Stack with nginx, Frontend, Backend, and PostgreSQL DB |
| [nginx-plone](nginx-plone) | Stack with nginx and Backend (Plone Classic) |
| [haproxy-plone-zeo](haproxy-plone-zeo) | Stack with HAProxy, Backend, and ZEO server |
| [traefik-volto-plone-varnish](traefik-volto-plone-varnish) | Stack with traefik, Frontend, Backend, Varnish |
