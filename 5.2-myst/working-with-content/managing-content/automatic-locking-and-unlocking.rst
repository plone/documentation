Automatic Locking and Unlocking
====================================

Plone gives you a locking message that will tell you that a document was locked, by whom, and how long ago - so you won't accidentally stomp on somebody else's changes.

When somebody clicks on the Edit tab, that item immediately becomes locked.
This feature prevents two people from editing the same document at the same time, or accidentally saving edits over another user's edits.



If a user leaves the edit page without clicking Save or Cancel, the content locking will remain effective for the next ten minutes after
which time, the locked content item becomes automatically unlocked.

This timeout feature is important for some browsers that do not execute the "on-unload" javascript action properly, such as Safari.
Should you desire to disable locking, go to the Plone control panel (Site Setup -> Site) and uncheck *Enable locking for through-the-web edits*.

Finally, users with the role "Site-Admin" can override the lock and unlock it.
