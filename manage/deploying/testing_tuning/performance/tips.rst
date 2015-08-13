===============================
 Performance tips
===============================

.. contents :: :local:

.. admonition:: Description

    Tips for Plone performance tuning and making your add-on product and
    customizations faster.

Profiling Plone
===========================

* https://pypi.python.org/pypi/collective.profiler/

Optimizing ZEO and threads
===========================

For multicore systems, which basically all production systems nowadays are,
you might want to optimize Python threading vs. processes. You may also tune
how many Python interpreter instructions are run before doing green thread
switches in the interpreter.

* https://mail.zope.org/pipermail/zodb-dev/2010-December/013897.html

Debugging slow threads in production
====================================

* https://pypi.python.org/pypi/Products.LongRequestLogger

Memcached as session storage
============================

Storing sessions in ZEO/ZODB does not scale well, since they are very prone
to raise ``ConflictErrors`` if there is considerable load on the system.

Memcached provides a more scalable session backend.

For more information, see
`lovely.session add-on product <https://pypi.python.org/pypi/lovely.session/0.2.2>`_.

Input/output performance of the server
======================================

http://plope.com/Members/chrism/iostat_debugging

Summary::

    <mcdonc> well, the example has await at about 40X svctime.. that's pretty shitty
    <mcdonc> i mean that box was useless


Tuning complex configurations
=============================

http://www.lovelysystems.com/the-decathlon-of-computer-science/

Reducing memory usage
=======================

These tips are especially critical when running Plone on low-memory virtual
private server (VPS). But using the memory tips below, and some filesystem and operating system tweaks,
it is also perfectly possible to run Plone on an ARM-based Android stick, or a Raspberry Pi. See http://polyester.github.io/

Disable extra languages
-------------------------

Add ``PTS_LANGUAGES`` to ``buildout.cfg`` to declare which .po files are loaded on the start-up::

        [instance]
        ...
        environment-vars =
            PTS_LANGUAGES=en fi

Upgrade DateTime
----------------

DateTime 3.x and higher use significant less memory than older versions. Pinning it to 3.0.3 (4.x not tested yet) has no
known side effects on all Plone 4.1.x and 4.2.x sites, but can give up to a 20-25% reduction in memory use on lower-end hardware/virtualmachines.


Large files
============

How to offload blob processing from Zope:

* http://www.slideshare.net/Jazkarta/large-files-without-the-trials


Sessions and performance
========================

Write transactions much worse performance-wise than read transactions.

By default, every login is a write transaction. Also, Plone needs to update
the logged-in user's session timestamp once in a while to keep the session
active.

With a high amount of users, you may start seeing many ``ConflictErrors``
(read conflicts) with ZODB.

There are some tricks you can use here:

* http://plone.293351.n2.nabble.com/the-mysterious-case-of-the-zope-sessions-that-shouldn-t-tp5731395p5731395.html

* https://pypi.python.org/pypi/collective.beaker/

ZServer thread count
======================

This specifies how many requests one ZEO front-end client (ZServer) can
handle.

The default set by buildout default is 2.

Adjust it::

        [client1]
        recipe = plone.recipe.zope2instance
        ....
        zserver-threads = 5

Find good value by doing performance testing for your site.

.. note ::

    Increasing thread count is useful if your Plone site does
    server-to-server traffic and your Plone site needs to wait for the other
    end, thus blocking Zope threads.

More info:

* https://pypi.python.org/pypi/plone.recipe.zope2instance

XSendFile
============

XSendFile is an enhancement over HTTP front end proxy protocol which allows
offloading of file uploads and downloads to the front end web server.

More info for Plone support:

* https://github.com/collective/collective.xsendfile
