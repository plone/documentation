Folder Contents
====================

The Contents tab shows a list of items in a folder. It is the place for
simple item-by-item actions and for the manipulative actions of copy,
cut, paste, move, reorder, etc.

The Contents tab for folders is like "File Manager" or "My Computer"
system utilities in Windows and Linux desktops and the "Finder" in Mac
OS X, with similar functionality.

Clicking the *Contents* tab for a folder, such as the "Skippers" folder
below, shows the *Contents* tab panel:

.. figure:: ../_static/foldercontents.png
   :align: center
   :alt: folder-contents.png

   folder-contents.png

The *Contents* tab panel is immediately recognized by observing the
check boxes beside the items in the contents list. Click these check
boxes to select multiple items for performing *copy*, *cut*, *rename*,
*delete*, or *change state* operations.

Plone has a clipboard for *copy* and *cut* operations. If you check one
or more items, and click cut or copy, a paste button will be added to
the row of buttons along the bottom of the panel. If you then click
another folder, you'll be able to paste the items there. For a cut
operation, the items will remain in the source folder -- they won't
disappear -- until they are pasted somewhere.

*Renaming* items will show a panel for entering a new name for the
*short name* (or *id*) of the item, as well as the *title*. The
distinction between *short name* and *title* is one that becomes
apparent only when you rename, because Plone automatically creates the
*short name* from the *title* in most Plone web sites. But the renaming
operation must show you the *short name* as well as the *title*, because
usually would want to change both, if changing either. Consider the
following example:

.. figure:: ../_static/renameitem.png
   :align: center
   :alt: rename-item.png

   rename-item.png

If you were to change the title to "Long-tailed Skippers," you would
also change the short name to "long-tailed-skippers." This keeps things
tidy -- it keeps them correct, so that the URL for the item, the web
address, is kept up-to-date with the actual content item. Note that the
short name should contain no blanks. Use dashes for any blanks in the
title, and otherwise make it a carbon copy of the title. Also, use
lowercase for the short name. See also the page "`What's in a Web
Name? <http://plone.org/documentation/manual/plone-4-user-manual/adding-content/whats-in-a-web-name>`_"
for a description of how Plone handles web addressing and the short
name. The following video also includes in illustration of renaming:

`|image11| <http://media.plone.org/LearnPlone/Copy,%20Paste,%20Cut,%20etc.swf>`_
Watch a Plone 2 video that includes `renaming an
item <http://media.plone.org/LearnPlone/Copy,%20Paste,%20Cut,%20etc.swf>`_.

The *delete* operation is straightforward. Click to select one or more
items, and then the delete button, and the items will be deleted.

The *change state* operation offers a great way to change the
publication state of a selection of folders, and their subfolders if you
select this option. In the following example, the publication state for
a folder called "Long-tailed Skippers" is being modified. Checking the
"Include Folder Items" will make the state change affect all contained
content. Don't forget that you can do this to, say, three folders at a
time, and all of their subfolders and contained content, so that in one
fell swoop you can quickly publish, unpublish, etc.

*Shift-clicking* to select a range of items works. This could be very
handy for a folder with more than a dozen items or so, and would be
indispensable for folders with hundreds of items.

.. figure:: ../_static/advancedstatepanel.png
   :align: center
   :alt: 

In addition to these individual action operations, reordering is a
natural mouse-driven manipulation, as described in the next section.

