==================
 Permissions
==================

.. admonition:: Description

    How to deal with permissions making your code permission-aware in Plone


Introduction
============

Permissions control whether logged-in or anonymous users can execute code
and access content.

Permissions in Plone are managed by
`Zope's AccessControl module <https://github.com/zopefoundation/AccessControl>`_.
Persistent permission setting and getting by role heavy lifting is done by
`AccessControl.rolemanager.RoleManager <https://github.com/zopefoundation/AccessControl/blob/master/src/AccessControl/rolemanager.py>`_.

Permission checks are done for:

* every view/method which is hit by incoming HTTP request
  (Plone automatically publishes traversable methods over HTTP);

* every called method for
  :doc:`RestrictedPython scripts </develop/plone/security/sandboxing>`.

The basic way of dealing with permissions is setting the ``permission``
attribute of view declaration. For more information see :doc:`views
</develop/plone/views/browserviews>`.

Debugging permission errors: Verbose Security
================================================

You can turn on ``verbose-security`` option in buildout to get better traceback info when
you encounter a permission problem on the site (you are presented a login dialog).

For the security reasons, this option is disabled by default.

* Set ``verbose-security = on`` in your buildout.cfg ``instance`` or related section.

* Rerun buildout

* Restart Plone properly after buildout ``bin/plonectl stop && bin/plonectl start``

* remove the ``Unauthorized`` exception from the list of ignored exceptions inside
  the ``error_log`` object within the Plone root folder through the Management Interface

More info

* https://pypi.python.org/pypi/plone.recipe.zope2instance

Checking if the logged-in user has a permission
====================================================

The following code checks whether the logged in user
has a certain permission for some object.

.. code-block:: python

    from AccessControl import getSecurityManager
    from AccessControl import Unauthorized

    # Import permission names as pseudo-constant strings from somewhere...
    # see security doc for more info
    from Products.CMFCore.permissions import ModifyPortalContent

    def some_function(self, obj):
        sm = getSecurityManager()
        if not sm.checkPermission(ModifyPortalContent, obj):
            raise Unauthorized("You need ModifyPortalContent permission to execute some_function")

         # ...
         # we have security clearance here
         #


Checking whether a specific role has a permission
==================================================

The following example uses the ``rolesOfPermission()`` method to check
whether the *Authenticated* role has a permission on a certain folder on the
site. The weirdness of the method interface is explained by the fact that
it was written for use in a Management Interface template::

    def checkDBPermission(self):
        from zope.app.component.hooks import getSite
        site = getSite()
        obj = site.intranet
        perms = obj.rolesOfPermission("View")
        found = False

        for perm in perms:
            if perm["name"] == "Authenticated":
                if perm["selected"] != "": # will be SELECTED if the permission is granted
                    found = True
                    break

        if not found:
            from Products.statusmessages.interfaces import IStatusMessage
            messages = IStatusMessage(self.request)
            messages.addStatusMessage(u"Possibe permission access problem with the intranet. Errors on creation form may happen.", type="info")


Permission Access
==================

Objects that are manageable :term:`TTW` inherit from
`RoleManager  <http://api.plone.org/CMF/1.5.4/private/AccessControl.Role.RoleManager-class.html>`_.
The API provided by this class permits you to manage permissions.

Example: see all possible permissions::

   >>> obj.possible_permissions()
   ['ATContentTypes Topic: Add ATBooleanCriterion',
    'ATContentTypes Topic: Add ATCurrentAuthorCriterion',
    ...
    ]

Show the security matrix of permission::

    >>> self.portal.rolesOfPermission('Modify portal content')
    [{'selected': '', 'name': 'Anonymous'},
     {'selected': '', 'name': 'Authenticated'},
     {'selected': '', 'name': 'Contributor'},
     {'selected': '', 'name': 'Editor'},
     {'selected': 'SELECTED', 'name': 'GroupAdmin'},
     {'selected': '', 'name': 'GroupContributor'},
     {'selected': '', 'name': 'GroupEditor'},
     {'selected': '', 'name': 'GroupLeader'},
     {'selected': '', 'name': 'GroupMember'},
     {'selected': '', 'name': 'GroupReader'},
     {'selected': '', 'name': 'GroupVisitor'},
     {'selected': 'SELECTED', 'name': 'Manager'},
     {'selected': '', 'name': 'Member'},
     {'selected': 'SELECTED', 'name': 'Owner'},
     {'selected': '', 'name': 'Reader'},
     {'selected': '', 'name': 'Reviewer'},
     {'selected': '', 'name': 'SubscriptionViewer'}]


Bypassing permission checks
===========================

The current user is defined by active security manager.
During both restricted and unrestricted execution certain
functions may do their own security checks
(``invokeFactory``, workflow, search)
to filter out results.

If a function does its own security checks,
there is usually a code path that will execute without security check.
For example the methods below have security-aware and raw versions:

* ``context.restrictedTraverse()`` vs. ``context.unrestrictedTraverse()``

* ``portal_catalog.searchResults()`` vs. ``portal_catalog.unrestrictedSearchResults()``

However, in certain situations you have only a security-aware code path
which is blocked for the current user. You still want to execute
this code path and you are sure that it does not violate your site
security principles.

Below is an example how you can call any Python function and
work around the security checks by establishing a temporary
``AccessControl.SecurityManager`` with a special role.

Example::

    from AccessControl import ClassSecurityInfo, getSecurityManager
    from AccessControl.SecurityManagement import newSecurityManager, setSecurityManager
    from AccessControl.User import nobody
    from AccessControl.User import Super as BaseUnrestrictedUser

    class UnrestrictedUser(BaseUnrestrictedUser):
        """Unrestricted user that still has an id.
        """
        def getId(self):
            """Return the ID of the user.
            """
            return self.getUserName()

    def execute_under_special_role(portal, role, function, *args, **kwargs):
        """ Execute code under special role privileges.

        Example how to call::

            execute_under_special_role(portal, "Manager",
                doSomeNormallyNotAllowedStuff,
                source_folder, target_folder)


        @param portal: Reference to ISiteRoot object whose access controls we are using

        @param function: Method to be called with special privileges

        @param role: User role for the security context when calling the privileged code; e.g. "Manager".

        @param args: Passed to the function

        @param kwargs: Passed to the function
        """

        sm = getSecurityManager()

        try:
            try:
                # Clone the current user and assign a new role.
                # Note that the username (getId()) is left in exception
                # tracebacks in the error_log,
                # so it is an important thing to store.
                tmp_user = UnrestrictedUser(
                    sm.getUser().getId(), '', [role], ''
                    )

                # Wrap the user in the acquisition context of the portal
                tmp_user = tmp_user.__of__(portal.acl_users)
                newSecurityManager(None, tmp_user)

                # Call the function
                return function(*args, **kwargs)

            except:
                # If special exception handlers are needed, run them here
                raise
        finally:
            # Restore the old security manager
            setSecurityManager(sm)

For a more complete implementation of this technique, see:

* http://github.com/ned14/Easyshop/blob/master/src/easyshop.order/easyshop/order/adapters/order_management.py

Catching ``Unauthorized``
=========================

Gracefully failing when the user does not have a permission. Example::

    from AccessControl import Unauthorized

    try:
        portal_state = context.restrictedTraverse("@@plone_portal_state")
    except Unauthorized:
        # portal_state may be limited to admin users only
        portal_state = None


Creating permissions
====================

Permissions are created declaratively in :term:`ZCML`. Before Zope 2.12
(that is, before Plone 4), the `collective.autopermission`_ package
was required to enable this, but now it is standard behaviour.

.. _collective.autopermission:
   https://pypi.python.org/pypi/collective.autopermission/1.0b1

* http://n2.nabble.com/creating-and-using-your-own-permissions-in-Plone-3-tp339972p1498626.html

* http://blog.fourdigits.nl/adding-zope-2-permissions-using-just-zcml-and-a-generic-setup-profile

Example:

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

Now you can use the permission both as a Zope 2-style permission
(``MyProduct: MyPermission``) or a Zope 3-style permission
(``myproduct.mypermission``).
The only disadvantage is that you can't import the permission string as a
variable from a ``permissions.py`` file,
as you can with permissions defined programmatically.

By convention, the permission id is prefixed with the name of the
package it's defined in, and uses lowercase only. You have to take care
that the title matches the permission string you used in
``permissions.py`` exactly --- otherwise a different, Zope 3 only,
permission is registered.

Zope 3 style permissions are necessary when using Zope 3 technologies
such as ``BrowserViews/formlib/z3c.form``. For example, from
``configure.zcml``:

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

Define Zope 2 permissions in Python code (old style)
------------------------------------------------------

If you want to protect certain actions in your product by a special
permission, you most likely will want to assign this permission to a role
when the product is installed.
You will want to use Generic Setup's ``rolemap.xml`` to assign these
permissions.  A new permission will be added to
the Zope instance by calling ``setDefaultRoles`` on it.

However, at the time when Generic Setup is run, almost none of your code has
actually been run, so the permission doesn't exist yet.  That's why we define
the permissions in ``permissions.py``, and call this from ``__init__.py``:

``__init__.py``::

    import permissions

``permissions.py``::

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
get an ``ImportError`` or ``NameError``.


Assigning permissions to users (roles)
======================================

Permissions are usually assigned to roles,
which are assigned to users through the web.

To assign a permission to a role, use ``profiles/default/rolemap.xml``:

.. code-block:: xml

   <?xml version="1.0"?>
    <rolemap>
      <permissions>
        <permission name="MyProduct: MyPermission" acquire="False">
          <role name="Member"/>
        </permission>
      </permissions>
    </rolemap>


Manually fix permission problems
================================

In the case you fiddle with permission and manage to lock out even the admin
user you can still fix the problem from the
:doc:`debug prompt </develop/plone/misc/commandline>`.

Example debug session, restoring ``Access Contents Information`` for all
users::

    >>> c = app.yoursiteid.yourfolderid.problematiccontent
    >>> import AccessControl
    >>> from Products.CMFCore.permissions import AccessContentsInformation
    >>> sm = AccessControl.getSecurityManager()
    >>> import transaction
    >>> anon = sm.getUser()
    >>> c.manage_permission(AccessContentsInformation, roles=anon.getRoles())
    >>> transaction.commit()

