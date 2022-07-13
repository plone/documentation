Portlet Hierarchy
======================

Portlets use a basic hierarchy approach which determines how and why they appear on each section of your site.

By default, the portlets that you assign at the root (homepage) of the site will propogate down to all the subsections of the site.

If you want a different set of portlets or order of portlets for a particular sub-section, you can use the **Block/unblock portlets** controls, to "block" the parent portlets.
When you block Portlets, you must explicitly add all the Portlets that
you wish to see on the child page.

There are some specific sets of portlets:

Group Portlets
    Created by your Site Manager for Groups of Users.
Content Type Portlets
    Assigned in the Plone Control Panel to specific Content Types by your Site Manager .

They can be blocked or unblocked separately from the (much more used) "Parent portlets"

.. note::

    Beware of the :doc:`default view for a Folder </working-with-content/managing-content/folder-view>`.

    When you set about creating Portlets that you want to propagate, be careful to that you are creating the Portlet at the Site Root or Folder and not at the Default View for that folder.

In this diagram, our Portlets are designated in blue underneath the Page
title:

.. figure:: /_static/hierarchy.png
   :align: center

   Portlet Hierarchy

As you can see we have two Portlets designated on our Home page (navigation and recent items).
These same Portlets appear on our About Page because of portlet hierarchy.

However, on the Documentation page we added a third portlet - the Collection Portlet.
Here we are still allowing Parental Portlets, but in addition we specifically added the Collection Portlet.

On **both** the Tutorials and Videos Pages we have to block Parental Portlets because we do not want the Collection Portlet that is on the Documentation Page to show.
When we block Parental Portlets we must re-add the Portlets to **each** Child page.
In this case we re-added the Navigation Portlet to both and then added the Search Portlet to both.

Remember that the child pages only inherit from the parent page directly above them.
In our example, if we added a page called *Staff* under About and allowed the parent portlets without adding any additional portlets, it would show the same Portlets as the Home Page as well as the About Page.
However do not think that it is inheriting from the Home page.
If we were to change the About Page and added a Search Portlet, our Staff Page would reflect the Portlets on the About Page not the Home
Page.

