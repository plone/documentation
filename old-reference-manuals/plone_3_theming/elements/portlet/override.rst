Overriding a Portlet
====================

A quick cheat sheet of how to override or customize a portlet.

Through the Web
~~~~~~~~~~~~~~~

-  Use Site Setup > Zope Management Interfaces >
   portal\_view\_customizations to customize the template of an existing
   Plone Default portlet.

In your own product
~~~~~~~~~~~~~~~~~~~

There is a detailed tutorial available here:

-  `http://plone.org/documentation/how-to/override-the-portlets-in-plone-3.0/ <http://plone.org/documentation/how-to/override-the-portlets-in-plone-3.0/>`_

You can also look up the details of the portlet you want to override in
the Elements section of this manual.

Quick Cheat Sheet
~~~~~~~~~~~~~~~~~

You will need to know the name of

Your theme-specific interface
    This is optional but ensures that your portlet is only available for
    your theme. If you used the plone3\_theme paster template, then the
    name will probably be IThemeSpecific.

You will need to create the following (you should be able to locate the
originals to copy by looking them up in the Elements section):

plone portlet renderer directive
    [your theme package]/browser/configure.zcml
page template
    [your theme package]/browser/[your template name].pt
Python class \*
    [your theme package]/browser/[your module name].py

\* in most cases you won't need a Python class

Sample configuration.zcml directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    <configure 
        xmlns:plone="http://namespaces.plone.org/plone">
        <include package="plone.app.portlets"  />
        <plone:portletRenderer
           portlet="[element interface]"
           template="[your template name].pt"
          (or class=".[your module].[your class name]")
          layer="[your theme specific interface]"
         />
    </configure>

Sample Python class for navigation portlet override
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you want to customize the navigation portlet, you may need to supply
the class as well as the template. Two templates are involved: the first
is the usual display template; the second handles the recursion through
the navigation tree. If you need to make your own version of the second,
then you'll need to assign it to the recurse method in the class.

::

    from plone.app.portlets.portlets.navigation import Renderer
    from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

    class [your class name](Renderer):
        _template = ViewPageTemplateFile([your template name].pt)  
        recurse = ViewPageTemplateFile([your recurse template name])

