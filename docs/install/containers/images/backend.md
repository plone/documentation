---
html_meta:
  "description": "Using plone/plone-backend image"
  "property=og:description": "Using plone/plone-backend image"
  "property=og:title": "Plone Backend image"
  "keywords": "Plone 6, install, installation, docker, containers, backend, plone/plone-backend"
---

# `plone/plone-backend`

This chapter covers Plone backend [Docker](https://www.docker.com/) images using Python 3 and [pip](https://pip.pypa.io/en/stable/).


## Using this image


### Simple usage

```shell
docker run -p 8080:8080 plone/plone-backend:6.0.0a4 start
```

Then point your browser at `http://localhost:8080`.
You should see the default Plone site creation page.


### Persisting data

There are several ways to store data used by applications that run in Docker containers.

We encourage users of the `Plone` images to familiarize themselves with the options available.

[The Docker documentation](https://docs.docker.com/) is a good starting point for understanding the different storage options and variations.


## Configuration Variables


### Main variables

| Environment variable | Zope option | Default value |
| --- | --- | --- |
| `DEBUG_MODE` | `debug-mode` | `off` |
| `SECURITY_POLICY_IMPLEMENTATION` | `security-policy-implementation` | `C` |
| `VERBOSE_SECURITY` | `verbose-security` | `false` |
| `DEFAULT_ZPUBLISHER_ENCODING` | `default-zpublisher-encoding` | `utf-8` |


### Site creation variables

| Environment variable | Description |
| --- | --- |
| `SITE` | Id of the site to be created, for example, `Plone` |
| `TYPE` | Type of the site, either `classic` or `volto`. Default: `volto` |
| `PROFILES` | Initialize site with additional profiles, for example, `eea.api.layout:default` |
| `DELETE_EXISTING` | Force site to be recreated if it already exists, for example, `true` |

It is possible to initialize your database with a Plone Site instance on its first run.
To do so, pass the `SITE` environment variable with the name of the Plone Site instance, for example, `SITE=Plone`.
This will add a Volto-ready Plone site.
If you want a Plone Classic UI instance, pass the environment variable and value `TYPE=classic`.
To initialize it with additional profiles, pass them as space separated values via the `PROFILES` environment variable, for example, `PROFILES=eea.api.layout:default`.
To recreate the Plone site when restarting the container, you can pass the `DELETE_EXISTING` environment variable.

Plone 6 example:

```shell
docker run -p 8080:8080 -e ADDONS="eea.api.layout" -e SITE="Plone" -e PROFILES="eea.api.layout:default" plone/plone-backend:6.0.0a4
```

Plone 6 Classic example:

```shell
docker run -p 8080:8080 -e ADDONS="eea.facetednavigation" -e SITE="Plone" -e TYPE="classic" -e PROFILES="eea.facetednavigation:default" plone/plone-backend:6.0.0a4
```

```{warning}
We advise against using this feature on production environments.
```

### ZOPE variables

| Environment variable | Description | Default value |
| --- | --- | --- | --- |
| `ZODB_CACHE_SIZE` | database cache size | `50000` |


### ZEO variables

| Environment variable | Description | ZEO option | Default value |
| --- | --- | --- | --- |
| `ZEO_ADDRESS` | URL of the ZEO interface, `host:port` |  |  |
| `ZEO_SHARED_BLOB_DIR` | ZEO option |`name` | `off` |
| `ZEO_READ_ONLY` | ZEO option |`read-only` | `false` |
| `ZEO_CLIENT_READ_ONLY_FALLBACK` | ZEO option |`read-only-fallback` | `false` |
| `ZEO_STORAGE` | ZEO option |`storage` | `1` |
| `ZEO_CLIENT_CACHE_SIZE` | ZEO option | `cache-size` | `128MB` |
| `ZEO_DROP_CACHE_RATHER_VERIFY` | ZEO option | `drop-cache-rather-verify` | `false` |


#### Example

```yaml
version: "3"
services:

  backend:
    image: plone/plone-backend:6.0.0a4
    restart: always
    environment:
      ZEO_ADDRESS: zeo:8100
    ports:
    - "8080:8080"
    depends_on:
      - zeo

  zeo:
    image: plone/plone-zeo:latest
    restart: always
    volumes:
      - data:/data
    ports:
    - "8100:8100"

volumes:
  data: {}
```


### Relational Database variables

| Environment variable | Description | RelStorage option | Default value |
| --- | --- | --- | --- |
| `RELSTORAGE_DSN` | [PostgreSQL DSN](#postgresql-dsn) for the database interface | | |
| `RELSTORAGE_NAME` | RelStorage option | `name` | `storage` |
| `RELSTORAGE_READ_ONLY` | RelStorage option | `read-only` | `off` |
| `RELSTORAGE_KEEP_HISTORY` | RelStorage option | `keep-history` | `true` |
| `RELSTORAGE_COMMIT_LOCK_TIMEOUT` | RelStorage option | `commit-lock-timeout` | `30` |
| `RELSTORAGE_CREATE_SCHEMA` | RelStorage option | `create-schema` | `true` |
| `RELSTORAGE_SHARED_BLOB_DIR` | RelStorage option | `shared-blob-dir` | `false` |
| `RELSTORAGE_BLOB_CACHE_SIZE` | RelStorage option | `blob-cache-size` | `100mb` |
| `RELSTORAGE_BLOB_CACHE_SIZE_CHECK` | RelStorage option | `blob-cache-size-check` | `10` |
| `RELSTORAGE_BLOB_CACHE_SIZE_CHECK_EXTERNAL` | RelStorage option | `blob-cache-size-check-external` | `false` |
| `RELSTORAGE_BLOB_CHUNK_SIZE` | RelStorage option | `blob-chunk-size` | `1048576` |
| `RELSTORAGE_CACHE_LOCAL_MB` | RelStorage option | `cache-local-mb` | `10` |
| `RELSTORAGE_CACHE_LOCAL_OBJECT_MAX` | RelStorage option | `cache-local-object-max` | `16384` |
| `RELSTORAGE_CACHE_LOCAL_COMPRESSION` | RelStorage option | `cache-local-compression` | `none` |
| `RELSTORAGE_CACHE_DELTA_SIZE_LIMIT` | RelStorage option | `cache-delta-size-limit` | `100000` |


```{note}
Currently this image supports only the configuration of a PostgreSQL backend via configuration variables.
If you need to use MySQL or Oracle, we recommend that you extend this image and overwrite the `/app/etc/relstorage.conf` file.
```

#### PostgreSQL DSN

A valid PostgreSQL DSN is a list of parameters separated with whitespace.
A typical DSN looks like the following:

```console
dbname='zodb' user='username' host='localhost' password='pass'
```


#### Example

```yaml
version: "3"
services:

  backend:
    image: plone/plone-backend:6.0.0a4
    environment:
      RELSTORAGE_DSN: "dbname='plone' user='plone' host='db' password='plone'"
    ports:
    - "8080:8080"
    depends_on:
      - db

  db:
    image: postgres
    environment:
      POSTGRES_USER: plone
      POSTGRES_PASSWORD: plone
      POSTGRES_DB: plone
    ports:
    - "5432:5432"
```


### CORS variables

| Environment variable | Description | Default value |
| --- | --- | --- |
| `CORS_ALLOW_ORIGIN` | Origins that are allowed access to the resource. Either a comma separated list of origins, for example `http://example.net,http://mydomain.com` or `*` | `http://localhost:3000,http://127.0.0.1:3000` |
| `CORS_ALLOW_METHODS` | A comma separated list of HTTP method names that are allowed by this CORS policy, for example `DELETE,GET,OPTIONS,PATCH,POST,PUT` | `DELETE,GET,OPTIONS,PATCH,POST,PUT` |
| `CORS_ALLOW_CREDENTIALS` | Indicates whether the resource supports user credentials in the request | `true` |
| `CORS_EXPOSE_HEADERS` | A comma separated list of response headers clients can access, for example `Content-Length,X-My-Header` | `Content-Length,X-My-Header` |
| `CORS_ALLOW_HEADERS` | A comma separated list of request headers allowed to be sent by the client, for example `X-My-Header` | `Accept,Authorization,Content-Type,X-Custom-Header` |
| `CORS_MAX_AGE` | Indicates how long the results of a preflight request can be cached | `3600` |

These variables are used to configure [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/CORS).


### Add-on variables

| Environment variable | Description | Details |
| --- | --- | --- |
| `ADDONS` | A space separated list of python libraries to install | [Add-ons](#add-ons) |
| `DEVELOP` | A space separated list of python libraries to install in editable mode | [Developing packages](#developing-packages) |
| `PIP_PARAMS` | Parameters used in `pip` installation commands | [`pip install`](https://pip.pypa.io/en/stable/cli/pip_install/) |


#### Add-ons

It is possible to install add-ons during startup time in a container created using this image.
To do so, pass the `ADDONS` environment variable with a space separated list of requirements to be added to the image:

```shell
docker run -p 8080:8080 -e ADDONS="pas.plugins.authomatic" plone/plone-backend:6.0.0a4 start
```

This approach also allows you to test Plone with a specific version of one of its core components

```shell
docker run -p 8080:8080 -e ADDONS="plone.volto==3.1.0a3" plone/plone-backend:6.0.0a4 start
```

```{warning}
We advise against using this feature on production environments.
In this case, extend the image as explained before.
```


### Developing packages variable

It is possible to install local packages instead of packages from pip.
To do so, pass the `DEVELOP` environment variable with a space separated list of paths to Python packages to be installed.
These packages will be installed with `pip install --editable`.

```shell
docker run -p 8080:8080 -e DEVELOP="/app/src/mysite.policy" plone/plone-backend:6.0.0a4 start
```

This approach also allows you to develop local packages by using a volume.

```shell
docker run -p 8080:8080 -e DEVELOP="/app/src/mysite.policy" -v /path/to/mysite.policy:/app/src/mysite.policy plone/plone-backend:6.0.0a4 start
```

```{warning}
We advise against using this feature on production environments.
```


## Extending from this image

In a directory create a  `Dockerfile` file:

```Dockerfile
FROM plone/plone-backend:6.0.0a4

RUN apt-get update \
    && apt-get install -y --no-install-recommends gcc \
    && rm -rf /var/lib/apt/lists/*
```

Build your new image.

```shell
docker build . -t myproject:latest -f Dockerfile
```

And start a container.

```shell
docker run -p 8080:8080 myproject:latest start
```


## Advanced usage


### Arbitrary `--user`

This image supports running as a (mostly) arbitrary user via `--user` on `docker run`, as long as the owner of `/data` matches:

```shell
docker run --user="$(id -u)" -v $(pwd)/data:/data plone/plone-backend
```

The main caveat to note is that some environment variables, such as `ADDONS` and `DEVELOP`, will not work:

```console
$ docker run --user="$(id -u)" -v $(pwd)/data:/data -e ADDONS="eea.facetednavigation" plone/plone-backend
...
error: [Errno 13] Permission denied: '/app/lib/python3.9/site-packages/eea'
```


### Multiple containers with ZEO

This image supports ZEO clusters as a simple way to allow horizontal scaling of the backend.
Check the example page: {doc}`/volto/configuration/environmentvariables`.


## Versions

For a complete list of tags and versions, visit the [`plone/plone-backend` page on Docker Hub](https://hub.docker.com/r/plone/plone-backend).


## Contribute

- [Issue Tracker](https://github.com/plone/plone-backend/issues)
- [Source Code](https://github.com/plone/plone-backend/)
- [Documentation](https://github.com/plone/plone-backend/)
