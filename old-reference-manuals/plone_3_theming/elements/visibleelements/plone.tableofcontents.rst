Table of Contents
=================

Provides a set of bookmarks for the current page.

Notes:
    Turned on per content item through Edit > Settings.
Snippet:
    ``<dl id="document-toc" class="portlet toc"    style="display: none"> … </dl>``
CSS:
    portlets.css
Name:
    plone.tableofcontents
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.tableofcontents

Customizing in your own product
-------------------------------

The following details will help you locate the files that you will need
to copy into your own product. They will also help you to provide the
correct information to create your own zcml directives, Python classes,
and interfaces.See
`viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_
for more information.

Located in:

    -  [your egg location]/plone/app/layout/viewlets/
    -  [your egg
       location]/plone.app.layout-[version].egg/plone/app/layout/viewlets/

Template Name:
    toc.pt
Class Name:
    plone.app.layout.viewlets.common.TableOfContentsViewlet
Manager:
    plone.abovecontentbody (name)
    plone.app.layout.viewlets.interfaces.IAboveContentBody (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of toc.pt in [your theme package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.common import TableOfContentsViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](TableOfContentsViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IAboveContentBody"
        class=".[your module].[your class name]"
        for="Products.ATContentTypes.interface.IATDocument"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.abovecontentbody" skinname="[your skin name]">
            <viewlet name="plone.tableofcontents" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.abovecontentbody" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

