======================
Requests and traversal
======================

.. admonition:: Description

        How does Zope handle requests and translate paths to
        published objects?

.. contents :: :local:

What happens when a request is received?
========================================

A request is received either via a WSGI pipeline or the Medusa web server. Using
Medusa, it first hits ``handle_request()`` in the ``zhttp_handler`` used by
``zhttp_server``, which consumes the request until it has enough to act on.
At this point ``continue_request()`` is called. This constructs a
``ZPublisher.HTTPRequest`` from the Medusa ``http_request`` environment and
prepares a ``ZServerHTTPResponse``, a subclass of ``ZPublisher``'s
``HTTPResponse``.

The actual request is delegated to a threadpool. In a non-WSGI setup, this
is managed by ``ZServer.PubCore.ZRendezvous.ZRendevous`` (note the typo in the
module name!). This keeps track of the requests and (skeletal) responses to
be processed, and passes them to an instance of a
``ZServer.PubCore.ZServerPublisher`` for handling. ``ZRendevous`` also deals
with thread locking.

The ``ZServerPublisher`` will call either ``ZPublisher.publish_module`` or
``ZPublisher.WSGIPublisher.publish_module``, depending on the deployment mode,
with the request and the response. The non-WSGI version also takes a module
name to publish, which is ``Zope2``. This is a relic of the Bobo publisher,
which could publish other modules with a ``bobo_application`` variable set
(recall that this variable was set in the startup phase described above).

The remainder of this section will describe the non-WSGI publisher. The WSGI
publisher performs the same actions, but deals in WSGI environs and response
body iterators.

There are two versions of ``publish_module``, one with profiling and one
without. ``publish_module_standard`` (without profiling) performs the following
actions:

* Set the default ZTK skin on the request, by adapting the request to
  ``IDefaultSkin``.
* Call ``publish()``, which does the real publication.
* Handle errors.
* Write the response body to ``stdout``, which is wired up to be the HTTP
  response stream.

.. What is a "ZTK" skin?

The more interesting function is ``publish()``. This starts by calling
``get_module_info()`` to get the information about the published module
(which, recall, is almost always going to be ``Zope2``). The results are
cached, so this will only do its work once:

.. code-block:: python

    (bobo_before,
     bobo_after,
     object,
     realm,
     debug_mode,
     err_hook,
     validated_hook,
     transactions_manager) = get_module_info(module_name)

The returned variables are:

* ``bobo_before``, set via a module level variable ``__bobo_before__``. This is
  a callable that will be invoked immediately before publication.
* ``bobo_after``, set via a module level variable ``__bobo_after__``. This is a
  callable that will be invoked immediately after publication.
* ``object`` to publish, which defaults to the module itself, but can be
  set via the module-level variable ``bobo_application`` (or ``web_objects``)
* ``realm``, set via the module level variable ``__bobo_realm__``, or a global
  default which can be set the ``ZConfig`` configuration file.
* ``debug_mode``, a boolean set using the module level variable
  ``__bobo_debug_mode__``.
* ``err_hook``, set via the module level variable ``zpublisher_exception_hook``.
  This is used to handle error responses (more below).
* ``validated_hook``, set via the module level variable
  ``zpublisher_validated_hook``. This is used to initialize a security manager
  once authentication and authorization have taken place (more below).
* ``transactions_manager``, set via the module level variable
  ``zpublisher_transactions_manager``, but defaulting to the
  ``DefaultTransactionsManager`` which uses the ``transaction`` API to manage
  transactions.

The publisher then performs the following steps:

* Notify the ``ZPublisher.pubevents.PubStart`` event.
* Create a new ``zope.security`` interaction.
* Call ``processInputs()`` on the request to process request parameters and
  the request body so that the Zope request object works as advertised.
* If the request contains a key ``SUBMIT`` with the value ``cancel`` and
  a key ``cancel_action`` with a path, a ``Redirect`` exception is raised,
  which will cause an HTTP 302 redirect to be raised.
* Set ``debug_mode`` and ``realm`` on the response, as returned by
  ``get_module_info()``.
* If ``bobo_before()`` is set, it is called with no arguments.
* Set the initial value for ``request['PARENTS']`` to be the published
  object. This will be the ``ZApplicationWrapper`` set during the startup
  phase.
* Begin a transaction using the ``transactions_manager``.
* Traverse to the actual object being published (e.g. a view) by calling
  ``object=request.traverse(path, validated_hook=validated_hook)``, where
  ``path`` is ``request['PATH_INFO']``. More on traversal below.
* Notify the ``ZPublisher.pubevents.PubAfterTraversal`` event.
* Note the path and authenticated user in the transaction.
* Call the object being pusblished using ``mapply()``:

  .. code-block:: python

        result=mapply(object, request.args, request,
                      call_object,1,
                      missing_name,
                      dont_publish_class,
                      request, bind=1)

  The ``ZPublisher.mapply.mapply()`` method is somewhat complicated, but in
  essence all it does is to call either a published method, or a published
  instance with a ``__call__()`` method.

  ``request.args`` can contain positional arguments supplied in an XML-RPC call,
  but is usually empty. The ``request`` is passed to act as a dictionary of
  keyword arguments, which allows request parameters to be turned into
  method parameters to a published method.

  The other parameters are about policy |---| we call any object (e.g. a method or
  object with a ``__call__`` method) to resolve it, but we don't publish class
  objects (which would in effect instantiate them). We do allow binding of
  ``self`` for methods on objects, and we pass the ``request`` as context for
  debugging.
* Set the result of the ``mapply()`` call as the response body. As a marker,
  the response object itself can be returned from the callable that ``mapply()``
  invokes to bypass this behavior, i.e. if the published object set the
  response body itself.
* Notify the ``ZPublisher.pubevents.PubBeforeCommit`` event.
* Commit the transaction using the ``transactions_manager``.
* End the ``zope.security`` interaction.
* Notify the ``ZPublisher.pubevents.PubSuccess`` event.
* Return the response object, which is then used by the ZServer to write to
  stdout.

If an exception happens during this process, the ``err_hook`` is called. This
is allowed to raise a ``Retry`` exception. Regardless, the event
``ZPublisher.pubevents.PubBeforeAbort`` is notified before the transaction is
aborted, and then ``ZPublisher.pubevents.PubFailure`` is raised after the
``zope.security`` interaction is ended.

If the request supports retry, it will be retried by cloning it and calling
``publish`` recursively. All HTTP requests support retry, but only up to a limit
of ``retry_max_count``, which by default is 3. Retry is mainly used to retry in
the case of write-conflict errors.

If there is no error hook installed, a simple abort is encountered, with no
retry.

The default error hook is an instance of
``Zope2.startup.ZPublisherExceptionHook``. This handles exceptions by performing
the following checks:

* ``SystemExit`` or ``Redirect`` exceptions are re-raised.
* A ``ConflictError``, which indicates a write-conflict in the ZODB, is turned
  into a ``Retry`` exception so that request can be retried.
* Other exception are stored in the ``__error_log__`` acquired from the
  published object, if possible.
* If a view named ``index.html`` is registered with the exception type as its
  context, this is resolved and returned as the response.
* If the published object or any of its acquisition parents have a method
  ``raise_standardErrorMessage()``, this will be called to create an error
  message instead of using the view approach. This is called with a first
  argument of whichever object in the acquisition chain has an attribute
  ``standard_error_message``, as well as the request and traceback information.

When handling an exception by returning an error message, the
``ZPublisherExceptionHook`` will call ``response.setStatus()`` with the
exception type (class) as an argument. The *name* of the exception class is
then used to look up the status code in the ``status_reasons`` dictionary in
``ZPublisher.HTTPResponse``. Hence, raising an exception called ``NotFound``
will automatically set the response code to 404.

How does publication traversal work?
====================================

Traversal is the process during which the path elements of a URL are resolved
to an actual object to publish (there is also *path traversal*, used in TAL
expressions in page templates, which is similar, but implemented differently |---|
see below).

Traversal is invoked during object publication, which calls
``request.traverse()`` with the path from the request (the ``PATH_INFO`` CGI
variable). This method is inordinately complicated, mostly because it caters for
a lot of edge cases. The basic idea is pretty simple, though: each path element
represents an item to traverse to, from the preceding object (its parent).
Traversal can mean dictionary-like access (``__getitem__``), attribute-like access
(``__getattr__``), or one of a number of different hooks for overriding or
extending traversal. Once the final element on the path is found, the user's
access to it is validated, before it is returned to be passed to ``mapply()``.

Here are the gory details:

* Clean up the path up by stripping leading and trailing slashes, explicitly
  disallowing access to things like ``REQUEST``, ``aq_base`` and ``aq_self``,
  and resolving ``.`` or ``..`` elements as in filesystem paths.
* Check if the top-level object (the application root) has a
  ``__bobo_traverse__`` method (it almost certainly will |---| as shown above, there
  is a wrapper around the application root that implements this method to open
  and close the ZODB connection upon traversal). If so, call it to obtain a new
  top level object (which will be the real Zope application root in the ZODB).
* Aquisition-wrap the top-level object in a ``RequestContainer``. This is the
  fake root object that makes it possible to acquire the attribute ``REQUEST``
  from any traversed-to context.
* Record the request variable ``ACTUAL_URL``, which is the inbound URL plus
  the original path. Hence, this variable provides access to the URL as the
  user saw it.
* Set up (and later, pop from) the request variable
  ``TraversalRequestNameStack``. This is a stack of path elements still to be
  processed. Traversal hooks sometimes use this to look ahead at the path
  elements that have not been traversed to and, in some cases, modify the
  stack to trick traversal into going somewhere other than what the inbound
  path specified.
* In a loop, process the traversal name stack:

  * Check if the current object (initially the application root) has a method
    ``__before_publishing_traverse__``. If so, call it with the request as an
    argument. This hook is used by many parts of Zope, CMF and Plone to support
    things like content object method aliases, setting the CMF skin from the
    request, or making the ``portal_factory`` tool work. This method cannot
    easily change the traversal path, except by modifying
    ``request['TraversalRequestNameStack']``.
  * If there are more elements in the path, pop the next element.
  * Append this to the variable ``request['URL']``, which contains the traversal
    URL. Various traversal tricks may mean this is not quite the same as what
    the user sees in their address bar, but it should be a valid, traversable URL.
  * Attempt to traverse to the next object using the name popped from the path
    stack. This takes place in the ``traverseName()`` method of the request:

    * If the name starts with a ``+`` or an ``@``, parse it as a traversal
      namespace. (A name starting with an ``@`` is taken as a shorthand for
      ``++view++<name>``, i.e. an entry in the ``++view++`` traversal namespace.
      Other namespaces include ``++skin++`` and ``++etc++``.) If a traversal
      namespace is found, attempt to look up an adapter from the current
      traversal object and the request to
      ``zope.traversing.interfaces.ITraversable`` with a name matching the
      traversal namespace (e.g. ``view``). Then call its ``traverse()`` method
      with the name of the next entry on the traversal stack as an argument.
      This is expected to return an object to traverse to next. If this
      succeeds, acquisition-wrap the returned object in the parent object.

      **Note**: As this implies, objects returned from the ``traverse()``
      method of an ``ITraversable`` adapter are *not* expected to be
      acquisition-wrapped. This is in contrast to objects returned by
      ``__bobo_traverse__()``, ``__getitem__()``, ``__getattr__()``, or a
      custom ``IPublishTraverse`` adapter (see below), which *are* expected
      to be wrapped.

    * If there is no namespace traversal adapter, find an ``IPublishTraverse``
      object in one of three places:

      * If the current traversal object implements it directly, use that;
      * if there is an adapter from the current object
        and the request to ``IPublishTraverse``, use that; or,
      * fall back to the ``DefaultPublishTraverse`` implementation found in
        ``ZPublisher.BaseRequest``.

    Then call the ``publishTraverse()`` method
    to find an object to traverse to and return that (without
    acquisition-wrapping it).

    Implementing ``IPublishTraverse`` is a common way to allow further
    traversal from a view, with paths like ``.../@@foo/some/path``, where
    the ``@@foo`` view either implements or is adaptable to
    ``IPublishTraverse``.

    ``DefaultPublishTraverse`` is used in most cases, either directly or as a
    fallback from custom implementations. It works like this:

    * If the name starts with an underscore, raise a ``Forbidden`` exception
    * If the object has a ``__bobo_traverse__`` method, call it with the
      request and the name of the next entry on the traversal stack as
      arguments. It may return either an object, or a tuple of objects.
      In the latter case, amend the request parents list as if traversal had
      happened over all the elements in the tuple except the last one, and
      treat that as the next object.
    * If the ``__bobo_traverse__`` call fails by raising an
      ``AttributeError``, ``KeyError`` or ``NotFound`` exception, attempt
      to look up a view with the traversal name (which would have been given
      without the explicit ``@@`` prefix). If this succeeds, set the status
      code to 200 (the preceding failure may have set it to 404),
      acquisition-wrap the view if applicable, and return it.
    * If there was no ``__bobo_traverse__``, or if it raised the special
      exception ``ZPublisher.interfaces.UseTraversalDefault``, try the
      following:

      * Attempt to look up the name as an attribute of the current object,
        using ``aq_base`` (i.e. explicitly not acquiring from parents of
        the current object). If this succeeds, return the attribute, which
        is expected to be acquisition-wrapped if applicable (i.e. the
        parent object extends ``Acquisition.Implicit`` or
        ``Acquisition.Explicit``).
      * Next, try to look up a view using the same semantics as above
      * Next, try ``getattr()`` without the ``aq_base`` check, i.e.
        allowing acquired attributes.
      * Next, try ``__getitem__()`` (dictionary-like) access.
      * If that fails, raise a ``KeyError`` to indicate the object could
        not be found (this is later turned into a 404 response).

    * If we now have a sub-object, check that it has a docstring. If it
      does not, raise a ``Forbidden`` exception.

      The requirement for a docstring is an ancient and primitive security
      restriction, since Zope can be used to publish all kinds of Python
      objects. It is mostly a nuisance these days, but note that views and
      custom ``ITraversable`` and ``IPublishTraverse`` traversal do not have
      this restriction.
    * Next, raise a ``Forbidden`` exception if traversal resolved a
      primitive or built-in list, tuple, set or dict |---| these are not
      directly traversable.
    * Finally, return the object.
  * If a ``KeyError``, ``AttributeError`` or ``NotFound`` exception is raised
    during name resolution, return a 404 response by raising an exception.
    Similarly, if a ``Forbidden`` exception is raised, set and return a 403
    response.
  * Once the end of the path is reached, we have the most specific item
    mentioned in the (possibly mutated) path. However, this may choose to
    delegate to another object (usually a subobject) through a mechanism known
    as "browser default", which is similar to the way web servers often serve
    an ``index.html`` file by default when traversing to a folder.

    A browser publisher is described by the interface ``IBrowserPublisher``,
    which is a sub-interface of ``IPublishTraverse`` and is implemented by the
    ``DefaultPublishTraverse`` class. Again, the ``IBrowserPublisher`` for the
    traversed-to object is found in one of three ways:
    * the object may implement it itself; or
    * it may be adaptable, with the request, to this interface; or
    * the fallback ``DefaultPublishTraverse`` may be used.
    The ``browserDefault()`` method on the ``IBrowserPublisher`` is then
    called with the request as an argument.

    The return value from ``browserDefault()`` is a tuple of a parent object
    (usually the most recently traversed-to object, i.e. ``self.context`` in the
    adapter) and a tuple of further names to traverse to from this parent.

    The default implementation in ``DefaultPublishTraverse`` does this:

    * If the object has a method ``__browser_default__()``, delegate to this.
    * If an ``IDefaultViewName`` has been registered for the context in ZCML,
      look up and use this. This is deprecated, however.
    * Otherwise, return ``self.context, ()``, i.e. no further traversal
      required.

  * If a further path is returned and it has more than one element, add its
    elements to the ``TraversalRequestNameStack`` and continue traversal as if
    these elements had been part of the original path all along.
  * If there is only one element in the further path returned by
    ``browserDefault()``, use this as the next entry name and continue traversal
    to this.
  * If no further path is used, fall back on the default method name
    ``index_html()`` (applicable for HTTP ``GET`` and ``POST`` requests |---| there
    is special handling of other HTTP verbs for WebDAV that we won't go into
    here) and continue traversal to this.
  * If there is no ``index_html()`` method, use the traversed-to object itself
    as the final entry, so break out of the traversal loop. We always end up
    here eventually: if the browser default element or ``index_html()`` method
    is the last item we traverse to, eventually we reach something publishable.

    This object will most likely be called (through ``mapply()``), so we ensure
    the roles used in security checks are obtained from the ``__call__()``
    method of the traversed-to object (note: function and method objects also have
    a ``__call__()`` in Python).
* Once we have reached the end of the traversal stack (phew!), we make sure
  the ``parents`` list is in the right order (it is built in reverse order),
  even if there was a failure. Hence, ``request['PARENTS']`` is always a useful
  indicator of what objects have been traversed over, with the last item being
  the special request container and the penultimate item being the application
  root.
* We then set ``request['PUBLISHED']`` to be the published callable. Note that
  this is usually a view or page template, though for content types like
  ``File`` or ``Image`` it is the ``index_html()`` method of the content object
  itself.
* Next, we validate that the current user has sufficient permissions to call
  the published object. If not, a 403 response is returned by calling
  ``response.unauthorized()``.

  The authentication works as follows:

  * The roles required to access the traversed-to object are fetched by calling
    ``getRoles()``, first on the application root, and, if applicable, on the
    ``__call__()`` method of the traversed-to object.
  * A user folder (i.e. ``acl_users``) is obtained by looking for the special
    attribute ``__allow_groups__`` on the published object or one of its
    parents. This attribute is set by user folders on their parent container
    when they are added.
  * The ``validate()`` method of the user folder is called (there is a fallback
    called ``old_validate()``, used if there is no user folder, but that should
    never happen in a modern Zope installation). This either returns a user
    object or ``None``, if the user is not found in this user folder, or there
    is a user, but the user cannot be authorized by this user folder.
  * If ``None`` is returned, the search continues up the list of traversal
    parents until a suitable user folder is found. If no such user folder is
    found, an ``Unauthorized`` exception is raised, unless there are no security
    declarations on the context.
  * If a user with permissions is found, and the ``validated_hook`` is set
    (found via ``get_module_info()`` as described above), it is called with the
    request and user as arguments. The standard ``validated_hook`` calls
    ``newSecurityManager()`` with the user, which sets the security context for
    the remainder of the request.
  * The user is then saved in the request variable ``AUTHENTICATED_USER``. The
    true traversal path is saved in the request variable
    ``AUTHENTICATION_PATH``.

* Finally, if any post-traverse functions have been registered (by using the
  ``post_traverse()`` method of the request to register functions and optional
  static arguments), they are called in the order they were registered. If any
  post-traverse function returns a value other than ``None``, no further
  post-traverse functions are called, and the return value is used as the return
  value of the ``traverse()`` function, discarding the actual object that was
  traversed to and security checked.

How does *path* traversal work?
===============================

Path traversal is invoked when using path expressions in page templates or
action expressions (e.g. ``context/Title``). It may be invoked explicitly in
code using the methods ``restrictedTraverse()`` (which performs security checks)
or ``unrestrictedTraverse()`` (which does not), defined in
``OFS.Traversable.Traversable`` and mixed into most persistent items in Zope.
This is semantically similar to publication (URL) traversal as described above,
but is not identical |---| see below.

All the logic is in the ``unrestrictedTraverse()`` method, which takes an
optional argument ``restricted`` that is set to ``True`` when called via
``restrictedTraverse()``. It takes a ``path`` string or element list as an
argument, and optionally a default to return if traversal fails. If no default
is specified, an exception will be raised if traversal fails. This may either be
an ``AttributeError``, ``KeyError`` or ``NotFound`` exception, depending on what
type of traversal failed.

If ``restricted`` is ``True``, ``unrestrictedTraverse()`` will perform a
security check using ``getSecurityManager().validate()`` for every step of
traversal. This is different to URL traversal, which only validates at the end
of traversal.

The implementation does the following:

* Strip any trailing slash from the ``path``.
* If the path starts with a slash, begin traversal from the physical application
  root. Otherwise, start from ``self``. If performing restricted traversal from
  the application root, validate access to it.
* For each slash-separated name element of the path:

  * If the name starts with an underscore, raise a ``zExceptions.NotFound``
    exception |---| traversal to names starting with an underscore is never allowed.
  * If the name is ``..``, get the acquisition parent of the current traversal
    object and continue traversal from here after validating access if
    applicable.
  * Otherwise, if the name starts with a ``+`` or ``@``, perform traversal
    namespace lookup as described for publication traversal above. If this
    throws a ``LocationError``, fail with an ``AttributeError``. If it succeeds,
    acquisition-wrap the result if possible and validate access to it if
    applicable before continuing traversal from this object.
  * Otherwise, if the object has a ``__bobo_traverse__()`` hook, invoke it to
    get the next object to traverse to. If this succeeds, validate access to the
    result if applicable, taking into account that it could be a method or
    non-security aware object, and that it may or may not be
    acquisition-wrapped. Then continue traversal from this object.
  * If there was no ``__bobo_traverse__()``, or if it returned or raised the
    sentinel ``ZPublisher.interfaces.UseTraversalDefault``, attempt to obtain a
    non-acquired attribute of the current object with the applicable name. If
    one is found, continue traversal from this. If security checking is being
    performed, use ``guarded_getattr()`` from ``AccessControl.ZopeGuards`` to
    get the attribute, which may raise ``Unauthorized``. (This is
    the special ``getattr()`` that is also used for all attribute access by
    untrusted Python code.) Otherwise, use standard ``getattr()``.
  * Otherwise, attempt dictionary-like (``__getitem__``) access and validate the
    result if applicable before continuing traversal from this object.
  * If any of the above failed with an ``AttributeError``, ``NotFound`` or
    ``KeyError``, attempt to look up a view on the current traversal object with
    the given name. If one is found, acquisition-wrap it if possible and
    validate access if applicable, before continuing traversal from the view
    instance.
  * If there is no view, but there was a ``__bobo_traverse__``, fail by re-
    raising the original exception. The logic behind this is that if there is a
    ``__bobo_traverse__()``, we should not attempt to acquire attributes.
  * Assuming we still don't have a value and there was no
    ``__bobo_traverse__()``, attempt to acquire an attribute, using either
    ``getattr()`` or ``guarded_getattr()`` depending on whether security checks
    are being made and continue traversal from the result if this succeeds.
* If we reach the end of the path, return the most recently traversed-to object.
* If an exception of any kind (other than a ``ConflictError``) is thrown and a
  ``default`` was passed in, return this rather than letting the exception
  bubble up to the caller.

Note: This logic does *not* check for the publication/request-orientated
``IPublishTraverse`` or ``IBrowserPublisher`` hooks, although they *do* allow
traversal to a view (e.g. ``context.restrictedTraverse('@@some-view')``).

.. |---| unicode:: U+02014 .. em dash
