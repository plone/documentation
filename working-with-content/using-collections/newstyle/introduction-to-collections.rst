Introduction to (new-style) Collections
========================================

A Collection in Plone works much like a report or query does in a database.
Use Collections to dynamically sort and display your content.

A **Collection** in Plone works much like a report or query does in a database.
The idea is that you use a Collection to search your website based on a set of **Criteria** such as: content type (page, news item, image), the date it was published, or keywords contained in the title, description, or body.

Let's say you have a large catalog of photos and maps on your website.
You can display them all at once by creating a link to the folder they're stored in.
You could even create different links for subfolders if you've organized things that way.
However, if your images and maps were spread out over the site in many folders this would quickly become cumbersome.
Also, there is no way with normal folders to display different content, from different parts of your site based on things like:

-  keywords in the title
-  date of creation
-  author
-  type of content

The need for showing content in a variety of dynamic ways has given rise to **Collections** (formerly known as **Smart Folders**, or **Rich Topic** in older versions of Plone).
Collections do not actually contain any content items themselves in the same way that a folder does.
Instead it is the **Criteria** that you establish which determines what content appears on each Collection page.

Common applications for Collections are:

-  News Archives
-  Event Archives
-  Photos Displayed by Date Range
-  Content Displayed by Keyword

