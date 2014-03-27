Lock
====

Indicates that the content item is locked for editing.

Snippet:
    ``<div id="plone-lock-status" />``
CSS:
    public.css
Name:
    plone.lockinfo
Type:
    `viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_

Use:
    Site Setup > Zope Management Interface >
    portal\_view\_customizations
Go to:
    plone.lockinfo

Customizing in your own product
-------------------------------

The following details will help you locate the files that you will need
to copy into your own product. They will also help you to provide the
correct information to create your own zcml directives, Python classes,
and interfaces.See
`viewlet <http://plone.org/documentation/manual/theme-reference/elements/elements/viewlet>`_
for more information.

Located in:

    -  [your egg location]/plone/locking/browser/
    -  [your egg
       location]/plone.locking-[version].egg/plone/locking/browser/

Template Name:
    info.pt
Class Name:
    plone.locking.browser.info.LockInfoViewlet
Manager:
    plone.abovecontent (name)
    plone.app.layout.viewlets.interfaces.IAboveContent (interface)

Sample files & directives
~~~~~~~~~~~~~~~~~~~~~~~~~

Put a version of info.pt in [your theme package]/browser/templates)

Create your own version of the class in [your theme
package]/browser/[your module].py

::

    from plone.locking.browser.info import LockInfoViewlet
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
    class [your class name](LockInfoViewlet):
        render = ViewPageTemplateFile("[your template name]")

Wire up your viewlet in [your theme package]/browser/configure.zcml

::

    <browser:viewlet
        name="[your namespace].[your viewlet name]"
        manager="plone.app.layout.viewlets.interfaces.IAboveContent"
        class=".[your module].[your class name]"
        for="plone.locking.interfaces.ITTWLockable"
        layer=".interfaces.[your theme specific interface]"
        permission="zope2.View"
    />

In [your theme package]/profiles/default/viewlets.xml

Hide the original viewlet (if you wish)

::

    <object>
        <hidden manager="plone.abovecontent" skinname="[your skin name]">
            <viewlet name="plone.lockinfo" />
        </hidden>

Insert your new viewlet in a viewlet manager

::

        <order manager="plone.abovecontent" skinname="[your skin name]"
               based-on="Plone Default">
            <viewlet name="[your namespace].[your viewlet name]"
                     insert-before="*" />
        </order>
    </object>

