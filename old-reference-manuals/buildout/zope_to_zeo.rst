============================================================================
Converting single process Zope instance to ZEO cluster buildout.cfg
============================================================================

.. contents:: :local:

Introduction
------------

See `ZEO <http://plone.org/documentation/manual/installing-plone/installing-on-linux-unix-bsd/to-zeo-or-not-to-zeo>`_.

See the `plone.app.blob product page <http://plone.org/products/plone.app.blob>`_
for good ZEO configuration examples.

Steps
-----

Use link above for a ``buildout.cfg`` example.

Changes needed to a single process ``buildout.cfg``:

* Add ``[zeo]`` section:

  .. code-block:: ini

     [zeo]
     recipe = plone.recipe.zope2zeoserver
     zope2-location = ${zope2:location}
     zeo-address = 127.0.0.1:8100
     zeo-var = ${buildout:directory}/var
     blob-storage = ${zeo:zeo-var}/blobstorage
     eggs = plone.app.blob

* Convert ``[instance]`` to ``[client1]``. Add the following new settings:

  .. code-block:: ini

     zeo-client = on
     zeo-address =  ${zeo:zeo-address}
     # If blobs are used
     shared-blob = on

* Add ``[client2]`` ... ``[clientN]`` sections:

  .. code-block:: ini

     [client2]
     recipe = plone.recipe.zope2instance
     http-address = 8081
     zope2-location = ${client1:zope2-location}
     zeo-client = ${client1:zeo-client}
     zeo-address = ${client1:zeo-address}
     blob-storage = ${client1:blob-storage}
     shared-blob = ${client1:shared-blob}
     user = ${client1:user}
     products = ${client1:products}
     eggs = ${client1:eggs}
     zcml = ${client1:zcml}


* Reconfigure ``[buildout]`` parts to include zeo, client1, client2...

  .. code-block:: ini

     [buildout]
     parts =
         plone
         zope2
         zeo
         client1
         client2
     # instance     ... instance is no longer required when running ZEO based instance

* Change all ``${instance:...}`` references to ``${client1:...}``. Search and replace ``${instance:`` -> ``${client1:``


Starting ZEO cluster
--------------------

You need to start ZEO and clients independently

* bin/zeo start

* bin/client1 start

* bin/client2 start

* etc.

Other resources
---------------

* http://blog.twinapex.fi/2008/07/07/zope-zeo-setupconversion-and-zeo-vs-standalone-performance-review/
