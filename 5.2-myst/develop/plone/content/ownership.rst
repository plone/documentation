====================
Ownership of content
====================


.. admonition:: Description

        Programmatically manipulate Plone content item's ownership

Introduction
------------

Each content item has an owner user.

Owned item instances are of subclass of AccessControl.Owned

* http://svn.zope.org/Zope/trunk/src/AccessControl/Owned.py?rev=96262&view=auto

Getting the owner of the item
-----------------------------

Example::

        # Returns PropertiedUser for Zope admin
        # Returns PloneUser for normal users object
        context.getOwner()

Changing ownership of content
-------------------------------

You can use AccessControl.Owner.changeOwnership::

        changeOwnership(self, user, recursive=0)

User is PropertiedUser object.

Example::

    # Get the user handle from member data object
    user = member.getUser()

    # Make the member owner of his home folder
    home_folder.changeOwnership(user, recursive=False)
    home_folder.reindexObjectSecurity()

.. warning::

        This only changes the owner attribute, not the role assignments. You
        need to change those too.

Example how to add ownership for additional user using local roles::

    home_folder.manage_setLocalRoles(username, ["Owner",])
    home_folder.reindexObjectSecurity()

.. note::

        This does not update Dublin Core metadata fields like
        creator.

Contributors
------------

Contributors is an automatically managed list where persons, who have been editing in the past,
real names are listed. Contributors data is available as Python list of real names.

.. note::

        Contributors does not store user references, because one might want to maintain
        contributor data even after the user has been deleted.

Some sample code::

        def format_contributors(contribs):
                """
                @return: String of comma separated list of all contributors
                """

                if len(contribs) == 0:
                    return None

                return ", ".join(contribs)

         data = {
                "contributors" : format_contributors(obj.Contributors()),
         }

.. code-block:: html

    <span tal:condition="o/contributors">
        <span tal:replace="o/contributors">Jim Smith, Jane Doe</span>
    </span>

