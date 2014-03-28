=========================================================
Upgrading Plone 4.1 to 4.2
=========================================================


.. admonition:: Description

   Instructions and tips for upgrading to a newer Plone version.

.. contents:: :local:


Upgrades to zc.buildout
========================================

By default, bootstrap.py now uses zc.buildout version 1.5.2 instead of 1.4.4. 1.5.2 no longer references your global python site packages and you may need to upgrade any custom products to specifically pull those package into the local build.

If you are having buildout ills, please check the `buildout troubleshooting guide <http://buildoutcoredev.readthedocs.org/en/latest/issues.html>`_ to try and fix it.


Search Templates
========================================

Search has been dramatically improved in 4.2, but that means that any customizations you may have made could be gone or just plain won't work. If you previously customized search in your custom folder or anywhere in skins, note that your shizzle won't work anymore.

You can do two things (I think - I'm sure there is a better way but if anyone has an idea paste it here!). You can keep your search form and all of it's logic in template mumble jumble. That info is below but why would you want to do that? I recommend customizing the shiny NEW search template to have your changes once again since it's just so gosh darn pretty.

To upgrade your sites search to be more like what you want (and flex your brain), copy `plone.app.search/plone/app/search/search.pt <https://github.com/plone/plone.app.search/blob/master/plone/app/search/search.pt>`_ into your templates folder in your product. Something like my.site/my/site/browser/templates/mysite_search.pt. I recommend using another name besides search.pt for sanity. Then override the search view to use the new template in your configure.zcml (likely in browser)::

    <browser:page
     name="search"
     class="plone.app.search.browser.Search"
     permission="zope2.View"
     for="Products.CMFPlone.interfaces.IPloneSiteRoot"
     layer="my.site.interfaces.IMySiteLayer"
     template="templates/mysite_search.pt"/>

Restart and make sure that's all working. Then update that search template to have all your changes that you had in the old template.

If you aren't convinced by the boat load of pretty that is the new search form, don't copy or paste anything and just omit the class= line in the code above. You can paste your old template as is. I'll sigh for you... *sigh*. It will look something like::

<browser:page
 name="search"
 permission="zope2.View"
 for="Products.CMFPlone.interfaces.IPloneSiteRoot"
 layer="my.site.interfaces.IMySiteLayer"
 template="templates/search.pt"/>


Upgrading to new collections
========================================

Upgrading
---------

When upgrading your Plone site, the old collections will still be available to you only they're now labeled "Collection (old-style)." Old collections will NOT be migrated to new-style collections.

Enabling old-style collections
-----------------------------------

If you're starting a new Plone site from scratch, the old collections will not be enabled by default and you may still want to use them on your site--especially if you're running add-ons that still depend on the old-style collections.

To manual enable old-style collections, follow these steps:

1. Visit the ZMI(or append /manage onto the url of your plone site)
2. Click "portal_types"
3. Click "Topic (Collection (old-style))"
4. Check the "Implicitly addable?"
5. Click the "Save" button


Developing for old and new collections
----------------------------------------

New style collections still implement the queryCatalog method which results the results from the catalog query so most likely the only thing you'll need to change is interface registrations and references to portal_type.

I have just updated collective.plonetruegallery for the new collections so I'll share some tips on integrating.


Conditional ZCML
----------------------------------------

In order to be backward compatible, you should use conditional zcml for any registrations or code that needs to be loaded. The collective docs has a `good section <http://collective-docs.plone.org/en/latest/zcml/tricks.html#id2>`_ on how to do this.

A simple example in practice is::

    <browser:page
      zcml:condition="installed plone.app.collection"
      name="myview"
      for="plone.app.collection.interfaces.ICollection"
      class=".views.MyView"
      permission="zope2.View"/>

Registering an interface for new collection
---------------------------------------------

    <class class="plone.app.collection.collection.Collection"
     zcml:condition="installed plone.app.collection">
     <implements interface=".interfaces.IMyInterface" />
    </class>

Retrieve the raw query
---------------------------------

    from plone.app.querystring import queryparser
    query = queryparser.parseFormquery(collectionobj, collectionobj.getRawQuery())


