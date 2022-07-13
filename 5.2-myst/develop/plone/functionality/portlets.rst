========
Portlets
========

.. admonition:: Description

   Programmatical manipulation of portlets in Plone.


Introduction
------------

Portlets are editable boxes in the left and right side bar of Plone user interface.
Add-ons allow portlets in other parts in of the user interface too, like above and below the content.

This document is a short introduction.
Please visit the `Portlets reference manual <http://docs.plone.org/4/en/old-reference-manuals/portlets/index.html>`_ for in-depth information.

Related add-ons and packages
----------------------------

You might want to check these before starting to write your own portlet -
for ready solution, for examples, for inspiration.

* `Create your own portlet managers with collective.panels <https://pypi.python.org/pypi/collective.panels>`_

* https://github.com/collective/collective.portletalias

* https://plone.org/products/contentwellportlets

* https://github.com/miohtama/imageportlet

* https://github.com/collective/collective.cover

.. note::

    Using paster is deprecated instead you should use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>`

Creating a portlet
------------------

* You need a paster-compatible product skeleton created using *paster create -t plone* or *paster create -t archetypes* commands.

* Use project specific paster command *paster addcontent portlet* to create a code skeleton for your new portlet.

.. deprecated:: may_2015
    Use :doc:`bobtemplates.plone </develop/addons/bobtemplates.plone/README>` instead

Subclassing a portlet
---------------------

You can subclass a portlet to create a new portlet type with your enhanced functionality.

* `subclassing portlets <http://docs/plone.org/4/en/old-reference-manuals/portlets/appendix/subclassing.html>`_

Using z3c.form in portlets
--------------------------

:doc:`z3c.form </develop/plone/forms/z3c.form>` is a modern form library for Plone. The out of the box Plone portlets
use older *zope.formlib*.

Discussion related to the matter

* http://stackoverflow.com/questions/5174905/can-i-use-z3c-form-on-plone-portlets-instead-of-zope-formlib

Overriding portlet rendering
----------------------------

Use ``<plone:portletRenderer>`` directive.
Specify 1) layer, 2) template and/or 3) class 4) portlet interface.

You need ``<include package="">`` directive for the package
whose portlet you are going to override.

.. code-block:: xml

        <configure
            xmlns:plone="http://namespaces.plone.org/plone"
            >

                <include package="plone.app.portlets" />

                <plone:portletRenderer
                   portlet="plone.app.portlets.portlets.news.INewsPortlet"
                   template="mytheme_news.pt"
                   layer=".interfaces.IThemeSpecific"
                   />

        </configure>

More information


update() and render()
---------------------

These methods should honour `zope.contentprovider.interfaces.IContentProvider call contract <https://github.com/zopefoundation/zope.contentprovider/blob/3.7.2/src/zope/contentprovider/interfaces.py>`_.

available property
------------------

The portlet renderer can define available property to hint the portlet manager when the portlet should be rendered.

Example ::

        class Renderer(base.Renderer):

            @property
            def available(self):
                # Show this portlet for logged in users only
                return not self.anonymous

Iterate portlets assigned to the portal root
---------------------------------------------

Below is an simple example how to print all portlets
which have been assigned to the portal root::

    def check_root_portlets(self):
        """ Print all portlet assignments in the portal root """

        from zope.component import getUtility, getMultiAdapter
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignment
        from plone.portlets.interfaces import IPortletAssignmentMapping

        content = self.portal

        for manager_name in [ "plone.leftcolumn", "plone.rightcolumn" ]:

            print "Checking portlet column:" + manager_name

            manager = getUtility(IPortletManager, name=manager_name, context=content)

            mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)

            # id is portlet assignment id
            # and automatically generated
            for id, assignment in mapping.items():
                print "Found portlet assignment:" + id + " " + str(assignment)

Looking up a portlet by id
--------------------------

Here are some tips how to extract the portlet id data in the portlet
renderer to pass around to be consumed elsewhere.

portlets.py::

    class Renderer(base.Renderer):

        def getImageURL(self, imageDesc):
            """
            :return: The URL where the image can be downloaded from.

            """
            context = self.context.aq_inner

            # [{'category': 'context', 'assignment': <imageportlet.portlets.Assignment object at 0x1138bb140>, 'name': u'bound-method-assignment-title-of-assignment-at-1', 'key': '/Plone/fi'},
            params = dict(
                portletName=self.__portlet_metadata__["name"],
                portletManager=self.__portlet_metadata__["manager"],
                image=imageDesc["id"],
                modified=self.data._p_mtime,
                portletKey=self.__portlet_metadata__["key"],
            )

            imageURL = "%s/@@image-portlet-downloader?%s" % (context.absolute_url(), urllib.urlencode(params))

            return imageURL

Then we can re-look-up this portlet and its image field, based on the field name, in the downloader view::


    # Zope imports
    from zExceptions import InternalError
    from zope.interface import Interface
    from zope.component import getUtility, getMultiAdapter
    from five import grok

    # Plone imports
    from plone.portlets.interfaces import IPortletManager
    from plone.portlets.interfaces import IPortletRetriever
    from plone.namedfile.utils import set_headers, stream_data


    # Local imports
    from interfaces import IAddonSpecific

    grok.templatedir("templates")
    grok.layer(IAddonSpecific)


    class ImagePortletHelper(grok.CodeView):
        """
        Expose stuff downloadable from the image portlet BLOBs.
        """
        grok.context(Interface)
        grok.baseclass()


    class ImagePortletImageDownload(ImagePortletHelper):
        """
        Expose image fields as downloadable BLOBS from the image portlet.

        Allow set caching rules (content caching for this view)
        """
        grok.context(Interface)
        grok.name("image-portlet-downloader")

        def getPortletById(self, content, portletManager, key, name):
            """
            :param content: Context item where the look-up is performed

            :param portletManager: Portlet manager name as a string

            :param key: Assignment key... context path as string for content portlets

            :param name: Portlet name as a string

            :return: Portlet assignment instance
            """

            # Make sure we got input
            assert key, "Give a proper portlet assignment key"
            assert name, "Give a proper portlet assignment name"

            # Resolve portlet and its image field
            manager = getUtility(IPortletManager, name=portletManager, context=content)

            # Mappings can be directly used only when
            # portlet is directly assignment to the content.
            # If it is assigned to the parent we would fail here.
            # mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)

            retriever = getMultiAdapter((content, manager,), IPortletRetriever)

            for assignment in retriever.getPortlets():
                if assignment["key"] == key and assignment["name"] == name:
                    return assignment["assignment"]

            return None

        def render(self):
            """

            """
            content = self.context.aq_inner

            # Read portlet assignment pointers from the GET query
            name = self.request.form.get("portletName")
            manager = self.request.form.get("portletManager")
            imageId = self.request.form.get("image")
            key = self.request.form.get("portletKey")

            portlet = self.getPortletById(content, manager, key, name)
            if not portlet:
                raise InternalError("Portlet not found: %s %s" % (key, name))

            image = getattr(portlet, imageId, None)
            if not image:
                # Ohops?
                raise InternalError("Image was empty: %s" % imageId)



See *imageportlet* add-on for the complete example.


Walking through every portlet on the site
-----------------------------------------

The following code iterates through all portlets assigned
directly to content items. This excludes dashboard, group and content type based portlets.
Then it prints some info about them and renders them.

Example code::

        from Products.Five.browser import BrowserView

        from zope.component import getUtility, getMultiAdapter
        from zope.app.component.hooks import setHooks, setSite, getSite

        from plone.portlets.interfaces import IPortletType
        from plone.portlets.interfaces import IPortletManager
        from plone.portlets.interfaces import IPortletAssignment
        from plone.portlets.interfaces import IPortletDataProvider
        from plone.portlets.interfaces import IPortletRenderer
        from plone.portlets.interfaces import IPortletAssignmentMapping
        from plone.portlets.interfaces import ILocalPortletAssignable

        from Products.CMFCore.interfaces import IContentish

        class FixPortlets(BrowserView):
                """ Magical portlet debugging view """

                def __call__(self):
                    """
                    """

                    request = self.request

                    portal = getSite()

                    # Not sure why this is needed...
                    view = portal.restrictedTraverse('@@plone')

                    # Query all content items on the site which can get portlets assigned
                    # Note that this should excule special, hidden, items like tools which otherwise
                    # might appearn in portal_catalog queries
                    all_content = portal.portal_catalog(show_inactive=True, language="ALL", object_provides=ILocalPortletAssignable.__identifier__)

                    # Load the real object instead of index stub
                    all_content = [ content.getObject() for content in all_content ]

                    # portal itself does not show up in the query above,
                    # though it might contain portlet assignments
                    all_content = list(all_content) + [portal]

                    for content in all_content:

                            for manager_name in [ "plone.leftcolumn", "plone.rightcolumn" ]:

                                    manager = getUtility(IPortletManager, name=manager_name, context=content)

                                    mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)

                                    # id is portlet assignment id
                                    # and automatically generated
                                    for id, assignment in mapping.items():
                                            print "Found portlet assignment:" + id + " " + str(assignment)

                                            renderer = getMultiAdapter((content, request, view, manager, assignment), IPortletRenderer)

                                            # Renderer acquisition chain must be set-up so that templates
                                            # et. al. can resolve permission inheritance
                                            renderer = renderer.__of__(content)

                                            # Seee https://github.com/zopefoundation/zope.contentprovider/blob/3.7.2/src/zope/contentprovider/interfaces.py
                                            renderer.update()
                                            html = renderer.render()
                                            print "Got HTML output:" + html


                    return "OK"

For more information about portlet assignments and managers, see

* https://github.com/plone/plone.app.portlets/blob/master/plone/app/portlets/tests/test_mapping.py

* https://github.com/plone/plone.app.portlets/blob/master/plone/app/portlets/tests/test_traversal.py

* https://github.com/plone/plone.app.portlets/blob/master/plone/app/portlets/configure.zcml

* https://github.com/plone/plone.portlets/blob/master/plone/portlets/interfaces.py

* https://github.com/zopefoundation/zope.contentprovider/blob/3.7.2/src/zope/contentprovider/interfaces.py (for portlet renderers)

Checking if a certain context portlet is active on a page
----------------------------------------------------------

* Iterate through portlet managers by name

* Get portlet retriever for the manager

* Get portlets

* Check if the portlet assignment provides your particular portlet marker interface

Example::


        import Acquisition
        from zope.component import getUtility, getMultiAdapter


        from plone.portlets.interfaces import IPortletRetriever, IPortletManager

        for column in ["plone.leftcolumn", "plone.rightcolumn"]:

            manager = getUtility(IPortletManager, name=column)

            retriever = getMultiAdapter((self.context, manager), IPortletRetriever)

            portlets = retriever.getPortlets()

            for portlet in portlets:

                # portlet is {'category': 'context', 'assignment': <FacebookLikeBoxAssignment at facebook-like-box>, 'name': u'facebook-like-box', 'key': '/isleofback/sisalto/huvit-ja-harrasteet
                # Identify portlet by interface provided by assignment
                if IFacebookLikeBoxData.providedBy(portlet["assignment"]):
                    return True

        return False

Rendering a portlet
--------------------------------

Below is an example how to render a portlet in Plone

* A portlet is assigned to some context in some portlet manager

* We can dig these assignments up by portlet id (not user visible) or portlet type (portlet assignment interface)

How to get your portlet HTML::

    from zope.component import getUtility, getMultiAdapter, queryMultiAdapter
    from plone.portlets.interfaces import IPortletRetriever, IPortletManager, IPortletRenderer
    from plone.portlets.interfaces import IPortletManagerRenderer


    from Products.Five import BrowserView


    class FakeView(BrowserView):
        """
        Portlet manager code goes down well with cyanide.
        """


    def get_portlet_manager(column):
        """ Return one of default Plone portlet managers.

        @param column: "plone.leftcolumn" or "plone.rightcolumn"

        @return: plone.portlets.interfaces.IPortletManagerRenderer instance
        """
        manager = getUtility(IPortletManager, name=column)
        return manager


    def render_portlet(context, request, view, manager, assignmentId):
        """ Render a portlet defined in external location.

        .. note::

            Portlets can be idenfied by id (not user visible)
            or interface (portlet class). This method supports look up
            by interface and will return the first matching portlet with this interface.

        @param context: Content item reference where portlet appear

        @param manager: IPortletManager instance through get_portlet_manager()

        @param view: Current view or None if not available

        @param interface: Marker interface class we use to identify the portlet. E.g. IFacebookPortlet

        @return: Rendered portlet HTML as a string, or empty string if portlet not found
        """

        if not view:
            # manager(context, request, view) does not accept None as multi-adapter lookup parameter
            view = FakeView(context, request)

        retriever = getMultiAdapter((context, manager), IPortletRetriever)

        portlets = retriever.getPortlets()

        assignment = None

        if len(portlets) == 0:
            raise RuntimeError("No portlets available for manager %s in the context %s" % (manager.__name__, context))

        for portlet in portlets:

            # portlet is {'category': 'context', 'assignment': <FacebookLikeBoxAssignment at facebook-like-box>, 'name': u'facebook-like-box', 'key': '/isleofback/sisalto/huvit-ja-harrasteet
            # Identify portlet by interface provided by assignment
            print portlet
            if portlet["name"] == assignmentId:
                 assignment = portlet["assignment"]
                 break

        if assignment is None:
            # Did not find a portlet
            raise RuntimeError("No portlet found with name: %s" % assignmentId)

        # Note: Below is tested only with column portlets

        # PortletManager provides convenience callable
        # which gives you the renderer. The view is mandatory.
        managerRenderer = manager(context, request, view)

        # PortletManagerRenderer convenience function
        renderer = managerRenderer._dataToPortlet(portlet["assignment"].data)

        if renderer is None:
            raise RuntimeError("Failed to get portlet renderer for %s in the context %s" % (assignment, context))

        renderer.update()
        # Does not check visibility here... force render always
        html = renderer.render()

        return html

How to use this code in your own view, please see `collective.portletalias source <https://github.com/collective/collective.portletalias/blob/master/collective/portletalias/portlets/aliasportlet.py#L73>`_

More info

* http://blog.mfabrik.com/2011/03/10/how%C2%A0to-render-a-portlet-in-plone/

Hiding unwanted portlets
-----------------------------

Example portlets.xml::

  <!-- This leaves only News portlet -->

  <portlet addview="portlets.Calendar" remove="true" />
  <portlet addview="portlets.Classic" remove="true" />
  <portlet addview="portlets.Login" remove="true" />
  <portlet addview="portlets.Events" remove="true" />
  <portlet addview="portlets.Recent" remove="true" />
  <portlet addview="portlets.rss" remove="true" />
  <portlet addview="portlets.Search" remove="true" />
  <portlet addview="portlets.Language" remove="true" />
  <portlet addview="plone.portlet.collection.Collection" remove="true" />
  <portlet addview="plone.portlet.static.Static" remove="true" />

  <!-- collective.flowplayer add-on -->
  <portlet addview="collective.flowplayer.Player" remove="true" />


Portlet names can be found in ``plone.app.portlets/configure.zcml``.

More info:

* http://stackoverflow.com/questions/5897656/disabling-portlet-types-site-wide-in-plone

Disabling right or left columns in a view or template
-----------------------------------------------------

Sometimes, when you work with custom views and custom templates you need to
disable right or left column for portlets.

This is how you do from within a template:

.. code-block:: xml

    <metal:override fill-slot="top_slot"
        tal:define="disable_column_one python:request.set('disable_plone.leftcolumn',1);
                    disable_column_two python:request.set('disable_plone.rightcolumn',1);"/>

And this is how you do it from within a view::

    import grok

    class SomeView(grok.View):
        grok.context(IPloneSiteRoot)

        def update(self):
            super(SomeView, self).update()
            self.request.set('disable_plone.rightcolumn',1)
            self.request.set('disable_plone.leftcolumn',1)

Source: http://stackoverflow.com/questions/5872306/how-can-i-remove-portlets-in-edit-mode-with-plone-4

Disabling right or left columns on a context
--------------------------------------------

Sometimes you just want to turn off the portlets in a certain context that doesn't have
a template or fancy view.  To do this in code do this::

    from zope.component import getMultiAdapter
    from zope.component import getUtility

    from plone.portlets.interfaces import IPortletManager
    from plone.portlets.interfaces import ILocalPortletAssignmentManager
    from plone.portlets.constants import CONTEXT_CATEGORY

    # Get the proper portlet manager
    manager = getUtility(IPortletManager, name=u"plone.leftcolumn")

    # Get the current blacklist for the location
    blacklist = getMultiAdapter((context, manager), ILocalPortletAssignmentManager)

    # Turn off the manager
    blacklist.setBlacklistStatus(CONTEXT_CATEGORY, True)


Or just do it using GenericSetup like a sane person:

* https://plone.org/documentation/manual/developer-manual/generic-setup/reference/portlets

* https://plone.org/products/plone/roadmap/203

Creating a new portlet manager
----------------------------------

If you need additional portlet slots at the site.
In this example we use ``Products.ContentWellCode`` to provide us some
facilities as a dependency.

* Create a viewlet which will handle portlet rendering in a normal page mode.
  Have several portlet slots, a.k.a. wells, where you can drop in portlets.
  Wells are rendered horizontally side-by-side and portlets going in
  from top to bottom.

* Register this viewlet in a viewlet manager where you wish to show your portlets
  on the main template

* Have a management view which allows you to shuffle portlets around. This
  is borrowed from ``Products.ContentWellPortlets``.

* Register portlet wells in ``portlets.xml`` - note that one
  management view can handle several slots as in the example below

The code skeleton works against `this Plone add-on template <https://github.com/miohtama/sane_plone_addon_template>`_.

Example portlet manager viewlets.py::

    """

        For more information see

        * http://docs.plone.org/5/en/develop/plone/views/viewlets.html

    """

    import logging
    from fractions import Fraction

    # Zope imports
    from zope.interface import Interface
    from zope.component import getMultiAdapter, getUtility, queryUtility
    from five import grok

    # Plone imports
    from plone.portlets.interfaces import IPortletManager
    from plone.app.layout.viewlets.interfaces import IPortalFooter
    from Products.CMFCore.utils import getToolByName

    # Local imports
    from interfaces import IAddonSpecific, IThemeSpecific

    grok.templatedir("templates")
    grok.layer(IThemeSpecific)

    # By default, set context to zope.interface.Interface
    # which matches all the content items.
    # You can register viewlets to be content item type specific
    # by overriding grok.context() on class body level
    grok.context(Interface)

    logger = logging.getLogger("PortletManager")


    class CustomPortletViewlet(grok.Viewlet):
        """ grok viewlet base class for a custom portlet renderer based on Products.ContentWellPortlets

        Orignal code from Products.ContentWellPortlets
        """
        grok.baseclass()

        # Id which we use to store portlets
        name = ""

        # Name of browser view which will render the management interface for portlets
        # in this manager
        manage_view = ""

        # We have 5 portlet slots in this viewlet
        portlet_count = 5

        def update(self):
            context_state = getMultiAdapter((self.context, self.request), name=u'plone_context_state')
            self.manageUrl =  '%s/%s' % (context_state.view_url(), self.manage_view)

            ## This is the way it's done in plone.app.portlets.manager, so we'll do the same
            mt = getToolByName(self.context, 'portal_membership')
            self.canManagePortlets = mt.checkPermission('Portlets: Manage portlets', self.context)

        def showPortlets(self):
            return '@@manage-portlets' not in self.request.get('URL')

        def portletManagersToShow(self):
            visibleManagers = []

            for n in range(1,self.portlet_count):
                name = '%s%s' % (self.name, n)

                try:
                    mgr = getUtility(IPortletManager, name=name, context=self.context)
                except:
                    # In the case we have problems to load portlet manager, do something about it
                    # This is graceful fallback in a situation where 1) add-on is already installed
                    # 2) new portlet code drops in and re-run add-on installer is
                    continue

                if mgr(self.context, self.request, self).visible:
                    visibleManagers.append(name)

            managers = []
            numManagers = len(visibleManagers)
            for counter, name in enumerate(visibleManagers):
                pos = 'position-%s' % str(Fraction(counter, numManagers)).replace('/',':')
                width = 'width-%s' % (str(Fraction(1, numManagers)).replace('/',':') if numManagers >1 else 'full')
                managers.append((name, 'cell %s %s %s' % (name.split('.')[-1], width, pos)))
            return managers


    class ColophonPortlets(CustomPortletViewlet):
        """
        Render a new series of portlets in colophon.
        """

        # This name is used to store portlets,
        # as referred in portlets.xml
        name = 'PortletsColophon'

        # This is custom management URL view for this,
        # registered thru ZCML to point to Products.ContentWellContent manager view class.
        manage_view = '@@manage-portlets-colophon'

        grok.viewletmanager(IPortalFooter)
        grok.template("portlets-colophon")

    # Define a portlet manager declaration
    from Products.ContentWellPortlets.browser.interfaces import IContentWellPortletManager

    class IColphonPortlets(IContentWellPortletManager):
         """
         This viewlet is a place holder to match portlets.xml and portlet management view together.

         * Manager is referred by name in manage page template

         * portlets.xml refers to this interface

         * provider:ColophonPortlets expression is also used in template to render the actual porlets
         """

Example ZCML bit

.. code-block:: xml

  <!-- Register new portlet management view for our portlet manager -->


  <include package ="plone.app.portlets" />

  <!--

      The .pt file is customized for the portlet manager name (from portlets.xml)
      and management link.

    -->
  <browser:page
     name="manage-portlets-colophon"
     for="plone.portlets.interfaces.ILocalPortletAssignable"
     class="plone.app.portlets.browser.manage.ManageContextualPortlets"
     template="templates/manage-portlets-colophon.pt"
     permission="plone.app.portlets.ManagePortlets"
  />


The page template for the manager ``manage-portlets-colophon.pt`` is the following

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          metal:use-macro="context/main_template/macros/master"
          >

        <head>
            <div metal:fill-slot="javascript_head_slot" tal:omit-tag="">
                <script type="text/javascript"
                    tal:attributes="src string:${context/absolute_url}/++resource++manage-portlets.js">
            </div>
        </head>
        <body class="manage-portlet-well">

            <metal:block fill-slot="top_slot"
                             tal:define="disable_column_one python:request.set('disable_plone.leftcolumn',1);
                                         disable_column_two python:request.set('disable_plone.rightcolumn',1);" />

            <div metal:fill-slot="main">

                <tal:warning tal:condition="plone_view/isDefaultPageInFolder">
                    <dl class="portalMessage warning">
                        <dt i18n:translate="message_warning_above_content_area_dt">Is this really where you want to add portlets above the content?</dt>
                        <dd i18n:translate="message_warning_above_content_area_dd">If you add portlets here, they will only appear on this item. If instead you want portlets to appear on all items in this folder,
                            <a href=""
                               tal:attributes="href string:${plone_view/getCurrentFolderUrl}/@@manage-portlets-colophon"
                               i18n:name="manage-portletsinheader_link">
                                <span i18n:translate="add_them_to_the_folder_itself">add them to the folder itself</span>
                            </a>
                        </dd>
                    <dl>
                </tal:warning>

                <h1 class="documentFirstHeading"
                    i18n:translate="manage_portlets_in_header">Manage portlets in colophon
                </h1>

                <p>
                     <a href=""
                           class="link-parent"
                           tal:attributes="href string:${context/absolute_url}"
                           i18n:translate="return_to_view">
                        Return
                     </a>
                </p>

                <div class="porlet-well_manager">
                    <h2 i18n:translate="portlet-well-a">Colophon Portlet Well 1</h2>
                    <span tal:replace="structure provider:PortletsColophon1" />
                </div>

                <div class="porlet-well_manager">
                    <h2 i18n:translate="portlet-well-a">Colophon Portlet Well 2</h2>
                    <span tal:replace="structure provider:PortletsColophon2" />
                </div>

                <div class="porlet-well_manager">
                    <h2 i18n:translate="portlet-well-a">Colophon Portlet Well 3</h2>
                    <span tal:replace="structure provider:PortletsColophon3" />
                </div>

                <div class="porlet-well_manager">
                    <h2 i18n:translate="portlet-well-a">Colophon Portlet Well 4</h2>
                    <span tal:replace="structure provider:PortletsColophon4" />
                </div>

                <div class="porlet-well_manager">
                    <h2 i18n:translate="portlet-well-a">Colophon Portlet Well 5</h2>
                    <span tal:replace="structure provider:PortletsColophon5" />
                </div>


            </div>

        </body>
    </html>

Then we have ``portlets-colophon.pt`` page template for the viewlet which renders
the portlets and related management link

.. code-block :: html

    <div id="portlets-colophon"
         class="row">

        <tal:block tal:condition="viewlet/showPortlets">
            <tal:portletmanagers tal:repeat="manager viewlet/portletManagersToShow">
                <div tal:attributes="class python:manager[1]"
                     tal:define="mgr python:manager[0]"
                     tal:content="structure provider:${mgr}" />

            </tal:portletmanagers>

            <div style="clear:both"><!-- --></div>

            <div class="manage-portlets-link"
               tal:condition="viewlet/canManagePortlets">
                <a href=""
                   class="managePortletsFallback"
                   tal:attributes="href viewlet/manageUrl">
                   Add, edit or remove a portlet in <b tal:content="viewlet/name" />
                </a>
            </div>

        </tal:block>

    </div>

Finally there is ``portlets.xml`` which lists all the portlet managers
and associates them with the used interface

.. code-block:: xml

    <?xml version="1.0"?>
    <!-- Set up all the new portlet managers we need above and below the content well -->
    <portlets>


        <portletmanager
             name="PortletsColophon1"
             type="youraddon.viewlets.IColphonPortlets"
        />

        <portletmanager
             name="PortletsColophon2"
             type="youraddon.viewlets.IColphonPortlets"
        />

        <portletmanager
             name="PortletsColophon3"
             type="youraddon.viewlets.IColphonPortlets"
        />

        <portletmanager
             name="PortletsColophon4"
             type="youraddon.viewlets.IColphonPortlets"
        />

        <portletmanager
             name="PortletsColophon5"
             type="youraddon.viewlets.IColphonPortlets"
        />

    </portlets>


More info

* https://weblion.psu.edu/svn/weblion/weblion/Products.ContentWellPortlets/trunk/Products/ContentWellPortlets/

* http://stackoverflow.com/questions/9766744/dynamic-tal-provider-expressions

Fixing relative links for static text portlets
-------------------------------------------------

.. note::

    This should be no longer issue with Plone 4.1 and TinyMCE 1.3+ when using UID
    links.

Example how to convert links in all static text portlets::

    from lxml import etree
    from StringIO import StringIO
    import urlparse
    from lxml import html

    def fix_links(content, absolute_prefix):
        """
        Rewrite relative links to be absolute links based on certain URL.

        @param html: HTML snippet as a string
        """

        parser = etree.HTMLParser()

        content = content.strip()

        tree  = html.fragment_fromstring(content, create_parent=True)

        def join(base, url):
            """
            Join relative URL
            """
            if not (url.startswith("/") or "://" in url):
                return urlparse.urljoin(base, url)
            else:
                # Already absolute
                return url

        for node in tree.xpath('//*[@src]'):
            url = node.get('src')
            url = join(absolute_prefix, url)
            node.set('src', url)
        for node in tree.xpath('//*[@href]'):
            href = node.get('href')
            url = join(absolute_prefix, href)
            node.set('href', url)

        data =  etree.tostring(tree, pretty_print=False, encoding="utf-8")

        return data

Other resources and examples
-----------------------------

* `Static text portlet <https://github.com/plone/plone.portlet.static/blob/master/plone/portlet/static/>`_.

* `Templated portlet <https://github.com/collective/collective.easytemplate/blob/master/collective/easytemplate/browser/portlets/templated.py>`_
