===========
 Traversing
===========

.. admonition:: Description

    Plone content is organized as a tree. Traversing means looking up
    content from this tree by path. When HTTP request hits a Plone
    server, Plone will traverse the corresponding content item
    and its view function by URI.


Introduction
============

In Plone, all content is mapped to a single tree: content objects, user
objects, templates, etc.  Even most object methods are directly mapped to
HTTP-accessible URIs.

Each object has a path depending on its location. :term:`Traversal` is a
method of getting a handle on a persistent object in the ZODB object graph
from its path.

Traversal can happen in two places:

* When an HTTP request hits the server, the method on the object which will
  generate the HTTP response is looked up using traversal.

* You can manually traverse the ZODB tree in your code to locate objects by
  their path.

When an HTTP request is being published the traversing happens in
``ZPublisher.BaseRequest.traverse``

* https://github.com/zopefoundation/Zope/blob/master/src/ZPublisher/BaseRequest.py

... but Zope includes other traversers, like ``unrestrictedTraverse()`` in
the OFS module.  Different traversing methods behave differently and may
fire different events.

Object ids
==========

Each content object has an id string which identifies the object in the
parent container.  The id string is visible in the browser address bar when
you view the object.  Ids are also visible in the Management Interface.

Besides id strings, the content objects have Unique Identifiers, or UID_,
which do not change even if the object is moved or renamed.

Though it's technically possible for ids to contain spaces or slashes, this
is seldom a good idea, as it complicates working with ids in various
situations.

Path
----

The Zope *path* is the location of the object in the object graph.
It is a sequence of id components from the parent node(s) to the child
separated by slashes.

.. Note:: A path need not always be a sequence of object ids. During
   traversal, an object may consume subsequent path elements, interpreting
   them however it likes.

Example::

    documentation/howTos/myHowTo

Exploring Zope application server
=================================

You can use the Management Interface to explore the content of your
Zope application server:

* Sites

* Folders within the sites

* ...and so on

The Management Interface does not expose individual attributes.
It only exposes traversable content objects.

Attribute traversing
====================

Zope exposes child objects as attributes.

Example::

    # you have obtained the plone.org portal root object somehow and it's
    # stored in local variable "portal"

    documentation = portal.documentation
    howTos = getattr(portal, "how-to") # note that we need use getattr because dash is invalid in syntax
    myHowTo = getattr(howTos, "manipulating-plone-objects-programmatically")

Container traversing
====================

Zope exposes child objects as container accessor.

Example::

    # you have obtained the plone.org portal root object somehow and it's
    # stored in a local variable "portal"

    documentation = portal["documentation"]
    howTos = documentation["how-to"]
    myHowTo = howTos["manipulating-plone-objects-programmatically"]


Traversing by full path
=======================

Any content object provides the methods ``restrictedTraverse()`` and
``unrestrictedTraverse()``.  See Traversable_.

**Security warning**: ``restrictedTraverse()`` executes with the privileges
of the currently logged-in user.  An Unauthorized_ exception is raised if
the code tries to access an object for which the user lacks the *Access
contents information* and *View* permissions.

Example::

    myHowTo = portal.restrictedTraverse("documentation/howTos/myHowTo")

    # Bypass security
    myHowTo = portal.unrestrictedTraverse("documentation/howTos/myHowTo")

.. warning::

    ``restrictedTraverse()``/``unrestrictedTraverse()`` does not honor
    ``IPublishTraverse`` adapters. `Read more about the issue in this
    discussion
    <http://mail.zope.org/pipermail/zope-dev/2009-May/036665.html>`_.

Getting the object path
=========================

An object has two paths:

- The *physical path* is the absolute location in the current ZODB object
  graph. This includes the site instance name as part of it.

- The *virtual path* is the object location relative to the Plone site root.

**Path mangling warning**: Always store paths as virtual paths, or
persistently stored paths will corrupt if you rename your site instance.

See Traversable_.

Getting physical path
---------------------

Use ``getPhysicalPath()``. Example::

    path = portal.getPhysicalPath() # returns "plone"

Getting virtual path
--------------------

For content items you can use ``absolute_url_path()`` from `OFS.Traversable
<http://svn.zope.org/Zope/trunk/src/OFS/Traversable.py?rev=122638&view=auto>`_::

    path = context.absolute_url_path()

Map physical path to virtual path using HTTP request object
``physicalPathToVirtualPath()``. Example::

    request = self.request # HTTPRequest object

    path = portal.document.getPhysicalPath()

    virtual_path = request.physicalPathToVirtualPath(path) # returns "document"

.. note::

    The virtual path is not necessarily the path relative to the site root,
    depending on the virtual host configuration.

Getting item path relative to the site root
---------------------------------------------

There is no a direct, easy way to accomplish this.

Example::

    from zope.component import getMultiAdapter

    def getSiteRootRelativePath(context, request):
        """ Get site root relative path to an item

        @param context: Content item which path is resolved

        @param request: HTTP request object

        @return: Path to the context object, relative to site root, prefixed with a slash.
        """

        portal_state = getMultiAdapter((context, request), name=u'plone_portal_state')
        site = portal_state.portal()

        # Both of these are tuples
        site_path = site.getPhysicalPath();
        context_path = context.getPhysicalPath()

        relative_path = context_path[len(site_path):]

        return "/" + "/".join(relative_path)


Getting canonical object (breadcrumbs, visual path)
----------------------------------------------------

The visual path is presented in the breadcrumbs. It is how the site visitor
sees the object path.

It may differ from the physical path:

* The *default content item* is not shown in the visual path.
* The *default view* is not shown in the visual path.

The canonical object is the context object which the user sees from the
request URL:

Example::

    context_helper = getMultiAdapter((context, self.request), name="plone_context_state")
    canonical = context_helper.canonical_object()


Getting object URL
==================

Use ``absolute_url()``. See Traversable_.

**URL mangling warning**: ``absolute_url()`` is sensitive to virtual host
URL mappings. ``absolute_url()`` will return different results depending on
if you access your site from URLs http://yourhost/ or
http://yourhost:8080/Plone.  Do not persistently store the result of
``absolute_url()``.

Example::

    url = portal.absolute_url() # http://nohost/plone in unit tests

Getting the parent
==================

The object *parent* is accessible is acquisition_ chain for the object is
set.

Use ``aq_parent``::

    parent = object.aq_parent

The parent is defined as ``__parent__`` attribute of the object instance::

    object.__parent__ = object.aq_parent

``__parent__`` is set when object's ``__of__()`` method is called::

    view = MyBrowserView(context, request)
    view = view.__of__(context) # Inserts view into acquisition chain and acquisition functions become available

Getting all parents
-------------------

Example::

    def getAcquisitionChain(object):
        """
        @return: List of objects from context, its parents to the portal root

        Example::

            chain = getAcquisitionChain(self.context)
            print "I will look up objects:" + str(list(chain))

        @param object: Any content object
        @return: Iterable of all parents from the direct parent to the site root
        """

        # It is important to use inner to bootstrap the traverse,
        # or otherwise we might get surprising parents
        # E.g. the context of the view has the view as the parent
        # unless inner is used
        inner = object.aq_inner

        iter = inner

        while iter is not None:
            yield iter

            if ISiteRoot.providedBy(iter):
               break

            if not hasattr(iter, "aq_parent"):
                raise RuntimeError("Parent traversing interrupted by object: " + str(parent))

            iter = iter.aq_parent

Getting the site root
=====================

You can resolve the site root if you have the handle to any context object.

Using portal_url tool
-----------------------

Example::

    from Products.CMFCore.utils import getToolByName

    # you know some object which is referred as "context"
    portal_url = getToolByName(context, "portal_url")
    portal = portal_url.getPortalObject()

You can also do shortcut using acquisition::

    portal = context.portal_url.getPortalObject()

.. note:: Application code should use the ``getToolByName`` method, rather
   than simply acquiring the tool by name, to ease forward migration (e.g.,
   to Zope3).

Using ``getSite()``
--------------------

Site is also stored as a thread-local variable. In Zope each request is
processed in its own thread. Site thread local is set when the request
processing starts.

You can use this method even if you do not have the context object
available, assuming that your code is called after Zope has traversed the
context object once.

Example::

    from zope.component.hooks import getSite

    site = getSite() # returns portal root from thread local storage

.. note:: Before Plone 4.3 getSite resided in zope.app.component.hooks. See
   https://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-4.2-to-4.3/referencemanual-all-pages

.. note:: Due to the fact that Plone does not show the default content item
   as a separate object, the page you are viewing in the browser from the
   site root URL is not necessary the root item itself. For example, in the
   default Plone installation this URL internally maps to Page whose id is
   ``front-page`` and you can still query the actual parent object which is
   the site root.

   If you need to traverse using user visible breadcrumbs, see how
   breadcrumbs viewlet code does it.

Traversing back to the site root
-----------------------------------

Sometimes ``getSite()`` or ``portal_url`` are not available, but you still
have the acquisition chain intact. In these cases you can simply traverse
parent objects back to the site root by iterating over the aquisition-chain or using the ``aq_parent`` accessor::

    from Products.CMFCore.interfaces import ISiteRoot

    def getSite(context):

        if not ISiteRoot.providedBy(context):
            return context
        else:
            for item in context.aq_chain:
                if ISiteRoot.providedBy(item):
                    return item

Checking for the site root
---------------------------

You can check if the current context object is Plone the site root::

    from Products.CMFCore.interfaces import ISiteRoot

    if ISiteRoot.providedBy(context):
        # Special case
    else:
        # Subfolder or on a page

Navigation root
----------------

In Plone, the Plone site root is not necessarily the navigation root (one
site can contain many navigation trees for example for the nested subsites).

The navigation root check has the same mechanism as the site root check::

    from plone.app.layout.navigation.interfaces import INavigationRoot

    if INavigationRoot.providedBy(context):
        # Top level, no up navigation
    else:
        # Up navigation and breadcrumbs

More info

* https://plone.org/products/plone/roadmap/234

Getting Zope application server handle
======================================

You can also access other sites within the same application server from your
code.

Example::

    app = context.restrictedTraverse('/') # Zope application server root
    site = app["plone"] # your plone instance
    site2 = app["mysiteid"] # another site

Acquisition effect
==================

Sometimes traversal can give you attributes which actually do not exist on
the object, but are inherited from the parent objects in the persistent
object graph. See :term:`acquisition`.

Default content item
====================

Default content item or view sets some challenges for the traversing, as the
object published path and internal path differ.

Below is an example to get the folder of the published object (parent folder
for the default item) in page templates:

.. code-block:: html

    <div tal:define="folder context/@@plone_context_state/canonical_object"
         tal:condition="python:hasattr(folder, 'carousel') and
                               hasattr(folder['carousel'],
                               'carouselText')">xxx</div>



Checking if an item is the site front page
--------------------------------------------

Example:

.. code:: python

    from zope.component import getMultiAdapter

    def is_front_page(self):
        """Check if we are in the context of a front page."""
        context_helper = getMultiAdapter((self.context, self.request), name='plone_context_state')
        return context_helper.is_portal_root()


Custom traversal
=================

There exist many ways to make your objects traversable:

* ``__getitem__()`` which makes your objects act like Python dictionary.
  This is the simplest method and recommended.

*  ``IPublishTraverse`` interface. There is an example below and works for
   making nice urls and path munging.

* ``ITraversable`` interface. You can create your own traversing hooks.
  ``zope.traversing.interfaces.ITraversable``
  provides an interface traversable objects must provider. You need to
  register ``ITraversable`` as adapter for your content types.  This is only
  for publishing methods for HTTP requests.

* ``__bobo_traverse__()`` which is an archaic method from the early 2000s.

.. warning:: Zope traversal is a minefield. There are different traversers.
   One is the *ZPublisher traverser* which does HTTP request looks.  One is
   ``OFS.Traversable.unrestrictedTraverse()`` which is used when you call
   traverse from Python code. Then another case is
   ``zope.tales.expression.PathExpr`` which uses a really simple traverser.

.. warning:: If an ``AttributeError`` is risen inside a ``traverse()``
   function bad things happen, as Zope publisher specially handles this and
   raises a ``NotFound`` exception which will mask the actual problem.

Example using ``__getitem__()``::

    class Viewlets(BrowserView):
        """ Expose arbitrary viewlets to traversing by name.
        Exposes viewlets to templates by names.
        Example how to render plone.logo viewlet in arbitrary template
        code point::

            <div tal:content="context/@@viewlets/plone.logo" />

        """

        ...

        def __getitem__(self, name):
            """
            Allow travering intoviewlets by viewlet name.

            @return: Viewlet HTML output

            @raise: ViewletNotFoundException if viewlet is not found
            """
            viewlet = self.setupViewletByName(name)
            if viewlet is None:
                active_layers = [ str(x) for x in self.request.__provides__.__iro__ ]
                active_layers = tuple(active_layers)
                raise ViewletNotFoundException("Viewlet does not exist by"
                    "name %s for the active theme layer set %s."
                    "Probably theme interface not registered in "
                    "plone.browserlayers. Try reinstalling the theme."
                    % (name, str(active_layers)))

            viewlet.update()
            return viewlet.render()


Example using ``IPublishTraverse``::

    from Products.Five.browser import BrowserView
    from zope.publisher.interfaces import IPublishTraverse
    from zope.interface import implementer
    from zope.component import getMultiAdapter
    from AccessControl import getSecurityManager
    from AccessControl import Unauthorized
    from plone import api

    @implementer(IPublishTraverse)
    class MyUser(BrowserView):
        """Registered as a browser view at '/user', collect the username and
        view name from the url, check security, and display that page. For
        example, '/user/jjohns/log' will look up the log view for user
        'jjohns'
        """
        path = []

        def publishTraverse(self, request, name):
            # stop traversing, we have arrived
            request['TraversalRequestNameStack'] = []
            # return self so the publisher calls this view
        	return self


        def __init__(self, context, request):
            """Once we get to __call__, the path is lost so we
            capture it here on initialization
            """
            super(MyUser, self).__init__(context, request)
            self.section = 'profile-latest' # default page
            if len(request.path) == 2:
                [self.section, profileid] = request.path
            elif len(self.request.path) == 1:
                self.section = request.path[0]

        def __call__(self):
            # do the permission check here, now that Zope has set
            # up the security context. It can't be checked in __init__
            # because the security manager isn't set up on traverse
            self.checkPermission()

            # XXX: still need to check the permission of the view
            try:
                view = api.content.get_view(self.section,
                                            self.context,
                                            self.request)
            except api.exc.InvalidParameterError:
                # just return the default view
                view = api.content.get_view('profile-latest',
                                            self.context,
                                            self.request)
            return view()

        def checkPermission(self):
            """You might want to do other stuff"""
            raise Unauthorized



More information:

* http://play.pixelblaster.ro/blog/archive/2006/10/21/custom-traversing-with-five-and-itraversable

Traverse events
===================

Use ``zope.traversing.interfaces.IBeforeTraverseEvent`` for register a
traversing hook for Plone site object or such.

Example::

    from Products.CMFCore.interfaces import ISiteRoot
    from zope.traversing.interfaces import IBeforeTraverseEvent
    from five import grok

    @grok.subscribe(ISiteRoot, IBeforeTraverseEvent)
    def check_redirect(site, event):
        """
        """
        request = event.request

        # XXX: To something

Use ``ZPublisher.BeforeTraverse`` to register traverse hooks for any
objects.

.. TODO:: Example - not sure if before travese hooks are persistent or not

Advanced traversing with search conditions
===========================================

All Plone content should exist in the :doc:`portal_catalog
</develop/plone/searching_and_indexing/query>`.  Catalog provides fast query access with
various indexes to the Plone content.

Other resources
===============

See object publishing_.

.. _acquisition: http://docs.zope.org/zope2/zope2book/source/Acquisition.html

.. _publishing: http://docs.zope.org/zope2/zope2book/source/ZopeArchitecture.html#fundamental-zope-concepts

.. _Traversable: https://github.com/zopefoundation/Zope/blob/master/src/OFS/Traversable.py

.. _Unauthorized: https://github.com/zopefoundation/AccessControl/blob/master/src/AccessControl/unauthorized.py

.. _UID: https://pypi.python.org/pypi/Products.CMFUid


