Editing Content
====================

Editing Plone content works the same as adding content -- usually the
data entry and configuration panels for the content are the same for
editing as for adding.

Of course, when we edit an item of content, the item already exists.
Click the Edit tab for an item and you will see the data entry panel for
the item, along with the existing values of the item's data.

For an example of something really simple, where editing looks the same
as adding, we can review how to edit a folder.

The *Edit* panel for a folder simply shows the title and description
input areas. Often a description is not provided for a folder, so the
only thing changed is the title.Â If you do wish to give a description,
which is a good idea for distinguishing folders in a list, the
description can be text only -- there is no opportunity for setting
styling of text, such as bold, italics, or other formatting.Â This keeps
the descriptions of Plone content items as simple as possible.

Here is the *Edit* panel for a folder, in this case, one called
"Butterflies":

.. figure:: ../_static/edititemfolder.png
   :align: center
   :alt: 

That's it. Change what you want and save, and the content item will be
updated in Plone's storage system. You can repeatedly edit content
items, just as you can repeatedly edit files on your local computer.Â By
now you have appreciated that Plone stores discrete content items as
separate entities, akin to "files" on a local computer, but you really
don't have to think about it that way. Plone is a content management
system, where the content comes in the form of numerous discrete content
items that may be individually edited. Edit away at your heart's
content.

For an example of editing a content item that is a bit different than
adding in the first place, we can examine editing an image. Editing an
Image can be done by navigating to an individual image and clicking the
*Edit* tab. Clicking the *Edit* tab for the image, you will see the
following *Edit Image* panel:

.. figure:: ../_static/editimage.png
   :align: center
   :alt: 

Here, an image called "Eastern Tiger Swallowtail Butterfly" is being
edited.Â You can change the title and description, as usual, in which
case you would usually keep the setting to "Keep existing image."Â You
can also change the image itself by checking the "Replace with new
image" choice. Or, clicking the "Delete current image" choice will
simply delete the image entirely.

Notice also the *Transform* tab at the top, which pertains specifically
to images, offering a choice of several image transforms:

.. figure:: ../_static/transformimage.png
   :align: center
   :alt: 

So, editing an image is a bit different than adding one in the first
place, but not by much.

Editing panels for other content items are also usually just like the
panels for adding.

Inline Editing (*optional*)
---------------------------

    Inline editing is disabled by default in the latest versions of
    Plone (3.3+). It can be enabled through the control panel by a Site
    Manager (Site Setup -> Editing -> Enable Inline Editing checkbox).

The normal procedure to edit a content item is to click the *Edit* tab
and use the discrete input fields for the item.Â For text fields, such
as Title, Description, Body Text, etc., there is a quicker way to edit
called inline editing. Inline editing is used when viewing the content
item (the *View* tab is active).

As the mouse passes over editable text parts of the item, a subtle box
will outline the editable text. In the following screen capture, the
mouse cursor is *not* over editable text, so you see the page title and
body text as normal:

.. figure:: ../_static/inlineeditingoff.png
   :align: center
   :alt: 

But when the mouse is moved over the body text, a box highlights the
body text as editable:

.. figure:: ../_static/inlineeditingbodytext1.png
   :align: center
   :alt: 

Clicking within the body text after the inline editing box has appeared
will bring up the visual editor:

.. figure:: ../_static/inlineeditingbodytext2.png
   :align: center
   :alt: 

Change or add text and save, and the normal view is back. This is
considerably quicker -- fewer clicks and less intervening wait time --
than clicking the *Edit* tab and bringing up the entire edit panel for
the page.

If the mouse is moved over the title, also editable, an inline editing
box appears:

.. figure:: ../_static/inlineeditingtitle1.png
   :align: center
   :alt: 

Clicking the title after the box appears will activate a very simple
editing field with a Save/Cancel choice:

.. figure:: ../_static/inlineeditingtitle2.png
   :align: center
   :alt: 

Change the title and save. The speed benefit of inline editing is really
sensed for editing something as simple as a title.

