===================
Functional testing
===================

.. admonition:: Description

        Functional testing tool allows you to use scripted
        browser to load pages from your site and fill in
        forms automatically.


Introduction
------------

PloneTestCase product provides `FunctionalTestCase <https://github.com/plone/Products.PloneTestCase/blob/master/Products/PloneTestCase/PloneTestCase.py>`_
base class for functional testing. Unlike unit tests, functional tests simulate real HTTP requests with transaction life cycle.

* Functional tests has different transaction for each browser.open() request

* Functional tests do traversing and can check e.g. for cookie based permissions

* Unit test method is executed in a single transaction and this might make impossible to
  test cache related behavior

Test browser
------------

Plone uses Products.Five.testbrowser as an browser emulator used in functional tests.
It is based on zope.testbrowser package.
You can find more information in the `zope.testbrowser docs home page <https://pypi.python.org/pypi/zope.testbrowser>`_. The API is described in `zope.testbrowser.interfaces (3.4 used by Plone 3) <http://svn.zope.org/zope.testbrowser/tags/3.4.2/src/zope/testbrowser/interfaces.py?rev=81337&view=markup>`_.

.. warning::

    There also exists old `zc.testbrowser <https://pypi.python.org/pypi/zc.testbrowser>`_,
    which is a different package with similar name.

All code assumes here is is executed in unit test context where self.portal is your unit test site instance.

Recording tests
----------------

You can record functional tests through the browser. Think it as a Microsoft Word macro recoder kind of thing.

* http://pyyou.wordpress.com/2008/04/11/how-to-install-zopetestrecorder-with-buildout/

* https://pypi.python.org/pypi/zope.testrecorder

Functional test skeleton
------------------------

First see collective.testlayer package which does some of the things
described below

* https://pypi.python.org/pypi/collective.testcaselayer

Example code::

    from Products.Five.testbrowser import Browser
    from Products.PloneTestCase import PloneTestCase as ptc

    class BaseFunctionalTestCase(ptc.FunctionalTestCase):
        """ This is a base class for functional test cases for your custom product.
        """

        def afterSetUp(self):
            """
            Show errors in console by monkey patching site error_log service
            """

            ptc.FunctionalTestCase.afterSetUp(self)

            self.browser = Browser()
            self.browser.handleErrors = False # Don't get HTTP 500 pages


            self.portal.error_log._ignored_exceptions = ()

            def raising(self, info):
                import traceback
                traceback.print_tb(info[2])
                print info[1]

            from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
            SiteErrorLog.raising = raising


        def loginAsAdmin(self):
            """ Perform through-the-web login.

            Simulate going to the login form and logging in.

            We use username and password provided by PloneTestCase.

            This sets session cookie for testbrowser.
            """
            from Products.PloneTestCase.setup import portal_owner, default_password

            # Go admin
            browser = self.browser
            browser.open(self.portal.absolute_url() + "/login_form")
            browser.getControl(name='__ac_name').value = portal_owner
            browser.getControl(name='__ac_password').value = default_password
            browser.getControl(name='submit').click()

Preparing error logger
----------------------

Since zope.testbrowser uses normal Plone paging mechanism, you won't get nice tracebacks to your console.

The following snippet allows you to extract traceback data from site.error_log utility and print it to the console.
Put it to your afterSetUp()::

        self.browser.handleErrors = False
        self.portal.error_log._ignored_exceptions = ()

        def raising(self, info):
            import traceback
            traceback.print_tb(info[2])
            print info[1]

        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

Opening an URL
--------------

Example::

    from Products.Five.testbrowser import Browser

    self.browser = Browser()

    self.browser.open(self.portal.absolute_url())

Logging in
----------

Example::

        from Products.PloneTestCase.setup import portal_owner, default_password

         # Go admin
        browser.open(self.portal.absolute_url() + "/login_form")
        browser.getControl(name='__ac_name').value = portal_owner
        browser.getControl(name='__ac_password').value = default_password
        browser.getControl(name='submit').click()

Logout
------

Example::

    def logoutWithTestBrowser(self):
        """
        """
        self.browser.open(self.portal.absolute_url() + '/logout')
        html = self.browser.contents
        self.assertTrue("You are now logged out" in html)


Showing the contents from the last request
------------------------------------------

After test browser has opened an URL its
content can be read from browser.contents variable.

Example::

    print browser.contents # browser is zope.testbrowser.Browser instance

Getting a form handler
----------------------

You can use testbrowser ``getForm()`` to access different forms on a page.

Form look-up is available by ``name`` or ``index``.

Example::

        form = browser.getForm(index=2) # Skip login and search form on Plone 4

Listing available form controls
-------------------------------

You can do the following to know what content your form has eaten

* the mechanize browser instance that is used through
  zope.testbrowser. zope.testbrowser internally uses a testbrowser
  provided by the mechanize package. The mechanize objects are saved in
  browser.mech_browser and as attributes on different other instances
  returned by zope.testbrowser. mechanize has a different, less convenient
  api, but also provides more options. To see a list of all controls
  in a for you can do e.g.::

    # get the login form from the zope.testbrowser
    login_form = self.browser.getForm('login_form')
    # get and print all controls
    controls = login_form.mech_form.controls
    for control in controls:
       print "%s: %s" % (control.attrs['name'], control.attrs['type'])

... or one-liner ...::

        for c in form.mech_form.controls: print c

* the HTML page source code::

        print browser.contents


Filling in a text field on  a page
-----------------------------------

You can manipulate ``value`` of various form input controls.

Example how to submit Plone search page::


        self.browser.open(self.portal.absolute_url() + "/search")

        # Input some values to the search that we see we get
        # zero hits and at least one hit
        for search_terms in [u"Plone", u"youcantfindthis"]:
            form = self.browser.getForm("searchform")

            # Fill in the search field
            input = form.getControl(name="SearchableText")
            input.value = search_terms

            # Submit the search form
            form.submit(u"Search")



Selecting a checkbox
--------------------

Checkboxes are usually presented as name:list style names::

    checkbox = form.getControl(name="myitem.select:list")
    checkbox.value = [u"selected"]

Clicking a button
-----------------

Example::

    button = form.getControl(name="mybuttonname")
    button.click()

If you have a form instance, you can use the submit action. To click
on the Button labeled "Log in" in the login form, you do::

    login_form = self.browser.getForm('login_form')
    login_form.submit('Log in')

Checking Unauthorized response
------------------------------

Example::

    def checkIsUnauthorized(self, url):
        """
        Check whether URL gives Unauthorized response.
        """

        import urllib2

        # Disable redirect on security error
        self.portal.acl_users.credentials_cookie_auth.login_path = ""

        # Unfuse exception tracking for debugging
        # as set up in afterSetUp()
        self.browser.handleErrors = True

        def raising(self, info):
            pass
        self.portal.error_log._ignored_exceptions = ("Unauthorized")
        from Products.SiteErrorLog.SiteErrorLog import SiteErrorLog
        SiteErrorLog.raising = raising

        try:
            self.browser.open(url)
            raise AssertionError("No Unauthorized risen:" + url)
        except urllib2.HTTPError,  e:
            # Mechanize, the engine under testbrowser
            # uses urlllib2 and will raise this exception
            self.assertEqual(e.code, 401, "Got HTTP response code:" + str(e.code))

Another example where test browser / Zope 2 publisher where invalidly handling Unauthorized exception::

    def test_anon_access_forum(self):
        """
        Anonymous users should not be able to open the forum page.
        """

        self.portal.error_log._ignored_exceptions = ()
        self.portal.acl_users.credentials_cookie_auth.login_path = ""

        exception = None
        try:
            self.browser.open(self.portal.intranet.forum.absolute_url())
        except:
            # Handle a broken case where
            # test browser spits out an exception without a base class (WTF)
            import sys
            exception = sys.exc_info()[0]

        self.assertFalse(exception is None)

Checking a HTTP response header
--------------------------------

Exaple:

        self.assertEqual(self.browser.headers["Content-type"], 'application/octet-stream')

Checking HTTP exception
-------------------------

Example how to check for HTTP 500 Internal Server Error::

    def test_no_language(self):
        """ Check that language parameter is needed and nothing is executed unless it is given. """

        from urllib2 import HTTPError
        try:
            self.browser.handleErrors = True # Don't get HTTP 500 pages
            url = self.portal.absolute_url() + "/@@mobile_sitemap?mode=mobile"
            self.browser.open(url)
            # should cause HTTPError: HTTP Error 500: Internal Server Error
            raise AssertionError("Should be never reached")
        except HTTPError, e:
            pass

Setting test browser headers
-----------------------------

Headers must be passed to underlying PublisherMechanizeBrowser instance
and test browser must be constructed based on this instance.

.. note::

        When passing parameters to PublisherMechanizeBrowser.addheaders HTTP prefix will be automatically added
        to header name.

Add header to browser
=====================

     >>> from Products.Five.testbrowser import Browser
     >>> browser = Browser()
     >>> browser.addHeader(key, value)



Setting user agent
=====================

Example::


    class BaseFunctionalTestCase(ptc.FunctionalTestCase):

        def setUA(self, user_agent):
            """
            Create zope.testbrowser Browser with a specific user agent.
            """

            # Be sure to use Products.Five.testbrowser here
            self.browser = UABrowser(user_agent)
            self.browser.handleErrors = False # Don't get HTTP 500 pages

    from zope.testbrowser import browser
    from Products.Five.testbrowser import PublisherHTTPHandler
    from Products.Five.testbrowser import PublisherMechanizeBrowser

    class UABrowser(browser.Browser):
        """A Zope ``testbrowser`` Browser that uses the Zope Publisher.

        The instance must set a custom user agent string.
        """

        def __init__(self, user_agent, url=None):

            mech_browser = PublisherMechanizeBrowser()
            mech_browser.addheaders = [("User-agent", user_agent),]

            # override the http handler class
            mech_browser.handler_classes["http"] = PublisherHTTPHandler
            browser.Browser.__init__(self, url=url, mech_browser=mech_browser)




For more information, see

* https://mail.zope.org/pipermail/zope3-users/2008-May/007871.html

