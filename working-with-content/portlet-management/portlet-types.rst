Portlet Types
==================

Descriptions of each Portlet Type

There are several different types of Portlets to chose from. The way
that Portlet types are named can be confusing at times. Also, some can
be configured through Manage Portlets and others require some setup
through the ZMI or by creating other content objects first. Below is a
basic description of the use and functionality of each available Portlet
type.

Navigation
-----------

The Navigation Portlet **allows users to navigate your site** with ease
by providing a structured "site map", or navigation tree. You have the
option to display the navigation for the overall site or choose to only
display the current folder contents. On LearnPlone.Org, you can see an
example of the Navigation Portlet in the left column. As you dig deeper
into the site, the tree will continue to expand. There are several
configuration options available that effect how the Navigation Portlet
will behave.

Calendar
--------

The Calendar Portlet is a very simple Portlet that will display a
Calendar on your site. This Portlet has no customizable options. If you
have published Event content objects on your site, the days upon which
they occur will be bolded in the calendar and will link to the
corresponding events on your site.

Classic
-------

A Classic Portlet is refers to the way portlets were used in older
version of Plone, prior to Plone 3. You must create a Page Template in
the ZMI and properly set the path and macro to enable the portlet. This
requires technical knowledege of both TALES and the ZMI.

Collection
----------

The Collection Portlet will allow you to **display the results of a
Collection**. You must have a Collection previously created when you add
this Portlet, then you can specifying the Collection to be used . This
is a great way to summarize the results of an important Collection so
that it is easily viewable to the public. For instructions on creating a
Collection Portlet follow this
`How-to <http://plone.org/documentation/manual/plone-4-user-manual/portlet-management/resolveuid/eb8800b7a664b35d069ddbcae7e4c837>`_.

Events
------

The Events Portlet will **display Upcoming Events**, provided that you
have Events on your site. You can determine how many events you want to
be displayed and also which events you want to display based on
publishing state.

Log in
------

The Log in Portlet is another non configurable Portlet that will simply
**display a Log in Form** that will allow users with Log in information
to log in to the site. Once a user is logged into the site, this Portlet
will not appear.

News
----

The News Portlet works exactly like the Events Portlet. However instead
of displaying Events, it **displays recent News items**. Once again you
can choose how many News items are displayed and filter them based on
their state.

RSS Feeds
---------

The RSS Feed Portlet allows you to link to an RSS Feed, choose how many
items to display, and specify the refresh rate.

Recent Items
------------

The Recent Items Portlet displays a customizable **number of Recent
Items**, listed by Title. A Recent Item is determined by its Last
Modified Date.

Review List
-----------

The Review List Portlet will display a **list of objects that have been
submitted for review**. If you are using a submit and review cycle (and
have properly set global roles for your users) this is a great way for
reviewers to see what content has been submitted for review. This
Portlet only appears to those logged in as this state is not viewable to
the public.

Search
------

The Search Portlet will place a search box in your Portlet Column. This
search box will search the Titles, Descriptions, and Body text of
objects on your site for the text specified. You have the option of
enabling Live Search. Live Search is a feature which shows live results
if the browser supports JavaScript.

Static Text
-----------

The Static Text Portlet allows you to enter content just as you would on
a normal Page object. This is useful for adding hyperlink to different
sites or any information that will not change. An example of this
Portlet is the "Still Stumped?" Portlet on the right hand side of this
site. For more on Static Text Portlets and an example view the How-to
`Static
Portlets <http://plone.org/documentation/manual/plone-4-user-manual/portlet-management/resolveuid/3698a06fc5f57d6f9bd6eaf1824f5cc8>`_.
