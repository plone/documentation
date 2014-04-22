================
 Caching rules 
================

.. contents :: :local:

.. admonition:: Description

    How to program front end caching server (Varnish, Apache) to cache the
    content from Plone site and thus make it faster.

Introduction
===============

Plone caching is configured using the 
`plone.app.caching <https://pypi.python.org/pypi/plone.app.caching>`_ add-on. 
It supplies a web user interface for cache configuration and default caching
rules for Plone.
 
Using only the web user interface, ``plone.app.caching`` is very flexible
already.  This document mainly deals how you can combine
``plone.app.caching`` with your custom code.

Internally ``plone.app.caching`` uses 
`z3c.caching <https://pypi.python.org/pypi/z3c.caching/>`_ which defines
programming level ZCML directives to create your cache rules.

``plone.app.caching`` does both:

* front end caching server support, and 

* in-memory cache in Zope.

``plone.app.caching`` also defines default rules for various Plone
out-of-the-box content views and item. See:

* https://github.com/plone/plone.app.caching/blob/master/plone/app/caching/caching.zcml

The caching operations (strong, moderate, weak) are defined in Python code
itself, as they have quite tricky conditions. You can find the default
operations here:

* https://github.com/plone/plone.app.caching/blob/master/plone/app/caching/operations/default.py

.. note ::

        You usually don't need to override the operation classes itself.
        ``plone.app.caching`` provides web UI to override parameters, like
        timeout, for each rule, on the *Detailed settings* tab in
        cache control panel (Create per-ruleset parameters link).

.. note ::

        Plone 3 has its own, older, caching mechanisms. 


Setting per-view cache rules
==============================

Here is an example how you can define a cache rules for your custom view
class.  In this example we want to cache our site front page in Varnish,
because is is very complex, and wakes up a lot of ZODB objects. The front
page is programmed using ``five.grok.View`` class, but it could be any kind
of view class that Plone understands.

Our front page is subject to moderate changes as new content comes in, but
the changes are not time critical, so we define a one hour timeout for
caching the front page.

.. note ::

        Currently, setting caching rules for view classes is not supported
        through the web, but using ZCML or Python is the way to go.

In our case we are also using "a dummy cache" which does not provide purging
through Plone |---| the only way to purge the front-end proxy is to do it
from the Varnish control panel.  But that is OK, because if something bad
ends up being cached, it will be gone in one hour.

Here is our ``configure.zcml`` for our custom add-on ``browser`` package:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:cache="http://namespaces.zope.org/cache"
        >

      <include package="z3c.caching" file="meta.zcml" />
    
      <!-- Let's define a ruleset which we use to cover all almost static
          pages which get heavy traffic.  This will appear in Cache
          configuration of Site setup control panel. -->
      <cache:rulesetType
          name="plone.homepage"
          title="Homepage"
          description="Site homepage view"
          />
    
      <!-- We include one grok.View class in our ruleset. This view is being
          used at the site front page. -->
      <cache:ruleset
          for=".views.CoursePage"
          ruleset="plone.homepage"
          />
    
            
    </configure>         

After defining the rule and checking that the rule appears in the caching
control panel, we'll:

* assign *Moderate caching* operation to *Homepage*;

* on the *Detailed settings* tab we'll use the *Create per-ruleset* command
  to override timeout to be 1h instead of default 24h for *Homepage*.
  
.. warning ::

        Do not enable the Zope RAM cache for page templates. Somehow, at
        some point, you will end up having some bad page HTML in Zope's
        internal cache and you have no idea how to clear it. 
        
.. note ::

        If you are testing the rule on a local computer first, remember
        to re-do caching control panels in the production environment, 
        as they are stored in the database.
   
Testing the rule
-----------------

* First, we'll test the rule on our local development computer to make sure
  that it loads;

* then we'll test the rule in the production environment with Varnish to see
  that Varnish picks up ``Expires`` header

.. note ::

        To test ``plone.app.caching`` rules you need to run the site in
        production mode (not in the foreground).  Otherwise
        ``plone.app.caching`` is disabled.

Here is an example showing how to test loading the page using the ``wget``
UNIX command-line utility (discard the retrieved document and print the HTTP
response headers)::

    $ wget --output-document=/dev/null --server-response http://localhost:8080/ 

The output looks like this::        

    huiske-imac:tmp moo$ wget --output-document=/dev/null --server-response http://localhost:8080/LS/courses
    --2011-08-03 15:18:27--  http://localhost:8080/LS/courses
    Resolving localhost (localhost)... 127.0.0.1, ::1
    Connecting to localhost (localhost)|127.0.0.1|:8080... connected.
    HTTP request sent, awaiting response... 
      HTTP/1.0 200 OK
      Server: Zope/(2.13.7, python 2.6.4, darwin) ZServer/1.1
      Date: Wed, 03 Aug 2011 12:18:55 GMT
      Content-Length: 42780
      X-Cache-Operation: plone.app.caching.moderateCaching
      Content-Language: en
      Expires: Sun, 05 Aug 2001 12:18:55 GMT
      Connection: Keep-Alive
      Cache-Control: max-age=0, s-maxage=3600, must-revalidate
      X-Cache-Rule: plone.homepage
      Content-Type: text/html;charset=utf-8
    Length: 42780 (42K) [text/html]

We see that ``X-Cache-Operation`` and ``X-Cache-Rule`` from
``plone.app.caching`` debug info are present, so we know that it is setting
HTTP headers correctly, so that the front end server (Varnish) will receive
the appropriate directives.

After deploying the change in the production environment, we'll check
Varnish is picking up the rule. We fetch the page twice: first run is *cold*
(not yet cached), the second run should be cached::

    wget --output-document=/dev/null --server-response http://www.site.com/courses
    wget --output-document=/dev/null --server-response http://www.site.com/courses        

The output::

    huiske-imac:tmp moo$ wget -S http://www.site.com/courses
    --2011-08-03 15:39:10--  http://www.site.com/courses
    Resolving www.site.com (www.site.com)... 79.125.22.172
    Connecting to www.site.com (www.site.com)|79.125.22.172|:80... connected.
    HTTP request sent, awaiting response... 
      HTTP/1.1 200 OK
      Server: Zope/(2.13.7, python 2.6.5, linux2) ZServer/1.1
      X-Cache-Operation: plone.app.caching.moderateCaching
      Content-Language: en
      Expires: Sun, 05 Aug 2001 12:34:06 GMT
      Cache-Control: max-age=0, s-maxage=3600, must-revalidate
      X-Cache-Rule: plone.homepage
      Content-Type: text/html;charset=utf-8
      Content-Length: 43466
      Date: Wed, 03 Aug 2011 12:34:14 GMT
      X-Varnish: 72735907 72735905
      Age: 8
      Via: 1.1 varnish
      Connection: keep-alive
    Length: 43466 (42K) [text/html]

We'll see that you have **two** numbers on line from Varnish::

    X-Varnish: 72735907 72735905
        
These are Varnish internal timestamps: when the request was pulled to the
cache and when it was served. If you see only one number on subsequent
requests it means that Varnish is not caching the request (because it's
fetching the page from Plone every time). If you see two numbers you know it
is OK (and you can feel the speed).          

More info:

* http://stackoverflow.com/questions/6170962/plone-app-caching-for-front-page-only

Creating a "cache forever" view
================================

You might create views which generate or produce resources (images, JS, CSS)
in-fly. If you refer this views always through content unique URL 
you can cache the view result forever.

This can be done

* Using blob._p_mtime, or similar, to get the modified timestamp of the related content item.
  All persistent ZODB objects have _p_mtime

* Setting *plone.stableResource* ruleset on the view

Related ZCML

.. code-block:: xml

     <configure
         xmlns="http://namespaces.zope.org/zope"
         xmlns:browser="http://namespaces.zope.org/browser"
         xmlns:cache="http://namespaces.zope.org/cache"
         >
     
       <include package="z3c.caching" file="meta.zcml" />
       <include package="plone.app.caching" />
     
       <!-- Because we generate the image URL containing image modified timestamp,
            the URL is always stable and when image changes the URL changes.
            Thus, we can use strong caching (cache URL forever)
         -->
     
       <cache:ruleset
           for=".views.ImagePortletImageDownload"
           ruleset="plone.stableResource"
           />
     
     
     </configure>
     
Related view code::

    class ImagePortletImageDownload(ImagePortletHelper):
        """
        Expose image fields as downloadable BLOBS from the image portlet.

        Allow set caching rules (content caching for this view)
        """
        grok.context(Interface)
        grok.name("image-portlet-downloader")

        def render(self):
            """

            """
            content = self.context

            # Read portlet assignment pointers from the GET query
            name = self.request.form.get("portletName")
            portletManager = self.request.form.get("portletManager")
            imageId = self.request.form.get("image")

            # Resolve portlet and its image field
            manager = getUtility(IPortletManager, name=portletManager, context=content)
            mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)
            portlet = mapping[name]
            image = getattr(portlet, imageId, None)
            if not image:
                # Ohops?
                return ""

            # Set content type and length headers
            set_headers(image, self.request.response)

            # Push data to the downstream clients
            return stream_data(image)

When we refer to the view in ``<img src>`` we use modified time parameter::

    def getImageURL(self, imageDesc):
        """
        :return: The URL where the image can be downloaded from.

        """
        context = self.context.aq_inner

        params = dict(
            portletName=self.__portlet_metadata__["name"],
            portletManager=self.__portlet_metadata__["manager"],
            image=imageDesc["id"],
            modified=self.data._p_mtime
        )

        imageURL = "%s/@@image-portlet-downloader?%s" % (context.absolute_url(), urllib.urlencode(params))

        return imageURL


.. |---| unicode:: U+02014 .. em dash
