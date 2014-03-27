Creating a New Viewlet Manager
==============================

A quick cheat sheet for creating a new viewlet manager.

Through the Web
~~~~~~~~~~~~~~~

You cannot create a new viewlet manager through the web. To override the
order in which viewlets appear in a viewlet manager, use the
instructions for viewlets.

In your own product
~~~~~~~~~~~~~~~~~~~

If you're basing your new viewlet manager on a Plone Default viewlet
manager, look up the details in the Elements section of this manual.

You will need to know the name of

Your theme specific interface
    This is optional, but ensures that your viewlet is only available
    for your theme. If you used the plone3\_theme paster template, then
    the name will probably be IThemeSpecific.

You will need to create the following (you should be able to locate the
originals to copy by looking them up in the elements section):

browser viewletManager directive
    [your theme package]/browser/configure.zcml
Your viewlet manager interface
    [your theme package]/browser/interfaces.py
configuration file directives
    [your theme package]/profiles/default/viewlets.xml

Sample Interface
~~~~~~~~~~~~~~~~

::

    from zope.viewlet.interfaces import IViewletManager

    class [your viewlet manager interface](IViewletManager):
        """ [A description of your viewlet manager goes here]  """

Sample configure.zcml directive
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    <browser:viewletManager
     name=[your namespace].[your element name]"
     provides=".interfaces.[your viewlet manager interface]"
     class="plone.app.viewletmanager.manager.OrderedViewletManager"
     layer="[your theme interface]"
     permission="zope2.View"
     />

