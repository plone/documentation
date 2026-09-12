---
myst:
  html_meta:
    "description": "Container images for historical Plone releases, from Plone 1.0 to Plone 5.2"
    "property=og:description": "Container images for historical Plone releases, from Plone 1.0 to Plone 5.2"
    "property=og:title": "Historical Plone images"
    "keywords": "Plone, install, installation, docker, containers, historical, legacy, migration, plone/plone"
---

# Historical images

This chapter covers the container images for Plone releases older than Plone 6, from Plone 1.0 to Plone 5.2.

```{warning}
These images are no longer supported.
Plone 1.x, 2.x, 3.x, 4.x and 5.x have reached end of life, and the images receive no security or dependency updates.
Never run them in production or expose them to an untrusted network.
```

Use these images for content extraction, migration rehearsal, and the study of past Plone releases.

For a supported Plone, use the Plone 6 images: {doc}`backend`, {doc}`aurora`, {doc}`frontend`, and {doc}`zeo`.


## Where the images live

The images are available on Docker Hub as [`plone/plone`](https://hub.docker.com/r/plone/plone).

```shell
docker pull plone/plone:5.2
```


## Available versions

Each release lists only its last version.

| Plone release | Last version | Python | Tags | Platforms |
| --- | --- | --- | --- | --- |
| 5.2 | 5.2.4 | 3.8.8 | `plone/plone:5.2`, `plone/plone:5.2.4` | linux/amd64 |
| 5.1 | 5.1.6 | 2.7.17 | `plone/plone:5.1`, `plone/plone:5.1.6` | linux/amd64 |
| 5.0 | 5.0.8 | 2.7.14 | `plone/plone:5.0`, `plone/plone:5.0.8` | linux/amd64 |
| 4.3 | 4.3.19 | 2.7.17 | `plone/plone:4.3`, `plone/plone:4.3.19` | linux/amd64 |
| 4.2 | 4.2.6 | 2.7.18 | `plone/plone:4.2`, `plone/plone:4.2.6` | linux/amd64 |
| 4.1 | 4.1.6 | 2.6.9 | `plone/plone:4.1`, `plone/plone:4.1.6` | linux/amd64 |
| 4.0 | 4.0.9 | 2.6.9 | `plone/plone:4.0`, `plone/plone:4.0.9` | linux/amd64 |
| 3.3 | 3.3.6 | 2.4.6 | `plone/plone:3.3`, `plone/plone:3.3.6` | linux/amd64 |
| 3.2 | 3.2.3 | 2.4.6 | `plone/plone:3.2`, `plone/plone:3.2.3` | linux/amd64 |
| 3.1 | 3.1.7 | 2.4.6 | `plone/plone:3.1`, `plone/plone:3.1.7` | linux/amd64 |
| 3.0 | 3.0.5 | 2.4.6 | `plone/plone:3.0`, `plone/plone:3.0.5` | linux/amd64 |
| 2.5 | 2.5.4-2 | 2.4.6 | `plone/plone:2.5`, `plone/plone:2.5.4-2` | linux/amd64 |
| 2.1 | 2.1.4 | 2.4.6 | `plone/plone:2.1`, `plone/plone:2.1.4` | linux/amd64 |
| 2.0 | 2.0.5 | 2.3.7 | `plone/plone:2.0`, `plone/plone:2.0.5` | linux/amd64 |
| 1.0 | 1.0.6 | 2.3.7 | `plone/plone:1.0`, `plone/plone:1.0.6` | linux/amd64 |

% TODO: List the variants of the Plone 4.3 to 5.2 images, such as `-alpine`, `-python2`, `-python36`, and `-python37`.

All images listen on port 8080, and store their data in a {file}`/data` volume.
To use an existing database, place its {file}`Data.fs` file at {file}`/data/filestorage/Data.fs` before the first start.


## Plone 5.2

```shell
docker run -p 8080:8080 -v plone52-data:/data plone/plone:5.2
```

Then point your browser at `http://localhost:8080`, and add a Plone site with the user `admin` and the password `admin`.


## Plone 5.1

```shell
docker run -p 8080:8080 -v plone51-data:/data plone/plone:5.1
```

Then point your browser at `http://localhost:8080`, and add a Plone site with the user `admin` and the password `admin`.


## Plone 5.0

```shell
docker run -p 8080:8080 -v plone50-data:/data plone/plone:5.0
```

Then point your browser at `http://localhost:8080`, and add a Plone site with the user `admin` and the password `admin`.


## Plone 4.3

```shell
docker run -p 8080:8080 -v plone43-data:/data plone/plone:4.3
```

Then point your browser at `http://localhost:8080`, and add a Plone site with the user `admin` and the password `admin`.


## Plone 4.2

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone42-data:/data plone/plone:4.2
```

Then point your browser at `http://localhost:8080`.


### Plone 4.2 demo variant

The `plone/plone:4.2-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:4.2-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 4.1

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone41-data:/data plone/plone:4.1
```

Then point your browser at `http://localhost:8080`.


### Plone 4.1 demo variant

The `plone/plone:4.1-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:4.1-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 4.0

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone40-data:/data plone/plone:4.0
```

Then point your browser at `http://localhost:8080`.


### Plone 4.0 demo variant

The `plone/plone:4.0-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:4.0-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 3.3

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone33-data:/data plone/plone:3.3
```

Then point your browser at `http://localhost:8080`.


### Plone 3.3 demo variant

The `plone/plone:3.3-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:3.3-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 3.2

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone32-data:/data plone/plone:3.2
```

Then point your browser at `http://localhost:8080`.


### Plone 3.2 demo variant

The `plone/plone:3.2-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:3.2-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 3.1

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone31-data:/data plone/plone:3.1
```

Then point your browser at `http://localhost:8080`.


### Plone 3.1 demo variant

The `plone/plone:3.1-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:3.1-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 3.0

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone30-data:/data plone/plone:3.0
```

Then point your browser at `http://localhost:8080`.


### Plone 3.0 demo variant

The `plone/plone:3.0-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:3.0-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 2.5

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone25-data:/data plone/plone:2.5
```

Then point your browser at `http://localhost:8080`.


### Plone 2.5 demo variant

The `plone/plone:2.5-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:2.5-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 2.1

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone21-data:/data plone/plone:2.1
```

Then point your browser at `http://localhost:8080`.


### Plone 2.1 demo variant

The `plone/plone:2.1-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:2.1-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 2.0

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone20-data:/data plone/plone:2.0
```

Then point your browser at `http://localhost:8080`.


### Plone 2.0 demo variant

The `plone/plone:2.0-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:2.0-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Plone 1.0

```shell
docker run -p 8080:8080 -e ADMIN_PASSWORD=secret -v plone10-data:/data plone/plone:1.0
```

Then point your browser at `http://localhost:8080`.


### Plone 1.0 demo variant

The `plone/plone:1.0-demo` image ships with a Plone site already created with the ID `Plone`.

```shell
docker run -p 8080:8080 plone/plone:1.0-demo
```

Then point your browser at `http://localhost:8080/Plone`, and log in with the user `admin` and the password `admin`.


## Upgrade a database

The images for Plone 1.0 to 4.2 carry an `upgrade` command that runs the Plone migration against the database in {file}`/data`.
To upgrade a database across several releases, mount the same volume into each next release, one at a time.

Stop any container that uses the database, then run the following command.

```shell
docker run --rm -v mydata:/data plone/plone:4.2 upgrade
```

The command commits nothing if the migration fails.


## Configuration variables

The images for Plone 1.0 to 4.2 support the following environment variables.

| Environment variable | Description | Default value |
| --- | --- | --- |
| `ADMIN_USER` | User name of the administrator account | |
| `ADMIN_PASSWORD` | Password of the administrator account | |
| `SITE_ID` | ID of the site to migrate with the `upgrade` command | `Plone` |
| `ZEO_ADDRESS` | Address of the ZEO server, `host:port`. Setting it turns the container into a ZEO client. | |
| `ZEO_STORAGE` | Storage name on the ZEO server | `1` |
| `ZEO_CLIENT_CACHE_SIZE` | Size of the ZEO client cache | `128MB` |
| `ZEO_SHARED_BLOB_DIR` | Set to `on` when the client and the server share a blob directory | `off` |

% TODO: Confirm the default values of `ADMIN_USER` and `ADMIN_PASSWORD`.
% TODO: Document the environment variables of the Plone 4.3 to 5.2 images.


## Contribute

- [Issue Tracker](https://github.com/plone/container-historical/issues)
- [Source Code](https://github.com/plone/container-historical/)
