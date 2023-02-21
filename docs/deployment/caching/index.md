---
myst:
  html_meta:
    "description": "Caching Plone"
    "property=og:description": "Caching Plone"
    "property=og:title": "Caching Plone"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-label)=

# Caching

## Overview

HTTP caching is a technique used to speed up the delivery of web content by storing previously requested resources (such as images, scripts, and stylesheets) in a cache. 
When a user requests a resource, the cache can serve the resource directly from its storage, rather than having to fetch it from the original source.

It is possible to use a web accelerator, like {term}`Varnish` to implement HTTP caching in your own premises. 
The usual setup will have the web accelerator installed between Plone and the Internet, and when a request is made to the site the web accelerator will intercept the request and check to see if it has a cached copy of the requested resource. 
If a cached copy is found, the accelerator will serve the cached copy directly to the client, otherwise it will make a request to the backend Plone server and then store a copy on the content in its local cache.

HTTP caching and the speed of delivering web content can be improved using a Content Delivery Network (CDN).
A CDN is a network of servers located in various geographic regions that work together to deliver web content to users quickly and efficiently. 
When a user requests a resource from a website that uses a CDN, the request is directed to the closest server in the CDN, rather than having to travel all the way to the website's origin server.

## Plone support

Plone ships with a powerful and extensible `HTTP` and `In-Memory` cache support, implemented by the package `plone.app.caching`.


```{toctree}
:maxdepth: 2
:hidden: true

enable
control-panel
profiles
rulesets-and-caching-operations
proxies
ram-cache
etags
composite-views
restapi
```
