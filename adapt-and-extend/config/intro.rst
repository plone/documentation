=========================
Introduction And Overview
=========================


This screen, which is available for the roles ``Site Admin`` and ``Manager``, is where you can configure most aspects of your website.

.. figure:: ../../_robot/site-overview.png
   :align: center
   :alt: Site setup configuration


When you have just created a new Plone site, you will see a warning here telling you to set up outgoing email for your site.

We'll come to that later.
The configuration area is divided into several parts, leading to further setup screens.

.. note::

   Many add-ons also come with their own setup area, you will also find these here after you have installed and activated them.

General
=======

Date and Time
    This sets up the :doc:`date and time related settings like timezone <date-and-time>`
Language
    :doc:`What languages are available <language>`. Also how the URL scheme works for multilingual sites.
Mail
    Configure :doc:`outgoing email <mail>`. This is needed to register users, email password reset requests and the like.
Navigation
    Configure :doc:`how navigation is constructed <navigation>`. Which content types should appear in navigation, should folders on the top level become tabs, and which workflows to show.
Site
    Various :doc:`site wide settings <site>`: Site name, logo, metadata, default settings for handling of icons and preview images, toolbar options, settings for search engines and more.
Add-ons
    :doc:`Activate and deactivate <add-ons>` add-ons that enhance Plone's functionality.
Search
    :doc:`Various search setting: <search>`: Activate live search, define which content types should be searched, etc.
Discussion
    :doc:`Comment settings <discussion>`. Here you set whether you would like to permit commenting, if comments should be moderated and enable spam-protection mechanisms for comments.
Theming
    All about :doc:`how your site looks <theming>`. Enable your own theme, and work with the embedded theme editor.
Social Media
    Set :doc:`metadata for social media <socialmedia>` such as Facebook app ID, twittercard ID.
Syndication
    Setting to :doc:`control RSS, Atom and itunes feeds <syndication>` so your articles can be picked up by blog aggregators.
TinyMCE
    Settings for :doc:`the text editor <tinymce>`. Enable spell and grammar checking, add extra CSS classes for editors to use, etc.

Content
=======

Content Rules
    Set up :doc:`automated mechanisms <content-rules>` to act on content when certain events occur. You can get an email when somebody adds a new item in a specific folder, and much more.
Editing
    Control :doc:`various editing settings <editing>`: which graphical editor to use, should automatic locking be performed when someone is editing, etc.
Image Handling
    Set up the :doc:`image sizes that Plone generates <image-handling>` and control image quality.
Markup
    Control if you want to :doc:`allow Markdown, Restructured Text <markup>` and other text formats.
Content Settings
    This is :doc:`where to control workflow, visibility and versioning of content<content-settings>`.
Dexterity Content types
    Here you can :doc:`create, adapt and extend <dexterity-content-types>` both the built-in content types, and your own ones. Define which fields are available, required, etc.


Users
=====

Users and Groups
    :doc:`Create, define, delete and otherwise control <users-groups>` the users that can log in. Define groups and assign users to them, and define which properties (like email, address, or job position in your organisation) you would like to store.

Security
========

HTML Filtering
    Set :doc:`which kind of tags <html-filtering>` you will allow users to enter. Malicious users, or users whose computer is infected by malware, can enter unwanted or dangerous content. Here you can finely choose what is acceptible and what now.
Security
    Various :doc:`security and privacy related settings <security>`: Can users self-register? Should anonymous site visitors see author info on an article?
Error log
    This will :doc:`list errors and exceptions <errors>` that may have occurred recently. You can inspect them and store them, if wanted. These can point to potential problems with missing content, but also clues on security related matters.

Advanced
========

.. note::

   The following can have large impact for your site. Take care when applying new settings.

Maintenance
    :doc:`Maintenance for the back-end database <maintenance>`. You can check the size of the database, and regularly *pack* it to keep it in optimal condition.
Management Interface
    This will take you to the :doc:`Management Interface <management-interface>`.
    In normal use, there is no need to go here. **Experts only**.
    But should you require access to the underlying software stack, here it is.
Caching
    Here you can :doc:`enable and fine-tune <caching>` Plone's caching settings. This can have a great beneficial effect on the speed of your site, but make sure to read the documentation first.
Configuration Registry
    Provides :doc:`direct acces to all system variables <configuration-registry>`. Handle with care.
Resource Registries
    Provides :doc:`direct access to JavaScript, CSS and LESS resources <resource-registries>`.
