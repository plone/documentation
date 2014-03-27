==========================
How are portlets rendered?
==========================

.. admonition:: Description

        The process to find, update and render portlets from
        the main views is rather complex. Here we describe
        how does it all work, step by step.

.. contents :: :local:

Portlets are always rendered inside a portlet manager. From a
template, we can ask a portlet manager to render itself and all its
portlets. This is achieved using a *zope.contentprovider*
'provider:' expression. In Plone's *main\_template*, for example,
you will find:

.. code-block:: xml

    <tal:block replace="structure provider:plone.leftcolumn" />

Behind the scenes, this will look up a local adapter on (context,
request, view) with name ``plone.leftcolumn`` (this is just how the
provider expression works).

As it happens, this local adapter factory was registered when the
portlet manager was installed (via ``portlets.xml``), and is a
callable that returns an ``IPortletManagerRenderer``. The portlet
manager renderer is the "view" of the portlet manager.

The default implementation will simply output each portlet wrapped
in a div tag with some helpful attributes to support AJAX via KSS.
You can of course register your own portlet manager renderers. A
portlet manager renderer is a multi-adapter on (context, request,
view, manager). The ``@@manage-portlets`` view, for example, relies
on a portlet manager renderer override for this particular view
that renders the add/move/delete operations. For most people, the
standard renderer will suffice, though.

The portlet manager renderer asks an ``IPortletRetriever`` to fetch
and order the portlet assignments that it should render. This is a
multi-adapter on (context, manager), which means that the fetch
algorithm can be overridden either based on the type of content
object being viewed, or the particular manager. There are two
default implementations - one for "placeful" portlet managers
(those which know about contextual portlets, such as the standard
left/right column ones) and one for "placeless" ones that only deal
in global categories. This latter retriever is used by the
dashboard, which stores its portlets in a global "user" category.

The ``IPortletRetriever`` algorithm is reasonably complex,
especially when contextual blacklisting/blocking is taken into
account (see below). To make it possible to re-use this algorithm
across multiple configurations, it is written in terms of an
``IPortletContext``. The context content object will be adapted to
this interface. The portlet context provides:


-  A universal identifier for the current context (usually just the
   physical path) - the ``uid`` property.
-  A way to obtain the parent object of the current context (for
   acquiring portlets and blacklist information in a placeful
   retriever) - the ``getParent()`` method.
-  A list of global portlet categories to look up, and the keys to
   look under (obtainable by using the ``globalPortletCategories()``
   method on the adapted context).

The last parameter is best described by an example. Let's say we're
logged in as "testuser", a member of both the "Administrators" and
"Reviewers" groups, and were looking at a Folder. The return value
of ``globalPortletCategories()`` would then be:

::

    >>> portlet_context.globalPortletCategories()
    [("content_type", "Folder",),
     ("group", "Administrators",),
     ("group", "Reviewers",),
     ("user", "testuser",)]

This informs the retriever that it should first look up any
portlets in the current portlet manager in the "content\_type"
category under the "Folder" key, and then portlets in the "group"
category under the "Administators" and "Reviewers" key, and finally
portlets in the "user" category under the "testuser" key, all in
that order. Thus, if we wanted to add a new category, or change the
order of categories, we could override the ``IPortletContext``,
either everywhere or just for one particular type of context.

Once the ``IPortletRetriever`` has retrieved the assignments that
should be shown for the current portlet manager, the portlet
manager renderer will look up the portlet renderer for each
assignment, ensure that it should indeed be rendered by checking
its ``available`` property, and finally call ``update()`` and
``render()``, placing the output in the reponse.
