---
myst:
  html_meta:
    "description": "Using the plone/aurora image"
    "property=og:description": "Using the plone/aurora image"
    "property=og:title": "Plone Aurora image"
    "keywords": "Plone 6, install, installation, docker, containers, Aurora, frontend, plone/aurora"
---

# `plone/aurora`

This chapter covers the container images for [Aurora](https://github.com/plone/aurora), the future React frontend of Plone.
Aurora requires a Plone backend to be running and accessible.

% TODO: Remove this admonition when Aurora has a final release.

```{important}
Aurora has not reached a final release yet.
Evaluate it before you use it in production.
```


## Using this image


### Simple usage

Create a network, and start a Plone backend with a site named `Plone` on it.

```shell
docker network create plone
docker run -d --name backend --network plone -e SITE=Plone plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
```

Start Aurora on the same network, and point it at the backend.

```shell
docker run -d --name aurora --network plone -p 3000:3000 -e PLONE_API_PATH=http://backend:8080/Plone plone/aurora:latest
```

Then point your browser at `http://localhost:3000`.

If your Plone backend runs on your computer instead of in a container, use `host.docker.internal` to reach it from the Aurora container.

```shell
docker run -d --name aurora -p 3000:3000 -e PLONE_API_PATH=http://host.docker.internal:8080/Plone plone/aurora:latest
```

% TODO: Confirm whether Linux hosts need `--add-host=host.docker.internal:host-gateway` for this example.


### Service configuration with Docker Compose

Create a directory for your project, and inside it create a {file}`docker-compose.yml` file with the following content.

```yaml
services:

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
    environment:
      SITE: Plone
    volumes:
      - data:/data

  frontend:
    image: plone/aurora:latest
    environment:
      PLONE_API_PATH: http://backend:8080/Plone
    ports:
      - "3000:3000"
    depends_on:
      - backend

volumes:
  data: {}
```

Now run `docker compose up -d` from your project directory.

Point your browser at `http://localhost:3000`, and you should see your Plone site.
Until the backend finishes starting, Aurora returns an error page.

The [{file}`examples` directory of the `plone/container-aurora` repository](https://github.com/plone/container-aurora/tree/main/examples) contains more complete configurations, with a web server in front of Aurora, and with ZEO or PostgreSQL as the database.


## Configuration variables

| Environment variable | Description | Default value |
| --- | --- | --- |
| `PLONE_API_PATH` | Address of the Plone site that Aurora uses as its backend | `http://localhost:8080/Plone` |
| `COOKIE_SECRET` | Secret that signs the authentication cookie | `default` |
| `PORT` | Port where Aurora listens | `3000` |
| `HOST` | Network address where Aurora listens | All network interfaces |

Always set `COOKIE_SECRET` to a long, random value in production.
Without it, Aurora signs the authentication cookie with a publicly known value, and logs a warning at startup.

Aurora runs in production mode, and marks its authentication cookie as secure.
Serve Aurora over HTTPS, so browsers keep the login session.


## Images

Each Aurora release publishes the following images, for the `linux/amd64` and `linux/arm64` platforms.

| Image | Description |
| --- | --- |
| `plone/aurora` | Aurora, ready to run in production |
| `plone/aurora-builder` | An Aurora project with its dependencies installed, used to build images |
| `plone/aurora-dev` | The Aurora development server, which also exposes Storybook on port 6006 |
| `plone/aurora-prod-config` | A minimal Node.js runtime, used as the base of production images |


## Extending from this image

The `plone/aurora` image is built in two stages.
The first stage builds Aurora in `plone/aurora-builder`, and the second copies the result onto `plone/aurora-prod-config`.
Use the same structure to build your own image.

In a directory, create a {file}`Dockerfile` file.

```Dockerfile
# syntax=docker/dockerfile:1
FROM plone/aurora-builder:latest AS builder

RUN <<EOT
    set -e
    pnpm build
    rm -rf node_modules
    pnpm install --prod
EOT

FROM plone/aurora-prod-config:latest

COPY --from=builder /app/ /app/

RUN corepack install
```

Build your new image.

```shell
docker build . -t myaurora:latest -f Dockerfile
```

% TODO: Document how to add your own add-ons to the image.


## Versions

Each release publishes a tag with its version, such as `1.0.0-alpha.7`, and updates the `latest` tag.
For a complete list of tags and versions, visit the [`plone/aurora` page on Docker Hub](https://hub.docker.com/r/plone/aurora).


## Contribute

- [Issue Tracker](https://github.com/plone/container-aurora/issues)
- [Source Code](https://github.com/plone/container-aurora/)
- [Aurora source code](https://github.com/plone/aurora/)
