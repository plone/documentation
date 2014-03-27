Analytics
=========

Google analytics code snippet.

Notes:
    Provide the code snippet for your site through the web: Site Setup >
    Site settings
Snippet:
    ``(code snippet defined by the site manager)``
CSS:
    none
Name:
    plone.analytics
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.analytics

Customizing in your own product
-------------------------------

The following details will help you locate the files that you will need
to copy into your own product. They will also help you to provide the
correct information to create your own zcml directives, Python classes,
and interfaces.See
`viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_
for more information.

Located in:

    -  [your egg location]/plone/app/layout/analytics/
    -  [your egg
       location]/plone.app.layout-[version].egg/plone/app/layout/analytics/

Template Name:
    none
Class Name:
    plone.app.layout.analytics.view.AnalyticsViewlet
Manager:
    plone.portalfooter (name)
    plone.app.layout.viewlets.interfaces.IPortalFooter (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.analytics.view import AnalyticsViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class [your class name](AnalyticsViewlet):
        [your code here]

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IPortalFooter"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.portalfooter" skinname="[your skin name]">
            <viewlet name="plone.analytics" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.portalfooter" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

