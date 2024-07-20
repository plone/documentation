---
myst:
  html_meta:
    "description": "How to add support for WebDAV, and accessing and modifying a content object using file-like operations in Plone"
    "property=og:description": "How to add support for WebDAV, and accessing and modifying a content object using file-like operations in Plone"
    "property=og:title": "How to add support for WebDAV, and accessing and modifying a content object using file-like operations in Plone"
    "keywords": "Plone, content types, WebDAV, file representations"
---

# WebDAV and other file representations

```{todo}
This chapter may have obsolete content.
It needs a content expert to review for accuracy for Plone 6.
```

This chapter describes how to add support for WebDAV, and accessing and modifying a content object using file-like operations.

Zope supports WebDAV, a protocol that allows content objects to be viewed, modified, copied, renamed, moved, and deleted as if they were files on the filesystem.
WebDAV is also used to support saving to remote locations from various desktop programs.

```{todo}
The following feature existed up until Plone 5.2.
There is an [open issue to restore this feature for Plone 6](https://github.com/plone/Products.CMFPlone/issues/3190).

> In addition, WebDAV powers the [External Editor] product, which allows users to launch a desktop program from within Plone to edit a content object.
```

To configure a WebDAV server, you can add the following option to the `[instance]` section of your `buildout.cfg` and re-run buildout.

```ini
webdav-address = 9800
```

See the documentation for [`plone.recipe.zope2instance`](https://pypi.org/project/plone.recipe.zope2instance/) for details.
When Zope is started, you should now be able to mount it as a WebDAV server on the given port.

Most operating systems support mounting WebDAV servers as folders.
Unfortunately, not all WebDAV implementations are very good.
Dexterity content should work with Windows Web Folders [^id2] and well-behaved clients.

[^id2]: open Internet Explorer, go to {guilabel}`File | Open`, type in a WebDAV address, e.g.  <http://localhost:9800>, and then select {guilabel}`Open as web folder` before hitting {guilabel}`OK`.

On macOS, the Finder claims to support WebDAV, but the implementation is so flaky that it is just as likely to crash macOS as it is to let you browse files and folders.
Use a dedicated WebDAV client instead, such as [Cyberduck](https://cyberduck.io/).


## Default WebDAV behavior

By default, Dexterity content can be downloaded and uploaded using a text format based on {RFC}`2822`, the same standard used to encode email messages.
Most fields are encoded in headers, whilst the field marked as "primary" will be contained in the body of the message.
If there is more than one primary field, a multi-part message is created.

A field can be marked as "primary" using the `primary()` directive from [plone.supermodel](https://pypi.org/project/plone.supermodel/), as shown in the following example.

```python
from plone.autoform import directives as form
from plone.supermodel import directives

class ISession(model.Schema):
    """A conference session. Sessions are managed inside Programs.
    """

    title = schema.TextLine(
            title=_("Title"),
            description=_("Session title"),
        )

    description = schema.Text(
            title=_("Session summary"),
        )

    directives.primary("details")
    details = RichText(
            title=_("Session details"),
            required=False
        )

    form.widget(presenter=AutocompleteFieldWidget)
    presenter = RelationChoice(
            title=_("Presenter"),
            source=ObjPathSourceBinder(object_provides=IPresenter.__identifier__),
            required=False,
        )

    form.write_permission(track="example.conference.ModifyTrack")
    track = schema.Choice(
            title=_("Track"),
            source=possibleTracks,
            required=False,
        )
```

This will actually apply the `IPrimaryField` marker interface from the [`plone.rfc822`](https://pypi.org/project/plone.rfc822/) package to the given fields.

By default a WebDAV download of this content item will look like the following.

```text
title: Test session
description: First session
presenter: 713399904
track: Administrators
MIME-Version: 1.0
Content-Type: text/html; charset="utf-8"
Portal-Type: example.conference.session

<p>Details <b>here</b></p>
```

Notice how most fields are encoded as header strings.
The `presenter` relation field stores a number, which is the integer ID of the target object.
Note that this ID is generated when the content object is created, and so is unlikely to be valid on a different site.
The `details` field, which we marked as primary, is encoded in the body of the message.

It is also possible to upload such a file to create a new session.
To do that, the `content_type_registry` tool needs to be configured with a predicate that can detect the type of content from the uploaded file and instantiate the correct type of object.
Such predicates could be based on an extension or a filename pattern.
Below, we will see a different approach that uses a custom "file factory" for the containing `Program` type.


### Containers

Container objects will be shown as *collections* (WebDAV-speak for folders) for WebDAV purposes.
This allows the WebDAV client to open the container and list its contents.
However, representing containers as collections makes it impossible to access the data contained in the various fields of the content object.

To allow access to this information, a pseudo-file called `_data` will be exposed inside a Dexterity container.
This file can be read and written like any other, to access or modify the container's data.
It cannot be copied, moved, renamed, or deleted.
Those operations should be performed on the container itself.


## Customizing WebDAV behavior

There are several ways in which you can influence the WebDAV behavior of your type.

-   If you are happy with the {RFC}`2822` format, you can provide your own `plone.rfc822.interfaces.IFieldMarshaler` adapters to provide alternate serializations and parsers for fields.
    See the [`plone.rfc822`](http://pypi.python.org/pypi/plone.rfc822) documentation for details.
-   If you want to use a different file representation, you can provide your own `IRawReadFile` and `IRawWriteFile` adapters.
    For example, if you have a content object that stores binary data, you could return this data directly, with an appropriate MIME type, to allow it to be edited in a desktop program, such as an image editor if the MIME type is `image/jpeg`.
    The file {file}`plone.dexterity.filerepresentation.py` contains two base classes, `ReadFileBase` and `WriteFileBase`, which you may be able to use to make it easier to implement these interfaces.
-   If you want to control how content objects are created when a new file or directory is dropped into a particular type of container, you can provide your own `IFileFactory` or `IDirectoryFactory` adapters.
    See [plone.dexterity.filerepresentation](https://github.com/plone/plone.dexterity/blob/master/plone/dexterity/filerepresentation.py) for the default implementations.

As an example, let's register a custom `IFileFactory` adapter for the `IProgram` type.
This adapter will not rely on the `content_type_registry` tool to determine which type to construct, but will instead create a `Session` object, since that is the only type that is allowed inside a `Program` container.

The code, in {file}`program.py`, is the following.

```python
from zope.component import adapter
from zope.component import createObject
from zope.interface import implementer
from zope.event import notify
from zope.lifecycleevent import ObjectCreatedEvent
from zope.filerepresentation.interfaces import IFileFactory

@implementer(IFileFactory)
@adapter(IProgram)
class ProgramFileFactory(object):
    """Custom file factory for programs, which always creates a Session.
    """

    def __init__(self, context)
        self.context = context

    def __call__(self, name, contentType, data):
        session = createObject('example.conference.session', id=name)
        notify(ObjectCreatedEvent(session))
        return session
```

We need to register the adapter in {file}`configure.zcml`.

```xml
<adapter factory=".program.ProgramFileFactory" />
```

This adapter overrides the `DefaultFileFactory` found in `plone.dexterity.filerepresentation`.
It creates an object of the designated type, fires an `IObjectModifiedEvent` and then returns the object, which will then be populated with data from the uploaded file.

To test this, you could write a text file like the one shown above in a text editor and save it on your desktop, then drag it into the folder in your WebDAV client representing a `Program`.

The following is an automated integration test for the same component.

```python
def test_file_factory(self):
    self.folder.invokeFactory("example.conference.program", "p1")
    p1 = self.folder["p1"]
    fileFactory = IFileFactory(p1)
    newObject = fileFactory("new-session", "text/plain", "dummy")
    self.assertTrue(ISession.providedBy(newObject))
```


## How it all works

The rest of this section describes in some detail how the various WebDAV related components interact in Zope 2, CMF, and Dexterity.
This may be helpful if you are trying to customize or debug WebDAV behavior.


### Background

Basic WebDAV support can be found in the `webdav` package.
This defines two base classes, `webdav.Resource.Resource` and `webdav.Collection.Collection`.
`Collection` extends `Resource`.
These are mixed into *item* and *container* content objects, respectively.

The `webdav` package also defines the `NullResource` object.
A `NullResource` is a kind of placeholder, which supports the HTTP verbs `HEAD`, `PUT`, and `MKCOL`.

Contents based on `ObjectManager` (including those in Dexterity) will return a `NullResource` if they cannot find the requested object and the request is a WebDAV request.

The [`zope.filerepresentation`](https://pypi.org/project/zope.filerepresentation/) package defines a number of interfaces which are intended to help manage file representations of content objects.
Dexterity uses these interfaces to allow the exact file read and write operations to be overridden without subclassing.


### `HEAD`

A `HEAD` request retrieves headers only.

`Resource.HEAD()` sets `Content-Type` based on `self.content_type()`, `Content-Length` based on `self.get_size()`, `Last-Modified` based on `self._p_mtime`, and an `ETag` based on `self.http__etag()`, if available.

`Collection.HEAD()` looks for `self.index_html.HEAD()` and returns its value if that exists.
Otherwise, it returns a "405 Method Not Allowed" response.
If there is no `index_html` object, it returns "404 Not Found".


### `GET`

A `GET` request retrieves headers and body.

Zope calls `manage_DAVget()` to retrieve the body.
The default implementation calls `manage_FTPget()`.

In Dexterity, `manage_FTPget()` adapts `self` to `IRawReadFile` and uses its `mimeType` and `encoding` properties to set the `Content-Type` header, and its `size()` method to set `Content-Length`.

If the `IRawReadFile` adapter is also an `IStreamIterator`, it will be returned for the publisher to consume directly.
This provides for efficient serving of large files, although it does require that the file can be read in its entirety with the ZODB connection closed.
Dexterity solves this problem by writing the file content to a temporary file on the server.

If the `IRawReadFile` adapter is not a stream iterator, its contents are returned as a string, by calling its `read()` method.
Note that this loads the entire file contents into memory on the server.

The default `IRawReadFile` implementation for Dexterity content returns an {RFC}`2822`-style message document.
Most fields on the object and any enabled behaviors will be turned into UTF-8 encoded headers.
The primary field, if any, will be returned in the body, also most likely encoded as a UTF-8 encoded string.
Binary data may be base64-encoded instead.

A type which wishes to override this behavior can provide its own adapter.
For example, an image type could return the raw image data.


### `PUT`

A `PUT` request reads the body of a request and uses it to update a resource that already exists, or to create a new object.

By default `Resource.PUT()` fails with "405 Method Not Allowed".
That is, it is not by default possible to `PUT` to a resource that already exists.
The same is true of `Collection.PUT()`.

In Dexterity, the `PUT()` method is overridden to adapt `self` to `zope.filerepresentation.IRawWriteFile`, and call its `write()` method one or more times, writing the contents of the request body, before calling `close()`.
The `mimeType` and `encoding` properties will also be set based on the value of the `Content-Type` header, if available.

The default implementation of `IRawWriteFile` for Dexterity objects assumes the input is an RFC 2822 style message document.
It will read header values and use them to set fields on the object or in behaviors, and similarly read the body and update the corresponding primary field.

`NullResource.PUT()` is responsible for creating a new content object and initializing it (recall that a `NullResource` may be returned if a WebDAV request attempts to traverse to an object which does not exist).
It sniffs the content type and body from the request, and then looks for the `PUT_factory()` method on the parent folder.

In Dexterity, `PUT_factory()` is implemented to look up an `IFileFactory` adapter on `self`, and use it to create the empty file.
The default implementation will use the `content_type_registry` tool to determine a type name for the request (for example, based on its extension or MIME type), and then construct an instance of that type.

Once an instance has been constructed, the object will be initialized by calling its `PUT()` method, as above.

Note that when content is created via WebDAV, an `IObjectCreatedEvent` will be fired from the `IFileFactory` adapter, just after the object has been constructed.
At this point, none of its values will be set.
Subsequently, at the end of the `PUT()` method, an `IObjectModifiedEvent` will be fired.
This differs from the event sequence of an object created through the web.
Here, only an `IObjectCreatedEvent` is fired, and only *after* the object has been fully initialized.


### `DELETE`

A `DELETE` request instructs the WebDAV server to delete a resource.

`Resource.DELETE()` calls `manage_delObjects()` on the parent folder to delete an object.

`Collection.DELETE()` does the same, but checks for write locks of all children of the collection, recursively, before allowing the delete.


### `PROPFIND`

A `PROPFIND` request returns all or a set of WebDAV properties.
WebDAV properties are metadata used to describe an object, such as the last modified time or the author.

`Resource.PROPFIND()` parses the request and then looks for a `propertysheets` attribute on `self`.

If an `allprop` request is received, it calls `dav__allprop()`, if available, on each property sheet.
This method returns a list of name/value pairs in the correct WebDAV XML encoding, plus a status.

If a `propnames` request is received, it calls `dav__propnames()`, if available, on each property sheet.
This method returns a list of property names in the correct WebDAV XML encoding, plus a status.

If a `propstat` request is received, it calls `dav__propstats()`, if available, on each property sheet, for each requested property.
This method returns a property name/value pair in the correct WebDAV XML encoding, plus a status.

The `PropertyManager` mixin class defines the `propertysheets` variable to be an instance of `DefaultPropertySheets`.
This in turn has two property sheets:

-   `default`, a `DefaultProperties` instance.
-   `webdav`, a `DAVProperties` instance.

The `DefaultProperties` instance contains the main property sheet.
This typically has a `title` property, for example.

`DAVProperties` will provides various core WebDAV properties.
It defines a number of read-only properties: `creationdate`, `displayname`,
`resourcetype`, `getcontenttype`, `getcontentlength`, `source`,
`supportedlock`, and `lockdiscovery`.
These in turn are delegated to methods prefixed with `dav__`.
For example, reading the `creationdate` property calls `dav__creationdate()` on the
property sheet instance.
These methods in turn return values based on the property manager instance, in other words, the content object, as explained below.

`creationdate`
:   returns a fixed date (January 1st, 1970).

`displayname`
:   Returns the value of the `title_or_id()` method.

`resourcetype`
:   Returns an empty string or `<n:collection/>`.

`getlastmodified`
:   Returns the ZODB modification time.

`getcontenttype`
:   Delegates to the `content_type()` method, falling back on the `default_content_type()` method.
    In Dexterity, `content_type()` is implemented to look up the `IRawReadFile` adapter on the context and return the value of its `mimeType` property.

`getcontentlength`
:   Delegates to the `get_size()` method (which is also used for the `size` column in Plone folder listings).
    In Dexterity, this looks up a `zope.size.interfaces.ISized` adapter on the object and calls `sizeForSorting()`.
    If this returns a unit of `'bytes'`, the value portion is used.
    Otherwise, a size of `0` is returned.

`source`
:   Returns a link to `/document_src`, if that attribute exists.

`supportedlock`
:   Indicates whether `IWriteLock` is supported by the content item.

`lockdiscovery`
:   Returns information about any active locks.

Other properties in this and any other property sheets are returned as stored when requested.

If the `PROPFIND` request specifies a depth of `1` or `infinity` (in other words, the client wants properties for items in a collection), the process is repeated for all items returned by the `listDAVObjects()` methods, which by default returns all contained items via the `objectValues()` method.


### `PROPPATCH`

A `PROPPATCH` request is used to update the properties on an existing object.

`Resource.PROPPATCH()` deals with the same types of properties from property sheets as `PROPFIND()`.
It uses the `PropertySheet` API to add or update properties as appropriate.


### `MKCOL`

A `MKCOL` request is used to create a new collection resource, in other words, create a new folder.

`Resource.MKCOL()` raises "405 Method Not Allowed", because the resource already exists
(remember that in WebDAV, the `MKCOL` request, like a `PUT` for a new resource, is sent with a location that specifies the desired new resource location, not the location of the parent object).

`NullResource.MKCOL()` handles the valid case where a `MKCOL` request has been sent to a new resource.
After checking that the resource does not already exist, that the parent is indeed a collection (folderish item), and that the parent is not locked, it calls the `MKCOL_handler()` method on the parent folder.

In Dexterity, the `MKCOL()_handler` is overridden to adapt `self` to an
`IDirectoryFactory` from `zope.filerepresentation` and use this to create a directory.
The default implementation calls `manage_addFolder()` on the parent.
This will create an instance of the `Folder` type.


### `COPY`

A `COPY` request is used to copy a resource.

`Resource.COPY()` implements this operation using the standard Zope content object copy semantics.


### `MOVE`

A `MOVE` request is used to relocate or rename a resource.

`Resource.MOVE()` implements this operation using the standard Zope content-object move semantics.


### `LOCK`

A `LOCK` request is used to lock a content object.

All relevant WebDAV methods in the `webdav` package are lock aware.
That is, they check for locks before attempting any operation that would violate a lock.

Also note that [`plone.locking`](https://pypi.org/project/plone.locking/) uses the lock implementation from the `webdav` package by default.

`Resource.LOCK()` implements locking and lock refresh support.

`NullResource.LOCK()` implements locking on a `NullResource`.
In effect, this means locking the name of the non-existent resource.
When a `NullResource` is locked, it is temporarily turned into a `LockNullResource` object, which is a persistent object set onto the parent (remember that a `NullResource` is a transient object returned when a child object cannot be found in a WebDAV request).


### `UNLOCK`

An `UNLOCK` request is used to unlock a locked object.

`Resource.UNLOCK()` handles unlock requests.

`LockNullResource.UNLOCK()` handles unlocking of a `LockNullResource`.
This deletes the `LockNullResource` object from the parent container.


### Fields on container objects

When browsing content via WebDAV, a container object (folderish item) will appear as a folder.
Most likely, this object will also have content in the form of schema fields.
To make this accessible, Dexterity containers expose a pseudo-file with the name `_data`, by injecting this into the return value of `listDAVObjects()` and adding a special traversal hook to allow its contents to be retrieved.

This file supports `HEAD`, `GET`, `PUT`, `LOCK`, `UNLOCK`, `PROPFIND`, and `PROPPATCH` requests.
An error will be raised if the user attempts to rename, copy, move, or delete it.
These operate on the container object, obviously.
For example, when the data object is updated via a PUT request, the `PUT()` method on the container is called, by default delegating to an `IRawWriteFile` adapter on the container.
