Comments
========

Supplies the commenting interface.

Notes:
    Comments can be turned on or off

    -  through the web: on an individual item (Edit > Settings > Allow
       Comments ) or Site Setup > Types (site-wide per type)
    -  in your product: profiles/default/types (per type)

Snippet:
    ``<div class="discussion"> … </div>``
CSS:
    public.css
Name:
    plone.comments
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.comments

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
    comments.pt
Class Name:
    plone.app.layout.viewlets.comments.CommentsViewlet
Manager:
    plone.belowcontent (name)
    plone.app.layout.viewlets.interfaces.IBelowContent (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of comments.pt in [your theme package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.comments import CommentsViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](CommentsViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IBelowContent"
        class=".[your module].[your class name]"
        for="Products.CMFCore.interfaces.IContentish"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.belowcontent" skinname="[your skin name]">
            <viewlet name="plone.comments" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.belowcontent" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

