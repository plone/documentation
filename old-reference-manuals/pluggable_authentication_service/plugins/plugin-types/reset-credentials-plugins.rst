.. _pas-reset-credentials-plugins:

=========================
Reset Credentials Plugins
=========================

.. contents :: :local:

.. admonition:: Description

        Credential clear plugins respond to a user logging out.

Stock Plugins
-------------

Cookie Auth Helper
^^^^^^^^^^^^^^^^^^
This plugin helps manage the details of Cookie Authentication. Allows you to extract credentials from a cookie, update them, reset them, etc.

Delegating Multi Plugin
^^^^^^^^^^^^^^^^^^^^^^^
This plugin delegates a PAS interface to some other acl_user folder, typically a "legacy" folder that implements some specific authentication functionality. For example, you can delegate the IAuthenticationPlugin interface to a legacy user folder via a Delegating Multi Plugin.

HTTP Basic Auth Helper
^^^^^^^^^^^^^^^^^^^^^^
Multi-plugin for managing details of HTTP Basic Authentication. Extracts credentials from request and implements the HTTP Auth challenge.

Inline Auth Helper
^^^^^^^^^^^^^^^^^^
Manages credentials for inline authentication.

Session Auth Helper
^^^^^^^^^^^^^^^^^^^
Extracts and manages credentials for session authentication.
