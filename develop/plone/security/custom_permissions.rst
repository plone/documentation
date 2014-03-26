==================
Custom permissions
==================

Creating special permissions for your product


Define Zope 2 permissions in python code
----------------------------------------

If you want to protect certain actions in your product by a special permission,
you most likely will want to assign this permission to a role when the product
is installed.  You will want to use Generic Setup's rolemap.xml to assign these
permissions.  A new permission will be added to the Zope instance by calling
setDefaultRoles on it. 

However, at the time when Generic Setup is run, almost none of your code has
actually been run, so the permission doesn't exist yet.  That's why we define
the permissions in permissions.py, and call this from __init__.py:

.. code-block:: python

    # __init__.py:

    import permissions

.. code-block:: python

    # permissions.py:

    from Products.CMFCore import permissions as CMFCorePermissions
    from AccessControl.SecurityInfo import ModuleSecurityInfo
    from Products.CMFCore.permissions import setDefaultRoles

    security = ModuleSecurityInfo('MyProduct')
    security.declarePublic('MyPermission')
    MyPermission = 'MyProduct: MyPermission'
    setDefaultRoles(MyPermission, ())

When working with permissions, always use the variable name instead of the
string value.  This ensures that you can't make typos with the string value,
which are hard to debug.  If you do make a typo in the variable name, you'll
get an ImportError or NameError.


Make the permissions available as a Zope 3 permissions
------------------------------------------------------

To use your permissions with BrowserViews/formlib/z3c.form, you need
to make them available available as Zope 3 permissions. This is done
in ZCML using a the <permission> directive. Example configure.zcml:

.. code-block:: xml
   
    <configure 
      xmlns="http://namespaces.zope.org/zope">

      <permission 
        id="myproduct.mypermission" 
	title="MyProduct: MyPermission" 
	/>
    
    </configure>

It's convention to prefix the permission id with the name of the
package it's defined in and use lower case only. You have to take care
that the title matches exactly the permission string you used in
permissions.py. Otherwise a different, zope 3 only, permission is
registered.

You can use the permission to e.g. protect BrowserViews. Example
configure.zcml:

.. code-block:: xml

    <configure 
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser">
   
      <permission 
        id="myproduct.mypermission" 
 	title="MyProduct: MyPermission" />
 
      <browser:page 
        for="*" 
	name="myexampleview"
        class="browser.MyExampleView"
        permission="myproduct.mypermission" 
	/>

    </configure>


Define both Zope 2 and Zope3 permissions in one Step in ZCML
------------------------------------------------------------

You can use `collective.autopermission 
<http://pypi.python.org/pypi/collective.autopermission/1.0b1>`_ 
(`svn repository 
<http://svn.plone.org/svn/collective/collective.autopermission>`_)
and define both the Zope 2 and Zope 3 permission at once with the
<permission> zcml-directive. To do that install
collective.autopermission. Either add "collective.autopermission" to
"install_requires" in setup.py or to your buildout. Then include
collective.autopermission's configure.zcml *before* you define the
permissions *and* before you use them.  (collective.autopermission is
not required in Zope 2.12/Plone 4 anymore!)

.. code-block:: xml
  
    <configure 
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser">
 
      <include package="collective.autopermission" />
 
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

Now you can use the permission both as a Zope 2 permission *('MyProduct:
MyPermission')* or a Zope 3 permission *('myproduct.mypermission')*. The
only disadvantage is that you can't import the permissionstring as a
variable from permissions.py.
