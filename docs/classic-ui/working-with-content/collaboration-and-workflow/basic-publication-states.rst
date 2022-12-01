Basic Publication States
=============================

The publication control system for Plone is very flexible, starting with basic settings for making an item private or public.

In the toolbar, for any content type --folders, images, pages, etc., and any specialized content types -- there is an item for publication state. This *state* menu has settings for controlling publication state:

.. figure:: ../../_robot/workflow-basic.png
   :align: center
   :alt: basic workflow menu


The toolbar will show the current publication state for the content item, such as *State: Published*, as shown above.
Private is the initial state when you create a content item -- a page, a news item -- and in the private state, as the name indicates, the content item will generally not be available to visitors to the website.

The *Publish* menu choice will make the content item available on the web site to anonymous visitors.
The *Submit for publication* menu choice is used on web sites where there are content editors who must approve items for publication, as discussed below.

Also, and this will be very important, certain content types, such as news items and events, will not appear on the website as you expect, until they are explicitly *published*.

.. note::

   Store this in your memory: **Publication state is important!**

Publication state can be changed only by users whose accounts have the necessary permissions.
The menu choices in the state menu will reflect existing permissions settings.
For example, in a big newspaper web site, a reporter could add pages for news articles, but the state menu will
not show a *Publish* menu choice, only a *Submit for publication* menu choice.
This is because a reporter must submit articles up the line to the editorial staff for approval before publication.
If your account has the permissions, however, the *Publish* menu choice will appear and you can simply publish in one step.

For an editor, a content item that has been submitted may be *published* or *rejected*, either outright, because it is an inappropriate
submission for the situation, or for the more typical reason that the content item needs revision.

After a content item has been *published*, it may be *retracted*, to change the state back to *public draft* state, or *sent back* to
private, if desired.
The menu choices in the state menu will change accordingly:

.. figure:: ../../_robot/workflow-reject.png
   :align: center
   :alt: basic workflow menu


Instead of completely deleting items in your site that have become obsolete or undesired for some reason, you can also think about retracting ("unpublishing"), or setting to *private*, any content .

Setting to *private* will take the item from public view and from showing up in search results, but will keep it around in case the format or the actual material (text, images, etc.) is needed later, or you later change your mind and want to re-publish the content.

.. note::

   Content that was published once on a public website may have been indexed by search engines. Unpublishing will make it invisible to direct visitors to *your* site, but search engines often keep a copy of it in their indexes. Then again, the same is valid for *deleting* content.

The decision to delete or to set to *private* may depend on whether or not the content exists elsewhere, on another computer or in your company central data storage.
Having large amounts of *private* content on a site might confuse editors, and it will take up some disk space on your webserver.

