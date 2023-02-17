# Composite views

A `composite view` is just a general term for most page views you see when you visit a Plone site.

It includes all content item views, content folder views, and many template views.

For our purposes, the distinguishing characteristic of composite views is the difficulty inherent in keeping track of all changes that might affect the final composited view.

Because of the difficulty of dependency tracking, composite views are often notoriously difficult to purge reliably from caching proxies so the default caching profiles set headers which expire the cache immediately (i.e. *weak caching*).

However, most of the inline resources linked to from the composite view (css, javascript, images, etc.) can be cached very well in proxy so the overall speed of most composite views will always be better with a caching proxy in front despite the page itself not being cached.

For relatively stable composite views or for those views for which you can tolerate some potential staleness, you might be tempted to try switching from *weak caching* to *moderate caching* with the `s-maxage` expiration value set to some tolerable value but first make sure you understand the issues regarding "split view" caching (see below).

A way to speedup a site with lots of composite view is to use "Terse" caching.

It caches a page for just a small time (be default 10s in browser and 60s in the caching proxy).

Thus the content is almost up to date, but on high load visitors are getting pages served from the cache.
