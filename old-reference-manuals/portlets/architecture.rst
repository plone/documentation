=================================
Basic plone.portlets architecture
=================================

.. admonition:: Description

        This section describes the general architecture of a portlet through an example. You can checkout the example code `from the collective <http://svn.plone.org/svn/collective/ploneexample.portlet/trunk/>`_.

.. contents :: :local:

The use case
~~~~~~~~~~~~

As an example, we will develop a portlet to display the last *n*
(where *n* is a positive integer ;) modified content items to
logged-in users, which will be available to add it to any portlet
manager (left or right column by default).

[screenshot follows]

The configuration data
~~~~~~~~~~~~~~~~~~~~~~

When a portlet is first created, there are often customizations
which can be made which tailor the portlet's behaviour to meet the
user's needs: eg. which content type to display, how many items to
list, etc... In our example, we want the person configuring the
portlet to be able to specify how many of the most recent items
will be displayed inside the portlet.

First, we have to describe the interface schema of the
configuration data we want to store using ``zope.schema`` (see
`this page <http://wiki.zope.org/zope3/schema.html>`_ for more info
on schemas). By convention, this interface derives from
``IPortletDataProvider``, which is just a marker interface. In the
package's *interfaces.py* file, type:

::

    from plone.portlets.interfaces import IPortletDataProvider
    from Products.CMFPlone import PloneMessageFactory as _
    
    class IRecentPortlet(IPortletDataProvider):
        count = schema.Int(title=_(u'Number of items to display'),
                           description=_(u'How many items to list.'),
                           required=True,
                           default=5)

The ``PloneMessageFactory`` makes our code ready to be localized
using the Plone i18n machinery.

After defining the configuration schema interface, we implement it
in a class called the Assignment class. This is a persistent
"content" class which stores the persistent configuration data (if
any) of the portlet. Even when a portlet is not configurable, it
needs to have an Assignment class, because the presence of an
Assignment instance in various places is what determines what
portlets show up where.

The Assignment class has a ``title`` attribute that is used in the
portlet management UI to distinguish different instances of the
portlet.

::

    from plone.app.portlets.portlets import base
    from zope.interface import implements
    from ploneexample.portlet.interfaces import IRecentPortlet
    
    class Assignment(base.Assignment):
        implements(IRecentPortlet)
    
        def __init__(self, count=5):
            self.count = count
    
        @property
        def title(self):
            return _(u"Recent items")

The add and edit forms
~~~~~~~~~~~~~~~~~~~~~~

To add the portlet and edit its configuration, we have to define
appropiate add and edit forms.

This is typically done using *zope.formlib* and the portlet schema,
together with some base form classes to save us from designing the
forms template and logic ourselves. If the portlet is not
configurable, this can use the special ``base.NullAddForm``, which
is just a view that creates the portlet and then redirects back to
the portlet management screen.

For more information about *zope.formlib*, check :doc:`this tutorial </old-reference-manuals/formlib/index>`.

The edit form can be omitted if the portlet configuration is not
editable.

::

    from zope.formlib import form
    class AddForm(base.AddForm):
        form_fields = form.Fields(IRecentPortlet)
        label = _(u"Add Recent Portlet")
        description = _(u"This portlet displays recently modified content.")
    
        def create(self, data):
            return Assignment(count=data.get('count', 5))
    
    class EditForm(base.EditForm):
        form_fields = form.Fields(IRecentPortlet)
        label = _(u"Edit Recent Portlet")
        description = _(u"This portlet displays recently modified content.")

As it can be seen above, the add form must return an Assignment
instance of the portlet.

The portlet presentation
~~~~~~~~~~~~~~~~~~~~~~~~

Next, we define how the portlet will be rendered.

The Portlet Renderer is the "view" of the portlet. This is just a
content provider (in the zope.contentprovider sense), in that it
has an ``update()`` and a ``render()`` method, which will be called
upon the rendering of the portlet.

It's a multi-adapter that takes a number of parameters which makes
it possible to vary the rendering of the portlet:

context 
    The current content object. Mind the type of content object that's
    being shown.
request 
    The current request. Mind the current theme/browser layer.
view 
    The current (full page) view. Mind the current view, and whether or
    not this is the canonical view of the object (as indicated by the
    ``IViewView`` marker interface) or a particular view, like the
    manage-portlets view.
manager 
    The portlet manager where this portlet was rendered (for now, think
    of a portlet manager as a column). Mind where in the page the
    portlet was rendered.
data 
    The portlet data, which is basically an instance of the portlet
    assignment class. Mind the configuration of the portlet
    assignment.

The Renderer base class relieves us from having to remember all
these parameters.

The Renderer class must have an ``available`` property, which is
used to determine whether this portlet should be shown or not. Note
you shouldn't include checks for the user id, group or content-type
here, since you can perform these assignments later by registering
the portlet under a certain category (more on this later).

::

    from plone.memoize.instance import memoize
    from zope.component import getMultiAdapter
    from Acquisition import aq_inner
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    
    class Renderer(base.Renderer):
        _template = ViewPageTemplateFile('recent.pt')
    
        def __init__(self, *args):
            base.Renderer.__init__(self, *args)
    
            context = aq_inner(self.context)
            portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
            self.anonymous = portal_state.anonymous()  # whether or not the current user is Anonymous
            self.portal_url = portal_state.portal_url()  # the URL of the portal object
            
            # a list of portal types considered "end user" types
            self.typesToShow = portal_state.friendly_types()  
    
            plone_tools = getMultiAdapter((context, self.request), name=u'plone_tools')
            self.catalog = plone_tools.catalog()
    
        def render(self):
            return self._template()
    
        @property
        def available(self):
            """Show the portlet only if there are one or more elements."""
            return not self.anonymous and len(self._data())
    
        def recent_items(self):
            return self._data()
    
        def recently_modified_link(self):
            return '%s/recently_modified' % self.portal_url
    
        @memoize
        def _data(self):
            limit = self.data.count
            return self.catalog(portal_type=self.typesToShow,
                                sort_on='modified',
                                sort_order='reverse',
                                sort_limit=limit)[:limit]

When reading the previous code, note that:


#. ``plone_portal_state`` and ``plone_tools`` are helper views
   providing some useful attributes to gather information from.
#. The ``memoize`` decorator is used here to cache the results of
   the catalog query to avoid the perfomance hit of re-generating them
   in each request. See the
   `plone.memoize doctests <http://dev.plone.org/plone/browser/plone.memoize/trunk/plone/memoize/README.txt>`_
   for more information.

Registering the portlet
~~~~~~~~~~~~~~~~~~~~~~~

A convenient ZCML directive is provided to glue all components of
the portlet in the Zope Component Architecture. In the package's
*configure.zcml* file (or any other ZCML file included from it),
write:

.. code-block:: xml

    <configure
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="ploneexample.portlet">
    
        <five:registerPackage package="." initialize=".initialize" />
    
        <include package="plone.app.portlets"/>
    
        <plone:portlet
            name="ploneexample.portlet.Recent"
            interface=".recent.IRecentPortlet"
            assignment=".recent.Assignment"
            renderer=".recent.Renderer"
            addview=".recent.AddForm"
            editview=".recent.EditForm"
            />
    
    </configure>

Note you have to define/reference the plone XML namespace for the
directive to work. There is also a ``<plone:portletRenderer />``
directive to override the renderer for a particular
context/layer/view/manager.

You can see the descriptions of all these directives together with
their arguments in the
`metadirectives.py file of the plone.app.portlets package <http://dev.plone.org/plone/browser/plone.app.portlets/trunk/plone/app/portlets/metadirectives.py>`_.

This ZCML directive is read at the Zope startup, so to register
each class appropiately into the Component Architecture, but you
won't be able to add your new portlet yet. You first need to
install its portlet type into your Plone site, as described in the
section which follows.

Installing the portlet
~~~~~~~~~~~~~~~~~~~~~~

The components and registration above make a new type of portlet
available for installation. To install the portlet type into a
particular Plone site, use GenericSetup.

First, register a new GenericSetup extension profile using a
registerProfile ZCML directive:

.. code-block:: xml

    <configure
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:plone="http://namespaces.plone.org/plone"
        xmlns:gs="http://namespaces.zope.org/genericsetup"
        i18n_domain="ploneexample.portlet">
    
        <five:registerPackage package="." initialize=".initialize" />
    
        <include package="plone.app.portlets"/>
    
        <gs:registerProfile
            name="ploneexample.portlet"
            title="Recent Items Example"
            directory="profiles/default"
            description="An example portlet"
            provides="Products.GenericSetup.interfaces.EXTENSION"
            />
    
        <plone:portlet
            name="ploneexample.portlet.Recent"
            interface=".recent.IRecentPortlet"
            assignment=".recent.Assignment"
            renderer=".recent.Renderer"
            addview=".recent.AddForm"
            editview=".recent.EditForm"
            />
    
    </configure>

Next, create the folder profiles/default and place a
``portlets.xml`` file inside with the following content:

.. code-block:: xml

    <?xml version="1.0"?>
    <portlets
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="plone">
      <portlet 
        addview="ploneexample.portlet.Recent"
        title="Recent items Example"
        description="An example portlet which can render a listing of recently changed items."
        i18n:attributes="title title_recent_portlet;
                         description description_recent_portlet">
        <for interface="plone.app.portlets.interfaces.IColumn" />
        <for interface="plone.app.portlets.interfaces.IDashboard" />
      </portlet>
    </portlets

When this is run, it will create a local utility in the Plone site
of the ``IPortletType``. This just holds some metadata about the
portlet for UI purposes.

``Title`` and ``description`` should be self-explanatory.

The ``addview`` is the name of the view used to add the portlet,
which helps the UI to invoke the right form when the user asks to
add the portlet. This should match the portlet name.

``for`` is an interface or list of interfaces that describe the
type of portlet managers that this portlet is suitable for. This
means that we can install a portlet that's suitable for the
dashboard, say, but not for the general columns. In this case,
we're making the portlet suitable for the dashboard and for any
(either left or right) column. Current portlet manager interfaces
include ``IColumn``, ``ILeftColumn``, ``IRightColumn`` and
``IDashboard``, all of them defined inside the plone.app.portlets
package.

Again, this is primarily about helping the UI construct appropriate
menus.
