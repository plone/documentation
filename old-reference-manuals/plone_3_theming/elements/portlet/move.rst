Moving, Removing or Hiding a Portlet
====================================

Some tips on moving or hiding portlets.

Whether or not portlets appear on your site is highly customizable
through the web, you can use the manage portlets link in most contexts.
For more information:

-  `http://plone.org/documentation/tutorial/where-is-what/portlets-1/ <http://plone.org/documentation/tutorial/where-is-what/portlets-1/>`_

It's assumed that you wouldn't want to *fix* portlets on a page
(otherwise they'd probably be viewlets). However, if you wish to set up
an initial assignment of portlets on installation of your theme product,
use

-  [your theme package]/profiles/default/portlets.xml.

Here's an extract from the Plone Default portlets.xml, setting up the
login and navigation portlet for the left-hand column, and the review
and news portlets for the right-hand column.

::

    <?xml version="1.0"?>
    <portlets
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="plone">

     
     <!-- Assign the standard portlets -->
     
     <assignment
         manager="plone.leftcolumn"
         category="context"
         key="/"
         type="portlets.Navigation"
         name="navigation"
         />
     
     <assignment
         manager="plone.leftcolumn"
         category="context"
         key="/"
         type="portlets.Login"
         name="login"
         />
         
      <assignment
         manager="plone.rightcolumn"
         category="context"
         key="/"
         type="portlets.Review"
         name="review"
         />

     <assignment
         manager="plone.rightcolumn"
         category="context"
         key="/"
         type="portlets.News"
         name="news"
         />
         
     
    </portlets>

 The attributes for the assignment directive are described in full here:
`http://plone.org/products/plone/roadmap/203/ <http://plone.org/products/plone/roadmap/203/>`_. 
In brief:

manager and type
    The names for these can be looked up in
    plone.app.portlets.portlets.configure.zcml (for type of portlet) or
    in the Plone Default profiles/default/portlets.xml file.
category
    This can be one of four values "context", "content\_type", "group"
    or "user" - depending on where you wish to assign your portlets.
key
    This will depend on the value given in category above. In the case
    of "context", the location in the site is indicated (the examples
    above specify the site root).

If you wish to configure the portlet in more detail, you can nest
property directives within the assignment directive. Here's a tweak to
ensure the navigation portlet appears at the root of the site:

::

    <assignment name="navigation" category="context" key="/"
        manager="plone.leftcolumn" type="portlets.Navigation">
         <property name="topLevel">0</property>
     </assignment>

