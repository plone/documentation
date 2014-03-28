=========================
Enabling HTML embed codes
=========================

.. admonition:: Description

    Normally, Plone will not allow you to paste the code necessary to embed videos, slideshows or music players from popular websites such as Flickr, YouTube, Google Maps and MySpace. Learn how to adjust the HTML filtering to allow this content.


Important security note
------------------------

Making these configuration changes has serious security implications for your site.
Plone filters out the tags that are used for HTML embedding for a good reason:
they can be abused by your site users to create privilege escalation attacks.
If you have untrusted people allowed to create content on your Plone site,
then a malicious person could create some "nasty" Javascript in some content,
then trick a person with Admin rights into viewing that content.
That "nasty" Javascript can now do HTTP requests to interact with the Plone site with the full Admin rights granted to the trusted user.

*Bottom line: do not use this technique to enable embeddable content in your Plone site unless you are certain that you absolutely trust all users who are allowed to create content in your site.*

Plone 4
-------

In Plone 4, there are two steps you need to take in order to easily embed content:

First, go to Site Setup>TinyMCE Visual Editor then click on the Toolbar tab.

- Enable the checkbox next to "Insert/edit Media"
- Scroll down to the bottom of the screen and click "Save"


Then, go to Site Setup>HTML Filtering

- Remove "Object" and "Embed" from the "Nasty Tags" list
- Remove "Object" and "Param" from the "Stripped Tags" list
- Add "Embed" and "iframe" to the "Custom Tags" list
- Scroll down to the bottom of the screen and click "Save"


With these changes made, you should be able to click newly-added "Embed Media" button in the TinyMCE toolbar.  You can paste in the URL of a YouTube video, and TinyMCE will do the rest for you!

For a Flickr slideshow, and most other embeds, switch into HTML editing mode and paste in the raw embed code.

.. note::

  To allow completely arbitrary HTML codes, see `David Glick's blogpost <http://glicksoftware.com/blog/disable-html-filtering>`_