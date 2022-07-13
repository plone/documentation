===============
Status messages
===============

Status messages are session-bound information which allow the user
to see notifications when the page is rendered next time.

Status messages are stored session in safely manner which prevents
Cross-Site Scripting attacks which might occur due to delivering
message information as HTTP GET query parameters.


Setting a status message
========================

Status messages have text (unicode) and type (str). All pending status messages
are shown to the user when the next page is rendered.

Example::

    from Products.statusmessages.interfaces import IStatusMessage

    messages = IStatusMessage(self.request)

    messages.add(u"Item deleted", type=u"info")

Example which you can use in Python scripts::

    # This message is in Plone i18n domain
    context.plone_utils.addPortalMessage(_(u'You are now logged in. Welcome to supa-dupa-system.'), 'info')

Rendering status message style by hand-crafted HTML
===================================================

If you want to insert elements looking status messages on your page
use the following mark-up

.. code-block:: html

        <dl class="portalMessage error">
            <dt>Error</dt>
            <dd>Login failed. Both login name and password are case sensitive, check that caps lock is not enabled.</dd>
        </dl>

