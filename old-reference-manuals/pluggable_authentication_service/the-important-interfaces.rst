========================
The important interfaces
========================

.. contents:: :local:

.. admonition:: Description

    PAS has a number of interfaces that are important for everyone.

The most important interfaces that you may want to configure are:

**Authentication**
   Authentication plugins are responsible for authenticating a set of
   credentials. Usually that will mean verifying if a login name and
   password are correct by comparing them with a user record in a database
   such as the ZODB or an SQL database.

**Extraction**
   Extraction plugins determine the credentials for a request.
   Credentials can take different forms, such as a HTTP cookie, HTTP form
   data or the user's IP address.

**Groups**
   These plugins determine which group(s) a user (or group) belongs to.

**Properties**
   Property plugins manage all properties for users.
   This includes the standard information such as the user's name and
   email address but can also be any other piece of data that you want to
   store for a user.
   Multiple properties plugins can be used in parallel,
   making it possible for example to use some information from a central
   system such as active directory while storing data specific to your
   Plone site in the ZODB.

**User Enumeration**
   User enumeration plugins implement the searching logic for users.
