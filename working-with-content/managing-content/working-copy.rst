Working Copy
==================

Working Copy lets you have two versions of your content in parallel.

**When a Plone site is first created, there a number of additional
features that can be enabled, including "Working Copy". If the Plone
site you are using doesn't show the "Check out" option under the Actions
menu, you will need to contact your site manager and request that
"Working Copy Support (Iterate)" be installed.**

.. include:: ../../_robot.rst
.. code:: robotframework

   *** Variables ***

   @{CONFIGURE_PACKAGES}  plone.app.iterate
   @{APPLY_PROFILES}  plone.app.iterate:plone.app.iterate
   ${REGISTER_TRANSLATIONS}  ${CURDIR}/../../_locales

   *** Test Cases ***

Overview
--------

You might have been in a situation like this before: you have published
a document, and you need to update it extensively, but you want the old
version to exist on the web site until you have published the new one.
You also want the new document to replace the current one, but you'd
like to keep the history of the old one, just in case. Working copy
makes all this possible.

Essentially, you "check out" a version of the currently published
document, which creates a "working copy" of the document. You then edit
the working copy (for as long as you like) and when you're ready for the
new version to go live, you "check in" your working copy, and it's live.
Behind the scenes, Plone will replace the original document with the new
one in the exact same location and web address â€” and archive the old
version as part of the document's version history.

Using "Check out"
-----------------

First, navigate to the page you want check out. Then from the "Actions"
drop-down menu, select "Check out":

.. replaces /_static/01.png
.. figure:: ../../_robot/working-copy_checkout.png
   :align: center
   :alt:
.. code:: robotframework

   Create sample content
       ${folder_id} =  Translate  folder_news_id
       ...  default=news
       ${folder_title} =  Translate  folder_news_title
       ...  default=News
       ${container} =  Create content  type=Folder
       ...  id=${folder_id}  title=${folder_title}

       ${item_id} =  Translate  sample_news_id
       ...  default=website-refresh
       ${item_title} =  Translate  sample_news_title
       ...  default=Welcome to our new site!
       ${item_description} =  Translate  sample_news_description
       ...  default=The long wait is now over
       ${item_text} =  Translate  sample_news_text
       ...  default=<p>Our new site is built with Plone.</p>

       ${item} =  Create content  container=${container}  type=News Item
       ...  id=${item_id}  title=${item_title}
       ...  description=${item_description}  text=${item_text}
       Fire transition  ${item}  publish

   Show how to checkout
       ${folder_id} =  Translate  folder_news_id
       ...  default=news
       ${item_id} =  Translate  sample_news_id
       ...  default=website-refresh
       Go to  ${PLONE_URL}/${folder_id}/${item_id}

       Page should contain element  css=#plone-contentmenu-actions dt a
       Click link  css=#plone-contentmenu-actions dt a
       Wait until element is visible
       ...  css=#plone-contentmenu-actions dd.actionMenuContent

       Mouse over  css=#plone-contentmenu-actions-iterate_checkout
       Update element style  css=a.managePortletsFallback  display  none
       Update element style  portal-footer-wrapper  display  none

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_checkout.png
       ...  contentActionMenus
       ...  css=#portal-column-content

An info message will appear indicating you're now working with a working
copy:

.. replaces /_static/03.png
.. figure:: ../../_robot/working-copy_checkout-notification.png
   :align: center
   :alt:
.. code:: robotframework

   Show checkout notification
       page should contain element
       ...  css=#plone-contentmenu-actions-iterate_checkout
       ${href} =  get element attribute
       ...  css=#plone-contentmenu-actions-iterate_checkout@href

       go to  ${href}

       Element should be visible  css=.portalMessage
       Update element style  css=a.managePortletsFallback  display  none

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_checkout-notification.png
       ...  css=#portal-column-content

Now you're free to edit your own local copy of a published document.
During this time, the original document is "locked" -- that is, no one
else can edit that published version while you have a working copy
checked out. This will prevent other changes from being made to (and
subsequently lost from) the published version while you edit your copy.

.. replaces /_static/locked.png
.. figure:: ../../_robot/working-copy_locked.png
   :align: center
   :alt:
.. code:: robotframework

   Show locked original
       ${folder_id} =  Translate  folder_news_id
       ...  default=news
       ${item_id} =  Translate  sample_news_id
       ...  default=website-refresh
       Go to  ${PLONE_URL}/${folder_id}/${item_id}

       Element should be visible  css=#plone-lock-status
       Update element style  css=a.managePortletsFallback  display  none

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_locked.png
       ...  css=#portal-column-content

Using "Check in"
----------------

When you are ready to have your edited copy replace the published one,
simply choose "Check-in" from the "Actions" drop-down menu:

.. replaces /_static/04a.png
.. figure:: ../../_robot/working-copy_checkin.png
   :align: center
   :alt:
.. code:: robotframework

   Show check-in option
       ${folder_id} =  Translate  folder_news_id
       ...  default=news
       ${item_id} =  Translate  sample_news_id
       ...  default=website-refresh
       Go to  ${PLONE_URL}/${folder_id}/copy_of_${item_id}

       Element should be visible  css=#plone-lock-status

       Click link  css=#plone-contentmenu-actions dt a
       Wait until element is visible
       ...  css=#plone-contentmenu-actions dd.actionMenuContent

       Mouse over  css=#plone-contentmenu-actions-iterate_checkin
       Update element style  css=a.managePortletsFallback  display  none
       Update element style  portal-footer-wrapper  display  none

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_checkin.png
       ...  contentActionMenus
       ...  css=#portal-column-content

You will then be prompted to enter a Check-in message. Fill it out and
click on "Check in":

.. replaces /_static/04b.png
.. figure:: ../../_robot/working-copy_checkin-form.png
   :align: center
   :alt:
.. code:: robotframework

   Show checkin form
       Page should contain element
       ...  css=#plone-contentmenu-actions-iterate_checkin
       ${href} =  Get element attribute
       ...  css=#plone-contentmenu-actions-iterate_checkin@href

       Go to  ${href}

       Element should be visible  css=#checkin_message
       ${checkin_message} =  Translate  checkin_message
       ...  default=Update news item ingress
       Input text  css=#checkin_message  ${checkin_message}

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_checkin-form.png
       ...  css=#portal-column-content

Your updated document will now replace the published copy and become the
new published copy.

.. replaces /_static/05.png
.. figure:: ../../_robot/working-copy_checkin-confirmation.png
   :align: center
   :alt:
.. code:: robotframework

   Show checkin confirmation

       Click button  form.button.Checkin

       Page should not contain  css=#plone-lock-status
       Page should contain element  css=.portalMessage.info
       Update element style  css=a.managePortletsFallback  display  none

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_checkin-confirmation.png
       ...  css=#portal-column-content

You will also notice that there is no longer a copy of the document in
the user's personal folder.

Note that it is not necessary (and in fact, it is not recommended) to
use the "State" drop-down menu on a working copy. If you inadvertently
do so, however, don't panic. Just go back to your working copy and use
"Check in" from the "Actions" menu.

Canceling a "Check out"
-----------------------

If for any reason it becomes necessary to cancel a check out and **you
don't want to save any of your changes**, simply navigate to the working
copy and select "Cancel check-out":

.. replaces /_static/cancel1.png
.. figure:: ../../_robot/working-copy_cancel-checkout.png
   :align: center
   :alt:
.. code:: robotframework

   Show cancel checkout
       ${folder_id} =  Translate  folder_news_id
       ...  default=news
       ${item_id} =  Translate  sample_news_id
       ...  default=website-refresh
       Go to  ${PLONE_URL}/${folder_id}/${item_id}

       page should contain element
       ...  css=#plone-contentmenu-actions-iterate_checkout
       ${href} =  get element attribute
       ...  css=#plone-contentmenu-actions-iterate_checkout@href

       go to  ${href}

       Element should be visible  css=.portalMessage

       Click link  css=#plone-contentmenu-actions dt a
       Wait until element is visible
       ...  css=#plone-contentmenu-actions dd.actionMenuContent

       Mouse over  css=#plone-contentmenu-actions-iterate_checkout_cancel
       Update element style  css=a.managePortletsFallback  display  none
       Update element style  portal-footer-wrapper  display  none

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_cancel-checkout.png
       ...  contentActionMenus
       ...  css=#portal-column-content

You will prompted to confirm the "Cancel checkout" or to "Keep
checkout":

.. replaces /_static/cancel2.png
.. figure:: ../../_robot/working-copy_cancel-checkout-form.png
   :align: center
   :alt:
.. code:: robotframework

   Show cancel checkout form

       Page should contain element
       ...  css=#plone-contentmenu-actions-iterate_checkout_cancel
       ${href} =  Get element attribute
       ...  css=#plone-contentmenu-actions-iterate_checkout_cancel@href

       Go to  ${href}

       Element should be visible  name=form.button.Cancel

       Capture and crop page screenshot
       ...  ${CURDIR}/../../_robot/working-copy_cancel-checkout-form.png
       ...  css=#portal-column-content

Note that if the user who has checked out a working copy is not
available to check in or cancel a check out, users with the Manager role
may navigate to the working copy and perform either the check in or
cancel check out actions. That's because not all contributors have the
*Check in* privilege. If that option is missing from your *Actions*
menu:

#. Use the *State* menu.
#. Submit for publication.
#. Ask a reviewer to **not** change the state.
#. Ask the reviewer to perform the check in on your behalf instead.

The check in routine will handle the state.
