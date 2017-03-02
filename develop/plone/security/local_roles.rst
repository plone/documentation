===========
Local roles
===========

.. admonition:: Description

    Creating and setting local roles of Plone members programmatically.


Introduction
============

Local roles allows user accounts to have special privileges
for a folder and its children.

By default Plone has roles like ``Contributor``, ``Reader``, ``Editor``, etc.
You can view these on the :guilabel:`Sharing` tab and in the Management Interface :guilabel:`Security` tab.

Good introduction to roles:
`Basic Roles and Permissions in Plone <http://www.sixfeetup.com/blog/basic-roles-and-permissions-in-plone>`_


Creating a new role
===================

New Plone roles can be created through the
:doc:`GenericSetup rolemap.xml </develop/addons/components/genericsetup>` file.

Example ``profiles/default/rolemap.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <rolemap>
      <roles>
        <role name="National Coordinator"/>
        <role name="Site Manager"/>
      </roles>
      <permissions>
      </permissions>
    </rolemap>


Adding a role to the Sharing Tab
================================

To let the newly created role appear in the @@sharing tab, create a
:doc:`GenericSetup sharing.xml </develop/addons/components/genericsetup>` file.

Example ``profiles/default/sharing.xml``

.. code-block:: xml

    <sharing xmlns:i18n="http://xml.zope.org/namespaces/i18n"
             i18n:domain="plone">
      <role
          id="Site Manager"
          title="Is a site coordinator"
          permission="Manage portal"
          i18n:attributes="title"
          />
    </sharing>

The title is the name to be shown on the sharing page. The required_permission
is optional. If given, the user must have this permission to be allowed to
manage the particular role.


Setting local role
===================

``manage_setLocalRoles`` is defined in `AccessControl.rolemanager.RoleManager <https://github.com/zopefoundation/AccessControl/blob/master/src/AccessControl/rolemanager.py#L339>`_.

Example::

    context.manage_setLocalRoles(userid, ["Local roles as a list"])


Getting local roles
===================

The ``get_local_roles()`` method returns currently-set local roles.
This does not return all the *effective* roles
(which may include roles acquired from the parent hierarchy).
``get_local_roles_for_userid()`` returns roles for a particular user as a tuple.

Example::

    # get_local_roles() return sequence like ( ("userid1", ("rolename1", "rolename2")), ("userid2", ("rolename1") )
    roles = context.get_local_roles()

The ``getRolesInContext()`` method returns the list of roles assigned to the user, including local roles assigned in the context of the passed-in object and both local roles assigned directly to the user and those assigned to the user's groups.

Example::

    from Products.CMFCore.utils import getToolByName
    pm = getToolByName(context, 'portal_membership')
    roles_in_context = pm.getAuthenticatedMember().getRolesInContext(context)

Deleting local roles
====================

``manage_delLocalRoles(userids)`` takes a *list of usernames* as argument.
All local roles for these users will be cleared.

The following example (``membrane``-specific)
will reset local roles based on external input ::

    def _updateLocalRoles(self):
        """ Resets Local Coordinator roles for associated users.

        Reads Archetypes field which is a ReferenceField to membrane users.
        Based on this field values users are granted local roles on this object.
        """

        # Build list of associated usernames
        usernames = []

        # Set roles for newly given users
        for member in self.getExtraLocalCoordinators():

            # We are only interested in this particular custom membrane user type
            if member.getUserType() == "local_coordinator":

                username = member.getUserName()

                usernames.append(username)

                self.manage_setLocalRoles(username, ["Local Coordinator"])

        membrane = getToolByName(self, "membrane_tool")

        # Make sure that users which do not appear in extraLocalCoordinators
        # will have their roles cleared
        for username, roles in self.get_local_roles():

            sits_user = membrane.getUserAuthProvider(username)

            if not username in usernames:
                print "Clearing:" + username
                self.manage_delLocalRoles([username])


Blocking local roles
====================

Local roles may need to be blocked on a particular object by default. This can be
achieved by add a flag to your content object, like so:

.. code-block:: python

    class MyType(content.Container):
        """My content type
        """
        implements(IMyType)
        __ac_local_roles_block__ = True



Local role caching
==================

Resolving effective local roles is a cumbersome operation, so the result is cached.

.. warning::
    **Unit testers**: Local roles are cached per request.
    You need to clear this cache after modifying an object's local roles
    or switching user if you want to get proper readings.

Unit test example method::

    def clearLocalRolesCache(self):
        """ Clear borg.localroles cache.

        borg.localroles check role implementation caches user/request combinations.
        If we edit the roles for a user we need to clear this cache,
        """
        from zope.annotation.interfaces import IAnnotations
        ann = IAnnotations(self.app.REQUEST)
        for key in list(ann.keys()): # Little destructive here, deletes *all* annotations
            del ann[key]


Debugging
=========

Set your breakpoint in ``Products.PlonePAS.plugins.local_role.LocalRolesManager.getRolesInContext()``
and ``Products.PlonePAS.plugins.role.GroupAwareRoleManager.getRolesForPrincipal()``.
There you see how roles for a given context are being resolved.

Check the ``acl_users.portal_role_manager`` via the Management Interface.

Please see the `zopyx.plone.cassandra <https://pypi.python.org/pypi/zopyx.plone.cassandra>`_ add-on product.

Other
-----

* http://toutpt.wordpress.com/2009/03/14/plone-and-local-roles-too-quiet/
