Related Items
=============

Items related to the content

Notes:
    This viewlet displays links to additional content items selected by
    the editor under the categorization tab.
Snippet:
    ``<div class="relatedItems"> … </div>``
CSS:
    public.css
Name:
    plone.belowcontentbody.relateditems
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.belowcontentbody.relateditems

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
    document\_relateditems.pt
Class Name:
    plone.app.layout.viewlets.content.ContentRelatedItems
Manager:
    plone.belowcontentbody (name)
    plone.app.layout.viewlets.interfaces.IBelowContentBody (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of document\_relateditems.pt in [your theme
package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.content import ContentRelatedItems
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](ContentRelatedItems):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IBelowContentBody"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.belowcontentbody" skinname="[your skin name]">
            <viewlet name="plone.belowcontentbody.relateditems" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.belowcontentbody" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

'
