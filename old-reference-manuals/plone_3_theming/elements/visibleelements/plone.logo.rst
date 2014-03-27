Logo
====

The site logo.

Snippet:
    ``<a id="portal-logo" ...>... </a>``
CSS:
    public.css
Name:
    plone.logo
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.logo
Further information:
    `http://plone.org/documentation/kb/where-is-what/the-logo <http://plone.org/documentation/kb/where-is-what/the-logo>`_
    See also the Quick Start Section of this manual.

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
    logo.pt
Class Name:
    plone.app.layout.viewlets.common.LogoViewlet
Manager:
    plone.portalheader (name)
    plone.app.layout.viewlets.interfaces.IPortalHeader (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of logo.pt in [your theme package]/browser/templates)

Modify the logo.pt to suit your needs. For example, if you want to use
an image named something other than logo.jpg, you could use this code
and style #header in your mytheme.css file.

::

    <a metal:define-macro="portal_logo"
       id="portal-logo"
       accesskey="1"
       tal:attributes="href view/navigation_root_url"
       i18n:domain="plone">
        <!-- <img src="logo.jpg" alt=""
             tal:replace="structure view/logo_tag" /> --> <!--commenting out the code that normally looks for logo.jpg -->
        <div id="banner"><!-- style this div in your mytheme.css --></div></a>

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.common import LogoViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](LogoViewlet):
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
            <viewlet name="plone.logo" />
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
