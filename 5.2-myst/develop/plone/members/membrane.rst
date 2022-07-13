======================
 Members as content
======================

.. admonition:: Description

    The ``Products.membrane`` and ``Products.remember`` add-ons provide
    member management where members are represented by Plone content items.
    The member-as-content paradigm makes member management radically
    flexible: members can be in different folders, have different workflows
    and states and different profile fields.

    It is also possible to use this approach with dexterity; for that,
    use the ``dexterity.membrane`` add-on.


Introduction
============

*remember* (small r) and *membrane* are framework add-on products for Plone
which allows you to manipulate site members as normal content
objects. The product also allows distributed user management and different
user classes.

* ``Products.membrane`` provides a framework for integrating ``acl_users``,
  which manages access rights, with content-like members and tasks like
  login.

* ``Products.remember`` is a basic implementation of this with two different
  user workflows and a normal user schema.

* ``dexterity.membrane`` is a port of ``Products.membrane`` to the dexterity
  framework.

Basics
======

* Read the `membrane tutorial <https://plone.org/documentation/tutorial/borg/membrane>`_.

* See the example code ``Products.membrane.example``.

* Read the documents at ``Products.remember/docs/tutorial``.

* See the `Weblion FacultyStaffDirectory product
  <https://weblion.psu.edu/trac/weblion/wiki/FacultyStaffDirectory>`_, which
  is a sophisticated implementation of the framework.

* It is recommended to enable debug-level logging output for membrane
  related unit tests, as ``PlonePAS`` code swallows several exceptions and
  does not output them unless debug level is activated.

Getting member by username
==========================

Example::

    from Products.CMFCore.utils  import getToolByName

    membrane = getToolByName(context, "membrane_tool")

    # getUserAuthProvider returns None if there is no membrane-based user
    # match for username
    # e.g. this will return None for Zope admin user
    sits_user = membrane.getUserAuthProvider(username)
    return sits_user

Getting Plone member from ``MembraneUser`` or ``owner`` record
===============================================================

Below is an example of how to resolve member content object from
``MembraneUser`` record "owner" who is user "local_user"::

    (Pdb) mbtool = self.portal.membrane_tool
    (Pdb) owner
    <MembraneUser 'local_user'>
    (Pdb) mbtool.getUserAuthProvider(owner.getId())
    <SitsLocalUser at /plone/country/hospital/local_users/local_user

Creating a member
=================

The following snippet works in unit tests::

    mem_password = 'secret'

    def_mem_data = {
        'email': 'noreply@xxxxxxxxyyyyyy.com',
        'password': mem_password,
        'confirm_password': mem_password,
         }

    mem_data = {
            'portal_member':
            {
              'fullname': 'Portal Member',
              'mail_me': True,
            },
            'admin_member':
            {
              'roles': ['Manager', 'Member']
            },
            'blank_member':
            {},
        }

    mdata = getToolByName(self.portal, 'portal_memberdata')

    mdata.invokeFactory("MyUserPortalType", name)
    member = getattr(mdata, name) #


Populating member fields automatically
======================================

Use the following unit test snippet::

    def populateUser(self, member):
        """ Auto-populate member object required fields based on Archetypes schema.

        @param member: Membrane member content object
        """

        from Products.SitsHospital.content.SitsUser import SitsUser

        schema = SitsUser.schema

        data = {}

        for f in schema._fields.values():

            if not f.required:
                continue

            if f.__name__ in [ "password", "id" ]:
                # Do not set password or member id
                continue

            # Autofill member field values
            if f.vocabulary:
                value = f.vocabulary[0][0]
            elif f.__name__ in [ "email" ]:
                value = "test@xyz.com"
            else:
                value = "foo"

            # print "filling in field:" + str(f)

            data[f.__name__] = value

        member.update(**data)

Checking member validity
========================

The following snippet is useful for unit testing::

    def assertValidMember(self, member):
        """ Emulate Products.remember.content.member validation behavior with verbose output.

        """
        errors = {}
        # make sure object has required data and metadata
        member.Schema().validate(member, None, errors, 1, 1)
        if errors:
            raise AssertionError("Member contained errors:" + str(errors))

Setting user password
=====================

Passwords are stored hashed and can be set using the
``BaseMember._setPassword()`` method.

``_setPassword()`` takes the password as a plain-text argument and hashes it
before storing::

    user_object._setPassword("secret")

You may also use the ``portal_registrations`` tool. This method is
security-checked and may be used from Management Interface scripts::

    rtool = context.portal_registration
    rtool.editMember(id, properties={}, password="secret")

Use ``getToolByName`` rather than acquiring the tool from  ``context``
if you're doing this in a browser view.

Accessing hashed password
-------------------------

Use the password attribute directly::

    hashed = user_object.password

The password hash should be a unicode string.

.. Note::
    By default, ``Products.remember`` uses the ``HMACHash`` hasher. As a
    salt, the ``str(context)`` string is used. This means that it is not
    possible to move hashed password from one context item to another. For
    more information, see the ``Products.remember.content.password_hashers``
    module.

Moving members
==============

Moving members is not straightforward, as by default member password is
hashed with the member location.

- Members need to reregister their password after being moved from one
  folder to another.

Here is a complex function to perform moving by recreating the user and
deleting the old object::

    import logging

    from Products.CMFCore.utils  import getToolByName
    from Products.Archetypes import public as atapi

    from Products.SitsHospital.interfaces import ISitsUser, ISitsLocalUser, ISitsLocalCoordinatorUser


    logger = logging.getLogger("RememberUserCopy")

    def createUser(sourceUser, username, targetFolder):
        """ Default example user createor """
        targetFolder.invokeFactory("Member", username)
        return targetFolder[username]


    def postProcess(sourceUser, targetUser):
        """ Hook to set-up additional fields which do not have 1:1 mapping in the new and old user objects """
        pass


    def copyRememberUser(sourceUser, targetFolder, user_constructor=createUser, post_process=postProcess, expected_creation_state="new_private", expected_initialization_state="private"):
        """
        Copies Product.remember based user from one location to another.

        This is useful if you have locally stored members on your site
        (for example one folder per country)
        and you need to move the person from one country to another.

        Member password is hashed against the member object location.
        Thus, the password will be invalid if the physical path of the member object changes.
        All moved members are asked to re-enter their passwords.

        If betahaus.emaillogin is installed we also update its catalog so that
        the email login works after the member has been moved.

        When all the fields in the user schema validate successfully,
        the re-registration email for the new user is automatically send
        (TODO: Not sure whether this is general condition for Products.Remember)

        @param sourceUser: from Products.remember.content.member.Member instance

        @param targetFolder: Any folderish object which can contain Member instances

        @param user_constructor: function(sourceUser, targetFolder) if special user creation is needed

        @param post_process: function(sourceUser, targetUser) for setting up custom fields if there is no 1:1 mapping between fields of the new and old user object. Also you can do workflow mangling here.

        @param expected_creation_state: The workflow state where the new member should be after it has been correctly initialized. In this point update() is not yet called, so Remember automatic registration mechanism should have not been triggered.

        @param expected_initialization_state: The workflow state where the new member should be after it has been correctly initialized. In this point update() is not yet called, so Remember automatic registration mechanism should have not been triggered.

        @return: The newly created national coordinator object.
        """

        # shortcut to the source user
        lc = sourceUser

        # Validate LC user
        errors = {}
        lc.Schema().validate(lc, None, errors, True, True)
        if errors:
            assert not errors, "The source user must be valid before moving. Errors:" + str(errors)

        username = lc.getUserName()

        logger.debug("Copying user:" + username)

        # Make sure that LC username is free
        id = lc.getId()
        parent = lc.aq_parent

        assert lc.cb_userHasCopyOrMovePermission(), "No permission"
        assert lc.cb_isMoveable(), "Object problem"

        # We temporarily rename the old object for the duration
        # of the moving so that the id of the member
        # object won't conflict with the newly created target user
        new_id = id + "-old"
        assert type(new_id) != unicode

        parent.manage_renameObject(id, new_id)

        # We need to re-fetch the object handle as it has changed in rename
        lc = parent[new_id]


        # nc = newly crated user
        nc = user_constructor(sourceUser, username, targetFolder)

        # List of field names which we cannot copy
        do_not_copy = ["id"]

        # Duplicate field data from old user object to new one by inspecting the user object schema
        for field in lc.Schema().fields():
            name = field.getName()

            # ComputedFields are handled specially,
            # and UID also
            if not isinstance(field, atapi.ComputedField) and name not in do_not_copy:

                if not field.writeable(nc):
                    raise RuntimeError("No permission to copy field value:" + name)

                if name == "password":
                    # Note: moving password from one user to another
                    # is not possible because password is hashed with
                    # the user location in Products.remember.content.password_hashers
                    # Insert dummy password which must be reseted
                    nc.password = "dummy"
                else:
                    value = field.getRaw(lc)

                    # The schema of new object
                    schema = nc.Schema()

                    # Check that the old field exists in the new schema
                    if name in schema:
                        newfield = schema[name]
                        logger.debug("Copying field " + name + " " + str(value))
                        newfield.set(nc, value)
                    else:
                        # The old field does not exist on the new object
                        logger.warning("Target does not have field " + name)

        #  Do custom setup for newly created user
        post_process(lc, nc)

        # Validate NC user
        errors = {}
        nc.Schema().validate(nc, None, errors, True, True)
        if errors:
            assert not errors, "Newly created user did not validate:" + str(errors)

        # Assert that the user is not yet log in-able
        workflow = getToolByName(lc, "portal_workflow")
        review_state = workflow.getInfoFor(nc, 'review_state')
        assert review_state == expected_creation_state, "Got review state:" + review_state

        # Remove the old user object
        parent = lc.aq_parent

        ##fore email-catalog removal and without the -old added
        lc_path='/'.join(lc.getPhysicalPath()).replace('-old','')
        parent.manage_delObjects([lc.getId()])

        # Trigger workflow state transition to register
        # Mark creation flag to be set

        nc.markCreationFlag()

        assert nc.isValid(), "The new NC was not valid after the creation flag was set"

        # This will trigger automatic workflow transition
        # to the registered state
        nc.update()

        # Validate NC user once again, just in case markCreationFlag and update did something bad
        errors = {}
        nc.Schema().validate(nc, None, errors, True, True)
        if errors:
            assert not errors, "Got errors:" + str(errors)
        nc.reindexObject()


        # Check if we have betahaus.emailcatalog extension installed for Plone 3.x
        email_catalog = getToolByName(nc, "email_catalog", default=None)

        if email_catalog is not None:
            # This ensures the member log-in will work in the future
            # as email_catalog does not automatically reflect member changes
            email_catalog.uncatalog_object(lc_path)
            email_catalog.reindexObject(nc)


        # Not needed - this email is automatically triggered by
        # workflow state change when the all user fields are
        # validated successfully in Schema()
        #nc.resetPassword()

        # Check that we are in active user state - the registeration email should have been send
        review_state = workflow.getInfoFor(nc, 'review_state')
        assert review_state == expected_initialization_state, "Newly created user was not auto-activated for some reason, state:" + review_state

        return nc


Configuring default roles with Dexterity
=========================================

To configure default roles for Dexterity-based members, you need a class
providing the ``IMembraneUserRoles`` interface, and to register it as adapter.

Define the class (here, in a file named ``roles.py``)::

    from Products.membrane.interfaces import IMembraneUserRoles
    from dexterity.membrane.behavior.membraneuser import DxUserObject
    from dexterity.membrane.behavior.membraneuser import IMembraneUser
    from zope.component import adapter
    from zope.interface import implementer

    DEFAULT_ROLES = ['Member']


    @implementer(IMembraneUserRoles)
    @adapter(IMembraneUser)
    class MyDefaultRoles(DxUserObject):

         def getRolesForPrincipal(self, principal, request=None):
             return DEFAULT_ROLES

And register this class in ``configure.zcml``:

.. code-block:: xml

    <adapter
         factory=".roles.MyDefaultRoles"
         provides="Products.membrane.interfaces.IMembraneUserRoles"
    />

