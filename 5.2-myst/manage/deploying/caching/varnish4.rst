===========
Varnish 4.x
===========

.. admonition:: Description

    Varnish is a caching front-end server.
    This document has notes on how to use Varnish with Plone.

Introduction
============

This chapter contains information about using the Varnish caching proxy with
Plone.

* http://varnish-cache.org/

To use Varnish with Plone

* Learn how to install and configure Varnish

* Add Plone virtual hosting rule to the default varnish configuration

Installation
============

The recommended method to install Varnish is by using your OS package manager.

Varnish is distributed in the Debian and Ubuntu package repositories.

.. code-block:: console

    $ sudo apt-get update
    $ sudo apt-get install varnish

For installation instructions on other operating systems check: https://www.varnish-cache.org/releases/index.html

You can also install Varnish using Buildout.
For examples check: https://pypi.python.org/pypi/plone.recipe.varnish

Management console
==================

``varnishadm``
--------------

You can access Varnish admin console on your server by::

    # Your system uses a secret handshake file
    varnishadm -T localhost:6082 -S /etc/varnish/secret

(Ubuntu/Debian installation)

Telnet console
--------------

The telnet management console is available on some configurations where ``varnishadm`` cannot be used.
The functionality is the same.

Example::

    ssh yourhost
    # Your system does not have a secret handshake file
    telnet localhost 6082

.. note::

    Port number depends on your Varnish settings.

More info
---------

* http://opensourcehacker.com/2013/02/07/varnish-shell-singleliners-reload-config-purge-cache-and-test-hits/

Quit console
------------

Quit command::

   quit

Purging the cache
-----------------

This will remove all entries from the Varnish cache::

   varnishadm "ban req.url ~ ."

Or remove all entries of JPG from the Varnish cache::

   varnishadm "ban req.url ~ .jpg"

Loading new VCL to live Varnish
===============================

More often than not, it is beneficial to load a new configuration without bringing the cache down for maintenance.
Using this method also checks the new Varnish Configuration Language (VCL) for syntax errors before activating it.
Logging in to Varnish CLI requires the ``varnishadm`` tool, the address of the management interface, and the secret file for authentication.

See the ``varnishadm`` man-page for details.

Opening a new CLI connection to the Varnish console, in a buildout-based Varnish installation::

    parts/varnish-build/bin/varnishadm -T localhost:8088

Port 8088 is defined in ``buildout.cfg``::

    [varnish-instance]
    telnet = localhost:8088

Opening a new CLI connection to the Varnish console, in a system-wide Varnish installation on Ubuntu/Debian::

    varnishadm -T localhost:6082 -S /etc/varnish/secret

You can dynamically load and parse a new VCL file to memory::

    vcl.load <name> <file>

For example::

    vcl.load newconf_1 /etc/varnish/newconf.vcl

... or ... ::

    # Ubuntu / Debian default config
    vcl.load defconf1 /etc/varnish/default.vcl

``vcl.load`` will load and compile the new configuration.
Compilation will fail and report on syntax errors, if any exist.
Now that the new configuration has been loaded, it can be activated with::

    vcl.use newconf_1

.. note::

    Varnish remembers ``<name>`` in ``vcl.load``, so every time you need to reload your config you need to invent a new name for vcl.load / vcl.use command pair.

See

* http://opensourcehacker.com/2013/02/07/varnish-shell-singleliners-reload-config-purge-cache-and-test-hits/

Logs
====

To see a real-time log dump (in a system-wide Varnish configuration)::

    varnishlog

By default, Varnish does not log to any file and keeps the log only in memory.
If you want to extract Apache-like logs from varnish, you need to use the ``varnishncsa`` utility.

Stats
=====

Check live "top-like" Varnish statistics::

    parts/varnish-build/bin/varnishstat

Use the admin console to print stats for you::

          Uptime mgt:   8+00:21:20
          Uptime child: 5+17:29:28

            NAME                                                                CURRENT       CHANGE      AVERAGE       AVG_10      AVG_100     AVG_1000
          MAIN.uptime                                                            494968         1.00         1.00         1.00         1.00         1.00
          MAIN.sess_conn                                                           1545         0.00          .           0.00         0.00         0.00
          MAIN.client_req                                                          1569         0.00          .           0.00         0.00         0.00
          MAIN.cache_hit                                                            461         0.00          .           0.00         0.00         0.00
          MAIN.cache_hitpass                                                         16         0.00          .           0.00         0.00         0.00
          MAIN.cache_miss                                                           477         0.00          .           0.00         0.00         0.00
          MAIN.backend_conn                                                        1060         0.00          .           0.00         0.00         0.00
          MAIN.fetch_head                                                            18         0.00          .           0.00         0.00         0.00
          MAIN.fetch_length                                                         996         0.00          .           0.00         0.00         0.00
          MAIN.fetch_204                                                              1         0.00          .           0.00         0.00         0.00
          MAIN.fetch_304                                                             46         0.00          .           0.00         0.00         0.00
          MAIN.pools                                                                  9         0.00          .           9.00         9.00         9.00
          MAIN.threads                                                              900         0.00          .         900.00       900.00       900.00
          MAIN.threads_created                                                      900         0.00          .           0.00         0.00         0.00
          ...

Virtual hosting proxy rule
==========================

Varnish 4.x example
-------------------

Varnish 4.x has been released, almost three years after the release of Varnish 3.0 in June 2011.
The backend fetching parts of VCL again have changed in Varnish 4.

An example with two separate Plone installations (Zope standalone mode) behind Varnish 4.x HTTP 80 port.

Example::

    # To make sure that people have upgraded their VCL to the current version,
    # Varnish now requires the first line of VCL to indicate the VCL version number.
    # VCL 4.1 does not compatible with Varnish < 6
    vcl 4.0;

    #
    # This backend never responds... we get hit in the case of bad virtualhost name
    #
    backend default {
        .host = "127.0.0.1";
        .port = "55555";
    }

    #
    # Plone Zope clients
    #
    backend site1 {
        .host = "127.0.0.1";
        .port = "9944";
    }

    backend site2 {
        .host = "127.0.0.1";
        .port = "9966";
    }

    #
    # Guess which site / virtualhost we are diving into.
    # Apache, Nginx or Plone directly
    #
    sub choose_backend {

        if (req.http.host ~ "^(.*\.)?site2\.fi(:[0-9]+)?$") {
            set req.backend_hint = site2;

            # Zope VirtualHostMonster
            set req.url = "/VirtualHostBase/http/" + req.http.host + ":80/Plone/VirtualHostRoot" + req.url;

        }

        if (req.http.host ~ "^(.*\.)?site1\.fi(:[0-9]+)?$") {
            set req.backend_hint = site1;

            # Zope VirtualHostMonster
            set req.url = "/VirtualHostBase/http/" + req.http.host + ":80/Plone/VirtualHostRoot" + req.url;
        }

    }

    # For now, we'll only allow purges coming from localhost
    acl purge {
        "127.0.0.1";
        "localhost";
    }

    sub vcl_recv {

        #
        # Do Plone cookie sanitization, so cookies do not destroy cacheable anonymous pages
        #
        if (req.http.Cookie) {
            set req.http.Cookie = ";" + req.http.Cookie;
            set req.http.Cookie = regsuball(req.http.Cookie, "; +", ";");
            set req.http.Cookie = regsuball(req.http.Cookie, ";(statusmessages|__ac|_ZopeId|__cp)=", "; \1=");
            set req.http.Cookie = regsuball(req.http.Cookie, ";[^ ][^;]*", "");
            set req.http.Cookie = regsuball(req.http.Cookie, "^[; ]+|[; ]+$", "");

            if (req.http.Cookie == "") {
                unset req.http.Cookie;
            }
        }

        call choose_backend;

        if (req.method != "GET" &&
          req.method != "HEAD" &&
          req.method != "PUT" &&
          req.method != "POST" &&
          req.method != "TRACE" &&
          req.method != "OPTIONS" &&
          req.method != "DELETE") {
            /* Non-RFC2616 or CONNECT which is weird. */
            return (pipe);
        }
        if (req.method != "GET" && req.method != "HEAD") {
            /* We only deal with GET and HEAD by default */
            return (pass);
        }
        if (req.http.Authorization || req.http.Cookie) {
            /* Not cacheable by default */
            return (pass);
        }
        return (hash);
    }

    sub vcl_hash {
        hash_data(req.url);
        if (req.http.host) {
            hash_data(req.http.host);
        } else {
            hash_data(server.ip);
        }
        return (lookup);
    }

    # error() is now synth()
    sub vcl_synth {
        if (resp.status == 720) {
            # We use this special error status 720 to force redirects with 301 (permanent) redirects
            # To use this, call the following from anywhere in vcl_recv: error 720 "http://host/new.html"
            set resp.status = 301;
            set resp.http.Location = resp.reason;
            return (deliver);
        } elseif (resp.status == 721) {
            # And we use error status 721 to force redirects with a 302 (temporary) redirect
            # To use this, call the following from anywhere in vcl_recv: error 720 "http://host/new.html"
            set resp.status = 302;
            set resp.http.Location = resp.reason;
            return (deliver);
        }

        return (deliver);
    }

    sub vcl_synth {
        set resp.http.Content-Type = "text/html; charset=utf-8";
        set resp.http.Retry-After = "5";

        synthetic( {"
                <?xml version="1.0" encoding="utf-8"?>
                <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
                <html>
                  <head>
                    <title>"} + resp.status + " " + resp.reason + {"</title>
                  </head>
                  <body>
                    <h1>Error "} + resp.status + " " + resp.reason + {"</h1>
                    <p>"} + resp.reason + {"</p>
                    <h3>Guru Meditation:</h3>
                    <p>XID: "} + req.xid + {"</p>
                    <hr>
                    <p>Varnish cache server</p>
                  </body>
                </html>
        "} );

        return (deliver);
    }


Load balancing
==============

Load balancing increases performance and resilience.
The Varnish ``vmod_directors`` module enables load balancing using a concept called "directors".

A director is a group of several backend servers.
A backend server is a server providing the content Varnish will accelerate.

Varnish supports the following directors:

round-robin
    Picks backends in a round-robin fashion.
fallback
    Try each of the added backends in turn, and return the first one that is healthy.
hash
    Chooses the backend server by computing the hash of a string.
random
    Distributes load over the backends using a weighted random probability distribution.

The following example shows how to configure round-robin load balancing of 2 Plone instances.

.. code-block:: text

    import directors;

    backend instance1 {
        .host = "localhost";
        .port = "8081";
    }

    backend instance2 {
        .host = "localhost";
        .port = "8082";
    }

    sub vcl_init {
        new plone = directors.round_robin();
        plone.add_backend(instance1);
        plone.add_backend(instance2);
    }

    sub vcl_recv {
        set req.backend_hint = plone.backend();
    }

For more information, see:

* https://www.varnish-cache.org/docs/trunk/users-guide/vcl-backends.html
* https://www.varnish-cache.org/docs/trunk/reference/vmod_directors.generated.html

Varnishd port and IP address to listen
======================================

You give IP addresses and ports for Varnish to listen to on the ``varnishd`` command line using the ``-a`` switch.
Edit ``/etc/default/varnish``::

    DAEMON_OPTS="-a 192.168.1.1:80 \
                 -T localhost:6082 \
                 -f /etc/varnish/default.vcl \
                 -s file,/var/lib/varnish/$INSTANCE/varnish_storage.bin,1G"


Cached and editor sub domains
=============================

You can provide an uncached version of the site for editors:

* http://serverfault.com/questions/297541/varnish-cached-and-non-cached-subdomains/297547#297547


Sanitizing cookies
==================

Any cookie set on the server side (session cookie) or on the client-side (e.g. Google Analytics JavaScript cookies) is poison for caching the anonymous visitor content.

HTTP caching needs to deal with both HTTP request and response cookie handling.

* HTTP request *Cookie* header. A browser sending an HTTP request
  with a ``Cookie`` header confuses Varnish cache look-up. This header can be
  set by JavaScript also, not just by the server.
  ``Cookie`` can be preprocessed in Varnish's ``vcl_recv`` step.

* HTTP response ``Set-Cookie`` header.
  This sets a server-side cookie. If your server is setting
  cookies, Varnish does not cache these responses by default.
  However, this might be desirable
  behavior if, for example, multi-lingual content is served from one URL with
  language cookies.
  ``Set-Cookie`` can be post-processed in Varnish's ``vcl_fetch`` step.

Example of removing all Plone-related cookies, besides ones dealing with the logged in users (content authors)::

    sub vcl_recv {

      if (req.http.Cookie) {
          # (logged in user, status message - NO session storage or language cookie)
          set req.http.Cookie = ";" + req.http.Cookie;
          set req.http.Cookie = regsuball(req.http.Cookie, "; +", ";");
          set req.http.Cookie = regsuball(req.http.Cookie, ";(statusmessages|__ac|_ZopeId|__cp)=", "; \1=");
          set req.http.Cookie = regsuball(req.http.Cookie, ";[^ ][^;]*", "");
          set req.http.Cookie = regsuball(req.http.Cookie, "^[; ]+|[; ]+$", "");

          if (req.http.Cookie == "") {
              unset req.http.Cookie;
          }
      }
      ...

    sub vcl_backend_response {

        # Here we could unset cookies explicitly,
        # but we assume plone.app.caching extension does it jobs
        # and no extra cookies fall through for HTTP responses we'd like to cache
        # (like images)

        if (beresp.ttl <= 0s
            || beresp.http.Set-Cookie
            || beresp.http.Surrogate-control ~ "no-store"
            || (!beresp.http.Surrogate-Control && beresp.http.Cache-Control ~ "no-cache|no-store|private")
            || beresp.http.Vary == "*") {

            /* * Mark as "Hit-For-Pass" for the next 2 minutes */
            set beresp.grace = 120s;
            set beresp.uncacheable = true;

            return (deliver);
        }

    }


An example of how to purge Google cookies only and allow other cookies by default::

    sub vcl_recv {
        # Remove Google Analytics cookies - will prevent caching of anon content
        # when using GA JavaScript. Also you will lose the information of
        # time spend on the site etc..
        if (req.http.cookie) {
           set req.http.Cookie = regsuball(req.http.Cookie, "__utm.=[^;]+(; )?", "");
           if (req.http.cookie ~ "^ *$") {
               unset req.http.cookie;
           }
         }
         ....

Debugging cookie issues
-----------------------

Use the following snippet to set a HTTP response debug header to see what the backend server sees as the cookie after ``vcl_recv`` clean-up regexes::

    sub vcl_backend_response {

        /* Use to see what cookies go through our filtering code to the server */
        set beresp.http.X-Varnish-Cookie-Debug = "Cleaned request cookie: " + bereq.http.Cookie;

        if (beresp.ttl <= 0s
            || beresp.http.Set-Cookie
            || beresp.http.Surrogate-control ~ "no-store"
            || (!beresp.http.Surrogate-Control && beresp.http.Cache-Control ~ "no-cache|no-store|private")
            || beresp.http.Vary == "*") {

            /* * Mark as "Hit-For-Pass" for the next 2 minutes */
            set beresp.ttl = 120s;
            set beresp.uncacheable = true;

            return (deliver);
        }
    }

And then test with ``wget``::

    cd /tmp # wget wants to save files...
    wget -S http://www.site.fi
    --2011-11-16 11:28:37--  http://www.site.fi/
    Resolving www.site.fi (www.site.fi)... xx.20.128.xx
    Connecting to www.site.fi (www.site.fi)|xx.20.128.xx|:80... connected.
    HTTP request sent, awaiting response...
      HTTP/1.1 200 OK
      Server: Zope/(2.12.17, python 2.6.6, linux2) ZServer/1.1
      X-Cache-Operation: plone.app.caching.noCaching
      Content-Language: fi
      Expires: Sun, 18 Nov 2001 09:28:37 GMT
      Cache-Control: max-age=0, must-revalidate, private
      X-Cache-Rule: plone.content.folderView
      Content-Type: text/html;charset=utf-8
      Set-Cookie: I18N_LANGUAGE="fi"; Path=/
      Content-Length: 23836
      X-Varnish-Cookie-Debug:Cleaned request cookie: __gads=ID=1477fbe04d35a542:T=1405963607:S=ALNI_MYJat5RSzKvD5xve78jLJsxl6-b_Q; __ac="NjE2NDZkNjk2ZTo2NDMxMzQyNDcwMzQ3MjMwNmMzMTc2MzM3Mg%253D%253D"
      Date: Wed, 16 Nov 2011 09:28:37 GMT
      X-Varnish: 1562749485
      Age: 0
      Via: 1.1 varnish-v4

More info
---------

* https://info.varnish-software.com/blog/adding-headers-gain-insight-vcl

Plone Language cookie (I18N_LANGUAGE)
-------------------------------------

This cookie could be removed in ``vcl_fetch`` response post-processing.
However, a better solution is to disable this cookie in the backend itself: in this case in Plone's ``portal_languages`` tool.
Disable it by :guilabel:`Use cookie for manual override` setting in ``portal_languages``.

More info
---------

* :doc:`Plone cookies documentation </develop/plone/sessions/cookies>`

* https://www.varnish-cache.org/docs/4.1/users-guide/increasing-your-hitrate.html#cookies

Do not cache error pages
========================

You can make sure that Varnish does not accidentally cache error pages.
For example, Varnish could cache the front page when the site is down, and we want to prevent that::

    sub vcl_backend_response {
        # Don't cache 50x responses
        if (beresp.status >= 500 && beresp.status < 600) {
            return (abandon);
        }
        ...
    }


Custom and full cache purges
============================

Below is an example of how to create an action to purge the whole Varnish cache.

First you need to allow an ``HTTP PURGE`` request in ``default.vcl`` from ``localhost``.
We'll create a special ``PURGE`` command which takes URLs to be purged out of the cache in a special header::

    acl purge {
        "localhost";
        # XXX: Add your local computer public IP here if you
        # want to test the code against the production server
        # from the development instance
    }
    ...

    sub vcl_recv {
        ...
        # Allow PURGE requests clearing everything
        if (req.method == "PURGE") {
            if (!client.ip ~ purge) {
                return(synth(405, "Not allowed."));
            }
            return (purge);
        }
    }

Then let's create a Plone view which will make a request from Plone to Varnish (``upstream localhost:80``) and issue the ``PURGE`` command.
We do this using the `Requests <https://pypi.python.org/pypi/requests>`_ Python library.

Example view code::

    import requests

    from Products.Five import BrowserView

    from requests.models import Request

    class Purge(BrowserView):
        """
        Purge upstream cache from all entries.

        This is ideal to hook up for admins e.g. through portal_actions menu.

        You can access it as admin::

            http://site.com/@@purge

        """

        def __call__(self):
            """
            Call the parent cache using Requests Python library and issue PURGE command for all URLs.

            Pipe through the response as is.
            """

            # This is the root URL which will be purged
            # - you might want to have different value here if
            # your site has different URLs for manage and themed versions
            site_url = self.context.portal_url() + "/"

            headers = {
                       # Match all pages
                       "X-Purge-Regex" : ".*"
            }

            resp = requests.request("PURGE", site_url + "*", headers=headers)

            self.request.response["Content-type"] = "text/plain"
            text = []

            text.append("HTTP " + str(resp.status_code))

            # Dump response headers as is to the Plone user,
            # so he/she can diagnose the problem
            for key, value in resp.headers.items():
                text.append(str(key) + ": " + str(value))

            # Add payload message from the server (if any)

            if hasattr(resp, "body"):
                text.append(str(resp.body))


Registering the view in ZCML:

.. code-block:: xml

    <browser:view
            for="Products.CMFPlone.interfaces.IPloneSiteRoot"
            name="purge"
            class=".views.Purge"
            permission="cmf.ManagePortal"
            />


More info
---------

* https://www.varnish-cache.org/docs/4.1/users-guide/purging.html
