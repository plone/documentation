=====================================================
How to update schemas for already registered portlets
=====================================================

.. admonition:: Description

         This describes how an Portlet schema can be updated for portlets,
         which are already registered in the Portal.

.. contents :: :local:

Note: David Glick suggested an really easy fix, so this one might become
obsolete:

    Add the new attribute as a class attribute of the portlet assignment class.
    e.g.

    class Assignment(base.Assignment):
        image_size = 42

    Then existing assignment instances which don't have that attribute will
    still get them from the class.

Once a portlet with a specific schema is registered, the schema cannot easily
be modified. Because zope.formlib will try to get the value for the new field
in the schema when you visit the edit screen, it will throw an error since
there is no attribute for that object yet. So, you have to update every
instance of that specific portlet type and add the missing attributes.

And here is how, in a generic way:

.. code-block:: python

    from Products.CMFCore.utils import getToolByName
    from plone.portlets.interfaces import ILocalPortletAssignable
    from plone.portlets.interfaces import IPortletManager
    from plone.portlets.interfaces import IPortletAssignmentMapping
    from zope.component import getUtilitiesFor, getMultiAdapter

    def update_portlet_schema(context, portlet_interface, attribute, value):
        """
        Helper function to update a schema of an already registered portlet.
        @param context: A Plone context.
        @param portlet_interface: The interface that the portlet implements.
        @param attribute: The name of the attribute to be added as string.
        @param value: The value, the attribute should be initialized with.

        """
        urltool = getToolByName(context, "portal_url")
        site = urltool.getPortalObject()

        cat = getToolByName(site, 'portal_catalog')
        query = {'object_provides': ILocalPortletAssignable.__identifier__}
        all_brains = cat(**query)
        all_content = [brain.getObject() for brain in all_brains]
        all_content.append(site)
        for content in all_content:
            for manager_name, manager in getUtilitiesFor(IPortletManager, context=content):
                mapping = getMultiAdapter((content, manager), IPortletAssignmentMapping)
                for id, assignment in mapping.items():
                    if portlet_interface.providedBy(assignment):
                        try:
                            getattr(assignment, attribute)
                        except AttributeError:
                            setattr(assignment, attribute, value)


Just pass the function update_portlet_schema any plone content context (e.g.
the portlet root object itself), the portlet's schema interface which was
modified, the attribute name as string and the value which should set
initially. Done.

You can find this function among other useful tools in the package
`collective.setuphandlertools
<http://pypi.python.org/pypi/collective.setuphandlertools>`_ and on `github
<https://github.com/collective/collective.setuphandlertools>`_.

A fix, so that zope.formlib accepts schema updates is beeing discussed in the
zope mailing list (see `here
<http://www.gossamer-threads.com/lists/zope/dev/230105>`_).
