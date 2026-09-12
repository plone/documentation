---
myst:
  html_meta:
    "description": "Plone 6 stack for Docker Swarm with Traefik, Varnish, a scalable frontend and backend, and a ZEO server."
    "property=og:description": "Plone 6 stack for Docker Swarm with Traefik, Varnish, a scalable frontend and backend, and a ZEO server."
    "property=og:title": "Docker Swarm: Traefik, Frontend, Backend, ZEO, Varnish example"
    "keywords": "Plone 6, Container, Docker, Docker Swarm, Traefik, Frontend, Backend, ZEO, Varnish"
---

# Docker Swarm: Traefik, Frontend, Backend, ZEO, Varnish example

This example deploys Plone 6 as a stack on a Docker Swarm cluster, with {term}`Varnish` caching the responses of the frontend and the backend.
The stack runs the following services.

`traefik`
:   {term}`Traefik Proxy` routes requests to the other services, and gets TLS certificates from Let's Encrypt.

`socket-proxy`
:   Gives Traefik access to the parts of the Docker API it needs, instead of the Docker socket itself.

`varnish`
:   Caches responses, with two replicas by default.

`purger`
:   Receives purge requests from the backend, and forwards them to every Varnish replica.

`frontend`
:   The Plone frontend, with two replicas by default.

`backend`
:   The Plone backend, with two replicas by default, which stores its data in the ZEO server.

`db`
:   The ZEO server, with its data persisted in a Docker volume.

Traefik receives public requests over HTTPS, and sends them to Varnish.
Varnish adds the `X-Varnish-Routed: 1` header to each request that it doesn't serve from its cache, and sends the request back to Traefik on port 8081, which routes it to the frontend or the backend.
The stack doesn't publish port 8081, so clients can only reach the site over HTTPS.
Requests to the Classic UI at `/ClassicUI` go straight from Traefik to the backend.


## Prerequisites

-   A Docker Swarm cluster.
    To create a cluster with a single node, run `docker swarm init` on that node.
-   DNS records that point the host names of `STACK_HOSTNAME`, `STACK_HOSTNAME_REDIRECT`, and `TRAEFIK_HOSTNAME` to your cluster.
-   Ports 80 and 443 open to the internet, so Let's Encrypt can validate your host names.


## Setup

Create an empty project directory named `swarm-traefik-volto-plone-varnish`.

```shell
mkdir swarm-traefik-volto-plone-varnish
```

Change into your project directory.

```shell
cd swarm-traefik-volto-plone-varnish
```


### Create the public network

Traefik and the services it routes requests to share an overlay network named `nw-public`.
Create it once on a manager node, before you deploy the stack.

```shell
docker network create --driver overlay nw-public
```


### Varnish configuration

Create a directory named `etc`.

```shell
mkdir etc
```

Create a file named `etc/varnish.vcl` with the following content.
It differs from the file in the {doc}`Docker Compose example <../compose/traefik-volto-plone-varnish>` in two places.
The backend is port 8081 of `traefik`, the name of the Traefik service in the stack, and the `purge` access control list doesn't include the `backend` host name.

```vcl
vcl 4.0;

import std;
import directors;

backend traefik_loadbalancer {
    .host = "traefik";
    .port = "8081";
    .connect_timeout = 2s;
    .first_byte_timeout = 300s;
    .between_bytes_timeout  = 60s;
}

/* Only allow PURGE from localhost and API-Server */
acl purge {
  "localhost";
  "127.0.0.1";
  "172.16.0.0/12";
  "10.0.0.0/8";
  "192.168.0.0/16";
}

sub detect_protocol{
  unset req.http.X-Forwarded-Proto;
  set req.http.X-Forwarded-Proto = "http";
}

sub detect_debug{
  # Requests with X-Varnish-Debug will display additional
  # information about requests
  unset req.http.x-vcl-debug;
  # Should be changed after switch to live
  if (req.http.x-varnish-debug) {
      set req.http.x-vcl-debug = false;
  }
}

sub detect_auth{
  unset req.http.x-auth;
  if (
      (req.http.Cookie && (
        req.http.Cookie ~ "__ac(_(name|password|persistent))?=" || req.http.Cookie ~ "_ZopeId" || req.http.Cookie ~ "auth_token")) ||
      (req.http.Authenticate) ||
      (req.http.Authorization)
  ) {
    set req.http.x-auth = true;
  }
}

sub detect_requesttype{
  unset req.http.x-varnish-reqtype;
  set req.http.x-varnish-reqtype = "Default";
  if (req.http.x-auth){
    set req.http.x-varnish-reqtype = "auth";
  } elseif (req.url ~ "\/@@(images|download|)\/?(.*)?$"){
    set req.http.x-varnish-reqtype = "blob";
  } elseif (req.url ~ "\/\+\+api\+\+/?(.*)?$") {
    set req.http.x-varnish-reqtype = "api";
  } else {
    set req.http.x-varnish-reqtype = "express";
  }
}

sub process_redirects{
  // Add manual redurect
  if (req.url ~ "^/old-folder/(.*)") {
    set req.http.x-redirect-to = regsub(req.url, "^/old-folder/(.*)", "^/new-folder/\1");
  }

  if (req.http.x-redirect-to) {
    return (synth(301, req.http.x-redirect-to));
  }
}

sub vcl_init {
  new cluster_loadbalancer = directors.round_robin();
  cluster_loadbalancer.add_backend(traefik_loadbalancer);
}

sub vcl_recv {
  set req.backend_hint = cluster_loadbalancer.backend();
  set req.http.X-Varnish-Routed = "1";

  # Annotate request with x-forwarded-proto
  # We always serve requests over https, but talk to Traefik
  # and then to Volto and Plone using http.
  call detect_protocol;

  # Annotate request with x-vcl-debug
  call detect_debug;

  # Annotate request with x-auth indicating if request is authenticated or not
  call detect_auth;

  # Annotate request with x-varnish-reqtype with a classification for the request
  call detect_requesttype;

  # Process redirects
  call process_redirects;

  # Sanitize cookies so they do not needlessly destroy cacheability for anonymous pages
  if (req.http.Cookie) {
    set req.http.Cookie = ";" + req.http.Cookie;
    set req.http.Cookie = regsuball(req.http.Cookie, "; +", ";");
    set req.http.Cookie = regsuball(req.http.Cookie, ";(sticky|I18N_LANGUAGE|statusmessages|__ac|_ZopeId|__cp|beaker\.session|authomatic|serverid|__rf|auth_token)=", "; \1=");
    set req.http.Cookie = regsuball(req.http.Cookie, ";[^ ][^;]*", "");
    set req.http.Cookie = regsuball(req.http.Cookie, "^[; ]+|[; ]+$", "");

    if (req.http.Cookie == "") {
        unset req.http.Cookie;
    }
  }

  if (req.http.x-auth) {
    return(pass);
  }

  if (req.method == "PURGE") {
      if (!client.ip ~ purge) {
          return (synth(405, "Not allowed."));
      } else {
          ban("req.url == " + req.url);
          return (synth(200, "Purged."));
      }

  } elseif (req.method == "BAN") {
      # Same ACL check as above:
      if (!client.ip ~ purge) {
          return (synth(405, "Not allowed."));
      }
      ban("req.http.host == " + req.http.host + "&& req.url == " + req.url);
      # Throw a synthetic page so the
      # request won't go to the backend.
      return (synth(200, "Ban added"));

  } elseif (req.method != "GET" &&
      req.method != "HEAD" &&
      req.method != "PUT" &&
      req.method != "POST" &&
      req.method != "PATCH" &&
      req.method != "TRACE" &&
      req.method != "OPTIONS" &&
      req.method != "DELETE") {
      /* Non-RFC2616 or CONNECT which is weird. */
      return (pipe);
  } elseif (req.method != "GET" &&
      req.method != "HEAD" &&
      req.method != "OPTIONS") {
      /* POST, PUT, PATCH will pass, always */
      return(pass);
  }

  return(hash);
}

sub vcl_pipe {
  /* This is not necessary if you do not do any request rewriting. */
  set req.http.connection = "close";
}

sub vcl_purge {
  return (synth(200, "PURGE: " + req.url + " - " + req.hash));
}

sub vcl_synth {
  if (resp.status == 301) {
    set resp.http.location = resp.reason;
    set resp.reason = "Moved";
    return (deliver);
  }
}

sub vcl_hit {
  if (obj.ttl >= 0s) {
    // A pure unadulterated hit, deliver it
    return (deliver);
  } elsif (obj.ttl + obj.grace > 0s) {
    // Object is in grace, deliver it
    // Automatically triggers a background fetch
    return (deliver);
  } else {
    return (restart);
  }
}


sub vcl_backend_response {

  # Don't allow static files to set cookies.
  # (?i) denotes case insensitive in PCRE (perl compatible regular expressions).
  # make sure you edit both and keep them equal.
  if (bereq.url ~ "(?i)\.(pdf|asc|dat|txt|doc|xls|ppt|tgz|png|gif|jpeg|jpg|ico|swf|css|js)(\?.*)?$") {
    unset beresp.http.set-cookie;
  }
  if (beresp.http.Set-Cookie) {
    set beresp.http.x-varnish-action = "FETCH (pass - response sets cookie)";
    set beresp.uncacheable = true;
    set beresp.ttl = 120s;
    return(deliver);
  }
  if (beresp.http.Cache-Control ~ "(private|no-cache|no-store)") {
    set beresp.http.x-varnish-action = "FETCH (pass - cache control disallows)";
    set beresp.uncacheable = true;
    set beresp.ttl = 120s;
    return(deliver);
  }

  # if (beresp.http.Authorization && !beresp.http.Cache-Control ~ "public") {
  # Do NOT cache if there is an "Authorization" header
  # beresp never has an Authorization header in beresp, right?
  if (beresp.http.Authorization) {
    set beresp.http.x-varnish-action = "FETCH (pass - authorized and no public cache control)";
    set beresp.uncacheable = true;
    set beresp.ttl = 120s;
    return(deliver);
  }

  # Use this rule IF no cache-control (SSR content)
  if ((bereq.http.x-varnish-reqtype ~ "express") && (!beresp.http.Cache-Control)) {
    set beresp.http.x-varnish-action = "INSERT (30s caching / 60s grace)";
    set beresp.uncacheable = false;
    set beresp.ttl = 30s;
    set beresp.grace = 60s;
    return(deliver);
  }

  if (!beresp.http.Cache-Control) {
    set beresp.http.x-varnish-action = "FETCH (override - backend not setting cache control)";
    set beresp.uncacheable = true;
    set beresp.ttl = 120s;
    return (deliver);
  }

  if (beresp.http.X-Anonymous && !beresp.http.Cache-Control) {
    set beresp.http.x-varnish-action = "FETCH (override - anonymous backend not setting cache control)";
    set beresp.ttl = 600s;
    return (deliver);
  }

  set beresp.http.x-varnish-action = "FETCH (insert)";
  return (deliver);
}

sub vcl_deliver {

  if (req.http.x-vcl-debug) {
    set resp.http.x-varnish-ttl = obj.ttl;
    set resp.http.x-varnish-grace = obj.grace;
    set resp.http.x-hits = obj.hits;
    set resp.http.x-varnish-reqtype = req.http.x-varnish-reqtype;
    if (req.http.x-auth) {
      set resp.http.x-auth = "Logged-in";
    } else {
      set resp.http.x-auth = "Anon";
    }
    if (obj.hits > 0) {
      set resp.http.x-cache = "HIT";
    } else {
      set resp.http.x-cache = "MISS";
    }
  } else {
    unset resp.http.x-varnish-action;
    unset resp.http.x-cache-operation;
    unset resp.http.x-cache-rule;
    unset resp.http.x-powered-by;
  }
}
```


### Stack file

Create a `stack.yml` file with the following content.

```yaml
services:

  socket-proxy:
    image: tecnativa/docker-socket-proxy
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock
    environment:
      NODES: 1
      SERVICES: 1
      TASKS: 1
      NETWORKS: 1
    networks:
      - nw-traefik
    deploy:
      placement:
        constraints:
          - node.role == manager

  traefik:
    image: traefik:{TRAEFIK_VERSION}
    ports:
      - "80:80"
      - "443:443"
    volumes:
      - vol-traefik-certs:/certificates
    command:
      - --providers.swarm
      - --providers.swarm.endpoint=tcp://socket-proxy:2375
      - --providers.swarm.exposedbydefault=false
      - --providers.swarm.network=nw-public
      - --providers.swarm.constraints=Label(`traefik.constraint-label`, `public`)
      - --entrypoints.http.address=:80
      - --entrypoints.https.address=:443
      - --entrypoints.varnish.address=:8081   # requests from Varnish, not published
      - --certificatesresolvers.le.acme.email=${TRAEFIK_EMAIL:?Set TRAEFIK_EMAIL}
      - --certificatesresolvers.le.acme.storage=/certificates/acme.json
      - --certificatesresolvers.le.acme.tlschallenge=true
      - --accesslog
      - --accesslog.format=json
      - --log.level=INFO
      - --log.format=json
      - --api
    networks:
      - nw-public
      - nw-traefik
    deploy:
      replicas: 1
      placement:
        constraints:
          - node.role == manager
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        - traefik.http.services.traefik-public.loadbalancer.server.port=8000

        # Dashboard
        - traefik.http.middlewares.admin-auth.basicauth.users=${TRAEFIK_BASIC_AUTH:?Set TRAEFIK_BASIC_AUTH}
        - traefik.http.routers.traefik-dashboard.rule=Host(`${TRAEFIK_HOSTNAME:?Set TRAEFIK_HOSTNAME}`)
        - traefik.http.routers.traefik-dashboard.entrypoints=https
        - traefik.http.routers.traefik-dashboard.tls=true
        - traefik.http.routers.traefik-dashboard.tls.certresolver=le
        - traefik.http.routers.traefik-dashboard.service=api@internal
        - traefik.http.routers.traefik-dashboard.middlewares=admin-auth

        # Generic middlewares
        - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
        - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
        - traefik.http.middlewares.gzip.compress=true
        - traefik.http.middlewares.gzip.compress.excludedcontenttypes=image/png, image/jpeg, font/woff2

        # Redirect every HTTP request to HTTPS
        - traefik.http.routers.generic-https-redirect.entrypoints=http
        - traefik.http.routers.generic-https-redirect.rule=HostRegexp(`^.+$$`)
        - traefik.http.routers.generic-https-redirect.priority=1
        - traefik.http.routers.generic-https-redirect.middlewares=https-redirect

  varnish:
    image: varnish
    configs:
      - source: varnish-vcl
        target: /etc/varnish/default.vcl
    networks:
      - nw-public
      - nw-internal
    deploy:
      replicas: ${STACK_VARNISH_REPLICAS:-2}
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        # Service
        - traefik.http.services.svc-${STACK_NAME:?Set STACK_NAME}-varnish.loadbalancer.server.port=80

        # Middleware
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.permanent=true
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.regex=^https://${STACK_HOSTNAME_REDIRECT:?Set STACK_HOSTNAME_REDIRECT}/(.*)
        - traefik.http.middlewares.mw-${STACK_NAME}-redirect.redirectregex.replacement=https://${STACK_HOSTNAME:?Set STACK_HOSTNAME}/$${1}

        # Routers
        ## Redirect
        - traefik.http.routers.rt-${STACK_NAME}-varnish-redirect.rule=Host(`${STACK_HOSTNAME_REDIRECT}`)
        - traefik.http.routers.rt-${STACK_NAME}-varnish-redirect.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-varnish-redirect.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-varnish-redirect.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-varnish-redirect.middlewares=mw-${STACK_NAME}-redirect
        ## Public requests
        - traefik.http.routers.rt-${STACK_NAME}-varnish.rule=Host(`${STACK_HOSTNAME}`)
        - traefik.http.routers.rt-${STACK_NAME}-varnish.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-varnish.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-varnish.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-varnish.service=svc-${STACK_NAME}-varnish
        - traefik.http.routers.rt-${STACK_NAME}-varnish.middlewares=gzip

  purger:
    image: ghcr.io/kitconcept/cluster-purger:latest
    environment:
      PURGER_MODE: swarm
      PURGER_SERVICE_NAME: ${STACK_NAME}_varnish
      PURGER_SERVICE_PORT: 80
      PURGER_PUBLIC_SITES: "['${STACK_HOSTNAME}']"
    networks:
      - nw-internal
    deploy:
      replicas: 2
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first

  frontend:
    image: plone/plone-frontend:{PLONE_FRONTEND_VERSION}
    environment:
      RAZZLE_INTERNAL_API_PATH: http://${STACK_NAME}_backend:8080/Plone
      RAZZLE_API_PATH: https://${STACK_HOSTNAME}
    networks:
      - nw-public
      - nw-internal
    deploy:
      replicas: ${STACK_FRONT_REPLICAS:-2}
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        # Service
        - traefik.http.services.svc-${STACK_NAME}-frontend.loadbalancer.server.port=3000

        # Routers
        ## / (requests from Varnish)
        - traefik.http.routers.rt-${STACK_NAME}-frontend.rule=Host(`${STACK_HOSTNAME}`) && Header(`X-Varnish-Routed`, `1`)
        - traefik.http.routers.rt-${STACK_NAME}-frontend.entrypoints=varnish
        - traefik.http.routers.rt-${STACK_NAME}-frontend.service=svc-${STACK_NAME}-frontend

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
    environment:
      SITE: Plone
      PROFILES: "plone.app.caching:with-caching-proxy"
      ZEO_ADDRESS: "${STACK_NAME}_db:8100"
    networks:
      - nw-public
      - nw-internal
    deploy:
      replicas: ${STACK_BACK_REPLICAS:-2}
      update_config:
        parallelism: 1
        delay: 5s
        order: start-first
      labels:
        - traefik.enable=true
        - traefik.constraint-label=public
        # Service
        - traefik.http.services.svc-${STACK_NAME}-backend.loadbalancer.server.port=8080

        # Middlewares
        ## Virtual Host Monster rewrite for /++api++/
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-api.replacepathregex.regex=^/\\+\\+api\\+\\+($$|/.*)"
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-api.replacepathregex.replacement=/VirtualHostBase/https/${STACK_HOSTNAME}/Plone/++api++/VirtualHostRoot$$1"
        ## Virtual Host Monster rewrite for /ClassicUI/
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-classic.replacepathregex.regex=^/ClassicUI($$|/.*)"
        - "traefik.http.middlewares.mw-${STACK_NAME}-backend-vhm-classic.replacepathregex.replacement=/VirtualHostBase/https/${STACK_HOSTNAME}/Plone/VirtualHostRoot/_vh_ClassicUI$$1"
        ## Basic authentication for /ClassicUI/
        - traefik.http.middlewares.mw-${STACK_NAME}-backend-auth.basicauth.users=${BASIC_AUTH_USER:?Set BASIC_AUTH_USER}:${BASIC_AUTH_PASSWORD_HASH:?Set BASIC_AUTH_PASSWORD_HASH}

        # Routers
        ## /++api++ (requests from Varnish)
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.rule=Host(`${STACK_HOSTNAME}`) && PathPrefix(`/++api++`) && Header(`X-Varnish-Routed`, `1`)
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.entrypoints=varnish
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.service=svc-${STACK_NAME}-backend
        - traefik.http.routers.rt-${STACK_NAME}-backend-api.middlewares=mw-${STACK_NAME}-backend-vhm-api
        ## /ClassicUI
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.rule=Host(`${STACK_HOSTNAME}`) && PathPrefix(`/ClassicUI`)
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.entrypoints=https
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.tls=true
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.tls.certresolver=le
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.service=svc-${STACK_NAME}-backend
        - traefik.http.routers.rt-${STACK_NAME}-backend-classic.middlewares=gzip,mw-${STACK_NAME}-backend-auth,mw-${STACK_NAME}-backend-vhm-classic

  db:
    image: plone/plone-zeo:{PLONE_ZEO_VERSION}
    volumes:
      - vol-site-data:/data
    networks:
      - nw-internal
    deploy:
      replicas: 1
      update_config:
        parallelism: 1
        delay: 1s
        order: stop-first

configs:
  varnish-vcl:
    file: ./etc/varnish.vcl

volumes:
  vol-traefik-certs: {}
  vol-site-data: {}

networks:
  nw-public:
    external: true
  nw-traefik:
    driver: overlay
    internal: true
  nw-internal:
    driver: overlay
    internal: true
```

Docker Swarm stores the content of `etc/varnish.vcl` under the name `varnish-vcl`, and you can't change it after you deploy the stack.
To change the Varnish configuration later, rename `varnish-vcl` in both places in `stack.yml`, for example to `varnish-vcl-2`, and deploy the stack again.

```{warning}
Docker volumes are local to the node where they're created.
In a cluster with more than one node, add a placement constraint to the `db` service, so the ZEO server always runs on the node that holds its data.
```


### Environment variables

The stack reads its configuration from the following environment variables.
Variables without a default value are required, and `docker stack deploy` stops with an error if one of them is missing.

| Variable | Description | Default value | Example |
| --- | --- | --- | --- |
| `STACK_NAME` | Name of the stack, which must match the name you pass to `docker stack deploy`. The services use it to reach each other, and Traefik uses it to name routers, services, and middleware. | | `plone` |
| `STACK_HOSTNAME` | Public host name of the site | | `www.example.com` |
| `STACK_HOSTNAME_REDIRECT` | Host name that permanently redirects to `STACK_HOSTNAME` | | `example.com` |
| `STACK_VARNISH_REPLICAS` | Number of Varnish replicas | `2` | `3` |
| `STACK_FRONT_REPLICAS` | Number of frontend replicas | `2` | `3` |
| `STACK_BACK_REPLICAS` | Number of backend replicas | `2` | `4` |
| `TRAEFIK_HOSTNAME` | Host name of the Traefik dashboard | | `traefik.example.com` |
| `TRAEFIK_EMAIL` | Email address of your Let's Encrypt account | | `admin@example.com` |
| `TRAEFIK_BASIC_AUTH` | User name and password hash for the Traefik dashboard, in the format `user:hash` | | `admin:$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0` |
| `BASIC_AUTH_USER` | User name for the Classic UI at `/ClassicUI` | | `admin` |
| `BASIC_AUTH_PASSWORD_HASH` | Password hash for the Classic UI at `/ClassicUI` | | `$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0` |

To create a password hash, run the following command, with your password instead of `secret`.

```shell
openssl passwd -apr1 secret
```

Create a `.env` file with your values.
Wrap values that contain a dollar sign, such as password hashes, in single quotes.

```shell
STACK_NAME=plone
STACK_HOSTNAME=www.example.com
STACK_HOSTNAME_REDIRECT=example.com
TRAEFIK_HOSTNAME=traefik.example.com
TRAEFIK_EMAIL=admin@example.com
TRAEFIK_BASIC_AUTH='admin:$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0'
BASIC_AUTH_USER=admin
BASIC_AUTH_PASSWORD_HASH='$apr1$Zq3mQ2vH$IX.Ug0PreO6h.m494Bn9L0'
```

`docker stack deploy` doesn't read `.env` files.
Load the variables into your shell before you deploy.

```shell
set -a
. ./.env
set +a
```


## Deploy the stack

Deploy the stack with the name from `STACK_NAME`.

```shell
docker stack deploy -c stack.yml "$STACK_NAME"
```

This pulls the needed images and starts Plone.


## Configure cache purging

The `plone.app.caching:with-caching-proxy` profile sets up caching rules for the site, but it doesn't set where the backend sends purge requests.
Go to the caching control panel at `https://www.example.com/ClassicUI/@@caching-controlpanel`, using your value of `STACK_HOSTNAME`, and set the following options.

{guilabel}`Enable purging`
:   Selected

{guilabel}`Caching proxies`
:   `http://purger`

{guilabel}`Send PURGE requests with virtual hosting paths`
:   Cleared

The backend then sends purge requests to the `purger` service, which forwards them to every Varnish replica.


## Access Plone

After startup, go to `https://www.example.com`, using your value of `STACK_HOSTNAME`, and you should see the site.

The Classic UI is available at `https://www.example.com/ClassicUI`, behind the user name and password from `BASIC_AUTH_USER` and `BASIC_AUTH_PASSWORD_HASH`.

The Traefik dashboard is available at the host name from `TRAEFIK_HOSTNAME`, behind the user name and password from `TRAEFIK_BASIC_AUTH`.


## Increase the number of backends

To run four backend replicas, scale the backend service.

```shell
docker service scale "${STACK_NAME}_backend=4"
```

The next `docker stack deploy` sets the number of replicas back to the value of `STACK_BACK_REPLICAS`.


## Shutdown and cleanup

The command `docker stack rm "$STACK_NAME"` removes the services and the stack networks, but preserves the Plone database and the TLS certificates in their volumes.
