---
html_meta:
  "description": "Using plone/plone-backend image"
  "property=og:description": "Using plone/plone-backend image"
  "property=og:title": "Plone Backend image"
  "keywords": "Plone 6, install, installation, docker, containers, backend, plone/plone-backend"
---

# `plone/plone-backend`

Plone backend [Docker](https://www.docker.com/) images using Python 3 and [pip](https://pip.pypa.io/en/stable/).


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


### Site creation

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

| Environment variable | Description |
| --- | --- |
| `SITE` | Id of the site to be created, for example, `Plone` |
| `TYPE` | Type of the site, either `classic` or `volto`. Default: `volto` |
| `PROFILES` | Initialize site with additional profiles, for example, `eea.api.layout:default` |
| `DELETE_EXISTING` | Force site to be recreated if it already exists, for example, `true` |

```{warning}
We advise against using this feature on production environments.
```


### ZEO

To use a ZEO database, you need to pass the `ZEO_ADDRESS` to the image:

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

The following is a list of supported environment variables for ZEO:

| Environment variable | ZEO option | Default value |
| --- | --- | --- |
| `ZEO_SHARED_BLOB_DIR` | `name` | `off` |
| `ZEO_READ_ONLY` | `read-only` | `false` |
| `ZEO_CLIENT_READ_ONLY_FALLBACK` | `read-only-fallback` | `false` |
| `ZEO_STORAGE` | `storage` | `1` |
| `ZEO_CLIENT_CACHE_SIZE` | `cache-size` | `128MB` |
| `ZEO_DROP_CACHE_RATHER_VERIFY` | `drop-cache-rather-verify` | `false` |


### Relational Database

```{note}
Currently this image supports only the configuration of a PostgreSQL backend via configuration variables.
If you need to use MySQL or Oracle, we recommend that you extend this image and overwrite the `/app/etc/relstorage.conf` file.
```

To use a PostgreSQL database, you need to pass the `RELSTORAGE_DSN` to the image:

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

A valid PostgreSQL DSN is a list of parameters separated with whitespace.
A typical DSN looks like the following.

```console
dbname='zodb' user='username' host='localhost' password='pass'
```

The following is a list of supported environment variables for Relstorage:

| Environment variable | RelStorage option | Default value |
| --- | --- | --- |
| `RELSTORAGE_NAME` | `name` | `storage` |
| `RELSTORAGE_READ_ONLY` | `read-only` | `off` |
| `RELSTORAGE_KEEP_HISTORY` | `keep-history` | `true` |
| `RELSTORAGE_COMMIT_LOCK_TIMEOUT` | `commit-lock-timeout` | `30` |
| `RELSTORAGE_CREATE_SCHEMA` | `create-schema` | `true` |
| `RELSTORAGE_SHARED_BLOB_DIR` | `shared-blob-dir` | `false` |
| `RELSTORAGE_BLOB_CACHE_SIZE` | `blob-cache-size` | `100mb` |
| `RELSTORAGE_BLOB_CACHE_SIZE_CHECK` | `blob-cache-size-check` | `10` |
| `RELSTORAGE_BLOB_CACHE_SIZE_CHECK_EXTERNAL` | `blob-cache-size-check-external` | `false` |
| `RELSTORAGE_BLOB_CHUNK_SIZE` | `blob-chunk-size` | `1048576` |
| `RELSTORAGE_CACHE_LOCAL_MB` | `cache-local-mb` | `10` |
| `RELSTORAGE_CACHE_LOCAL_OBJECT_MAX` | `cache-local-object-max` | `16384` |
| `RELSTORAGE_CACHE_LOCAL_COMPRESSION` | `cache-local-compression` | `none` |
| `RELSTORAGE_CACHE_DELTA_SIZE_LIMIT` | `cache-delta-size-limit` | `100000` |


### CORS

| Environment variable | Description | Default value |
| --- | --- | --- |
| `CORS_ALLOW_ORIGIN` | Origins that are allowed access to the resource. Either a comma separated list of origins, for example `http://example.net,http://mydomain.com` or `*` | `http://localhost:3000,http://127.0.0.1:3000` |
| `CORS_ALLOW_METHODS` | A comma separated list of HTTP method names that are allowed by this CORS policy, for example `DELETE,GET,OPTIONS,PATCH,POST,PUT` | `DELETE,GET,OPTIONS,PATCH,POST,PUT` |
| `CORS_ALLOW_CREDENTIALS` | Indicates whether the resource supports user credentials in the request | `true` |
| `CORS_EXPOSE_HEADERS` | A comma separated list of response headers clients can access, for example `Content-Length,X-My-Header` | `Content-Length,X-My-Header` |
| `CORS_ALLOW_HEADERS` | A comma separated list of request headers allowed to be sent by the client, for example `X-My-Header` | `Accept,Authorization,Content-Type,X-Custom-Header` |
| `CORS_MAX_AGE` | Indicates how long the results of a preflight request can be cached | `3600` |


### Add-on installation

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


### Developing packages

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

RUN ./bin/pip install "pas.plugin.authomatic"
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
To use it, create a directory for your project, and inside it create a `docker-compose.yml` file that starts your Plone instance and the ZEO instance with volume mounts for data persistence.
HAProxy is used for load balancing in this example.

```yaml
version: "3"
services:

  lb:
    image: plone/plone-haproxy
    depends_on:
    - backend
    ports:
    - "8080:8080"
    - "1936:1936"
    environment:
      FRONTEND_PORT: "8080"
      BACKENDS: "backend"
      BACKENDS_PORT: "8080"
      DNS_ENABLED: "True"
      HTTPCHK: "GET /"
      INTER: "5s"
      LOG_LEVEL: "info"

  backend:
    image: plone/plone-backend:6.0.0a4
    restart: always
    environment:
      ZEO_ADDRESS: zeo:8100
    ports:
    - "8080"
    depends_on:
      - zeo

  zeo:
    image: plone/plone-zeo:latest
    restart: always
    volumes:
      - data:/data
    ports:
    - "8100"

volumes:
  data: {}
```

Now run `docker-compose up -d --scale backend=4` from your project directory.

Point your browser at `http://localhost:8080`, using the username and password combination of `admin` and `admin`, and you should see the default Plone site creation page.

Point your browser at `http://localhost:1936`, using the username and password combination of `admin` and `admin`, and you should see HAProxy statistics for your Plone cluster.


## Versions

For a complete list of tags and versions, visit the [`plone/plone-backend` page on Docker Hub](https://hub.docker.com/r/plone/plone-backend).


## Contribute

- [Issue Tracker](https://github.com/plone/plone-backend/issues)
- [Source Code](https://github.com/plone/plone-backend/)
- [Documentation](https://github.com/plone/plone-backend/)
