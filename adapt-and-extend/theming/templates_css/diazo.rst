======================
 Diazo theming
======================

.. admonition:: Description

    Theming Plone and integrating external sites under one theme service
    using Diazo.

.. contents:: :local:

Introduction
-------------

Diazo is the new name of what was previously known as XDV.
Diazo, like XDV, is an external HTML theming engine, a.k.a. theming proxy, which allows 
you to mix and match HTML and CSS from internal and external sites 
by using simple XML rules. It separates the theme development from the site development, 
so that people with little HTML and CSS knowledge can create themes
without need to know underlying Python, PHP or whatever. It also enables
integration of different services and sites to one, unified, user experience. 
For more information, you can always read the `wikipedia article <http://en.wikipedia.org/wiki/Diazo_%28software%29>`_

Example backends to perform diazo transformation include:

* ``plone.app.theming`` (as a normal Plone add-on)

* Apache's ``mod_transform``

* Nginx web server transform module

Diazo theming can be used together with Plone, in which case enhanced
support is provided by the 
`plone.app.theming package <https://pypi.python.org/pypi/plone.app.theming>`_. 
(This is the Plone integration package for Diazo, like
`collective.xdv package <https://pypi.python.org/pypi/collective.xdv>`_
was the integration package for XDV)
Technically, ``plone.app.theming`` adds a Plone settings panel (Diazo)
and does XSL transformation in Zope's post-publication hook using the
``lxml`` library.

The community (Martin Aspeli) is currently working on an online theme
editing interface, so designers can make a diazo theme for a Plone site
entirely through the web.
For more information, have a look at his 
`branch of plone.app.theming <https://github.com/plone/plone.app.theming/tree/optilude-ace>`_.

Diazo can be used standalone with 
`Diazo package <https://pypi.python.org/pypi/diazo>`_ to theme any web site, 
whether it's Wordpress, Joomla, Drupal or a custom in-house PHP solution
from the year 2000.


Theming editing interface (backend)
=====================================

The editing interface, backend, or admin site, however you wish to call it,
can also be themed with ``plone.app.theming``. 
If you don't want to theme the editing interface, however,
you can fallback to the default Plone theme.

There are several reasons for this:

* The Plone editing interface is powerful and has very good
  usability, which means that it is internally quite complex
  (makes complex things to pose itself as a simple to the end user).
  
* The public theme you are building would not fit to the 
  editing interface very well. E.g. no space for portlets.
  This is especially problematic if an external
  artist has created the visuals without properly
  fitting them for Plone. 
  
With Diazo you can easily also have a separate ``admin.yoursite.com``
domain where the Plone editing interface is untouched.  

Related links
-------------

* https://pypi.python.org/pypi/plone.app.theming
 
* https://pypi.python.org/pypi/diazo

* http://diazo.org

* http://plone.org/products/collective.examples.diazo


Creating your first Diazo theme package
---------------------------------------

.. commented out as missing resource gives sphinx error.
.. :doc:`ZopeSkel package </tutorials/paste>` includes XDV theme skeleton
.. since version 2.20.

to be documented

Setting up Diazo
----------------

If you are working with Plone you can integrate ``plone.app.theming`` to
your site's existing buildout. 

If you are not working with Plone, the 
`Diazo home page <http://docs.diazo.org/en/latest/installation.html>`_
has instructions how to deploy the Diazo command standalone.

Diazo Rules 
-----------

Rules (``rules.xml``) will tell how to fit content from external sources to
your theme HTML.

It provides straightforward XML-based syntax to manipulate HTML easily:

* Append, replace and drop HTML pieces

* Insert HTML snippets

* CSS or XPath selectors can be used to identify HTML parts
  
* It is possible to mix and match content from more than two sites

* etc.

Rules XML syntax is documented at the
`Diazo homepage <http://docs.diazo.org>`_.

The actual theming is done by one of the XSL backends listed above,
by taking HTML as input and applying XSL transformations on it.

Dropping specific CSS files with Diazo
--------------------------------------

For example if you wish to get rid of the ``base-cachekey????.css`` file
that comes from a Plone site,
but still want to keep the authoring CSS and any special CSS
files that come from add-ons::

    <drop content="/html/head[style *=
    'portal_css/Plone%20Default/base-cachekey']/style" />


Benefits of using Diazo theming instead of creating native Wordpress (or other) themes
--------------------------------------------------------------------------------------

* You need to maintain only one theming add-on product
  e.g. one for your main CMS and Wordpress receives 
  updates to this site and theme automatically

* Wordpress does not need to be touched

* You can host your Wordpress on a different server,
  even wordpress.com, and still integrate it to your main CMS

* The theme can be recycled not only for Wordpress, but also
  other external services: Bugzilla, Trac, Webmail, phpBB,
  you-name-it  


Applying the theme in Apache production environment
=====================================================

http://docs.diazo.org/en/latest/deployment.html#apache
