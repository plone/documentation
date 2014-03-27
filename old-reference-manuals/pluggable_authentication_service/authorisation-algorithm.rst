=======================
Authorisation algorithm
=======================

.. contents:: :local:

These are the steps the PAS user folder follows in its ``validate`` method:

#. extract all credentials.
   This looks for any possible form of authentication information in a
   request: HTTP cookies, HTTP form parameters, HTTP authentication
   headers, originating IP address, etc.
   A request can have multiple (or no) sets of credentials.  

#. for each set of credentials found:

  #. try to authorise the credentials.
     This checks if the credentials correspond to a known user and are
     valid.
  #. create a user instance
  #. try to authorise the request.
     If successful, use this user and stop further processing.

#. create an anonymous user

#. try to authorise the request using the anonymous user.
   If successful use this, if not:

#. issue a challenge.
