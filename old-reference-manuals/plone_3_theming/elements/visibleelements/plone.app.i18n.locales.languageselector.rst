Language Selector
=================

Provides a drop down list to select a different language.

Snippet:
    ``<ul id="portal-languageselector"> … </ul>``
Name:
    plone.app.i18n.locales.languageselector
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.app.i18n.locales.languageselector

Customizing in your own product
-------------------------------

The following details will help you locate the files that you will need
to copy into your own product. They will also help you to provide the
correct information to create your own zcml directives, Python classes,
and interfaces.See
`viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_
for more information.

Located in:

    -  [your egg location]/plone/app/i18n/locales/browser/
    -  [your egg
       location]/plone.app.i18n-[version].egg/plone/app/i18n/locales/browser/

Template Name:
    languageselector.pt
Class Name:
    plone.app.i18n.locales.browser.selector.LanguageSelector
Manager:
    Portal Top (name)
    plone.app.layout.viewlets.interfaces.IPortalTop (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of languageselector.pt in [your theme
package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.app.i18n.locales.browser.selector import LanguageSelector
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](LanguageSelector):
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
        <hidden manager="Portal Top" skinname="[your skin name]">
            <viewlet name="plone.app.i18n.locales.languageselector" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="Portal Top" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

