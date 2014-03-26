Portlet Hierarchy
======================

Portlets use a basic hierarchy approach which determines how and why
they appear on each section of your site.

Portlets use a basic hierarchical approach. By default, the portlets
that you assign at the root (homepage) of the site will propogate down
to all the subsections of the site. If you want a different set of
portlets or order of portlets for a particular sub-section, you must use
the **Block/unblock portlets** controls, to "block" the parent portlets.
When you block Portlets, you must explicitly add all the Portlets that
you wish to see on the child page.

The portlet management screen has been updated in Plone 4 to show all
portlets, including portlets that are blocked. Users can now see what's
being blocked and what's being inherited. When a portlet is blocked, you
will notice a subtle change in color on on the portlet management
screen:

.. figure:: ../_static/blocked_portlets.png
   :align: center
   :alt: Blocked portlets in management

   Blocked portlets in management

In this diagram, our Portlets are designated in blue underneath the Page
title:

.. figure:: ../_static/hierarchy.gif
   :align: center
   :alt: hierarchy.gif

   hierarchy.gif

As you can see we have two Portlets designated on our Home page
(navigation and recent items). These same Portlets appear on our About
Page because of portlet hierarchy.

However, on the Documentation page we added a third portlet - the
Collection Portlet. Here we are still allowing Parental Portlets, but in
addition we specifically added the Collection Portlet.

On **both** the Tutorials and Videos Pages we have to block Parental
Portlets because we do not want the Collection Portlet that is on the
Documentation Page to show. When we block Parental Portlets we must
re-add the Portlets to **each** Child page. In this case we re-added the
Navigation Portlet to both and then added the Search Portlet to both.

Remember that the child pages only inherit from the parent page directly
above them. In our example, if we added a page called *Staff* under
About and allowed the parent portlets without adding any additional
portlets, it would show the same Portlets as the Home Page as well as
the About Page. However do not think that it is inheriting from the Home
page. If we were to change the About Page and added a Search Portlet,
our Staff Page would reflect the Portlets on the About Page not the Home
Page.

