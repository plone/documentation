==============
Cookies
==============

.. admonition:: Description

    Handling session and other cookies in Plone

.. contents:: :local:

Introduction
=================

Setting and getting cookies

* http://www.dieter.handshake.de/pyprojects/zope/book/chap3.html

* http://stackoverflow.com/questions/1034252/how-do-you-get-and-set-cookies-in-zope-and-plone

Reading cookies
==================

Usually you want to read incoming cookies sent by the browser.

Example::

    self.request.cookies.get("cookie_name", "default_value_if_cookie_not_set")

Setting cookies
=====================

See `HTTPResponse.setCookie() <https://github.com/zopefoundation/Zope/blob/master/src/ZPublisher/HTTPResponse.py#L241>`_.

Modifying HTTP response cookies
===================================

You might want to tune up or clean cookies after some other part of Plone code has set them.
You can do this in :doc:`post-publication event handler </develop/plone/serving/http_request_and_response>`.

Example ``cleancookies.py`` (needs ZCML subscriber registration too)::

    """

        Clean I18N cookies from non-HTML responses so that e.g. Image
        content, which has language set, and is cross-linked across page,
        don't inadvertiately change the langauge.

    """

    from zope.interface import Interface
    from zope.component import adapter
    from plone.postpublicationhook.interfaces import IAfterPublicationEvent


    @adapter(Interface, IAfterPublicationEvent)
    def clean_language(object, event):
        """ Clean up cookies after HTTPResponse object has been constructed completely.

        Post-publication handler.
        """
        request = event.request

        #print "%s %s" % (request["URL"], request.response.cookies)

        # All non-HTML payloads
        if not request.response.headers["content-type"].startswith("text/html"):
            # Rip-off I18N_language cookie
            if "I18N_LANGUAGE" in request.response.cookies:
                print "Cleaned up cookie for %s" % request["URL"]
                del request.response.cookies["I18N_LANGUAGE"]


Default Plone cookies
======================

Typical Plone cookies::

	# Logged in cookie
	__ac="NjE2NDZkNjk2ZTMyOjcyNzQ3NjQxNjQ2ZDY5NmUzNjM2MzczNw%253D%253D";

	# Language chooser
	I18N_LANGUAGE="fi";

	# Status message
	statusmessages="BURUZXJ2ZXR1bG9hISBPbGV0IG55dCBraXJqYXV0dW51dCBzaXPDpMOkbi5pbmZv"

	# Google Analytics tracking
	__utma=39444192.1440286234.1270737994.1321356818.1321432528.21;
	__utmz=39444192.1306272121.6.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none);
	__utmb=39444192.3.10.1321432528;
	__utmc=39444192;

	# Plone copy-paste clipboard
	__cp="x%25DA%2515%258AA%250A%25800%250C%2504%25A3%25A0%25E0E%257CF%25FF%25E4%2529%2587%25801%25D5B%25B3-%25F8%257B%25D3%25C3%250E%25CC%25B0i%2526%2522%258D%25D19%2505%25D2%2512%25C0P%25DF%2502%259D%25AB%253E%250C%2514_%25C3%25CAu%258B%25C0%258Fq%2511s%25E8k%25EC%250AH%25FE%257C%258Fh%25AD%25B3qm.9%252B%257E%25FD%25D1%2516%25B3"; Path=/

Zope session cookie
------------------------

This cookie looks like::

	_ZopeId="25982744A40dimYreFU"

It is set first time when session data is written.

Language cookie
-----------------------

``I18N_LANGUAGE`` is set by ``portal_languages`` tool.
Disable it by *Use cookie for manual override* setting in
``portal_languages``.

Also, language cookie has a special lifecycle when LinguaPlone is installed.
This may affect your front-end web server caching. If configured improperly,
the language cookie gets set on images and static assets like CSS HTTP responses.

* http://stackoverflow.com/questions/5715216/why-plone-3-sets-language-cookie-to-css-js-registry-files-and-how-to-get-rid-o

Session cookie lifetime
=========================

Setting session cookie lifetime

* http://plone.org/documentation/kb/cookie-duration

Sanitizing cookies for the cache
====================================

You don't want to store HTTP responses with cookies in a front end cache
server, because this would be a leak of other users' information.

Don't cache pages with cookies set. Also with multilingual sites it makes
sense to have unique URLs for different translations as this greatly
simplifies caching (you can ignore language cookie).

Note that cookies can be set:

* by the server (Plone itself)

* on the client side, by Javascript (Google Analytics)

... so you might need to clean cookies for both incoming HTTP requests and
HTTP responses.

:doc:`More info in Varnish section of this manual </manage/deploying/caching/varnish>`.

Signing cookies
=================

Kind of... crude example

* https://gist.github.com/3951630
