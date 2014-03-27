----------------------
 Diazo / XDV theming
----------------------

.. admonition:: Description

    Theming Plone and integrating external sites under one theme service
    using Diazo / XDV solution.

.. contents :: :local:

Introduction
=============

XDV is an external HTML theming engine, a.k.a. a theming proxy, which allows
you to mix and match HTML and CSS from internal and external sites
by using simple XML rules. It separates the theme development from the site development,
so that people with little HTML and CSS knowledge can create themes
without the need to know the underlying Python, PHP or whatever. It also enables
integration of different services and sites to one unified user experience.
For example, XDV is used by `plone.org <http://plone.org>`_ to integrate
the Plone CMS and the Trac issue tracker.

XDV compiles theming rules to XSL templates, which has been a standard
XML based template language since 1999. XSL has good support
in every programming language and web server out there.

Example backends to perform XDV transformation include:

* collective.xdv (as a normal Plone add-on, a post-process hook)

* Apache's mod_transform

* Nginx web server transform module

XDV theming can be used together with Plone, where enhanced support is provided
by the `collective.xdv package <http://pypi.python.org/pypi/collective.xdv>`_.
Technically, collective.xdv adds a Plone settings panel and does the XSL transformation in Zope's
post-publication hook using lxml library.

XDV can be used standalone with the `XDV package <http://pypi.python.org/pypi/xdv/0.3a2>`_ to theme any web site,
let it be Wordpress, Joomla, Drupal or a custom in-house PHP solution from year 2000.

XDV is based on the `Deliverance specification <http://deliverance.openplans.org/>`_
The difference between XDV and the Deliverance reference implementation
is that XDV internally compiles themes to XSL templates, whereas Deliverance relies
on processing HTML in Python. Currently the XDV approach seems to be
working better, as we had many problems trying to apply Deliverance
for Wordpress sites (redirects didn't work, HTTP posts didn't work, etc.).

Theming editing interface (backend)
-------------------------------------

The editing interface, backend, or admin site, however you wish to call it,
can be themed with collective.xdv. However, it does not need to be
and the edit interface can fallback to the default Plone theme.

There are several reasons for this:

* The Plone editing interface is powerful and has very high
  usability, which means that it is internally quite complex
  (it takes complex things to seem simple to the end user).

* The public theme you are building would not fit to the
  editing interface very well. E.g. no space for portlets.
  This is especially problematic if an external
  artist has created the visuals without properly
  fitting them for Plone.

With XDV you can easily have a separate admin.yoursite.com
where the Plone editing interface is untouched.

Tutorials
===========

* http://reinout.vanrees.org/weblog/2010/12/29/xdv-setup.html

* http://plone.org/products/collective.xdv/documentation/reference-manual/theming

* http://pypi.python.org/pypi/collective.xdv

* http://pypi.python.org/pypi/xdv

* http://pypi.python.org/pypi/dv.xdvserver (with WSGI)

Creating your first XDV project
==================================

The :doc:`ZopeSkel package </develop/addons/paste>` includes an XDV theme skeleton
since version 2.20.

Example how to boostrap your theme.




Setting up XDV development tools
=================================

XDV tools are deployed as Python eggs.
You can use tools like the `buildout <http://www.buildout.org/>`_
configuration and assembly tool or easy_install
to get XDV on your development computer and the server.

If you are working with Plone you can integrate XDV to your
existing site's buildout. If you are not working with Plone, the
`XDV home page <http://pypi.python.org/pypi/xdv#installation>`_ has instructions
on how to deploy the XDV command standalone.

XDV Rules
===========

Rules (rules.xml) will tell how to fit content from external source to
your theme HTML.

It provides a straightforward XML based syntax to manipulate HTML easily:

* Append, replace and drop HTML pieces

* Insert HTML snippets

* CSS or XPath selectors can be used to identify HTML parts

* It is possible to mix and match content from more than two sites

* etc.

The rules XML syntax is documented at `XDV homepage <http://pypi.python.org/pypi/xdv>`_.

Rules will be compiled to an XSL template (theme.xsl) by the *xdvcompiler* command.
The actual theming is done by one of the XSL backends listed above,
by taking HTML as input and applying XSL transformations on it.

Note that currently rules without matching selectors are silently ignored
and there is no bullet-proof way to debug what happens inside
XSL transformation, except by looking into the compiled theme.xsl.

Dropping specific CSS files with XDV
=====================================

For example if you wish to get rid of the base-cachekey????.css file that comes from
a Plone site, but still want to keep the authoring CSS and any special CSS
files that come from add-ons, you can use the following rule::

    <drop content="/html/head[style *=
    'portal_css/Plone%20Default/base-cachekey']/style" />

More info

* http://www.coactivate.org/projects/deliverance/lists/deliverance-discussion/archive/2010/09/1284795659190

Handling .. relative URLs
===========================

Here is an example of :doc:`monkey-patch </develop/plone/misc/monkeypatch>`
which you can use to override relative URLs in your theme using
a dot notation.

It adds a custom behavior to normal ``urlparse.urljoin()`` logic.

.. code-block:: python

        from xdv import rules

        from urlparse import urljoin

        def apply_absolute_prefix(theme_doc, absolute_prefix):

            def join(prefix, url):
                """ Handle relative URLs specially.

                Theme files may contain .. URLs referring to other file locations on the file system.
                Since transformation is not file system location aware, we need to manually fix these
                kind references. This join assumes that all URLs with .. go to the absolute prefix root.

                This behavior might depend on the context of the theme files, so we can't have
                bullet-proof solution here but these must be solved case-by-case basis.
                """
                if url.startswith("../"):
                    url = url[3:]

                final = urljoin(prefix, url)

                return final

            if not absolute_prefix:
                return
            if not absolute_prefix.endswith('/'):
                absolute_prefix = absolute_prefix + '/'
            for node in theme_doc.xpath('//*[@src]'):
                url = join(absolute_prefix, node.get('src'))
                node.set('src', url)
            for node in theme_doc.xpath('//*[@href]'):
                url = join(absolute_prefix, node.get('href'))
                node.set('href', url)
            for node in theme_doc.xpath('//comment() | //style'):
                if node.tag == 'style' or node.tag == etree.Comment and node.text.startswith("[if IE"):
                    node.text = IMPORT_STYLESHEET.sub(
                        lambda match: match.group(1) + join(absolute_prefix, match.group(2)) + match.group(3),
                        node.text)

        # Monkey-patch XDV to support relative URL handling
        rules.apply_absolute_prefix = apply_absolute_prefix


Using XDV to theme and integrate a Wordpress site
==================================================

Below are instructions for how to integrate a Wordpress site to your CMS.
In this example the CMS is Plone, but it could be any other system.

We will create an XDV theme which will theme a Wordpress site
to match our CMS site on the fly.

The Wordpress theme is built with XDV, using a live Plone web page
as a theme template.

This way the Wordpress theme inherits "live data"
from the Plone site, like top tabs (portal sections), footer, CSS and
other stuff which can be changed on-the-fly and reflecting
such changes to two separate theming products would be cumbersome.

Benefits of using Wordpress for blogging instead of the main CMS:

* Wordpress post and comment management is easy

* Wordpress does not need to be touched:
  the old public Wordpress instance can keep
  happily running wherever it is during the whole process

* You do not need to migrate legacy Wordpress installations
  to your CMS's internal blogging tool

* Wordpress comes with extensive blog spam filtering tools.
  We get 11000 spam comments a month.

* Wordpress is designed for blogging and the user interface is
  good for that

* Wordpress integrates well with blog pingback support services

* Wordpress supports Gravatars and other blogging plug-ins

* ..and so on...

Benefits of using XDV theming instead of creating a native Wordpress theme are

* You need to maintain only one theming add-on product
  i.e. the one for your main CMS and Wordpress
  receives the updates to this site and the theme automatically

* Wordpress does not need to be touched

* You can host your Wordpress on a different server,
  even wordpress.com, and still integrate it to your main CMS

* The theme can be recycled not only for Wordpress, but also
  other external services: Bugzilla, Trac, Webmail, phpBB,
  you-name-it

* Even though Wordpress has a slick UI, it is a well known fact that
  it is a can of worms internally.
  My developers do not like the idea of PHP development and would
  spit on my face if I ask them to go develop a Wordpress
  theme for us

Theme elements
------------------

The theme will consist of the following pieces

* Deliverance rules XML file which defines how to combine Plone and Wordpress HTML
  (rules.xml)

* Additional CSS definitions active only for Wordpress (wordpress.css).
  Dependency on this CSS in injected in the <head> by rules XML

* Special Plone page template which will provide slots where Wordpress can drop in the content
  (wordpress_listing.pt)

* A helper script which makes it easy to perform repeatable
  theming actions, like recompiling the theme
  (xdv.py)

CMS page template
^^^^^^^^^^^^^^^^^^

This explains how to create a Plone page template where Wordpress
content will be dropped in. This step is not necessary,
as we could do this without touching Plone. However, it
makes things more straightforward and explicit when we known
that the Wordpress theme uses a certain template and we explicitly define slots
for Wordpress content there.

Example::

        <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
              xmlns:tal="http://xml.zope.org/namespaces/tal"
              xmlns:metal="http://xml.zope.org/namespaces/metal"
              xmlns:i18n="http://xml.zope.org/namespaces/i18n"
              lang="en"
              metal:use-macro="here/main_template/macros/master"
              i18n:domain="plone">


        <body>

            <div metal:fill-slot="content">

                <div id="wordpress-content">
                        <!-- Your Wordpress "left column" will go here -->
                </div>

            </div>

        </body>
        </html>

Theming rules
^^^^^^^^^^^^^^^^^^^^^^

Following are the XDV rules (rules.xml) for how we will fit the Wordpress site to the Plone frame.

It will integrate

* Content from Wordpress

* Metadata from Wordpress

* CSS from Plone

* Page basic structrure from Plone

rules.xml::

        <?xml version="1.0" encoding="UTF-8"?>
        <rules xmlns="http://namespaces.plone.org/xdv"
               xmlns:xsl="http://www.w3.org/1999/XSL/Transform"
               xmlns:css="http://namespaces.plone.org/xdv+css">

            <!-- Remove Wordpress CSS by filtering out <style> tags-->
            <drop css:content="style" />

            <!-- Make sure that Wordpress metadata is present in <head> section -->
            <append css:content="head link" css:theme="head" />

            <!-- note: replace does not seem to handle multiple meta tags very well -->
            <drop css:theme="meta" />
            <append css:content="head meta" css:theme="head" />

            <!-- Use blog title instead of Plone page title -->
            <replace css:content="title" css:theme="title" />

            <!-- Put Wordpress sidebar in Plone's portlets section -->
            <append css:content="#r_sidebar" css:theme="#portal-column-one .visualPadding" />

            <!-- Place wordpress content into our theme content area -->
            <copy css:content="#contentleft" css:theme="#wordpress-content" />

            <!-- This mixes in Wordpress specific CSS sheet which is applied for pages
                 served from Wordpress only and does not concern Plone CMS.
                 This stylesheet will theme Wordpress specific tags,
                 like blog posts and comment fields.
                 We keep this file in Plone, but this could be served from elsewhere. -->
            <append css:theme="head">
                <style type="text/css">
                   @import url(http://mfabrik.com/++resource++plonetheme.mfabrik/wordpress.css);
                </style>
            </append>

            <!-- This stylesheet is used by special spam protection plug-in NoSpamNX -->
            <append css:theme="head">
                <link rel="stylesheet" href="http://blog.mfabrik.com/wp-content/plugins/nospamnx/nospamnx.css" type="text/css" />
            </append>

            <!-- Remove Google Analytics script used for CMS site -->
            <drop css:theme="#page-bottom script" />

            <!-- Rebuild our Google Analytics code, using a different tracker id this time
                 which is a specific to our blog.
              -->
            <append css:theme="#page-bottom">

                <script type="text/javascript">
                        var gaJsHost = (("https:" == document.location.protocol) ? "https://ssl." : "http://www.");
                        document.write(unescape("%3Cscript src='" + gaJsHost + "google-analytics.com/ga.js' type='text/javascript'%3E%3C/script%3E"));
                </script>

                <script type="text/javascript">
                        try {
                               var pageTracker = _gat._getTracker("UA-8819100-2");
                               pageTracker._trackPageview();
                        } catch(err) {
                        }
                </script>
            </append>

        </rules>

Wordpress specific CSS
^^^^^^^^^^^^^^^^^^^^^^

This CSS has styles which are applied only to Wordpress pages.
They are mainly corner case fixes where Wordpress and CMS styles
must match.

The CSS file is loaded when rules.xml injects it into the <head> section.

wordpress.css::

        /* Font and block style fixes */

        #wordpress-content h1 {
                border: 0;
        }

        #wordpress-content .post-end {
                margin-bottom: 60px;
        }

        #wordpress-content pre {
                width: 600px;
                overflow: auto;
                background: white;
                border: 1px solid #888;
        }

        #wordpress-content ul {
                margin-left: 20px;
        }


        #wordpress-content .post-info-date,
        #wordpress-content .post-info-categories,
        #wordpress-content .post-info-tags {
                font-size: 80%;
                color: #888;
        }

        /* Make sure that posts and comments look sane in our theme */

        #wordpress-content .post {
                margin-top: 15px;
        }

        #wordpress-content .commentlist li {
                margin: 20px;
                background: white;
                padding: 10px;
        }

        #wordpress-content .commentlist li img {
                float: left;
                margin-right: 20px;
                margin-bottom: 20px;
        }

        #wordpress-content #commentform {
                margin: 20px;
        }

        #wordpress-content {
                margin-left: 20px;
                margin-right: 20px;
        }

        /* Make Wordpress "sidebaar" look like Plone "portlets */

        .template-wordpress_listing #portal-column-one ul {
                list-style: none;
                margin-bottom: 40px;
        }

        .template-wordpress_listing #portal-column-one ul#Recent li {
                margin-bottom: 8px;
        }

        .template-wordpress_listing #portal-column-one ul#Categories a {
                line-height: 120%;
        }


        .template-wordpress_listing #portal-column-one h2 {
                background: transparent;
                border: 0;
                font-weight:normal;
                line-height:1.6em;
                padding:0;
                text-transform:none;
                font-size: 16px;
                color: #9b9b9b;
                border-bottom:4px solid #CDCDCD;
        }

Helper script
^^^^^^^^^^^^^^

The following Python script (xdv.py) makes it easy for us to:

* Recompile the theme

* Test the theme applied on the site

* Preview the theme in our browser

It is basically wrapped with default file locations around the
 *bin/xdvcompiler* and *bin/xdvrun* commands with some
 webbrowser opening magic.

Drop the file into your Plone theme package and modify it to fit your needs.

xdv.py::

         """

         This command line Python script compiles your rules.xml to XDV XSL

         Modify it for your own needs.

         It assumes your buildout.cfg has an xdv section and generates XDV
         commands under bin/

         To compile, execute in the buildout folder::

             python src/plonetheme.mfabrik/xdv.py

         To build test HTML::

             python src/plonetheme.mfabrik/xdv.py --test


         To build test HTML and preview it in a browser, execute in buildout folder::

             python src/plonetheme.mfabrik/xdv.py --preview

         If you want to use alternative development theme source::

             python src/plonetheme.mfabrik/xdv.py --preview --development

        """

        import getopt, sys
        import os
        import webbrowser

        # rules XML for theming
        RULES_XML = "src/plonetheme.mfabrik/deliverance/etc/rules.xml"

        # Which XSL file to generate for compiled XDV
        OUTPUT_FILE = "theme.xsl"

        # Which file to generate applied theme test runs
        TEST_HTML_FILE = "test.html"

        # Our "theme.html" is a remote template served for each request.
        # Because we are doing live integration, this is a HTTP resource,
        # not a local file.
        THEME="http://mfabrik.com/news/wordpress_listing/"

        # Alternative theme location - used for development
        DEVELOPMENT_THEME="http://localhost:8080/mfabrik/news/wordpress_listing/"

        #
        # External site you are theming.
        # Note: must have ending slash (lxm cannot handle redirects)
        #
        SITE="http://blog.twinapex.fi/"

        # We need to explicitly
        INTEGRATED_SITE_URL="http://blog.mfabrik.com"

        try:
            opts, args = getopt.getopt(sys.argv[1:], "ptd", ["preview", "test", "development"])
        except getopt.GetoptError, err:
            # print help information and exit:
            print str(err) # will print something like "option -a not recognized"

        # Convert options to simple list
        opts = [ opt for opt, value in opts ]

        if "-d" in opts or "--development" in opts:
            THEME = DEVELOPMENT_THEME
            print "Using development theme source:" + THEME
        else:
            print "Using production theme source:" + THEME

        print "Compiling transformation"
        value = os.system("bin/xdvcompiler -o " + OUTPUT_FILE + " " + RULES_XML +" " + THEME)
        if value != 0:
            print "Compilation failed"
            sys.exit(1)


        if "-p" in opts or "--preview" in opts or "-t" in opts or "--test" in opts:
              print "Generating test HTML page"
              value = os.system("bin/xdvrun -o " + TEST_HTML_FILE + " " + OUTPUT_FILE + " " + SITE)
              if value != 0:
                  print "Page transformation failed"
                  sys.exit(1)

        if "-p" in opts or "--preview" in opts:
            # Preview the result in a browser
            # NOTE: OSX needs Python >= 2.5 to make this work

            # Make sure test run succeeded
            url = "file://" + os.path.abspath(TEST_HTML_FILE)
            print "Opening:" + url

            # We prefer Firefox for preview for its superior
            # Firebug HTML debugger and XPath rule generator
            try:
                browser = webbrowser.get("firefox")
            except webbrowser.Error:
                # No FF on the system, or OSX which can't find its browsers
                browser = webbrowser.get()

            browser.open_new_tab(url)

Compiling the theme
----------------------

This will generate XSL templates to do the theming transform.
It will compile the rules XML with some boilerplate XSL.

Running our compile script::

        python src/plonetheme.mfabrik/xdv.py

Since Plone usually does not use any relative paths or relative resources in HTML,
we do not give the parameter "Absolute prefix" to the compilation stage.
In Plone, everything is mapped through a virtual hosting aware resource
locator: portal_url and VirtualHostMonster.

For more information see

* http://pypi.python.org/pypi/xdv/0.3a2#compilation

Testing the theme
-------------------

The following command will apply the theme to an example external page::

        bin/xdvrun -o theme.html theme.xsl http://blog.twinapex.fi
        firefox theme.xhtml

... or we can use the shortcut provided by our script ... ::

        python src/plonetheme.mfabrik/xdv.py --preview

... alternatively we can specify that the theme source should be fetched from the
development server (localhost)::

        python src/plonetheme.mfabrik/xdv.py --preview --development

Applying the theme in an Apache production environment
------------------------------------------------------

These steps tell how to apply the integration
theme for Wordpress when Wordpress is running under an
Apache virtualhost.

Installing dependencies
^^^^^^^^^^^^^^^^^^^^^^^

We use Apache and mod_transform.
`Instructions on how to set up modules for Apache <http://pypi.python.org/pypi/xdv#apache>`_
are available on the XDV homepage. Some hand-built modules must be used,
instructions to set them up for Ubuntu / Debian are available.

Apache 2 supports `filter chains <http://httpd.apache.org/docs/2.2/mod/mod_filter.html>`_ which allow you to
perform magic on the HTTP response before sending it out.
This corresponds to Python's WSGI middleware.

We will use special builds of mod_transform and mod_depends
which are known to work. These modules were forked from their
orignal creations to make them XDV compatible, as the orignal
has not been updated since 2004 (this is a good example of how
the freedom of open source guarantees that you "won't run out of support")

* `XDV mod_transform and mod_depends homepage <http://code.google.com/p/html-xslt/>`_

* `Orignal mod_transform and mod_depends homepage <http://www.outoforder.cc/projects/apache/mod_transform/>`_

Example::

        sudo -i
        apt-get install libxslt1-dev libapache2-mod-apreq2 libapreq2-dev apache2-threaded-dev
        wget http://html-xslt.googlecode.com/files/mod-transform-html-xslt.tgz
        wget http://html-xslt.googlecode.com/files/mod-depends-html-xslt.tgz
        tar -xzf mod-transform-html-xslt.tgz
        tar -xzf mod-depends-html-xslt.tgz
        cd mod-depends-html-xslt ; ./configure ; make ; make install ; cd ..
        cd mod-transform-html-xslt ; ./configure ; make ; make install ; cd ..

Enable built-in Apache modules::

        a2enmod filter
        a2enmod ext_filter

For modules *depends* and *transform* you need to manually add
them to the end of Apache configuration, as they do not
provide a2enmod stubs for Debian. Edit /etc/apache2/apache.conf::

        LoadModule depends_module /usr/lib/apache2/modules/mod_depends.so
        LoadModule transform_module /usr/lib/apache2/modules/mod_transform.so

You need to hard reset Apache to make the new modules effective::

        /etc/init.d/apache2 force-reload

Virtual host configuration
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Standard Configuration
=========================
The example below shows a typical xdv setup
::

        <VirtualHost *:80>
        ServerName www.yourserver.com

        FilterDeclare THEME
        FilterProvider THEME XSLT resp=Content-Type $text/html

        TransformOptions ApacheFS HTML HideParseErrors
        TransformSet /theme.xsl
        TransformCache /theme.xsl /home/plone/path/to/your/theme.xsl


        <LocationMatch "/">
            FilterChain THEME
        </LocationMatch>


        <Proxy *>
                    Order deny,allow
                    Allow from all
        </Proxy>

        ProxyVia on
        RewriteEngine On
        RewriteRule ^/static(.*) /path/to/your/theme/static/$1 [L]
        RewriteRule ^/(.*) http://localhost:8080/VirtualHostBase/http/%{HTTP_HOST}:80/Plone/VirtualHostRoot/$1 [L,P]

        </VirtualHost>

Integrating with Wordpress
=============================
Below is our virtualhost configuration which runs Wordpress and PHP.
Transformation filter chain has been added in.

/etc/apache/sites-enabled/blog.mfabrik.com::

        <VirtualHost *>

            ServerName blog.mfabrik.com
            ServerAdmin info@mfabrik.com

            LogFormat       combined
            TransferLog     /var/log/apache2/blog.mfabrik.com.log

            # Basic Wordpress setup

            Options +Indexes FollowSymLinks +ExecCGI

            DocumentRoot /srv/www/wordpress

            <Directory /srv/www/wordpress>
                Options FollowSymlinks
                AllowOverride All
            </Directory>

            AddType application/x-httpd-php .php .php3 .php4 .php5
            AddType application/x-httpd-php-source .phps

            # Theming set-up

            # This chain is used for public web pages
            FilterDeclare THEME
            FilterProvider THEME XSLT resp=Content-Type $text/html

            TransformOptions +ApacheFS +HTML +HideParseErrors
            # This is the location of compiled XSL theme transform
            TransformSet /theme.xsl

            # This will make Apache not to reload transformation every time
            # it is performed. Instead, a compiled version is hold in the
            # virtual URL declared above.
            TransformCache /theme.xsl /srv/plone/twinapex.fi/theme.xsl

            # We want to apply theme only for
            # 1. public pages (otherwise Wordpress administrative interface stops working)
            <Location "/">
                FilterChain THEME
            </Location>

            # 2. Admin interface and feeds should not receive any kind of theming
            <LocationMatch "(wp-login|wp-admin|wp-includes|xmlrpc|plugins|feed|rss|uploads)">
                # The following resets the filter chain
                # http://httpd.apache.org/docs/2.2/mod/mod_filter.html#filterchain
                FilterChain !
            </LocationMatch>

        </VirtualHost>

Running it
----------

After Apache has all modules enabled and your virtualhost configuration is ok,
you should see Wordpress through your new theme by visiting the site
served through Apache:

* http://blog.mfabrik.com

Automatically reflecting CMS changes back to XDV theme
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The theme should be recompiled every time

* Plone is restarted: CSS references change in <head> as CSS cache is rebuilt

* CSS is modified: CSS references change in <head> as CSS cache is rebuilt

* Plone content is changed and changes reflect back to Wordpress theme
  (e.g. a new top level site section is being added)

This is because the compilation will hard-link resources and template
snippets to the resulting theme.xsl file. If hard-linked resources change
on the Plone site, the transformation XSL file does not automatically
reflect back the changes.

It could be possible to use Plone events automatically to rerun theme
compilation when concerned resources change. However,
this would be quite complex.  For now, we are satisfied with a scheduled task
which will recompile the theme now and then.

Alternatively, mod_transforms could be run in non-cached mode with
some performance implications.

Here is a shell script, update-wordpress-theme.sh,
which will perform the recompilation
and make Apache's transformation cache aware of changes::

        #!/bin/sh
        #
        # Periodically update Wordpress theme to reflect changes on CMS site
        #

        # Recompile theme
        sudo -H -u twinapex /bin/sh -c cd /srv/plone/twinapex.fi ; python src/plonetheme.mfabrik/xdv.py

        # Make Apache aware of theme changes
        sudo apache2ctl restart

Then we call it periodically in cron job, every 15 minutes
in /etc/cron.d/update-wordpress::

        # Make Wordpress XDV theme to reflect changes on CMS
        0,15,30,45 * * * * /srv/plone/twinapex.fi/update-wordpress-theme.sh


.. warning ::

        It looks like Varnish has issues with Apache2 apache2ctl graceful
        restart. Do only hard restarts when using Apache in conjunction
        with Varnish.

Updating Wordpress settings
----------------------------

No changes on Wordpress needed if the domain name is not changed in the theme
transformation process.

Site URL
^^^^^^^^

Unlike Plone, Wordpress does not have decent virtual hosting machinery.
It knowns only one URL which it uses to refer to the site in the external context
(e.g. RSS feeds).

This setting can be overridden in

* Wordpress administrative interface

* wp-config.php

Here is an example how we override this in our wp-config.php::

        // http://codex.wordpress.org/Editing_wp-config.php#WordPress_address_.28URL.29
        define('WP_HOME','http://blog.mfabrik.com');
        define('WP_SITEURL','http://blog.mfabrik.com');

HTTP 404 Not Found special case
--------------------------------

Http 404 Not Found responses are not themed by the Apache filter chain. This
is not possible due to the order of the pipeline in Apache.

As a workaround you can set up a custom HTTP 404 page in
Wordpress which does not expose the old theme.

* Go to Wordpress admin interface, Theme editor

* Edit 404.php and modify it so that it does not pull in the Wordpress theme::

        <html>
        <head>
        <title>Not found</title>
        </head>
        <body>

                <h1>Not Found, Error 404</h1>
                <p>Aaaaw, snap! The page you are looking for no longer exists. It must be our hamster who ate it.</p>

                <a href="<?php bloginfo('url'); ?>">Go to blog homepage</a>

                <a href="http://mfabrik.com">mFabrik business site</a>
        </body>
        </html>

For more information see

* http://codex.wordpress.org/Creating_an_Error_404_Page

Roll-out checklist
--------------------

Below is a checklist you need to go to through to confirm
that the theme integration works on your production site

* Wordpress public pages are loaded with the new theme

* Wordpress login works

* Wordpress administrative interface works

* RSS feed from Wordpress works and contains correct URLs

* HTTP 404 not found is handled correctly

* HTTP 302 redirect is handled correctly (i.e. missing / at the end of blog post URL)

* Changes on CMS site are reflected to Wordpress theme within the update delay

* Old blog site is redirected to new site using HTTP 301 (if applicable)



Using XDV to theme and integrate a phpBB forum
==================================================

What we want to achieve is to have a regular Plone site for
the CMS pages, and a mix of Plone and phpBB for the forum part.
By mix, I mean combination of elements from the two products.
The header and menu will come from Plone, and the body will be
from phpBB. This mixing will be done with XDV.

First thought that came to mind was to use collective.xdv which
has a nice control panel page that holds all the configuration
stuff needed for XDV, and it does all the magic for me and I
don’t need to think about configuration or compiling on each change.
This is a very nice thing when the Plone site is the main site and
only some elements are needed to be dropped in from another
location. As usual, we need the opposite of this: the phpBB site
needs to be the main one, and drop in some minor content from the
Plone site. This means that we can’t use the magic of collective.xdv,
but we must set up everything by hand.

A detailed tutorial on how to make this happen can be found here:

* http://alasdoo.com/2010/12/xdv-plone-and-phpbb-under-one-nginx-roof/
