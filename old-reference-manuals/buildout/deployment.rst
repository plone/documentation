===========================
A deployment configuration
===========================

.. admonition:: Description

   How to use buildout for deployment configuration

Finally, let's take a look at a more advanced configuration, better
suited for deployment. Save this file as *deployment.cfg*, at the
root of the buildout next to the main *buildout.cfg* file:

::

    [buildout]
    extends =
        buildout.cfg
    
    parts +=
        debug-instance
        zeoserver
        varnish-build
        varnish-instance
    
    [zeoserver]
    recipe = plone.recipe.zope2zeoserver
    zope2-location = ${instance:zope2-location}
    zeo-address = ${instance:zeo-address}
    
    [instance]
    recipe = plone.recipe.zope2instance
    zope2-location = ${zope2:location}
    zeo-client = true
    zeo-address = 8100
    zodb-cache-size = 5000
    zeo-client-cache-size = 300MB
    debug-mode = off
    verbose-security = off
    eggs += Products.CacheSetup
    
    [debug-instance]
    recipe = collective.recipe.zope2cluster
    instance-clone = instance
    http-address = 8081
    debug-mode = on
    verbose-security = on
    
    [varnish-build]
    recipe = zc.recipe.cmmi
    url = http://downloads.sourceforge.net/varnish/varnish-2.0.2.tar.gz
    
    [varnish-instance]
    recipe = plone.recipe.varnish
    daemon = ${buildout:parts-directory}/varnish-build/sbin/varnishd
    bind = 127.0.0.1:8082
    backends = 127.0.0.1:8080
    cache-size = 1G

Here, we are:


-  Referencing the main *buildout.cfg* file, extending and
   overriding it with configuration more appropriate for deployment.
-  Setting up a ZEO server with two client instances, instance**and
   *debug-instance* (see `plone.recipe.zope2zeoserver`_ and
   `plone.recipe.zope2instance`_ for more details)
-  Compiling the Varnish cache server (see `plone.recipe.varnish`_
   for more details).

By combining buildout configuration files like this, you can create
tailor-made configurations for different deployment scenarios. To
learn more about the advanced features of buildout, see
`its documentation`_.

To build this environment, you must explicitly specify a
configuration file:

::

    $ ./bin/buildout -c deployment.cfg

To start Zope and Plone, you will need to start the ZEO server, the
instance and the Varnish server:

::

    $ ./bin/zeoserver start
    $ ./bin/instance start
    $ ./bin/varnish-instance

If you need to bring up an instance for debugging then you can
start up the *debug-instance* in foreground mode.

::

    $ ./bin/debug-instance fg

The recipes will also create scripts to back up the ZODB
filestorage (in *./bin/repozo*) and to pack the database (in
.*/bin/zeopack*).

Further options
---------------

``zc.buildout`` is a very flexible system. It is relatively easy to
create new recipes, and you can combine existing recipes in
powerful ways. Search the `Cheese Shop for "buildout"`_ to find
more recipes, or take a look at the
`source code for some of Plone's own recipes`_ to understand how
recipes are created.

 

.. _plone.recipe.zope2zeoserver: http://cheeseshop.python.org/pypi/plone.recipe.zope2zeoserver
.. _plone.recipe.zope2instance: http://cheeseshop.python.org/pypi/plone.recipe.zope2instance
.. _plone.recipe.varnish: http://cheeseshop.python.org/pypi/plone.recipe.varnish
.. _its documentation: http://cheeseshop.python.org/pypi/zc.buildout
.. _Cheese Shop for "buildout": http://cheeseshop.python.org/pypi?:action=search&term=buildout&submit=search
.. _source code for some of Plone's own recipes: http://dev.plone.org/collective/browser/buildout
