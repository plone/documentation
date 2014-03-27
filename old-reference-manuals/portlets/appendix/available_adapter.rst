===========================================================
How to make portlets availability configurable via adapters
===========================================================

.. admonition:: Description

         Sometimes you may want to make specific portlets available only on
         some pages, like the portal root. This describes, how to implement
         such a functionality for custom portlets.

.. contents :: :local:

The interface IPortletRenderer in plone.portlets.interfaces specifies an
available property, which is used to decide if an portlet should be shown or
not. The Renderer class in plone.app.portlets.base, from which most Renderer
classes derive, implements the available property which always returns True.
You can override this property in you own Renderer class. And if you use the
adapter pattern to calculate the available property, it gets configurable also
outside the package, your portlet is defined in.


1) Define a default adapter including the adapter interface

   .. code-block:: python
   
      from zope.interface import implementer
      from zope.interface import Interface, Attribute
   
      class IPortletAvailable(Interface):
          """ Interface for Adapters, implementing logic to determine, if the
              Portlet should be shown or not.
          """
          portlet = Attribute(u"""The portlet assignment""")
          manager = Attribute(u"""The portlet manager""")
          context = Attribute(u"""The context, this portlet is shown""")
   
      @implementer(IPortletAvailable)
      def portlet_default_available(portlet, manager, context):
          return True


2) Register the adapter with zcml. The default adapter is registered as
   multiadapter to a portlet assignment, a portlet manager and a generic
   context. The portlet assignment specifies for which portlet type the adapter
   is registered (in this case IMyPortlet). The portlet manager adapted in this
   example is IPortletManager - the most generic one which includes IDashBoard,
   ILeftColumn and IRightColumn. The context in this example is also very
   generic - any content which can display portlets.

   .. code-block:: xml

       <adapter
           factory=".portlet.portlet_default_available"
           for="MY.PACKAGE.portlet.IMyPortlet
                plone.portlets.interfaces.IPortletManager
                plone.portlets.interfaces.ILocalPortletAssignable" />


3) Use the adapter in your custom portlet:

   .. code-block:: python
   
      from Acquisition import aq_inner, aq_base
      from zope.component import getMultiAdapter, queryMultiAdapter
   
      class PortletRenderer(base.Renderer):
          ...
   
          @property
          def available(self):
              context = aq_inner(self.context)
              assignment = aq_base(self.data)
              # first try to get a named multi adapter, then an unnamed
              available = queryMultiAdapter(
                  (assignment, self.manager, context),
                  IPortletAvailable, name=assignment.id,
                  default=getMultiAdapter(
                      (assignment, self.manager, context),
                      IPortletAvailable))
              return available


   The first adapter lookup is a named one. So it's possible to register an
   adapter for one specific portlet only, whereas the second adapter lookup
   can apply to more than one portlet.
    
   The default adapter registered above always returns True. But we can override
   this behavior in another package, e.g. an Pone integration package (call it
   "policy product").


4) Define custom adapters:

   .. code-block:: python
   
      from MY.PACKAGE.portlet import IPortletAvailable
      from zope.interface import implementer
   
      @implementer(IPortletAvailable)
      def portlet_disabled(portlet, manager, context):
          # also some fancy logic can be implemented here
          return False
   
      @implementer(IPortletAvailable)
      def portlet_enabled(portlet, manager, context):
          return True


5) Register the adapters:

   .. code-block:: xml
   
      <adapter
          factory=".portlet_adapters.portlet_enabled"
          for="MY.PACKAGE.portlet.IMyPortlet
               plone.app.portlets.interfaces.ILeftColumn
               Products.CMFPlone.interfaces.siteroot.IPloneSiteRoot" />
   
      <adapter
          factory=".portlet_adapters.portlet_disabled"
          for="MY.PACKAGE.portlet.IMyPortlet
               plone.app.portlets.interfaces.ILeftColumn
               plone.portlets.interfaces.ILocalPortletAssignable" />
   
      <adapter
          factory=".portlet_adapters.main_teaser_available"
          for="MY.PACKAGE.portlet.IMyPortlet
               plone.app.portlets.interfaces.IRightColumn
               plone.portlets.interfaces.ILocalPortletAssignable" />
   
      <adapter
          factory=".portlet_adapters.portlet_disabled"
          for="MY.PACKAGE.portlet.IMyPortlet
               plone.app.portlets.interfaces.IRightColumn
               Products.CMFPlone.interfaces.siteroot.IPloneSiteRoot" />


   Here, if the portlet is registered on ILeftColumn and IRightColumn, it is only
   shown on ILeftColumn, if the context is the portal root. Otherwise, it's shown
   on IRightColumn.
