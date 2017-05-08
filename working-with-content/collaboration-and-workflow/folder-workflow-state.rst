=================================================
How a folder's workflow state affects its content
=================================================

.. admonition:: Description

   On this page we are referring to workflow states and their effects on content as they are configured in a default Plone installation.  Your specific site may have custom workflows, and the following discussion may or may not apply.

When it comes to the *Private* state, **Folders** are somewhat special.
Changing a folder to (or leaving it in) *private* state has the following effects:

- The folder *as well as all its contents* are taken out of the navigation and site map for anonymous users, and also for logged-in users who don't have permission to see private content.
  This means that all these users will not be able to find either the folder or any of its contents through any of the navigation menus.
  Of course, this includes external search engine robots.
- The folder itself can not be viewed by anonymous users, or by logged-in users who do not have permission to see private content.
  This is true even if an anonymous user, for example, had the direct URL to the folder, which would be the case if a link to the folder was part of the content body of a page in a different section of the same site or even a different site.
  Clicking such a link would result in being redirected to the login form.
- However, any **published** content of a **private** folder (or even of any of its sub-folders) **will** appear in the site search, even for anonymous users.
- Also, anonymous users who know the URL of a *published* content item inside a *private* folder will be able to view this content.
  Consequently, if a link to any such published content of a private folder is embedded in any part of the same site or external site, that content will be viewable by anyone.

Thus, putting a folder in the private state is not a guarantee of security for any of its contents.
Unless, of course, all the content has been made private, as well.
This can be done in bulk and in a single step, as described in :doc:`Advanced Control <advanced-control>`.

This is especially true of a folder's default item view (see :doc:`Setting an Individual Content Item as the View for a Folder </working-with-content/managing-content/folder-view>`).
If the contained item that is set as the folder's default view is published, then the folder will in a sense be public as well, even if it's own state has been set to private.
However, the folder will still be hidden from navigation for anonymous users.

When it comes to the folder default item view, care must be taken to have clarity on whether the desired workflow state is set on the folder, the default view item, or both.

A caveat: Images and Files
--------------------------

When discussing **published** content of a **private** folder above, we glossed over an important assumption: namely, that all content items actually have a **published** state.
This assumption is actually incorrect.
The *Image* content type and the *File* content type do not have the *State* menu (in a default Plone installation).
Thus, they can not be made public or private or any other state.
Instead, Images and Files *inherit* their state from the container in which they find themselves.
Therefore an image in a private folder will be private;  an image in a public folder will be public.

It is possible to bypass this inheritance of a folder's workflow state by contained images and files.

One of the workflows shipped with Plone by default is called "Single State Workflow".
To change the workflow for all Image content items, go to Content Settings on the Site Setup page.
Select *Image* (or *File*) in the top dropdown menu, and then "Single State Workflow" from the *New workflow* dropdown menu.
Once you click *Apply changes*, all Image content items will acquire the new workflow, and in particular, they will all be in published state, and will not inherit the containing folder's workflow state.

Some site administrators prefer all **Images** to be published, but do have special workflow states for **Files**, as some files may only be accessible for logged-in users with a certain role.
That is entirely possible using the above method, and setting an appropriate workflow on the type **File**
