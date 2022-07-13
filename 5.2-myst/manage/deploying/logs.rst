Logs and log rotation
=====================

Plone and Zope maintain a variety of log files. As with all log files, you
need to rotate your logs or your server will die from lack of storage. Log
rotation is a process of maintaining a set of historical log files while
periodically starting the current log file anew.

Log types and locations
-----------------------

The buildout recipes that set up ZEO server and client components allow you
to set the names and location of your log files. We'll describe below the
common names and locations. If this doesn't match your situation, check your
buildout's zeoserver and zope2instance sections.

.. note::
    If Zope instance is started in the foreground mode logs will be printed in the console (stdout).

ZEO server log
~~~~~~~~~~~~~~

A ZEO server only maintains one log file, which records starts, stops and
client connections. Unless you are having difficulties with ZEO client
connections, this file is uninformative. It also typically grows very
slowly - so slowly that you may never need to rotate it.

The ZEO server log for a cluster will typically be found under your buildout
directory at var/zeoserver/zeoserver.log.

Client logs
~~~~~~~~~~~

Client logs are much more interesting and grow more rapidly. There are two
kinds of client logs, and each of your clients will maintain both:

Access logs

    A record of HTTP, WebDAV, and - if it's turned on - ftp accesses to the
    client. This resembles traditional web-server log files. Typical location
    of a client's access log is var/client#/Z2.log.

Event logs

    Startup, shutdown and error messages. Event logs need attention so that
    errors are quickly discovered. Typical location of a client's event log
    is var/client#/event.log.

Log levels
~~~~~~~~~~

You may set the verbosity level of access and event logs via the zope2instance
sections for your clients. In the context of deployments, it can be
very useful for change the loglevel for access logs. The default verbosity level for access
logs - WARN - creates an entry for every HTTP access. If you are recording
HTTP accesses via your proxy server, you may change the access logging level
to "ERROR" and dramatically slow the rate at which your access logs grow::

    [client1]
    recipe = plone.recipe.zope2instance
    ...
    z2-log-level = ERROR
    ...

Don't turn down the access log level until you've had a chance to tune up
your proxy cache. Seeing which requests make it through to the ZEO client
is very useful information when checking caching and load balancing.

Client log rotation
-------------------

The basic option here is between using the ZEO client log rotation mechanisms
built into Zope and using external mechanisms - such as the log-rotation
facilities available on your server.

Plone 4.2.2+
~~~~~~~~~~~~

Plone 4.2.2+ allows you to set a simple size-based mechanism for client log
rotation.

The mechanism actually is built into Zope 2.12+ (used in Plone 4.0+), but
there was no easy way to use it in a buildout until release 4.2.5 of
plone.recipe.zope2instance. That recipe version ships with Plone 4.2.2+.
We'll describe later a not-as easy mechanism for earlier 4.x series releases
of Plone.

For Plone 4.2.2+, just add configuration settings like these to your
buildout's zope2instance sections::

    [client1]
    recipe = plone.recipe.zope2instance
    ...
    event-log-max-size = 5 MB
    event-log-old-files = 5
    access-log-max-size = 20 MB
    access-log-old-files = 10

This will maintain five generations of event logs of maximum five megabytes
in size and 10 generations of 20 megabyte access logs.

For earlier versions of Plone in the 4.x series, you may use a custom log
setup command to pass parameters to Zope::

    [client1]
    recipe = plone.recipe.zope2instance
    ...
    event-log-custom =
        <logfile>
            max-size = 5mb
            old-files 5
        </logfile>
    access-log-custom =
        <logfile>
            max-size = 20mb
            old-files 10
        </logfile>

Other log rotation mechanisms
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Unix-ish systems have several log rotation mechanisms available. Two common
ones are ``newsyslog`` and ``logrotate``. Both are well-documented. The
critical thing you need to know for each is how to signal Zope that a log
rotation has occurred, forcing it to reopen the log file. Zope will do this
if you send the client process a USR2 signal.

For example, with logrotate, you can rotate a client's logs with a
configuration like::

    # rotate logs for client #2
    /var/db/plone4/zeocluster/var/client2/Z2.log
    /var/db/plone4/zeocluster/var/client2/event.log {
        rotate 5
        weekly
        sharedscripts
        postrotate
           kill -USR2 `cat /var/db/plone4/zeocluster/var/client2/client2.pid`
        endscript
    }

Error alerts
------------

Zope can email access log error messages. As with other logging instructions,
this is done with an addition to client zope2instance sections of your
buildout::

    [client1]
    recipe = plone.recipe.zope2instance
    ...
    mailinglogger =
        <mailing-logger>
          flood-level 10
          level error
          smtp-server localhost
          from errors@yourdomain.com
          to errors@yourdomain.com
          subject [My domain error] [%(hostname)s] %(line)s
        </mailing-logger>

For complete detail on configuration, see the
`mailinglogger documentation <http://mailinglogger.readthedocs.io/en/latest/>`_.
