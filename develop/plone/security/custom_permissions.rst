==================
Custom permissions
==================

.. admonition:: Description

        Creating special permissions for your product


If you want to protect certain actions in your product by a special permission,
you most likely will want to assign this permission to a role when the product is installed.

First the permission is defined in *zcml*.
It includes an example how to use the permission in a browser page

.. code-block:: xml

    <configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser">

      <permission
        id="myproduct.mypermission"
        title="MyProduct: MyPermission"
    />

      <browser:page
        for="*"
        name="myexampleview"
        class="browser.MyExampleView"
        permission="myproduct.mypermission"
    />

    </configure>

Now you can use the permission both as a Zope 2 permission *('MyProduct: MyPermission')* or a Zope 3 permission *('myproduct.mypermission')*.
The only disadvantage is that you can't import the permissionstring as a variable from a *permissions.py* like from *Products.CMFCore.permissions*.

Use Generic Setup's *rolemap.xml* to assign the new permission to roles.
This defines the defaults.
With the use of (custom) workflows this mapping may change.

.. code-block:: xml

    <?xml version="1.0"?>
    <rolemap>
      <permissions>
        <permission name="MyProduct: MyPermission"
                    acquire="True">
          <role name="Manager"/>
          <role name="Site Administrator"/>
          <role name="Owner"/>
          <role name="Contributor"/>
        </permission>
      </permissions>
    </rolemap>

A new permission will be added to the whole Zope instance by calling *setDefaultRoles* on it.
This step is only *rarely needed*,
i.e. if the permission must be available outside of Plone Site.

Define the following code in your  __init__.py:

.. code-block:: python

    from Products.CMFCore.permissions import setDefaultRoles

    setDefaultRoles('MyProduct: MyPermission', ('Manager', 'Owner',))
