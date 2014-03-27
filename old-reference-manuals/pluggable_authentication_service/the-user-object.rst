===============
The user object
===============

.. contents:: :local:

.. admonition:: Description

    In contrast to other user folders, a user in a PAS environment does
    not have a single source.
    Various aspects of a user (properties, groups, roles, etc.) are
    managed by different plugins.
    To accommodate this, PAS features a user object which provides a
    single interface to all different aspects.

There are two basic user types:
a normal user (as defined by the ``IBasicUser`` interface)
and a user with member properties 
(defined by the ``IPropertiedUser`` interface).
Since basic users are not used within Plone we will only consider
``IPropertiedUser`` users.

``getId()``
   returns the user id. This is a unique identifier for a user.

``getUserName()``
   Return the login name used by the user to log into the system.

``getRoles()``
   Return the roles assigned to a user "globally".

``getRolesInContext(context)``
   Return the roles assigned to the user within a specific context.
   This includes the global roles as returned by ``getRoles()``.
