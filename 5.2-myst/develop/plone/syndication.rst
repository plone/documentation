===========
Syndication
===========


Introduction
-------------

In Plone 4.3, there is a new syndication framework that allows you to customize
how content in your site is syndicated.


Customize how a content type is syndicated
------------------------------------------

In this example, we'll show how to customize how News items are syndicated on
your site.


Create adapter
~~~~~~~~~~~~~~

We'll create an adapter that overrides the body text::

    from Products.CMFPlone.browser.syndication.adapters import BaseItem
    from Products.CMFPlone.interfaces.syndication import IFeed
    from Products.ATContentTypes.interfaces import IATNewsItem
    from zope.component import adapts

    class NewsFeedItem(BaseItem):
        adapts(IATNewsItem, IFeed)

        @property
        def body(self):
            return 'Cooked:' + self.context.CookedBody()


Register Adapter
~~~~~~~~~~~~~~~~

Example:

.. code-block:: xml

    <adapter
      factory=".NewsFeedItem"
      for="Products.ATContentTypes.interfaces.IATNewsItem
           Products.CMFPlone.interfaces.syndication.IFeed"
      provides="Products.CMFPlone.interfaces.syndication.IFeedItem" />

Dexterity type
~~~~~~~~~~~~~~

If the type you're customizing is a dexterity type then Plone will use the
Products.CMFPlone.browser.syndication.DexterityItem adapter by default for adopting
Dexterity content to syndication.IFeedItem. You can override the default adapter by
registering your own adapter this way:


.. code-block:: python

    from zope.component import adapts
    from Products.CMFPlone.interfaces.syndication import IFeed
    from plone.dexterity.interfaces import IDexterityContent
    from Products.CMFPlone.browser.syndication.adapters import DexterityItem

    class MyAdapter(DexterityItem):
        adapts(IMyType, IFeed)

        @property
        def link(self):
            return '...some custom url'

        guid = link


.. code-block:: xml

    <adapter
      factory=".adapters.MyAdapter"
      for="my.package.mytype.IMyType
           Products.CMFPlone.interfaces.syndication.IFeed"
      provides="Products.CMFPlone.interfaces.syndication.IFeedItem" />


Register your Folderish type as syndicatable
--------------------------------------------

Just make sure it implements the ISyndicatable interface::

    from Products.CMFPlone.interfaces.syndication import ISyndicatable

    ...
    class MyFolderishType(object):
        implements(ISyndicatable)
    ...


Create your own feed type
-------------------------

Example of creating your own simple feed type and registering it.

Create your feed template:

.. code-block:: xml

    <?xml version="1.0" ?>
    <feed xml:base=""
        xml:lang="en"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        xmlns:tal="http://xml.zope.org/namespaces/tal"
        tal:define="feed view/feed;
                    url feed/link;"
        tal:attributes="xml:base url; xml:lang feed/language"
        i18n:domain="Products.CMFPlone">
    <link rel="self"
            href=""
            tal:attributes="href request/ACTUAL_URL" />
    <title type="html" tal:content="feed/title" />
    <subtitle tal:content="feed/description" />
    <updated tal:content="python:feed.modified.ISO8601()" />
    <link tal:attributes="href url" rel="alternate" type="text/html" />
    <id tal:content="string:urn:syndication:${feed/uid}" />
    <tal:repeat repeat="item feed/items">
        <entry tal:define="published item/published;
                        modified item/modified;">
        <title tal:content="item/title"></title>
        <link rel="alternate" type="text/html" href="" tal:attributes="href item/link" />
        </entry>
    </tal:repeat>
    </feed>


Register the view in ZCML:

.. code-block:: xml

    <browser:page
        for="Products.CMFPlone.interfaces.syndication.ISyndicatable"
        class="Products.CMFPlone.browser.syndication.views.FeedView"
        name="myfeed.xml"
        permission="zope2.View"
        template="myfeed.xml.pt"
        />


Finally, register the feed view in the control panel `syndication-settings`
in the `Allowed Feed Types` setting. You should be able to append a new feed
type like this::

    myfeed.xml|My Feed Type


Now, if the `My Feed Type` is enabled on a syndicatable item(you'll probably
also need to allow editing syndication settings), you'll be able to append
`myfeed.xml` onto the url to use the new syndication.


Creating a json feed type
~~~~~~~~~~~~~~~~~~~~~~~~~

First, we'll create the json feed view class::

    from Products.CMFPlone.browser.syndication.views import FeedView
    import json

    class JSONFeed(FeedView):

        def index(self):
            data = []
            feed = self.feed()
            for item in feed.items:
                data.append({
                    'link': item.link,
                    'title': item.title,
                    'description': item.description
                })
            return json.dumps(data)


Then register the adapter with ZCML:

.. code-block:: xml

    <browser:page
        for="Products.CMFPlone.interfaces.syndication.ISyndicatable"
        class=".JSONFeed"
        name="json"
        permission="zope2.View"
        />


Finally, register the feed view in the control panel `syndication-settings`
in the `Allowed Feed Types` setting. You should be able to append a new feed
type like this::

    json|JSON


Now, if the `JSON` is enabled on a syndicatable item(you'll probably
also need to allow editing syndication settings), you'll be able to append
`json` onto the url to use the new syndication.


Available FeedItem properties to override
-----------------------------------------

If you're inheriting Products.CMFPlone.browser.syndication.adapters.BaseItem
or Products.CMFPlone.browser.syndication.adapters.DexterityItem in an attempt
to override the default feed item behavior, these are the properties available
to you to override:

* link
* title
* description
* categories
* published
* modified
* uid
* rights
* publisher
* author
* author_name
* author_email
* body
* guid
* has_enclosure
* file
* file_url
* file_length
* file_type


Available feed properties to override
-------------------------------------

If you're inheriting from Products.CMFPlone.browser.syndiction.adapters.FolderFeed
in an attempt to override the functionality of a feed folder or collection,
these are the available properties to override:

* link
* title
* description
* categories
* published
* modified
* uid
* rights
* publisher
* logo
* icon
* items
* limit
* language

