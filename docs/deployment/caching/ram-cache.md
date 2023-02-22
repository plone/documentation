---
myst:
  html_meta:
    "description": "In-memory cache support in Plone"
    "property=og:description": "In-memory cache support in Plone"
    "property=og:title": "In-memory cache support in Plone"
    "keywords": "Plone, deployment, automation, caching, In-memory, RAM"
---

(caching-ram-cache-label)=

# RAM cache

In addition to caching content in users' browsers through setting appropriate response headers and a caching proxy, Plone can cache certain information in memory.
This is done in two main ways:

-   Developers may use the `plone.memoize` package's `ram` module to cache the results of certain functions in RAM.
    For example, some viewlets and portlets cache their rendered output in RAM for a time, alleviating the need to calculate them every time.
-   Some caching operations may cache an entire response in memory, so that they can later intercept the request to return a cached response.

Caching in RAM in Zope is not as efficient as caching in a proxy, for a number of reasons.

-   Zope still has to perform traversal, security, transaction management, and so on before serving a request with a RAM-cached response.
-   Zope's use of memory is not as efficient as that of a finely optimised caching proxy.
-   Storing lots of content in RAM may compete with the standard ZODB object cache and other memory pools used by Zope, thus slowing down Zope overall.
-   In multi-client ZEO setups, the RAM cache is (by default at least) not shared among instances, although it is shared among threads in that instance.
    Thus each Plone client process will maintain its own cache.

You can use the {guilabel}`RAM cache` tab in the Caching control panel to view statistics about the use of the RAM cache.
On the {guilabel}`Change settings` tab, you can also control the size of the cache, and the frequency with which it is purged of old items.


## Alternative RAM cache implementations

The RAM cache exposed through `plone.memoize.ram` is looked up via an `ICacheChoser` utility.
The default implementation looks up a `zope.ramcache.interfaces.ram.IRAMCache` utility.
Plone installs a local utility (to allow its settings to be persisted; the cache itself is not persistent), which is shared by all users of the cache.

You can provide your own `ICacheChooser` utility to change this policy, by installing this as a local utility or overriding it in `overrides.zcml`.
One reason to do this may be to back the cache with a [memcached](https://memcached.org/) server, which would allow a single cache to be shared among multiple Zope clients.

Below is a sketch of such a cache chooser, courtesy of Wojciech Lichota.

```python
from plone.memoize.interfaces import ICacheChooser
from plone.memoize.ram import MemcacheAdapter
from pylibmc import Client
from threading import local
from zope.interface import implementer

@implementer(ICacheChooser)
class MemcachedCacheChooser():
    _v_thread_local = local()

    def getClient(self):
        """
        Return thread local connection to memcached.
        """
        connection = getattr(self._v_thread_local, 'connection', None)
        if connection is None:
            connection = Client(['127.0.0.1:11211'])
            self._v_thread_local.connection = connection

        return connection

    def __call__(self, fun_name):
        """
        Create new adapter for plone.memoize.ram.
        """
        return MemcacheAdapter(client=self.getClient(), globalkey=fun_name)
```

You could install this with the following lines in an `overrides.zcml`.

```xml
<utility factory=".memcached.MemcachedCacheChooser" />
```
