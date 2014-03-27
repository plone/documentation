========================
Subclassing new portlets
========================

.. admonition:: Description

         This how-to briefly explains how to create new portlets
         based on another existing portlet class. (Mikko Ohtama)

.. contents :: :local:

.. highlight:: xml

Portlet subclassing is not trivial due to explict references
between portlet engine parts. Here are short instructions minimal
steps to needed to a subclass a portlet to another portlet. Instead
of modifying the existing portlet, we need to create a new
invariant with little changed properties.
`See this general briefing about Plone 3.x portlet mechanism. <http://martinaspeli.net/articles/an-introduction-to-plone-portlets>`_
This example modifies the render behavior of static text portlet,
by adding a grey backgroundd CSS class for it.


#. Create a portlet interface stub and portlets Python module: To
   define a new portlet. Refer this in your product ZCML.
#. Create a new assigment class: To make new portlet assignable
   through portlet manager
#. Create a new add form class: To make new portlet creatable,
   returning your custom portlet instances
#. Create a configure.xml ZCML entry: To make Zope to find the new
   portlet definition
#. Create a portlets.xml installer entry: To make the portlet
   appear in the portlet manager menu

The portlet interface class is fixed to a portlet when the portlet
is created. Thus, if you make changes any of above, you might need
to create a new portlet to see the effect - old portlet instances
don't necessarily see the changees.

Our portlet code lies in *myproduct/browser/portlets/misc.py*:

.. code-block:: python

    from zope.interface import implements
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    from plone.portlet.static import PloneMessageFactory as _
    
    # Import the base portlet module whose properties we will modify
    from plone.portlet.static import static
    
    class IGreyStaticPortlet(static.IStaticPortlet):
        """ Defines a new portlet "grey static" which takes properties of the existing static text portlet. """
        pass
    
    class GreyStaticRenderer(static.Renderer):
        """ Overrides static.pt in the rendering of the portlet. """
        render = ViewPageTemplateFile('grey_static.pt')
    
    class GreyStaticAssignment(static.Assignment):
        """ Assigner for grey static portlet. """
        implements(IGreyStaticPortlet)
    
    class GreyStaticAddForm(static.AddForm):
        """ Make sure that add form creates instances of our custom portlet instead of the base class portlet. """
        def create(self, data):
            return GreyStaticAssignment(**data)

*myproduct/browser/portlets/configure.zcml* snippet. Note that we
do not need to override all (EditForm) views:

::

    <configure xmlns="http://namespaces.zope.org/zope"
               xmlns:browser="http://namespaces.zope.org/browser"
               xmlns:plone="http://namespaces.plone.org/plone">
    
        <include package="plone.app.portlets" />
    
            <plone:portlet
            name="lsm.GreyStaticPortlet"
            interface=".misc.IGreyStaticPortlet"
             assignment=".misc.GreyStaticAssignment"
             view_permission="zope2.View"
             edit_permission="cmf.ManagePortal"
             renderer=".misc.GreyStaticRenderer"
             addview=".misc.GreyStaticAddForm"
             editview="plone.portlet.static.static.EditForm"
             />
    
    </configure>


*myproducts/profiles/default/portlets.xml* quick installer
snippet:

::

    <portlets>
    
      <portlet
        addview="lsm.GreyStaticPortlet"
        title="Static portlet (grey)"
        description="Portlet with light grey background"
        />
    
    </portlets>

*myproduct/browser/portlets/grey\_static.pt*. We have added one new
CSS class (portletGrey) which has a CSS class definition defined in
ploneCustom.css (through-the-web) or some of the product's CSS
files:

::

    <div tal:condition="view/data/omit_border"
         tal:attributes="class string:portletStaticText ${view/css_class}"
         tal:content="structure view/data/text" />
    <dl tal:condition="not:view/data/omit_border"
        tal:attributes="class string:portlet portletStaticText portletGrey ${view/css_class}"
        i18n:domain="plone">
    
        <dt class="portletHeader">
            <span class="portletTopLeft"></span>
            <span>
               <a tal:omit-tag="not:view/has_link"
                  tal:attributes="href view/data/more_url"
                  tal:content="view/data/header"
                  />
            </span>
            <span class="portletTopRight"></span>
        </dt>
    
        <dd class="portletItem odd">
            <div tal:replace="structure view/data/text" />
            <tal:corners condition="not:view/has_footer">
                <span class="portletBottomLeft"></span>
                <span class="portletBottomRight"></span>
            </tal:corners>
        </dd>
    
        <dd class="portletFooter" tal:condition="view/has_footer">
            <span class="portletBotomLeft"></span>
            <span>
               <a tal:omit-tag="not:view/has_link"
                  tal:attributes="href view/data/more_url"
                  tal:content="view/data/footer"
                  />
            </span>
            <span class="portletBottomRight"></span>
        </dd>
    
    </dl>

*myproduct/browser/portlets/\_\_init\_\_.py*. Create empty file to
a mark a Python module.

*myproduct/configure.zcml*. Add following snippet:

::

    <include package=".portlets" />
