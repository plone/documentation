---
myst:
  html_meta:
    "description": "Caching composite views in Plone"
    "property=og:description": "Caching composite views in Plone"
    "property=og:title": "Caching composite views in Plone"
    "keywords": "Plone, deployment, automation, caching, composite views"
---

(caching-composite-views-label)=
# Composite views

The term *composite view* refers to most of the page views that are visible on a Plone website, including views of content listings, content folders, many template views, and rarely also specific content items.

These views can be difficult to manage because of the various changes that may affect the final composite view.
As a result, composite views are typically challenging to remove reliably from caching proxies.
To address this issue, the default caching profiles set headers that expire the cache immediately, a process known as *weak caching*.

However, the inline resources linked from the composite view—such as CSS, JavaScript, and images—can typically be cached effectively in proxies.
As a result, caching proxies can improve the overall speed of most composite views, even if the page itself is not cached.

For relatively stable composite views or views where some staleness is tolerable, it may be tempting to switch from *weak caching* to *terse caching* with the `s-maxage` expiration value set to 60 seconds by default.

To increase the speed of a site that contains many composite views, a technique called _Terse_ caching can be used.
Terse caching involves caching a page for a brief period, typically 10 seconds in the browser and 60 seconds in the caching proxy.
This ensures that the content is almost up to date, but during periods of high traffic, visitors may receive pages served from the cache.
This technique can actually speed up a site during periods of high traffic compared to low traffic since, during high traffic, the request can be served from the cache instead of having to go to the backend.
