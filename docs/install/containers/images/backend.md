---
myst:
  html_meta:
    "description": "Using plone/plone-backend image"
    "property=og:description": "Using plone/plone-backend image"
    "property=og:title": "Plone Backend image"
    "keywords": "Plone 6, install, installation, docker, containers, backend, plone/plone-backend"
---

# `plone/plone-backend`

This chapter covers Plone backend [Docker](https://www.docker.com/) images using Python 3 and [pip](https://pip.pypa.io/en/stable/).

For a complete reference of all environment variables, see {doc}`backend-reference`.

## Using this image


### Simple usage

```shell
docker run -p 8080:8080 plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION} start
```

Then point your browser at `http://localhost:8080`.
You should see the default Plone site creation page.


### Persisting data

There are several ways to store data used by applications that run in Docker containers.

We encourage users of the `Plone` images to familiarize themselves with the options available.

[The Docker documentation](https://docs.docker.com/get-started/docker-concepts/running-containers/persisting-container-data/) is a good starting point for understanding the different storage options and variations.


## Site creation

It is possible to initialize your database with a Plone Site instance on its first run.
To do so, pass the `SITE` environment variable with the name of the Plone Site instance, for example, `SITE=Plone`.
This will add a Volto-ready Plone site.
If you want a Plone Classic UI instance, pass the environment variable and value `TYPE=classic`.
To initialize it with additional profiles, pass them as space separated values via the `PROFILES` environment variable, for example, `PROFILES=eea.api.layout:default`.
To recreate the Plone site when restarting the container, you can pass the `DELETE_EXISTING` environment variable.

For a complete reference of site creation variables, see {doc}`backend-reference`.

Plone 6 example:

```shell
docker run -p 8080:8080 -e ADDONS="eea.api.layout" -e SITE="Plone" -e PROFILES="eea.api.layout:default" plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
```

Plone 6 Classic example:

```shell
docker run -p 8080:8080 -e ADDONS="eea.facetednavigation" -e SITE="Plone" -e TYPE="classic" -e PROFILES="eea.facetednavigation:default" plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
```

```{warning}
We advise against using this feature on production environments.
```


## Using ZEO

For a complete reference of ZEO environment variables, see {doc}`backend-reference`.

#### Example

```yaml
version: "3"
services:

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
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


## Using Relational Database

For a complete reference of Relational Database environment variables, see {doc}`backend-reference`.

### PostgreSQL DSN

A valid PostgreSQL DSN is a list of parameters separated with whitespace.
A typical DSN looks like the following:

```console
dbname='zodb' user='username' host='localhost' password='pass'
```

### Example

```yaml
version: "3"
services:

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
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

```{note}
Currently this image supports only the configuration of a PostgreSQL backend via configuration variables.
If you need to use MySQL or Oracle, we recommend that you extend this image and overwrite the `/app/etc/relstorage.conf` file.
```


## CORS configuration

These variables are used to configure [CORS](https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CORS).

For a complete reference of CORS environment variables, see {doc}`backend-reference`.


(containers-images-backend-add-ons-label)=

### Add-ons

It is possible to include add-ons during startup time in a container created using this image.

```{warning}
We advise against using this feature on production environments — the recommended method is to
extend the official container images to include your desired add-ons in your own container.
This has several advantages, among which is the certainty that your container will always
run the exact add-on code you built into it.
```

To do so, pass the `ADDONS` environment variable with a space separated list of requirements to be added to the image
(see below for documentation of the supported variables):

```shell
docker run -p 8080:8080 -e ADDONS="pas.plugins.authomatic" plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION} start
```

After Plone has started, you can add your Plone site (if none exists yet) and install the added
add-ons to your site.

This approach also allows you to test Plone with a specific version of one of its core components

```shell
docker run -p 8080:8080 -e ADDONS="plone.volto==3.1.0a3" plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION} start
```

For a complete reference of add-on environment variables, see {doc}`backend-reference`.

#### Adding configuration to `zope.conf` or additional ZCML

Some Plone add-ons require changes to `zope.conf` or extra ZCML.

With the standard container, it is not possible to add configuration fragments to
`zope.conf` directly or add extra ZCML, like it is with the `buildout` deployment
method.

However, you can derive your own container image, and drop in configuration
fragments.  See {ref}`backend-extending-from-this-image-label` below for instructions.


### Developing packages

It is possible to install local packages instead of packages from pip.
To do so, pass the `DEVELOP` environment variable with a space separated list of paths to Python packages to be installed.
These packages will be installed with `pip install --editable`.

```{warning}
We advise against using this feature on production environments — the recommended method is to
extend the official container images to include your desired add-ons in your own container.
```

```shell
docker run -p 8080:8080 -e DEVELOP="/app/src/mysite.policy" plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION} start
```

This approach also allows you to develop local packages by using a volume.

```shell
docker run -p 8080:8080 -e DEVELOP="/app/src/mysite.policy" -v /path/to/mysite.policy:/app/src/mysite.policy plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION} start
```

For a complete reference of developing packages variables, see {doc}`backend-reference`.

(backend-extending-from-this-image-label)=

## Extending from this image

In a directory create a  `Dockerfile` file:

```Dockerfile
FROM plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}

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

### Changing default values of environment variables

All the environment variables documented above are supported in your
derived container's Dockerfile.  You can override the default values
of variables as follows:

```Dockerfile
# Add environment variables before any CMD or ENTRYPOINT stanzas,
# and after any FROM, RUN and COPY stanzas.
ENV ZODB_CACHE_SIZE="120000"
```

Of course, you can always override these variables upon container
start by using the Docker `docker run` argument `-e VAR=value`.

Be aware that some variables are not intended to be used in production.
Check the respective variable documentation above to determine whether
you should use it, or use a different method to get the desired result
in production.

### Adding `zope.conf` configuration fragments

In the directory containing your `Dockerfile`, create a folder `etc/zope.conf.d`.
Add your `zope.conf` configuration fragments there.

Now add the following to your `Dockerfile`, before any `CMD` or `ENTRYPOINT`
stanzas it may have, and after the `FROM` and any `RUN` stanzas:

```Dockerfile
COPY /etc/zope.conf.d/*.conf /app/etc/zope.conf.d/
```

This ensures your fragments are deployed in the `zope.conf.d` folder, which then
will be used to amend the `zope.conf` file prior to starting Plone.

### Adding ZCML fragments

In the directory containing your `Dockerfile`, create a folder `etc/package-includes`.
Add your ZCML configuration fragments (named `*-meta.zcml`, `*-configure.zcml`,
`*-overrides.zcml`) as files in that folder.

Now add the following to your `Dockerfile`, before any `CMD` or `ENTRYPOINT`
stanzas it may have, and after the `FROM` and any `RUN` stanzas:

```Dockerfile
COPY /etc/package-includes/*.zcml /app/etc/package-includes/
```

Your ZCML fragments will be copied into the container and automatically included
when Plone starts.

## Advanced usage

This section describes advanced usage of the Plone backend Docker image.


### Arbitrary user and persistent data

You can run Docker as an arbitrary user with the `--user` option.

To persist backend data between restarts of Docker, use both options of `--user` and `-v`.

The following command will run the Plone backend container as an arbitrary user, and persist the backend data in a volume, provided that the owner of the directory `/data` is the same as the `--user` option.

```shell
docker run --user="$(id -u)" -v $(pwd)/data:/data plone/plone-backend
```

````{note}
Some environment variables, such as `ADDONS` and `DEVELOP`, will not work.

```console
$ docker run --user="$(id -u)" -v $(pwd)/data:/data -e ADDONS="eea.facetednavigation" plone/plone-backend
...
error: [Errno 13] Permission denied: '/app/lib/python3.9/site-packages/eea'
```
````


### Multiple containers with ZEO

This image supports ZEO clusters as a simple way to allow horizontal scaling of the backend.
Check the example page: {doc}`/volto/configuration/environmentvariables`.


## Versions

For a complete list of tags and versions, visit the [`plone/plone-backend` page on Docker Hub](https://hub.docker.com/r/plone/plone-backend).


## Contribute

- [Issue Tracker](https://github.com/plone/plone-backend/issues)
- [Source Code](https://github.com/plone/plone-backend/)
- [Documentation](https://github.com/plone/plone-backend/)
