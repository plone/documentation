=======
 WebDAV
=======

.. admonition:: Description

    WebDAV is a protocol to manage your site directly from MS Windows
    Explorer, Mac OS, Linux and so on. Plone supports WebDAV without add-ons, and Plone responds to WebDAV requests out of the box.


Introduction
============

WebDAV is enabled by default in Plone. A Plone server listening on port 8080 will also
accept WebDAV traffic on that port.

.. note::

    WebDAV historically was used  mainly for uploading files in bulk to Plone.
    In Plone 5, this functionality comes standard. For earlier versions, he add-on `collective.wildcardfoldercontents <https://pypi.python.org/pypi/wildcard.foldercontents>`_ provides this.

Connecting to Plone via WebDAV
------------------------------

For common cases, client-side tools should work reasonably well.

`"OS X Mavericks: Connect to a WebDAV server": <https://support.apple.com/kb/PH13859>`_

Permissions
-----------

The "WebDAV access" permission is required for any user to be able to connect to WebDAV.

To allow Plone users (ie. users created within a Plone site, as opposed to users created in Zope) to connect using WebDAV, go to the Security tab of the Zope (e.g. http://yoursite:8080/manage_access), find the permission "WebDAV access", check the box for it under the Anonymous column, and press the Save Changes button.
This generally grants WebDAV connection access.
Normal Plone permissions will take care of who can view or change actual content.

Enabling WebDAV on an extra port in Zope
----------------------------------------

You can have Plone listen for WebDAV requests on additional ports by modifying your buildout configuration's client setup to add a WebDAV address:

Here is a short ``buildout.cfg`` example::



     [instance]
     ...
     recipe = plone.recipe.zope2instance
     ...
     webdav-address=1980
     ...


Here is an alternative ``buildout.cfg`` configuration snippet which might be needed for some WebDAV clients::


   [instance]
   ...
   zope-conf-additional =
       enable-ms-author-via on
       <webdav-source-server>
       address YOUR_SERVER_PUBLIC_IP_ADDRESS_HERE:1980
       force-connection-close off
       </webdav-source-server>


These snippets will be in the **generated** ``parts/instance/etc/zope.conf``
after buildout has been re-run.

This will enable the WebDAV server on http://www.mydomain.com:1980/.

.. note:: You cannot use this URL in your web browser, just in WebDAV clients.

Using the web browser will give you an error message ``AttributeError:
manage_FTPget``. You could also just run the WebDAV server on ``localhost``
with address 1980, forcing you to either use a WebDAV client locally or
proxy WebDAV through Apache.

Disabling WebDAV
----------------

You can't disable WebDAV in Plone itself; it's tightly integrated in Zope.
You could take away the "WebDAV access" permission from everyone, but the
Zope server will still answer each request.

What you can do is make your web server filter out the WebDAV commands;
this will stop WebDAV requests before they reach your Zope server.

Nginx
~~~~~

For nginx, this is done by adding::


	dav_methods off

to the server block in your nginx.conf. (http://wiki.nginx.org/HttpDavModule)

If you do not use the HttpDavModule, you can add::


    limit_except GET POST {
     deny   all;
    }

to the location block.

Apache
~~~~~~

For Apache, you can use the ``limit`` statement, see http://httpd.apache.org/docs/current/mod/core.html#limit


.. seealso:: `"How can I stop people accessing a Plone server via WebDAV?" <http://stackoverflow.com/questions/9127269/how-can-i-stop-people-accessing-a-plone-server-via-webdav>`_


Supporting WebDAV in your custom content
========================================

Please read more about it in the `Dexterity WebDAV manual <https://github.com/plone/plone.dexterity/blob/master/docs/WebDAV.txt>`_.
