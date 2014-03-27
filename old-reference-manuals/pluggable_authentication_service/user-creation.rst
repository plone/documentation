=============
User creation
=============

.. contents:: :local:

.. admonition:: Description

    PAS uses a multi-phase algorithm to create a user object

#. An ``IUserFactoryPlugin`` plugin is used to create a new user object.
#. All ``IPropertiesPlugin`` plugins are queried to get the property sheets.
#. All ``IGroupsPlugin`` plugins are queried to get the groups.
#. All ``IRolesPlugin`` plugins are queried to get the global roles.
