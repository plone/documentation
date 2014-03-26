Restricting Types in a Folder
===================================

The Add new... menu has a choice for restricting the content types that
can be added to the folder.

Restricting types available for adding to a folder is the simplest way
to control content creation on a Plone web site. You may want to
restrict content types if your site is going to be worked on by several
people. In this way you can enforce good practices such as putting just
images in the images folder.

First, select the last choice in the *Add new...* menu called
*Restrictions...*:

.. figure:: ../_static/addnewmenu.png
   :align: center
   :alt: add-new-menu.png

   add-new-menu.png

There are three choices shown for restricting types in the folder:

.. figure:: ../_static/restricttypes.png
   :align: center
   :alt: 

The default choice, to use the setting of the parent folder. Having this
as the default means that if you create a folder and restrict the types
that can be added, any subfolders created in the folder will
automatically carry the restrictions. The second choice, to allow the
standard types to be added, is a way to reset to the default,
unrestricted setting. The last choice allows selection from a list of
available types:

.. figure:: ../_static/restricttypesmanually.png
   :align: center
   :alt: 

Types listed under the *Allowed types* heading are those available on
the web site. The default, as shown, is to allow all types. Allowed
types may be toggled on and off for the folder.

Use of *Secondary types* allows a kind of more detailed control. For
example, if it is preferred to store images in one folder, instead of
scattering them in different folders on the web site -- a scheme that
some people prefer -- an "Images" folder could be created with the
allowed type set to the Image content type *only*. Likewise an "Company
Events" folder could be created to hold only the Event content type. If
left this way, content creators would be forced (or a single web site
owner) to follow this strict scheme. Perhaps some flexibility is desired
for images, though. By checking the Image content type under the
*Secondary types* heading for the "Company Events" folder, images could
be added if really needed, by using the *More...* submenu, which would
appear when this mechanism is in place.

Some people prefer a heterogeneous mix of content across the web site,
with no restrictions. Others prefer a more regimented approach,
restricting types in one organizational scheme or another. Plone has the
flexibility to accommodate a range of designs.

