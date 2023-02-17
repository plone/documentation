---
myst:
  html_meta:
    "description": "Caching support for Rest API"
    "property=og:description": "Caching support for Rest API"
    "property=og:title": "Caching support for Rest API"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-restapi-label)=

# Rest API support

## Strategy

Caching for anonymous users for all GET requests.

Remark: Some POST requests, like `@querystring`, should be turned into GET in order to better cache.

We have endpoints following classic `plone.content.itemView` content and do not accept parameters.
Those can be handled with the default rules, including purge.

There are others delivering dynamic content, like search, impossible to purge.
Those shall be cached using a shorttime cache (like some seconds to some minutes).

This get covered by the rulesetType `plone.content.dynamic`.
It is configured to cache by default in browser 10sec, in caching-proxy 60 seconds.
Its goal is primary to reduce the load/peak-load on the server.
Also, it reduces the impact of loading the same endpoint more than one time in one page.


## plone.restapi GET endpoints

And its environment and assignments:

- `@actions`

  - Anonymous
  - rule plone.content.dynamic (might be influenced by other content)
  - purge

- `@addons`

  - Authenticated
  - no rule assignment

- `@breadcrumbs`

  - Anonymous
  - rule plone.content.dynamic (parent may change)
  - purge

- `@comments`

  - Anonymous
  - rule plone.content.itemView
  - purge

- `/` (content)

  - Anonymous
  - expander!
  - rule plone.content.dynamic

- `@history`

  - Authenticated
  - no rule assignment

- `@lock`

  - Authenticated
  - no rule assignment

- `@translations`

  - Anonymous
  - with parameters
  - rule plone.content.dynamic

- `@translations-locator`

  - Authenticated
  - no rule assignment

- `@navigation`

  - Anonymous
  - with parameters
  - rule plone.content.dynamic

- `@querysources`

  - Authenticated
  - with parameters
  - can not be cached

- `@querystring`

  - Anonymous
  - (values on IPloneSiteRoot from registry)
  - rule plone.content.dynamic

- `@querystring-search`

  - is in `get.py` BUT configured as POST
  - Anonymous
  - with json body
  - can not be cached

- `@registry`

  - Authenticated
  - with subpath
  - no rule assignment

- `@roles`

  - Authenticated
  - no rule assignment

- `@search`

  - Anonymous
  - with parameters
  - rule plone.content.dynamic

- `@sources`

  - Authenticated
  - no rule assignment

- `@tiles`

  - pre-deprecation
  - Anonymous
  - with subpath
  - no rule assignment

- `@types`

  - Authenticated
  - no rule assignment
