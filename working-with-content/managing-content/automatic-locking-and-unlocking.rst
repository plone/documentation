Automatic Locking and Unlocking
====================================

Plone gives you a locking message that will tell you that a document was
locked, by whom, and how long ago — so you won't accidentally stomp on
somebody else's changes.

When somebody clicks on the Edit tab, that item immediately becomes
locked. This feature prevents two people from editing the same document
at the same time, or accidentally saving edits over another users edits.
In this example, George Schrubb has started editing the "Widget
Installation" document. When Jane Smythe (who has permissions to edit
that document as well) goes to view it, she will see the following:

.. figure:: ../_static/locking01.png
   :align: center
   :alt: locking01.png

   locking01.png

Once George has finished editing the document and clicks the Save
button, the document is automatically unlocked and available to be
edited by others (should they have the proper permissions to do so, of
course).

However, if it becomes clear to Jane that George isn't really editing
the document anymore (e.g. the locking message says that the item was
locked several days ago and not just a few minutes ago) then Jane can
"unlock" it and make it available for editing again.

In Plone 3.3 or higher:
If a user leaves the edit page without clicking Save or Cancel, the
content locking will remain effective for the next ten minutes after
which time, the locked content item becomes automatically unlocked. This
timeout feature is important for browsers that do not execute the
"on-unload" javascript action properly such as Safari.
Should you desire to disable locking, go to the Plone control panel
(Site Setup -> Site) and uncheck *Enable locking for through-the-web
edits*.

