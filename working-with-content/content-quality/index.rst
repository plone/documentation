=========================================
Create and maintain good quality content
=========================================

.. admonition:: Description

   Plone comes with several tools to maintain the quality of the content you create.
   This ensures both good results in search engines, as better usability for the visitors.


What is "content quality"?
--------------------------

Under this heading we list several tools that help you to ensure content can be properly indexed, is enriched with meta-data such as tags, dates and even geo-location, and to make sure links are not broken.

This will also help you with accessibility certification for your content, and Search Engine Optimization (SEO)


Batteries included
-------------------

Plone comes standard with a whole host of features that help you:

- The URL's for content are derived from the Title, making sure you have human-readable URL's
- `Dublin Core <http://dublincore.org/>`_ metadata is used throughout
- The navigation is automatic, and within folders you can also enable "previous/next" style links
- Automatic filters in the editor ensure that the page will be saved as valid HTML
- Behind the scenes, Plone registers internal links with so-called "UUIDs". In short, a unique key is generated for every content item, making sure all internal links will work if you move pieces of content or even whole folders around.
- When you delete a piece of content, you will receive a warning if there are other places in your site that still link to this content. You'll get the option to correct those other pages.
- If you move content around and people come to your site using the old URL, they will be automatically redirected to the new location. *(Tip: you can even use this to create short 'alias' URL's...)*
- Images are automatically scaled. Even if your editors upload high-resolution images, you will get smaller sizes that ensure quick loading of your page. Of course the original image size is also available, if you want.

And there are some hidden gems as well: you can enable (in the Control Panel, as site administrator) the `After The Deadline <http://www.afterthedeadline.com/>`_ intelligent spelling and grammar checker. Now while this is only available at the moment for English, French, Spanish and Portuguese, if your site uses one of those languages this is a very valuable add-on.
For testing and light use, you can use the connection to the online service; if you have many users or create much content, you are advised to set up your own instance of the After The Deadline server. It is free and open source software.

In the next section, we will point to several add-ons that can help even more to create and maintain high-quality content.

.. toctree::
    :maxdepth: 2

    content-quality-helpers
