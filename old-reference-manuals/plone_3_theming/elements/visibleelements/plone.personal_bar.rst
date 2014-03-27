Personal Bar
============

Provides the Log in link and further links for users once logged in.

Notes:
    You can reorder, add, or remove specific links in the personal bar

    -  through the web: Site Setup >Zope Management Interface >
       portal\_actions > user
    -  In your product: profiles/default/actions.xml

Snippet:
    ``<div id="portal-personaltools-wrapper"> …</div>``
CSS:
    public.css
Name:
    plone.personal\_bar
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.personal\_bar
Further information:
    `http://plone.org/documentation/kb/where-is-what/the-personal-bar <http://plone.org/documentation/kb/where-is-what/the-personal-bar'>`_

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
    personal\_bar.pt
Class Name:
    plone.app.layout.viewlets.common.PersonalBarViewlet
Manager:
    plone.portaltop (name)
    plone.app.layout.viewlets.interfaces.IPortalTop (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of personal\_bar.pt in [your theme
package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.common import PersonalBarViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](PersonalBarViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IPortalTop"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.portaltop" skinname="[your skin name]">
            <viewlet name="plone.personal_bar" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.portaltop" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

'
