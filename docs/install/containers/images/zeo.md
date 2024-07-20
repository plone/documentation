---
myst:
  html_meta:
    "description": "Using plone/plone-zeo image"
    "property=og:description": "Using plone/plone-zeo image"
    "property=og:title": "Plone ZEO image"
    "keywords": "Plone 6, install, installation, docker, containers, plone/plone-zeo"
---

# `plone/plone-zeo`

A ZEO Server [Docker](https://www.docker.com/) image using Python 3 and [pip](https://pip.pypa.io/en/stable/).


## Using this image


### Simple usage

Run a container exposing port 8100:

```shell
docker run -p 8100:8100 plone/plone-zeo:latest
```


### Service configuration with Docker Compose

Create a directory for your project, and inside it create a `docker-compose.yml` file that starts your Plone instance and the ZEO instance with volume mounts for data persistence:

```yaml
version: "3"
services:

  backend:
    image: plone/plone-backend:latest
    environment:
      ZEO_ADDRESS: zeo:8100
    ports:
    - "8080:8080"
    depends_on:
      - zeo

  zeo:
    image: plone/plone-zeo:latest
    volumes:
      - data:/data
    ports:
    - "8100:8100"

volumes:
  data: {}
```

Now, run `docker compose up -d` from your project directory.

Point your browser at http://localhost:8080 and you should see the default Plone site creation page.


### Persistent data

There are several ways to store data used by applications that run in Docker containers.

We encourage users of the `Plone` images to familiarize themselves with the options available.

[The Docker documentation](https://docs.docker.com/) is a good starting point for understanding the different storage options and variations.


## Configuration


### Main variables

| Environment variable | ZEO option | Default value |
| --- | --- | --- |
| `ZEO_PORT` | `address` | `8100` |
| `ZEO_READ_ONLY` | `read-only` | `false` |
| `ZEO_INVALIDATION_QUEUE_SIZE` | `invalidation-queue-size` | `100` |
| `ZEO_PACK_KEEP_OLD` | `pack-keep-old` | `true` |

In case you need to configure an option not present in the environment variables, we suggest you to create a new image based on the default one:

```Dockerfile
FROM plone/plone-zeo:latest

COPY mylocalconfig /app/etc/zeo.conf
```
And then build the new image and start the container.


## Versions

For a complete list of tags and versions, visit the [`plone/plone-zeo` page on Docker Hub](https://hub.docker.com/r/plone/plone-zeo).


## Contribute

- [Issue Tracker](https://github.com/plone/plone-zeo/issues)
- [Source Code](https://github.com/plone/plone-zeo/)
- [Documentation](https://github.com/plone/plone-zeo/)
