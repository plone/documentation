=====
Views
=====

.. admonition:: Description

    Rendering HTML pages in Plone using the Zope 3 *view* pattern.


Introduction
============

Plone/Zope uses a *view* pattern to output dynamically generated HTML pages.

*Views* are the basic elements of modern Python web frameworks. A view runs
code to setup Python variables for a rendering template. Output is not
limited to HTML pages and snippets, but may contain :term:`JSON`,
file download payloads, or other data formats.

Views are usually a combination of:

* a Python class, which performs the user interface logic setup, and a
* corresponding :term:`ZPT` page template, or direct Python string output.

By keeping as much of the view logic in a separate Python class as we
can and making the page template as simple as possible, better component
readability and reuse is achieved. You can override the Python logic
or the template file, or both.

When you are working with Plone, the most usual view type is ``BrowserView``
from the `Products.Five`_ package, but there are others.

Each ``BrowserView`` class is a Python callable.
The ``BrowserView.__call__()`` method acts as an entry point to executing
the view code. From Zope's point of view, even a function would be
sufficient, as it is a callable.

More information
================

* `Mastering Plone Training <http://training.plone.org/5/>`_ has several chapters on views.



View components
===============

Views are Zope Component Architecture (:term:`ZCA`) *multi-adapter
registrations*.

Views are looked up by name. The Zope publisher always does a view lookup,
instead of traversing, if the name to be traversed is prefixed with ``@@``.

Views are resolved with three inputs:

*context*
    Any class/interface for which the view applies. If not given, ``zope.interface.Interface``
    is used (corresponds to a registration ``for="*"``). Usually this is a content item
    instance.

*request*
    The current HTTP request. Interface
    ``zope.publisher.interfaces.browser.IBrowserRequest`` is used.

*layer*
    Theme layer and addon layer interface. If not given,
    ``zope.publisher.interfaces.browser.IDefaultBrowserLayer`` is used.

Views return HTTP request payload as the output. Returned
strings are turned to HTML page responses.

Views can be any Python class taking in (context, request) construction parameters. Minimal view would be::

      class MyView(object):

           def __init__(self, context, request):
                self.context = context
                self.request = request

           def __call__(self):
                return "Hello world. You are rendering this view at the context of %s" % self.context

However, in the most of cases

* Full Plone page views are subclass of `Products.Five.browser.BrowserView <https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/browser/__init__.py#L23>`_
  which is a wrapper class. It wraps `zope.publisher.browser.BrowserView <https://github.com/zopefoundation/zope.publisher/blob/master/src/zope/publisher/browser.py#L896>`_
  and adds an acquisition (parent traversal) support for it.

* Views have ``index`` attribute which points to :doc:`TAL page template </adapt-and-extend/theming/templates_css/template_basics>`
  responsible rendering the HTML code. You get the HTML output by doing self.index() and page template
  gets a context argument ``view`` pointing to the view class instance. ``index`` value
  is usually instance of `Products.Five.browser.pagetemplate.ViewPageTemplateFile <https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/browser/pagetemplatefile.py#L33>`_
  (full Plone pages) or `zope.pagetemplate.pagetemplatefile.PageTemplateFile <https://github.com/zopefoundation/zope.pagetemplate/blob/master/src/zope/pagetemplate/pagetemplatefile.py#L40>`_
  (HTML snippets, no acquisition)

* View classes should implement :doc:`interface </develop/addons/components/interfaces>`
  `zope.browser.interfaces.IBrowserView <https://github.com/zopefoundation/zope.browser/blob/master/src/zope/browser/interfaces.py#L27>`_

Views rendering page snippets and parts can be subclasses of zope.publisher.browser.BrowserView directly
as snippets might not need acquisition support which adds some overhead to the rendering process.

Customizing views
=================

To customize existing Plone core or add-on views you have different options.

* Usually you can simply override the related page template file (``.pt``).

* Sometimes you need to change the related Python view class code also.
  In this case, you override the Python class by using your own add-on which
  installs a view class replacement using add-on layer.

Overriding view template
------------------------

Follow instructions how to :doc:`use z3c.jbot
</adapt-and-extend/theming/templates_css/template_basics>` to override templates.

Overriding view class
---------------------

Here is a short introduction on finding how existing views are defined.

First, you go to ``portal_types`` to see what views have been registered for
a particular content type.

For example, if you want to override the *Tabular* view of a *Folder*,
you find out that it is registered as the handler for
``/folder_tabular_view``.

You look for both ``folder_tabular_view`` old-style page templates and
``@@folder_tabular_view`` BrowserView ZCML registrations in the Plone
source tree |---| it can be either.

Example of how to search for this using UNIX tools (assuming that
`collective.recipe.omelette`_ is in use, to keep included code together):

.. code-block:: console

    # find old style .pt files:
    find parts/omelette -follow -name "folder_tabular_view*"
    # find new style view registrations in ZCML files:
    grep -ri --include="\*.zcml" folder_tabular_view parts/omelette

The ``folder_tabular_view`` is found in
the :doc:`skin layer </adapt-and-extend/theming/templates_css/skin_layers>`
called ``plone_content`` in the CMFPlone product.

More info:

* :doc:`How to override old style page templates </adapt-and-extend/theming/templates_css/skin_layers>`

Creating and registering a view
===============================

This shows how to create and register view in a Zope 3 manner.


Creating a view
---------------

Create your add-on product using :doc:`Dexterity project template </develop/addons/bobtemplates.plone/README>`.

Python logic code
`````````````````

Add the file ``yourcompany.app/yourcompany/app/browser/views.py``::

    """ Example view
    """

    # Zope imports
    from zope.interface import Interface
    from Products.Five.browser import BrowserView
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class MyView(BrowserView):
        """ Render the title and description of item only (example)
        """
        index = ViewPageTemplateFile("myview.pt")


.. warning::

    Do not attempt to run any code in the ``__init__()`` method of a
    view.  If this code fails and an exception is raised, the
    ``zope.component`` machinery remaps this to a "View not found"
    exception or traversal error.

    Additionally, view class may be instantiated in other places than where
    you intended to render the view.
    For example, plone.app.contentmenu does this when creating the menu to
    select a view layout.
    This will result in the ``__init__()`` being called on unexpected
    contexts, probably wasting a lot of time.

    Instead, use a pattern where you have a ``setup()`` or similar
    method which ``__call__()`` or view users can explicitly call.


Registering a view
``````````````````

Zope 3 views are registered in :term:`ZCML`, an XML-based configuration
language.  Usually, the configuration file, where the registration done, is
called ``yourapp.package/yourapp/package/browser/configure.zcml``.

The following example registers a new view (see below for comments):

.. code-block:: xml

    <configure
          xmlns="http://namespaces.zope.org/zope"
          xmlns:browser="http://namespaces.zope.org/browser"
          >

        <browser:page
              for="*"
              name="test"
              permission="zope2.Public"
              class=".views.MyView"
              />

    </configure>

``for``
    specifies which content types receive this view.
    ``for="*"`` means that this view can be used for any content type. This
    is the same as registering views to the ``zope.interface.Interface``
    base class.

``name``
    is the name by which the view is exposed to traversal and
    ``getMultiAdapter()`` look-ups. If your view's name is ``test``, then
    you can render it in the browser by calling
    http://yourhost/site/page/@@test

``permission``
    is the permission needed to access the view.
    When an HTTP request comes in, the currently logged in user's access
    rights in the current context are checked against this permission.
    See :doc:`Security chapter </develop/plone/security/permission_lists>` for Plone's
    out-of-the-box permissions. Usually you want have ``zope2.View``,
    ``cmf.ModifyPortalContent``, ``cmf.ManagePortal`` or ``zope2.Public``
    here.

``class``
    is a Python dotted name for a class based on ``BrowserView``, which is
    responsible for managing the view. The Class's ``__call__()`` method is
    the entry point for view processing and rendering.

.. Note:: You need to declare the ``browser`` namespace in your
   ``configure.zcml`` to use ``browser`` configuration directives.


The view in question is not registered against any :doc:`layer </develop/plone/views/layers>`,
it is immediately available after restart without need to run :doc:`Add/remove in Site setup </develop/addons/components/genericsetup>`.

Page template
`````````````

Create a :doc:`page template for your view. </adapt-and-extend/theming/templates_css/template_basics>`.
Create a file ``myview.pt`` file in ``yourcompany.app/yourcompany/app/browser/templates``
and add the template:

.. code-block:: xml

	<html xmlns="http://www.w3.org/1999/xhtml"
	      xmlns:metal="http://xml.zope.org/namespaces/metal"
	      xmlns:tal="http://xml.zope.org/namespaces/tal"
	      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
	      metal:use-macro="context/main_template/macros/master">

	    <metal:block fill-slot="content-core">
	            XXX - this text comes below title and description
	    </metal:block>

	</html>

When you restart to Plone (or use :doc:`auto-restart add-on </develop/plone/getstarted/index>`)
the view should be available through your browser.

Accessing your newly created view
`````````````````````````````````

Now you can access your view within the news folder::

    http://localhost:8080/Plone/news/myview

... or on a site root::

    http://localhost:8080/Plone/myview

... or on any other content item.

You can also use the ``@@`` notation at the front of the view name to make
sure that you are looking up a *view*, and not a content item that happens
to have the same id as a view::

        http://localhost:8080/Plone/news/@@myview

More info

* https://plone.org/products/dexterity/documentation/manual/five.grok/browser-components/views

Content slots
-------------

Available :doc:`slot </adapt-and-extend/theming/templates_css/template_basics>`
options you can use for ``<metal fill-slot="">`` in your template which
inherits from ``<html metal:use-macro="context/main_template/macros/master">``:

``content``
    render edit border yourself

``main``
    overrides main slot in main template; you must render title and description yourself

``content-title``
    title and description prerendered, Plone version > 4.x

``content-core``
    content body specific to your view, Plone version > 4.x

``header``
    A slot for inserting content above the title; may be useful in conjunction with
    content-core slot if you wish to use the stock content-title provided by the
    main template.

Relationship between views and templates
----------------------------------------

The ZCML ``<browser:view template="">`` directive will set the ``index``
class attribute.

The default view's ``__call__()`` method will return the value
returned by a call to ``self.index()``.

Example: this ZCML configuration:

.. code-block:: xml

    <browser:page
        for="*"
        name="test"
        permission="zope2.Public"
        class=".views.MyView"
        />

and this Python code::

    from Products.Five.browser import BrowserView
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class MyView(BrowserView):

        index = ViewPageTemplateFile("my-template.pt")

is equal to this ZCML configuration::

    <browser:page
        for="*"
        name="test"
        permission="zope2.Public"
        class=".views.MyView"
        template="my-template.pt"
        />

and this Python code::

    class MyView(BrowserView):
        pass

Rendering of the view is done as follows::

    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class MyView(BrowserView):

        # This may be overridden in ZCML
        index = ViewPageTemplateFile("my-template.pt")

        def render(self):
            return self.index()

        def __call__(self):
            return self.render()


Overriding a view template at run-time
--------------------------------------

Below is a sample code snippet which allows you to override an already
constructed ``ViewPageTemplateFile`` with a chosen file at run-time::

    import plone.z3cform
    from zope.app.pagetemplate import ViewPageTemplateFile as Zope3PageTemplateFile
    from zope.app.pagetemplate.viewpagetemplatefile import BoundPageTemplate

    # Construct template from a file which lies in a certain package
    template = Zope3PageTemplateFile(
            'subform.pt',
            os.path.join(
                    os.path.dirname(plone.z3cform.__file__),
                    "templates"))

    # Bind template to context:
    # make the template callable with template() syntax and context
    form_instance.template = BoundPageTemplate(template, form_instance)

Several templates per view
--------------------------

You can bind several templates to one view and render them individually.
This is useful for reusable templating, or when you subclass
your functional views.

Example using `five.grok`_::

	class CourseTimetables(grok.View):

	    # For communicating state variables from Python code to JavaScript
	    jsHeaderTemplate = grok.PageTemplateFile("templates/course-timetables-fees-js-snippet.pt")

	    def renderJavascript(self):
	        return self.jsHeaderTemplate.render(self)

And then call in the template:

.. code-block:: html

    <metal:javascriptslot fill-slot="javascript_head_slot">
        <script tal:replace="structure view/renderJavascript" />
    </metal:javascriptslot>

View ``__init__()`` method special cases
`````````````````````````````````````````

The Python constructor method of the view, ``__init__()``, is special.
You should never try to put your code there. Instead, use helper method or
lazy construction design pattern if you need to set-up view variables.

The ``__init__()`` method of the view might not have an :doc:`acquisition chain </develop/plone/serving/traversing>`
available, meaning that it does not know the parent or hierarchy where the view is.

This information is set after the constructor have been run.
All Plone code which relies on acquisition chain, which means almost all Plone helper code, does not work in ``__init__()``.
Thus, the called Plone API methods return ``None`` or tend to throw exceptions.

Layers
------

Views can be registered against a specific *layer* interface.
This means that views are only looked up if the specified layer is in use.
Since one Zope application server can contain multiple Plone sites, layers
are used to determine which Python code is in effect for a given Plone site.

A layer is in use when:

* a theme which defines that layer is active, or
* if a specific add-on product which defines that layer is installed.

You should register your views against a certain layer in your own code.

For more information, see

* :doc:`browser layers </develop/plone/views/layers>`

Register and unregister view directly using zope.component architecture
-----------------------------------------------------------------------

Example how to register::

	import zope.component
	import zope.publisher.interfaces.browser

        zope.component.provideAdapter(
            # Our class
            factory=TestingRedirectHandler,
            # (context, request) layers for multiadapter lookup
            # We provide None as layers are not used
            adapts=(None, None),
            # All views are registered as IBrowserView interface
            provides=zope.publisher.interfaces.browser.IBrowserView,
            # View name
            name='redirect_handler')


Example how to unregister::

        # Dynamically unregister a view
        gsm = zope.component.getGlobalSiteManager()
        gsm.unregisterAdapter(factory=TestingRedirectHandler,
                              required=(None, None),
                              provided=zope.publisher.interfaces.browser.IBrowserView,
                              name="redirect_handler")


Content type, mimetype and Template start tag
=============================================

If you need to produce non-(X)HTML output, here are some resources:

* http://plone.293351.n2.nabble.com/Setting-a-mime-type-on-a-Zope-3-browser-view-td4442770.html

Zope ViewPageTemplateFile vs. Five ViewPageTemplateFile
=======================================================

.. warning::

    There are two different classes that share the same ``ViewPageTemplateFile`` name.

* Zope  `BrowserView source code <https://github.com/zopefoundation/zope.publisher/blob/master/src/zope/publisher/browser.py>`_.

* `Five version  <https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/browser/__init__.py>`_.
  `Products.Five`_ is a way to access some Zope 3 technologies from the Zope
  2 codebase, which is used by Plone.

Difference in code::

    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

vs.::

    from zope.app.pagetemplate import ViewPageTemplateFile


The difference is that the *Five* version supports:

* Acquisition.
* The ``provider:`` TAL expression.
* Other Plone-specific TAL expression functions like ``test()``.
* Usually, Plone code needs the Five version of ``ViewPageTemplateFile``.
* Some subsystems, notably the ``z3c.form`` package, expect the Zope 3
  version of ``ViewPageTemplateFile`` instances.


Overriding a view class in a product
====================================

Most of the code in this section is copied from a `tutorial by Martin Aspeli
(on slideshare.net)
<http://www.slideshare.net/wooda/martin-aspeli-extending-and-customising-plone-3>`_.
The main change is that, at least for Plone 4, the interface should subclass
``plone.theme.interfaces.IDefaultPloneLayer`` instead of
``zope.interface.Interface``.

In this example we override the ``@@register`` form from the
``plone.app.users`` package, creating a custom form which subclasses the
original.

* Create an interface in ``interfaces.py``::

    from plone.theme.interfaces import IDefaultPloneLayer

    class IExamplePolicy(IDefaultPloneLayer):
        """ A marker interface for the theme layer
        """

* Then create ``profiles/default/browserlayer.xml``:

.. code-block:: xml

    <layers>
      <layer
        name="example.policy.layer"
        interface="example.policy.interfaces.IExamplePolicy"
      />
    </layers>

* Create ``browser/configure.zcml``:

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="example.policy">
      <browser:page
          name="register"
          class=".customregistration.CustomRegistrationForm"
          permission="cmf.AddPortalMember"
          for="plone.app.layout.navigation.interfaces.INavigationRoot"
          layer="example.policy.interfaces.IExamplePolicy"
          />
    </configure>

.. note::

    We've retained the permissions and marker interface of the original view.
    You may provide a specific permission or marker interface instead of these
    as your product requires.

* Create ``browser/customregistration.py``::

    from plone.app.users.browser.register import RegistrationForm

    class CustomRegistrationForm(RegistrationForm):
        """ Subclass the standard registration form
        """

Helper views
============

Not all views need to return HTML output, or output at all.
Views can beused as helpers in the code to provide APIs to objects. Since views
can be overridden using layers, a view is a natural plug-in point which an
add-on product can customize or override in a conflict-free manner.

View methods are exposed to page templates and such, so you can also call
view methods directly from a page template, not only from Python code.

More information
----------------

- :doc:`Context helpers </develop/plone/misc/context>`

- :doc:`Expressions </develop/plone/functionality/expressions>`

Historical perspective
-----------------------

Often, the point of using helper views is that you can have reusable
functionality which can be plugged in as one-line code around the system.
Helper views also get around the following limitations:

* TAL security.
* Limiting Python expression to one line.
* Not being able to import Python modules.

.. Note::

    Using ``RestrictedPython`` scripts (creating Python through the
    Management Interface) and Zope 2 Extension modules is discouraged.
    The same functionality can be achieved with helper views, with less
    potential pitfalls.

Reusing view template snippets or embedding another view
========================================================

To use the same template code several times you can either:

* create a separate ``BrowserView`` for it and then call this view (see
  `Accessing a view instance in code`_ below);

* share a ``ViewPageTemplate`` instance between views and using it several
  times.

.. Note::

    The Plone 2.x way of doing this with TAL template language macros is
    discouraged as a way to provide reusable functionality in your add-on
    product.
    This is because macros are hardwired to the TAL template language, and
    referring to them outside templates is difficult.

    If you ever need to change the template language, or mix in other
    template languages, you can do better when templates are a
    feature of a pure Python based view, and not vice versa.

Here is an example of how to have a view snippet which can be used by
subclasses of a base view class. Subclasses can refer to this template
at any point of the view rendering, making it possible for subclasses
to have fine-tuned control over how the template snippet is
represented.

Related Python code::

    from Products.Five import BrowserView
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class ProductCardView(BrowserView):
        """
        End user visible product card presentation.
        """
        implements(IProductCardView)

        # Nested template which renders address box + buy button
        summary_template = ViewPageTemplateFile("summarybox.pt")


        def renderSummary(self):
            """ Render summary box

            @return: Resulting HTML code as Python string
            """
            return self.summary_template()

Then you can render the summary template in the main template associated
with ``ProductCardView`` by calling the ``renderSummary()`` method and TAL
non-escaping HTML embedding.

.. code-block:: html

    <h1 tal:content="context/Title" />

    <div tal:replace="structure view/renderSummary" />

    <div class="description">
        <div tal:condition="python:context.Description().decode('utf-8') != u'None'" tal:replace="structure context/Description" />
    </div>

The ``summarybox.pt`` itself is a piece of HTML code without the
Plone decoration frame (``main_template/master`` etc. macros).  Make sure
that you declare the ``i18n:domain`` again, or the strings in this
template will not be translated.

.. code-block:: html

    <div class="summary-box" i18n:domain="your.package">
        ...
    </div>

Accessing a view instance in code
=================================

You need to get access to the view in your code if you are:

* calling a view from inside another view, or
* calling a view from your unit test code.

Below are two different approaches for that.


By using ``getMultiAdapter()``
------------------------------

This is the most efficient way in Python.

Example::

    from Acquisition import aq_inner
    from zope.component import getMultiAdapter

    def getView(context, request, name):
        # Remove the acquisition wrapper (prevent false context assumptions)
        context = aq_inner(context)
        # May raise ComponentLookUpError
        view = getMultiAdapter((context, request), name=name)
        # Add the view to the acquisition chain
        view = view.__of__(context)
        return view


By using traversal
------------------

Traversal is slower than directly calling ``getMultiAdapter()``.  However,
traversal is readily available in templates and ``RestrictedPython``
modules.

Example::

    def getView(context, name):
        """ Return a view associated with the context and current HTTP request.

        @param context: Any Plone content object.
        @param name: Attribute name holding the view name.
        """

        try:
            view = context.unrestrictedTraverse("@@" + name)
        except AttributeError:
            raise RuntimeError("Instance %s did not have view %s" % (str(context), name))

        view = view.__of__(context)

        return view

You can also do direct view look-ups and method calls in your template
by using the ``@@``-notation in traversing.

.. code-block:: html

    <div tal:attributes="lang context/@@plone_portal_state/current_language">
        We look up lang attribute by using BrowserView which name is "plone_portal_state"
    </div>


Use a skin-based template in a Five view
----------------------------------------

Use ``aq_acquire(object, template_name)``.

Example: Get an object by its path and render it using its default
template in the current context.

.. code-block:: python

    from Acquisition import aq_base, aq_acquire
    from Products.Five.browser import BrowserView

    class TelescopeView(BrowserView):
        """
        Renders an object in a different location of the site when passed the
        path to it in the querystring.
        """
        def __call__(self):
            path = self.request["path"]
            target_obj = self.context.restrictedTraverse(path)
            # Strip the target_obj of context with aq_base.
            # Put the target in the context of self.context.
            # getDefaultLayout returns the name of the default
            # view method from the factory type information
            return aq_acquire(aq_base(target_obj).__of__(self.context),
                              target_obj.getDefaultLayout())()

Listing available views
=======================

This is useful for debugging purposes::

    from plone.app.customerize import registration
    from zope.publisher.interfaces.browser import IBrowserRequest

    # views is generator of zope.component.registry.AdapterRegistration objects
    views = registration.getViews(IBrowserRequest)

Listing all views of certain type
---------------------------------

How to filter out views which provide a certain interface::

    from plone.app.customerize import registration
    from zope.publisher.interfaces.browser import IBrowserRequest

    # views is generator of zope.component.registry.AdapterRegistration objects
    views = registration.getViews(IBrowserRequest)

    # Filter out all classes which implement a certain interface
    views = [ view.factory for view in views if IBlocksView.implementedBy(view.factory) ]


Default view of a content item
==============================

Objects have views for default, view, edit, and so on.

The distinction between the *default* and *view* views are that for files,
the default can be *download*.

The default view ...

* This view is configured in :doc:`portal_types </develop/plone/content/types>`.

* This view is rendered when a content item is called |---| even though
  they are objects, they have the ``__call__()`` Python method
  defined.

If you need to get a content item's view for page
rendering explicitly, you can do it as follows::

    def viewURLFor(item):
        cstate = getMultiAdapter((item, item.REQUEST),
                                 name='plone_context_state')
        return cstate.view_url()

More info:

* :doc:`Context helpers and utilities </develop/plone/misc/context>`

* http://plone.293351.n2.nabble.com/URL-to-content-view-tp6028204p6028204.html


Allowing the contentmenu on non-default views
=============================================

In general, the contentmenu (where the actions, display views, factory types,
workflow, and other dropdowns are) is not shown on non-default views. There are
some exceptions, though.

If you want to display the contentmenu in such non-default views, you have to
mark them with the IViewView interface from plone.app.layout either by letting
the class provide IViewView by declaring it with zope.component.implements or
by configuring it via ZCML like so::

  <class class="dotted.path.to.browser.view.class">
    <implements interface="plone.app.layout.globals.interfaces.IViewView" />
  </class>


Views and automatic member variable acquisition wrapping
========================================================

View class instances will automatically assign themselves as a parent for all member
variables. This is because ``five`` package based views inherit from ``Acquisition.Implicit`` base class.

E.g. you have a ``Basket`` content item with ``absolute_url()`` of::

    http://localhost:9666/isleofback/sisalto/matkasuunnitelmat/d59ca034c50995d6a77cacbe03e718de

Then if you use this object in a view code's member variable assignment in e.g. ``Viewlet.update() method``::

    self.basket = my_basket

... this will mess up the Basket content item's acquisition chain::

    <Basket at /isleofback/sisalto/yritykset/katajamaan_taksi/d59ca034c50995d6a77cacbe03e718de>

This concerns views, viewlets and portlet renderers. It will, for example, make the following code to fail::

            self.obj = self.context.reference_catalog.lookupObject(value)
            return self.obj.absolute_url() # Acquistion chain messed up, getPhysicalPath() fails

One workaround to avoid this mess is to use aq_inner when accessing self.obj values:

* http://stackoverflow.com/a/11755348/315168

.. _Products.Five:
   https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/doc/manual.txt
.. _five.grok: https://pypi.python.org/pypi/five.grok
.. _collective.recipe.omelette:
   https://pypi.python.org/pypi/collective.recipe.omelette
.. |---| unicode:: U+02014 .. em dash
