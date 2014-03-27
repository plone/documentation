==========
Challenges
==========

.. contents :: :local:

.. admonition:: Description

        If the current (possibly anonymous) user is not authorised to access a resource Zope asks
        PAS to challenge the user. Generally this will result in a login form being shown, asking
        the user with a appropriately priviliged account.

The IChallengeProtocolChooser and IChallengePlugins plugins work together to do this. Since Zope can be accessed via various protocols (browsers, WebDAV, XML-RPC, etc.) PAS first needs to figure out what kind of protocol it is dealing with. This is done by quering all IChallengeProtocolChooser plugins. The default implementation is ChallengeProtocolChooser, which asks all IRequestTypeSniffer plugins to test for specific protocols.

Once the protocol list has been build PAS will look at all active IChallengePlugins plugins.
Writing a plugin

The IChallengePlugin interface is very simple: it only contains one method::

   def challenge( request, response ):
       """ Assert via the response that credentials will be gathered.
       Takes a REQUEST object and a RESPONSE object.
       Returns True if it fired, False otherwise.
       Two common ways to initiate a challenge:
         - Add a 'WWW-Authenticate' header to the response object.
           NOTE: add, since the HTTP spec specifically allows for
           more than one challenge in a given response.
         - Cause the response object to redirect to another URL (a
           login form page, for instance)
       """

The plugin can look at the request object to determine what, or if, it needs to do. It can then modify the response object to issue its challenge to the user. For example::

   def challenge(self, request, response):
       response.redirect("http://www.disney.com/")
       return True

this will redirect a user to the Disney homepage every time he tries to access something he is not authorised for.
