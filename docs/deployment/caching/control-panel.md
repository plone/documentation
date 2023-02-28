---
myst:
  html_meta:
    "description": "Caching control panel for Plone"
    "property=og:description": "Caching control panel for Plone"
    "property=og:title": "Caching Control Panel"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-control-panel-label)=

# Control panel

The Caching control panel in Plone's `Site Setup` supports a granular control of caching operations for a Plone site.

````{card}
```{image} /_static/caching/caching-disabled.png
:alt: Caching Control Panel
:target: /_static/caching/caching-disabled.png
```
+++
_Caching Control Panel_
````

This control panel consists of four main tabs:

## {guilabel}`Change settings`

Where you can control caching behaviour, it contains five fieldsets:

### {guilabel}`Global settings`

For global options, such as turning caching on or off.

### {guilabel}`Caching proxies`

Where you can control Plone's use of a caching proxy, such as Varnish or a CDN.

### {guilabel}`In-memory cache`

Where you can control Plone's use of in-memory cache.

### {guilabel}`Caching operation`

Where caching rulesets (hints about views and resources used for caching purposes) can be associated with caching operations.

Those either intercept a request to return a cached response, or modify a response to add cache control headers.

This is also where rulesets for legacy page templates (created through the web or the  `portal_skins` tool) are configured.

### {guilabel}`Detailed settings`

Where you can configure parameters for individual caching operations.


## {guilabel}`Import settings`

Where you can import pre-defined profiles of cache settings.

## {guilabel}`Purge caching proxy`

Where you can manually purge content from a caching proxy.

This tab only appears if you have purging enabled under {guilabel}`Change settings`.

## {guilabel}`RAM cache`

Where you can view statistics about and purge the RAM cache.
