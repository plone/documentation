---
myst:
  html_meta:
    "description": "Control panel for Plone caching"
    "property=og:description": "Control panel for Plone caching"
    "property=og:title": "Caching Control Panel"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-control-panel-label)=

# Control panel

The Caching control panel in Plone's `Site Setup` supports a granular control of caching operations for a Plone site.

```{image} /_static/caching/ControlPanel-02.png
:alt: Plone Control Panel (Classic UI)
```

This control panel consists of four main tabs:

## `Change settings`

Where you can control caching behaviour, it contains four fieldsets:

### `Global settings`

For global options such as turning caching on or off.

### `Caching proxies`

Where you can control Plone's use of a caching proxy such or Varnish or a CDN.

### `In-memory cache`

Where you can control Plone's use of in-memory cache.

### `Caching operation`

Where caching rulesets (hints about views and resources used for caching purposes) can be associated with caching operations.

Those either intercept a request to return a cached response, or modifies a response to add cache control headers.

This is also where rulesets for legacy page templates (created through the web or the  portal_skins tool) are configured.

### `Detailed settings`

Where you can configure parameters for individual caching operations.


## `Import settings`

Where you can import pre-defined profiles of cache settings

## `Purge caching proxy`

Where you can manually purge content from a caching proxy.

This tab only appears if you have purging enabled under *Change settings*.

## `RAM cache`

Where you can view statistics about and purge the RAM cache.
