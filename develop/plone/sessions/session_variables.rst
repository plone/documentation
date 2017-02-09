=========
 Sessions
=========

.. admonition:: Description

	How Plone handles anonymous and logged-in user sessions.
	How to store and retrieve session data variables programmatically.

Introduction
============

Sessions are visitor sessions at the site.

Sessions have features like:

* Login and logout, but also identified by a cookie

* Timeout

* Hold arbitrary per-user data on server side

* Identified by cookies

In Plone, sessions are managed by Zope's session_data_manager tool.
The source code is in `Products.Sessions <https://github.com/zopefoundation/Zope/blob/master/src/Products/Sessions/>`_.


Setting a session parameter
===========================

Plone has a tool called ``session_data_manager``.

Example::

    sdm = self.context.session_data_manager
    session = sdm.getSessionData(create=True)
    session.set("my_option", any_python_object_supporting_pickling)


Getting a session
=================

Plone has a convenience method to get the session of the current user::

    session = sdm.getSessionData(create=True)


Getting session id
==================

Each session has a unique id associated with it, for both both anonymous and
logged-in users.

Session data is stored in browser cookies, so sessions are browser-specific.
If the same user has multiple browsers open on your site, each browser will
have its own session.

If you need to refer to the session id, you can query for it::

    sdm = self.context.session_data_manager
    session_id = sdm.getBrowserIdManager().getBrowserId(create=False)
    # Session id will be None if the session has not been created yet


Initial construction of session data
======================================

The example below creates a session data variable when it is accessed for
the first time. For the subsequent accesses, the same object is returned.
The object changes are automatically persisted if it inherits from the
``persistent.Persistent`` class.

.. note::

    Session data stored this way does not survive Plone restart.

Example::

    def getOrCreateCheckoutSession(context, create=False, browser_id=None):
        """ Get the named session object for storing session data.

        Each add-on product can have their own session data slot(s)
        identified by a string name.

        @param context: Any Plone content item with acquisition support

        @param create: Force new data creation, otherwise return None if not exist

        @param browser_id: Cookie id in the user browsers. We can set this
            explicitly if we want to

        @return: ICheckoutData instance
        """

        session_manager = context.session_data_manager
        if browser_id is None:
            if not session_manager.hasSessionData() and not create:
                return
            session = session_manager.getSessionData()
        else:
            session = session_manager.getSessionDataByKey(browser_id)
            if session is None:
                return
        if not session.has_key(CHECKOUT_DATA_SESSION_KEY):
            if create:
                session[CHECKOUT_DATA_SESSION_KEY] = CheckoutData()
            else:
                return None

Deleting session data
======================

Example::

    def _destroyCartForSession(self, context, browser_id=None):
        session_manager = getToolByName(context, 'session_data_manager')
        if browser_id is None:
            if not session_manager.hasSessionData(): #nothing to destroy
                return None
            session = session_manager.getSessionData()
        else:
            session = session_manager.getSessionDataByKey(browser_id)
            if session is None:
                return
        if not session.has_key('getpaid.cart'):
            return
        del session['getpaid.cart']

	
Session data and unit testing
=============================

* Please see http://article.gmane.org/gmane.comp.web.zope.plone.user/104243

Using Plone authentication cookie in other systems
====================================================

* http://stackoverflow.com/questions/12167202/how-to-wrap-plone-authentication-around-a-third-party-servlet/12171528#comment16307483_12171528

Exploring Plone session configuration
======================================

* http://stackoverflow.com/questions/12211682/how-to-export-plone-session-configuration
