=========================
Credential authentication
=========================

.. contents :: :local:

.. admonition:: Description

        The credentials as returned by the credential extraction plugins only reflect the
        authentication information provided by the user. These credentials need to be authenticated
        by an authentication plugin to check if they are correct for a real user.

The IAuthenticationPlugin interface is a simple one::

   def authenticateCredentials( credentials ):
       """ credentials -> (userid, login)
       o 'credentials' will be a mapping, as returned by IExtractionPlugin.
       o Return a  tuple consisting of user ID (which may be different
         from the login name) and login
       o If the credentials cannot be authenticated, return None.
       """

Here is a simple example::

   def authenticateCredentials(self, credentials):
       users={ "hanno" : "hannosch", "martin" : "optilude",
               "philipp" : "philiKON" }
   
       if "login" not in credentials or "password" not in credentials:
           return None
   
       login=credentials["login"]
       password=credentials["password"]
       if users.get(login, None)==password:
           return (login, login)
   
       return None

This plugin allows the users *hanno*, *martin* and *philipp* to login with their nickname as password.
