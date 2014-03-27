.. _pas-roles-plugins:

=============
Roles Plugins
=============

.. contents :: :local:

.. admonition:: Description

        Roles plugins determine the global roles which a user has.

Stock Plugins
-------------

Delegating Multi Plugin
^^^^^^^^^^^^^^^^^^^^^^^
This plugin delegates a PAS interface to some other acl_user folder, typically a "legacy" folder that implements some specific authentication functionality. For example, you can delegate the IAuthenticationPlugin interface to a legacy user folder via a Delegating Multi Plugin.

Domain Auth Helper
^^^^^^^^^^^^^^^^^^
Authenticates users based on their IP address. Has nothing to do with Windows "Domain" Authentication.

ZODB Role Manager
^^^^^^^^^^^^^^^^^
Stores role information for users in the ZODB. Handles roles storage, role enumeration, and role assignment.
