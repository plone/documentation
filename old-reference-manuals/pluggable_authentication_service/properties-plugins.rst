==================
Properties plugins
==================

.. contents:: :local:

Properties are stored in property sheets: 
mapping-like objects, such as a standard python dictionary,
which contain the properties for a principal.
The property sheets are ordered:
if a property is present in multiple property sheets only the property in
the sheet with the highest priority is visible.

Property sheets are created by plugins implementing the 
``IPropertiesPlugin`` interface.
This interface contains only a single method::

    def getPropertiesForUser( user, request=None ):
        """ user -> {}
        o User will implement IPropertiedUser.
        o Plugin may scribble on the user, if needed (but must still
          return a mapping, even if empty).
        o May assign properties based on values in the REQUEST object, if
          present
        """

Here is a simple example::

    def getPropertiesForUser(self, user, request=None):
        return { "email" : user.getId() + "@ourcompany.com" }

this adds an *email* property to a user which is hardcoded to the user id
followed by a company's domain name.
