Content to Template
===================

How content reaches a Page Template.

There are three ways in which content from your content items can reach
a page.

-  directly from a content item
-  from the catalog
-  via a view component (using Python)

Getting content directly from a content item
--------------------------------------------

A page template can pull data directly from the content item it is
displaying. Here’s a snippet of the RSS template, calling the
description field of a Collection content item:

::

    <description>
        <metal:block define-slot="description">
           <tal:block content="context/Description">
              Default rss description goes here
           </tal:block>
        </metal:block>
    </description>

-  *context*\ refers to the current content item
-  *Description*\ is the accessor of the description field

Accessors
~~~~~~~~~

An accessor is simply the method by which data in a field is extracted.
In most cases the name of an accessor is the field name with the first
letter capitalized and prefaced by 'get' (e.g., getStartTime). There's
an exception to this rule. The title and description field, common to
most content types, have 'Title' and 'Description' as their accessors
(i.e. no 'get', but the first letter is capitalized).

Widgets
~~~~~~~

This snippet from the news item template does exactly the same thing but
calls a specific display "widget" macro for the field rather than just
the data.

::

    <p class="documentDescription">
     <metal:field use-macro="python:here.widget('description',  mode='view')">
         .....
    </metal:field>
    </p>

Getting content from the catalog
--------------------------------

Every content item is catalogued on creation and editing. Some of its
fields are indexed for quick searching and sorting, while the values of
others are stored in what's called the "brains" or "metadata" for quick
access.

Pages pulling together a number of content types - a folder or
collection listing for instance - often get their content from a catalog
query and the brains, rather than waking up every content item in turn.
You'll normally find a variable defined somewhere which holds the
results of a catalog query:

::

    folderContents here.queryCatalog(contentFilter);

Then the template will loop through the results and call values from the
brains/metadata:

::

    item_url item/getURL;
    item_id item/getId;

These look pretty much like normal accessors, in fact they are the names
of fields in the catalog brains/metadata. This can get confusing - if
you try to access a field which isn't in the brains/metadata you'll get
an error.

You can see what fields are available to you via

-  Site Setup > Zope Management Interface > portal\_catalog > metadata
   tab

If you want to understand more about the catalog, there is a useful,
general overview in the `Zope
book <http://www.plope.com/Books/2_7Edition/SearchingZCatalog.stx>`_,
and a more Plone-specific runthrough in `The Definitive Guide to
Plone <http://docs.neuroinf.de/PloneBook/ch11.rst#searching-and-categorizing-content>`_
(this book is for Plone 2 only, but the catalog section is still
relevant to Plone 3).

Getting content via Python (using a view component)
---------------------------------------------------

It is often more efficient to use a view to process the data from the
content item (or a group of content items) and then drop it into the
page template. In this case, by "view" we mean a specific component
defined in ZCML.

Here’s a snippet calling a view to render the sitemap:

::

    <ul id="portal-sitemap"
        class="navTreeLevel0 visualNoMarker"
        tal:define="view context/@@sitemap_view;">
         <tal:sitemap replace="structure view/createSiteMap" />
    </ul>

-  *context/@@sitemap\_view* is assigned to a variable called
   (helpfully) 'view'
-  *createSiteMap* is a method of @@sitemap\_view
-  @@ indicates that this is a view component

Here's the wiring in ZCML that creates @@sitemap\_view:

::

    <browser:page
         for="*"
    (there’s no restriction on where I can be used)
         name="sitemap_view"
    (this is my name)
         class=".sitemap.SitemapView"
    (this is where you can find the code to deliver my content)
         permission="zope.Public"
    (you can see me if you have the Public permission)
         allowed_interface=".interfaces.ISitemapView"
    />

In summary

-  the content is processed by a Python class
-  ZCML wires this class up into a component
-  the template calls this component

 

 
