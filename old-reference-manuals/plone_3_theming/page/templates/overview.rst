Templates and Components to Page
================================

An overview of how templates, viewlets, and portlets mesh together to
create a page.

Plone's page templates can be frustrating at first. There's no single
template which seems to contain everything you need.

Content Views
-------------

Since each content type is likely to have a different combination of
fields, each content type requires a separate template for display. As
we saw in the `templates and templating
language <http://plone.org/documentation/manual/theme-reference/page/buildingblocks/skin/templates>`_
section, these usually have \_view appended to their name. You can find
those for the standard Plone content types in

-  [your zope instance]/Products/CMFPlone/Skins/plone\_content.

main\_template
--------------

Knowing about content views only gets you so far, however. It is the
main template (main\_template.pt) which draws the content together with
the page furniture and design. You can find this in

-  [your zope instance]/Products/CMFPlone/skins/plone\_templates.

It is important to remember that the content view templates aren't
complete in themselves, they merely provide a snippet of content which
is dropped into a "slot" in the main\_template - called 'main'.

.. figure:: /old-reference-manuals/plone_3_theming/images/maintemplate.gif
   :align: center
   :alt: 

If you feel unsure about slots, then have a look back at the `templates
and templating language
section <http://plone.org/documentation/manual/theme-reference/page/buildingblocks/skin/templates>`_.

Around this main slot, the components - viewlets and portlets come into
play - supplying the page furniture and decoration around the content.
The main template simply pulls these in via viewlet managers and portlet
managers.

Viewlets are so flexible that they can even be pulled into the content
view. The abovecontentbody manager, for instance, is used in a number of
content views, and handles, amongst other things, the presentation
viewlet we looked at in previous sections.

In more detail
--------------

You might find it helpful to look at an example in context.

Have a look at:

-  Products/CMFPlone/Skins/plone\_templates/main\_template

and

-  Products/CMFPlone/Skins/plone\_content/document\_view

About document\_view (a content view template)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Although document\_view looks like a complete HTML page, ignore this.
Just note that right at the top it calls the main\_template.

::

    metal:use-macro="here/main_template/macros/master"

The code that gets used from document\_view is actually the bit between
these tags:

::

    <metal:main fill-slot="main"> …… </metal:main>

This gets dropped into a slot in the main\_template:

::

    <metal:bodytext metal:define-slot="main" 
                    tal:content="nothing">
    ... 
    </metal:bodytext>

2. Going back to the fill-slot in the document\_view you’ll see a few
tags calling the relevant fields from the content type – like this:

::

    <metal:field 
           use-macro="python:here.widget('title', mode='view')">
    </metal:field>

You’ll also see a few tags like calling viewlet managers which, in turn,
will summon up groups of viewlets:

::

    <div tal:replace="structure provider:plone.abovecontentbody" />

These enable you to drop extra bits of page furniture around the
specific content from the fields (e.g., the presentation mode link).

About the main template
~~~~~~~~~~~~~~~~~~~~~~~

1. Jump back to main\_template and you’ll see similar calls to other
viewlet managers managing groups of viewlets for more page furniture:

::

    <div tal:replace="structure provider:plone.portaltop" />

2. And calls to portlet managers to pull up the portlets defined for
that particular page:

::

    <tal:block replace="structure provider:plone.leftcolumn" />

3. You’ll also see a number of additional slots (define-slot), which
could also be filled (fill-slot) from the content view template if you
wanted. Here's one you could use to add a bit of css:

::

    <metal:styleslot define-slot="style_slot" />

Jump back to your content view template and simply add an additional
fill-slot (outside of the main fill-slot):

::

    <metal:mystyleslot fill-slot="style_slot">
     ..... 
    </metal:mystyleslot>

We'll go into other ways of providing styles in more detail in the next
section.
