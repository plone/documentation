.. _pas-update-credentials-plugins:

==========================
Update Credentials Plugins
==========================

.. contents :: :local:

.. admonition:: Description

        Credential update plugins respond to the user changing credentials.

Stock Plugins
-------------

Cookie Auth Helper
^^^^^^^^^^^^^^^^^^
This plugin helps manage the details of Cookie Authentication. Allows you to extract credentials from a cookie, update them, reset them, etc.

Delegating Multi Plugin
^^^^^^^^^^^^^^^^^^^^^^^
This plugin delegates a PAS interface to some other acl_user folder, typically a "legacy" folder that implements some specific authentication functionality. For example, you can delegate the IAuthenticationPlugin interface to a legacy user folder via a Delegating Multi Plugin.

Inline Auth Helper
^^^^^^^^^^^^^^^^^^
Manages credentials for inline authentication.

Session Auth Helper
^^^^^^^^^^^^^^^^^^^
Extracts and manages credentials for session authentication.
