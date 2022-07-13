======================
Helper views and tools
======================


Introduction
============

This document explains how to access view and context utilities in Plone.

IPortalState and IContextState
==============================

``IPortalState`` defines ``IContextState`` view-like interfaces
to access miscellaneous information useful for the rendering of the current page.

The views are cached properly, they should access the information effectively.

* ``IPortalState`` is mapped as the ``plone_portal_state`` name view.

* ``IContextState`` is mapped as the ``plone_context_state`` named view.

* ``ITools`` is mapped as the ``plone_tools`` named view.

To see what's available through the interface,
read the documentation in the
`plone.app.layout.globals.interfaces <https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/globals/interfaces.py>`_
module.

Example showing how to get the portal root URL::

    from zope.component import getMultiAdapter
    ...

    class MyView(BrowserView):

        ...

        def __call__(self):
            # aq_inner is needed in some cases like in the portlet renderers
            # where the context itself is a portlet renderer and it's not on the
            # acquisition chain leading to the portal root.
            # If you are unsure what this means always use context.aq_inner
            context = self.context.aq_inner
            portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')

            self.some_url = portal_state.portal_url() + "/my_foo_bar"


Example showing how to get the current language::

    from zope.component import getMultiAdapter

    ...

    portal_state = getMultiAdapter((self.context, self.request), name=u'plone_portal_state')
    current_language = portal_state.language()

Example showing how to expose ``portal_state`` helper to a template:

1. ZCML includes ``portal_state`` in ``allowed_attributes``

.. code-block:: xml

    <browser:page
        for="*"
        name="test"
        permission="zope2.Public"
        class=".views.MyView"
        allowed_attributes="portal_state"
        />

A Python class exposes the variable::

    from Acquisition import aq_inner
    from zope.component import getMultiAdapter

    class MyView(BrowserView):

        def portal_state(self):
            context = aq_inner(self.context)
            portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
            return portal_state

Templates can use it as follows:

.. code-block:: html

    <div>
        The language is <span tal:content="view/portal_state/language" />
    </div>

You can directly look up ``portal_state`` in templates using acquisition
and view traversal, without need of ZCML code
or Python view code changes. This is useful e.g. in overridden
viewlet templates:

.. code-block:: html

    <!--

        During traversal, ``@@`` signals that the traversing
        machinery should look up a view by that name.

        First we look up the view and then use
        it to access the variables defined in
        ``IPortalState`` interface.

    -->

    <div tal:define="portal_state context/@@plone_portal_state" >
        The language is <span tal:content="portal_state/language" />
    </div>

Use in templates and expressions
==================================

You can use ``IContextState`` and ``IPortalState`` in :term:`TALES`
expressions, e.g. ``portal_actions``, as well.

Example ``portal_actions`` conditional expression::

    python:object.restrictedTraverse('@@plone_portal_state').language() == 'fi'


Tools
=====

Tools are persistent utility classes available in the site root.
They are visible in the Management Interface, and sometimes expose useful
information or configuration here. Tools include e.g.:

``portal_catalog``
    Search and indexing facilities for content
``portal_workflow``
    Look up workflow status, and do workflow-related actions.
``portal_membership``
    User registration information.


.. warning::
    Portal tools are deprecated and are phased out and being replaced by
    `utilities <develop/addons/components/utilities.html>`_. The
    `Removal of selected portal tools <https://github.com/plone/documentation/pull/704>`_
    PLIP is created to migrate from tools to utilities.


Get a portal tool using plone.api
---------------------------------

It is recommended to use `plone.api </develop/plone.api/docs/portal.html#get-tool>`_
to get a portal tool::

    from plone import api
    catalog = api.portal.get_tool(name='portal_catalog')

The ``plone.api`` package exposes functionality from portal tools, it is not
longer necessary to directly call a tool. For example; the API can be used
the get the
`workflow state </develop/plone.api/docs/content.html#get-workflow-state>`_,
`change the workflow state </develop/plone.api/docs/content.html#transition>`_,
`get a member </develop/plone.api/docs/user.html#get-all-users>`_ and
`get the member properties </develop/plone.api/docs/user.html#user-properties>`_.


ITools interface
----------------

`plone.app.layout.globals.interfaces.ITools interface <https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/globals/interfaces.py>`_
and Tools BrowserView provide cached access for the most commonly
needed tools.

``ITools`` is mapped as the ``plone_tools`` view for traversing.

Example::

    from Acquisition import aq_inner
    from zope.component import getMultiAdapter

    context = aq_inner(self.context)
    tools = getMultiAdapter((context, self.request), name=u'plone_tools')

    portal_url = tools.url()

    # The root URL of the site is got by using portal_url.__call__()
    # method

    the_current_root_url_of_the_site = portal_url()

``IPlone``
-------------

`Products.CMFPlone.browser.interfaces.IPlone <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/interfaces.py#L183>`_
provides some helper methods for Plone specific functionality and user interface.

* ``IPlone`` helper views is registered under the name ``plone``

``getToolByName``
------------------

``getToolByName`` is the old-fashioned way of getting tools,
using the context object as a starting point.
It also works for tools which do not implement the ``ITools`` interface.

``getToolByName`` gets any Plone portal root item using acquisition.

Example::

    from Products.CMFCore.WorkflowCore import WorkflowException

    # Do the workflow transition "submit" for the current context
    workflowTool = getToolByName(self.context, "portal_workflow")
    workflowTool.doActionFor(self.context, "submit")

