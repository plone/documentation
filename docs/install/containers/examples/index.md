---
myst:
  html_meta:
    "description": "Examples of Plone 6 setup with containers"
    "property=og:description": "Examples of Plone 6 setup with containers"
    "property=og:title": "Examples of Plone 6 using containers"
    "keywords": "Plone 6, install, installation, docker, containers"
---

# Examples of Plone 6 using containers

This section provides examples of how to use Plone 6 with container orchestration tools and various deployment configurations.

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

## Container orchestration

Plone 6 can be deployed using various container orchestration tools:

### Docker Compose

Most examples in this section use {term}`Docker Compose` for orchestrating multiple containers.
Docker Compose is ideal for development, testing, and small to medium deployments.

All the examples below use `docker compose` (or `docker-compose` in older versions) to manage multi-container setups.

### Docker Swarm

For production deployments requiring high availability and scaling, you can use Docker Swarm mode.
Docker Swarm provides native clustering capabilities for Docker containers, allowing you to:

- Deploy services across multiple nodes
- Scale services up or down
- Manage rolling updates
- Provide service discovery and load balancing

To use Docker Swarm with Plone, you can convert `docker-compose.yml` files to Docker Swarm stack files.
The basic structure remains similar, but you may need to adjust networking and volume configurations for multi-node deployments.

```{seealso}
For more information about production orchestration with Docker Swarm, see {doc}`/deployment/orchestration`.
```

### Other orchestration tools

Plone 6 container images are OCI-compliant and can be used with other orchestration platforms:

- **Kubernetes**: For large-scale, production deployments with advanced features like auto-scaling, self-healing, and service mesh integration
- **Podman Compose**: An alternative to Docker Compose that works with Podman
- **Nomad**: HashiCorp's container orchestration platform

The examples provided here focus on Docker Compose, but the concepts can be adapted to other orchestration tools.

## Example configurations

Examples of projects running Plone using `docker compose`:

| Project example | Description |
| --- | --- |
| [nginx-volto-plone](nginx-volto-plone) | Stack with nginx, Frontend, and Backend |
| [nginx-volto-plone-zeo](nginx-volto-plone-zeo) | Stack with nginx, Frontend, Backend, and ZEO server |
| [nginx-volto-plone-postgresql](nginx-volto-plone-postgresql) | Stack with nginx, Frontend, Backend, and PostgreSQL DB |
| [nginx-plone](nginx-plone) | Stack with nginx and Backend (Plone Classic) |
| [haproxy-plone-zeo](haproxy-plone-zeo) | Stack with HAProxy, Backend, and ZEO server |
| [traefik-volto-plone-varnish](traefik-volto-plone-varnish) | Stack with traefik, Frontend, Backend, Varnish |
