=======================
Component architecture
=======================

Introduction 
----------------

Plone logic is wired together by Zope 3 component architecture.
It provides "enterprise business logic" engine for Plone.

The architecture provides pluggable system :doc:`interfaces </develop/addons/components/interfaces>`, 
adapters, utilities
and registries. The wiring of components is done on XML based language
called :doc:`ZCML </develop/addons/components/zcml>`.

Grok - wrapper around Z3
============================

On Z3 component layer there exist higher level framework called :doc:`Grok </develop/addons/components/grok>`
which gives you a way to automatic scan Python modules for decorators and directives without
the need off manually writing ZCML code or Python to register your business logic.

Database drops using Generic setup
====================================

Zope 3 components act on Python codebase level which is shared by all sites in the 
same Zope application server process.
When you install new add-ons to Plone site, the add-ons modify the site database
using :doc:`GenericSetup </components/genericsetup>` framework. GenericSetup
is mostly visible as */profiles/default* folder and its XML files 
in your add-on.

More info

* http://www.muthukadan.net/docs/zca.html

.. toctree::
    :maxdepth: 1

    interfaces
    adapters
    utilities
    zcml
    grok
    genericsetup
    events
    customizing_plone
