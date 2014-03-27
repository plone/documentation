=====================
Credential extraction
=====================

.. contents :: :local:

.. admonition:: Description

        Within PAS credentials are a set of information which can identify and authenticate a user.
        A users login name and password are for example very common credentials. You may also use
        an HTTP cookie to track users; if you do so the cookie will be your credential.

PAS user credential extraction plugins to find all credentials in a request. Authentication of these credentials is done at a later stage by seperate authentication plugin.

Writing a plugin
----------------

If you want to write your own credential extraction plugin it has to implement the IExtractionPlugin interface. This interface only has a single method::

   def extractCredentials( request ):
       """ request -> {...}
       o Return a mapping of any derived credentials.
       o Return an empty mapping to indicate that the plugin found no
         appropriate credentials.
       """

Here is a simple example::

   def extractCredentials(self, request):
       login=request.get("login", None)
   
       if login is None:
           return {}
   
       password="request.get("password", None)
   
       return { "login" : login, "password" : password }

This plugin extracts the login name and password from fields with the same name in the request object.

