---
myst:
  html_meta:
    "description": "Plone 6 Docker image recipes"
    "property=og:description": "Plone 6 Docker image recipes"
    "property=og:title": "Plone 6 image recipes"
    "keywords": "Plone 6, install, installation, Docker, containers, official images"
---

# Docker recipes

This chapter offers some useful recipes when working with Plone containers.


## Remove access log from Plone containers

When you generate a project using [Cookieplone](https://github.com/plone/cookieplone), it creates Plone containers for your project that are based on the official [`plone/plone-backend`](https://github.com/plone/plone-backend) images.

When you run your container or the official `plone/plone-backend` image with logging, the output mixes both the event log and the access log, making it hard to follow the logs you may have added to your application.
In such cases, you may have a Docker Compose setup with several components including a proxy server that already provides access logs.
Instead of duplicating the logging output, it is common to remove the access logging from the Plone container.

To do so, create a custom {file}`zope.ini` file in your project's {file}`backend` folder with the following content.

```{code-block} ini
:emphasize-lines: 17-20

[app:zope]
use = egg:Zope#main
zope_conf = %(here)s/%(config_file)s

[server:main]
use = egg:waitress#main
host = 0.0.0.0
port = 8080
threads = 2
clear_untrusted_proxy_headers = false
max_request_body_size = 1073741824

[filter:translogger]
use = egg:Paste#translogger
setup_console_handler = False

[pipeline:main]
pipeline =
    egg:Zope#httpexceptions
    zope

[loggers]
keys = root, waitress.queue, waitress, wsgi

[handlers]
keys = accesslog, eventlog

[formatters]
keys = generic, message

[formatter_generic]
format = %(asctime)s %(levelname)s [%(name)s:%(lineno)s][%(threadName)s] %(message)s
datefmt = %Y-%m-%d %H:%M:%S

[formatter_message]
format = %(message)s

[logger_root]
level = INFO
handlers = eventlog

[logger_waitress.queue]
level = INFO
handlers = eventlog
qualname = waitress.queue
propagate = 0

[logger_waitress]
level = INFO
handlers = eventlog
qualname = waitress
propagate = 0

[logger_wsgi]
level = WARN
handlers = accesslog
qualname = wsgi
propagate = 0

[handler_accesslog]
class = StreamHandler
args = (sys.stdout,)
level = INFO
formatter = message

[handler_eventlog]
class = StreamHandler
args = (sys.stderr,)
level = INFO
formatter = generic
```

Comparing this file with the [original `zope.ini` file](https://github.com/plone/plone-backend/blob/6.1.x/skeleton/etc/zope.ini) that comes with the `plone/plone-backend` container, you may realize that the only change is the `translogger` configuration was removed from the `pipeline` section.
This [`translogger` middleware produces logs in the Apache Combined Log Format](https://docs.pylonsproject.org/projects/waitress/en/latest/logging.html).
The above configuration removes it from the setup.

After adding the {file}`zope.ini` file in your project, adjust the {file}`Dockerfile` by inserting the command `COPY zope.ini etc/` before the `RUN` command as highlighted below.
This new command copies the {file}`zope.ini` file into the container.

```{code-block} dockerfile
:emphasize-lines: 4

# Add local code
COPY scripts/ scripts/
COPY . src
COPY zope.ini etc/

# Install local requirements and pre-compile mo files
RUN <<EOT
```

After making these changes, build the project container as usual.
It will no longer output the access log, but will continue to output the event log.


## Pack the ZODB

A common maintenance task of a Plone instance is to [pack the ZODB](https://zodb.org/en/stable/reference/zodb.html#ZODB.DB.pack).
Packing removes old revisions of objects.
It is similar to [routine vacuuming in PostgreSQL](https://www.postgresql.org/docs/8.3/routine-vacuuming.html).

The official {doc}`/install/containers/images/backend` container and project containers based on them have a `pack` command to pack the ZODB.
The command will work in standalone mode, ZEO mode, and RelStorage mode but only with PostgreSQL.

Invoke the command in a running container by passing in the appropriate command for the mode.

In standalone mode, ZODB is in a mounted volume, so the command would be similar to the following.

```shell
docker run -v /path/to/your/volume:/data plone/plone-backend pack
```

In ZEO mode, run the command next to your ZEO instance.

```shell
docker run -e ZEO_ADDRESS=zeo:8100 --link zeo plone/plone-backend pack
```

In RelStorage mode, pass the connection DSN.

```shell
docker run -e RELSTORAGE_DSN="dbname='plone' user='plone' host='db' password='password' port='5432'" pack
```

In running containers that use Docker Compose, the command is less complicated.

```shell
docker compose run backend pack
```

The above command assumes that the service that runs the Plone instance is named `backend`.
Otherwise replace `backend` with your container's name.

