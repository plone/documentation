Creating a New Portlet Manager
==============================

How to create a new portlet manager.

A practical example of creating a new portlet manager can be found here

-  `http://plone.org/documentation/how-to/adding-portlet-managers <http://plone.org/documentation/how-to/adding-portlet-managers>`_

Here's a quick checklist of what you need to do.

Quick Cheat Sheet
-----------------

Through the Web
~~~~~~~~~~~~~~~

You cannot create a new portlet manager through the web.

In your own product
~~~~~~~~~~~~~~~~~~~

You will need to provide the name of

Your theme-specific interface
    This is optional but ensures that your portlet manager is available
    for your theme only. If you used the plone3\_theme paster template,
    then the name will probably be IThemeSpecific.

You will need to create the following (you should be able to locate the
originals to copy by looking them up in the elements section):

Interface
    This will go in [your theme package]/browser/interfaces.py. You can
    give it any name you like, but by convention, it should be prefaced
    with "I".
configuration directive
    [your theme package]/profiles/default/portlets.xml
browser:page directive (for the management view)
    [your theme package]/browser/configure.zcml
page template (for the management view)
    [your theme package]/browser/[your template].pt

Sample interface
~~~~~~~~~~~~~~~~

::

    from plone.portlets.interfaces import IPortletManager

    class [your portlet manager interface](IPortletManager):
     """A description goes here    """

Sample portlets.xml
~~~~~~~~~~~~~~~~~~~

::

    <?xml version="1.0"?>
    <portlets>
     <portletmanager
        name="[your namespace].[your portlet manager]"
        type="[your namespace].[your theme name].browser.interfaces.[your portlet manager interface]"
     />
    </portlets>

Sample configure.zcml directive (for the management view)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

::

    <browser:page
     for="plone.portlets.interfaces.ILocalPortletAssignable"
     class="plone.app.portlets.browser.manage.ManageContextualPortlets"
     name="[your view name]"
     template="[your template name].pt"
     permission="plone.app.portlets.ManagePortlets"
    />

