Introduction
============

.. admonition:: Description

        Writing, including and customizing Javascript for Plone add-ons

.. note::

   This part of the documentation is **under construction**.
   Important parts for adding javascript to addons can be found in the documentation about the :doc:`Plone 5 Resource Registry </adapt-and-extend/theming/resourceregistry>`.
   You should also look at the javascript part of the official `plone training <http://training.plone.org/5/javascript/index.html>`_.
   While we are updating this documentation, you should also look at the following blogposts:

   - `Updating JavaScript for Plone 5 <https://www.nathanvangheem.com/news/updating-javascript-for-plone-5>`_
   - `Customizing JavaScript pattern options in Plone 5 <https://www.nathanvangheem.com/news/customizing-javascript-pattern-options-in-plone-5>`_


For JavaScript and CSS development, Plone 5 makes extensive use of tools like Bower, Grunt, RequireJS and Less for an optimized development process.
The JavaScript and CSS resources are managed in the :doc:`Plone 5 Resource Registry </adapt-and-extend/theming/resourceregistry>`.
The Resource Registry was completly rewritten in Plone 5 to support the new dependency based RequireJS approach.
It also allows us to build Less and RequireJS bundles Through-The-Web for a low entry barrier.

Javascript basic tips
---------------------

Always use DOM ready event before executing your DOM manipulation.

Don't include Javascript inline in HTML code unless you are passing variables from Python to Javascript.

Use JSLint with your code editor and ECMAStrict 5 strict mode to catch common Javascript mistakes (like missing var).

For more Javascript tips see `brief introduction to good Javascript practices and JSLint <http://opensourcehacker.com/2011/11/05/javascript-how-to-avoid-the-bad-parts/>`_
