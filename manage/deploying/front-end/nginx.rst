=====
Nginx
=====

.. admonition:: Description

    Using the nginx web server to host Plone sites.


Introduction
============

Nginx is a modern alternative server to Apache.

* It acts as a proxy server and load balancer in front of Zope.
* It handles rewrite rules.
* It handles HTTPS.

Minimal Nginx front end configuration for Plone on Ubuntu/Debian Linux
======================================================================

This is a minimal configuration to run nginx on Ubuntu/Debian in front of a Plone site.
These instructions are *not* for configurations where one uses the buildout configuration tool to build a static Nginx server.

* Plone will by default be served on port 8080.

* We use :term:`VirtualHostMonster` to pass the original protocol and hostname to Plone. VirtualHostMonster provides a way to rewrite the request path.

* We also need to rewrite the request path, because you want the site be served from the port 80 root (``/``), where Plone sites are nested in the Zope application server as paths, for example, ``/site1``, ``/site2``, and so on.

* You don't need to configure VirtualHostMonster in Plone/Zope in any way, because all the installers will automatically install one for you. Nginx configuration is all you need to touch.

* The URL passed to VirtualHostMonster is the URL Plone uses to construct links in the template (``portal_url`` in the code, also used by content ``absolute_url()`` method). If your site loads without CSS styles, usually it is a sign that the VirtualHostMonster URL is incorrectly written. Plone uses the URL to link stylesheets also.

* Plone itself contains a mini web server (Medusa) which serves the requests from port 8080. Nginx acts as a HTTP proxy between Medusa and outgoing port 80 traffic.  Nginx does not spawn Plone process or anything like that, but Plone processes are externally controlled, usually by buildout-created ``bin/instance`` and ``bin/plonectl`` commands, or by a ``supervisor`` instance.

Create the file ``/etc/nginx/sites-available/yoursite.conf`` with the following contents:

.. code-block:: nginx

    # This adds security headers
    add_header X-Frame-Options "SAMEORIGIN";
    add_header Strict-Transport-Security "max-age=15768000; includeSubDomains";
    add_header X-XSS-Protection "1; mode=block";
    add_header X-Content-Type-Options "nosniff";
    #add_header Content-Security-Policy "default-src 'self'; img-src *; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval'";
    add_header Content-Security-Policy-Report-Only "default-src 'self'; img-src *; style-src 'self' 'unsafe-inline'; script-src 'self' 'unsafe-inline' 'unsafe-eval'";

    # This specifies which IP and port Plone is running on.
    # The default is 127.0.0.1:8080
    upstream plone {
        server 127.0.0.1:8090;
    }

    # Redirect all www-less traffic to the www.site.com domain
    # (you could also do the opposite www -> non-www domain)
    server {
        listen 80;
        server_name yoursite.com;
        return 301 http://www.yoursite.com$request_uri;
    }

    server {

        listen 80;
        server_name www.yoursite.com;
        access_log /var/log/nginx/yoursite.com.access.log;
        error_log /var/log/nginx/yoursite.com.error.log;

        # Note that domain name spelling in VirtualHostBase URL matters
        # -> this is what Plone sees as the "real" HTTP request URL.
        # "Plone" in the URL is your site id (case sensitive)
        location / {
              proxy_pass http://plone/VirtualHostBase/http/yoursite.com:80/Plone/VirtualHostRoot/;
        }
    }

Then enable the site by creating a symbolic link::

    sudo -i
    cd /etc/nginx/sites-enabled
    ln -s ../sites-available/yoursite.conf .

Verify that your nginx configuration is valid::

    /etc/init.d/nginx configtest

    ok
    configuration file /etc/nginx/nginx.conf test is successful
    nginx.

If your system does not provide the ``configtest`` command, then you can test the configuration with::

    /usr/sbin/nginx

If the configuration is OK, then restart nginx::

    /etc/init.d/nginx restart

More info:

* https://mediatemple.net/community/products/developer/204405534/install-nginx-on-ubuntu#3

* https://www.starzel.de/blog/securing-plone-sites-with-https-and-nginx

Content Security Policy (CSP) prevents a wide range of attacks, including cross-site scripting and other cross-site injections, but
the CSP header setting may require careful tuning.
To enable it, replace the ``Content-Security-Policy-Report-Only`` by ``Content-Security-Policy``.
The example above works with Plone 4.x and up (including TinyMCE) but it is general.
You may need to adjust it if you want to make CSP more restrictive or use additional Plone Products.
For more information, see:

* https://www.w3.org/TR/CSP/


Buildout and recipe
===================

If, and only if, you cannot use a platform install of nginx, you may use the recipe and buildout example below to get started.

* http://www.martinaspeli.net/articles/an-uber-buildout-for-a-production-plone-server

* https://pypi.python.org/pypi/gocept.nginx

A buildout will download, install and configure nginx from scratch.
The buildout file contains an nginx configuration which can use template variables from ``buildout.cfg`` itself.

When you change the configuration of nginx in buildout, you probably don't want to rerun the whole buildout, but only the nginx part of it:

.. code-block:: shell

    bin/buildout -c production.cfg install balancer

Config test
===========

Assuming you have a buildout nginx section called ``balancer``:

.. code-block:: shell

    bin/balancer configtest

    Testing nginx configuration
    the configuration file /srv/plone/isleofback/parts/balancer/balancer.conf syntax is ok
    configuration file /srv/plone/isleofback/parts/balancer/balancer.conf test is successful

Deployment configuration
========================

`gocept.nginx <https://pypi.python.org/pypi/gocept.nginx/>`_ supports a special deployment configuration where you manually configure all directories.
One important reason why you might wish to do this is to change the location of the ``pid`` file.
Normally this file would be created in ``parts``, which is deleted and recreated when you re-run buildout.
This interferes with reliably restarting nginx, since the pid file may have been deleted since startup. In this case, you need to manually kill nginx to get things back on track.

Example deployment configuration in ``production.cfg``:

.. code-block:: ini

    # Define folder and file locations for nginx called "balancer"
    # If deployment= is set on gocept.nginx recipe it uses
    # data provider here
    [nginx]
    run-directory = ${buildout:directory}/var/nginx
    etc-directory = ${buildout:directory}/var/nginx
    log-directory = ${buildout:directory}/var/logs
    rc-directory = ${buildout:directory}/bin
    logrotate-directory =
    user =

    [balancer]
    recipe = gocept.nginx
    nginx = nginx-build
    deployment = nginx
    configuration =
            #user ${users:balancer};
            error_log ${buildout:directory}/var/log/balancer-error.log;
            worker_processes 1;

Install this part:

.. code-block:: shell

    bin/buildout -c production.cfg install balancer

Then you can use the following cycle to update the configuration:

.. code-block:: shell

    bin/balancer-nginx-balancer start
    # Update config in buildout
    nano production.cfg
    # This is non-destructive, because now our PID file is in var/nginx
    bin/buildout -c production.cfg install balancer
    # Looks like reload is not enough
    bin/nginx-balancer stop ; bin/nginx-balancer start


Manually killing nginx
======================

If you have lost the ``PID`` file, or the recorded ``PID`` does not match the real ``PID`` any longer, then use buildout's starter script as a search key:

.. code-block:: shell

    (hardy_i386)isleofback@isleofback:~$ bin/balancer reload
    Reloading nginx
    cat: /srv/plone/isleofback/parts/balancer/balancer.pid: No such file or directory

    (hardy_i386)isleofback@isleofback:~$ ps -Af|grep -i balancer
    1001     14012     1  0 15:26 ?        00:00:00 nginx: master process /srv/plone/isleofback/parts/nginx-build/sbin/nginx -c /srv/plone/isleofback/parts/balancer/balancer.conf
    1001     16488 16458  0 16:34 pts/2    00:00:00 grep -i balancer
    (hardy_i386)isleofback@isleofback:~$ kill 14012

    # balancer is no longer running
    (hardy_i386)isleofback@isleofback:~$ ps -Af|grep -i balancer
    1001     16496 16458  0 16:34 pts/2    00:00:00 grep -i balancer

    (hardy_i386)isleofback@isleofback:~$ bin/balancer start
    Starting nginx

    # Now it is running again
    (hardy_i386)isleofback@isleofback:~$ ps -Af|grep -i balancer
    1001     16501     1  0 16:34 ?        00:00:00 nginx: master process /srv/plone/isleofback/parts/nginx-build/sbin/nginx -c /srv/plone/isleofback/parts/balancer/balancer.conf
    1001     16504 16458  0 16:34 pts/2    00:00:00 grep -i balancer

Debugging nginx
===============

Set nginx logging to debug mode:

.. code-block:: shell

    error_log ${buildout:directory}/var/log/balancer-error.log debug;

www-redirect
============

Below is an example of how to do a basic *yourdomain.com -> www.yourdomain.com* redirect.

Put the following in your ``gocept.nginx`` configuration:

.. code-block:: nginx

    http {
        ....
        server {
                listen ${hosts:balancer}:${ports:balancer};
                server_name ${hosts:main-alias};
                return 301 $scheme://${hosts:main}$request_uri;
        }

Hosts are configured in a separate buildout section:

.. code-block:: ini

        [hosts]
        # Hostnames for servers
        main = www.yoursite.com
        main-alias = yoursite.com

More info

* https://www.nginx.com/resources/wiki/start/topics/tutorials/config_pitfalls/#taxing-rewrites

Permanent redirect
==================

Below is an example redirect rule:

.. code-block:: nginx

    # Redirect old Google front page links.
    # Redirect event to new Plone based systems.

    location /tapahtumat.php {
            rewrite ^ http://${hosts:main}/tapahtumat permanent;
    }

.. note::

    Nginx ``location match`` evaluation rules are not always top-down.
    You can add more specific matches after ``location /``.

Cleaning up query string
------------------------

By default, nginx includes all trailing ``HTTP GET`` query parameters in the redirect.
You can disable this behavior by adding a trailing ``?``:

.. code-block:: nginx

    location /tapahtumat.php {
            rewrite ^ http://${hosts:main}/no_ugly_query_string? permanent;
    }

Matching incoming query string
------------------------------

The ``location`` directive does not support query strings.  Use the ``if`` directive from the HTTP rewrite module.

Example:

.. code-block:: nginx

    location /index.php {
            # index.php?id=5
            if ($args ~ id=5) {
                    rewrite ^ http://${hosts:main}/sisalto/lomapalvelut/ruokailu? permanent;
            }
    }


More info
---------

nginx location matching rules

* http://nginx.org/en/docs/http/ngx_http_core_module.html#location

nginx rewrite module docs

* http://nginx.org/en/docs/http/ngx_http_rewrite_module.html

More info on nginx redirects

* https://scott.yang.id.au/2007/04/do-you-need-permalink-redirect.html

Make nginx aware where the request came from
============================================

If you set up nginx to run in front of Zope, and set up a virtual host with it like this:

.. code-block:: nginx

    server {
            server_name demo.webandmobile.mfabrik.com;
            location / {
                    rewrite ^/(.*)$ /VirtualHostBase/http/demo.webandmobile.mfabrik.com:80/Plone/VirtualHostRoot/$1 break;
                    proxy_pass http://127.0.0.1:8080/;
            }
    }

Zope will always get the request from ``127.0.0.1:8080`` and not from the actual host, due to the redirection.
To solve this problem, correct your configuration to be like this:

.. code-block:: nginx

    server {
            server_name demo.webandmobile.mfabrik.com;
            location / {
                    rewrite ^/(.*)$ /VirtualHostBase/http/demo.webandmobile.mfabrik.com:80/Plone/VirtualHostRoot/$1 break;
                    proxy_pass http://127.0.0.1:8080/;
                    proxy_set_header        Host            $host;
                    proxy_set_header        X-Real-IP       $remote_addr;
                    proxy_set_header        X-Forwarded-For $proxy_add_x_forwarded_for;
            }
    }


SSI: server-side include
========================

In order to include external content in a page (XDV), we must set up nginx to make these includes for us.
For including external content we will use the SSI (server-side include) method, which means that on each request nginx will get the needed external content, put it in place, and only then return the response.
Here is a configuration that sets up the filtering and turns on SSI for a specific location:

.. code-block:: nginx

    server {
            listen 80;
            server_name localhost;

            # Decide if we need to filter
            if ($args ~ "^(.*);filter_xpath=(.*)$") {
                set $newargs $1;
                set $filter_xpath $2;
                # rewrite args to avoid looping
                rewrite    ^(.*)$    /_include$1?$newargs?;
            }

            location @include500 { return 500; }
            location @include404 { return 404; }

            location ^~ /_include {
                # Restrict to subrequests
                internal;
                error_page 404 = @include404;

                # Cache in Varnish for 1h
                expires 1h;

                # Proxy
                rewrite    ^/_include(.*)$    $1    break;
                proxy_pass http://127.0.0.1:80;

                # Our safety belt.
                proxy_set_header X-Loop 1$http_X_Loop; # unary count
                proxy_set_header Accept-Encoding "";
                error_page 500 = @include500;
                if ($http_X_Loop ~ "11111") {
                    return 500;
                }

                # Filter by xpath
                xslt_stylesheet /home/ubuntu/plone/eggs/xdv-0.4b2-py2.6.egg/xdv/filter.xsl
                xpath=$filter_xpath
                ;
                xslt_html_parser on;
                xslt_types text/html;
            }


            location /forum {
                xslt_stylesheet /home/ubuntu/plone/theme/theme.xsl
                path='$uri'
                ;
                xslt_html_parser on;
                xslt_types text/html;
                # Switch on ssi here to enable external includes.
                ssi on;

                root   /home/ubuntu/phpBB3;
                index  index.php;
                try_files $uri $uri/ /index.php?q=$uri&$args;
            }
    }


Session affinity
================

If you intend to use nginx for session balancing between ZEO processes, you need to be aware of session affinity.
By default, ZEO processes don't share session data.
If you have site functionality which stores user-specific data on the server—let's say an ecommerce site shopping cart—you must always redirect users to the same ZEO client process or they will have 1/number of processes chance to see the original data.

Make sure that your :doc:`Zope session cookie </develop/plone/sessions/cookies>` are not cleared by any front-end server (nginx, Varnish).

By using IP addresses
---------------------

This is the most reliable way. nginx will balance each incoming request to a front end client by the request's source IP address.

This method is reliable as long as nginx can correctly extract the IP address from the configuration.

* http://nginx.org/en/docs/http/ngx_http_upstream_module.html#ip_hash

By using cookies
----------------

These instructions assume you are installing nginx via buildout.

* `Nginx sticky sessions module <http://nginx-sticky-module.googlecode.com/files/nginx-sticky-module-1.0-rc2.tar.gz>`_

Manually extract ``nginx-sticky-module`` under ``src``:

.. code-block:: shell

    cd src
    wget https://code.google.com/p/nginx-sticky-module/downloads/list

Then add it to the ``nginx-build`` part in buildout:

.. code-block:: ini

    [nginx-build]
    recipe = zc.recipe.cmmi
    url = http://sysoev.ru/nginx/nginx-0.7.65.tar.gz
    extra_options = --add-module=${buildout:directory}/src/nginx-sticky-module-1.0-rc2

Now test reinstalling nginx in buildout:

.. code-block:: shell

    mv parts/nginx-build/ parts/nginx-build-old # Make sure full rebuild is done
    bin/buildout install nginx-build

See that it compiles without errors. Here is the line for compiling sticky:

.. code-block:: shell

    gcc -c -O -pipe  -O -W -Wall -Wpointer-arith -Wno-unused-parameter \
        -Wunused-function -Wunused-variable -Wunused-value -Werror -g  \
        -I src/core -I src/event -I src/event/modules -I src/os/unix   \
        -I objs -I src/http -I src/http/modules -I src/mail \
        -o objs/addon/nginx-sticky-module-1.0-rc2/ngx_http_sticky_module.o

Now add ``sticky`` to the load-balancer section of the nginx configuration:

.. code-block:: ini

        [balancer]
        recipe = gocept.nginx
        nginx = nginx-build
        ...
        http {
            client_max_body_size 64M;
            upstream zope {
                sticky;
                server ${hosts:client1}:${ports:client1} max_fails=3 fail_timeout=30s;
                server ${hosts:client2}:${ports:client2} max_fails=3 fail_timeout=30s;
                server ${hosts:client3}:${ports:client3} max_fails=3 fail_timeout=30s;
            }

Reinstall nginx balancer configuration and start-up scripts:

.. code-block:: shell

    bin/buildout install balancer

Make sure that the generated configuration is ok:

.. code-block:: shell

    bin/nginx-balancer configtest

Restart nginx:

.. code-block:: shell

    bin/nginx-balancer stop ;bin/nginx-balancer start

Check that some (non-anonymous) page has the ``route`` cookie set:

.. code-block:: shell

    Huiske-iMac:tmp moo$ wget -S http://yoursite.com/sisalto/saariselka-infoa
    --2011-03-21 21:31:40--  http://yoursite.com/sisalto/saariselka-infoa
    Resolving yoursite.com (yoursite.com)... 12.12.12.12
    Connecting to yoursite.com (yoursite.com)|12.12.12.12|:80... connected.
    HTTP request sent, awaiting response...
      HTTP/1.1 200 OK
      Server: nginx/0.7.65
      Content-Type: text/html;charset=utf-8
      Set-Cookie: route=7136de9c531fcda112f24c3f32c3f52f
      Content-Language: fi
      Expires: Sat, 1 Jan 2000 00:00:00 GMT
      Set-Cookie: I18N_LANGUAGE="fi"; Path=/
      Content-Length: 41471
      Date: Mon, 21 Mar 2011 19:31:40 GMT
      X-Varnish: 1979481774
      Age: 0
      Via: 1.1 varnish
      Connection: keep-alive


Now test it by doing session-related activity and see that your shopping cart is not "lost".

More info:

* http://code.google.com/p/nginx-sticky-module/source/browse/trunk/README

* http://nathanvangheem.com/news/nginx-with-built-in-load-balancing-and-caching


Securing Plone-Sites with https and nginx
=========================================

For instructions on how to use SSL for all authenticated traffic, see this blog-post:

* https://www.starzel.de/blog/securing-plone-sites-with-https-and-nginx

Setting log files
=================

nginx.conf example:

.. code-block:: nginx

    worker_processes 2;
    error_log /srv/site/Plone/zinstance/var/log/nginx-error.log warn;

    events {
        worker_connections  256;
    }

    http {
        client_max_body_size 10M;

        access_log /srv/site/Plone/zinstance/var/log/nginx-access.log;

Proxy Caching
=============

Nginx can do rudimentary proxy caching.
It may be good enough for your needs.
Turn on proxy caching by adding to your ``nginx.conf`` or a separate ``conf.d/proxy_cache.conf``:

.. code-block:: nginx

    ##
    # common caching setup; use "proxy_cache off;" to override
    ##
    proxy_cache_path  /var/www/cache  levels=1:2 keys_zone=thecache:100m max_size=4000m inactive=1440m;
    proxy_temp_path /tmp;
    proxy_redirect                  off;
    proxy_cache                     thecache;
    proxy_set_header                Host $host;
    proxy_set_header                X-Real-IP $remote_addr;
    proxy_set_header                X-Forwarded-For $proxy_add_x_forwarded_for;
    client_max_body_size            0;
    client_body_buffer_size         128k;
    proxy_send_timeout              120;
    proxy_buffer_size               4k;
    proxy_buffers                   4 32k;
    proxy_busy_buffers_size         64k;
    proxy_temp_file_write_size      64k;
    proxy_connect_timeout           75;
    proxy_read_timeout              205;
    proxy_cache_bypass              $cookie___ac;
    proxy_http_version              1.1;
    add_header X-Cache-Status $upstream_cache_status;

Create a ``/var/www/cache`` directory owned by your nginx user (usually ``www-data``).

Limitations:

* Nginx does not support the ``vary`` header.
  That's why we use ``proxy_cache_bypass`` to turn off the cache for all authenticated users.

* Nginx does not support the ``s-maxage`` cache-control directive. Only ``max-age``.
  This means that moderate caching will do nothing. However, strong caching works and will cause all your static resources and registry items to be cached.
  Don't underestimate how valuable that is.

Enabling gzip compression
=========================

Enabling gzip compression in nginx will make your web sites respond much more quickly for your web site users and will reduce the amount of bandwidth used by your web sites.

Instructions for enabling gzip in nginx:

* https://varvy.com/pagespeed/enable-compression.html
* https://www.nginx.com/resources/admin-guide/compression-and-decompression/
