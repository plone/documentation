=========================
Enabling HTML Embed Codes
=========================

.. admonition:: Description

    You can set up Plone so it will not allow you to paste the code necessary to embed videos,
     slideshows or music players from popular websites such as Flickr, YouTube, Google Maps and MySpace.

    Learn how to adjust the HTML filtering to achieve the desired level of safety versus convenience.

.. figure:: ../../_robot/filter-setup.png
   :align: center
   :alt: HTML filter setup configuration


.. warning::

   Making these configuration changes has serious security implications for your site !


.. note::

   Plone filters out many tags for a good reason:
   they can be abused by your site users to create privilege escalation attacks.

   If you have allowed untrusted people to create content on your Plone site, then a malicious person could create some "nasty" JavaScript in some content,
   then trick a person with Admin rights into viewing that content.

   That "nasty" JavaScript can now do HTTP requests to interact with the Plone site with the full Admin rights granted to the trusted user.

*Bottom line: do not use this technique to enable embeddable content in your Plone site unless you are certain that you trust all
users who are allowed to create content in your site.*

Plone 5
=======

In Plone 5, there are two steps you need to take in order to embed content that is not using an *iframe* tag:

.. note::

   Per default, Plone 5 will allow <iframe> as a valid tag.
   That enables embedding media from the most popular sites like Vimeo and YouTube.

   This behavior is a change from earlier versions.
   If you are in a high-security environment, add "iframe" to the list of *nasty tags* and embedding will stop working.


First, go to Site Setup>TinyMCE Visual Editor then click on the Toolbar tab.

- Enable the checkbox next to "Insert/edit Media"
- Scroll down to the bottom of the screen and click "Save"


Then, go to Site Setup>HTML Filtering

- Remove "Object" and "Embed" from the "Nasty Tags" list
- Remove "Object" and "Param" from the "Stripped Tags" list
- Add "Embed" to the "Custom Tags" list
- Scroll down to the bottom of the screen and click "Save"


With these changes made, you should be able to click newly-added "Embed Media" button in the TinyMCE toolbar.

You can paste in the URL of a YouTube video, and TinyMCE will do the rest for you!

For a Flickr slideshow, and most other embeds, switch into HTML editing mode and paste in the raw embed code.

.. note::

  To allow completely arbitrary HTML codes, see :doc:`WYSIWYG text editing and TinyMCE </develop/plone/forms/wysiwyg>`
  and `David Glick's blogpost <http://glicksoftware.com/blog/disable-html-filtering>`_.
