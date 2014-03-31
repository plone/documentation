==========================
Theming guide for Plone 3
==========================

.. contents :: :local:

Preface
-------------

This is a theming guide for Plone 3. The technologies here work
directly on Zope Page Templates (TAL) and viewlets.
On Plone 4.2+ versions of Plone the suggested approach for theming your site
is `plone.app.theming <https://pypi.python.org/pypi/plone.app.theming>`_
where you can create your theme through-the-web and with less
needed low level programming information.

Even if not recommended the techniques described are
still useful and might be needed with new versions of Plone.
Please consult
`stackoverflow.com (plone tag) <http://stackoverflow.com/questions/tagged/plone>`_ or
`plone-users mailing list <http://plone.org/support/forums/general>`_
when in confusion.

Introduction
-------------

.. toctree::
    :maxdepth: 1

    intro/intro
    intro/what
    intro/overview

Quick start
-------------

.. toctree::
    :maxdepth: 1

    quick-start/overview
    quick-start/change-the-logo
    quick-start/change-the-font-colours
    quick-start/firefox-mozilla-ui-development-tools

Approaches
------------

.. toctree::
    :maxdepth: 1

    approaches/plonedefault
    approaches/filesystem
    approaches/directions

Tools
---------

.. toctree::
    :maxdepth: 1

    tools/authoring
    tools/debug
    tools/egg1/overview

Building blocks
-------------------

Skin, Components, Configuration. The three main building blocks of a
theme; interconnected, but each with a distinctive way of behaving.

**Overview**

.. toctree::
    :maxdepth: 1

    buildingblocks/overview
    buildingblocks/skin/locations

**Templates**

.. toctree::
    :maxdepth: 1

    buildingblocks/skin/templates/overview
    buildingblocks/skin/templates/getting-started
    buildingblocks/skin/templates/advanced-usage
    buildingblocks/skin/templates/create-an-alternative-edit-template
    buildingblocks/skin/templates/global-template-variables
    buildingblocks/skin/templates/macros-and-slots
    buildingblocks/skin/templates/how-to-customise-view-or-edit-on-archetypes-content-items
    buildingblocks/skin/templates/customizing-at-templates/introduction
    buildingblocks/skin/templates/customizing-at-templates/what-makes-it-tick
    buildingblocks/skin/templates/customizing-at-templates/customizing-widgets
    buildingblocks/skin/templates/customizing-at-templates/total-control-the-view-template
    buildingblocks/skin/templates/customizing-at-templates/conclusion
    buildingblocks/skin/templates/customizing-at-templates/reference

**Skin layers**

.. toctree::
    :maxdepth: 1

    buildingblocks/skin/layers/overview
    buildingblocks/skin/layers/precedence
    buildingblocks/skin/layers/making

**CSS stylesheets on skin layers**

.. toctree::
    :maxdepth: 1

    buildingblocks/skin/style-sheets/customstylesheet

**Components**

.. toctree::
    :maxdepth: 1

    buildingblocks/components/index
    buildingblocks/components/wiring
    buildingblocks/components/viewletsandportlets
    buildingblocks/components/customizing
    buildingblocks/components/componentparts/interfaces
    buildingblocks/components/componentparts/pythonclasses
    buildingblocks/components/componentparts/permissions
    buildingblocks/components/themespecific
    buildingblocks/components/skinorcomponents
    buildingblocks/components/locations

**Configuration**

.. toctree::
    :maxdepth: 1

    buildingblocks/configuration/profiles
    buildingblocks/configuration/gsxml
    buildingblocks/configuration/tool
    buildingblocks/configuration/locations

Page
-------

How do all these bits and pieces go together to make up a web page? And,
more importantly, how do you get content onto the page?


.. toctree::
    :maxdepth: 1

    page/content/overview
    page/templates/overview
    page/templates/folder-views-example
    page/templates/how-to-scale-images-using-pil-in-page-templates
    page/buildingblocks/components/skinorcomponents
    page/using-jquery-and-jquery-tools
    page/otherinfo

Elements
--------------

A reference for the viewlets, portlets, viewlet managers, and portlet
columns which make up a page. There's a quick reference to each
component type with links and reminders on how to handle them, a visual
index of page elements plus code snippets to make your life easier.

**Viewlet**

.. toctree::
    :maxdepth: 1

    elements/viewlet/anatomy
    elements/viewlet/override/overview
    elements/viewlet/move/overview

**Viewlet manager**

.. toctree::
    :maxdepth: 1

    elements/viewletmanager/anatomy
    elements/viewletmanager/override
    elements/viewletmanager/move

**Portlet**

.. toctree::
    :maxdepth: 1

    elements/portlet/anatomy
    elements/portlet/move
    elements/portlet/override
    elements/portlet/override-the-portlets-in-plone-3.0

**Portlet manager**

.. toctree::
    :maxdepth: 1

    elements/portletmanager/createnew
    elements/portletmanager/move
    elements/portletmanager/hide
    elements/portletmanager/practical/adding-portlet-managers

**Structural elements**

.. toctree::
    :maxdepth: 1

    elements/structuralelements/plone.header

**Visible elements**

.. toctree::
    :maxdepth: 1

    elements/visibleelements/plone.abovecontenttitle.documentactions
    elements/visibleelements/plone.app.i18n.locales.languageselector
    elements/visibleelements/plone.belowcontentbody.contenthistory
    elements/visibleelements/plone.belowcontentbody.relateditems
    elements/visibleelements/plone.belowcontentbody.workflowhistory
    elements/visibleelements/plone.belowcontenttitle.documentbyline
    elements/visibleelements/plone.belowcontenttitle.keywords
    elements/visibleelements/plone.colophon
    elements/visibleelements/plone.comments
    elements/visibleelements/plone.contentactions
    elements/visibleelements/plone.contentviews
    elements/visibleelements/plone.footer
    elements/visibleelements/plone.global_sections
    elements/visibleelements/plone.lockinfo
    elements/visibleelements/plone.logo
    elements/visibleelements/plone.nextprevious
    elements/visibleelements/plone.path_bar
    elements/visibleelements/plone.personal_bar
    elements/visibleelements/plone.presentation
    elements/visibleelements/plone.searchbox
    elements/visibleelements/plone.site_actions
    elements/visibleelements/plone.tableofcontents

**Hidden elements**

.. toctree::
    :maxdepth: 1

    elements/hiddenelements/plone.analytics
    elements/hiddenelements/plone.htmlhead.dublincore
    elements/hiddenelements/plone.htmlhead.kss-base-url
    elements/hiddenelements/plone.htmlhead.title
    elements/hiddenelements/plone.links.author
    elements/hiddenelements/plone.links.favicon
    elements/hiddenelements/plone.links.navigation
    elements/hiddenelements/plone.links.RSS
    elements/hiddenelements/plone.links.search
    elements/hiddenelements/plone.nextprevious.links
    elements/hiddenelements/plone.skip_links
    elements/index.rst

Where is what?
------------------

How to locate the bits and pieces you need. Links to useful visual aids
for identifying page elements, pointers to locating your product and
eggs directories, diagrams of a theme egg on the file system.

.. toctree::
    :maxdepth: 1

    whereiswhat/components
    whereiswhat/configuration
    whereiswhat/egg
    whereiswhat/egglocation
    whereiswhat/page
    whereiswhat/productlocation
    whereiswhat/productsdirectory
    whereiswhat/skin
    whereiswhat/theme
    whereiswhat/zopeinstance
    whereiswhat/index



