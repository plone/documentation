Anatomy of a Viewlet
====================

The bits that go to make up a viewlet component.

Directive in ZCML
-----------------

<browser:viewlet />

Attributes in ZCML
------------------

name
    e.g. [your namespace].[your viewlet name]
manager
    a manager interface
layer
    a marker interface for your particular theme
class
    a Python class. This class requires a 'render' attribute, which, in
    most cases, will point to a template. You don't need to specify the
    template in the ZCML, however, in Plone version 3.1.3 and higher,
    you can override this template using the template attribute below
template
    in Plone version 3.1.2 and lower, you can only use this if you
    aren't using a class; in Plone version 3.1.3 and higher, you can use
    this to override the template you've set in the class you specified
    above
permission
    in most cases this will be Zope.Public
for
    specify an interface marking a group of content types, if you wish.
    The viewlet will then be restricted to those content types (for an
    example see the `Presentation
    viewlet <http://plone.org/documentation/manual/theme-reference/elements/visibleelements/plone.presentation>`_
    in the Elements section)
view
    specify an interface marking a specific browser view, if you wish.
    The viewlet will be restricted to items with that specific view (for
    an example investigate the source code of the Content Actions
    viewlet - you'll find directions on where to locate this code on the
    `Content
    Actions <http://plone.org/documentation/manual/theme-reference/elements/visibleelements/plone.contentactions>`_
    page of the Elements section)

