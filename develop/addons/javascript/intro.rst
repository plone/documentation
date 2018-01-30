============
Introduction
============

.. admonition:: Description

        Writing, including and customizing JavaScript for Plone add-ons

.. note::

   This part of the documentation is **under construction**.
   Important parts for adding JavaScript to addons can be found in the documentation here:

- the :doc:`Plone 5 Resource Registry </adapt-and-extend/theming/resourceregistry>`.
- `plone training <http://training.plone.org/5/javascript/index.html>`_.

   While we are updating this documentation, you should also look at the following blogposts:

- `Updating JavaScript for Plone 5 <https://www.wildcardcorp.com/blog/updating-javascript-for-plone-5>`_
- `Customizing JavaScript pattern options in Plone 5 <https://www.wildcardcorp.com/blog/customizing-javascript-pattern-settings-in-plone-5>`_


For JavaScript and CSS development, Plone 5 makes extensive use of tools like Bower, Grunt, RequireJS and Less for an optimized development process.
The JavaScript and CSS resources are managed in the :doc:`Plone 5 Resource Registry </adapt-and-extend/theming/resourceregistry>`.
The Resource Registry was completly rewritten in Plone 5 to support the new dependency based RequireJS approach.
It also allows us to build Less and RequireJS bundles Through-The-Web for a low entry barrier.

JavaScript basic tips
---------------------

Always use DOM ready event before executing your DOM manipulation.

Don't include JavaScript inline in HTML code unless you are passing variables from Python to JavaScript.

Use JSLint with your code editor and ECMAStrict 5 strict mode to catch common JavaScript mistakes (like missing var).

For more JavaScript tips see `brief introduction to good JavaScript practices and JSLint <http://opensourcehacker.com/2011/11/05/javascript-how-to-avoid-the-bad-parts/>`_


Add a pattern or other javascript to your own bundle
----------------------------------------------------

1. Write your JavaScript file or pattern

There are two options:

- Use ``define`` to define a pattern that can be imported by other modules
- Use ``require`` to add your own javascript that does not need to be imported by other modules (see here for more details: https://github.com/plone/Products.CMFPlone/issues/1163#issuecomment-148086841)

A good example for a new pattern can be found here: https://github.com/collective/pat-fancytree (Work in progress)

It uses the new Base Pattern that was added to patternslib recently. The way how this example registers the Pattern assumes that require.js is available and used.
To make a pattern work without ``require.js`` please use the way like it is proposed by the patterslib documentation: http://patternslib.com/creating-a-pattern/#main-content

There is also a Yeoman patternslib generator that can be found here:
https://www.npmjs.com/package/generator-patternslib
It produces a boilerplate for creating a new pattern


2. Add your pattern or JavaScript file as a resource (in registry.xml)

..  code-block:: xml

    <records prefix="plone.resources/MY-PATTERN"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
       <value key="js">++resource+MY-PATTERN-PATH/MY-PATTERN.js</value>
    </records>

Make sure that your pattern is available over the provided resource directory path

3. Create bundle resource (only if “define” is used under 1)

See ``Products.CMFPlone/Products/CMFPlone/static/plone.js`` for an example

4. Add bundle resource (only if “define” is used under 1) (in registry.xml)

..  code-block:: xml

    <records prefix="plone.resources/MY-BUNDLE-RESOURCE"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
       <value key="js">++resource++MY-BUNDLE-RESOURCE-PATH/MY-BUNDLE-RESOURCE.js</value>
       <value key="css">
         <element>++resource++MY-BUNDLE-RESOURCE-PATH/MY-BUNDLE-RESOURCE.less</element>
       </value>
    </records>

5. Define bundle

..  code-block:: xml

    <records prefix="plone.bundles/MY-BUNDLE"
             interface='Products.CMFPlone.interfaces.IBundleRegistry'>
     <value key="resources">
       <element>MY-BUNDLE-RESOURCE</element>
     </value>
     <value key="enabled">True</value>
     <value key="jscompilation">++resource++MY-BUNDLE-PATH/MY-BUNDLE-compiled.min.js</value>
     <value key="csscompilation">++resource++MY-BUNDLE-PATH/MY-BUNDLE-compiled.min.css</value>
     <value key="depends">BUNDLE-DEPENDENCY</value>
    </records>

6. Compile bundle

First you need to install your addon in a fresh plone site. Then execute

.. code-block:: bash

   bin/plone-compile-resources --site-id=Plone --bundle=MY-BUNDLE

Open questions for addons developers:

- Do I need to create a bundle for every add on? I there a possibility to add a resource to an existing bundle? If yes, how is this done?

What is missing here?

- How do I setup a dev environment for the JavaScript topic?


How to add a patternslib pattern to plone bundle in Products.CMFPlone
---------------------------------------------------------------------

1. Add resource

..  code-block:: xml

    <records prefix="plone.resources/patternslib-patterns-autofocus"
             interface='Products.CMFPlone.interfaces.IResourceRegistry'>
        <value key="js">++plone++static/components/patternslib/src/pat/autofocus/autofocus.js</value>
    </records>

2. Add pattern to ``static/plone.js``
