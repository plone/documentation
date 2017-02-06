====================
Conceptual Overview
====================

An explanation of Plone as a content management system

What is Plone?
==============

Plone is a content management system (CMS) which you can use to build a
web site. With Plone, ordinary people can contribute content to a web
site without the help of a computer geek. Plone runs over the Web, too.

You don't need to install any special software on your computer.
The word *content* is meant to be general, because you can publish so
many types of information, including:

.. figure:: /_static/content_types_into_plone.png
   :align: center
   :alt:

A Plone web site contains various kinds of content, including text,
photos, and images. These can exist in many forms: documents, news
items, events, videos, audio files, any types of file and data that can
be uploaded or created on a web site. Content can also be uploaded from
your local computer. You create *folders* on a Plone web site to hold
content, and those automatically also create the navigation structure:

.. figure:: /_static/content_is_added_to_folders.png
   :align: center
   :alt:

You Love Butterflies
====================

For example, to add content about butterflies, you might add a folder
named "Butterflies," then add some text to a web page in the folder:

.. figure:: /_static/butterflies_folder_text.png
   :align: center
   :alt:

And then you might add some butterfly photos to the folder:

.. figure:: /_static/butterflies_folder.png
   :align: center
   :alt:

You can add many types of content to a folder, including sub-folders.
After adding a few reports and videos to the Butterflies folder, the
content would be organized like this, with two sub-folders within the
Butterflies folder:

.. figure:: /_static/folders_within_folders.png
   :align: center
   :alt:

What Goes on Behind the Scenes
==============================

You may wonder how it all works. A typical Plone web site exists as an
installation of Plone software on a web server. The web server may be
anywhere, often at a website server company within a "rack" of computers
dedicated to the task:

.. figure:: /_static/server_rack.png
   :align: center
   :alt:

The diagram shows the many cables that connect individual server
computers to the Internet, across fast network connections. Your Plone
site is software and database storage software installed on one of
the individual server computers. As you type or click on your computer,
data is sent up and down the networking cables and communication
channels of the Internet to interact with your Plone software
installation on the server.

Let's simplify the diagram showing how you interact with Plone:

.. figure:: /_static/client_to_server_simple.png
   :align: center
   :alt:

You use your web browser -- Firefox, Safari, Internet Explorer, etc. --
to view and edit your Plone web site, and the changes are stored by the
Plone software into its database storage system.

For example, imagine your butterfly Plone web site is located at
mysite.com. You type www.mysite.com into your web browser. After you
press Enter, the following sequence of events happens as your browser
talks to the web server at mysite.com:

.. figure:: /_static/client_request.png
   :align: center
   :alt:

The Plone software responds:

.. figure:: /_static/server_response.png
   :align: center
   :alt:

Plone reads its database to look for information stored in mysite.com.
It then sends back the web page to your computer, in a code called HTML.
HTML is a computer language that describes how a web page looks. It
includes text, graphics, fonts, the color of the background, and just
about everything else. There are many online resources that can teach
you HTML details, but one of Plone's advantages is that you don't
need to know about HTML. That's one reason for Plone and other
similar web software; to let you focus on your content, e.g., butterfly
text and graphics, instead of learning a new computer language.

But back to our overview. Your web browser "renders" (translates) this
HTML, and you see the resulting web page:

.. figure:: /_static/my_site_served.png
   :align: center
   :alt:

As you view your butterfly web page, you can choose to change it or add
to it. You can also upload photos, documents, etc. at any time:

.. figure:: /_static/plone_donut.png
   :align: center
   :alt:

After you make your edits and click "save changes," the new version of
the web page will be immediately available to anyone surfing to your
site:

.. figure:: /_static/plone_donut_full.png
   :align: center
   :alt:
