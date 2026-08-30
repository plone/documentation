---
myst:
  html_meta:
    "description": "Reference for plone/plone-backend image environment variables"
    "property=og:description": "Reference for plone/plone-backend image environment variables"
    "property=og:title": "Plone Backend image - Environment Variables Reference"
    "keywords": "Plone 6, install, installation, docker, containers, backend, plone/plone-backend, reference, environment variables"
---

# `plone/plone-backend` - Environment Variables Reference

This reference document covers all environment variables available for the Plone backend [Docker](https://www.docker.com/) image.

For usage instructions and examples, see {doc}`backend`.


## Main variables

| Environment variable | Zope option | Default value |
| --- | --- | --- |
| `DEBUG_MODE` | `debug-mode` | `off` |
| `SECURITY_POLICY_IMPLEMENTATION` | `security-policy-implementation` | `C` |
| `VERBOSE_SECURITY` | `verbose-security` | `false` |
| `DEFAULT_ZPUBLISHER_ENCODING` | `default-zpublisher-encoding` | `utf-8` |
| `LISTEN_PORT` | (no equivalent) | `8080` |

### Listen port

By default, the Zope process inside the container will listen on TCP port 8080.
In certain circumstances — Kubernetes or Podman pods — there may be a need to run
more than one Zope process within the network namespace, which would result in
listen port clashes as two different processes within the same namespace attempt
to listen to the same TCP port.

In these cases, the variable `LISTEN_PORT` can be set to any particular port above
1024 to ensure that the container will listen on the desired port.


## Site creation variables

| Environment variable | Description |
| --- | --- |
| `SITE` | Id of the site to be created, for example, `Plone` |
| `TYPE` | Type of the site, either `classic` or `volto`. Default: `volto` |
| `PROFILES` | Initialize site with additional profiles, for example, `eea.api.layout:default` |
| `DELETE_EXISTING` | Force site to be recreated if it already exists, for example, `true` |


## ZOPE variables

| Environment variable | Description | Default value |
| --- | --- | --- |
| `ZODB_CACHE_SIZE` | database cache size | `50000` |


## ZEO variables

| Environment variable | Description | ZEO option | Default value |
| --- | --- | --- | --- |
| `ZEO_ADDRESS` | URL of the ZEO interface, `host:port` |  |  |
| `ZEO_SHARED_BLOB_DIR` | ZEO option |`name` | `off` |
| `ZEO_READ_ONLY` | ZEO option |`read-only` | `false` |
| `ZEO_CLIENT_READ_ONLY_FALLBACK` | ZEO option |`read-only-fallback` | `false` |
| `ZEO_STORAGE` | ZEO option |`storage` | `1` |
| `ZEO_CLIENT_CACHE_SIZE` | ZEO option | `cache-size` | `128MB` |
| `ZEO_DROP_CACHE_RATHER_VERIFY` | ZEO option | `drop-cache-rather-verify` | `false` |


## Relational Database variables

| Environment variable | Description | RelStorage option | Default value |
| --- | --- | --- | --- |
| `RELSTORAGE_DSN` | {ref}`containers-images-backend-postgresql-dsn-label` for the database interface | | |
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

(containers-images-backend-postgresql-dsn-label)=

### PostgreSQL DSN

A valid PostgreSQL DSN is a list of parameters separated with whitespace.
A typical DSN looks like the following:

```console
dbname='zodb' user='username' host='localhost' password='pass'
```


## CORS variables

| Environment variable | Description | Default value |
| --- | --- | --- |
| `CORS_ALLOW_ORIGIN` | Origins that are allowed access to the resource. Either a comma separated list of origins, for example `http://example.net,http://mydomain.com` or `*` | `http://localhost:3000,http://127.0.0.1:3000` |
| `CORS_ALLOW_METHODS` | A comma separated list of HTTP method names that are allowed by this CORS policy, for example `DELETE,GET,OPTIONS,PATCH,POST,PUT` | `DELETE,GET,OPTIONS,PATCH,POST,PUT` |
| `CORS_ALLOW_CREDENTIALS` | Indicates whether the resource supports user credentials in the request | `true` |
| `CORS_EXPOSE_HEADERS` | A comma separated list of response headers clients can access, for example `Content-Length,X-My-Header` | `Content-Length,X-My-Header` |
| `CORS_ALLOW_HEADERS` | A comma separated list of request headers allowed to be sent by the client, for example `X-My-Header` | `Accept,Authorization,Content-Type,X-Custom-Header` |
| `CORS_MAX_AGE` | Indicates how long the results of a preflight request can be cached | `3600` |

These variables are used to configure [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS).

(containers-images-backend-add-ons-label)=

## Add-on variables

| Environment variable | Description | Details |
| --- | --- | --- |
| `ADDONS` | A space separated list of python libraries to install | {ref}`containers-images-backend-add-ons-label` |
| `DEVELOP` | A space separated list of python libraries to install in editable mode | See {ref}`containers-images-backend-add-ons-label` |
| `PIP_PARAMS` | Parameters used in `pip` installation commands | [`pip install`](https://pip.pypa.io/en/stable/cli/pip_install/) |

