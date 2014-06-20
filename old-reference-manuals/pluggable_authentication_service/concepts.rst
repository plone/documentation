========
Concepts
========

.. contents:: :local:

.. admonition:: Description

    PAS has a few basic concepts that you must understand in order to
    develop PAS related code.

There are a few basic concepts used in PAS:

**credentials**
   Credentials are a set of information which can be used to authenticate
   a user.
   This can be a login name and password, an IP address, a session cookie
   or something else.

**user name**
   The user name is the name used by the user to log into the system.
   To avoid confusion between "user id" and "user name" this tutorial will
   use the term login name instead.

**user id**
   All users must be uniquely identified by their user id.
   A user's id can be different than the login name.

**principal**
   A principal is an identifier for any entity within the authentication
   system.
   This can be either a user or a group.
   This implies that it is not legal to have a user and a group with the
   same id!
