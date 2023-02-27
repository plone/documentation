---
myst:
  html_meta:
    "description": "Rulesets and caching operations"
    "property=og:description": "Rulesets and caching operations"
    "property=og:title": "Rulesets and caching operations"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-rulesets-label)=

# Rulesets and caching operations

This chapter requires that you first {ref}`import-a-caching-profile-label` and {ref}`enable-caching-label`.

The caching infrastructure works on the principle of *rulesets* mapped to *caching operations*.

A ruleset is basically just a name, and is normally applied in {term}`ZCML` by the author of a particular view.

There are also some default rulesets applied to general resources.

Please note that `plone.app.caching` places the caching ruleset registry into "explicit" mode.
This means that you *must* declare a caching ruleset with the `<cache:rulesetType />` directive before you can use it.

Caching operations are components written in Python which either interrupt rendering to provide a cached response (such as a `304 NOT MODIFIED` response), or add caching information to a response (such as setting the `Cache-Control` HTTP response header).

For more details on how to use these components, see the documentation for [`plone.caching`](https://pypi.org/project/plone.caching).

Once rulesets and caching operations have been registered, they will appear in the Caching control panel under {guilabel}`Caching operation`.


## Default rulesets

`plone.app.caching` declares a few default rulesets.
They are listed with descriptions in the control panel.

### Content feed (`plone.content.feed`)

A dynamic feed, such as RSS or ATOM.

### Content files and images (`plone.content.file`)

Includes files and images in content space, usually either downloaded or included as an inline element in one of the other public-facing views.

### Content folder view (`plone.content.folderView`)

A public-facing view for a content item that is a folder or container for other items.

### Content item view (`plone.content.itemView`)

A public-facing view for a content item that is not a folder or container for other items.

### File and image resources (`plone.resource`)

Includes images and files created or customised through the ZMI, those exposed in the `portal_skins` tool, and images registered in resource directories on the file system.

### Stable file and image resources (`plone.stableResource`)

Stable resources such as the CSS, and JavaScript files registered with the Resource Registries.
These are resources which can be cached "forever".
Normally this means that if the object does change, its URL changes, too.

## Default cache operations

`plone.app.caching` also declares a number of default operation types.

These are listed in the control panel as available operations for the various rulesets.
Hover your mouse over an operation in the select list to view its description.

### Strong caching (`plone.app.caching.strongCaching`)

Cache in browser and proxy (default: 24 hours).

```{caution}
Only use this operation for stable resources that never change without changing their URL, or resources for which temporary staleness is not critical.
```

In the caching profiles `without-caching-proxy` and `with-caching-proxy`, this operation is mapped to the rulesets `plone.resource` and `plone.stableResource`, which causes the following headers to be added to the response:

```text
Last-Modified: <last-modified-date>
Cache-Control: max-age=<seconds>, proxy-revalidate, public
```


### Moderate caching (`plone.app.caching.moderateCaching`)

Cache in browser but expire immediately (same as `weak caching`), and cache in proxy (default: 24 hours).
Use a purgable caching reverse proxy for best results.

```{caution}
If the proxy cannot be purged reliably—for example, in the case of composite pages where it may be difficult to track when a dependency has changed—then stale responses might be seen until the cached entry expires.
```

A similar caution applies even if in the purgeable case, if the proxy cannot be configured to disallow caching in other intermediate proxies that may exist between the local proxies and the browser.
See the example proxy configs included with this package for some solutions to this problem.

In the caching profile `with-caching-proxy`, this operation is mapped to the rulesets `plone.content.feed` and `plone.content.file`, which causes the following headers to be added to the response.

#### `plone.content.feed`

```text
ETag: <etag-value>
Cache-Control: max-age=0, s-maxage=<seconds>, must-revalidate
```

#### `plone.content.file`

```text
Last-Modified: <last-modified-date>
Cache-Control: max-age=0, s-maxage=<seconds>, must-revalidate
```

### Weak caching (`plone.app.caching.weakCaching`)

Cache in browser but expire immediately and enable 304 responses on subsequent requests.
304s require configuration of the `Last-Modified` and/or `ETags` settings.
If the `Last-Modified` header is insufficient to ensure freshness, turn on ETag checking by listing each ETag component that should be used to to construct the ETag header.
To also cache public responses in Zope memory, set the `RAM cache` parameter to `True`.

In the caching profile `without-caching-proxy`, this operation is mapped to the rulesets `plone.content.itemView`, `plone.content.folderView`, `plone.content.feed`, and `plone.content.file`, which causes the following headers to be added to the response.

#### `plone.content.itemView`, `plone.content.folderView`, `plone.content.feed`

```text
ETag: <etag-value>
Cache-Control: max-age=0, must-revalidate, private
```

### plone.content.file

```text
Last-Modified: <last-modified-date>
Cache-Control: max-age=0, must-revalidate, private
```

In the caching profile `with-caching-proxy`, this operation is mapped only to the rulesets `plone.content.itemView` and `plone.content.folderView`.

### No caching (`plone.app.caching.noCaching`)

Use this operation to keep the response out of all caches.
The default settings generate an Internet Explorer-safe no-cache operation.
Under certain conditions, Internet Explorer chokes on `no-cache` and `no-store` `Cache-Control` tokens.
Instead we exclude caching in shared caching proxies with the `private` token, expire immediately in the browser, and disable validation.
This emulates the usual behavior expected from the `no-cache` token.

If the nominally more secure, but occasionally troublesome, `no-store` token is also desired, set the `No store` parameter to `True`.

```{todo}
'no store' option not done yet
```

### Chain (`plone.caching.operations.chain`)

Allows multiple operations to be chained together.
When intercepting the response, the first chained operation to return a value will be used.
Subsequent operations are ignored.
When modifying the response, all operations will be called in order.

These operation descriptions are a bit simplified.
Several of these operations also include tests to downgrade caching depending on various parameter settings, workflow state, and access privileges.
For more detail, it's best to review the operation code itself.


## Default ruleset operation mappings

To recap, `plone.app.caching` defines three default cache policies containing the cache operation mappings for each of the six rulesets.
The default mappings are as follows.

| ..  | without-caching-proxy  | with-caching-proxy  | with-caching-proxy-splitviews |
| --- | ---  | --- | --- |
| itemView | weakCaching | weakCaching | moderateCaching |
| folderView | weakCaching | weakCaching | moderateCaching |
| feed | weakCaching | moderateCaching | moderateCaching |
| file | weakCaching | moderateCaching | moderateCaching |
| resource | strongCaching | strongCaching | strongCaching |
| stableResource | strongCaching | strongCaching | strongCaching |


## Cache operation parameters

Much of the cache operation behavior is controlled via user-adjustable parameters.
In fact, three of the default caching operations—strong caching, moderate caching, and weak caching—are essentially all the same operation but with different default parameter settings and with some parameters hidden from the user interface.

### Maximum age (`maxage`)

Time in seconds to cache the response in the browser or caching proxy.

Adds a `Cache-Control: max-age=<value>` header and a matching `Expires` header to the response.

### Shared maximum age (`smaxage`)

Time in seconds to cache the response in the caching proxy.

Adds a `Cache-Control: s-maxage=<value>` header to the response.

### ETags (`etags`)

A list of the names of the ETag components to include in the `ETag` header.
Also turns on `304 Not Modified` responses for `If-None-Match` conditional requests.

### Last-modified validation (`lastModified`)

Adds a `Last-Modified` header to the response and turns on `304 Not Modified` responses for `If-Modified-Since` conditional requests.

### RAM cache (`ramCache`)

Turn on caching in Zope memory.

If the URL is not specific enough to ensure uniqueness, then either `ETags` or `Last-Modified` should also be added to the list of parameters to generate a unique cache key.

### Vary (`vary`)

Name(s) of HTTP headers in the request that must match (in addition to the URL) for a caching proxy to return a cached response.

### Anonymous only (`anonOnly`)

Set this to `True` if you want to force logged-in users to always get a fresh copy.

This works best with the "moderate caching" operation, and will not work well with a `Max age` (to cache content in the browser) greater than zero.

By setting this option, you can focus the other cache settings on the anonymous use case.

Note that if you are using a caching proxy, you will need to set a `Vary` header of `X-Anonymous` or similar, and ensure that such a header is set in the proxy for logged in users.
A blunter alternative is to use `Cookie` as the header, although this can have false positives).
See the example Varnish configuration that comes with this package for more details.

### Request variables that prevent caching (`cacheStopRequestVariables`)

A list of variables in the request (including `Cookies`) that prevent caching if present.

Note, unlike the other parameters above, this global parameter is not directly visible in the {guilabel}`plone.app.caching` user interface.

It is unlikely to need to change this list but, if needed, it can be edited via the {guilabel}`Configuration Registry` control panel.


## Caching operation helper functions

If you will find the implementations of the default caching operations in the package `plone.app.caching.operations`.

If you are writing a custom caching operation, the `utils` module contains helper functions which you may find useful.


### Debug headers and logging

It can sometimes be useful to see which rulesets and operations (if any) are being applied to published resources.
There are two ways to see this: via debug response headers, and via debug logging.

Several debug response headers are added automatically by `plone.app.caching` and `plone.caching`.

These headers include:

-   `X-Cache-Rule: <matching rule id>`
-   `X-Cache-Operation: <matching operation id>`
-   `X-Cache-Chain-Operations: <list of chain operation ids>`
-   `X-RAMCache: <ram cache id>`

Viewing these headers is relatively easy with Web Developer Tools in Firefox or Developer Tools in Chrome.

If you enable the `DEBUG` logging level for the `plone.caching` logger, you will get additional debug output in your event log.
One way to do that is to set the global Zope logging level to `DEBUG` in `zope.conf`:

```xml
<eventlog>
      level DEBUG
      <logfile>
      path <file_path_here/>
      level DEBUG
      </logfile>
</eventlog>
```

You should see output in the log like:

```console
2010-01-11 16:44:10 DEBUG plone.caching Published: <Image at /test/i> Ruleset: plone.download Operation: None
2010-01-11 16:44:10 DEBUG plone.caching Published: <Image at /test/i> Ruleset: plone.download Operation: plone.caching.operations.chain
```

The `None` indicates that no ruleset or operation was mapped.

It is probably not a good idea to leave debug logging on for production use, as it can produce a lot of output, fill up log files, and add unnecessary load to your disks.

## `Content-type` based rulesets

Normally you declare caching rulesets for a view as shown below.

```xml
<cache:ruleset
      ruleset="plone.content.itemView"
      for=".browser.MyItemView"
      />
```

See [`plone.caching`](https://pypi.org/project/plone.caching) for details.

`plone.app.caching` installs a special ruleset lookup adapter that is invoked for skin layer page templates and browser views not assigned a more specific rule set.
This adapter allows you to declare a ruleset for the *default view* of a given content type by supplying a content type class or interface to the `<cache:ruleset />` directive.

```xml
<cache:ruleset
      ruleset="plone.content.itemView"
      for=".interfaces.IMyContentType"
      />
```
Or for a class.

```xml
<cache:ruleset
    ruleset="plone.content.itemView"
    for=".content.MyContentType"
    />
```

There are two reasons to do this.

-   Your type uses a skin layer page template for its default view, instead of a browser view.
    In this case, you can either declare the ruleset on the type as shown above (in ZCML), or map the type name in the registry, using the GUI or GenericSetup.
    The former is more robust and certainly more natural if you are declaring other, more conventional rulesets in {term}`ZCML` already.
-   You want to set the ruleset for a number of content types.
    In fact, `plone.app.caching` already does this for you.
    Dexterity `IDexterityItem` and `IDexterityContainer` interfaces are assigned the rulesets `plone.content.itemView` and `plone.content.folderview`, respectively.
