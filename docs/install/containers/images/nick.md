---
myst:
  html_meta:
    "description": "Using the plone/nick image"
    "property=og:description": "Using the plone/nick image"
    "property=og:title": "Plone Nick image"
    "keywords": "Plone 6, install, installation, docker, containers, Nick, REST API, plone/nick"
---

# `plone/nick`

This chapter covers the official container image for [Nick](https://nick.docs.plone.org), the Nearly Headless CMS that serves the Plone REST API.
The image source is in the [`plone/container-nick`](https://github.com/plone/container-nick) repository.
Nick needs a PostgreSQL database.


## Tags

Each Nick release publishes an image tagged with its version, such as `plone/nick:3.0.0`, for the `linux/amd64` and `linux/arm64` platforms.
The moving tags point to the newest release they cover:

- `3.0` points to the newest 3.0.x release.
- `3` points to the newest 3.x release.
- `latest` points to the version in the {file}`version.txt` file of the repository.

A prerelease, such as `3.1.0-alpha.1`, gets only its own tag.
It does not move `latest`, `3`, or `3.0`.

Published images are rebuilt in place, so a tag such as `plone/nick:3.0.0` can point to a new build of the same version.
To run one exact build, pin its image digest.
Read the digest of a tag from the registry:

```shell
docker buildx imagetools inspect plone/nick:3.0.0 --format '{{.Manifest.Digest}}'
```

Then use the digest in place of the tag, as `plone/nick@sha256:<digest>`.


## Usage

This section describes how to use the `plone/nick` image.


### Run with PostgreSQL

The image runs `nick`, which migrates the database, installs the profiles, and starts the API on port 8080 and the job worker.
Pass the required `DB_PASSWORD` and `SECRET` environment variables with the `-e` option of `docker run`, as in the following examples.
The container stops at startup if either one is missing.

Create a network and two named volumes, and start a PostgreSQL database on the network.

```shell
docker network create plone
docker volume create nick-data
docker volume create nick-blobs
docker run -d --name nick-db --network plone -v nick-data:/var/lib/postgresql -e POSTGRES_USER=nick -e POSTGRES_PASSWORD=nick -e POSTGRES_DB=nick postgres:18-alpine
```

A named volume is storage that Docker manages, and it outlives the container that uses it.
The `nick-data` volume keeps the database, and the `nick-blobs` volume keeps the uploaded files in the default `file` blob storage.
With these named volumes, it's possible to remove the container without removing the data and files it holds.

To remove the containers only, stop them, and then remove them with the following command.
The volumes and their data remain.

```shell
docker stop nick nick-db
docker rm nick nick-db
```

To remove the data, remove the volumes with the following command.

```shell
docker volume rm nick-data nick-blobs
```

It's not possible to remove a volume that a container references, even if that container is stopped.
Remove the containers first.

Start Nick on the same network, and point it at the database.
Give PostgreSQL a few seconds to start before you run Nick.

```shell
docker run -d --name nick --network plone -p 8080:8080 -v nick-blobs:/app/var/blobstorage -e DB_HOST=nick-db -e DB_USER=nick -e DB_PASSWORD=nick -e DB_NAME=nick -e SECRET=change-me plone/nick:latest
```

Then request the API from your computer.
A response with the title `Welcome to Nick!` shows that the API runs and the demo profile is installed.

```shell
curl -H "Accept: application/json" http://localhost:8080/
```

The `DB_HOST` value must name a database that the container can reach, which is why both containers join the same network.
Use your own values for `DB_USER`, `DB_PASSWORD`, `DB_NAME`, and `SECRET` in any real setup.


### Run with Docker Compose

The [`examples/nick-postgres`](https://github.com/plone/container-nick/tree/main/examples/nick-postgres) directory of the `plone/container-nick` repository runs Nick with PostgreSQL in Docker Compose.
It splits Nick into three services that share one configuration:

- `migrate` migrates the database and installs the profiles, then exits.
  The `api` and `worker` services start only after it finishes successfully.
- `api` serves the REST API on port 8080, with `NICK_MODULES` set to `api`.
- `worker` runs the job worker and scheduler, with `NICK_MODULES` set to `worker`.
  It does not publish a port.

Save the following content as {file}`docker-compose.yml`, and run `docker compose up` from its directory.

```yaml
services:
  # Migrates the database and installs the profiles, then exits
  migrate:
    image: plone/nick:latest
    command: --modules=migrate
    environment: &nick-environment
      DB_HOST: db
      DB_USER: nick
      DB_PASSWORD: nick
      DB_NAME: nick
      SECRET: change-me
    depends_on:
      db:
        condition: service_healthy

  api:
    image: plone/nick:latest
    environment:
      <<: *nick-environment
      NICK_MODULES: api
      ALLOWED_ORIGINS: http://localhost:3000
    ports:
      - "8080:8080"
    volumes:
      - blobs:/app/var/blobstorage
    depends_on:
      migrate:
        condition: service_completed_successfully

  worker:
    image: plone/nick:latest
    environment:
      <<: *nick-environment
      NICK_MODULES: worker
    volumes:
      - blobs:/app/var/blobstorage
    depends_on:
      migrate:
        condition: service_completed_successfully

  db:
    image: postgres:18-alpine
    environment:
      POSTGRES_USER: nick
      POSTGRES_PASSWORD: nick
      POSTGRES_DB: nick
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "nick", "-d", "nick"]
      interval: 5s
      timeout: 5s
      retries: 10
    volumes:
      - data:/var/lib/postgresql

volumes:
  blobs: {}
  data: {}
```

The `data` volume holds the PostgreSQL database.
The `blobs` volume holds the uploaded files in the `file` blob storage, and the `api` and `worker` services share it.
`docker compose down` keeps both volumes, but `docker compose down -v` deletes them, and the data with them.
The stack uses the `nick` password and the `change-me` secret for demonstration only.


### Run selected modules

By default, the container runs all three modules.
To run only some of them, pass the modules as the command, or set the `NICK_MODULES` variable.
The modules are `migrate`, `api`, and `worker`.

```shell
docker run plone/nick --modules=migrate
docker run plone/nick --modules=api
docker run plone/nick --modules=worker
```

The `migrate` module exits with a non-zero status when it hits errors.
Each command needs the database and secret variables from the previous section.

To set the modules with an environment variable instead, pass it before the image name.
For example, for the `api` module, use the following command.

```shell
docker run -e NICK_MODULES=api plone/nick
```


## Configuration variables

The image reads these settings from the environment.

```{warning}
Without `PROFILES`, the image installs the demo site, with an `admin` user whose password is `admin`.
Set `PROFILES` and a real `SECRET` before you run the image in production.
```

| Environment variable | Description |
| --- | --- |
| `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME` | PostgreSQL connection. `DB_PASSWORD` is required. |
| `SECRET` | Secret that signs the authentication tokens. Required. |
| `PROFILES` | Profiles to install, separated by commas. Default: `@plone/nick:default`, the demo site with an `admin` user whose password is `admin`. |
| `NICK_MODULES` | Modules to run: `migrate`, `api`, or `worker`, separated by commas. Default: all of them. |
| `PORT` | Port where the API listens. Default: `8080`. |
| `ALLOWED_ORIGINS` | Origins that CORS allows, such as the address of the frontend. |
| `BLOBS_DIR` | Directory of the `file` blob storage. Default: {file}`/app/var/blobstorage`. Mount a volume there, or use the `db` or `s3` blob storage. |
| `ADDONS` | Add-ons from npm to install when the container starts, as space-separated `pnpm add` specs. Use it only to try out add-ons. |
| `/app/config.ts` | A {file}`config.ts` file mounted at this path replaces the environment configuration. |

Nick reads other settings from the environment as well.
For the full list, and for the settings of a production deployment, see the [Deployment](https://nick.docs.plone.org/admin-guide/deployment) guide in the Nick documentation.


## Add-ons

A Nick add-on is an npm package with profiles, migrations, and code.
Build an image on top of this one to add your add-ons, as in the following {file}`Dockerfile`.

```Dockerfile
FROM plone/nick:3.0.0

RUN pnpm add @acme/nick-addon@1.2.0

ENV PROFILES=@plone/nick:core,@acme/nick-addon:default
```

Read the [Add-ons](https://nick.docs.plone.org/developer-guide/addons) chapter of the Nick documentation for how to write one.

The `ADDONS` variable installs add-ons every time the container starts.
Use it only to try out an add-on, and build an image for production.


## Contribute

To contribute to Nick or its image, use the following links.

- [`container-nick` issue tracker](https://github.com/plone/container-nick/issues)
- [`container-nick` source code](https://github.com/plone/container-nick)
- [Nick source code](https://github.com/plone/nick)
