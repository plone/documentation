===============
Member profiles
===============


.. admonition:: Description

    How to manage Plone member properties programmatically

Introduction
=============

Member profile fields are the fields which the logged-in member
can edit himself on his user account page.

For more info, see:

``MemberDataTool``
    https://github.com/zopefoundation/Products.CMFCore/blob/master/Products/CMFCore/MemberDataTool.py

``MemberData`` class
    https://github.com/zopefoundation/Products.CMFCore/blob/master/Products/CMFCore/MemberDataTool.py

PlonePAS subclasses and extends MemberData and MemberDataTool.

* `See PlonePAS MemberDataTool <https://gist.github.com/svx/0f0b88ac2da4aaa38098>`_.

* `See PlonePAS MemberData class <https://gist.github.com/svx/7ced29e3dded6fe893c9>`_.

Getting member profile properties
=================================

.. note::

    The following applies to vanilla Plone.
    If you have customized membership behavior it won't necessarily work.

Member profile properties (title, address, biography, etc.)
are stored in ``portal_membership`` tool.

Available fields can be found in the Management Interface -> ``portal_membership`` -> :guilabel:`Properties` tab.

The script below is a simple example showing how to list all member
email addresses::

   from Products.CMFCore.utils import getToolByName
   memberinfo = []
   membership = getToolByName(self.context, 'portal_membership')
   for member in membership.listMembers():
       memberinfo.append(member.getProperty('email'))
   return memberinfo


Accessing member data
---------------------

.. TODO::

    Get member data by username

Further reading
---------------

* `ToolbarViewlet has some sample code <https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/viewlets/common.py>`_
   how to retrieve these properties.


Getting member fullname
-----------------------

In Python code you can access properties on the ``MemberData`` object::

    fullname = member_data.getProperty("fullname")

In a template you can do something along the same lines::

    <tal:with-fullname define="membership context/portal_membership;info python:membership.getMemberInfo(user.getId()); fullname info/fullname">
        You are are <span class="name" tal:content="fullname" />
    </tal:with-fullname>

Note that this code won't work for anonymous users.

Setting member profile properties
=================================

Use ``setMemberProperties(mapping={...})`` to batch update properties.
Old properties are not removed.

Example::

    member = portal_membership.getMemberById(user_id)
    member.setMemberProperties(mapping={"email":"aaa@aaa.com"})

New properties must be explicitly declared in ``portal_memberdata``,
before creation of the member,
or ``setMemberProperties()`` will silently fail.

.. TODO::

    How to retrofit existing members with new properties?

Example::

    def prepareMemberProperties(site):
        """ Adjust site for custom member properties """

        # Need to use ancient Z2 property sheet API here...
        portal_memberdata = getToolByName(site, "portal_memberdata")

        # When new member is created, it's MemberData
        # is populated with the values from portal_memberdata property sheet,
        # so value="" will be the default value for users' home_folder_uid
        # member property
        if not portal_memberdata.hasProperty("home_folder_uid"):
            portal_memberdata.manage_addProperty(id="home_folder_uid", value="", type="string")

     ....

    def createMatchingHomeFolder(member):
        """ """

        email = member.getProperty("email")
        home_folder.setEmail(email)

        # Store UID of the created folder in memberdata so we can
        # look it up later to e.g. generate the link to the member folder
        member.setMemberProperties(mapping={"home_folder_uid": home_folder.UID()})


        return home_folder

Setting password
-----------------

Password is a special case.

Example how to set the user password::

    # Password is set in a special way
    # passwd is password as plain text
    member.setSecurityProfile(password=passwd)


Increase minimum password size
------------------------------

To increase the minimum password size, copy ``validate_pwreset_password``
to your custom folder and insert the following lines::

    if len(password) < 8:
        state.setError('password', 'ERROR')

This will increase the minimum password size for the password reset form
to 8 characters. (This does not effect new user registration, that limit
will still be 5.)

Don't forget to update your form templates to reflect your changes!



Default password length - password reset form
---------------------------------------------

The password reset form's minimum password length is 5 characters.
To increase this:

Copy ``validate_pwreset_password`` into your custom folder
and add the following lines::

    if len(password) < 8:
        state.setError('password','ERROR')

before the ``if state.getErrors():`` method.

This would increase the minimum password size to 8 characters.
Remember to update your form templates accordingly.


Setting visual editor for all users
------------------------------------

The *visual editor* property is set on the member upon creation.

If you want to change all site members to use TinyMCE instead of Kupu.
you have to do it using the command-line ---
Plone provides no through-the-web way to change
the properties of other members.
Here is a script which does the job:

``migrate.py``::

    import transaction

    # Traverse to your Plone site from Zope application root
    context = app.yoursiteid.sitsngta # site id is yoursiteid

    usernames = context.acl_users.getUserNames()
    portal_membership = context.portal_membership
    txn = transaction.get()

    i = 0
    for userid in usernames:
        member = portal_membership.getMemberById(userid)
        value = member.wysiwyg_editor

        # Show the existing editor choice before upgrading
        print str(userid) + ": " + str(value)

        # Set WYSIWYG editor for the member
        member.wysiwyg_editor = "TinyMCE"

        # Make sure transaction buffer does not grow too large
        i += 1
        if i % 25 == 0:
            txn.savepoint(optimistic=True)

    # Once done, commit all the changes
    txn.commit()

Run it::

    bin/instance run migrate.py

.. note::

    The script does not work through the Management Interface
    as member properties do not have proper security declarations,
    meaning, no changes are permitted.

Password reset requests
========================

Directly manipulating password reset requests is useful e.g. for testing.

Poking requests::

    # Poke password reset information
    reset_requests = self.portal.portal_password_reset._requests.values()
    self.assertEqual(1, len(reset_requests))
    # reset requests are keyed by their random magic string
    key = self.portal.portal_password_reset._requests.keys()[0]
    reset_link = self.portal.pwreset_constructURL(key)

Clearing all requests::

        # Reset all password reset requests
        self.portal.portal_password_reset._requests = {}
