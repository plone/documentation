============
Roles plugin
============

.. contents:: :local:

The ``IRolesPlugin`` plugins determine the global roles for a principal.
Like the other interfaces the ``IRolesPlugin`` interface contains only a
single method::

    def getRolesForPrincipal( principal, request=None ):
        """ principal -> ( role_1, ... role_N )
        o Return a sequence of role names which the principal has.
        o May assign roles based on values in the REQUEST object, if present.
        """

Here is a simple example::

    def getRolesForPrincipal(self, principal, request=None):
        # Only act on the current user
        if getSecurityManager().getUser().getId()!=principal:
            return ()

        # Only act if the request originates from the local host
        if request is not None:
            ip=request.get("HTTP_X_FORWARDED_FOR", request.get("REMOTE_ADDR", ""))
            if ip!="127.0.0.1":
                return ()

        return ("Manager",)

This gives the current user in Manager role if the site is being accessed
from the Zope server itself.
