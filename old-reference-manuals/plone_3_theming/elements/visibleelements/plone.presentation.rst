Presentation
============

Provides a link to a presentation view of a document.

Notes:
    Only available for a document. The link to a presentation view can
    be turned on or off

    -  through the web: on an individual item (Edit > Settings >
       Presentation ) or Site Setup > Types (site-wide per type)
    -  in your product: profiles/default/types (per type)

Snippet:
    ``<p id="link-presentation">...</p>``
CSS:
    none
Name:
    plone.presentation
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.presentation

Customizing in your own product
-------------------------------

The following details will help you locate the files that you will need
to copy into your own product. They will also help you to provide the
correct information to create your own zcml directives, Python classes,
and interfaces.See
`viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_
for more information.

Located in:

    -  [your egg location]/plone/app/layout/presentation/
    -  [your egg
       location]/plone.app.layout-[version].egg/plone/app/layout/presentation/

Template Name:
    none
Class Name:
    plone.app.presentation.PresentationViewlet
Manager:
    plone.abovecontentbody (name)
    plone.app.layout.viewlets.interfaces.IAboveContentBody (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.presentation import PresentationViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class [your class name](PresentationViewlet):
        [your code here]

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
            <viewlet name="plone.presentation" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.abovecontentbody" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

