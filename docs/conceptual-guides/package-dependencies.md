---
myst:
  html_meta:
    "description": "This chapter describes the architecture of Plone's packages and dependencies."
    "property=og:description": "This chapter describes the architecture of Plone's packages and dependencies."
    "property=og:title": "Architecture: packages and dependencies"
    "keywords": "Architecture, packages, dependencies, Plone"
---

# Architecture: packages and dependencies

This chapter describes the architecture of Plone's packages and dependencies.


## Motivation

Over the years, Plone has developed many indirections in its packages and dependencies.
The goal in the long run is to untangle them and get a simple dependency graph.
This document shows the current state, as an orientation to its architecture.


## Overview

There are multiple level of dependencies:

-   package level (`setup.py`/`setup.cfg`/`pyproject.toml`)
-   Python level (imports)
-   {term}`ZCML` level (includes)
-   testing (need for layers, such as functional testing)

Circular dependencies at the package level have now been resolved.
Nevertheless, there is indirection on all other levels.
Since Plone consists of a lot of packages, it is complex to untangle those.


## Mental model

This section describes a mental model that organizes Plone 6.1 packages into three groups separated by two packages that define the borders between these groups.


### Borders

In Plone 6.1, there are two packages that serve as dividing lines.

1.  `Products.CMFPlone` and all packages below it define the Plone core.
    Everything in here depends on the `plone.base`.
2.  `plone.base` is the border between the Application Server and Content Management Framework (CMF) with its dependencies.

```{mermaid}
:alt: Mental model of Plone
:caption: _Mental model of Plone_

block-beta
    columns 4
    Plone["Plone<br/>integraton of all in one release"]:4
    Distributions
    Upgrade
    coreapis["Core APIs"]
    coreaddons["Core add-ons"]
    cmfplone["Products.CMFPlone"]:4
    ploneapp["Most of plone.app.* namespace"]:2
    otherlay["Various related packages"]:2
    plonebase["plone.base"]:4
    block:groupfoundation:4
        zopecore["Zope core/ ZCA"]
        zopeeco["Zope ecosystem"]
        cmfcore["CMFCore"]
        ploneworld["Plone generic libraries"]
        libraries["Other libraries"]
    end  
    style cmfplone fill:#fff9e6
    style plonebase fill:#fff9e6
```

### Main components

The following points describe the mental model.

-   Foundation:
    - `Zope` core and its dependencies is the application server,
    - the Zope component architecture (ZCA) framework and 
    - some additional packages from the wider Zope ecosystem.
    - Then there are generic, standalone Plone libraries,  
    - plus various other Python libraries.
-   `Products.CMFCore` provides very basic content management features on top of Zope on which Plone relies.
-   `plone.base` defines several interfaces as contracts for the component architecture on which Plone is built.
    Additionally, it provides some base classes and utility functions that Plone often uses. 
    It also depends on `Products.CMFCore`, and therefore `Zope`.
    Additionally, it depends on generic functionality provided by `plone.dexterity`, `plone.behavior`, and `plone.registry`.
-   The space of many `plone.*`, `plone.app.*`, and their related libraries defines the core of Plone.
-   On top of this core, depending on these packages, is `Products.CMFPlone`, which is the package to depend on if the basic Plone core is referenced.
-   On top of `Products.CMFPlone` are the following.
    -   The core APIs `plone.api` and `plone.restapi`.
    -   There is distribution support in `plone.distribution` and specific distributions, currently `plone.volto` and `plone.classicui`.
    -   Core add-ons include Working Copy Support from `plone.app.iterate`, discussion support (`plone.app.discussion`), and other add-ons.
    -   `plone.app.upgrade` is the package to upgrade between Plone versions.
-   If you want to depend on the whole Plone with everything, you should depend on the package `Plone`.
    This meta package without any code depends on all other packages.
    It is what you want to install if you don't care about the details and get "batteries included".


### The space on top of `Products.CMFPlone`

Add-on developers and integrators primarily interact with the dependencies on top of `Products.CMFPlone`.
The following diagram visualizes this part.
You can zoom in on the diagram.

```{mermaid}
:config: {"sankey": {"showValues": false, "width": 1600, "height": 800, "nodeAlignment": "right"}}
:zoom:
:alt: Diagram of the space on top of Products.CMFPlone
:caption: _Diagram of the space on top of `Products.CMFPlone`_

sankey-beta

    Plone,Distributions,100

    Distributions,plone.volto,50
    Distributions,plone.classicui,30
    Distributions,other dist.,20



    plone.volto,plone.distribution,10
    plone.volto,plone.restapi,20
    plone.volto,plone.api,20

    Multlilingual,plone.api,20
    Commenting,plone.api,20
    Working Copies,plone.api, 20
    Caching,plone.api,20

    plone.classicui,plone.distribution,15
    plone.classicui,plone.api,15
    other dist.,plone.distribution,4
    other dist.,plone.api,8
    other dist.,plone.restapi,8


    Plone,Core-Addons,80

    Core-Addons,Multlilingual,20
    Core-Addons,Commenting,20
    Core-Addons,Working Copies,20
    Core-Addons,Caching,20

    plone.distribution,Export/Import,15
    plone.distribution,plone.api,14
    plone.restapi,Core,20
    Export/Import,plone.api,8
    plone.restapi,plone.api,15
    Export/Import,plone.restapi,7
    Upgrade,Core,20
    plone.api,Core,160

    Plone,Upgrade,20
```


## Detailed view of the architecture

The following diagram provides a more detailed view of the whole architecture of Plone.
You can zoom in on the diagram.

```{mermaid}
:config: {"theme": "base", "darkMode": "true"}
:zoom:
:alt: Architecture of Plone
:caption: _Architecture of Plone_

%%{
  init: {
    'theme': 'base',
    'themeVariables': {
      'primaryColor': '#fefefe',
      'lineColor': '#aaa'
    }
  }
}%%

flowchart TB
 subgraph Release["Release"]
        Plone[["'Plone' Package"]]
  end
 subgraph subGraph1["Distributions"]
        volto{{"plone.volto"}}
        classicui{{"plone.classicui"}}
        other{{"other ..."}}
  end
 subgraph Core-Addons["Core-Addons"]
        multilingual("Multilingual")
        iterate("Working Copies")
        discussion("Commenting")
        caching("Caching")
  end
 subgraph API["API"]
        restapi("RestAPI")
        ploneapi("API")
        upgrade("Upgrade")
        exportimport("Export/Import")
        distribution["Distribution"]
  end
 subgraph subGraph4["The Inner Core"]
        thecore((("Core-Features: plone.*, ...")))
  end
 subgraph Core["Core"]
        cmfplone["Products.CMFPlone"]
        plonebase["plone.base"]
        subGraph4
  end
 subgraph Foundations["Foundations"]
        zope["Zope/CMF/ZODB/..."]
        supportlibs["Several Supporting Libraries"]
  end
    Plone == provides ==> volto
    Plone -. provides .-> classicui & other & upgrade & multilingual & iterate & discussion & caching
    volto -- installs --> restapi
    volto == is a ==> distribution
    classicui -. is a .-> distribution
    other -. is a .-> distribution
    distribution -- uses --> exportimport
    distribution == depends on ==> ploneapi
    restapi -- depends on --> ploneapi
    cmfplone == depends on ==> thecore
    thecore == depends on ==> plonebase
    plonebase == depends on ==> zope
    plonebase -- depends on --> supportlibs
    zope -- depends on --> supportlibs
    ploneapi == depends on ==> cmfplone
    upgrade -- depends on --> cmfplone
    multilingual -- depends on --> ploneapi
    iterate -- depends on --> ploneapi
    discussion -- depends on --> ploneapi
    caching -- depends on --> ploneapi
    exportimport -- uses serializers of --> restapi
    exportimport -- depends on --> ploneapi
```


## Packages in detail

Looking deeper into those packages, there are more subdivisions which fall into three groups.


### Above `Products.CMFPlone`

-   Plone
-   plone.api
-   plone.app.caching
-   plone.app.discussion
-   plone.app.iterate
-   plone.app.multilingual
-   plone.app.upgrade
-   plone.classicui
-   plone.distribution
-   plone.exportimport
-   plone.restapi
-   plone.volto
-   Products.CMFPlacefulWorkflow

### Between `Products.CMFPlone` and `plone.base`

-   collective.monkeypatcher
-   plone.app.content
-   plone.app.contentlisting
-   plone.app.contentmenu
-   plone.app.contentrules
-   plone.app.contenttypes
-   plone.app.customerize
-   plone.app.dexterity
-   plone.app.event
-   plone.app.i18n
-   plone.app.intid
-   plone.app.layout
-   plone.app.linkintegrity
-   plone.app.locales
-   plone.app.lockingbehavior
-   plone.app.portlets
-   plone.app.querystring
-   plone.app.redirector
-   plone.app.registry
-   plone.app.relationfield
-   plone.app.textfield
-   plone.app.theming
-   plone.app.users
-   plone.app.uuid
-   plone.app.versioningbehavior
-   plone.app.viewletmanager
-   plone.app.vocabularies
-   plone.app.widgets
-   plone.app.workflow
-   plone.app.z3cform
-   plone.browserlayer
-   plone.cachepurging
-   plone.contentrules
-   plone.formwidget.namedfile
-   plone.formwidget.recurrence
-   plone.i18n
-   plone.namedfile
-   plone.outputfilters
-   plone.portlet.collection
-   plone.portlet.static
-   plone.portlets
-   plone.protect
-   plone.resourceeditor
-   plone.rfc822
-   plone.schemaeditor
-   plone.session
-   plone.staticresources
-   plone.stringinterp
-   plone.theme
-   plonetheme.barceloneta
-   Products.isurlinportal


### The foundation below `plone.base`


#### Plone world

-   borg.localrole
-   plone.alterego
-   plone.autoform
-   plone.autoinclude
-   plone.batching
-   plone.behavior
-   plone.caching
-   plone.dexterity
-   plone.event
-   plone.folder
-   plone.indexer
-   plone.intelligenttext
-   plone.keyring
-   plone.locking
-   plone.memoize
-   plone.registry
-   plone.resource
-   plone.rest
-   plone.scale
-   plone.schema
-   plone.subrequest
-   plone.supermodel
-   plone.transformchain
-   plone.uuid
-   plone.z3cform
-   Products.DateRecurringIndex
-   Products.ExtendedPathIndex
-   Products.MimetypesRegistry
-   Products.PlonePAS
-   Products.PortalTransforms
-   Products.statusmessages


#### Zope ecosystem

-   Chameleon
-   diazo
-   five.customerize
-   five.intid
-   five.localsitemanager
-   icalendar
-   Products.CMFCore
-   Products.CMFDiffTool
-   Products.CMFDynamicViewFTI
-   Products.CMFEditions
-   Products.CMFUid
-   Products.DCWorkflow
-   Products.ExternalMethod
-   Products.GenericSetup
-   Products.MailHost
-   Products.PluggableAuthService
-   Products.PluginRegistry
-   Products.PythonScripts
-   Products.Sessions
-   Products.SiteErrorLog
-   Products.StandardCacheManagers
-   Products.ZopeVersionControl
-   repoze.xmliter
-   webresource
-   z3c.caching
-   z3c.form
-   z3c.formwidget.query
-   z3c.objpath
-   z3c.pt
-   z3c.relationfield
-   z3c.zcmlhook
-   zc.recipe.egg
-   zc.relation
-   zodbverify
-   zope.copy
-   zope.intid
-   zope.keyreference


#### Zope core

-   AccessControl
-   Acquisition
-   AuthEncoding
-   beautifulsoup4
-   BTrees
-   DateTime
-   DocumentTemplate
-   ExtensionClass
-   Missing
-   MultiMapping
-   Persistence
-   persistent
-   Products.BTreeFolder2
-   Products.ZCatalog
-   Record
-   RestrictedPython
-   transaction
-   zc.lockfile
-   ZConfig
-   zdaemon
-   ZEO
-   zExceptions
-   ZODB
-   ZODB3
-   zodbpickle
-   Zope
-   zope.annotation
-   zope.app.locales
-   zope.browser
-   zope.browsermenu
-   zope.browserpage
-   zope.browserresource
-   zope.cachedescriptors
-   zope.component
-   zope.componentvocabulary
-   zope.configuration
-   zope.container
-   zope.contentprovider
-   zope.contenttype
-   zope.datetime
-   zope.deferredimport
-   zope.deprecation
-   zope.dottedname
-   zope.event
-   zope.exceptions
-   zope.filerepresentation
-   zope.globalrequest
-   zope.hookable
-   zope.i18n
-   zope.i18nmessageid
-   zope.interface
-   zope.lifecycleevent
-   zope.location
-   zope.pagetemplate
-   zope.processlifetime
-   zope.proxy
-   zope.ptresource
-   zope.publisher
-   zope.ramcache
-   zope.schema
-   zope.security
-   zope.sendmail
-   zope.sequencesort
-   zope.site
-   zope.size
-   zope.structuredtext
-   zope.tal
-   zope.tales
-   zope.testbrowser
-   zope.testing
-   zope.traversing
-   zope.viewlet
-   Zope2


#### Libraries

-   attrs
-   cffi
-   cssselect
-   decorator
-   docutils
-   feedparser
-   future
-   importlib_metadata
-   jsonschema
-   Markdown
-   multipart
-   Paste
-   PasteDeploy
-   piexif
-   Pillow
-   pycparser
-   PyJWT
-   pyrsistent
-   python_dotenv
-   python_gettext
-   requests
-   roman
-   sgmllib3k
-   simplejson
-   soupsieve
-   Unidecode
-   urllib3
-   waitress
-   WebOb
-   WebTest
-   WSGIProxy2
-   zipp
