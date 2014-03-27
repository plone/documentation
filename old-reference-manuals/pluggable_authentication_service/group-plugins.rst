=============
Group plugins
=============

.. contents:: :local:

Group plugins return the identifiers for the groups a principal is a
member of. Since a principal can be either a user or a group this means
that PAS can support nested group members. The default PAS configuration
does not support this though.

Like other PAS interfaces, the ``IGroupsPlugin`` interface is simple and
only specifies a single method::

    def getGroupsForPrincipal(principal, request=None):
        """ principal -> ( group_1, ... group_N )
        o Return a sequence of group names to which the principal
          (either a user or another group) belongs.
        o May assign groups based on values in the REQUEST object, if present
        """

Here is a simple example::

    def getGroupsForPrincipal(self, principal, request=None):
        # Manager can not be itself
        if principal == "Manager":
            return ()

        # Only act on the current user
        if getSecurityManager().getUser().getId() != principal:
            return ()

        # Only act if the request originates from the local host
        if request is not None:
            ip=request.get("HTTP_X_FORWARDED_FOR", request.get("REMOTE_ADDR", ""))
            if ip != "127.0.0.1":
                return ()

        return ("Manager",)

This puts the current user in the Manager group if the site is being
accessed from the Zope server itself.
