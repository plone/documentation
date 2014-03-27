Adding Portlet Managers
=======================

You need portlets at an additional place in your Plone. In this example
we put contextual portlets above the content (contributed by Jens Klein)

    This is about adding Portlet MANAGERS, hint: **PortletManager !=
    Portlet.**\ A PortletManager is a kind of container for the
    portlets, like the ViewletManager is for Viewlets. So, after
    reducing the momentum of misunderstanding, lets start:

Prerequsites
------------

I assume you're familar with GenericSetup based setups for Plone 3. Take
a look at *DIYPloneStyle* and related tutorials if not.

You need Plone 3 installed and a Product NEWTHEME for your own skin
(based on DIYPloneStyle works fine).

Strategy
--------

In my example I don't want to customize the main-template. So the idea
is to add a viewlet to the
*plone.app.layout.viewlets.interfaces.IContentViews* viewletmanager. So
the steps need to be done is

#. Add a viewlet to the viewlet-manager
#. Add a portlet-manager
#. Add a management view for the portlet-manager.

Step One: Add a viewlet
-----------------------

in Products.NEWTHEME add a file *abovecontentportlets.pt* containing:

::

    <tal:block replace="structure provider:my.abovecontentportlets" />

Here we call the portlet manager, we create it in step two.
But first lets register our new viewlet for the viewletmanager.
Edit your Products/NEWTHEME/configure.zcml and add:

::

    <browser:viewlet
        name="my.abovecontentportlets"
        manager="plone.app.layout.viewlets.interfaces.IContentViews"
        template="abovecontentportlets.pt"
        permission="zope2.View" 
    /> 

Step Two: Add a portlet manager
-------------------------------

Create a marking interface for the manager and add or edit
*Products/NEWTHEME/interfaces.py*

::

    from plone.portlets.interfaces import IPortletManager

    class IMyAboveContent(IPortletManager):
        """we need our own portlet manager above the content area.
        """

Add (or edit) your *Products/NEWTHEME/profiles/default/portlets.xml* and
register a portlet manager:

::

    <?xml version="1.0"?>
    <portlets> 
     <portletmanager 
       name="my.abovecontentportlets"
       type="Products.NEWTHEME.interfaces.IMyAboveContent"
     />
    </portlets>

Thats all you need if you don't want to manage the portlets through the
web. Oh, you want to? So you need a third step:

Step Three: Add a management view for the portlet manager
---------------------------------------------------------

The management view is rendered for the left and right slots directly on
the main-template. But we use a viewlet and in here we have a different
view. so we need to call explicitly our view and call the our manager
within its context.

 

We need to register a new browser view for an own page template directly
calling our manager. Again add some lines to your *configure.zcml*:

::

    <browser:page
        for="plone.portlets.interfaces.ILocalPortletAssignable"
        class="plone.app.portlets.browser.manage.ManageContextualPortlets"
        name="manage-myabove"
        template="templates/managemyabove.pt"
        permission="plone.app.portlets.ManagePortlets"
    />

And finally we need the template, so add an file *managemyabove.pt* and
edit it:

 

::

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          metal:use-macro="context/main_template/macros/master"
          i18n:domain="plone">
    <head>
        <div metal:fill-slot="javascript_head_slot" tal:omit-tag="">
            <link type="text/css" rel="kinetic-stylesheet"
                tal:attributes="href string:${context/absolute_url}/++resource++manage-portlets.kss"/>
        </div>
    </head>
    <body>
    <div metal:fill-slot="main">
      <h1 class="documentFirstHeading">Manage My Portlets</h1>
      <span tal:replace="structure provider:my.abovecontentportlets" />
    </div>
    </body>
    </html>

That's it. After restarting your zope you can call
*http://DOMAIN.TLD/plone/path/to/some/context/@@manage-myabove*

and assign portlets over your content.

 
