=========================================================
Upgrading from 4.0 to 4.1
=========================================================


.. admonition:: Description

   Upgrading your site and your products from Plone 4.0 to Plone 4.1.

.. contents:: :local:


Updating add-on products for Plone 4.1
========================================

This is a list of the most common updates that need to be applied by product authors to ensure that their products work on Plone 4.1.


Changing dependencies from Plone to Products.CMFPlone, updating permissions and aliases
----------------------------------------------------------------------------------------

Plone 4.1 separates the Products.CMFPlone package from the Plone egg to give integrators the option of building Plone sites with a cut down feature set.

Updating your setup.py
^^^^^^^^^^^^^^^^^^^^^^

In your package's *setup.py* where you currently have::

    install_requires=[
      'setuptools',
      'Plone',
    ],

Instead you should use::

    install_requires=[
      'setuptools',
      'Products.CMFPlone',
    ],

You should also list the other packages you depend on, e.g. *Products.Archetypes* or *plone.app.portlets*.


Updating Permissions
^^^^^^^^^^^^^^^^^^^^^^

If you are protecting any templates, pages, etc... in zcml with CMF core permissions (anything in the cmf namespace, e.g. cmf.ModifyPortalContent), you must add the following to configure.zcml::

    <include package="Products.CMFCore" />

Most importantly this loads the permissions.zcml, if it is available. The above statement is the easiest and will work in all Plone versions; previously a more fancy statement with a condition was advocated, which we will give here for good measure::

    <include package="Products.CMFCore" file="permissions.zcml"
               xmlns:zcml="http://namespaces.zope.org/zcml"
               zcml:condition="have plone-41" />


Updating Aliases
^^^^^^^^^^^^^^^^^^^^^^

Some old import aliases may no longer work. Please update:

* from Products.CMFPlone import Batch -> from Products.CMFPlone.PloneBatch import Batch
* from zope.app.interface import queryType -> from zope.app.content import queryType
* from Products.Five.formlib import formbase -> from five.formlib import formbase (this counts for a lot of formlib changes - most things are now imported from five.formlib.formbase)


Maintaining compatibility with Plone 4.0 and 3.3
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Version 4.0 of *Products.CMFPlone* is a forward compatibility shim (an empty egg depending on the *Plone* package) to enable Plone extension packages depending on *Products.CMFPlone* to continue working with Plone 4.0 or 3.3.


Use Generic Setup for defining versioning policies
---------------------------------------------------

From Plone 4.1 on, versioning policies for custom types can be configured using Generic Setup (repositorytool.xml).

If you activated versioning for your custom content types you most likely followed one of these How-Tos:

* :doc:`History and Versioning </develop/plone/content/history>`

Both basically recommend to set the versioning policies CMFEditions is using in a custom setuphandler::

    from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES

    portal_repository = getToolByName(portal, 'portal_repository')
    versionable_types = list(portal_repository.getVersionableContentTypes())

    for type_id in ['MyType', 'AnotherType']:
        if type_id not in versionable_types:
            versionable_types.append(type_id)
            # Add default versioning policies to the versioned type
            for policy_id in DEFAULT_POLICIES:
                portal_repository.addPolicyForContentType(type_id, policy_id)
    portal_repository.setVersionableContentTypes(versionable_types)

when migrating to plone4.1 you'll get the following error::

    ImportError: cannot import name DEFAULT_POLICIES

To make your Product compatible with Plone4.1 you can remove the code for setting versionableContenttypes above and simply add a file named repositorytool.xml to your package's Generic Setup profile and you're done::

    <?xml version="1.0"?>
    <repositorytool>
        <policymap>
            <type name="MyType">
                <policy name="at_edit_autoversion"/>
                <policy name="version_on_revert"/>
            </type>
            <type name="AnotherType">
                <policy name="at_edit_autoversion"/>
                <policy name="version_on_revert"/>
            </type>
        </policymap>
    </repositorytool>

If you need to be backward compatible you can add repositorytool.xml (which will be used in plone >= 4.1) and add a condition to your setupandler. eg::

    try:
        from Products.CMFEditions.setuphandlers import DEFAULT_POLICIES
        # we're on plone < 4.1, configure versionable types manually
        setVersionedTypes(portal)
    except ImportError:
        # repositorytool.xml will be used
        pass

<include package="Products.CMFCore" />
