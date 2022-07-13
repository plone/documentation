===
RSS
===

.. admonition:: Description

        Programming RSS feeds on Plone sites

.. contents :: local

Introduction
------------

Plone can generate RSS feeds from folderish content types (folder / collection).
If you want to aggregate content from all the site to RSS feed, you first create
a collection content item and then enable RSS feed on this collection content item.

Creating a global, language neutral, Plone site content aggregator
-----------------------------------------------------------------------

These instructions tell you how to create a RSS feed collection for your Plone site.
You can choose what content types ends up to the RSS stream. Also,
the aggregator is language aware so that it works correctly on multilingual sites.

Creating the collection
========================
First we create a collection which will aggregate all the site content
for the RSS feed.

* Go to site root

* Add new collection

* Title "Your site name - RSS feed"

* On *Category* tab, set *Language* to neutral

* On *Settings* tab, choose *Exclude from navigation*

* Save

* Go to site root / *Contents* tab

* Check your RSS content collection

* Choose *Rename* button

* Change item id to ``site-feed``

Collecting content for the RSS feed
====================================

* Go to your collection content item

* Go to *criteria* tab

* Set *content types* criteria

* Set sort by publishing date, reverse

* Save

* Now, choose content items you want to appear in the feed and *Save* again

You can now preview the content of RSS feed
on *View* tab.

Linking the RSS feed to site action links
===========================================

*Site actions* is the top right link slot on the Plone site.
By default, Plone site wide RSS link will appear there if enabled.

* Go to portal_actions in the Management Interface

* Go to */portal_actions/site_actions/rss*

* In URL expression type::

        string:${object/@@plone_portal_state/portal_url}/site-feed/RSS?set_language=${object/@@plone_portal_state/language}

This expression will

* Get URL for *site-feed* object, using *RSS* template

* Will explicitly set HTTP GET query parameter *set_language* which can be used to manually
  force Plone content language. We use the current language (from the user cookie) here,
  to make sure that the user gets RSS feed in correct language on multilingual sites.

More about :doc:`expressions </develop/plone/functionality/expressions>`.

Publish and test
================

Publish collection after the content seems to be right, using the workflow
menu on the collection content item.

Test RSS feed by copy-pasting RSS URL from the site action to your RSS Reader, like
*Google Reader*.

Syndication Settings
--------------------

Plone <= 4.2
============

``portal_syndication`` is a persistent utility  managing RSS settings.
It provides settings to for formatting RSS feeds (frequency of updates, number of items).

* https://github.com/plone/Products.CMFPlone/blob/4.2.x/Products/CMFPlone/SyndicationTool.py

Plone >= 4.3
============

In Plone 4.3, the ``portal_syndication`` utility was replaced by a browser view and registry settings.

The view may be traversed to from any context with ``@@syndication-util``.

for example, in Plone 4.2 you check for the ability to syndicate a context like so:

.. code-block:: html

    <p class="discreet"
       tal:condition="context/portal_syndication/isSiteSyndicationAllowed">
        <a href=""
           class="link-feed"
           i18n:translate="title_rss_feed"
           tal:define="here_url context/@@plone_context_state/object_url"
           tal:attributes="href string:$here_url/search_rss?${request/QUERY_STRING}">
             Subscribe to an always-updated feed of these search terms</a>
    </p>

In Plone 4.3, this is updated to look like this:

.. code-block:: html

    <p class="discreet"
       tal:condition="context/@@syndication-util/search_rss_enabled">
        <a href=""
           class="link-feed"
           i18n:translate="title_rss_feed"
           tal:define="here_url context/@@plone_context_state/object_url"
           tal:attributes="href string:$here_url/search_rss?${request/QUERY_STRING}">
             Subscribe to an always-updated feed of these search terms</a>
    </p>

The ``syndication-util`` view is found in ``Products.CMFPlone.browser.syndication.utils``

 * https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/syndication/utils.py

Publishing content through RSS in Plone 4
-----------------------------------------

Access /content/synPropertiesForm and publish.

RSS feed content
----------------

RSS feed content is the content of the folder or special stream provided by
the content type.

``portal_syndication`` uses the following logic to pull the content::

        if hasattr(obj, 'synContentValues'):
            values = obj.synContentValues()
        else:
            values = obj.getFolderContents()
        return values


Changing RSS feed template
---------------------------

RSS feed is stored in template *CMFPlone/skins/plone_templates/rss_template*.

Enabling full body text in RSS feed
====================================

See `this example <http://rudd-o.com/en/linux-and-free-software/a-hack-to-enable-full-text-feeds-in-plone>`_.





