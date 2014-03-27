Global Sections
===============

The top level sections of the site.

Notes:
    The sections are either auto-generated from top level content items
    or can be set up manually

    -  through the web: Site Setup > Navigation (for auto-generation)
       Site Setup > Zope Management Interface > portal\_tabs (for
       manually defined sections)
    -  in your product: profiles/default/actions.xml and
       propertiestool.xml

Snippet:
    ``<h5 class="hiddenStructure">Sections</h5> <ul id="portal-globalnav"> … </ul>``
CSS:
    public.css
Name:
    plone.global\_sections
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.global\_sections
Further information:
    `http://plone.org/documentation/kb/where-is-what/the-navigation-tabs <http://plone.org/documentation/kb/where-is-what/the-navigation-tabs>`_

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
    sections.pt
Class Name:
    plone.app.layout.viewlets.common.GlobalSectionsViewlet
Manager:
    plone.portalheader (name)
    plone.app.layout.viewlets.interfaces.IPortalHeader (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of sections.pt in [your theme package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.common import GlobalSectionsViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](GlobalSectionsViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.portalheader" skinname="[your skin name]">
            <viewlet name="plone.global_sections" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.portalheader" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

'
