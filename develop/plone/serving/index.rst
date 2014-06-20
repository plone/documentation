=======================================
HTTP serving and traversing site data
=======================================

Serving content from your site to your users is effectively a mechanism to
generate HTTP responses to HTTP requests.

In Plone, answering to HTTP requests can be divided to three subproblems:

* managing the lifecycle of the HTTP request and response pair;
* publishing, by traversing the request to the target object by its URI;
* choosing different parts of the code depending on active layers.

Plone and Zope 2 application servers support FTP, WebDAV and XML-RPC protocols besides plain HTTP.

.. toctree::
   :maxdepth: 1

   http_request_and_response
   traversing
   publishing
   xmlrpc
   webdav
   ftp
