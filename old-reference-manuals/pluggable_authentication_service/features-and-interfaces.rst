=======================
Features and interfaces
=======================

.. contents:: :local:

.. admonition:: Description

    A user folder such as PAS provides a number of different services:
    it takes care of user authentication,
    it asks users to login if needed,
    and it allows you to search for users and groups.

In order to make both configuration and implementation simpler 
and more powerful, all these different tasks have been divided 
into different interfaces.
Each interface describes how a specific feature,
such as authenticating a user, has to be implemented.

Within PAS, plugins are used to provide these features.
Plugins are small pieces of logic which implement one or more functions
as defined by these interfaces.

This separation is useful for different reasons:

* it makes it possible to configure different aspects of the system
  separately. 
  For example *how* users authenticate (cookies, login forms, etc.) can be
  configured separately 
  from *where* user information is stored (ZODB, LDAP, RADIUS, SQL, etc.).
  This flexibility makes it very easy to tune the system to specific needs.
* it makes it possible for developers to write small pieces of code 
  that only perform a single task.
  This leads to code that is easier to understand,
  more testable and better maintainable.
