=============================
Tutorial: Overriding Viewlets
=============================

This tutorial [1]_ describes two simple examples of overriding viewlets. To learn more about views and viewlets, see the Developer Manual section on `Views and Viewlets`_


Overriding the Logo
-------------------

In this example, we override the logo for the site. I assume you have a theme product named my.theme with an IThemeSpecific interface.

#. Create an entry in browser/configure.zcml of your theme to override the viewlet.::

    <browser:viewlet
        name="plone.logo"
        manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
        class="plone.app.layout.viewlets.common.LogoViewlet"
        template="logo.pt"
        layer=".interfaces.IThemeSpecific"
        permission="zope2.View"
        />

#. Create a template file named logo.pt inside the browser directory that displays your logo image. It could contain something as simple as this.::

    <div>
        <a metal:define-macro="portal_logo"
           accesskey="1"
           tal:attributes="href view/navigation_root_url"
           i18n:domain="plone">
            <img src="" tal:attributes="src string:${context/portal_url}/++resource++my.theme.images/my_logo.png" alt="some alternative text" /></a>
    </div>

#. Add your logo image to the browser/images directory of your theme. In this example, ++resource++my.theme.images/my_logo.png points to a file named my_logo.png inside the theme's browser/images resource directory.


Overriding the Title
--------------------

In this example we override the view class associated with the title viewlet. I assume you have a theme product with an IThemeSpecific interface.

#. Create an entry in browser/configure.zcml of your theme to override the view class.::

    <browser:viewlet
        name="plone.htmlhead.title"
        manager="plone.app.layout.viewlets.interfaces.IHtmlHead"
        class=".common.TitleViewlet"
        layer=".interfaces.IThemeSpecific"
        permission="zope2.View"
        />

#. Create a class named TitleViewlet inside browser/common.py of your theme containing code to return the appropriate title.::

    class TitleViewlet(ViewletBase):

        def update(self):
            # do any setup you need

        def index(self):
            ...
            return the appropriate title


Discussion
----------

Overriding the logo
^^^^^^^^^^^^^^^^^^^

To override a viewlet in Plone, you need to know which viewlet to override. Using @@manage-viewlets is helpful here. It shows you all the viewlet managers on a page and the viewlets they contain.

You can add /@@manage-viewlets to any url in your site and see the active viewlets there. Something like::

    http://localhost:8080/Plone/@@manage-viewlets

Using this shows us that the logo is in the plone.logo Viewlet within the plone.portalheader ViewletManager

    .. image:: manage_viewlets.png

Viewlets are defined in the plone/app/layout/viewlets/configure.zcml file within the eggs area of your buildout. Looking inside that configure.zcml file we see::

    <!-- The logo -->
    <browser:viewlet
        name="plone.logo"
        manager=".interfaces.IPortalHeader"
        class=".common.LogoViewlet"
        permission="zope2.View"
        />

Here's our overriding entry from above to compare::

    <browser:viewlet
        name="plone.logo"
        manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
        class="plone.app.layout.viewlets.common.LogoViewlet"
        template="templates/logo.pt"
        layer=".interfaces.IThemeSpecific"
        permission="zope2.View"
        />

The name is the same as the item we are overriding. Notice that we give the full path to the manager, and that we are reusing the class. We also declare the name and location of our overriding template file, use our theme's interface, and set a permission.


Overriding the title
^^^^^^^^^^^^^^^^^^^^

Here is TitleViewlet from plone.app.layout. It has the page title on the left and the portal title on the right, with an emdash in between.::

    class TitleViewlet(ViewletBase):
        index = ViewPageTemplateFile('title.pt')

        def update(self):
            portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
            context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
            page_title = escape(safe_unicode(context_state.object_title()))
            portal_title = escape(safe_unicode(portal_state.navigation_root_title()))
            if page_title == portal_title:
                self.site_title = portal_title
            else:
                self.site_title = u"%s &mdash; %s" % (page_title, portal_title)

Here is an example for comparison that switches page title and portal title, and separates them with a pipe. The only differences are on the last line.::

    class TitleViewlet(ViewletBase):
        index = ViewPageTemplateFile('title.pt')

        def update(self):
            portal_state = getMultiAdapter((self.context, self.request),
                                            name=u'plone_portal_state')
            context_state = getMultiAdapter((self.context, self.request),
                                             name=u'plone_context_state')
            page_title = escape(safe_unicode(context_state.object_title()))
            portal_title = escape(safe_unicode(portal_state.navigation_root_title()))
            if page_title == portal_title:
                self.site_title = portal_title
            else:
                self.site_title = u"%s | %s" % (portal_title, page_title)

More information about the title tag can be found at the `HTML Head Title`_ page which is part of the `Plone Theme Reference`_.


.. [1] https://plone.org/author/spanky
.. _Views and Viewlets: http://docs.plone.org/5/en/develop/plone/views/viewlets.html
.. _HTML Head Title: https://plone.org/documentation/manual/theme-reference/elements/hiddenelements/plone.htmlhead.title
.. _Plone Theme Reference: http://docs.plone.org/5/en/adapt-and-extend/theming/index.html
