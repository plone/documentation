---
myst:
  html_meta:
    "description": "Very simple Plone 6 setup with only one or more backend instances accessing a ZEO server and data being persisted in a Docker volume."
    "property=og:description": "Very simple Plone 6 setup with only one or more backend instances accessing a ZEO server and data being persisted in a Docker volume."
    "property=og:title": "nginx, Frontend, Backend, ZEO container example"
    "keywords": "Plone 6, Container, Docker, nginx, Frontend, Backend, ZEO"
---

# nginx, Frontend, Backend, ZEO container example

This example is a very simple setup with one or more backend instances accessing a ZEO server and data being persisted in a Docker volume.

{term}`nginx` in this example is used as a [reverse proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/).


## Setup

Create an empty project directory named `nginx-volto-plone-zeo`.

```shell
mkdir nginx-volto-plone-zeo
```

Change into your project directory.

```shell
cd nginx-volto-plone-zeo
```


### nginx configuration

Add a `default.conf` that will be used by the nginx image:

```nginx
upstream backend {
  server backend:8080;
}
upstream frontend {
  server frontend:3000;
}

server {
  listen 80  default_server;
  server_name  plone.localhost;

  location ~ /\+\+api\+\+($|/.*) {
      rewrite ^/(\+\+api\+\+\/?)+($|/.*) /VirtualHostBase/http/$server_name/Plone/++api++/VirtualHostRoot/$2 break;
      proxy_pass http://backend;
  }

  location ~ / {
      location ~* \.(js|jsx|css|less|swf|eot|ttf|otf|woff|woff2)$ {
          add_header Cache-Control "public";
          expires +1y;
          proxy_pass http://frontend;
      }
      location ~* static.*\.(ico|jpg|jpeg|png|gif|svg)$ {
          add_header Cache-Control "public";
          expires +1y;
          proxy_pass http://frontend;
      }

      proxy_set_header        Host $host;
      proxy_set_header        X-Real-IP $remote_addr;
      proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
      proxy_set_header        X-Forwarded-Proto $scheme;
      proxy_redirect http:// https://;
      proxy_pass http://frontend;
  }
}
```

```{note}
`http://plone.localhost/` is the URL you will be using to access the website.
You can either use `localhost`, or add it in your `/etc/hosts` file or DNS to point to the Docker host IP.
```


### Service configuration with Docker Compose

Now let's create a `docker-compose.yml` file:

```yaml
version: "3"
services:

  webserver:
    image: nginx
    volumes:
      - ./default.conf:/etc/nginx/conf.d/default.conf
    depends_on:
      - backend
      - frontend
    ports:
    - "80:80"

  frontend:
    image: plone/plone-frontend:latest
    environment:
      RAZZLE_INTERNAL_API_PATH: http://backend:8080/Plone
    ports:
    - "3000:3000"
    depends_on:
      - backend

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
    environment:
      SITE: Plone
      ZEO_ADDRESS: db:8100
    ports:
    - "8080:8080"
    depends_on:
      - db

  db:
    image: plone/plone-zeo:latest
    restart: always
    volumes:
      - data:/data
    ports:
    - "8100:8100"

volumes:
  data: {}
```


## Build the project

Start the stack with `docker compose`.

```shell
docker compose up -d
```

This pulls the needed images and starts Plone.


## Access Plone via Browser

After startup, go to `http://plone.localhost/` and you should see the site.


## Increase the number of backends

To use two containers for the backend, run `docker compose` with `--scale`.

```shell
docker compose up --scale backend=2
```


## Shutdown and cleanup

The command `docker compose down` removes the containers and default network, but preserves the Plone database.

The command `docker compose down --volumes` removes the containers, default network, and the Plone database.
