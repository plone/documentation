---
myst:
  html_meta:
    "description": "Caching support for Plone REST API"
    "property=og:description": "Caching support for Plone REST API"
    "property=og:title": "Caching support for Plone REST API"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-restapi-label)=

# REST API support

This chapter describes techniques to implement caching with the Plone REST API.

## Strategy

This section desribes how to cache all GET requests from anonymous users.

```{note}
Some POST requests, such as `@querystring`, should be turned into GET to improve cache.
```

We have endpoints following classic `plone.content.itemView` content and do not accept parameters.
Those can be handled with the default rules, including purge.

There are others delivering dynamic content, such as search, which are impossible to purge.
Those will be cached using a transient cache, lasting a few seconds or minutes.

This gets covered by the `rulesetType` `plone.content.dynamic`.
By default it is configured to cache in the browser for 10 seconds, and in the caching proxy server for 60 seconds.
Its primary goal is to reduce the load and peak-load on the server.
Also it reduces the impact of loading the same endpoint more than one time in one page.


## `plone.restapi` GET endpoints

Environment and assignments:

-   `@actions`
j
    -   Anonymous
    -   rule `plone.content.dynamic` (might be influenced by other content)
    -   purge

-   `@addons`

    -   Authenticated
    -   no rule assignment

-   `@breadcrumbs`

    -   Anonymous
    -   rule `plone.content.dynamic` (parent may change)
    -   purge

-   `@comments`

    -   Anonymous
    -   rule `plone.content.itemView`
    -   purge

-   `/` (content)

    -   Anonymous
    -   expander!
    -   rule `plone.content.dynamic`

-   `@history`

    -   Authenticated
    -   no rule assignment

-   `@lock`

    -   Authenticated
    -   no rule assignment

-   `@translations`

    -   Anonymous
    -   with parameters
    -   rule `plone.content.dynamic`

-   `@translations-locator`

    -   Authenticated
    -   no rule assignment

-   `@navigation`

    -   Anonymous
    -   with parameters
    -   rule `plone.content.dynamic`

-   `@querysources`

    -   Authenticated
    -   with parameters
    -   can not be cached

-   `@querystring`

    -   Anonymous
    -   (values on `IPloneSiteRoot` from registry)
    -   rule `plone.content.dynamic`

-   `@querystring-search`

    -   is in `get.py` but configured as POST
    -   Anonymous
    -   with JSON body
    -   can not be cached

-   `@registry`

    -   Authenticated
    -   with subpath
    -   no rule assignment

-   `@roles`

    -   Authenticated
    -   no rule assignment

-   `@search`

    -   Anonymous
    -   with parameters
    -   rule `plone.content.dynamic`

-   `@sources`

    -   Authenticated
    -   no rule assignment

-   `@tiles`

    -   pre-deprecation
    -   Anonymous
    -   with subpath
    -   no rule assignment

-   `@types`

    -   Authenticated
    -   no rule assignment
