=========================================================
Upgrading Plone 4.2 to 4.3
=========================================================


.. admonition:: Description

   Instructions and tips for upgrading to a newer Plone version.

.. contents:: :local:


Updating package dependencies
========================================

Plone 4.3's dependencies have been cleaned up so it pulls in fewer packages than Plone 4.2. If your add-on uses one of the packages that was removed, it needs to be updated.

Plone includes a couple hundred Python packages as dependencies. In recent history, many of these have been packages in the zope.app.* namespace that were not strictly necessary, but included as transitive dependencies of other packages. For Plone 4.3 we made a concerted effort to remove unnecessary dependencies.

This is great because it reduces Plone's baseline memory usage and speeds imports. But it does mean that any add-ons relying on the dependencies that were removed will need to make one of the following adjustments:

1. Update imports to newer zope.* packages that have fewer dependencies, or
2. Be sure to declare their dependency in the "install_requires" setting in setup.py

Here is a full list of packages that were automatically included in Plone 4.2 but no longer in Plone 4.3:

* elementtree (lxml is used instead)
* Products.kupu
* plone.app.kss (Can be added as an add-on to regain the inline editing feature. However it will no longer be maintained as a Plone core project.)
* zope.app.cache
* zope.app.component
* zope.app.container
* zope.app.pagetemplate
* zope.app.publisher
* zope.copypastemove
* zope.dublincore
* zope.hookable

The following table lists some commonly used imports that have new preferred locations. The last column has the minimum Plone version that you need for the new location to work.

==================== ========================================== ===================================== ==========================
Name                 Old location                               New, preferred location               Minimum for new location
==================== ========================================== ===================================== ==========================
getSite, setSite     zope.app.component.hooks,                  zope.component.hooks                  Plone 4.0
                     zope.site.hooks
ISite                zope.app.component.interfaces.ISite        zope.component.interfaces.ISite       Plone 4.1
IAdding              zope.app.container.interfaces              zope.browser.interfaces               Plone 4.1
IObjectRemovedEvent  zope.app.container.interfaces              zope.lifecycleevent.interfaces        Plone 4.1
INameChooser         zope.app.container.interfaces              zope.container.interfaces             Plone 4.1
WidgetInputError     zope.app.form.interfaces                   zope.formlib.interfaces               Plone 4.1
contains             zope.app.container                         zope.container                        Plone 4.1
contained            zope.app.container                         zope.container                        Plone 4.0
ViewPageTemplateFile zope.app.pagetemplate.viewpagetemplatefile zope.browserpage.viewpagetemplatefile Plone 4.1
==================== ========================================== ===================================== ==========================

Dexterity optional extras
=========================

Plone 4.3 includes Dexterity, but without Grok or support for relations. If you need those you must require them explicitly.

The easiest way to include the optional packages is by specifying an 'extra' for the plone.app.dexterity egg.

If you use Grok (five.grok, plone.directives.form or plone.directives.dexterity)::

    [instance]
    eggs =
        plone.app.dexterity [grok]

If you need support for relations::

    [instance]
    eggs =
        plone.app.dexterity [relations]

Note that these may be combined::

    [instance]
    eggs =
        plone.app.dexterity [grok, relations]

Don't forget to reinstall Dexterity from the Add-ons control panel.

For more information see `Dexterity 2.0's release notes. <https://pypi.python.org/pypi/plone.app.dexterity/2.0>`_ 


Changed imports and functions
=============================

Codebase changes needed to upgrade your addons for Plone 4.3 compatibility:

zope.app.component.hooks.setSite
--------------------------------

Example::

    try:
     # Plone < 4.3
     from zope.app.component.hooks import setSite
    except ImportError:
     # Plone >= 4.3
     from zope.component.hooks import setSite  # NOQA 

zope.app.publisher.interfaces.IResource
---------------------------------------

Example::

    try:
     # Plone < 4.3
     from zope.app.publisher.interfaces import IResource
    except ImportError:
     # Plone >= 4.3
     from zope.browserresource.interfaces import IResource

plone.app.content.batching.Batch
--------------------------------

Example::

    try:
        from plone.app.content.batching import Batch # Plone < 4.3
        HAS_PLONE43 = False
    except ImportError:
        from plone.batching import Batch # Plone >= 4.3
        HAS_PLONE43 = True

The two implementations have a different API.

The pagesize argument is named size in plone.app.batching; also, instead of a page number a start index is required.

If you have a piece of code like this::

    b = Batch(items,
                  pagesize=pagesize,
                  pagenumber=pagenumber)

you should change it to look like this::

    if HAS_PLONE43:
        b = Batch(items,
                size=pagesize,
                start=pagenumber * pagesize)
    else:
        b = Batch(items,
                pagesize=pagesize,
                pagenumber=pagenumber)

plone.directives.form
--------------------------------

You need to use special egg declaration::

    eggs =
         plone.app.dexterity [grok]

For more information see Dexterity info page on this manual.

five.intid and z3c.relationfield
----------------------------------

If you get::

    AttributeError: type object 'IIntIds' has no attribute 'iro'

or::

    AttributeError: type object 'ICatalog' has no attribute '__iro__'

or::

    AttributeError: getObject

include Dexterity with relations extras in buildout.cfg::

    eggs =
          plone.app.dexterity [relations]

See Dexterity migrations page for more information.


portal_syndication removed
--------------------------

The portal_syndication tool has been removed and replaced with the @@syndication-utils browser view

This is an example of the type of change required to adapt::

    <p class="discreet"
      tal:condition="context/portal_syndication/isSiteSyndicationAllowed">
     <a href=""
         class="link-feed"
         i18n:translate="title_rss_feed"
         tal:define="here_url context/@@plone_context_state/object_url"
         tal:attributes="href string:$here_url/search_rss?${request/QUERY_STRING}">
     Subscribe to an always-updated feed of these search terms</a>
    </p>

The lookup of portal_syndication above should be changed as follows::

    <p class="discreet"
      tal:condition="context/@@syndication-util/search_rss_enabled">
     <a href=""
         class="link-feed"
         i18n:translate="title_rss_feed"
         tal:define="here_url context/@@plone_context_state/object_url"
         tal:attributes="href string:$here_url/search_rss?${request/QUERY_STRING}">
     Subscribe to an always-updated feed of these search terms</a>
    </p>

Please see `Products.CMFPlone.browser.syndication.utils <https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/syndication/utils.py>`_ for information on the API provided by this view.


Grok static folders
===================

**Grok 1.3 does not support autodiscovered static folders**

If you are using :doc:`static folder functionality of Grok </adapt-and-extend/theming/templates_css/resourcefolders>` it no longer works with Plone 4.3.

To work around this manually declare your static folder in configure.zcml::

    <configure
        ...
        xmlns:browser="http://namespaces.zope.org/browser"
        >

      <!-- Grok the package to initialise schema interfaces and content classes -->
      <grok:grok package="." />

      <browser:resourceDirectory
         name="your.package"
         directory="static"
         />

    </configure>


Hiding KSS spinner
==================

KSS is not shipped anyore. You might want to hide related theme elements if you have a custom theme.

Hide KSS spinner in your custom CSS::

    #kss-spinner {
         display: none;
    }
