HTML Head Title
===============

The page title in the HTML head.

Snippet:
    ``<title> ...</title>``
CSS:
    none
Name:
    plone.htmlhead.title
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.htmlhead.title

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
    none
Class Name:
    plone.app.layout.viewlets.common.TitleViewlet
Manager:
    plone.htmlhead (name)
    plone.app.layout.viewlets.interfaces.IHtmlHead (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.layout.viewlets.common import TitleViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class [your class name](TitleViewlet):
        [your code here]

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IHtmlHead"
        class=".[your module].[your class name]"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.htmlhead" skinname="[your skin name]">
            <viewlet name="plone.htmlhead.title" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.htmlhead" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

