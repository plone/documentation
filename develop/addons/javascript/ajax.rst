====
AJAX
====

.. admonition:: Description

    Creating AJAX programming logic in Plone.


Introduction
============

´AJAX <http://en.wikipedia.org/wiki/Ajax_%28programming%29>`_ (an acronym for Asynchronous JavaScript and XML) is a group of interrelated web development techniques used on the client-side to create asynchronous web applications.

JSON views and loading data via AJAX
====================================

The best way to output JSON for AJAX call endpoints is to use Python's dict structure and convert
it to JSON using Python ``json.dumps()`` call.

You should pass the AJAX target URLs to your JavaScript using the settings passing pattern explained above.

Examples

Generator

* https://github.com/miohtama/silvuple/blob/master/silvuple/views.py#L342

AJAX loader

* https://github.com/miohtama/silvuple/blob/master/silvuple/static/main.js#L247

Cross-Origin Resource Sharing (CORS) proxy view
===============================================

Old web browsers do not support `Allow-acces-origin HTTP header <https://developer.mozilla.org/en-US/docs/Web/HTTP/Access_control_CORS>`_
needed to do cross-domain AJAX requests (IE6, IE7).

Below is an example how to work around this for jQuery getJSON() calls by

* Detecting browsers which do not support this using jQuery.support API

* Doing an alternative code path through a local website proxy view which uses Python ``urllib``
  to make server-to-server call and return it as it would be a local call, thus
  working around cross-domain restriction

This example is for Plone, but the code is portable to other web frameworks.

.. note::

        This is not a full example code. Basic Python and JavaScript skills are needed
        to interpret and adapt the code for your use case.

JavaScript example

.. code-block:: javascript

        /**
         * Call a RESTful service vie AJAX
         *
         * The final URL is constructed by REST function name, based
         * on a base URL from the global settings.
         *
         * If the browser does not support cross domain AJAX calls
         * we'll use a proxy function on the local server. For
         * performance reasons we do this only when absolutely needed.
         *
         * @param {String} functionName REST function name to a call
         *
         * @param {Object} Arguments as a dictionary like object, passed to remote call
         */
        function callRESTful(functionName, args, callback) {

            var src = myoptions.restService + "/" +functionName;

            // set to true to do proxied request on every browser
            // useful if you want to use Firebug to debug your server-side proxy view
            var debug = false;

                console.log("Doing remote call to:" + src)

                // We use jQuery API to detect whether a browser supports cross domain AJAX calls
                // http://api.jquery.com/jQuery.support/
                if(!jQuery.support.cors || debug) {
                        // http://alexn.org/blog/2011/03/24/cross-domain-requests.html
                        // Opera 10 doesn't have this feature, neither do IExplorer < 8, Firefox < 3.5

                        console.log("Mangling getJSON to go through a local proxy")

                        // Change getJSON to go to our proxy view on a local server
                        // and pass the orignal URL as a parameter
                        // The proxy view location is given as a global JS variable
                        args.url = src;
                        src = myoptions.portalUrl + "/@@proxy";
                }

                // Load data from the server
                $.getJSON(src, args, function(data) {
                        // Parse incoming data and construct Table rows according to it
                        console.log("Data successfully loaded");
                        callback(data, args);

             });

        }

The server-side view::


        import socket
        import urllib
        import urllib2
        from urllib2 import HTTPError

        from Products.Five import BrowserView
        from mysite.app import options


        class Proxy(BrowserView):
            """
            Pass a AJAX call to a remote server. This view is mainly indended to be used
            with jQuery.getJSON() requests.

            This will work around problems when a browser does not support Allow-Access-Origin HTTP header (IE).

            Asssuming only HTTP GET requests are made.s
            """

            def isAllowed(self, url):
                """
                Check whether we are allowed to call the target URL.

                This prevents using your service as an malicious proxy
                (to call any internet service).
                """

                allowed_prefix = options.REST_SERVICE_URL

                if url.startswith(allowed_prefix):
                    return True

                return False

            def render(self):
                """
                Use HTTP GET ``url`` query parameter for the target of the real request.
                """

                # Make sure any theming layer won't think this is HTML
                # http://stackoverflow.com/questions/477816/the-right-json-content-type
                self.request.response.setHeader("Content-type", "application/json")

                url = self.request.get("url", None)
                if not url:
                    self.request.response.setStatus(500, "url parameter missing")

                if not self.isAllowed(url):
                    # The server understood the request, but is refusing to fulfill it. Authorization will not help and the request SHOULD NOT be repeate
                    self.request.response.setStatus(403, "proxying to the target URL not allowed")
                    return

                # Pass other HTTP GET query parameters direclty to the target server
                params = {}
                for key, value in self.request.form.items():
                    if key != "url":
                        params[key] = value

                # http://www.voidspace.org.uk/python/articles/urllib2.shtml
                data = urllib.urlencode(params)

                full_url = url + "?" + data
                req = urllib2.Request(full_url)

                try:

                    # Important or if the remote server is slow
                    # all our web server threads get stuck here
                    # But this is UGLY as Python does not provide per-thread
                    # or per-socket timeouts thru urllib
                    orignal_timeout = socket.getdefaulttimeout()
                    try:
                        socket.setdefaulttimeout(10)

                        response = urllib2.urlopen(req)
                    finally:
                        # restore orignal timeoout
                        socket.setdefaulttimeout(orignal_timeout)


                    # XXX: How to stream respone through Zope
                    # AFAIK - we cannot do it currently

                    return response.read()

                except HTTPError, e:
                    # Have something more useful to log output as plain urllib exception
                    # using Python logging interface
                    # http://docs.python.org/library/logging.html
                    logger.error("Server did not return HTTP 200 when calling remote proxy URL:" + url)
                    for key, value in params.items():
                        logger.error(key + ": "  + value)

                    # Print the server-side stack trace / error page
                    logger.error(e.read())

                    raise e

Registering the view in ZCML:

.. code-block:: xml

    <browser:view
            for="Products.CMFPlone.interfaces.IPloneSiteRoot"
            name="proxy"
            class=".views.Proxy"
            permission="zope.Public"
            />


Speeding up AJAX loaded content HTML
====================================

By observing Plone's ``main_template.pt``, having a True value on the ``ajax_load`` request key means some parts of the page aren't displayed, hence the speed:

* No CSS or JavaScript from ``<head />`` tag is loaded

* Nothing from the ``plone.portaltop`` ViewletManager, such as the personal bar, searchbox, logo and main menu

* Nothing from the ``plone.portalfooter`` ViewletManager, which contains footer and colophon information, site actions and the Analytics javascript calls if you have that configured in your site

* Neither the left nor the right column, along with all the portlets there assigned
