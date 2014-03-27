Templates and the Templating Language
=====================================

The main elements of a skin are page templates, images, Python scripts,
CSS files, and JavaScript files.

(Zope) Page Templates
---------------------

Page templates (.pt files or ZPT) are an essential part of a Plone theme
and are probably the easiest aspect of Plone to get to grips with. They
are written in an elegant XML-based templating language called TAL,
sometimes make use of macros (METAL), and sometimes incorporate Python
expressions (small one-line calculations) or Python scripts.

There are several excellent introductions to ZPT, and it doesn't take
long to learn TAL. Try these:

-  `Zope Page Templates tutorial on
   plone.org <http://plone.org/documentation/tutorial/zpt/>`_
-  `ZPT Reference on
   Zope.org <http://www.zope.org/Documentation/Books/ZopeBook/2_6Edition/AppendixC.stx>`_

TAL is the one language that we really recommend you learn properly. The
rest you can pick your way through or familiarise yourself with as you
go along.

-  `Zope Page Template Tutorial on plone.org - Advanced
   Usage <http://plone.org/documentation/tutorial/zpt/advanced-usage>`_

A Plone web page is delivered via an aggregation of templates, rather
than just one, and there a couple of aspects of Zope Page Template that
you'll need to be aware of.

1. Slot
~~~~~~~

A slot is a predefined section of a template. This can be left empty, or
given some default content, but it is available to be filled on the fly.
A slot is defined in a template in code like this:

::

    <metal:bodytext metal:define-slot="main" tal:content="nothing">
        .....
    </metal:bodytext>

And filled via another template like this:

::

    <metal:main fill-slot="main">
     <h1 class="documentFirstHeading">
        ......
     </h1>
    </metal:main>

The ZPT tutorial on plone.org talks you through this in more detail, and
the `Templates and Components to
Page <http://plone.org/documentation/manual/theme-reference/buildingblocks/page/templates>`_
section of this manual gives you an example.

2. Content view templates (\_view)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    Note: the term "view" also has a more technical application, so in
    the context of Components (discussed later in this manual) it will
    mean something different.

From the user's, contributor's, or visitor's perspective, a view is the
way in which a content item is presented on the page. There's a `useful
introduction <http://plone.org/documentation/plone-2.5-user-manual/managing-content/folder-view/>`_
to this in the Plone User Manual.

Templates that are used to render a content item for a view have \_view
appended to their name (e.g., document\_view.pt) and may have a title
such as "Standard View." These templates are, in fact, sets of
information ready to drop into slots.

Scripts
-------

These are small stand-alone functions for times when you need a few
lines of code to perform your calculation. On the file system, they have
a .py extension; you'll find them in the Zope Management Interface as
Script (Python).

Here's a snippet from the event\_view template (the content view for the
event content type) which uses a Python script to format the a time
field according to the default format for the site. If you look in
CMFPlone/skins/plone\_scripts, you'll find toLocalizedTime.py - just a
few lines of code.

::

    <span metal:define-slot="inside" 
                class="explain"
                tal:attributes="title python:here.end()"
                tal:content="python:here.toLocalizedTime(here.end(),
                             long_format=1)">End Date Time</span>

 
