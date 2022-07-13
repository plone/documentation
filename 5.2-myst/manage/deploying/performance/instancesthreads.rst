============================================================
About Instances and Threads, Performance and RAM consumption
============================================================

.. admonition:: Description

    Understanding how instances per core, threads per instance and ZODB caches
    are influencing performance.

Introduction
------------

In a usual production Zope/Plone setup there are some tunings possible.
For a certain size of site, you need more than one Zope-instance and use `HAproxy`_ or `Pound`_ to load-balance between them.
Then you may ask yourself: How many instances do I need?
Next you see there is value "threads per instance" and wonder about the different
recommendations: Only one thread or two, or four? And how does it effect memory usage?

Rule of Thumb
-------------

A good **rule-of-thumb** for a common setup was (and still is) **two
instances per core, two threads per instance, and adjust the number of objects in
the ZODB cache to a number that your memory uses.**

This rule may not apply when any of the following scenarios exist:

* your setup gets more complex
* you have several logged in users
* you have only anonymous users
* you use official, fancy, specific or home-grown add-ons

In any of these scenarios, you will need to figure it out yourself. It's more important to understand the mechanism behind performance than following a set rule.

With recent, faster hardware and the (sometimes odd) behavior of virtual
machines (which can be very very different dependent on the kind of VM) this
needs slight or major adjustment.

Theory
------

Threads:
  A Zope instance runs a pool of threads. It queues an incoming
  request and dispatches it to a free thread. If no thread is free, the request
  remains in the queue and is dispatched when a thread is freed. If all threads
  are used by long-running request-to-response cycles, then this may block simple
  tasks such as publishing a tiny icon.

Database-Connection-Pool and its Cache:
  Once a thread runs, it requests a ZODB
  database connection from the connection pool. It locks the connection so no
  other thread can use it. The connection pool opens a new connection if all
  existing connections are already in use. If the request-to-response cycle is
  finished and the thread is freed, then the connection is released back to the pool.

Memory Cache:
  Each connection has its own memory cache. The file system cache is shared by
  all connections. Each cache can have the configured number of objects in
  memory. Having them in memory is important. Otherwise they are unpickled when
  loaded from the database, the process of which is expensive.

  An instance may never get enough load so that all available threads are used
  concurrently. In this case you may find in the Management Interface (Zope-root -> Control_Panel
  -> Database -> Main DB) that there are only 2 connections, but you have 4
  threads. That's because there are never 4 connections used in parallel.

Instances and memory:
  An instance creates only minimal memory usage overhead. If you have two
  instances, each with 2 threads, or one with 4 threads, and all threads are used
  in either case, it won't make much difference (~15-20MB overhead per instance
  at the time of writing).

  Now while Plone is running for some time, another significant (but low compared to
  ZODB cache) amount of RAM is consumed for RAM caching inside Zope
  (in other words, with ``plone.memoize``). RAM cache is shared by all threads, but not between
  instances. To optimize RAM caching in a multi-instance environment, "memcached"
  may be used to optimize memory cache and cache usage and reduce an instances
  memory footprint.

  In any case, most memory is used (in a common setup) to cache the ZODB.

Python GIL (global interpreter lock):
  Well, yes, the GIL is mentioned here. In a threaded environment such as Zope,
  it has an impact on performance. But it is low, and Python has been optimized
  over the years. Also Zope has a lot of I/O which reduces the GIL impact. A
  good and important optimization is to set the right check interval for your
  machine. `jarn.checkinterval`_ is a good tool to test for the right value.

Practice
--------

All theory is just theory, until it is put into practice. How does theory apply to your setup if the rule-of-thumb
above does not apply?

Get measurements! First of all, you need to check what happens on your
machine. Learn how to use `Munin`_ (with `munin.zope`_), HAproxy
(or Pound), or [tool of your choice here]. After that you'll get graphs of RAM,
CPU, and load, and some Zope related values. HAproxy or Pound may mark a node
as "down" because all threads were blocked by long running requests. To identify
these requests, `collective.stats`_ might help.

Do you have more instances or threads? This question is asked often, and cannot be
answered without knowing more about the Plone scenario. We can divide it roughly
into four kinds of scenarios:

- Only or almost all users are logged in
- Only or almost all visitors are anonymous
- Mixed, with many users and lots of hardware resources
- Mixed, with few users and constrained hardware resources

If you deal with logged in users, there is no easy way to cache HTML pages
(highly recommended anyway for all static items) in a reverse proxy cache (i.e.
`Varnish`_) in front of Plone. Zope does much more work rendering pages. To
render pages, objects need to be loaded form the database. Loading is expensive.
If an object is already in the database RAM cache, then it decreases the time to render a
page significantly. In a setup with lots of logged in users, we need to ensure that
almost all objects are loaded already. Each thread fetches a connection
from the pool, and each connection has its cache. If a user now requests a page, it
is first logged in, and Zope needs a bunch of objects for this from the ZODB. Also
other user specific information is loaded. Furthermore, the user may operate in an Intranet
within a specific area, so these objects also need to be loaded. For example,
if we now have 1 instance with 5 threads, then we have up to 5 pools (5 caches). All objects of
interest are loaded 5 times in the worst case. If there's 1 instance with 1 thread
(1 cache), data is loaded only once. But if there is only one instance with one
thread, then a browser shooting at the web server with lots of requests at one time
fills up the request queue of the instance and may time out soon. Also a second
user may want to access data at the same time, but the only thread is blocked,
and the CPU idles. So the best is to stick users in a load-balancer (bind it to
the ``__ac`` cookie) to 1 instance with 2 threads (also this can be adjusted
dependent on your setup by testing it yourself). Provide as many instances as you
can (memory consumption and CPU usage will stop you). In such a setup, usage of
`memcached`_ is highly encouraged.

If you have almost all anonymous users it is much easier. You can provide fewer
instances (here the rule-of-thumb of 2 instances per core applies in most cases) and increase
threads. Too many threads are not good, because of the GIL. You need to find the
number yourself, as it depends on hardware. Here without memcached configured,
good results can be expected, because memory cache is used efficiently. Increase
objects per connection cache until your memory consumption hits its hard limit, and
always look at your CPU usage.

In large mixed environments with enough budget for hardware, divide
your environment in two: one for logged in users, and one for anonymous users, such that the above
applies.

In smaller mixed environments with less hardware resources available, you need to find your
own balance. A good method is to configure your load balancer to direct logged-in
users to one or two distinct instances. If there are more users, this is
tricky and may take some time to figure out a good setup. As such, this is the
most difficult setup.

.. _HAproxy: http://www.haproxy.org/
.. _Pound: http://www.apsis.ch/pound
.. _jarn.checkinterval: https://pypi.python.org/pypi/jarn.checkinterval
.. _Munin: http://munin-monitoring.org/
.. _munin.zope: https://pypi.python.org/pypi/munin.zope
.. _Varnish: https://www.varnish-cache.org
.. _collective.stats: https://pypi.python.org/pypi/collective.stats
.. _memcached: https://www.memcached.org/
