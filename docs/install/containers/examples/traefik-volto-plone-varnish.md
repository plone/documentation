---
myst:
  html_meta:
    "description": "Very simple Plone 6 setup with only one backend and data being persisted in a Docker volume."
    "property=og:description": "Very simple Plone 6 setup with only one backend and data being persisted in a Docker volume."
    "property=og:title": "Traefik Proxy, Frontend, Backend, Varnish container example"
    "keywords": "Plone 6, Container, Docker, Traefik Proxy, Frontend, Backend, Varnish"
---

# Traefik Proxy, Frontend, Backend, Varnish container example

This example is a very simple setup with one backend and data being persisted in a Docker volume.

{term}`Traefik Proxy` in this example is used as a reverse proxy.

{term}`Varnish` is used for caching.

A purger component is also used. This solves the problem of invalidating the cache in multiple Varnish servers, which could be desirable in containerized deployment.

## Create a project space

Create an empty project directory named `traefik-volto-plone-varnish`.

```shell
mkdir traefik-volto-plone-varnish
```

Change into your project directory.

```shell
cd traefik-volto-plone-varnish
```


## Varnish configuration

Create an empty directory named `etc`.

```shell
mkdir etc
```

Add there a file {file}`varnish.vcl` that will be used by the Varnish image:

```vcl
vcl 4.0;

import std;
import directors;

backend traefik_loadbalancer {
    .host = "webserver";
    .port = "80";
    .connect_timeout = 2s;
    .first_byte_timeout = 300s;
    .between_bytes_timeout  = 60s;
}

/* Only allow PURGE from localhost and API-Server */
acl purge {
  "localhost";
  "backend";
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

```{note}
`http://plone.localhost/` is the URL you will be using to access the website.
You can either use `localhost`, or add it in your `/etc/hosts` file or DNS to point to the Docker host IP.
```

## Service configuration with Docker Compose

Now let's create a {file}`docker-compose.yml` file:

```yaml
version: "3"
services:
  webserver:
    image: traefik

    ports:
      - 80:80

    labels:
      - traefik.enable=true
      - traefik.constraint-label=public

      # GENERIC MIDDLEWARES
      # - traefik.http.middlewares.https-redirect.redirectscheme.scheme=https
      # - traefik.http.middlewares.https-redirect.redirectscheme.permanent=true
      - traefik.http.middlewares.gzip.compress=true
      - traefik.http.middlewares.gzip.compress.excludedcontenttypes=image/png, image/jpeg, font/woff2

      # GENERIC ROUTERS
      # - traefik.http.routers.generic-https-redirect.entrypoints=http
      # - traefik.http.routers.generic-https-redirect.rule=HostRegexp(`{host:.*}`)
      # - traefik.http.routers.generic-https-redirect.priority=1
      # - traefik.http.routers.generic-https-redirect.middlewares=https-redirect

    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro

    command:
      - --providers.docker
      - --providers.docker.constraints=Label(`traefik.constraint-label`, `public`)
      - --providers.docker.exposedbydefault=false
      - --entrypoints.http.address=:80
      # - --entrypoints.https.address=:443
      - --accesslog
      - --accesslog.format=json
      - --accesslog.fields.headers.names.X-Varnish-Routed=keep
      - --accesslog.fields.headers.names.RequestHost=keep
      - --log
      - --log.level=DEBUG
      - --api

  frontend:
    image: plone/plone-frontend:latest
    environment:
      RAZZLE_INTERNAL_API_PATH: http://backend:8080/Plone
      RAZZLE_API_PATH: http://plone.localhost
      DEBUG: superagent
    labels:
      - traefik.enable=true
      - traefik.constraint-label=public
      # Service
      - traefik.http.services.svc-frontend.loadbalancer.server.port=3000
      # Router: Varnish Public
      - traefik.http.routers.rt-frontend-public.rule=Host(`plone.localhost`)
      - traefik.http.routers.rt-frontend-public.entrypoints=http
      - traefik.http.routers.rt-frontend-public.service=svc-varnish
      - traefik.http.routers.rt-frontend-public.middlewares=gzip
      # Router: Internal
      - traefik.http.routers.rt-frontend-internal.rule=Host(`plone.localhost`) && Headers(`X-Varnish-Routed`, `1`)
      - traefik.http.routers.rt-frontend-internal.entrypoints=http
      - traefik.http.routers.rt-frontend-internal.service=svc-frontend
    depends_on:
      - backend
    ports:
      - "3000:3000"

  backend:
    image: plone/plone-backend:{PLONE_BACKEND_MINOR_VERSION}
    environment:
      SITE: Plone
      PROFILES: "plone.app.caching:with-caching-proxy"
    labels:
      - traefik.enable=true
      - traefik.constraint-label=public
      # Service
      - traefik.http.services.svc-backend.loadbalancer.server.port=8080
      # Middleware
      ## Virtual Host Monster for /++api++/
      - "traefik.http.middlewares.mw-backend-vhm-api.replacepathregex.regex=^/\\+\\+api\\+\\+($$|/.*)"
      - "traefik.http.middlewares.mw-backend-vhm-api.replacepathregex.replacement=/VirtualHostBase/http/plone.localhost/Plone/++api++/VirtualHostRoot$$1"
      ## Virtual Host Monster for /ClassicUI/
      - "traefik.http.middlewares.mw-backend-vhm-ui.replacepathregex.regex=^/ClassicUI($$|/.*)"
      - "traefik.http.middlewares.mw-backend-vhm-ui.replacepathregex.replacement=/VirtualHostBase/http/plone.localhost/Plone/VirtualHostRoot/_vh_ClassicUI$$1"
      # Router: Varnish Public
      ## /++api++/
      - traefik.http.routers.rt-backend-api-public.rule=Host(`plone.localhost`) && PathPrefix(`/++api++`)
      - traefik.http.routers.rt-backend-api-public.entrypoints=http
      - traefik.http.routers.rt-backend-api-public.service=svc-varnish
      - traefik.http.routers.rt-backend-api-public.middlewares=gzip
      # Router: Internal
      ## /++api++/
      - traefik.http.routers.rt-backend-api-internal.rule=Host(`plone.localhost`) && PathPrefix(`/++api++`) && Headers(`X-Varnish-Routed`, `1`)
      - traefik.http.routers.rt-backend-api-internal.entrypoints=http
      - traefik.http.routers.rt-backend-api-internal.service=svc-backend
      - traefik.http.routers.rt-backend-api-internal.middlewares=gzip,mw-backend-vhm-api
      ## /ClassicUI/
      - traefik.http.routers.rt-backend-ui-internal.rule=Host(`plone.localhost`) && PathPrefix(`/ClassicUI`) && Headers(`X-Varnish-Routed`, `1`)
      - traefik.http.routers.rt-backend-ui-internal.entrypoints=http
      - traefik.http.routers.rt-backend-ui-internal.service=svc-backend
      - traefik.http.routers.rt-backend-ui-internal.middlewares=gzip,mw-backend-vhm-ui
    ports:
      - "8080:8080"

  purger:
    image: ghcr.io/kitconcept/cluster-purger:latest
    platform: linux/amd64
    environment:
      PURGER_SERVICE_NAME: varnish
      PURGER_SERVICE_PORT: 80
      PURGER_MODE: "compose"
      PURGER_PUBLIC_SITES: "['plone.localhost']"

  varnish:
    image: varnish
    volumes:
      - ./etc/varnish.vcl:/etc/varnish/default.vcl
    labels:
      - traefik.enable=true
      - traefik.constraint-label=public
      # SERVICE
      - traefik.http.services.svc-varnish.loadbalancer.server.port=80
    networks:
      default:
        aliases:
          - plone.localhost
    ports:
      - "8000-8001:80"
    depends_on:
      - backend
```


## Build the project

Start the stack with `docker compose`.

```shell
docker compose up -d
```

This pulls the needed images and starts Plone.


## Access Plone via Browser

After startup, go to `http://plone.localhost/` and you should see the site.


## Shutdown and cleanup

The command `docker compose down` removes the containers and default network, but preserves the Plone database.

The command `docker compose down --volumes` removes the containers, default network, and the Plone database.
