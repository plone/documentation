===
CSS
===

.. admonition:: Description

    Creating and registering CSS files for Plone and Plone add-on products.
    CSS-related Python functionality.


Introduction
============

This page has Plone-specific CSS instructions.

In Plone, most CSS files are managed by the ``portal_css`` tool via the Management Interface.
Page templates can still import CSS files directly, but ``portal_css`` does CSS file compression and merging automatically if
used.

View all Plone HTML elements
============================

To test Plone HTML element rendering go to ``test_rendering`` page on your site *http://localhost:8080/Plone/test_rendering*.

It will output a styled list of all commonly used Plone user interface elements.

Registering a new CSS file
==========================

You can register stylesheets to be included in Plone's various CSS bundles
using GenericSetup XML.

Example ``profiles/default/cssregistry.xml``:

.. code-block:: xml

    <?xml version="1.0"?>
    <!-- Setup configuration for the portal_css tool. -->

    <object name="portal_css">

     <!-- Stylesheets are registered with the portal_css tool here.
          You can also specify values for existing resources if you need to
          modify some of their properties.
          Stylesheet elements accept these parameters:
          - 'id' (required): it must respect the name of the CSS or DTML file
            (case sensitive). '.dtml' suffixes must be ignored.
          - 'expression' (optional, default: ''): a TAL condition.
          - 'media' (optional, default: ''): possible values: 'screen', 'print',
            'projection', 'handheld', ...
          - 'rel' (optional, default: 'stylesheet')
          - 'rendering' (optional, default: 'import'): 'import', 'link' or
            'inline'.
          - 'enabled' (optional, default: True): boolean
          - 'cookable' (optional, default: True): boolean (aka 'merging allowed')

          See registerStylesheet() arguments in
          ResourceRegistries/tools/CSSRegistry.py for the latest list of all
          available keys and default values.
          -->

         <stylesheet
            id="++resource++yourproduct.something/yourstylesheet.css"
            cacheable="True"
            compression="safe"
            cookable="True"
            enabled="1"
            expression=""
            media=""
            rel="stylesheet"
            rendering="import"
            insert-after="ploneKss.css" />

    </object>

In this case there should be a registered resource directory named *yourproduct.something*.
In the directory should be a file yourstylesheet.css.

If you have registered the stylesheet directly in zcml

    <browser:resource
     name="yourstylesheet.css"
     file="yourstylesheet.css"
     />

then id must be

    id="++resource++yourstylesheet.css"

Expressions
-----------

The ``expression`` attribute of ``portal_css`` defines when your CSS file is included on an HTML page.

For more information see :doc:`expressions documentation </develop/plone/functionality/expressions>`.

Inserting CSS as last into anonymous bundles
---------------------------------------------

Plone compresses and merges CSS files to *bundles*.



.. TODO:: Also for Plone 4.x?

CSS files for logged-in members only
--------------------------------------

Add the following expression to your CSS file::

    not: portal/portal_membership/isAnonymousUser

If you want to load the CSS in the same bundle as Plone's default
``member.css``, use ``insert-after="member.css"``. In this case, however,
the file will be one of the first CSS files to be loaded and cannot override
values from other files unless the CSS directive ``!important`` is used.

Condition for Diazo themed sites
--------------------------------

To check if theming is active, will return true if Diazo is enabled::

    request/HTTP_X_THEME_ENABLED | nothing

Conditional comments (IE)
==============================

* https://plone.org/products/plone/roadmap/232

``cssregistry.xml`` example:

.. code-block:: xml

    <!-- Load stylesheet for IE6 - IE8 only to fix layout problems -->
    <stylesheet
        id="++resource++plonetheme.xxx.stylesheets/ie.css"
        applyPrefix="False"
        authenticated="False"
        cacheable="True"
        compression="safe"
        conditionalcomment="lt IE 9"
        cookable="True"
        enabled="1"
        expression=""
        media="screen"
        rel="stylesheet"
        rendering="link"
        title=""
        insert-before="ploneCustom.css" />


Generating CSS classes programmatically in templates
====================================================

# Try to put string generation code in your view/viewlet if you have one.

# If you do not have a view (e.g. you're dealing with ``main_template``)
  you can create a view and
  call it as in the following example.

View class generating CSS class spans::

    from Products.Five.browser import BrowserView
    from Products.CMFCore.utils  import getToolByName

    class CSSHelperView(BrowserView):
        """ Used by main_template <body> to set CSS classes """

        def __init__(self, context, request):
            self.context = context
            self.requet = request

        def logged_in_class(self):
            """ Get CSS class telling whether the user is logged in or not

            This allows us to fine-tune layout when edit frame et. al.
            are on the screen.
            """
            mt = getToolByName(self.context, 'portal_membership')
            if mt.isAnonymousUser(): # the user has not logged in
                return "member-anonymous"
            else:
                return "member-logged-in"

Registering the view in ZCML:

.. code-block:: xml

    <browser:view
            for="*"
            name="css_class_helper"
            class=".views.CSSHelperView"
            permission="zope.Public"
            allowed_attributes="logged_in_class"
            />

Calling the view in ``main_template.pt``:

.. code-block:: html

    <body
        tal:define="css_class_helper nocall:here/@@css_class_helper"
        tal:attributes="class string:${here/getSectionFromURL} template-${template/id} ${css_class_helper/logged_in_class};
                        dir python:test(isRTL, 'rtl', 'ltr')">

Defining CSS styles reaction to the presence of the class:

.. code-block:: css

    #region-content { padding: 0 0 0 0px !important;}
    .member-logged-in #region-content { padding: 0 0 0 4px !important;}

Per-folder CSS theme overrides
=================================

* https://pypi.python.org/pypi/Products.CustomOverrides

Striping listing colors
=======================

In your template you can define classes for 1) the item itself 2) extra odd
and even classes.

.. code-block:: html

     <div tal:attributes="class python:'feed-folder-item feed-folder-item-' + (repeat['child'].even() and 'even' or 'odd')">

And you can colorize this with CSS:

.. code-block:: css

    .feed-folder-item {
            padding: 0.5em;
    }

    /* Make sure that all items have same amount of padding at the bottom,
    whether they have last paragraph with margin or not.*/
    #content .feed-folder-item p:last-child {
        margin-bottom: 0;
    }

    .feed-folder-item-odd {
        background: #ddd;
    }

    .feed-folder-item-even {
        background: white;
    }


``plone.css``
=============

``plone.css`` is automagically generated dynamically based on the full
``portal_css`` registry configuration.  It is used in e.g. TinyMCE to load
all CSS styles into the TinyMCE ``<iframe>`` in a single pass. It is not
used on the normal Plone pages.

``plone.css`` generation:

* https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/skins/plone_scripts/plone.css.py

.. note: plone.css is @import-ed by dialog.css which "hides" it from a browser refresh of a normal Plone page,
   even when Plone is in development mode.  This means you may find you do not see your CSS updates within the
   TinyMCE plugin (e.g. in the link/image browser) whilst developing your theme.
   If this is the case, then simply do a hard refresh in your browser *directly* on: <yoursite>/plone.css to clear
   the cached version.

CSS reset
===========

If you are building a custom theme and you want to do a cross-browser CSS
reset, the following snippet is recommended:

.. code-block:: css

    /* @group CSS Reset .*/

    /* Remove implicit browser styles, to have a neutral starting point:
       - No elements should have implicit margin/padding
       - No underline by default on links (we add it explicitly in the body text)
       - When we want markers on lists, we will be explicit about it, and they render inline by default
       - Browsers are inconsistent about hX/pre/code, reset
       - Linked images should not have borders
       .*/

    * { margin: 0; padding: 0; }
    * :link,:visited { text-decoration:none }
    * ul,ol { list-style:none; }
    * li { display: inline; }
    * h1,h2,h3,h4,h5,h6,pre,code { font-size:1em; }
    * a img,:link img,:visited img { border:none }
    a { outline: none; }
    table { border-spacing: 0; }
    img { vertical-align: middle; }

Adding new CSS body classes
=============================

Plone themes provide certain standard CSS classes on the ``<body>`` element
to identify view, template, site section, etc. for theming.

The default body CSS classes look like this:

.. code-block:: html

  <body class="template-subjectgroup portaltype-XXX-app-subjectgroup site-LS section-courses icons-on" dir="ltr">

But you can include your own CSS classes as well.
This can be done by overriding ``plone.app.layout.globals.LayoutPolicy``
class which is registered as the ``plone_layout`` view.

``layout.py``:

.. code-block:: python

    """ Override the default Plone layout utility.
    """

    from zope.component import queryUtility
    from zope.component import getMultiAdapter

    from plone.i18n.normalizer.interfaces import IIDNormalizer
    from plone.app.layout.globals import layout as base
    from plone.app.layout.navigation.interfaces import INavigationRoot


    class LayoutPolicy(base.LayoutPolicy):
        """
        Enhanced layout policy helper.

        Extend the Plone standard class to have some more <body> CSS classes
        based on the current context.
        """

        def bodyClass(self, template, view):
            """Returns the CSS class to be used on the body tag.
            """

            # Get content parent
            body_class = base.LayoutPolicy.bodyClass(self, template, view)

            # Include context and parent ids as CSS classes on <body>
            normalizer = queryUtility(IIDNormalizer)

            body_class += " context-" + normalizer.normalize(self.context.getId())

            parent = self.context.aq_parent

            # Check that we have a valid parent
            if hasattr(parent, "getId"):
                body_class += " parent-" + normalizer.normalize(parent.getId())

            # Get path with "Default content item" wrapping applied
            context_helper = getMultiAdapter((self.context, self.request), name="plone_context_state")
            canonical = context_helper.canonical_object()

            # Mark site front page with special CSS class
            if INavigationRoot.providedBy(canonical):

                if "template-document_view" in body_class:
                    body_class += " front-page"

            # Add in logged-in / not logged in status
            portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")
            if portal_state.anonymous():
                body_class += " anonymous"
            else:
                body_class += " logged-in"

            return body_class

Related ZCML registration:

.. code-block:: xml

    <browser:page
        name="plone_layout"
        for="*"
        permission="zope.Public"
        class=".layout.LayoutPolicy"
        allowed_interface="plone.app.layout.globals.interfaces.ILayoutPolicy"
        />
