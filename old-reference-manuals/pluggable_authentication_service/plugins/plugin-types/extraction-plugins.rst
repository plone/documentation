.. _pas-extraction-plugins:

==================
Extraction Plugins
==================

.. contents :: :local:

.. admonition:: Description

        Extraction plugins are responsible for extracting credentials from the request.

Stock Plugins
-------------
The following stock plugins provide the IExtractionPlugin Interface.

Cookie Auth Helper
^^^^^^^^^^^^^^^^^^
This plugin helps manage the details of Cookie Authentication. Allows you to extract credentials from a cookie, update them, reset them, etc.

HTTP Basic Auth Helper
^^^^^^^^^^^^^^^^^^^^^^
Multi-plugin for managing details of HTTP Basic Authentication. Extracts credentials from request and implements the HTTP Auth challenge.

Inline Auth Helper
^^^^^^^^^^^^^^^^^^
Manages credentials for inline authentication.

Session Auth Helper
^^^^^^^^^^^^^^^^^^^
Extracts and manages credentials for session authentication.

Methods
-------
Each plugin implements the following methods:

    * extractCredentials() -- gets credential info from the relevant request, cookie, session, etc.
    * updateCredentials() -- responds to a change of credentials
    * resetCredentials() -- empties out currently stored values

if appropriate, the plugin will also implement a challenge() method which will challenge the user for authentication.
