Anatomy of a Portlet
====================

The bits that go to make up a portlet renderer (which is the bit of a
portlet you'll want to customize).

Customizing a portlet is similar to overriding a viewlet, but rather
more straightforward. There is a specific ZCML directive for
customization.

Directive in ZCML
-----------------

<plone:portletRenderer />

Attributes in ZCML
------------------

layer
    a marker interface for your particular theme
portlet
    the interface of the portlet you wish to customize
template
    location of the template you wish to override
class
    your custom class (use this if you don't specify a template) for
    rendering the portlet

