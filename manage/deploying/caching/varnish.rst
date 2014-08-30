===================
 Varnish
===================

.. admonition:: Description

    Varnish is a caching front-end server. This document has notes on how to
    use Varnish with Plone.

.. contents:: :local:

.. highlight:: console

Introduction
============

This chapter contains information about using the Varnish caching proxy with
Plone.

* http://varnish-cache.org/

To use Varnish with Plone

* Learn how to install and configure Varnish

* Add Plone virtual hosting rule to the default varnish configuration

.. note ::

    Some of these examples were written for Varnish 2.x.
    Varnish 3.x (Jun 2011) and Varnish 4.x (Apr 2014) has radically altered syntax of VCL language
    and command line tools, so you might need to adapt the examples a bit.

Installation
==========================

The suggest method to install Varnish is to use your OS package manager.

* You can install using packages (RPM/DEB) - consult your operating system instructions.

* For more up to date packages for Debian you could check: https://www.varnish-cache.org/installation/debian

* You can install backports

* You can install using buildout

Buildout examples

* https://pypi.python.org/pypi/plone.recipe.varnish

Management console
==================

``varnishadm``
--------------------------------------------

You can access Varnish admin console on your server by::

    # Your system uses a secret handshake file
    varnishadm -T localhost:6082 -S /etc/varnish/secret

(Ubuntu/Debian installation)

Telnet console
-----------------

The telnet management console is available on some configurations
where ``varnishadm`` cannot be used. The functionality is the same.

Example::

    ssh yourhost
    # Your system does not have a secret handshake file
    telnet localhost 6082

.. note::

    Port number depends on your Varnish settings.

More info

* http://opensourcehacker.com/2013/02/07/varnish-shell-singleliners-reload-config-purge-cache-and-test-hits/

Quit console
-------------

Quit command::

   quit

Purging the cache
------------------

This will remove all entries from the Varnish cache::

   varnishadm "ban.url ."


Loading new VCL to live Varnish
===============================

More often than not, it is beneficial to load new configuration without
bringing the cache down for maintenance.  Using this method also checks the
new VCL for syntax errors before activating it.  Logging in to Varnish CLI
requires the ``varnishadm`` tool, the address of the management interface,
and the secret file for authentication.

See the ``varnishadm`` man-page for details.

Opening a new CLI connection to the Varnish console, in a buildout-based
Varnish installation::

    parts/varnish-build/bin/varnishadm -T localhost:8088

Port 8088 is defined in ``buildout.cfg``::

    [varnish-instance]
    telnet = localhost:8088

Opening a new CLI connection to the Varnish console, in a system-wide
Varnish installation on Ubuntu/Debian::

    varnishadm -T localhost:6082 -S /etc/varnish/secret

You can dynamically load and parse a new VCL config file to memory::

    vcl.load <name> <file>

For example::

    vcl.load newconf_1 /etc/varnish/newconf.vcl

... or ... ::

    # Ubuntu / Debian default config
    vcl.load defconf1 /etc/varnish/default.vcl

``vcl.load`` will load and compile the new configuration. Compilation will
fail and report on syntax errors.  Now that the new configuration has been
loaded, it can be activated with::

    vcl.use newconf_1

.. note::

    Varnish remembers ``<name>`` in ``vcl.load``, so every time you
    need to reload your config you need to invent a new name for
    vcl.load / vcl.use command pair.

See

* http://opensourcehacker.com/2013/02/07/varnish-shell-singleliners-reload-config-purge-cache-and-test-hits/

Logs
======

To see a real-time log dump (in a system-wide Varnish configuration)::

    varnishlog

By default, Varnish does not log to any file and keeps the log only in
memory.  If you want to extract Apache-like logs from varnish, you need to
use the ``varnishncsa`` utility.

Stats
=====

Check live "top-like" Varnish statistics::

    parts/varnish-build/bin/varnishstat

Use the admin console to print stats for you::

    stats
    200 2114

           95717  Client connections accepted
          132889  Client requests received
           38638  Cache hits
           21261  Cache hits for pass
          ...

Virtual hosting proxy rule
==========================

Varnish 4.x example
--------------------

Varnish 4.x has been released, almost three years after the release of Varnish 3.0 in June 2011, 
the backend fetch parts of VCL again have changed in Varnish 4.

An example with two separate Plone installations (Zope standalone mode)
behind Varnish 4.x HTTP 80 port.

Example::

    # To make sure that people have upgraded their VCL to the current version, 
    # Varnish now requires the first line of VCL to indicate the VCL version number
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

    sub vcl_purge {
        return (synth(200, "Purged"));
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

    #
    # Show custom helpful 500 page when the upstream does not respond
    # vcl_error is now vcl_backend_error

    sub vcl_backend_error {
        // Let's deliver a friendlier error page.
        // You can customize this as you wish.
        set resp.http.Content-Type = "text/html; charset=utf-8";
        set resp.http.Retry-After = "5";
        synthetic( {"
            <?xml version="1.0" encoding="utf-8"?>
            <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
            "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
            <html>
             <head>
              <title>"} + resp.status + " " + resp.reason + {"</title>
              <style type="text/css">
               #page {width: 400px; padding: 10px; margin: 20px auto; border: 1px solid black; background-color: #FFF;}
               p {margin-left:20px;}
               body {background-color: #DDD; margin: auto;}
              </style>
             </head>
             <body>
              <div id="page">
               <h1>This page is not available</h1>
                <p>Sorry, not available.</p>
                <hr />
                <h4>Debug Info:</h4>
                <pre>Status: "} + resp.status + {" Response: "} + resp.reason + {" XID: "} + req.xid + {"</pre>
              </div>
             </body>
            </html>
        "} );
        return (deliver);
    }

Varnish 3.x example
-------------------

An example with two separate Plone installations (Zope standalone mode)
behind Varnish 3.x HTTP 80 port.

Example::

    #
    # This backend never responds... we get hit in the case of bad virtualhost name
    #
    backend default {
        .host = "127.0.0.1";
        .port = "55555";
    }

    #
    # Plone Zope front end clients running on koskela
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
            set req.backend = site2;

            # Zope VirtualHostMonster
            set req.url = "/VirtualHostBase/http/" + req.http.host + ":80/Plone/VirtualHostRoot" + req.url;

        }

        if (req.http.host ~ "^(.*\.)?site1\.fi(:[0-9]+)?$") {
            set req.backend = site1;

            # Zope VirtualHostMonster
            set req.url = "/VirtualHostBase/http/" + req.http.host + ":80/Plone/VirtualHostRoot" + req.url;
        }

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
                remove req.http.Cookie;
            }
        }

        call choose_backend;

        if (req.request != "GET" &&
          req.request != "HEAD" &&
          req.request != "PUT" &&
          req.request != "POST" &&
          req.request != "TRACE" &&
          req.request != "OPTIONS" &&
          req.request != "DELETE") {
            /* Non-RFC2616 or CONNECT which is weird. */
            return (pipe);
        }
        if (req.request != "GET" && req.request != "HEAD") {
            /* We only deal with GET and HEAD by default */
            return (pass);
        }
        if (req.http.Authorization || req.http.Cookie) {
            /* Not cacheable by default */
            return (pass);
        }
        return (lookup);
    }


    #
    # Show custom helpful 500 page when the upstream does not respond
    #
    sub vcl_error {
      // Let's deliver a friendlier error page.
      // You can customize this as you wish.
      set obj.http.Content-Type = "text/html; charset=utf-8";
      synthetic {"
      <?xml version="1.0" encoding="utf-8"?>
      <!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
       "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
      <html>
        <head>
          <title>"} + obj.status + " " + obj.response + {"</title>
          <style type="text/css">
          #page {width: 400px; padding: 10px; margin: 20px auto; border: 1px solid black; background-color: #FFF;}
          p {margin-left:20px;}
          body {background-color: #DDD; margin: auto;}
          </style>
        </head>
        <body>
        <div id="page">
        <h1>This page is not available</h1>
        <p>Sorry, not available.</p>
        <hr />
        <h4>Debug Info:</h4>
        <pre>Status: "} + obj.status + {"
    Response: "} + obj.response + {"
    XID: "} + req.xid + {"</pre>
          </div>
        </body>
       </html>
      "};
      return(deliver);
    }

Varnish 2.x example
-------------------

When Varnish has been set-up you need to include Plone virtual hosting
rule in its configuration file.

If you want to map Varnish backend directly to Plone-as-a-virtualhost (i.e.
Zope's VirtualHostMonster is used to map site name to Plone site instance
id) use ``req.url`` mutating.

The following maps the Plone site id *plonecommunity* to the
*plonecommunity.mobi* domain.  Plone is a single Zope instance, running on
port 9999.

Example::

    backend plonecommunity {
            .host = "127.0.0.1";
            .port = "9999";
    }

    sub vcl_recv {
            if (req.http.host ~ "^(www.)?plonecommunity.mobi(:[0-9]+)?$"
                || req.http.host ~ "^plonecommunity.mfabrik.com(:[0-9]+)?$") {

                    set req.backend = plonecommunity
                    set req.url = "/VirtualHostBase/http/" req.http.host ":80/plonecommunity/VirtualHostRoot" req.url;
                    set req.backend = plonecommunity;
            }
    }



Varnishd port and IP address to listen
========================================

You give IP address(s) and ports to Varnish to listen to
on the ``varnishd`` command line using -a switch.
Edit ``/etc/default/varnish``::

    DAEMON_OPTS="-a 192.168.1.1:80 \
                 -T localhost:6082 \
                 -f /etc/varnish/default.vcl \
                 -s file,/var/lib/varnish/$INSTANCE/varnish_storage.bin,1G"


Cached and editor subdomains
==============================

You can provide an uncached version of the site for editors:

* http://serverfault.com/questions/297541/varnish-cached-and-non-cached-subdomains/297547#297547

Varnish and I18N
=================

Please see :doc:`cache issues related to LinguaPlone </develop/plone/i18n/cache>`.

Sanitizing cookies
==================

Any cookie set on the server side (session cookie) or on the client-side
(e.g. Google Analytics Javascript cookies)
is poison for caching the anonymous visitor content.

HTTP caching needs to deal with both HTTP request and response cookie handling

* HTTP request *Cookie* header. The browser sending HTTP request
  with ``Cookie`` header confuses Varnish cache look-up. This header can be
  set by Javascript also, not just by the server.
  ``Cookie`` can be preprocessed in varnish's ``vcl_recv`` step.

* HTTP response ``Set-Cookie`` header.
  This sets a server-side cookie. If your server is setting
  cookies Varnish does not cache these responses by default.
  Howerver, this might be desirable
  behavior if e.g. multi-lingual content is served from one URL with
  language cookies.
  ``Set-Cookie`` can be post-processed in varnish's ``vcl_fetch`` step.

Example of removing all Plone-related cookies,
besides ones dealing with the logged in users (content authors)::

    sub vcl_recv {

      if (req.http.Cookie) {
          # (logged in user, status message - NO session storage or language cookie)
          set req.http.Cookie = ";" req.http.Cookie;
          set req.http.Cookie = regsuball(req.http.Cookie, "; +", ";");
          set req.http.Cookie = regsuball(req.http.Cookie, ";(statusmessages|__ac|_ZopeId|__cp)=", "; \1=");
          set req.http.Cookie = regsuball(req.http.Cookie, ";[^ ][^;]*", "");
          set req.http.Cookie = regsuball(req.http.Cookie, "^[; ]+|[; ]+$", "");

          if (req.http.Cookie == "") {
              remove req.http.Cookie;
          }
      }
      ...

    # Let's not remove Set-Cookie header in VCL fetch
    sub vcl_fetch {

        # Here we could unset cookies explicitly,
        # but we assume plone.app.caching extension does it jobs
        # and no extra cookies fall through for HTTP responses we'd like to cache
        # (like images)

        if (!beresp.cacheable) {
            return (pass);
        }
        if (beresp.http.Set-Cookie) {
            return (pass);
        }
        set beresp.prefetch =  -30s;
        return (deliver);
    }

In the Varnish 4.x vcl_fetch is now vcl_backend_response, then the above example looks like this::

    sub vcl_recv {

      if (req.http.Cookie) {
          # (logged in user, status message - NO session storage or language cookie)
          set req.http.Cookie = ";" req.http.Cookie;
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

        if (!beresp.ttl > 0s) {
          set beresp.uncacheable = true;
          return (deliver);
        }
 
        if (beresp.http.Set-Cookie) {
          set beresp.uncacheable = true;
          return (deliver);
        }

        set beresp.grace = 120s;
        return (deliver);
    }

The snippet for stripping out non-Plone cookies comes from
http://www.phase2technology.com/node/1218/

That article notes that "this processing occurs only between Varnish and the
backend [...]; the client, typically a user’s browser, still has all the
cookies.  Nothing is happening to the client’s original request." While it's
true that the browser still has the cookies, they never reach the backend
and are therefor ignored.

Another example how to purge Google cookies only and allow other cookies by default::

    sub vcl_recv {
        # Remove Google Analytics cookies - will prevent caching of anon content
        # when using GA Javascript. Also you will lose the information of
        # time spend on the site etc..
        if (req.http.cookie) {
           set req.http.Cookie = regsuball(req.http.Cookie, "__utm.=[^;]+(; )?", "");
           if (req.http.cookie ~ "^ *$") {
               remove req.http.cookie;
           }
         }
         ....

Debugging cookie issues
------------------------------------

Use the following snippet to set a HTTP response debug header to see what
the backend server sees as cookie after ``vcl_recv`` clean-up regexes::

    sub vcl_fetch {

        /* Use to see what cookies go through our filtering code to the server */
        set beresp.http.X-Varnish-Cookie-Debug = "Cleaned request cookie: " + req.http.Cookie;

        if (beresp.ttl <= 0s ||
            beresp.http.Set-Cookie ||
            beresp.http.Vary == "*") {
            /*
             * Mark as "Hit-For-Pass" for the next 2 minutes
             */
            set beresp.ttl = 120 s;
            return (hit_for_pass);
        }
        return (deliver);
    }

Varnish 4.x::

    sub vcl_backend_response {

        /* Use to see what cookies go through our filtering code to the server */
        set beresp.http.X-Varnish-Cookie-Debug = "Cleaned request cookie: " + req.http.Cookie;

        if (beresp.ttl <= 0s ||
            beresp.http.Set-Cookie ||
            beresp.http.Vary == "*") {
            /*
             * Mark as "Hit-For-Pass" for the next 2 minutes
             */
            # hit_for_pass objects are created using beresp.uncacheable
            set beresp.uncacheable = true;
            set beresp.ttl = 120s;
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
      X-Cookie-Debug: Request cookie: (null)
      Date: Wed, 16 Nov 2011 09:28:37 GMT
      X-Varnish: 1562749485
      Age: 0
      Via: 1.1 varnish

Plone Language cookie (I18N_LANGUAGE)
-------------------------------------

This cookie could be removed in ``vcl_fetch`` response post-processing (how?).
However, a better solution is to disable this cookie in the backend itself:
in this case in Plone's ``portal_languages`` tool.
Disable it by :guilabel:`Use cookie for manual override` setting in
``portal_languages``.

More info
---------

* :doc:`Plone cookies documentation </develop/plone/sessions/cookies>`

* https://www.varnish-cache.org/trac/wiki/VCLExampleCacheCookies

* https://www.varnish-cache.org/trac/wiki/VCLExampleRemovingSomeCookies

* https://www.varnish-cache.org/docs/3.0/tutorial/cookies.html

Do not cache error pages
==========================

You can make sure that Varnish does not accidentally cache error pages.
E.g. it would cache front page when the site is down::

    sub vcl_fetch {
        if ( beresp.status >= 500 ) {
            set beresp.ttl = 0s;
            set beresp.cacheable = false;
        }
        ...
    }

More info

* https://www.varnish-cache.org/lists/pipermail/varnish-misc/2010-February/003774.html

Custom and full cache purges
============================

Below is an example how to create an action to purge the whole Varnish cache.

First you need to allow ``HTTP PURGE`` request in ``default.vcl`` from
``localhost``.
We'll create a special ``PURGE`` command which takes URLs to be purged out of
the cache in a special header::

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
        if (req.request == "PURGE") {
            if (!client.ip ~ purge) {
                error 405 "Not allowed.";
            }
            # Purge for the current host using reg-ex from X-Purge-Regex header
            purge("req.http.host == " req.http.host " && req.url ~ " req.http.X-Purge-Regex);
            error 200 "Purged.";
        }
    }

In the Varnish 4.x::

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

Then let's create a Plone view which will make a request from Plone to
Varnish (``upstream localhost:80``)
and issue the ``PURGE`` command.
We do this using the `Requests <https://pypi.python.org/pypi/requests>`_
Python library.

Example view code::

    import requests

    from Products.CMFCore.interfaces import ISiteRoot
    from five import grok

    from requests.models import Request

    class Purge(grok.CodeView):
        """
        Purge upstream cache from all entries.

        This is ideal to hook up for admins e.g. through portal_actions menu.

        You can access it as admin::

            http://site.com/@@purge

        """

        grok.context(ISiteRoot)

        # Onlyl site admins can use this
        grok.require("cmf.ManagePortal")

        def render(self):
            """
            Call the parent cache using Requets Python library and issue PURGE command for all URLs.

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



More info

* https://www.varnish-cache.org/docs/3.0/tutorial/purging.html

* https://www.varnish-cache.org/trac/wiki/BackendConditionalRequests

* http://kristianlyng.wordpress.com/2010/02/02/varnish-purges/


Round-robin balancing
========================

Varnish can do round-robin load balancing internally.
Use this if you want to distribute CPU-intensive load between several
ZEO front end client instances, each listening on
its own port.

Example::

    # Round-robin between two ZEO front end clients

    backend app1 {
        .host = "localhost";
        .port = "8080";
    }

    backend app2 {
        .host = "localhost";
        .port = "8081";
    }

    director app_director round-robin {
        {
            .backend = app1;
        }
        {
            .backend = app2;
        }
    }

    sub vcl_recv {

    if (req.http.host ~ "(www\.|www2\.)?app\.fi(:[0-9]+)?$") {
        set req.url = "/VirtualHostBase/http/www.app.fi:80/app/app/VirtualHostRoot" req.url;

        # Varnish 3.x
        #set req.url = "/VirtualHostBase/http/" + req.http.host + ":80/app/app/VirtualHostRoot" + req.url;

        set req.backend = app_director;
    }

Example with Varnish 4::

    # Round-robin between two ZEO front end clients

    backend app1 {
        .host = "localhost";
        .port = "8080";
    }

    backend app2 {
        .host = "localhost";
        .port = "8081";
    }

    # Directors have been moved to the vmod_directors
    # To make directors (backend selection logic) easier to extend, the directors are now defined in loadable VMODs.
    # Setting a backend for future fetches in vcl_recv is now done as bellow, is an example redirector based on round-robin requests.

    import directors;

    sub vcl_init {
        new cluster1 = directors.round_robin();
        cluster1.add_backend(site1);    # Backend site1 defined above
        cluster1.add_backend(site2);    # Backend site2 defined above
    }


    sub vcl_recv {
        if (req.http.host ~ "(www\.|www2\.)?app\.fi(:[0-9]+)?$") {
            set req.backend_hint = cluster1.backend();
            set req.url = "/VirtualHostBase/http/" + req.http.host + ":80/app/app/VirtualHostRoot" + req.url;
        }

        ...
    }
