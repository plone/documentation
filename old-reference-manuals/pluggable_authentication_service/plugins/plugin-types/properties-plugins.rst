.. _pas-properties-plugins:

==================
Properties Plugins
==================

.. contents :: :local:

.. admonition:: Description

        Properties plugins generate property sheets for users.

Stock Plugins
-------------

Delegating Multi Plugin
^^^^^^^^^^^^^^^^^^^^^^^
This plugin delegates a PAS interface to some other acl_user folder, typically a "legacy" folder that implements some specific authentication functionality. For example, you can delegate the IAuthenticationPlugin interface to a legacy user folder via a Delegating Multi Plugin.
