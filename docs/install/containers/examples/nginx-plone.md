---
myst:
  html_meta:
    "description": "Simple Plone 6 setup with one backend and data being persisted in a Docker volume."
    "property=og:description": "Simple Plone 6 setup with one backend and data being persisted in a Docker volume."
    "property=og:title": "nginx, Plone Classic container example"
    "keywords": "Plone 6, Container, Docker, nginx, Plone Classic"
---

# nginx, Plone Classic container example

This example is a simple setup with one backend and data being persisted in a Docker volume.

{term}`nginx` in this example is used as a [reverse proxy](https://docs.nginx.com/nginx/admin-guide/web-server/reverse-proxy/).


## Setup

Create an empty project directory named `nginx-plone`.

```shell
mkdir nginx-plone
```

Change into your project directory.

```shell
cd nginx-plone
```


### nginx configuration

Add a `default.conf` that will be used by the nginx image:

```nginx
upstream backend {
  server backend:8080;
}

server {
  listen 80 default_server;
  server_name plone.localhost;

  location / {
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_redirect http:// https://;
    if (!-f $request_filename) {
      rewrite ^/(.*)$ /VirtualHostBase/http/plone.localhost:80/Plone/VirtualHostRoot/$1;
    }
  }

  location /VirtualHostBase/ {
    proxy_pass http://backend;
  }
}
```

```{note}
`http://plone.localhost/` is the URL you will be using to access the website.
You can either use `plone.localhost`, or add it in your `/etc/hosts` file or DNS, to point to the Docker host IP.
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
    ports:
    - "80:80"

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
    environment:
      SITE: Plone
      TYPE: classic
    volumes:
      - data:/data
    ports:
    - "8080:8080"

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
You can also open the main Plone control page where you can create more Plone sites at `http://plone.localhost:8080`.


## Shutdown and cleanup

The command `docker compose down` removes the containers and default network, but preserves the Plone database.

The command `docker compose down --volumes` removes the containers, default network, and the Plone database.
