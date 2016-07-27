==========================================
Create a theme based on a website template
==========================================

Introduction
------------

We have a static theme based on HTML/CSS and want to use it for Plone. The theme separates the frontend for anonymous users from the backend with default Plone UI for editors.


Requirements
++++++++++++

We assume that you have a Plone site up and running. You are logged in as a Manager and can access the Control Panel.


Getting started
---------------

TODO


Create a theme package
++++++++++++++++++++++

If you already have a package you can skip this step. If you start from scratch you need to create a theme package for Plone. This manual shows how you can create a package.

Link to bobtemplates...


Download an existing theme
++++++++++++++++++++++++++

In our example we start by downloading an existing bootstrap-based theme from Start Bootstrap.

http://startbootstrap.com/template-overviews/business-casual/


Move static files into package
++++++++++++++++++++++++++++++

Copy the entire static theme you get from your designer into the static folder inside your theme package.

Code here...


Show Plone default UI for logged in Users
+++++++++++++++++++++++++++++++++++++++++

Code here...


Create Diazo rules for several templates
+++++++++++++++++++++++++++++++++++++++++

We have existing templates for several templates in our static folder. Now we want to write proper Diazo rules to make use of them.

* Frontpage
* News Item View (Includes views for Document, File, Link, Image)
* Event View
* Folder Summary View
* Folder Full Vieew (Blog, Newslisting, etc.)
* Overlays
* Contact Form
* Login Form
* Search Results
* Sitemap


Create a static theme based on Bootstrap
----------------------------------------

Tips for creating website templates based on bootstrap for easy reuse.


Further reading
---------------

Ways to optimise maintaining that static theme (jekyll or other templating)

