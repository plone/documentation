============================================================
About Instances and Threads, Performance and RAM consumption
============================================================

.. admonition:: Description

    Understanding how instances-per-core, threads-per-instance and ZODB-caches
    are influencing performance.

Introduction
------------

In a usual production Zope/Plone setup there are some tunings possible.
For a certain size of site, you need more than one Zope-instance and use `HAproxy`_ or `Pound`_ to load-balance between them.
Then you may ask yourself: How many instances do I need?
Next you see there is value "threads per instance" and wonder about the different
recommendations: Only one thread or two, or four? And how does it effect memory usage?

Rule Of The Thumb
-----------------

A good **rule-of-the-thumb** for a common setup was and still is: **two
instances per core, two threads per instance, adjust the number of objects in
the ZODB cache to a number that your memory is used.**

**But attention!** If your setup gets more complex, if you have several logged
in users or only anonymous users, if you use official, fancy, specific or
home-grown add-ons: This rule may not apply.

In this case you need to figure out yourself. It's more important to understand
the mechanism behind than sticking to a rule.

With recent, faster hardware and the (sometimes odd) behavior of virtual
machines (which can be very very different dependent on the kind of VM) this
needs slight or major adjustment.

Theory
------

Threads:
  A Zope instance is running a pool of threads. It queues an incoming
  request and dispatches it to a free thread. If no thread is free the request
  remains in the queue and is dispatched when a thread was freed. If all threads
  are used by long-running request-to-response cycles this may block such simple
  tasks as publishing a tiny icon.

Database-Connection-Pool and its Cache:
  Once a thread runs, it requests a ZODB
  database connection from the connection pool. It locks the connection so no
  other thread can use it. The connection pool opens a new connection if all
  existing connections are already in use. If the request-to-response cycle is
  finished and the thread is freed the connection is released back to the pool.

Memory Cache:
  Each connection has its own memory cache. The file-system cache is shared by
  all connections. Each cache can have the configured number of objects in
  memory. Having them in memory is important, because they are unpickled if
  loaded from the DB - and the process of unpickling is still expensive.

  An instance may never get enough load so that all available threads are used
  concurrently. In this case you may find in the Management Interface (Zope-root -> Control_Panel
  -> Database -> Main DB) that there are only 2 connections, but you have 4
  threads. That's because there were never 4 connections used in parallel.

Instances and memory:
  An instance creates only a minimal memory usage overhead. If you have two
  instances with each 2 threads or one with 4 threads and all threads are used
  in both cases it wont make much a difference (~15-20MB overhead per instance
  at time of writing).

  Now while Plone is running for some time another significant (but compared to
  ZODB cache low) amount of consumed RAM is used for RAM-caching inside Zope
  (i.e. with plone.memoize). RAM-cache is shared by all threads but not between
  instances. To optimize ram-caching in a multi-instance environment "memcached"
  may be used to optimize memory cache and cache-usage and reduce an instances
  memory footprint.

  But anyway, most memory is used (in a common setup) to cache the ZODB.

Python GIL - global interpreter lock:
  Well yes, the GIL is mentioned here. In a threaded environment such as Zope
  is it has an impact on performance. But it is low and python was optimized
  over the years, also Zope has a lot of I/O which reduces the GIL impact. A
  good and important optimization is to set the right check interval for your
  machine. With `jarn.checkinterval`_ there's a good and simple to use tool to
  test for the right value.

Practice
--------

All theory is gray. But what does this mean for your setup if the rule-of-thumb
above does not apply?

Get measurements! First of all you need to check yourself what happens on your
machine(s), go and learn how to use `Munin`_ (with `munin.zope`_), HAproxy
(or Pound), [tool of your choice here]. After that you'll get graphs of RAM,
CPU, and load and some zope related values. HAproxy or Pound may mark a node
as down because all threads were blocked by long running requests, identify
these requests, `collective.stats`_ helps here.

More instances or more threads? This question is asked often. And can not be
answered without knowing more about the Plone system. We can divide it roughly
into four kinds of systems:

- Only or almost logged in users,
- Only or almost only anonymous visitors,
- Mixed with many users and lots of hardware behind,
- Mixed with few users and low-budget hardware.

If you deal with logged in users there is no easy way to cache html-pages
(highly recommended anyway for all static items) in a reverse proxy cache (i.e.
`Varnish`_) in front of Plone. Zope has much more work rendering pages. To
render pages, objects need to be loaded form the database. Loading is expensive.
If an object is already in the DB RAM cache it decreases the time to render a
page significantly. So in a setup with lots of logged in users we need to take
care almost all objects are loaded already. Each thread fetches a connection
from the pool, each connection has its cache. If a user now requests a page it
is first logged in and zope need a bunch of objects for this from the ZODB. Also
other user specific information is loaded. Then user may operate in an intranet
within a specific area, so these objects also need to be loaded. If we now have
i.e 1 instance with 5 threads we have up to 5 pools (5 caches). All objects of
interest are loaded in worst case 5 times. If there's 1 instance with 1 thread
(1 cache) data is loaded only once. But if there is only one instance with one
thread a browser shooting at the web-server with lots of requests at one time
fills up the request queue of the instance and may time out soon. Also a second
user may want to access data at the same time, but the only thread is blocked
and the CPU idles. So the best is to stick users in a load-balancer (bind it to
the __ac cookie) to 1 instance with 2 threads (also this can be adjusted
dependent on your setup, test it yourself). Provide as much instances as you
can (memory-consumption and cpu-usage will stop you). In such a setup usage of
`memcached`_ is highly encouraged.

If you have almost all anonymous users it is much easier. You can provide less
instances (here rule-of-thumb 2 per core applies in most cases) and increase
threads. Too many threads are not good, because of the GIL. You need to find the
number yourself, it depends much on hardware. Here - w/o memcached configured -
good results can be expected, because memory cache is used efficient. Increase
objects per connection cache until your memory-consumption stops you and look
always at your CPU usage.

In large mixed environments with enough budget for hardware it is easy: Divide
your environment in two, one for logged in users, one for anonymous - so above
applies.

In smaller mixed environments with less hardware behind you need to find your
own balance. A good way is configuring your load balancer to stick logged-in
users to one or two distinct instances. If there are more users this is kind
of tricky and may take some time to figure out a good setup. So this is the
most difficult setup.

.. _HAproxy: http://haproxy.1wt.eu
.. _Pound: http://www.apsis.ch/pound
.. _jarn.checkinterval: https://pypi.python.org/pypi/jarn.checkinterval
.. _Munin: http://munin-monitoring.org
.. _munin.zope: https://pypi.python.org/pypi/munin.zope
.. _Varnish: https://www.varnish-cache.org
.. _collective.stats: https://pypi.python.org/pypi/collective.stats
.. _memcached: https://en.wikipedia.org/wiki/Memcached
