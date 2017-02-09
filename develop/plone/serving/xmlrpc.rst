=======
XML-RPC
=======


.. admonition:: Description

        Using XML-RPC remote call protocol to manipulate Plone site.

Introduction
------------

Zope provides transparent XML-RPC support for any traversable object.

Example::

       # URL to the object
       target = 'http://localhost:8080/plone'

       # Call remote method
       path = xmlrpclib.ServerProxy(target).getPhysicalPath()

.. warning::

        Zope object handles are not transferable across function call boundaries.
        Thus, you can only call functions with primitive arguments. If you
        need to call function with object arguments you need to create
        server side helper code first.

For more information see

* transmogrifier.ploneremote

Authentication
---------------

The simplest way to authenticate the user for XML-RPC calls
is to embed HTTP Basic Auth data to URL::

       # URL to the object
       target = 'http://admin:admin@localhost:8080/plone'

       # Call remote method
       path = xmlrpclib.ServerProxy(target).getPhysicalPath()


ZPublisher client
------------------------------------------------------

XML-RPC does not marshal objects reliable between remote calls.
Getting the real remote object can be done with ZPublisher.Client.Object.

.. note::

        This approach works only for Python clients and
        needs Zope libraries available at the client side.

.. warning::

        Zope object handles are not transferable across function call boundaries.
        Thus, you can only call functions with primitive arguments. If you
        need to call function with object arguments you need to create
        server side helper code first.

* http://svn.zope.org/Zope/tags/ajung-final-zpt-integration-before-merge-savepoint/utilities/load_site.py?rev=67269&view=auto

* http://maurits.vanrees.org/weblog/archive/2009/10/lighting-talks-friday#id2


Web Services API for Plone (wsapi4plone)
----------------------------------------

This is an add-on product exposes more methods available through Zope's
XML-RPC api.

*  https://plone.org/products/wsapi4plone.core

Importing an Image Using WSAPI
==============================

In the following example we retrieve, from the 'Pictures' folder, an image called 'red-wine-glass.jpg',
post it to a folder called 'ministries' and give it the name 'theimage'.

::

    import os
    from xmlrpclib import ServerProxy
    from xmlrpclib import Binary

    client = ServerProxy("http://username:password@localhost:8080/path/to/plone")

    data = open(os.path.join('Pictures', 'red-wine-glass.jpg')).read()

    myimage = {'ministries/theimage': [{'title': 'a beautiful wine glass', 'image':Binary(data)},'Image']}


    output = client.get_object(client.post_object(myimage))

For more information see `wsapi4plone.core <https://plone.org/products/wsapi4plone.core/>`_ add-on product adds XML-RPC operations
support for Plone.




More information
----------------

* http://www.zope.org/Members/Amos/XML-RPC
