Byline
======

The 'about' information (who created a content item and when it was
modified).

Notes:
    You can turn off the Byline for anonymous viewers

    -  through the web: Site Setup > Security
    -  In your product: profiles/default/propertiestool.xml

Snippet:
    ``<div id="plone-document-byline" class="documentByLine">...  </div>``
CSS:
    public.css
Name:
    plone.belowcontenttitle.documentbyline
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.belowcontenttitle.documentbyline

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
    document\_byline.pt
Class Name:
    plone.app.layout.viewlets.content.DocumentBylineViewlet
Manager:
    plone.belowcontenttitle (name)
    plone.app.layout.viewlets.interfaces.IBelowContentTitle (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of document\_byline.pt in [your theme
package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.content import DocumentBylineViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](DocumentBylineViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IBelowContentTitle"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.belowcontenttitle" skinname="[your skin name]">
            <viewlet name="plone.belowcontenttitle.documentbyline" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.belowcontenttitle" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

