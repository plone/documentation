===================
User factory plugin
===================

.. contents:: :local:

PAS supports multiple user types.
The two default user types are: ``IBasicUser`` and ``IPropertiesUser``.
``IBasicUser`` is a simple user type which supports a user id,
login name, roles and domain restrictions.
``IPropertiedUser`` extends this type and adds user properties.

A user factory plugin creates a new user instance.
PAS will add properties, groups and roles to this instance as part of its
user creation process.

If no user factory plugin is able to create a user, PAS will fall back to
creating a standard ``PropertiedUser`` instance.

The ``IUserFactoryPlugin`` interface is a simple one containing a single
method::

    def createUser( user_id, name ):
        """ Return a user, if possible.
        o Return None to allow another plugin, or the default, to fire.
        """

The default PAS behaviour is demonstrated by this code::

    def createUser(self, user_id, name):
        return ProperiedUser(user_id, name)
