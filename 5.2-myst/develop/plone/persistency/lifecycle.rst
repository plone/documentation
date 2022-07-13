===================
Object lifecycles
===================

Plone has different lifecycles for different objects

* Persistent objects: These objects are transparently persistent. They look like
  normal Python objects, but they are serialized to the disk if the transaction
  completes successfully. Persistent object inherit from Zope's
  various persistent classes: persistent.Persistent, PersistentDict, PersistentList and
  they have special attributes like _p_mtime when the object was last written to disk.
  To make object persistent, it must be referred from Zope's App traversing
  graph. Examples: content objects, user account objects.

* Request attached objects and thread-local objects: Each HTTP request is processed by
  its own Python thread. These objects disappear when the request has been processed.
  Examples: request object itself, getSite() thread-local way to access the site object,
  request specific permission caches.

* In-process objects, or "static" objects are created when the server application is launched
  and they are gone when the application quits. Usually these objects are set-up during Plone
  initialization and they are read-only for served HTTP requests. Examples:
  content type vocabulary lists.



