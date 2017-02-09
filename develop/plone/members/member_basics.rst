=============================
 Member manipulation
=============================

.. admonition:: Description

    How to programmatically create, read, edit and delete site members.


Introduction
============

In Plone, there are two loosely-coupled subsystems relating to members:

*Authentication and permission* information
    (``acl_users`` under site root), managed by the :term:`PAS`.
    In a default installation, this corresponds to Zope user objects.
    PAS is *pluggable*, though, so it may also be authenticating against
    an LDAP server, Plone content objects, or other sources.

*Member profile* information
    accessible through the ``portal_membership`` tool.
    These represent Plone members. PAS authenticates,
    and the Plone member object provides metadata about the member.


Getting the logged-in member
============================

Anonymous and logged-in members are exposed via the
:doc:`IPortalState context helper </develop/plone/misc/context>`.

Example (browserview: use ``self.context`` since ``self`` is not
acquisition-wrapped)::

    from zope.component import getMultiAdapter

    portal_state = getMultiAdapter(
            (self.context, self.request), name="plone_portal_state")
    if portal_state.anonymous():
        # Return target URL for the site anonymous visitors
        return self.product.getHomepageLink()
    else:
        # Return edit URL for the site members
        return product.absolute_url()

or from a template:

.. code-block:: html

    <div tal:define="username context/portal_membership/getAuthenticatedMember/getUserName">
        ...
    </div>

Getting any member
==================

To get a member by username (you must have ``Manager`` role)::

    mt = getToolByName(self.context, 'portal_membership')
    member = mt.getMemberById(username)

To get all usernames::

    mt = getToolByName(self.context, 'portal_membership')
    memberIds = mt.listMemberIds()

Getting member information
==========================

Once you have access to the member object,
you can grab basic information about it.

Get the user's name::

    member.getName()

Reseting user password without emailing them
-----------------------------------------------

* https://plone.org/documentation/kb/reset-a-password-without-having-to-email-one-to-the-user

Exporting and importing member passwords
----------------------------------------

You can also get at the hash of the user's password
(only the hash is available, and only for standard Plone user objects)
(in this example we're in Plone add-on context, since ``self`` is
acquisition-wrapped)::

    uf = getToolByName(self, 'acl_users')
    passwordhash_map = uf.source_users._user_passwords
    userpasswordhash = passwordhash_map.get(member.id, '')

Note that this is a private data structure.
Depending on the Plone version and add-ons in use, it may not be available.

You can use this hash directly when importing your user data,
for example as follows (can be executed from a
:doc:`debug prompt </develop/plone/misc/commandline>`.)::

    # The file 'exported.txt' contains lines with: "memberid hash"
    lines = open('exported.txt').readlines()
    changes = []
    c = 0
    members = mt.listMembers()
    for l in lines:
        memberid, passwordhash_exported = l.split(' ')
        passwordhash_exported = passwordhash_exported.strip()
        member = mt.getMemberById(memberid)
        if not member:
            print 'missing', memberid
            continue
        passwordhash = passwordhash_map.get(memberid)
        if passwordhash != passwordhash_exported:
            print 'changed', memberid, passwordhash, passwordhash_exported
            c += 1
            changes.append((memberid, passwordhash_exported))

    uf.source_users._user_passwords.update(changes)

Also, take a look at a script for exporting Plone 3.0's memberdata and
passwords:

* http://blog.kagesenshi.org/2008/05/exporting-plone30-memberdata-and.html



Iterating all site users
============================

Example::

    buffer = ""

    # Returns list of site usernames
    mt = getToolByName(self, 'portal_membership')
    users = mt.listMemberIds()
    # alternative: get member objects
    # members = mt.listMembers()

    for user in users:
       print "Got username:" + user

.. note::

    Zope users, such as *admin*, are not included in this list.


Getting all *Members* for a given *Role*
========================================

In this example we use the ``portal_membership`` tool.
We assume that a role called ``Agent`` exists and that we already
have the context::

    from Products.CMFCore.utils import getToolByName

    membership_tool = getToolByName(self, 'portal_membership')
    agents = [member for member in membership_tool.listMembers()
                if member.has_role('Agent')]


Groups
======

Groups are stored as ``PloneGroup`` objects. ``PloneGroup`` is a subclass of
``PloneUser``.  Groups are managed by the ``portal_groups`` tool.

* https://github.com/plone/Products.PlonePAS/blob/master/Products/PlonePAS/plugins/ufactory.py

* https://github.com/plone/Products.PlonePAS/blob/master/Products/PlonePAS/plugins/group.py

Creating a group
----------------

Example::

    groups_tool = getToolByName(context, 'portal_groups')

    group_id = "companies"
    if not group_id in groups_tool.getGroupIds():
        groups_tool.addGroup(group_id)

For more information, see:

* https://github.com/plone/Products.PlonePAS/blob/master/Products/PlonePAS/tests/test_groupstool.py

* https://github.com/plone/Products.PlonePAS/blob/master/Products/PlonePAS/plugins/group.py

Add local roles to a group
--------------------------

Example::

   from AccessControl.interfaces import IRoleManager
   if IRoleManager.providedBy(context):
       context.manage_addLocalRoles(groupid, ['Manager',])

.. Note:: This is an example of code in a *view*, where ``context`` is
   available.

Update properties for a group
-----------------------------

The ``editGroup`` method modifies the title and description in the
``source_groups`` plugin, and subsequently calls ``setGroupProperties(kw)``
which sets the properties on the ``mutable_properties`` plugin.

Example::

    portal_groups.editGroup(groupid, **properties)
    portal_groups.editGroup(groupid, roles = ['Manager',])
    portal_groups.editGroup(groupid, title = u'my group title')

Getting available groups
------------------------

Getting all groups on the site is possible through ``acl_users`` and the
``source_groups`` plugin, which provides the functionality to manipulate
Plone groups.

Example to get only ids::

    acl_users = getToolByName(self, 'acl_users')
    # Iterable returning id strings:
    groups = acl_users.source_groups.getGroupIds()

Example to get full group information::

    acl_users = getToolByName(self, 'acl_users')
    group_list = acl_users.source_groups.getGroups()

    for group in group_list:
        # group is PloneGroup object
        yield (group.getName(), group.title)

List users within all groups
----------------------------

Example to get the email addresses of all users on a site, by group::

    acl_users = getToolByName(context, 'acl_users')
    groups_tool = getToolByName(context, 'portal_groups')
    groups = acl_users.source_groups.getGroupIds()
    for group_id in groups:
        group = groups_tool.getGroupById(group_id)
        if group is None:
            continue
        members = group.getGroupMembers()
        member_emails = [m.getProperty('email') for m in members]
        ...


Adding a user to a group
------------------------

Example::

    # Add user to group "companies"
    portal_groups = getToolByName(self, 'portal_groups')
    portal_groups.addPrincipalToGroup(member.getUserName(), "companies")

Removing a user from a group
------------------------------

Example::

    portal_groups.removePrincipalFromGroup(member.getUserName(), "companies")

Getting groups for a certain user
---------------------------------

Below is an example of getting groups for the logged-in user (Plone 3 and
earlier)::

    mt = getToolByName(self.context, 'portal_membership')
    mt.getAuthenticatedMember().getGroups()

In Plone 4 you have to use::

    groups_tool = getToolByName(self, 'portal_groups')
    groups_tool.getGroupsByUserId('admin')


Checking whether a user exists
===============================

Example::

    mt = getToolByName(self, 'portal_membership')
    return mt.getMemberById(id) is None

See also:

* http://svn.zope.org/Products.CMFCore/trunk/Products/CMFCore/RegistrationTool.py?rev=110418&view=auto

.. XXX: Why reference revision 110418 specifically?


Creating users
===============

Use the ``portal_registration`` tool. Example (browserview)::

    def createCompany(request, site, username, title, email, passwd=None):
        """
        Utility function which performs the actual creation, role and permission magic.

        @param username: Unicode string

        @param title: Fullname of user, unicode string

        @return: Created company content item or None if the creation fails
        """

        # If we use custom member properties they must be initialized
        # before regtool is called
        prepareMemberProperties(site)

        # portal_registration manages new user creation
        regtool = getToolByName(site, 'portal_registration')

        # Default password to the username
        # ... don't do this on the production server!
        if passwd == None:
            passwd = username

        # We allow only lowercase
        username = username.lower()

        # Username must be ASCII string
        # or Plone will choke when the user tries to log in
        try:
            username = str(username)
        except UnicodeEncodeError:
            IStatusMessage(request).addStatusMessage(_(u"Username must contain only characters a-z"), "error")
            return None

        # This is the minimum required information
        # to create a working member
        properties = {
            'username': username,
            # Full name must always be utf-8 encoded
            'fullname': title.encode("utf-8"),
            'email': email
            }

        try:
            # addMember() returns MemberData object
            member = regtool.addMember(username, passwd, properties=properties)
        except ValueError, e:
            # Give user visual feedback what went wrong
            IStatusMessage(request).addStatusMessage(_(u"Could not create the user:") + unicode(e), "error")
            return None

.. XXX: The unicode check above doesn't match the error message.

Batch member creation
-----------------------

* An example script can be run with bin/plonectl, tested on Plone 4.3.3; see http://gist.github.com/l34marr/02a9ef12a1e51c474bee

* An example script tested on Plone 2.5.x; see https://plone.org/documentation/kb/batch-adding-users


Email login
===========


* In Plone 4 and up, it is a default feature.


Custom member creation form: complex example
=============================================

Below is an example of a Grok form which the administrator can use to create
new users. New users will receive special properties and a folder for which
they have ownership access.  The password is set to be the same as the
username.  The user is added to a group named "companies".

Example ``company.py``::

    """ Add companies.

        Create user account + associated "home folder" content type
        for a company user.
        User accounts have a special role.

        Note: As of this writing, in 2010-04, we need the
        plone.app.directives trunk version which
        contains an unreleased validation decorator.
    """

    # Core Zope 2 + Zope 3 + Plone
    from zope.interface import Interface
    from zope import schema
    from five import grok
    from Products.CMFCore.interfaces import ISiteRoot
    from Products.CMFCore.utils import getToolByName
    from Products.CMFCore import permissions
    from Products.statusmessages.interfaces import IStatusMessage

    # Form and validation
    from z3c.form import field
    import z3c.form.button
    from plone.directives import form
    from collective.z3cform.grok.grok import PloneFormWrapper
    import plone.autoform.form

    # Products.validation uses some ugly ZService magic which I can't quite comprehend
    from Products.validation import validation

    # Our translation catalog
    from zope.i18nmessageid import MessageFactory
    OurMessageFactory = MessageFactory('OurProduct')
    OurMessageFactory = _

    # If we're building an addon, we may already have one, for example:
    # from isleofback.app import appMessageFactory as _

    grok.templatedir("templates")

    class ICompanyCreationFormSchema(form.Schema):
        """ Define fields used on the form """

        username = schema.TextLine(title=u"Username")

        company_name = schema.TextLine(title=u"Company name")

        email = schema.TextLine(title=u"Email")


    class CompanyCreationForm(plone.autoform.form.AutoExtensibleForm, form.Form):
        """ Form action controller.

        form.DisplayForm will automatically expose the form
        as a view, no wrapping view creation needed.
        """

        # Form label
        name = _(u"Create Company")

        # Which schema is used by AutoExtensibleForm
        schema = ICompanyCreationFormSchema

        # The form does not care about the context object
        # and should not try to extract field value
        # defaults out of it
        ignoreContext = True

        # This form is available at the site root only
        grok.context(ISiteRoot)

        # z3c.form has a function decorator
        # which turns the function to a form button action handler

        @z3c.form.button.buttonAndHandler(_('Create Company'), name='create')
        def createCompanyAction(self, action):
            """ Button action handler to create company.
            """

            data, errors = self.extractData()
            if errors:
                self.status = self.formErrorsMessage
                return

            obj = createCompany(self.request, self.context, data["username"], data["company_name"], data["email"])
            if obj is not None:
                # mark as finished only if we get the new object
                IStatusMessage(self.request).addStatusMessage(_(u"Company created"), "info")


    class CompanyCreationView(PloneFormWrapper):
        """ View which exposes form as URL """

        form = CompanyCreationForm

        # Set up security barrier -
        # non-priviledged users can't access this form
        grok.require("cmf.ManagePortal")

        # Use http://yourhost/@@create_company URL to access this form
        grok.name("create_company")

        # This view is available at the site root only
        grok.context(ISiteRoot)

        # Which template is used to decorate the form
        # -> forms.pt in template directory
        grok.template("form")


    @form.validator(field=ICompanyCreationFormSchema['email'])
    def validateEmail(value):
        """ Use old Products.validation validators to perform the validation.
        """
        validator_function = validation.validatorFor('isEmail')
        if not validator_function(value):
            raise schema.ValidationError(u"Entered email address is not good:" + value)


    def prepareMemberProperties(site):
        """ Adjust site for custom member properties """

        # Need to use ancient Z2 property sheet API here...
        portal_memberdata = getToolByName(site, "portal_memberdata")

        # When new member is created, its MemberData
        # is populated with the values from portal_memberdata property sheet,
        # so value="" will be the default value for users' home_folder_uid
        # member property
        if not portal_memberdata.hasProperty("home_folder_uid"):
            portal_memberdata.manage_addProperty(id="home_folder_uid", value="", type="string")


        # Create a group "companies" where newly created members will be added
        acl_users = getToolByName(site, 'acl_users')
        gt = getToolByName(site, 'portal_groups')

        group_id = "companies"
        if not group_id in gt.getGroupIds():
            gt.addGroup(group_id, [], [], {'title': 'Companies'})

    def createCompany(request, site, username, title, email, passwd=None):
        """
        Utility function which performs the actual creation, role and permission magic.

        @param username: Unicode string

        @param title: Fullname of user, unicode string

        @return: Created company content item or None if the creation fails
        """

        # If we use custom member properties
        # they must be intiialized before regtool is called
        prepareMemberProperties(site)

        # portal_registrations manages new user creation
        regtool = getToolByName(site, 'portal_registration')

        # Default password to the username
        # ... don't do this on the production server!
        if passwd == None:
            passwd = username

        # Only lowercase allowed
        username = username.lower()

        # Username must be ASCII string
        # or Plone will choke when the user tries to log in
        try:
            username = str(username)
        except UnicodeEncodeError:
            IStatusMessage(request).addStatusMessage(_(u"Username must contain only characters a-z"), "error")
            return None

        # This is minimum required information set
        # to create a working member
        properties = {
            'username': username,
            # Full name must be always as utf-8 encoded
            'fullname': title.encode("utf-8"),
            'email': email
            }

        try:
            # addMember() returns MemberData object
            member = regtool.addMember(username, passwd, properties=properties)
        except ValueError, e:
            # Give user visual feedback what went wrong
            IStatusMessage(request).addStatusMessage(_(u"Could not create the user:") + unicode(e), "error")
            return None

        # Add user to group "companies"
        gt = getToolByName(site, 'portal_groups')
        gt.addPrincipalToGroup(member.getUserName(), "companies")

        return createMatchingHomeFolder(request, site, member)

    def createMatchingHomeFolder(request, site, member, target_folder="yritykset", target_type="IsleofbackCompany", language="fi"):
        """ Creates a folder, sets its ownership for the member and stores the folder UID in the member data.

        @param member: MemberData object

        @param target_folder: Under which folder a new content item is created

        @param language: Initial two language code of the item
        """

        parent_folder = site.restrictedTraverse(target_folder)

        # Cannot add custom memberdata properties unless explicitly declared

        id = member.getUserName()

        parent_folder.invokeFactory(target_type, id)

        home_folder = parent_folder[id]
        name = member.getProperty("fullname")

        home_folder.setTitle(name)
        home_folder.setLanguage(language)

        email = member.getProperty("email")
        home_folder.setEmail(email)

        # Unset the Archetypes object creation flag
        home_folder.processForm()

        # Store UID of the created folder in memberdata so we can
        # look it up later to e.g. generate the link to the member folder
        member.setMemberProperties({"home_folder_uid": home_folder.UID()})

        # Get the user handle from member data object
        user = member.getUser()
        username = user.getUserName()

        home_folder.manage_setLocalRoles(username, ["Owner",])
        home_folder.reindexObjectSecurity()

        return home_folder
