RSS Link
========

The RSS link in the HTML head.

Snippet:
    ``<link rel="alternate" title="RSS 1.0" ... />``
CSS:
    none
Name:
    plone.links.RSS
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.links.RSS

Customizing in your own product
-------------------------------

The following details will help you locate the files that you will need
to copy into your own product. They will also help you to provide the
correct information to create your own zcml directives, Python classes,
and interfaces.See
`viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_
for more information.

Located in:

    -  [your egg location]/plone/app/layout/links/
    -  [your egg
       location]/plone.app.layout-[version].egg/plone/app/layout/links/

Template Name:
    rsslink.pt
Class Name:
    plone.app.layout.links.viewlets.RSSViewlet
Manager:
    plone.htmlhead.links (name)
    plone.app.layout.viewlets.interfaces.IHtmlHeadLinks (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of navigation.pt in [your theme
package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.links.viewlets import RSSViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](RSSViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IHtmlHeadLinks"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.htmlhead.links" skinname="[your skin name]">
            <viewlet name="plone.links.RSS" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.htmlhead.links" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

