Anatomy of a Viewlet Manager
============================

The bits that go to make up a Viewlet Manager.

Directive in ZCML
-----------------

<browser:viewletManager />

Attributes in ZCML
------------------

name
    e.g., [your namespace].[your viewlet manager name]
provides
    a marker interface defining what this manager does
layer
    a marker interface for your particular theme
class
    this will be plone.app.viewletmanager.manager.OrderedViewletManager
permission
    in most cases this will be Zope.Public
for
    specify an interface marking a group of content types, if you wish.
    The viewlet manager will then be restricted to those content types
view
    specify an interface marking a view, if you wish. The viewlet
    manager will be restricted to items with those views.

