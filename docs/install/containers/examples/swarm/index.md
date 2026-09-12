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

traefik-volto-plone
traefik-volto-plone-zeo
traefik-volto-plone-postgresql
traefik-plone
traefik-volto-plone-varnish
```

Examples of stacks for running Plone with `docker swarm`.

| Stack example | Description |
| --- | --- |
| [`traefik-volto-plone`](traefik-volto-plone) | Stack with Traefik, Frontend, and Backend |
| [`traefik-volto-plone-zeo`](traefik-volto-plone-zeo) | Stack with Traefik, Frontend, Backend, and ZEO server |
| [`traefik-volto-plone-postgresql`](traefik-volto-plone-postgresql) | Stack with Traefik, Frontend, Backend, and PostgreSQL DB |
| [`traefik-plone`](traefik-plone) | Stack with Traefik and Backend (Plone Classic) |
| [`traefik-volto-plone-varnish`](traefik-volto-plone-varnish) | Stack with Traefik, Frontend, Backend, ZEO server, and Varnish |
