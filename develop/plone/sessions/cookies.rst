=======
Cookies
=======

.. topic:: Description

    Handling cookies in Plone


Introduction
============

Cookies in Plone are read from the request and set on the response.
There are methods on request and response for cookie handling.
Reading the raw cookie direct from the request header is still possible, but not needed.
Same is valid for setting or expiring cookies on the response.


Reading cookies
===============

Incoming cookies are sent by the browser in the request header.
The incoming request was already parsed by the publisher.
Cookies are available as ``cookies`` mapping variable on the request.

.. code-block:: python

    self.request.cookies.get("cookie_name", "default_value_if_cookie_not_set")

Setting cookies
===============

Setting cookies is done on the response.
Each cookie name there can be a new or an existing one.
When sending the response, the information is turned into a properly formatted ``Set-Cookie`` header.

.. code-block:: python

    self.request.response.setCookie("cookie_name", "cookie_value")

A cookie may have `cookie-attributes <https://en.wikipedia.org/wiki/HTTP_cookie#Cookie_attributes>`_ set.
Those are passed as keyword arguments to ``setCookie``.
Turning a cookie into a non-session cookie requires an ``expires='date'`` keyword and value.
Limiting the cookie to a path requires a ``path='/somepath'`` keyword and value for the ``setCookie()`` method.
The usual browser cookie rules apply here.

.. code-block:: python

    self.request.response.setCookie(
        "cookie_name",
        "cookie_value",
        quoted=False,  # default is True
        attribute_on_cookie="attribute value",
        another_attribute="another attribute value",
    )


Clearing cookies
================

If a cookie needs to be removed, the browser has to be told to expire it.
The ``expireCookie`` method does this.
It always sets ``max_age`` to ``0`` and the ``expires`` date to the past.
Additionally the cookie value will be set to ``deleted``.

.. code-block:: python

    self.request.response.expireCookie("cookie_name")

The method ``expireCookie`` allows additional attributes to be passed as keyword arguments, similar to ``setCookie``.
The aforementioned keywords ``max_age``, ``expires``, and ``value`` are reserved and are not allowed.
A common keyword used here is ``path``.


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

Authentication cookie
---------------------

The ``__ac`` cookie is set by the PluggableAuthentication service after login.
For better and more secure control over the cookie and its lifetime `plone.session <https://pypi.org/project/plone.session/>`_ can be used.


Zope session cookie
-------------------

This cookie looks like::

	_ZopeId="25982744A40dimYreFU"

It is set first time when session data is written.

Language cookie
---------------

The cookie ``I18N_LANGUAGE`` is set by Plone ``portal_languages`` tool.

The cookie can be disabled.
Be aware, after disabling the cookie, language switching using the language selector viewlet is no longer functional.
To disable the cookie, untick the checkbox :guilabel:`Use cookie for manual override` in Plone controlpanel :guilabel:`Language` under :guilabel:`Negotiation Scheme`.

Also, language cookie has a special lifecycle when plone.app.multilingual is installed.
This may affect your front-end web server caching.
If configured improperly, the language cookie gets set on images and static assets like CSS HTTP responses.

* http://stackoverflow.com/questions/5715216/why-plone-3-sets-language-cookie-to-css-js-registry-files-and-how-to-get-rid-o


Sanitizing cookies for the cache
================================

You do not want to store HTTP responses with cookies in a front end cache server, because this would be a leak of other users' information.

Do not cache pages with cookies set.
Also with multilingual sites it makes sense to have unique URLs for different translations as this greatly simplifies caching (you can ignore language cookie).

Note that cookies can be set:

* by the server (Plone itself)

* on the client side, by JavaScript (Google Analytics)

... so you might need to clean cookies for both incoming HTTP requests and HTTP responses.

:doc:`More info in Varnish section of this manual </manage/deploying/caching/varnish3>`.


Late cleanup of HTTP response cookies
=====================================

You can do this after all processing is done and before the transaction is committed by subscribing to the ``ZPublisher.interfaces.IPubBeforeCommit`` event.

Put the code below in a file ``cleancookies.py``.

.. code-block:: python

    """Clean I18N cookies from non-HTML responses.
    E.g. Image content, which has language set, and is cross-linked across page,
    do not inadvertently change the language.
    """

    from zope.interface import Interface
    from zope.component import adapter
    from ZPublisher.interfaces import IPubBeforeCommit


    @adapter(Interface, IAfterPublicationEvent)
    def clean_language(object, event):
        """ Clean up cookies after HTTPResponse object has been constructed completely.

        Post-publication handler.
        """
        request = event.request

        # All non-HTML payloads
        if (
            not event.request.response.headers["content-type"].startswith("text/html"):
            and "I18N_LANGUAGE" in request.response.cookies
        ):
            del request.response.cookies["I18N_LANGUAGE"]


Register the `clean_language` function as a subscriber in ZCML:

.. code-block:: xml

    <subscriber handler=".cleancookies.clean_language" />


Signing cookies
=================

Kind of... crude example

* https://gist.github.com/3951630
