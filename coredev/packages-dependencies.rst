======================================
Architecture: Packages and Dependecies
======================================

Motivation
==========

In past lots of indirections were introduced in our packages and dependecies.

Our goal in the long run is to untangle them and get a directed dependency graph.

This document shows the current state as an orientation.


Overview
========

There are multiple level of dependencies:

- package level (setup.py/cfg)
- Python level (imports)
- zcml level (includes)
- testing (need for layers, i.e. functional testing)

We do not have any circular dependencies on package level anymore. This was solved already.

Nevertheless we have indirection on all other levels. Since Plone consists of a lot of packages it is complex to untangle those.

Mental Model
============

A base mental model for how Plone is organized in Plone 6 since alpha 4 is like so::

    ┌────────────────────────────┐
    │                            │
    │ On top of Products.CMFPlone│
    │ like:                      │
    │ - Plone                    │
    │ - plone.api                │
    │ - plone.volto              │
    │ - plone.app.iterate        │
    │ - plone.app.update         │
    │                            │
    ├────────────────────────────┤
    │                            │
    │     Products.CMFPlone      │
    │                            │
    ├────────────────────────────┤
    │                            │
    │ The space between          │
    │                            │
    │ - most of plone.app.*      │
    │ - but also some other      │
    │                            │
    │                            │
    ├────────────────────────────┤
    │                            │
    │         plone.base         │
    │                            │
    ├────────────────────────────┤
    │                            │
    │ The Foundations            │
    │                            │
    │ - Zope                     │
    │ - CMFCore                  │
    │ - PAS/PlonePAS             │
    │ - plone.registry           │
    │ - plone.dexterity          │
    │ - plone.behavior           │
    │ - ....                     │
    │                            │
    └────────────────────────────┘

So as a rough model we have two packages as dividing lines:

1. ``Products.CMFPlone``
2. ``plone.base``

Packages in Detail
==================

If we look deeper into those we have more sub-dividers, but first group all into the three groups:

Then, based on the 6.0.0.a4 release, These are the packages:

Above ``Products.CMFPlone``
---------------------------

- Plone
- plone.api
- plone.app.iterate
- plone.app.upgrade
- plone.restapi
- plone.volto
- Products.CMFPlacefulWorkflow


Between ``Products.CMFPlone`` and ``plone.base``
------------------------------------------------

- collective.monkeypatcher
- plone.app.caching
- plone.app.content
- plone.app.contentlisting
- plone.app.contentmenu
- plone.app.contentrules
- plone.app.contenttypes
- plone.app.customerize
- plone.app.dexterity
- plone.app.discussion
- plone.app.event
- plone.app.i18n
- plone.app.intid
- plone.app.layout
- plone.app.linkintegrity
- plone.app.locales
- plone.app.lockingbehavior
- plone.app.multilingual
- plone.app.portlets
- plone.app.querystring
- plone.app.redirector
- plone.app.registry
- plone.app.relationfield
- plone.app.textfield
- plone.app.theming
- plone.app.users
- plone.app.uuid
- plone.app.versioningbehavior
- plone.app.viewletmanager
- plone.app.vocabularies
- plone.app.widgets
- plone.app.workflow
- plone.app.z3cform
- plone.browserlayer
- plone.cachepurging
- plone.contentrules
- plone.formwidget.namedfile
- plone.formwidget.recurrence
- plone.i18n
- plone.namedfile
- plone.outputfilters
- plone.portlet.collection
- plone.portlet.static
- plone.portlets
- plone.protect
- plone.resourceeditor
- plone.rfc822
- plone.schemaeditor
- plone.session
- plone.staticresources
- plone.stringinterp
- plone.theme
- plonetheme.barceloneta
- Products.isurlinportal


The Foundation Below ``plone.base``
-----------------------------------

Plone World
~~~~~~~~~~~

- borg.localrole
- plone.alterego
- plone.autoform
- plone.autoinclude
- plone.batching
- plone.behavior
- plone.caching
- plone.dexterity
- plone.event
- plone.folder
- plone.indexer
- plone.intelligenttext
- plone.keyring
- plone.locking
- plone.memoize
- plone.registry
- plone.resource
- plone.rest
- plone.scale
- plone.schema
- plone.subrequest
- plone.supermodel
- plone.transformchain
- plone.uuid
- plone.z3cform
- Products.DateRecurringIndex
- Products.ExtendedPathIndex
- Products.MimetypesRegistry
- Products.PlonePAS
- Products.PortalTransforms
- Products.statusmessages

Zope Ecosystem
~~~~~~~~~~~~~~

- Chameleon
- diazo
- five.customerize
- five.intid
- five.localsitemanager
- icalendar
- Products.CMFCore
- Products.CMFDiffTool
- Products.CMFDynamicViewFTI
- Products.CMFEditions
- Products.CMFUid
- Products.DCWorkflow
- Products.ExternalMethod
- Products.GenericSetup
- Products.MailHost
- Products.PluggableAuthService
- Products.PluginRegistry
- Products.PythonScripts
- Products.Sessions
- Products.SiteErrorLog
- Products.StandardCacheManagers
- Products.ZopeVersionControl
- repoze.xmliter
- webresource
- z3c.caching
- z3c.form
- z3c.formwidget.query
- z3c.objpath
- z3c.pt
- z3c.relationfield
- z3c.zcmlhook
- zc.recipe.egg
- zc.relation
- zodbverify
- zope.copy
- zope.intid
- zope.keyreference

Zope Core
~~~~~~~~~

- AccessControl
- Acquisition
- AuthEncoding
- beautifulsoup4
- BTrees
- DateTime
- DocumentTemplate
- ExtensionClass
- Missing
- MultiMapping
- Persistence
- persistent
- Products.BTreeFolder2
- Products.ZCatalog
- Record
- RestrictedPython
- transaction
- zc.lockfile
- ZConfig
- zdaemon
- ZEO
- zExceptions
- ZODB
- ZODB3
- zodbpickle
- Zope
- zope.annotation
- zope.app.locales
- zope.browser
- zope.browsermenu
- zope.browserpage
- zope.browserresource
- zope.cachedescriptors
- zope.component
- zope.componentvocabulary
- zope.configuration
- zope.container
- zope.contentprovider
- zope.contenttype
- zope.datetime
- zope.deferredimport
- zope.deprecation
- zope.dottedname
- zope.event
- zope.exceptions
- zope.filerepresentation
- zope.globalrequest
- zope.hookable
- zope.i18n
- zope.i18nmessageid
- zope.interface
- zope.lifecycleevent
- zope.location
- zope.pagetemplate
- zope.processlifetime
- zope.proxy
- zope.ptresource
- zope.publisher
- zope.ramcache
- zope.schema
- zope.security
- zope.sendmail
- zope.sequencesort
- zope.site
- zope.size
- zope.structuredtext
- zope.tal
- zope.tales
- zope.testbrowser
- zope.testing
- zope.traversing
- zope.viewlet
- Zope2

Libraries
~~~~~~~~~

- attrs
- cffi
- cssselect
- decorator
- docutils
- feedparser
- future
- importlib_metadata
- jsonschema
- Markdown
- multipart
- Paste
- PasteDeploy
- piexif
- Pillow
- pycparser
- PyJWT
- pyrsistent
- python_dotenv
- python_gettext
- requests
- roman
- sgmllib3k
- simplejson
- soupsieve
- Unidecode
- urllib3
- waitress
- WebOb
- WebTest
- WSGIProxy2
- zipp
