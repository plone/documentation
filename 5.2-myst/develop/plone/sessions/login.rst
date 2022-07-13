================
Login and logout
================

.. admonition:: Description

    Login and logout related programming activities in Plone

Introduction
============

This chapter contains login and logout related code snippets.

Login entry points
------------------

There are two login points in Plone

``/login`` view (appended to any content URL) directs you to the page where you came from after the login.

``/login_form`` view does login without the redirect back to the original page.

In addition, the ``/logout`` action logs the user out.

The logic that drives the login process is implemented using the CMF form controller framework (legacy). To customize it, you need to override one or more of the ``login_*`` scripts. This can be accomplished in two ways: register your own skin directory or use `z3c.jbot <https://pypi.python.org/pypi/z3c.jbot>`_. Note that in both cases, you need to copy the ``.metadata`` file as well.


Extracting credentials
----------------------

Extracting credentials try to extract log-in (username, password) from HTTP request.

Below is an example how to extract and authenticate the user manually.
It is mostly suitable for unit testing.
Note that given login field isn't necessarily the username. For example,
`betahaus.emaillogin <https://pypi.python.org/pypi/betahaus.emaillogin>`_ add-on authenticates users by their email addresses.

Credential extraction will go through all plug-ins registered for
`PlonePAS <https://github.com/plone/Products.PlonePAS/blob/master/README.rst>`_ system.

The first found login/password pair attempt will be used for user authentication.

Unit test example::

    def extract_credentials(self, login, password):
        """ Spoof HTTP login attempt.

        Functional test using zope.testbrowser would be
        more appropriate way to test this.
        """

        request  = self.portal.REQUEST

        # Assume publishing process has succeeded and object has been found by traversing
        # (this is usually set by ZPublisher)
        request['PUBLISHED'] = self.portal

        # More ugly ZPublisher stubs
        request['PARENTS'] = [self.portal]
        request.steps = [self.portal]

        # Spoof HTTP request login fields
        request["__ac_name"] = login
        request["__ac_password"] = password

        # Call PluggableAuthService._extractUserIds()
        # which will return a list of user ids  extracted from the request
        plugins = self.portal.acl_users.plugins

        users = self.portal.acl_users._extractUserIds(request, plugins)

        if len(users) == 0:
            return None

        self.assertEqual(len(users), 1)

        # User will be none if the authentication fails
        # or anonymous if there were no credential fields in HTTP request
        return users[0]


Authenticating the user
=======================

Using username and password
---------------------------

Authenticating the user will check that username and password are correct.

Pluggable Authentication Service (acl_users under site root)
will go through all authentication plug-ins and return the first successful
authenticated users.

Read more in
`PlonePAS <https://github.com/plone/Products.PlonePAS/blob/master/README.rst>`_.

Unit test example::

    def authenticate_using_credentials(self, login, password):

        request = self.portal.REQUEST

        # Will return valid user object
        user = self.portal.acl_users.authenticate(login, password, request)
        self.assertNotEqual(user, None)


Using username only
-------------------

Useful for sudo style logins.

::

    def loginUser(self, username):
        """
        Login Plone user (without password)
        """
        self.context.acl_users.session._setupSession(username, self.context.REQUEST.RESPONSE)
        self.request.RESPONSE.redirect(self.portal_state.portal_url())

See also

* https://github.com/miohtama/niteoweb.loginas/blob/master/niteoweb/loginas/browser/login_as.py

Post-login actions
-------------------

Post-login actions are executed after a successful login. Post-login actions which you could want to change are

* Where to redirect the user after login

* Setting the status message after login

You can use the `collective.onlogin <https://pypi.python.org/pypi/collective.onlogin>`_ package to set up many actions for you.

If you need more control, post-login code can be executed with :doc:`events </develop/addons/components/events>` defined in
PluggableAuthService service.

* ``IUserLoggedInEvent``

* ``IUserInitialLoginInEvent`` (logs for the first time)

* ``IUserLoggedOutEvent``

Here is an example how to redirect a user to
a custom folder after he/she logs in (overrides standard Plone login behavior)

``configure.zcml``::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        i18n_domain="my.package">

        <subscriber
            for="Products.PluggableAuthService.interfaces.events.IUserLoggedInEvent"
            handler=".postlogin.logged_in_handler"
            />

    </configure>

``postlogin.py``::

    # Python imports
    import logging

    # ZODB imports
    from ZODB.POSException import ConflictError

    # Zope imports
    from AccessControl import getSecurityManager
    from zope.interface import Interface
    from zope.component import getUtility
    from zope.app.component.hooks import getSite
    from zope.globalrequest import getRequest

    # CMFCore imports
    from Products.CMFCore import permissions

    # Plone imports
    from Products.CMFPlone.interfaces.siteroot import IPloneSiteRoot

    # Logger output for this module
    logger = logging.getLogger(__name__)

    #: Site root relative path where we look for the folder with an edit access
    CUSTOM_USER_FOLDERS = "fi/yritykset"


    def redirect_to_edit_access_folder(user):
        """
        Redirects the user to a folder he/she has editor access.

        This is for use cases where you have a owned content
        (e.g. company/product data) on a shared site.

        You want to make it simple for the users with limited knowledge to edit their own data
        by redirecting to the edit view right after the login.

        :return: URL if we should redirect, otherwise None
        """

        # Fetch the site related to the current HTTP request
        portal = getSite()

        # Look for portal relative paths where the items are
        try:
            target = portal.unrestrictedTraverse(CUSTOM_USER_FOLDERS)
        except ConflictError:
            # Transaction retries must be
            # always handled specially in exception handlers
            raise
        except Exception, e:
            # Let the login proceed even if the folder has been deleted
            # don't make it impossible to login to the site
            logger.exception(e)
            return None

        # Check if the current user has Editor access
        # in the any items of the folder
        sm = getSecurityManager()

        for obj in target.listFolderContents():
            if sm.checkPermission(permissions.ModifyPortalContent, obj):
                logger.info("Redirecting user %s to %s" % (user, obj))
                return obj.absolute_url() + "/edit"

        logger.warn("User %s did not have his/her own content item in %s" % (user, target))

        # Let the normal login proceed to the page "You are now logged in" etc.
        return None


    def logged_in_handler(event):
        """
        Listen to the event and perform the action accordingly.
        """

        user = event.object

        url = redirect_to_edit_access_folder(user)
        if url:
            request = getRequest()
            if request is None:
                # HTTP request is not present e.g.
                # when doing unit testing / calling scripts from command line
                return

            # check if came_from is not empty, then clear it up, otherwise further
            # Plone scripts will override our redirect
            if request.get('came_from', None):
                request['came_from'] = ''
                request.form['came_from'] = ''
            request.RESPONSE.redirect(url)


Post-logout actions
===================

Products.PlonePAS.tools.membership fires ``Products.PlonePAS.events.UserLoggedOutEvent``
when the user logs out via *Log out* menu item.

.. note::

	You cannot catch session timeout events this way... only explicit logout
	action.

Example ZCML

.. code-block:: xml


    <subscriber for="Products.PlonePAS.events.UserLoggedOutEvent"
        handler=".smartcard.clear_extra_cookies_on_logout" />

Example Python::

	def clear_extra_cookies_on_logout(event):
	    """
	    Logout event handler.

	    When user explicitly logs out from the Logout menu, clear our privileges smartcard cookie.
	    """

	    # Which cookie we want to clear
	    cookie_name = SmartcardHelper.PRIVILEDGED_COOKIE_NAME

	    request = event.object.REQUEST
	    # YES CAPS LOCK WAS MUST WHEN ZOPE 2 WAS INVENTED
	    # SOMEWHERE AROUND NINETIES. THEN IT WAS THE CRUISE
	    # CONTROL FOR COOLNESS AND ZOPE IS SOO COOOOOL.
	    response = request.RESPONSE
	    # Voiding our special cookie on logout
	    response.expireCookie(cookie_name)


More info

* https://github.com/plone/Products.PlonePAS/blob/master/Products/PlonePAS/tools/membership.py#L645

Entry points to logged in member handling
=========================================

See ``Products.PluggableAuthService.PluggableAuthService._extractUserIds()``.
It will try to extract credentials from incoming HTTP request, using
different "extract" plug-ins of PAS framework.

``PluggableAuthService`` is also known as ``acl_users`` persistent
object in the site root.

For each set of extracted credentials, try to authenticate
a user;  accumulate a list of the IDs of such users over all
our authentication and extraction plugins.

``PluggableAuthService`` may use :doc:`ZCacheable </manage/deploying/performance/ramcache>`
pattern to see if the user data exists already in the cache, based on
any extracted credentials, instead of actually checking whether
the credentials are valid or not. PluggableAuthService must
be set to have cache end. By default it is not set,
but installing LDAP sets it to RAM cache.

More info

* https://github.com/plone/plone.app.ldap/blob/master/plone/app/ldap/ploneldap/util.py

PAS cache settings
==================

Here is a short view snippet to set PAS cache state::

    from Products.Five.browser import BrowserView
    from zope.app.component.hooks import getSite

    from Products.CMFCore.utils import getToolByName

    class PASCacheController(BrowserView):
        """
        Set PAS caching parameters from browser address bar.
        """

        def getPAS(self):
            site=getSite()
            return getToolByName(site, "acl_users")

        def setPASCache(self, value):
            """
            Enables or disables pluggable authentication service caching.

            The setting is stored persistently in PAS

            This caches credentials for authenticated users after the first login.

            This will make authentication and permission operations little bit faster.
            The downside is that the cache must be purged if you want to remove old values from there.
            (user has been deleted, etc.)

            More info

            * https://github.com/plone/plone.app.ldap/blob/master/plone/app/ldap/ploneldap/util.py

            """

            pas = self.getPAS()

            if value:

                # Enable

                if pas.ZCacheable_getManager() is None:
                    pas.ZCacheable_setManagerId(manager_id="RAMCache")

                pas.ZCacheable_setEnabled(True)

            else:
                # Disable
                pas.ZCacheable_setManagerId(None)
                pas.ZCacheable_setEnabled(False)


        def __call__(self):
            """ Serve HTTP GET queries.
            """

            cache_value = self.request.form.get("cache", None)

            if cache_value is None:
                # Output help text
                return "Use: http://localhost/@@pas-cache-controller?cache=true"

            value = (cache_value == "true")

            self.setPASCache(value)

            return "Set value to:" + str(value)

... and related ZCML

.. code-block:: xml

    <browser:page
     for="Products.CMFCore.interfaces.ISiteRoot"
     name="pas-cache-controller"
     class=".pascache.PASCacheController"
     permission="cmf.ManagePortal"
    />


Login as another user ("sudo")
==============================

If you need to login to production system another user and you do not know the password,
there is an add-on product for it

*  https://pypi.python.org/pypi/niteoweb.loginas

Another option

* https://pypi.python.org/pypi/Products.OneTimeTokenPAS

Getting logged in users
-----------------------

.. TODO:: Was somewhere, but can't find where.

Locking user account after too many retries
-------------------------------------------

For security reasons, you might want to locking users after too many tries of logins.
This protects user accounts against brute force attacks.

* https://github.com/collective/Products.LoginLockout/tree/master/Products/LoginLockout

Hyperlinks to authenticated Plone content in Microsoft Office
---------------------------------------------------------------------------

Microsoft Office applications (in the first instance Word and Excel), have
been observed to attempt to resolve hyperlinks once clicked, prior to sending
the hyperlink to the user's browser. If such a link points to some
Plone content that requires authentication, the Office application will
request the URL first, and receive a 302 Redirect to the ``require_login``
Python script on the relevant Plone instance.  If your original hyperlink
was like so::

    http://example.com/myfolder/mycontent

and this URL requires authentication, then the Office application will send
your browser to this URL::

    http://example.com/acl_users/credentials_cookie_auth/require_login?came_from=http%3A//example.com/myfolder/mycontent

Normally, this isn't a problem if a user is logged out at the time. They will
be presented with the relevant login form and upon login, they will be
redirected accordingly to the ``came_from=`` URL.

However, if the user is *already* logged in on the site, visiting this URL
will result in an ``Insufficient Privileges`` page being displayed.  This is
to be expected of Plone (as this URL is normally only reached if the given
user has no access), but because of Microsoft Office's mangling of the URL,
may not necessarily be correct as the user may indeed have access.

The following drop-in replacement for the ``require_login`` script has been
tested in Plone 4.1.3 (YMMV).  Upon a request coming into this script,
it attempts (a hack) to traverse to the given path. If permission is actually
allowed, Plone redirects the user back to the content. Otherwise, things
proceed normally and the user has no access (and is shown the appropriate
message)::

    ## Script (Python) "require_login"
    ##bind container=container
    ##bind context=context
    ##bind namespace=
    ##bind script=script
    ##bind subpath=traverse_subpath
    ##parameters=
    ##title=Login
    ##

    login = 'login'

    portal = context.portal_url.getPortalObject()
    # if cookie crumbler did a traverse instead of a redirect,
    # this would be the way to get the value of came_from
    #url = portal.getCurrentUrl()
    #context.REQUEST.set('came_from', url)

    if context.portal_membership.isAnonymousUser():
        return portal.restrictedTraverse(login)()
    else:
        expected_location = context.REQUEST.get('came_from')
        try:
            #XXX Attempt a traverse to the given path
            portal.restrictedTraverse(expected_location.replace(portal.absolute_url()+'/',''))
            container.REQUEST.RESPONSE.redirect(expected_location)
        except:
            return portal.restrictedTraverse('insufficient_privileges')()

For further reading see:

* http://plone.293351.n2.nabble.com/Linking-to-private-page-from-MS-Word-redirect-to-login-form-td5495131.html
* http://plone.293351.n2.nabble.com/Problem-with-links-to-files-stored-in-Plone-td3055014.html
* http://bytes.com/topic/asp-classic/answers/596062-hyperlinks-microsoft-applications-access-word-excel-etc
* https://community.jivesoftware.com/docs/DOC-32157

Single Sign-On and Active Directory
===================================

Plone can be used in a Microsoft Active Directory environment (or standard Kerberos environment) such that users are automatically
and transparently authenticated to Plone without requesting credentials from the user.

This is quite an advanced topic and requires some set up on the server, but can be achieved with Plone running on either Unix/Linux
or Windows environments.

More details can be found in this presentation from Plone Open Garden 2013:

* http://www.slideshare.net/hammertoe/plone-and-singlesign-on-active-directory-and-the-holy-grail
* http://www.youtube.com/watch?v=-FLQxeD5_1M

Preventing duplicate logins from different browsers
===================================================

* http://stackoverflow.com/questions/2562385/limit-concurrent-user-logins-in-plone-zope

