==================
TAL Page Templates
==================

.. admonition:: Description

    Plone uses Zope Page Templates (:term:`ZPT`). This document contains references to this template language and generally available templates,
    macros and views you can use to build your Plone add-on product.


Introduction
=============

Plone uses `Zope Page Templates <http://docs.zope.org/zope2/zope2book/AppendixC.html>`_, consisting of the three related standards:
* Template Attribute Language (:term:`TAL`)
* TAL Expression Syntax (:term:`TALES`)
* Macro Expansion TAL (:term:`METAL`).

A normal full Plone HTML page consists of:

* the *master template*, defining the overall layout of the page
* *slots*, defined by the master template, and filled by the object being published,
* :doc:`viewlets and Viewlet managers </develop/plone/views/viewlets>`.

Templates can be associated with Python view classes (also known as "new style", circa 2008) or they can be standalone ("old style", circa 2001).

.. note::

    The rationale for moving away from standalone page templates is that
    the page template code becomes cluttered with inline Python
    code. This makes templates hard to customize or override.  New style
    templates provide better separation with view logic (Python code)
    and HTML generation (page template).


The MIME-Type
=============
Basically a document file got a mime-type.
This is also important for Plone Templates if you don't want to export to text/html.

If you want to export to a XML File you have to change the mime-type because otherwise the browser won't recognize the file as an XML.
At the moment Plone supports text/html which is the default value. And text/xml.
You got 2 opportunities to change this value.
If you customize a template you got an input box which called "Content-Type".

The other Way is to create a file named by your template name and extend the name by `.metadata`.

 Example:
   * my_view.pt
   * my_view.pt.metadata

Content of metadata file::

         [default]
         content_type = text/xml


Overriding templates
====================

The recommended approach to customize ``.pt`` files for Plone 4 is to use a
little helper called `z3c.jbot`_.

If you need to override templates in core Plone or in an existing add-on,
you can do the following:

* `Roll out your own add-on`_
  which you can use to contain your page templates on the file system.

* Use the `z3c.jbot`_ Plone helper add-on to override existing page
  templates.
  This is provided in the `sane_plone_addon_template`_ add-in, no separate
  set-up needed.

* `z3c.jbot`_ can override page templates (``.pt`` files) for views,
  viewlets, old style page templates and portlets.
  In fact it can override any ``.pt`` file in the Plone source tree.

Overriding a template using z3c.jbot
------------------------------------

1. First of all, make sure that your customization add-on supports
   `z3c.jbot`_.
   `sane_plone_addon_template`_ has a ``templates`` folder where you can
   drop in your new ``.pt`` files.

2. Locate the template you need to override in Plone source tree.
   You can do this by searching the ``eggs/`` folder of your Plone
   installation for ``.pt`` files. Usually this folder is
   ``.../buildout-cache/eggs``.

   Below is an example UNIX ``find`` command to find ``.pt`` files.
   You can also use Windows Explorer file search or similar tools:

   .. code-block:: console

       $ find ~/code/buildout-cache/eggs -name "\*.pt"
       ./archetypes.kss-1.4.3-py2.4.egg/archetypes/kss/browser/edit_field_wrapper.pt
       ./archetypes.kss-1.4.3-py2.4.egg/archetypes/kss/browser/view_field_wrapper.pt
       ./archetypes.kss-1.6.0-py2.6.egg/archetypes/kss/browser/edit_field_wrapper.pt
       ./archetypes.kss-1.6.0-py2.6.egg/archetypes/kss/browser/view_field_wrapper.pt
       ...

   .. Note::

       Your ``eggs/`` folder may contain several versions of the same egg
       if you have re-run buildout or upgraded Plone.
       In this case the correct action is usually to pick the latest
       version.

3. Make a copy of ``.pt`` file you are going to override.

   Rename the file to its so-called *canonical* name: to do this,
   exclude the ``.egg`` folder name from the filename, and
   then replace all slashes ``/`` with dot ``.``::

       archetypes/kss/browser/edit_field_wrapper.pt

   to::

       archetypes.kss.browser.edit_field_wrapper.pt

   Drop the file in the templates folder you have registered for ``z3c.jbot``
   in your add-on.

   Make your changes in the new ``.pt`` file.

   .. warning::

       After overriding the template for the first time
       (adding the file to the ``templates/`` folder)
       you need to restart Plone.
       `z3c.jbot`_ scans new overrides only during the restart.

After the file is in place, changes to the file are instantly picked up:
the template code is re-read on every HTTP request |---| just hit enter in
your browser location bar. (Hitting enter in the location bar is quicker
than hitting :guilabel:`Refresh`, which also reloads CSS and JS files.)

If you want to override an already overridden template, read here:
<http://stackoverflow.com/questions/16209392/how-can-i-override-an-already-overriden-template-by-jbot>

More info:

* https://pypi.python.org/pypi/z3c.jbot/

* http://blog.keul.it/2011/06/z3cjbot-magical-with-your-skins.html


Main template
=============

The master page template in Plone is called ``main_template.pt`` and it is
provided by the
`Products.CMFPlone package <https://github.com/plone/Products.CMFPlone/blob/4.3.x/Products/CMFPlone/skins/plone_templates/main_template.pt>`_.

This template provides the visual frame for Plone themes. The template is
an old-style page template living in ``plone_skins/plone_templates``.

Custom per view main template
-----------------------------

Here is an example how to provide a customized main template for one view.
In this example we have customized main template so that only the content area is visible.

First we register our template in ``configure.zcml``::

    <!-- Provide a custom main_template for our consumption -->
    <browser:page
        name="widgets-demo-main-template"
        for="*"
        permission="zope.Public"
        template="barebone-main-template.pt"
        />

We refer it in our page template instead of ``here/main_template``::

     <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
           xmlns:tal="http://xml.zope.org/namespaces/tal"
           xmlns:metal="http://xml.zope.org/namespaces/metal"
           xmlns:i18n="http://xml.zope.org/namespaces/i18n"
           metal:use-macro="here/@@widgets-demo-main-template/macros/master"
           i18n:domain="plone.app.widgets"
           lang="en"
           >

``barebone-main-template.pt`` is an edited copy of ``portal_skins/sunburst_templates/main_template.pt``::

    <metal:page define-macro="master">
    <tal:doctype tal:replace="structure string:&lt;!DOCTYPE html&gt;" />

    <html xmlns="http://www.w3.org/1999/xhtml"
        tal:define="portal_state context/@@plone_portal_state;
            context_state context/@@plone_context_state;
            plone_view context/@@plone;
            lang portal_state/language;
            view nocall:view | nocall: plone_view;
            dummy python: plone_view.mark_view(view);
            portal_url portal_state/portal_url;
            checkPermission nocall: context/portal_membership/checkPermission;
            site_properties context/portal_properties/site_properties;
            ajax_load request/ajax_load | nothing;
            ajax_include_head request/ajax_include_head | nothing;"
        tal:attributes="lang lang;">

    <head>
        <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

        <metal:baseslot define-slot="base">
            <base tal:attributes="href plone_view/renderBase" /><!--[if lt IE 7]></base><![endif]-->
        </metal:baseslot>

        <tal:notajax tal:condition="python:not ajax_load or ajax_include_head">
            <div tal:replace="structure provider:plone.htmlhead" />
            <link tal:replace="structure provider:plone.htmlhead.links" />

            <tal:comment replace="nothing">
                Various slots where you can insert elements in the header from a template.
            </tal:comment>
            <metal:topslot define-slot="top_slot" />
            <metal:headslot define-slot="head_slot" />
            <metal:styleslot define-slot="style_slot" />
            <metal:javascriptslot define-slot="javascript_head_slot" />

            <meta name="viewport" content="width=device-width, initial-scale=0.6666, maximum-scale=1.0, minimum-scale=0.6666" />
            <meta name="generator" content="Plone - https://plone.org" />
        </tal:notajax>
    </head>

    <body tal:define="isRTL portal_state/is_rtl;
                      sl python:plone_view.have_portlets('plone.leftcolumn', view);
                      sr python:plone_view.have_portlets('plone.rightcolumn', view);
                      body_class python:plone_view.bodyClass(template, view);
                      classes python:context.restrictedTraverse('@@sunburstview').getColumnsClasses(view)"
        tal:attributes="class body_class;
                        dir python:isRTL and 'rtl' or 'ltr'">

    <div id="visual-portal-wrapper">

        <div id="portal-columns" class="row">

            <div id="portal-column-content" class="cell" tal:attributes="class classes/content">

                <div id="viewlet-above-content" tal:content="structure provider:plone.abovecontent" tal:condition="not:ajax_load" />

                <metal:block define-slot="content">
                    <div metal:define-macro="content"
                        tal:define="show_border context/@@plone/showToolbar; show_border python:show_border and not ajax_load"
                        tal:attributes="class python:show_border and 'documentEditable' or ''">

                        <div metal:use-macro="context/global_statusmessage/macros/portal_message">
                         Status message
                        </div>

                        <metal:slot define-slot="body">
                            <div id="content">

                                <metal:header define-slot="header" tal:content="nothing">
                                Visual Header
                                </metal:header>

                                <metal:bodytext define-slot="main">

                                 <div id="viewlet-above-content-title" tal:content="structure provider:plone.abovecontenttitle" tal:condition="not:ajax_load" />
                                  <metal:title define-slot="content-title">
                                     <metal:comment tal:content="nothing">
                                         If you write a custom title always use
                                         <h1 class="documentFirstHeading"></h1> for it
                                     </metal:comment>
                                     <h1 metal:use-macro="context/kss_generic_macros/macros/generic_title_view">
                                         Generic KSS Title. Is rendered with class="documentFirstHeading".
                                     </h1>
                                 </metal:title>

                                 <div id="viewlet-below-content-title" tal:content="structure provider:plone.belowcontenttitle" tal:condition="not:ajax_load" />

                                 <metal:description define-slot="content-description">
                                     <metal:comment tal:content="nothing">
                                         If you write a custom description always use
                                         <div class="documentDescription"></div> for it
                                     </metal:comment>
                                     <div metal:use-macro="context/kss_generic_macros/macros/generic_description_view">
                                         Generic KSS Description. Is rendered with class="documentDescription".
                                     </div>
                                 </metal:description>

                                 <div id="viewlet-above-content-body" tal:content="structure provider:plone.abovecontentbody" tal:condition="not:ajax_load" />

                                 <div id="content-core">
                                     <metal:text define-slot="content-core" tal:content="nothing">
                                         Page body text
                                     </metal:text>
                                 </div>

                                 <div id="viewlet-below-content-body" tal:content="structure provider:plone.belowcontentbody" tal:condition="not:ajax_load" />

                                </metal:bodytext>
                            </div>
                        </metal:slot>

                        <metal:sub define-slot="sub" tal:content="nothing">
                           This slot is here for backwards compatibility only.
                           Don't use it in your custom templates.
                        </metal:sub>
                    </div>
                </metal:block>

            </div>
        </div>

    </div>
    </body>
    </html>

    </metal:page>


Plone template element map
==========================

Plone 4 ships with the *Sunburst* theme. Its viewlets and viewlets managers are described :doc:`here </develop/plone/views/viewlets>`.

.. note:: Plone 3 viewlets differ from Plone 4 viewlets.

Zope Page Templates
===================

Zope Page Templates, or :term:`ZPT` for short, is an XML-based templating
language, consisting of the Template Attribute Language (:term:`TAL`), TAL
Expression Syntax (:term:`TALES`), and Macro Expansion TAL (:term:`METAL`).

It operates using two XML namespaces (``tal:`` and ``metal:``) that can
occur either on attributes of elements in another namespace (e.g. you will
often have :term:`TAL` attributes on HTML elements) or on elements (in which
case the element itself will be ignored, but all its attributes will be
recognized as :term:`TAL` or :term:`METAL` statements).

A statement in the ``tal:`` namespace will modify the element on which it
occurs and/or its child elements.

A statement in the ``metal:`` namespace defines how a template interacts
with other templates (defining or using macros and slots to be filled by
macros).

The value of an attribute in the ``tal:`` namespace is an expression. The
syntax of this expression is defined by the :term:`TALES` standard.

TAL
===

`TAL <http://wiki.zope.org/ZPT/TALSpecification14>`_ is the Template
Attribute Language used in Plone.

* `TAL Guide <http://www.owlfish.com/software/simpleTAL/tal-guide.html>`_


Escaped and unescaped content
=============================

By default, all :term:`TAL` output is escaped for security reasons::

    view.text = "<b>Test</b>"

.. code-block:: html

    <div tal:content="view/text" />

Will output escaped HTML source code:

.. code-block:: html

    &lt;b&gt;Testlt;/b&gt;

Unescaped content can be output using the TALES ``structure`` keyword
in the expression for the ``tal:replace`` and ``tal:content`` statements:

.. code-block:: html

    <div tal:replace="structure view/text" />

Will output unescaped HTML source code:

.. code-block:: html

    <b>Test</b>

METAL
======

The :term:`METAL` (Macro Expansion TAL) standard provides *macros* and
*slots* to the template language.

Using METAL macros is no longer recommended, since they couple programming
logic too tightly with the template language.  You should use views instead.

Read more about them in the
`TAL Guide <http://www.owlfish.com/software/simpleTAL/tal-guide.html>`_.

TALES expressions
======================

The value of TAL statements are defined by TALES expressions. A TALES
expression starts with the expression type. If no type is specified, the
default is assumed. Three types are standard:

* ``path:`` expressions (*default*),
* ``python:`` expressions,
* ``string:`` expressions.

They are generally useful, and not limited to use in Page Templates.
For example, they are widely used in various other parts of Plone:

* CSS and JavaScript registries, to decide whether to include a
  particular file;
* Action conditions, to decide whether to show or hide action link;
* Workflow security guards, to decide whether to allow a workflow state
  transition
* etc.

Read more about expressions in `TAL Guide <http://www.owlfish.com/software/simpleTAL/tal-guide.html>`_.

See the :doc:`Expressions chapter </develop/plone/functionality/expressions>` for more information.

Omitting tags
=================

Sometimes you need to create XML control structures which should not end up
to the output page.

You can use ``tal:omit-tag=""``:

.. code-block:: html

    <div tal:omit-tag="">
          Only the content of the tag is rendered, not the DIV tag itself.
    </div>

Images
======

See :doc:`how to use images in templates </develop/plone/images/templates>`.

Overriding templates for existing Plone views
==============================================

#. New style templates can be overridden by overriding the view using the
   template.

#. Old stype templates can be overridden by register a new skins layer in
   ``plone_skins``.

View page template
------------------

* http://lionfacelemonface.wordpress.com/2009/03/02/i-used-macros-in-my-browser-views-and-saved-a-bunch-of-money-on-my-car-insurance/

Old style page template
-----------------------

* Create a new layer in ``portal_skins``

* Templates are resolved by their name, and a property on the
  ``portal_skins`` tool defines the order in which skin layers are
  searched for the name (see the *Properties* tab on ``portal_skins``).

* You can reorder layers for the active theme so that your layer takes
  priority.

Portlet slots
=============

By default, Plone ``main_template`` has slots for left and right portlets.
If you have a view where you don't explicitly want to render portlets you
can do:

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
            xmlns:tal="http://xml.zope.org/namespaces/tal"
            xmlns:metal="http://xml.zope.org/namespaces/metal"
            xmlns:i18n="http://xml.zope.org/namespaces/i18n"
            lang="en"
            metal:use-macro="here/main_template/macros/master"
            i18n:domain="plone">

            <head>
                <metal:block fill-slot="column_one_slot" />
                <metal:block fill-slot="column_two_slot" />
            </head>

This blanks out the ``column_one_slot`` and ``column_two_slot`` slots.

Head slots
================

You can include per-template CSS and JavaScript in the ``<head>``
element using extra slots defined in Plone's ``main_template.pt``.

Note that these media files do not participate in
:doc:`portal_css </adapt-and-extend/theming/templates_css/css>` or
:doc:`portal_javascript </develop/addons/javascript/index>`
resource compression.

Extra slots are:

.. code-block:: html

    <tal:comment replace="nothing"> A slot where you can insert elements in the header from a template </tal:comment>
    <metal:headslot define-slot="head_slot" />

    <tal:comment replace="nothing"> A slot where you can insert CSS in the header from a template </tal:comment>
    <metal:styleslot define-slot="style_slot" />

    <tal:comment replace="nothing"> This is deprecated, please use style_slot instead. </tal:comment>
    <metal:cssslot define-slot="css_slot" />

    <tal:comment replace="nothing"> A slot where you can insert JavaScript in the header from a template </tal:comment>
    <metal:javascriptslot define-slot="javascript_head_slot" />

Example use:

.. code-block:: html

    <html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en"
          lang="en"
          metal:use-macro="here/main_template/macros/master"
          i18n:domain="sits">

          <metal:slot fill-slot="css_slot">
              <style media="all" type="text/css">

                .schema-browser {
                        border-collapse: collapse;
                }

                .schema-browser td,
                .schema-browser th {
                        vertical-align: top;
                        border: 1px solid #aaa;
                        padding: 0.5em;
                        text-align: left;
                }

                .default {
                        color: green;
                }

                .mandatory {
                        color: red;
                }
              </style>
          </metal:slot>

    <body>
        <metal:main fill-slot="main">
            <p>
                Protocols marked with question marks can be required or not
                depending of the current state of the patient.  For example,
                priodisability field depends on other set fields of the
                patient.
            </p>
        ...


Edit frame
---------------

By default, Plone draws a green *edit* frame around the content if you can
edit it. You might want to disable this behavior for particular views.

Hiding the edit frame
---------------------------

If you'd like to hide the (green) editing frame, place the following code in
your Zope 2-style page template::

     <metal:block fill-slot="top_slot"
                tal:define="dummy python:request.set('disable_border',1)" />

Examples of this usage:

* The `Contact info page <https://github.com/plone/Products.CMFPlone/blob/4.3.x/Products/CMFPlone/skins/plone_templates/contact-info.cpt>`_.

* The `Recently modified page <https://github.com/plone/Products.CMFPlone/blob/4.3.x/Products/CMFPlone/skins/plone_templates/recently_modified.pt>`_.

Special style on individual pages
===================================

To override page layout partially for individual pages you can use marker
interfaces to register special overriding viewlets.

More information:

* :doc:`Viewlets </develop/plone/views/viewlets>`

* http://starzel.de/blog/how-to-get-a-different-look-for-some-pages-of-a-plone-site

URL quoting inside TAL templates
----------------------------------

You need to escape TAL attribute URLs if they contain special characters like plus (+)
in query parameters. Otherwise browsers will mangle links, leading to incorrect parameter
passing.

Zope 2 provides ``url_quote()`` function which you can access

.. code-block:: xml

  <td id="cal#"
        tal:define="std modules/Products.PythonScripts.standard;
                    url_quote nocall: std/url_quote;

Then you can use this function in your TAL code

.. code-block:: xml

       <a href="#" tal:define="start_esc python:url_quote(start)"
          tal:attributes="href string: ${url}/day?currentDate=${start_esc}&xmy=${xmy}&xsub=${xsub}">

If you need to also quote spaces, use ``url_quote_plus`` rather than ``url_quote``.

Using macros
=============

Here is an example how to use `<metal:block define-macro="xxx">` and
`<metal:block use-macro="xxx">` in your :doc:`view class </develop/plone/views/browserviews>`
template files.

.. code-block:: html

      <html xmlns="http://www.w3.org/1999/xhtml"
            xmlns:tal="http://xml.zope.org/namespaces/tal"
            xmlns:metal="http://xml.zope.org/namespaces/metal"
            xmlns:i18n="http://xml.zope.org/namespaces/i18n"
            tal:omit-tag=""
            >

          <metal:row define-macro="row">
               <!--
                   A macro. You can call this using metal:use-macro
                   and pass variables to using tal:define.
               -->
          </metal:row>

          <!-- Call macro in different parts of the main template using *widget* variable as a parameter -->

          <table class="datagridwidget-table-view" tal:attributes="data-extra view/extra">

              <tbody class="datagridwidget-body">
                  <tal:row repeat="widget view/getNormalRows">
                      <tr>
                          <metal:macro use-macro="template/macros/row" />
                      </tr>
                  </tal:row>

                  <tal:row condition="view/getTTRow" define="widget view/getTTRow">
                      <tr>
                          <metal:macro use-macro="template/macros/row" />
                      </tr>
                  </tal:row>


                  <tal:row condition="view/getAARow" define="widget view/getAARow">
                      <tr>
                          <metal:macro use-macro="template/macros/row" />
                      </tr>
                  </tal:row>

          </tbody>
      </table>
      </html>

More info

* http://stackoverflow.com/q/13165748/315168

.. _z3c.jbot: https://pypi.python.org/pypi/z3c.jbot
.. _Roll out your own add-on:
.. _sane_plone_addon_template:
   https://github.com/miohtama/sane_plone_addon_template
.. |---| unicode:: U+02014 .. em dash
