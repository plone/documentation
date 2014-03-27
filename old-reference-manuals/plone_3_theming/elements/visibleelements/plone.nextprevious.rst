Next Previous
=============

Provides next/previous functionality for a folder.

Notes:
    Turn this on per folder using Edit > Settings.
Snippet:
    ``<div class="listingBar">…</div>``
CSS:
    public.css
Name:
    plone.nextprevious
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.nextprevious

Customizing in your own product
-------------------------------

The following details will help you locate the files that you will need
to copy into your own product. They will also help you to provide the
correct information to create your own zcml directives, Python classes,
and interfaces.See
`viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_
for more information.

Located in:

    -  [your egg location]/plone/app/layout/nextprevious/
    -  [your egg
       location]/plone.app.layout-[version].egg/plone/app/layout/nextprevious/

Template Name:
    nextprevious.pt
Class Name:
    plone.app.layout.nextprevious.view.NextPreviousViewlet
Manager:
    plone.belowcontent (name)
    plone.app.layout.viewlets.interfaces.IBelowContent (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of nextprevious.pt in [your theme
package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.nextprevious.view import NextPreviousViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](NextPreviousViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IBelowContent"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.belowcontent" skinname="[your skin name]">
            <viewlet name="plone.nextprevious" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.belowcontent" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

