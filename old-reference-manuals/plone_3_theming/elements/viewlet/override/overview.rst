Override viewlet
========================

A quick cheat sheet on how to customize or create a new viewlet.

You can customize a viewlet template through the web, but you can't
alter the underlying Python class.

On the file system, rather than customize, the process is to wire up a
new viewlet, or re-wire an existing viewlet.

You'll find a detailed tutorial on creating a viewlet in `this
article <http://plone.org/documentation/kb/customizing-main-template-viewlets/adding-a-viewlet/>`_.

Quick Cheat Sheet
-----------------

Through the Web
~~~~~~~~~~~~~~~

-  Use Site Setup > Zope Management Interfaces >
   portal\_view\_customizations to customize the template of an existing
   Plone Default viewlet.
-  You cannot create a new viewlet through the web.

In your own product
~~~~~~~~~~~~~~~~~~~

You will need to know the name of:

1. The viewlet manager interface
    Look this up in the Elements section of this manual
2. Your theme specific interface
    This is optional, but ensures that your viewlet is only available
    for your theme. If you used the plone3\_theme paster template, then
    the name will probably be IThemeSpecific.

You will need to create the following (you should be able to locate the
originals to copy by looking at the Elements section or by using
`GloWorm <http://plone.org/documentation/products/gloworm>`_):

3. browser viewlet directive
    This will go in [your theme package]/browser/configure.zcml
4. configuration file
    [your theme package]/profiles/default/viewlets.xml

5. page template
    [your theme package]/browser/[your template name].pt 
6. Python class
    This is optional (but see the note below for Plone version 3.1.2 or
    lower)
    put this in [your theme package]/browser/[your module].py

Sample configuration.zcml directives
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Re-wiring a Plone Default viewlet to use your own template (note the
layer attribute is really important here)

::

    <browser:viewlet
     name="plone.[viewlet name]"
     manager="[viewlet manager interface]"
     class="plone.app.layout.viewlets.common.[viewlet class name]"
     template="templates/[your template name]"
     layer="[your theme specific interface]"
     permission="zope2.View"
     />

Wiring up a new viewlet but borrowing a Plone Default viewlet class

::

    <browser:viewlet
     name=[your namespace].[your viewlet name]"
     manager="[viewlet manager interface]"
     class="plone.app.layout.viewlets.common.[viewlet class name]"
     template="templates/[your template name]"
     layer="[your theme specific interface]"
     permission="zope2.View"
     />

Wiring up with a brand new viewlet with your own class or your own
template

::

    <browser:viewlet
     name=[your namespace].[your viewlet name]"
     manager="[viewlet manager interface]"
     class=".[your module].[your class name]"
     (or: template="templates/[your template name]")
     layer="[your theme specific interface]"
     permission="zope2.View"
     />

Notes for Plone version 3.1.2 or lower:
---------------------------------------

Sample Python class
~~~~~~~~~~~~~~~~~~~

In Plone version 3.1.2 or lower, you will need to use this to override a
Plone Default viewlet, even if you only want to change the page
template.

::

    from [element namespace] import [element class name]
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFileclass

    [your class name]([element class name]):
        render = ViewPageTemplateFile("[your template name]")


