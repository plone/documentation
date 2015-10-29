========
 Apache
========

.. admonition:: Description

        Tips and guides for hosting Plone with Apache web server.

.. contents :: :local:

Introduction
------------

Here are useful information and snippets when hosting Plone behind Apache.

Installing Apache front-end for Plone
---------------------------------------

Apache runs on port 80. Plone runs on port 8080. Apache accepts all HTTP
traffic to your internet domain.

Here are quick instructions for Ubuntu / Debian.

Install required software::

	sudo apt-get install apache2
	sudo a2enmod rewrite
	sudo a2enmod proxy
	sudo a2enmod proxy_http
	sudo a2enmod headers
        sudo /etc/init.d/apache2 restart

Add virtual host config file ``/etc/apache2/sites-enabled/yoursite.conf``.
Assuming *Plone* is your site id in Zope Management Interface (capital lettering do matter) and your
domain name is ``yoursite.com`` (note with or without www matters, see below)::

        UseCanonicalName On

	NameVirtualHost *
	<VirtualHost *>
	    ServerAlias yoursite.com
	    ServerSignature On

            Header set X-Frame-Options "SAMEORIGIN"
            Header set Strict-Transport-Security "max-age=15768000; includeSubDomains"
            Header set X-XSS-Protection "1; mode=block"
            Header set X-Content-Type-Options "nosniff"
            Header set Content-Security-Policy-Report-Only "default-src 'self'; img-src *; style-src 'unsafe-inline'; script-src 'unsafe-inline' 'unsafe-eval'"

	    ProxyVia On

	    # prevent your web server from being used as global HTTP proxy
	    <LocationMatch "^[^/]">
	      Deny from all
	    </LocationMatch>

	    <Proxy *>
	        Order deny,allow
	        Allow from all
	    </Proxy>

            RewriteEngine on
	    RewriteRule ^/(.*) http://localhost:8080/VirtualHostBase/http/yoursite.com:80/Plone/VirtualHostRoot/$1 [P,L]

	</VirtualHost>

        <VirtualHost *>
            ServerAlias   *
            ServerRoot    /var/www
            ServerSignature On
        </VirtualHost>

Eventually you have one virtual host configuration file per one domain on your server.

Restart apache::

      sudo apache2ctl configtest
      sudo apache2ctl restart

Check that Plone responds::

      http://yoursite.com:8080/Plone

Check that Apache responds::

      http://yoursite.com

If everything is good then your Plone site properly configured using Apache front-end.

Content Security Policy (CSP) prevents a wide range of attacks, including cross-site scripting and other cross-site injections, but
the CSP header setting may require careful tuning.
To enable it, replace the Content-Security-Policy-Report-Only by Content-Security-Policy.
The example above works with Plone 5.x (including TinyMCE) but it very wide.
You may need to adjust it if you want to make CSP more restrictive or use additional Plone Products.
For more information, see

*  http://www.w3.org/TR/CSP/

For an SSL configuration, just modify the rewrite rule from::

	    RewriteRule ^/(.*) http://localhost:8080/VirtualHostBase/http/yoursite.com:80/Plone/VirtualHostRoot/$1 [P,L]

to::

	    RewriteRule ^/(.*) http://localhost:8080/VirtualHostBase/https/yoursite.com:443/Plone/VirtualHostRoot/$1 [P,L]

inside an SSL-enabled Apache virtual host definition.

Apache and Plone guide (old)
==============================



Procedure to restart Apache in production environment
------------------------------------------------------

You might share the same Apache web server across several production sites.
You don't want to hinder the performance of the other sites when doing Apache configuration changes to one site.

The correct procedure to restart Apache is (on Ubuntu/Debian Linux)

.. code-block:: console

        # Check that config files are working after editing them
        apache2ctl configtest

        # Let Apache finish serving all the on-going requests before
        # restarting worker processes
        apache2ctl graceful

www-redirects
-------------

If you wish to force people to use your site with or without www prefix you can use the rules below.
Note that setting this kind of rule is very useful from the search engine optimization point of view also.

Example in <VirtualHost> section to redirect www.site.com -> site.com::

  <VirtualHost 127.0.0.1:80>

           ServerName site.com
           ServerAlias www.site.com


          <IfModule mod_rewrite.c>
               RewriteEngine On
               RewriteCond %{HTTP_HOST} ^www\.site\.com [NC]
               RewriteRule (.*) http://site.com$1 [L,R=302]

           </IfModule>

Example in <VirtualHost> section to redirect site.com -> www.site.com::

  <VirtualHost 127.0.0.1:80>

           ServerName site.com
           ServerAlias www.site.com


          <IfModule mod_rewrite.c>
               RewriteEngine On
               RewriteCond %{HTTP_HOST} ^site\.com [NC]
               RewriteRule (.*) http://www.site.com$1 [L,R=302]
           </IfModule>

Redirecting all the pages to the root of a new site:

       RewriteEngine On
       RewriteRule (.*) http://www.newsite.com [L,R=302]

Migration redirects
--------------------

To redirect traffic from all pages permanently (301) to the landing page of a new site::

	RewriteEngine On
	RewriteRule (.*) http://docs.plone.org/ [L,R=301]

Proxying other site under Plone URI space
-----------------------------------------

The following rule can be used to put a static web site to sit in the same URI space with Plone.
Put these rules **before** VirtualHost ProxyPass.

Examples::

   ProxyPass /othersite/ http://www.some.other.domain.com/othersite/
   ProxyPassReverse /othersite/ http://www.some.other.domain.com/othersite/

Reverse proxy host
===================

By default, host name is correctly delivered from Apache to Plone.
Otherwise you might see all your HTTP requests coming from localhost, Apache.

You need::

        ProxyPreserveHost On

For more information, see

* http://macadames.wordpress.com/2009/05/23/some-deliverance-tips/

Redirecting certain URIs to old site
-------------------------------------

This is useful if you migrate to a Plone from some legacy technology and you still need to have some part of the URI space to point to the old server.

* Create alternative domain name for the existing old site (e.g. www2)

* Modify Apache configuration so that URLs still being used are redirected to the old server with alternative name, Put in this rewrite

::

          <location /media>
                  RedirectMatch /media/(.*)$ http://www2.site.fi/media/$1
          </location>

Virtual hosting Apache configuration generator
----------------------------------------------

* http://betabug.ch/zope/witch


Caching images
---------------

First of all, there are much better caching solutions for Plone than Apache's mod_cache, see the :doc:`Guide to caching </manage/deploying/caching/index>`.

One important thing to know about mod_cache is that by default it caches Set-Cookie headers. Most likely, this is not what you want when using it with Plone, so you should use the CacheIgnoreHeaders directive to strip Set-Cookie headers from cached objects.
Have a close look at the official `Apache documentation <http://httpd.apache.org/docs/current/mod/mod_cache.html>`_) and also read the comments at the bottom, they are very informative - even more so in the `2.2 version <http://httpd.apache.org/docs/2.2/mod/mod_cache.html>`_.

If you cannot avoid using mod_cache, you can configure disk based Apache caching as follows:

First you need to enable the relevant Apache modules::

* mod_cache, mod_diskcache

On Debian this is::

	sudo a2enmod

Then you can add to your virtual host configuration::

  # Disk cache configuration
  CacheEnable disk /
  CacheRoot "/var/cache/yourorganization-production"
  CacheLastModifiedFactor 0.1
  #CacheDefaultExpire 1
  #CacheMaxExpire 7200
  CacheDirLength 2
  # the next line is important, see above
  CacheIgnoreHeaders Set-Cookie

Then go to *Cache Configration* (Plone 4.1+)
and configure `the caching options <https://pypi.python.org/pypi/plone.app.caching>`_.

Testing cache headers
---------------------

Use UNIX *wget* command. -S flag will display request headers.

Remember to do different request for HTML, CSS, JS and image payloads - the cache rules might not be the same.

HTTP example::

        cd /tmp

        wget --cache=off -S http://production.yourorganizationinternational.org/yourorganizationlogotemplate.gif

        HTTP request sent, awaiting response...
          HTTP/1.1 200 OK
          Date: Tue, 09 Mar 2010 12:33:26 GMT
          Server: Apache/2.2.8 (Ubuntu) DAV/2 SVN/1.4.6 mod_python/3.3.1 Python/2.5.2 PHP/5.2.4-2ubuntu5.4 with Suhosin-Patch mod_ssl/2.2.8 OpenSSL/0.9.8g
          Last-Modified: Wed, 25 Nov 2009 06:51:41 GMT
          Content-Length: 4837
          Via: 1.0 production.yourorganizationinternational.org
          Cache-Control: max-age=3600, public
          Expires: Tue, 09 Mar 2010 13:02:29 GMT
          Age: 1857
          Keep-Alive: timeout=15, max=100
          Connection: Keep-Alive
          Content-Type: image/gif
        Length: 4837 (4.7K) [image/gif]
        Saving to: `yourorganizationlogotemplate.gif.14'

HTTPS example::

         cd /tmp
         wget --cache=off --no-check-certificate -S https://production.yourorganizationinternational.org/


Flushing cache
--------------

Manually cleaning Apache disk cache::

	sudo -i
	cd /var/cache/yoursite
	rm -rf *

Custom 500 internal error page
--------------------------------

To make you look more pro when you update the server or Plone goes down

* https://httpd.apache.org/docs/2.2/custom-error.html

Load balanced Apache virtual host configuration
------------------------------------------------

This complex config example includes

* HTTPS and SSL certificate set-up

* Load balancing using ZEO front-ends and Apache load balancer module

* Apache disk cache. This should provide static resource caching w/HTTPS support if you are using plone.app.caching.

* https://httpd.apache.org/docs/2.2/caching.html

See

* http://stackoverflow.com/questions/5650716/are-sticky-sessions-needed-when-load-balancing-plone-3-3-5

More information about how to set a sticky session cookie if you need to support Zope sessions in your code

* http://opensourcehacker.com/2011/04/15/sticky-session-load-balancing-with-apache-and-mod_balancer-on-ubuntu-linux/

Example::

        <VirtualHost 123.123.123.123:443>

          ServerName  production.yourorganization.org
          ServerAdmin rocks@mfabrik.com

          SSLEngine On
          SSLCertificateFile /etc/apache2/ssl-keys/yourorganization.org.cer
          SSLCertificateKeyFile /etc/apache2/ssl-keys/yourorganization.org.key
          SSLCertificateChainFile /etc/apache2/ssl-keys/InstantValidationCertChain.crt

          LogFormat       combined
          TransferLog     /var/log/apache2/production.yourorganization.org.log

          <IfModule mod_proxy.c>
           ProxyVia On

           # prevent the webserver from being used as proxy
           <LocationMatch "^[^/]">
             Deny from all
           </LocationMatch>
          </IfModule>

          # Balance load between 4 ZEO front-ends
          <Proxy balancer://lbyourorganization>
            BalancerMember http://127.0.0.1:13001/
            BalancerMember http://127.0.0.1:13002/
            BalancerMember http://127.0.0.1:13003/
            BalancerMember http://127.0.0.1:13004/
            # Use Pending Request Counting Algorithm (s. http://httpd.apache.org/docs/current/mod/mod_lbmethod_bybusyness.html).
            # This will reduce latencies that occur as a result of long running requests temporarily blocking a ZEO client.
            # You will need to install the separate mod_lbmethod_bybusyness module in Apache 2.4.
            ProxySet lbmethod=bybusyness
          </Proxy>

          # Note: You might want to disable this URL of being public
          # as it can be used to access Apache live settings
          <Location /balancer-manager>
            SetHandler balancer-manager
            Order Deny,Allow
            # Your trusted IP addresses
            Allow from 123.123.123.123
          </Location>

          ProxyPass /balancer-manager !
          ProxyPass             / balancer://lbyourorganization/http://localhost/VirtualHostBase/https/production.yourorganization.org:443/yourorganization_plone_site/VirtualHostRoot/
          ProxyPassReverse      / balancer://lbyourorganization/http://localhost/VirtualHostBase/https/production.yourorganization.org:443/yourorganization_plone_site/VirtualHostRoot/

          # Disk cache configuration, if you really must use Apache for caching
          CacheEnable disk /
          # Must point to www-data writable directly which depends on OS
          CacheRoot "/var/cache/yourorganization-production"
          CacheLastModifiedFactor 0.1
          CacheIgnoreHeaders Set-Cookie

          # Debug header flags all requests coming from this server
          Header append X-YourOrganization-Production yes

        </VirtualHost>



