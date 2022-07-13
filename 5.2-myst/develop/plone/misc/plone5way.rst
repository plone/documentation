=============================
Looking ahead towards Plone 5
=============================

Concerns regarding removal of portal_skins and reliance on browser views
------------------------------------------------------------------------


Specific Things We Like to Do with portal_skins
-----------------------------------------------


This document includes a bunch of specific use cases showing how we as
integrators typically rely on portal_skin.

Nathan Van Gheem's responses below are indented.


Live Sites
----------

We can modify live sites’ appearance without having to touch the file system by
putting things in the custom folder.



    Plone has, and will always try to provide a rich TTW editing and
    customization story. This is true with plone.app.theming and diazo. If all
    skins are removed, we WILL provide an alternative way to customize template
    TTW. Right now, it looks to me like making portal_view_customizations work
    better.


No Filesystem or Buildout Access
--------------------------------

We often do not have access to the file system nor can we run buildout.


    See Live Sites response.

Customizing a collection’s display
----------------------------------

We have some custom content types that we want to display using a collection.
We build the collection and specify “item type”.  We want the display to show
fields that are unique to the custom content types.  We locate the collection
view template, customize it, rename it (to, say, custom_collection_view),
enhance it to show the additional field values, then in portal_types we add the
new custom_collection_view to the list of available views for Topics.  The
collection’s “Display” menu now includes the new custom_collection_view.


    First off, best case we still have a story to do the exact same thing only
    with portal_view_customizations.

    Secondly, it can be easier to hit that use-case with a combination of
    collective.listingviews and diazo. There has been discussion of integrating
    a lot of what collective.listingviews does and more into plone.app.theming.


Creating a cloned content type so that it has a different default view
----------------------------------------------------------------------

Let’s say a site has a custom content type based on Document but we want to have
the default view include boilerplate text around the rich text and description.
We would go to portal_types, clone the Document type, rename the cloned type
“Project”.  Then we go to portal_skins, find document_view, customize it,
rename it to project_view, and add the boilerplate text we want.  Then back in
portal_types for Project, we change the default view to project_view.  This way,
anywhere in the site we create a Project object, its default view (its only
view) shows the boilerplate text we wanted.


    Cloned content types will still be available with dexterity. In fact, it’ll
    be incredibly more robust and powerful.


    For the views, look to the previous point about using
    collective.listingviews and diazo.


Classic Portlets
----------------

We use classic portlets a lot to put together (quickly) something that displays
arbitrary content.


    There is nothing scheduled to get rid of portlet or the classic portlet
    right now. portal_skins will still be there.


    That being said, I might need more specific use-cases of how you’re using
    classic portlets in order to explain how it’d be a replacement.


Things We Don’t Like About Having to Rely Only on Browser Views
===============================================================


Why browser views are hard for integrators (non-developers):

* We may not have file system access
* We may not want to have to (and are not in fact able to) create a product to
  register a new view
* We may not want to have to re-run buildout (nor are we able to) to register a
  new view
* Unless a browser view is correctly registered, customizing it via
  portal_view_customizations breaks Python methods associated with the view


    I hope I’ve addressed your concerns. The final point is valid and a concern
    of mine also. We’ll need to make sure there is a way to customize all
    templates safely. I sort of hope people simply won’t be doing TTW
    customizations of templates as much anymore though and they’ll just use
    diazo with something like listingviews.

    Others might have different ideas about how things will work. Dylan Jay
    might be someone that can give really good answers regarding these questions.

    A good discussion regarding some of these issues can be found at:
    http://plone.293351.n2.nabble.com/enhanced-collections-views-td7565206.html;cid=1372262563684-127

    The final response there has a good overview.
