---
myst:
  html_meta:
    "description": "Caching content in Plone"
    "property=og:description": "Caching content in Plone"
    "property=og:title": "Caching content in Plone"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-label)=

# Caching

HTTP caching is a technique used to speed up the delivery of web content by storing previously requested resources, such as images, scripts, and stylesheets, in a cache.

A web accelerator, such as {term}`Varnish`, may be used to implement HTTP caching.
The usual set up will place the web accelerator between Plone and the Internet.
When a request is made to the site, the web accelerator will intercept the request.
It then checks to see if it has a cached copy of the requested resource.
If a cached copy is found, the accelerator will serve the cached copy directly to the client, else it will make a request to the backend Plone server and then store a copy on the content in its local cache.

HTTP caching and the speed of delivering web content can be improved using a {term}`Content Delivery Network` (CDN).
A CDN is a network of servers located in various geographic regions that work together to deliver web content to users quickly and efficiently.
When a user requests a resource from a website that uses a CDN, the request is directed to the closest server in the CDN, rather than having to travel all the way to the website's origin server.

## Cache support in Plone

Plone ships with powerful and extensible `HTTP` and `In-Memory` cache support, implemented by the package [`plone.app.caching`](https://github.com/plone/plone.app.caching/).


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
