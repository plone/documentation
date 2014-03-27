.. _pas-user-enumeration-plugins:

========================
User_Enumeration Plugins
========================

.. contents :: :local:

.. admonition:: Description

        Enumeration plugins allow querying users by ID, and searching for users who match
        particular criteria.

Stock Plugins
-------------

Delegating Multi Plugin
^^^^^^^^^^^^^^^^^^^^^^^
This plugin delegates a PAS interface to some other acl_user folder, typically a "legacy" folder that implements some specific authentication functionality. For example, you can delegate the IAuthenticationPlugin interface to a legacy user folder via a Delegating Multi Plugin.

Search Principals Plugin
^^^^^^^^^^^^^^^^^^^^^^^^
Plugin to delegate enumerateUsers and enumerateGroups requests to another PluggableAuthService

ZODB User Manager
^^^^^^^^^^^^^^^^^
ZODB-based user storage. Does authentication, enumeration and properties for users and stores its data in the ZODB.
