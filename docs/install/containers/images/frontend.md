---
html_meta:
  "description": "Using plone/plone-frontend image"
  "property=og:description": "Using plone/plone-frontend image"
  "property=og:title": "Plone Frontend image"
  "keywords": "Plone 6, install, installation, docker, containers, plone/plone-frontend"
---

# `plone/plone-frontend`

Plone 6 default frontend [Docker](https://www.docker.com/) image using Node.
The frontend is written using React and requires a Plone backend to be running and accessible.

This image is **not a base image** to be extended in your projects, but an example of the Plone user experience out of the box.


## Using this image


## Configuration Variables


### Main variables


| Environment variable | Description | Example |
| --- | --- | --- |
| `RAZZLE_API_PATH` | Used to generate frontend calls to the backend. Needs to be a public url accessible by client browser | `http://api.site.org/++api++/` |
| `RAZZLE_INTERNAL_API_PATH` | Used by the middleware to construct requests to the backend. It can be a non-public address | `http://backend:8080/Plone` |
| `VOLTO_ROBOTSTXT` | Override the `robots.txt` file | `"User-agent: *\nDisallow: "` |

```{note}
For an extensive list of environment variables used by the frontend, visit {doc}`/volto/configuration/environmentvariables`.
```

## As an example for your volto project

To use this image as an example of a docker image for your own volto project, you will need to copy the [`Dockerfile`](https://github.com/plone/plone-frontend/blob/main/Dockerfile) file in your project.

In the `Dockerfile` file, replace the `yo @plone/volto` command with the `COPY . /build/plone-frontend` command.

### Create a custom entrypoint

The `plone-frontend` docker image does not have a custom entrypoint file, so for any commands you need to run on docker container start, you will need to create it.

After creating the `entrypoint.sh` file, make sure it has execute permission by running `chmod 755 entrypoint.sh`.

```{note}
Do not forget to add the `exec "$@"` command at the end of the `entrypoint.sh` file, to run the default `yarn start` command.
```

In the `Dockerfile` you will need to add this 2 commands to make the docker container run it on start:

```Dockerfile
COPY entrypoint.sh /
ENTRYPOINT ["/entrypoint.sh"]
```

### Build

Build your new image.

```shell
docker build . -t myfrontend:latest -f Dockerfile
```

### Start it

You can use it in this `docker-compose.yml` file 

```yaml
version: "3"
services:

  backend:
    image: plone/plone-backend:6.0.0a4
    # Plone 5.2 series can be used too
    # image: plone/plone-backend:5.2.7
    ports:
      - '8080:8080'
    environment:
      - SITE=Plone
      - 'ADDONS=plone.restapi==8.21.0 plone.volto==4.0.0a3 plone.rest==2.0.0a2 plone.app.iterate==4.0.2 plone.app.vocabularies==4.3.0'
      - 'PROFILES=plone.volto:default-homepage'

  frontend:
    image: 'myfrontend:latest'
    ports:
      - '3000:3000'
    restart: always
    environment:
      # These are needed in a Docker environment since the
      # routing needs to be amended. You can point to the
      # internal network alias.
      RAZZLE_INTERNAL_API_PATH: http://backend:8080/Plone
      RAZZLE_DEV_PROXY_API_PATH: http://backend:8080/Plone
    depends_on:
      - backend
```

To start, run
```shell
docker-compose up -d
```     

## Versions

For a complete list of tags and versions, visit the [`plone/plone-frontend` page on Docker Hub](https://hub.docker.com/r/plone/plone-frontend).


## Contribute

- [Issue Tracker](https://github.com/plone/plone-frontend/issues)
- [Source Code](https://github.com/plone/plone-frontend/)
- [Documentation](https://github.com/plone/plone-frontend/)
