Collaboration through Sharing
==================================

The Sharing tab empowers you collaborate with other users through the
use of several built-in roles.

Example 1: Letting others add content to a folder you created
-------------------------------------------------------------

In this example, Jane Smythe has full access to her Plone site. She can
add, edit, delete and publish content anywhere in the site. For now, she
has created a folder called "Documentation" and added one Page to it,
"Project Overview". She hasn't published either the folder or the
document. The default workflow for this Plone site has not been
modified.
Now she wants to let her colleague, George Shrubb, add content to the
Documentation folder. He have permission to edit any of the existing
content, but she needs him to start adding content. Before we follow
along with Jane, let's take a peek at what George currently sees when he
logs in on this Plone site:

.. figure:: ../_static/02b.png
   :align: center
   :alt: 

Notice that as of right now, George can't even view the Documentation
folder, because Jane created it and it is still in the *Private* state.
All the default permissions are currently in place and work as expected.

Jane gives George the permissions he needs to add content to the
Documentation folder.

Jane navigates to the Documentation folder and clicks on the Sharing
tab:

.. figure:: ../_static/03.png
   :align: center
   :alt: 

One of the first things to notice is that Jane already has all the
permissions available for this Folder. These permissions were actually
granted from higher up in the site as indicated by the green/check mark
symbol.

Taking a closer look at the available permissions, they are:

-  **Can add** - This means that when this permission is granted to a
   particular user (or group of users), that user can then add new
   content items. And since that user was also the creator of that
   content item, they will be able to edit it as they like.
-  **Can edit**- When this permission is granted on a folder, the user
   can not only edit the Folder (its title and description) but can also
   edit any of the items in the folder. Note, however, the user is not
   allowed to delete any of the content. When this permission is granted
   on a Page, for example, the user can only edit that Page and none of
   the other items in the folder.
-  **Can view** - When this permission is used on a folder or other
   item, the user can view the content but not make any changes.
-  **Can review** - When this permission is granted, the user can
   publish items.

Note: these permissions will override the default workflow permissions!
For example, if you grant a user "Can view" permission on a Page that is
in the Private state, that user will be able to see that Page.

In this example, Jane will grant George "Can add" permission on the
"Documentation" folder so that he can add content to the folder. First,
she searches to find him by his name:

.. figure:: ../_static/04.png
   :align: center
   :alt: 

Jane can now add specific permissions for George in the "Documentation"
folder. She is going to give him the "Can add" permission and then click
on "Save":

.. figure:: ../_static/05.png
   :align: center
   :alt: 

And that's all there is to it! Let's see how George views the site now.

Note: George does NOT need to log out and log back in. Permissions are
always current because they are checked every time a user accesses
anything (e.g. clicks on a link) on a Plone site.

George clicks on the *Home* tab (for example) to refresh his view of the
site and can now see the "Documentation" folder:

.. figure:: ../_static/06.png
   :align: center
   :alt: 

When George clicks on the "Documentation" tab, he notices that he can
view all the content in the "Documentation" folder, and he now is able
to add the available content types to the folder, as shown in the *Add
new...* menu:

.. figure:: ../_static/07.png
   :align: center
   :alt: 

George wants to review what Jane has already created, so he clicks on
the Project Overview link and sees:

|image25|

While George can view the document, his limited permissions do not allow
him to edit it or change its state. The only thing he can do beyond
viewing the document is to make his own copy of it.

George adds a Page called "Widget Installation" and creates the content
for that Page. When he's done he saves it:

.. figure:: ../_static/08.png
   :align: center
   :alt: 

Jane views the work George has done. She clicks on the "Documentation"
tab and sees that George indeed has been busy. She clicks on "Widget
Installation" page to take a closer look:

.. figure:: ../_static/09.png
   :align: center
   :alt: 

Notice that Jane has full access to the page that George created. She
can edit it as well as cut/copy/paste it. Instead, she will wait until
George submits the page for review before actually doing anything
further with this page.

Example 2: Letting others edit content you created
--------------------------------------------------

Both Jane and George have been hard at work creating pages in the
Documentation folder. **Jane has published the Documentation folder and
several pages:**

.. figure:: ../_static/09b.png
   :align: center
   :alt: 

Jane has decided that she wants to turn over all editing (but not
publishing) control of the "Documentation" folder to George. So she
returns to the "Documentation" folder and clicks on the *Sharing* tab:

.. figure:: ../_static/10.png
   :align: center
   :alt: sharing10.png

   sharing10.png

From here she only needs to tick the "Can edit" check box and George
will be able to edit all the content in the "Documentation" folder --
including the "Documentation" folder itself. When George next visits the
folder and clicks on "Project Overview" (which is a Page that Jane
created), this is what he sees:

.. figure:: ../_static/11.png
   :align: center
   :alt: sharing11.png

   sharing11.png

So now George can edit any item in the "Documentation" folder regardless
of who created it or when.

Meanwhile, Molly has joined George as a new team member. George helps
Molly start updating the "Widget Installation" document. He goes to the
sharing tab for "Widget Installation" and searches on Molly's Full Name
(not username) and gives her the "Can edit" permissions on this
document.

.. figure:: ../_static/12.png
   :align: center
   :alt: sharing12.png

   sharing12.png

Now when Molly goes to the "Documentation" folder, she can see the two
published items and the private item that she is now allowed to edit:

.. figure:: ../_static/13.png
   :align: center
   :alt: sharing13.png

   sharing13.png

And, in fact, when she clicks on the "Widget Installation" document, she
is able to edit it:

.. figure:: ../_static/13b.png
   :align: center
   :alt: sharing13b.png

   sharing13b.png

Notice, however, when she clicks on either of the two items she isn't
allowed to edit, she doesn't have any additional access. She can view
these two items because they are published and in the default Plone
workflow (meaning that anyone can view them).

.. figure:: ../_static/13c.png
   :align: center
   :alt: sharing13c.png

   sharing13c.png

One final note on this example: if the "Documentation" folder was not in
the published state OR Molly had not been given any other permissions
(for example, "Can view" on the Documentation folder), then Molly would
have needed the complete URL to reach the document she had been given
access to edit. Permissions are very specific in Plone!

.. |image25| image:: ../_static/07b.png
