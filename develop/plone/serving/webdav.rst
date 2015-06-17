===========
 WebDAV
===========

.. admonition:: Description

    WebDAV is a protocol to manage your site directly from MS Windows
    Explorer and such.  Plone supports WebDAV without add-ons, and Plone responds to WebDAV requests out of the box.

.. contents:: :local:

Introduction
==============

WebDAV is enabled by default. A Zope server listening on port 8080 will also
accept WebDAV traffic on that port. For common cases, client-side tools
should work reasonably well.

Connecting to Plone via WebDAV
------------------------------

"OS X Mavericks: Connect to a WebDAV server": https://support.apple.com/kb/PH13859

Permissions
-----------

The "WebDAV access" permission is required for any user to be able to connect to WebDAV.

If you create new Zope users (e.g. at http://yoursite:8080/acl_users/users/manage_users) they will be able to connect to your site using WebDAV.

Enabling WebDAV on an extra port in Zope
----------------------------------------

You can have Plone listen for WebDAV requests on additional ports by modifying your buildout configuration's client setup to add a WebDAV address:

Short ``buildout.cfg`` example::

     [instance]
     ...
     recipe = plone.recipe.zope2instance
     ...
     webdav-address=1980
     ...

Alternative ``buildout.cfg`` configuration snippet which might be needed for
some WebDAV clients::

   [instance]
   ...
   zope-conf-additional =
       enable-ms-author-via on
       <webdav-source-server>
       address YOUR_SERVER_PUBLIC_IP_ADDRESS_HERE:1980
       force-connection-close off
       </webdav-source-server>

These snippets will be in the **generated** ``parts/instance/etc/zope.conf``
after buildout has been re-run.

This will enable the WebDAV server on http://www.mydomain.com:1980/. Note
that you cannot use this URL in your web browser, just in WebDAV clients.
Using the web browser will give you an error message ``AttributeError:
manage_FTPget``. You could also just run the WebDAV server on ``localhost``
with address 1980, forcing you to either use a WebDAV client locally or
proxy WebDAV through Apache.

Disabling WebDAV
----------------

You can't disable WebDAV in Plone itself; it's tightly integrated in Zope.
You could take away the "Access WebDAV" permission from everyone, but the
Zope server will still answer each request.

What you can do is make your web server filter out the WebDAV commands;
this will stop WebDAV requests before they reach your Zope server.

Nginx
~~~~~

For nginx, this is done by adding::

            dav_methods off

to the server block in your nginx.conf. (http://wiki.nginx.org/HttpDavModule)

If you do not use the HttpDavModule, you can add::

            limit_except GET POST {
              deny   all;
            }

to the location block.

Apache
~~~~~~

For Apache, you can use the ``limit`` statement, see http://httpd.apache.org/docs/current/mod/core.html#limit

See also
~~~~~~~~

"How can I stop people accessing a plone server via webdav?" http://stackoverflow.com/questions/9127269/how-can-i-stop-people-accessing-a-plone-server-via-webdav


Supporting WebDAV in your custom content
========================================

Please read more about it in the
`Dexterity WebDAV manual <https://github.com/plone/plone.dexterity/blob/master/docs/WebDAV.txt>`_.

WebDAV notes
==============

WebDAV uses a number of HTTP verbs to perform different operations. The
following notes describe how they are implemented in Zope 2 and Dexterity.

Background
----------------

Basic WebDAV support can be found in the ``webdav`` package. This defines two
base classes, ``webdav.Resource.Resource`` and
``webdav.Collection.Collection``.  ``Collection`` extends ``Resource``. These
are mixed into item and container content objects, respectively.

The webdav package also defines the ``NullResource`` object. A
``NullResource`` is a kind of placeholder, which supports the HTTP verbs ``HEAD``,
``PUT``, and ``MKCOL``.

Containers based on ``ObjectManager`` (including those in Dexterity) will
return a ``NullResource`` if they cannot find the requested object and the
request is a WebDAV request.

The ``zope.filerepresentation`` package defines a number of interfaces which
are intended to help manage file representations of content objects. Dexterity
uses these interfaces to allow the exact file read and write operations to
be overridden without subclassing.

``HEAD``
----------------

A ``HEAD`` request retrieves headers only.

``Resource.HEAD()`` sets ``Content-Type`` based on ``self.content_type()``,
``Content-Length`` based on ``self.get_size()``, ``Last-Modified`` based on
``self._p_mtime``, and an ETag based on ``self.http__etag()``, if available.

``Collection.HEAD()`` looks for ``self.index_html.HEAD()`` and returns its
value if that exists. Otherwise, it returns a ``405 Method Not Allowed`` response.
If there is no ``index_html`` object, it returns ``404 Not Found``.

``GET``
----------------

A ``GET`` request retrieves headers and body.

Zope calls ``manage_DAVget()`` to retrieve the body. The default
implementation calls ``manage_FTPget()``.

In Dexterity, ``manage_FTPget()`` adapts ``self`` to ``IRawReadFile`` and uses
its ``mimeType`` and ``encoding`` properties to set the ``Content-Type``
header, and its ``size()`` method to set ``Content-Length``.

If the ``IRawReadFile`` adapter is also an ``IStreamIterator``, it will be
returned for the publisher to consume directly. This provides for efficient
serving of large files, although it does require that the file can be read
in its entirety with the ZODB connection closed. Dexterity solves this problem
by writing the file content to a temporary file on the server.

If the ``IRawReadFile`` adapter is not a stream iterator, its contents are
returned as a string, by calling its ``read()`` method. Note that this loads
the entire file contents into memory on the server.

The default ``IRawReadFile`` implementation for Dexterity content returns an
:RFC:`2822` style message document. Most fields on the object and any enabled
behaviours will be turned into UTF-8 encoded headers. The primary field, if
any, will be returned in the body, also most likely encoded as an UTF-8
encoded string. Binary data may be base64 encoded instead.

A type which wishes to override this behaviour can provide its own adapter.
For example, an image type could return the raw image data.

``PUT``
----------------

A ``PUT`` request reads the body of a request and uses it to update a resource
that already exists, or to create a new object.

By default ``Resource.PUT()`` fails with ``405 Method Not Allowed``. That is, it
is not by default possible to ``PUT`` to a resource that already exists. The same
is true of ``Collection.PUT()``.

In Dexterity, the ``PUT()`` method is overridden to adapt self to
``zope.filerepresentation.IRawWriteFile``, and call its ``write()`` method one
or more times, writing the contents of the request body, before calling
``close()``. The ``mimeType`` and ``encoding`` properties will also be set
based on the value of the ``Content-Type`` header, if available.

The default implementation of ``IRawWriteFile`` for Dexterity objects assumes
the input is an :RFC:`2822` style message document. It will read header values
and use them to set fields on the object or in behaviours, and similarly read
the body and update the corresponding primary field.

``NullResource.PUT()`` is responsible for creating a new content object and
initialising it (recall that a ``NullResource`` may be returned if a WebDAV
request attempts to traverse to an object which does not exist). It sniffs the
content type and body from the request, and then looks for the
``PUT_factory()`` method on the parent folder.

In Dexterity, ``PUT_factory()`` is implemented to look up an ``IFileFactory``
adapter on self and use it to create the empty file. The default
implementation will use the ``content_type_registry`` tool to determine a
type name for the request (e.g. based on its extension or MIME type), and
then construct an instance of that type.

Once an instance has been constructed, the object will be initialised by
calling its ``PUT()`` method, as above.

Note that when content is created via WebDAV, an ``IObjectCreatedEvent`` will
be fired from the ``IFileFactory`` adapter, just after the object has been
constructed. At this point, none of its values will be set. Subsequently,
at the end of the ``PUT()`` method, an ``IObjectModifiedEvent`` will be fired.
This differs from the event sequence of an object created through the web.
Here, only an ``IObjectCreatedEvent`` is fired, and only *after* the object
has been fully initialised.

``DELETE``
----------------

A ``DELETE`` request instructs the WebDAV server to delete a resource.

``Resource.DELETE()`` calls ``manage_delObjects()`` on the parent folder to delete
an object.

``Collection.DELETE()`` does the same, but checks for write locks of all
children of the collection, recursively, before allowing the delete.

``PROPFIND``
----------------

A ``PROPFIND`` request returns all or a set of WebDAV properties. WebDAV
properties are metadata used to describe an object, such as the last modified
time or the author.

``Resource.PROPFIND()`` parses the request and then looks for a
``propertysheets`` attribute on self.

If an ``allprop`` request is received, it calls ``dav__allprop()``, if
available, on each property sheet. This method returns a list of name/value
pairs in the correct WebDAV XML encoding, plus a status.

If a ``propnames`` request is received, it calls ``dav__propnames()``, if
available, on each property sheet. This method returns a list of property
names in the correct WebDAV XML encoding, plus a status.

If a ``propstat`` request is received, it calls ``dav__propstats()``, if
available, on each property sheet, for each requested property. This method
returns a property name/value pair in the correct WebDAV XML encoding, plus a
status.

The ``PropertyManager`` mixin class defines the ``propertysheets`` variable to
be an instance of ``DefaultPropertySheets``. This in turn has two property
sheets, ``default``, a ``DefaultProperties`` instance, and ``webdav``, a
``DAVProperties`` instance.

The ``DefaultProperties`` instance contains the main property sheet. This
typically has a ``title`` property, for example.

``DAVProperties`` will provides various core WebDAV properties. It defines a
number of read-only properties: ``creationdate``, ``displayname``,
``resourcetype``,  ``getcontenttype``, ``getcontentlength``, ``source``,
``supportedlock``, and ``lockdiscovery``. These in turn are delegated to
methods prefixed with ``dav__``, so e.g. reading the ``creationdate`` property
calls ``dav__creationdate()`` on the property sheet instance. These methods
in turn return values based on the property manager instance (i.e. the
content object). In particular:

``creationdate``
    returns a fixed date (January 1st, 1970).
``displayname``
    returns the value of the ``title_or_id()`` method
``resourcetype``
    returns an empty string or <n:collection/>
``getlastmodified``
    returns the ZODB modification time
``getcontenttype``
    delegates to the ``content_type()`` method, falling
    back on the ``default_content_type()`` method. In Dexterity,
    ``content_type()`` is implemented to look up the ``IRawReadFile`` adapter
    on the context and return the value of its ``mimeType`` property.
``getcontentlength``
    delegates to the ``get_size()`` method (which is also
    used for the "size" column in Plone folder listings). In Dexterity,
    this looks up a ``zope.size.interfaces.ISized`` adapter on the object and
    calls ``sizeForSorting()``. If this returns a unit of ``'bytes'``, the
    value portion is used. Otherwise, a size of 0 is returned.
``source``
    returns a link to ``/document_src``, if that attribute exists
``supportedlock``
    indicates whether ``IWriteLock`` is supported by the content item
``lockdiscovery``
    returns information about any active locks

Other properties in this and any other property sheets are returned as stored
when requested.

If the ``PROPFIND`` request specifies a depth of 1 or infinity
(i.e. the client wants properties for items in a collection),
the process is repeated for all
items returned by the ``listDAVObjects()`` methods,
which by default returns
all contained items via the ``objectValues()`` method.

``PROPPATCH``
----------------

A ``PROPPATCH`` request is used to update the properties on an existing object.

``Resource.PROPPATCH()`` deals with the same types of properties from property
sheets as ``PROPFIND()``. It uses the ``PropertySheet`` API to add or update
properties as appropriate.

``MKCOL``
----------------

A ``MKCOL`` request is used to create a new collection resource, i.e. create a
new folder.

``Resource.MKCOL()`` raises 405 Method Not Allowed, because the resource
already exists (remember that in WebDAV, the ``MKCOL`` request, like a ``PUT`` for a
new resource, is sent with a location that specifies the desired new resource
location, not the location of the parent object).

``NullResource.MKCOL()`` handles the valid case where a ``MKCOL`` request has
been sent to a new resource. After checking that the resource does not already
exist, that the parent is indeed a collection (folderish item), and that the
parent is not locked, it calls the ``MKCOL_handler()`` method on the parent
folder.

In Dexterity, ``MKCOL()_handler`` is overridden to adapt self to an
``IDirectoryFactory`` from ``zope.filerepresentation`` and use this to create
a directory. The default implementation simply calls ``manage_addFolder()``
on the parent. This will create an instance of the ``Folder`` type.

``COPY``
----------------

A ``COPY`` request is used to copy a resource.

``Resource.COPY()`` implements this operation using the standard Zope content
object copy semantics.

``MOVE``
----------------

A ``MOVE`` request is used to relocate or rename a resource.

``Resource.MOVE()`` implements this operation using the standard Zope content
object move semantics.

``LOCK``
----------------

A ``LOCK`` request is used to lock a content object.

All relevant WebDAV methods in the ``webdav`` package are lock aware.
That is,
they check for locks before attempting any operation that would violate a
lock.

Also note that ``plone.locking`` uses the lock implementation from the
``webdav`` package by default.

``Resource.LOCK()`` implements locking and lock refresh support.

``NullResource.LOCK()`` implements locking on a ``NullResource``. In effect,
this means locking the name of the non-existent resource. When a
``NullResource`` is locked, it is temporarily turned into a
``LockNullResource`` object, which is a persistent object set onto the
parent (remember that a ``NullResource`` is a transient object returned
when a child object cannot be found in a WebDAV request).

``UNLOCK``
----------------

An ``UNLOCK`` request is used to unlock a locked object.

``Resource.UNLOCK()`` handles unlock requests.

``LockNullResource.UNLOCK()`` handles unlocking of a ``LockNullResource``.
This deletes the ``LockNullResource`` object from the parent container.

Fields on container objects
--------------------------------

When browsing content via WebDAV, a container object (folderish item) will
appear as a folder. Most likely, this object will also have content in the
form of schema fields. To make this accessible, Dexterity containers expose
a pseudo-file with the name '_data', by injecting this into the return value
of ``listDAVObjects()`` and adding a special traversal hook to allow its
contents to be retrieved.

This pseudo-file supports ``HEAD``, ``GET``, ``PUT``, ``LOCK``,
``UNLOCK``, ``PROPFIND`` and ``PROPPATCH`` requests
(an error will be raised if the user attempts to rename, copy, move
or delete it). These operate on the container object, obviously.
For example, when the data object is updated via a ``PUT`` request,
the ``PUT()`` method on the container is called,
by default delegating to an ``IRawWriteFile`` adapter on the container.
