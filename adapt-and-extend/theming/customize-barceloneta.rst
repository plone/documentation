=======================================
Customize the Barceloneta default theme
=======================================

TODO


Heading
-------

TODO


Subheading
++++++++++

TODO


Subheading
++++++++++

TODO


Heading
-------

TODO


Introduction
------------

Target group
++++++++++++

A Systems integrator with average knowledge about Plone. Aims to theme a Plone site. 


Aim
+++

In this tutorial you will learn how to build a custom theme for your website by changing several elements of Plone. You will learn where to find and how to customise different building blocks in Plone while keeping the basic concepts and structure intact. 

Demarcation
+++++++++++

This is not about creating a standalone theme which behaves independently from Plone UI concepts. If you plan to do this, you should read the next scenario.

Requirements
++++++++++++

We assume that you want to keep your customisations in filesystem code. You are  familiar with how to create and register an egg to accommodate the customisations. You can e.g. create such an egg by using mr.bob and following the mr.bob documentation on pypi <https://github.com/plone/bobtemplates.plone>`_ and picking the theme option.



Getting started with the Basics
-------------------------------

New logo
++++++++

Probably the very first thing you want to change in a new site is the logo and the favicon. Let’s start with the logo.


First we override the existing logo using `z3c.jbot <https://pypi.python.org/pypi/z3c.jbot>`_. Hierfür gibt es in unserem neu erstellten Paket bereits den Ordner ``overrides`` in ``your.egg/src/your/egg/browser/``.

::

    $ cd your.egg/src/your/egg/browser/overrides/
    $ cp fromplonepositionoflogo .
    $ mv logo.png Products.CMFPlone.skins.plone_images.logo.png

We assume you 
Anschließend kann die Instanz neu gestartet werden, eine Plone-Site erstellt und ``vs.base`` aktiviert werden.


Change the favicon
++++++++++++++++++

The favicon is stored in a different place. To exchange it, you need to do…

#get your favicon.ico from anywhere and follow the steps explained in the step above.

   $ mv your_favicon.ico Products.CMFPlone.skins.plone_images.favicon.ico


Play with the variables!
++++++++++++++++++++++++

Now the last thing to make the site really look differently is to change a few styles to match your desired CI. Plone already supports a few parameters to customise typical elements. These variables are located … and can be customised like this…

You can set the LESS variables values in the "plone.lessvariables" record in your profile's registry.xml.
Note: you will have to re-build your resources.


Your own custom css file
++++++++++++++++++++++++

While the above variables allow you quite some control, it is quite likely that there are style elements that cannot be controlled by them. In this case, it may be a good solution to just add a bunch of your own styles in addition to the default styles provided by Plone. With these styles you can add more styling or override existing styling rules in css. 

Note: While Plone supports “less” syntax in style files, you can of course also write plain css only.

These steps show you how to register your own styles file so that it gets included into the Plone theme.

code here

Note: If you are changing styles in your style file, remember to recompile (describe the actual steps necessary from changing a style in the file to actually seeing the difference in your browser).


Change CSS that’s already there
+++++++++++++++++++++++++++++++

The previous steps should already have gotten your site into a quite decent state. You can do already a lot with custom css, but as soon as your custom css file get’s quite long, things become crowded and you might get a desire for more structure. Instead of now adding even more of your own custom css files and slowly duplicating most of the css, you can actually also exchange existing Plone css.

Plone keeps its css in a very well structured, componentized way. If you want to change the styling for a certain area or component, chances are good that you will find them already grouped in a dedicated less file. 

Take a look what’s available here… (where are the barceloneta less files?)

If you can identify the styles group you want to exchange, perform the following steps to unregister the original one and register your own.


Customise Special Elements
--------------------------

Change the toolbar logo
+++++++++++++++++++++++

By now you have probably noticed that there are a few more elements that you might want to alter. One is the little Plone logo in the toolbar. If you want to change that, you can do that by …

code here

 
The Omnipresent Icons
+++++++++++++++++++++

Plone doesn’t use images as icons for content types or actions anymore. Instead it uses a fontello font which is configured to contain all the icons needed as characters. If you want to change these, yo can of course provide your own and override via css, but you can also upload the font definition file to fontello, reconfigure it there and readd the modified font file to your customisation.

Here is how you upload and modify the fontello font file:

code here

Here is how you override the font in your own code:

code here

Change the markup (jbot)
++++++++++++++++++++++++

So far we have only touched the styles and resources. And while you can do a lot with css, there are moments where you might need an insane amount of effort or simply unmaintainable hacks to achieve what you want. In the contrary, just changing e.g. the order  of the markup might just do what you need.

Luckily, changing components of the Plone theme is easy and straightforward. Once you have registered jbot for your package (link to jbot installation), you can copy the original template file and place it into your package - just following a simple naming convention:

describe an example how to override a viewlet using jbot

Note: Overriding with jbot is not limited to html files. You can basically override every template and resource - even logo files.

Overriding the way, z3c forms are rendered
++++++++++++++++++++++++++++++++++++++++++

Plone Forms are generated using z3cforms. As forms are generated, you will not find the forms itself for overriding in jbot. Instead you can override the template that z3cforms uses to generate the widgets itself.

Describe Customizing plone.app.z3cform.templates.widget.pt

Registering your own templates
++++++++++++++++++++++++++++++

If you have tried styling a generated form and the natural limitations imposed by generic generated mechanisms are still too limiting for you, you might want to register your own form template. This allows you full control over the used markup.

code here 

Next steps
----------

By now you have customised every single element of the visual appearance of plone. Of course you can do much more, and typically this will involve adding new functionality. Customising plone is covered in other sections and a good read to go forward may now be one of those:

* Add browser views
* Add Portlets and Viewlets
* Create content types
* etc. (Put here typical good links to documentation how to extend plone)
