Versioning
===============

An overview on how to view the version history of an item, compare
versions, preview previous versions and revert to previous versions.

Creating a new version
--------------------------

Plone includes a versioning feature. By default, the following content
types have versioning enabled:

-  Pages
-  News Items
-  Events
-  Links

Note that all other content types do track workflow history.

Content items can be configured to have versioning enabled/disabled
through the Site Setup â†’ Plone Configuration panel under "Types".

When editing an item, you may use the **change note** field at the
bottom; the change note will be stored in the item's version history. If
the change note is left blank, Plone includes a default note: "Initial
Revision".

A new version is created every time the item is saved. Versioning keeps
track of all kinds of edits: content, metadata, settings, etc.

Viewing the version history
---------------------------

Once an item as been saved, you can use the **History** link found near
the top of the page. Simply click it to show the History overlay:

.. figure:: ../_static/history-viewlet.png
   :align: center
   :alt: history-viewlet.png

   history-viewlet.png

The most recent version is listed first. The History viewlet provides
the following information:

-  The type of edit (content or workflow)
-  Which user made the edit
-  What date and time the edit occurred

Comparing versions
------------------

From the History viewlet you can compare any previous version with the
current version or any other version with the version just before it.

To compare any previous version with the one just before it, click the
*Compare* link located between two adjacent versions in the History
overlay.

.. figure:: ../_static/compare-button.png
   :align: center
   :alt: compare-button.png

   compare-button.png

By clicking this button, you'll see a screen like this one where you can
see the differences between the two versions:

.. figure:: ../_static/compare-versions.png
   :align: center
   :alt: compare-versions.png

   compare-versions.png

In this example, text in red is text which has been deleted and text in
green is text which has been added to the newer version. You can toggle
between **inline** or **as code** views of the differences between
versions.

.. figure:: ../_static/versioncompare-src.png
   :align: center
   :alt: Comparing Versions (HTML Source)

   Comparing Versions (HTML Source)

You may also compare any previous version to the *current* version by
clicking the *Compare to current* link History overlay, found to the far
right of each version listed.

Viewing and reverting to previous versions 
------------------------------------------

**You can preview any previous version** of a document by clicking the
*View* link to the right of any version listed.

**To revert back to a previous version**, click on the *Revert to this
revision* button to the right of any version listed.


