Keywords
========

The categories (a.k.a. keywords / tags / labels) that have been assigned
to the item.

Notes:
    This will only appear if some categories have been assigned using
    Edit > Categories.
Snippet:
    ``<div id="category" class="documentByLine">…</div>``
CSS:
    public.css
Name:
    plone.belowcontenttitle.keywords
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.belowcontenttitle.keywords

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
    keywords.pt
Class Name:
    none
Manager:
    plone.belowcontenttitle (name)
    plone.app.layout.viewlets.interfaces.IBelowContentTitle (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of keywords.pt in [your theme package]/browser/templates)

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
        template="templates/[your template name].pt"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.belowcontenttitle" skinname="[your skin name]">
            <viewlet name="plone.belowcontenttitle.keywords" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.belowcontenttitle" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

