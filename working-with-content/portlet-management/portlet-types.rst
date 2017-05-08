=============
Portlet Types
=============

Descriptions of each Portlet Type

There are several different types of Portlets to choose from.

.. note::

   These are the default portlets for Plone 5.
    Your site may have more available, as many add-ons come with their own portlets.

Navigation
==========

The Navigation Portlet **allows users to navigate your site** with ease by providing a structured "site map", or navigation tree.

You have the option to display the navigation for the overall site or choose to display the current folder contents.

As you dig deeper into the site, the tree will continue to expand.

There are several configuration options available that effect how the Navigation Portlet will behave.

You can set the *Title*, the *Root node* (which is from where the tree will start), and various other options to limit how deep you want to expand the tree.

Calendar
========

The Calendar Portlet is a simple Portlet that will display a Calendar on your site.

The main use is to highlight "Events".

You can choose what the workflow state of the Events (or other items like it) should be, and can choose whether you want all events on your site or only the ones within a given subfolder.

If you have published Event content objects on your site, the days upon which they occur will be highlighted in the calendar and will link to the corresponding events on your site.

Collection
==========

The Collection Portlet will allow you to **display the results of a Collection**.

You must have a Collection previously created when you add this Portlet, then you can specifying the Collection to be used.

This is a great way to present targeted queries like for example "newest pages with tag "Latin America".

Events
======

The Events Portlet will **display Upcoming Events**, provided that you have Events on your site.
You can determine how many events you want to be displayed and also which events you want to display based on publishing state.

Log in
======

The Log in Portlet is another non configurable Portlet that will simply **display a Log in Form** that will allow users with Log in information to log in to the site.

Once a user is logged into the site, this Portlet will not appear.

News
====

The News Portlet works exactly like the Events Portlet.

Instead of displaying Events, it **displays recent News items**.

Once again you can choose how many News items are displayed and filter them based on their state.

.. note::

   Both the "News" and "Events" portlets could be created by using a "Collection" portlet which finds the right content items.

   They are provided for convenience.

RSS Feeds
=========

The RSS Feed Portlet allows you to link to an RSS Feed, choose how many items to display, and specify the refresh rate.

Recent Items
============

The Recent Items Portlet displays a customizable **number of Recent Items**, listed by Title.
A Recent Item is determined by its Last Modified Date.

Review List
===========

The Review List Portlet will display a **list of objects that have been submitted for review**.

If you are using a submit and review cycle (and have properly set global roles for your users) this is a great way for reviewers to see what content has been submitted for review.

This Portlet only appears to those logged in as this state is not viewable to the public.

Search
======

The Search Portlet will place a search box in your Portlet Column.
This search box will search the Titles, Descriptions, and Body text of objects on your site for the text specified.

You have the option of enabling Live Search.

Live Search is a feature which shows live results if the browser supports JavaScript.

Static Text
===========

The Static Text Portlet allows you to enter content just as you would on a normal Page object.
This is useful for adding for example contact information, your company motto, or any information that is relatively static.


Classic
=======

A Classic Portlet is refers to the way portlets were used in older version of Plone, prior to Plone 3.

You must create a Page Template in the Management Interface and properly set the path and macro to enable the portlet.

This requires technical knowledege of both TALES and the Management Interface.

.. warning::

   The 'classic' portlet is provided strictly for sites that have very old legacy code.

   You should refrain from using it in any modern Plone site.
