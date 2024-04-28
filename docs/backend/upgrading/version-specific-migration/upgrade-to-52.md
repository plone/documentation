---
myst:
  html_meta:
    "description": "Upgrading to Plone 5.1 to 5.2"
    "property=og:description": "Upgrading to Plone 5.1 to 5.2"
    "property=og:title": "Upgrading to Plone 5.1 to 5.2"
    "keywords": "Upgrading, Plone, 5.2, 5.1"
---


(upgrading-plone-5.1-to-5.2-label)=

# Upgrading Plone 5.1 to 5.2

This chapter provides instructions and tips for upgrading to Plone 5.2.


## General information

-   Before you upgrade read {doc}`../intro` and {doc}`../preparations`.
-   Always upgrade from the latest version of 5.1.x to the latest version of 5.2.x.
    This will resolve many migration-specific issues.
-   If you have problems, ask for help in the [Plone Community Forum](https://community.plone.org).


## Upgrading

This upgrade is unique because Plone 5.2 supports both Python 2 and Python 3.
The upgrade to 5.2 needs to be done in Python 2.7, and is not different from previous migrations.
To run the upgrade to 5.2, follow the links at the top of the control panel or visit the ZMI for your site at `/@@plone-upgrade`.

If you also want to upgrade from Python 2 to 3 with an existing database, you need to run an additional database migration while the site is not running.
See the section {ref}`python-3-support` below for details.


## Changes between Plone 5.1 and 5.2

The following PLIPs (Plone Improvement Proposals) have been implemented for 5.2.


(python-3-support)=

### Python 3 support

Plone 5.2 supports Python 3.6, 3.7, and 3.8, as well as Python 2.7.

This is [PLIP 2368](https://github.com/plone/Products.CMFPlone/issues/2368) and [PLIP 2890](https://github.com/plone/Products.CMFPlone/issues/2890).


#### For end users

Nothing changes.


#### For developers

All custom code and add-ons need to support Python 3.
Existing databases need to be upgraded as well.

The migration to Python 3 follows these steps:

1.  Upgrade add-ons and code to Plone 5.2 while running Python 2.7.
2.  Upgrade the Database to Plone 5.2 while running Python 2.7.
    To run that upgrade, follow the links at the top of the control panel or visit the ZMI for your site at `/@@plone-upgrade`.
3.  Drop any remaining Archetypes dependencies.
    Migrate these to Dexterity instead.
4.  Port add-ons and custom code to Python 3 without the existing database.
5.  Migrate the database using `zodbupdate`.
    If you are working on a new project without an existing database, you can skip this step.

See {doc}`upgrade-to-python3` for details about porting code and a database to Python 3.


### Zope 4.0

Plone runs on top of Zope 4.0 instead of Zope 2.13.x.

This is [PLIP 1351](https://github.com/plone/Products.CMFPlone/issues/1351).


#### For end users

This has no changes for Editors.
Admins will notice that the ZMI has a new Twitter Bootstrap-based theme, and some control panels have moved.


#### For developers

There are a lot of changes in Zope.
For details please see the following documents.

-   [What's new in Zope 4.0](https://zope.readthedocs.io/en/latest/news.html#what-s-new-in-zope-4)
-   [Changelog for alpha versions](https://github.com/zopefoundation/Zope/blob/4.0a6/CHANGES.rst)
-   [Changelog for beta versions](https://zope.readthedocs.io/en/latest/changes.html)

Many of the changes in Zope had effects on Plone that have been addressed.
For most add-ons, though, the changes have little to no effect.

Some tools from `CMFCore` are now utilities and can also be accessed as such.
Example:

```python
# old
from Products.CMFCore.utils import getToolByName
wf_tool = getToolByName(self.context, 'portal_workflow')

# new
from Products.CMFCore.interfaces import IWorkflowTool
from zope.component import getUtility
wf_tool = getUtility(IWorkflowTool)
```

The deprecated module `Globals` was removed.
Example:

```python
# old:
import Globals
develoment_mode = Globals.DevelopmentMode

# new
from App.config import getConfiguration
develoment_mode = getConfiguration().debug_mode
```

Functional tests using the `zope.testbrowser` now use `WebTest` instead of `mechanize`.
That means that tests that used internal methods of `mechanize` need to be updated.


### WSGI

This is a result of the PLIP for Python 3.
Plone 5.2 by default uses the WSGI-Server [waitress](https://docs.pylonsproject.org/projects/waitress/en/stable/).


#### For end users

Nothing changes.


#### For developers

By default, Plone uses `waitress` instead of `ZServer` as an HTTP server because `ZServer` will not be ported to Python 3.
Only when running on Python 2, you can still use `ZServer` by setting `wsgi = off` in the buildout part that configures the instance with `plone.recipe.zope2instance`.

Some options that used to configure `ZServer` are no longer available in `plone.recipe.zope2instance` when running on `WSGI`.
Check https://pypi.org/project/plone.recipe.zope2instance for details.


### plone.restapi

This is [PLIP 2177](https://github.com/plone/Products.CMFPlone/issues/2177).


#### For end users

Nothing changes.


#### For developers

You can now use a RESTful hypermedia API for Plone to build modern JavaScript frontends on top of Plone.
Also, the REST API can be used to import or export data.

See https://plonerestapi.readthedocs.io/en/latest/ for details.


### New navigation with dropdown

This is [PLIP 2516](https://github.com/plone/Products.CMFPlone/issues/2516).


#### For end users

Site Administrators can use the navigation control panel (`/@@navigation-controlpanel`) to configure the dropdown navigation.


#### For developers

For upgraded sites, the dropdown navigation is disabled by default.
For new sites, it is set to display 3 levels.

The code for the global navigation has moved to `plone.app.layout.navigation.navtree.NavTreeProvider`, and the template `plone.app.layout/plone/app/layout/viewlets/sections.pt` has changed.
Overrides of the previous navigation may no longer work and may need to be updated.

Developers who used add-ons or custom code for a dropdown navigation should consider migrating to the new navigation since it is extremely fast, accessible, and implemented almost entirely with CSS and HTML.


### Merge `Products.RedirectionTool` into core

This is [PLIP 1486](https://github.com/plone/Products.CMFPlone/issues/1486).


#### For end users

Site Administrators can use the {guilabel}`URL Management` control panel (`/@@redirection-controlpanel`) to manage and add alternative URLs, including bulk upload of alternative URLs.

As an Editor, you can see the {guilabel}`URL Management` link in the {guilabel}`actions` menu of a content item, and add or remove alternative URLs for this specific content item.


#### For developers

Since the add-on `Products.RedirectionTool` has been merged into Plone core, you should remove it.
You can either uninstall it before upgrading to Plone 5.2, or remove the product from the eggs and let the upgrade code from Plone remove it.
Any alternative URLs (aliases) that you have added manually will be kept.


### New Login

This is [PLIP 2092](https://github.com/plone/Products.CMFPlone/issues/2092).


#### For end users

Nothing changes.


#### For developers

Overrides of any templates or Python scripts that dealt with login or logout need to be changed.

The login has moved from a skin-based system to browser views.
You can use `z3c.jbot` to override templates, and use the component architecture to override the views.
The main code is now in `Products.CMFPlone.browser.login.login.LoginForm`.

You can customize the location to which a user will be redirected after login with an adapter.
Here is an example:

```python
from plone import api
from Products.CMFPlone.interfaces import IRedirectAfterLogin
from Products.CMFPlone.utils import safe_unicode
from zope.interface import implementer


@implementer(IRedirectAfterLogin)
class RedirectAfterLoginAdapter(object):

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self, came_from=None, is_initial_login=False):
        if 'Reviewer' in api.user.get_roles():
            api.portal.show_message(u'Get to work!', self.request)
            came_from = self.context.portal_url() + '/@@full_review_list'
        else:
            user = api.user.get_current()
            fullname = safe_unicode(user.getProperty('fullname'))
            api.portal.show_message(u'Nice to see you again, {0}!'.format(fullname), self.request)
        if not came_from:
            came_from = self.context.portal_url()
        return came_from
```

Then register the adapter through ZCML:

```xml
<adapter
    factory="your.addon.adapters.RedirectAfterLoginAdapter"
    for="OFS.interfaces.ITraversable
         zope.publisher.interfaces.IRequest"
/>
```

This adapter adapts context and request, thus you can modify these according to your needs.
You can also write similar adapters for `IInitialLogin` and `IForcePasswordChange`.


### Deprecate Archetypes

This is [PLIP 2390](https://github.com/plone/Products.CMFPlone/issues/2390).


#### For end users

Nothing changes.


#### For developers

In Plone 5.2 Archetypes is only available if you run Python 2.7 and if you add it to your dependencies.

You can add it by either adding `Products.ATContentTypes` to the list of your add-ons or by using the "extra" `archetypes` with the egg `Plone` in your buildout:

```ini
[instance]
recipe = plone.recipe.zope2instance
eggs =
    Plone[archetypes]
    your.addon
```

```{note}
Instead of using Archetypes in Plone 5.2, you should consider migrating to Dexterity.
Dexterity is also a hard requirement to be able to use Python 3.
See [`plone.app.contenttypes` documentation on Migration](https://github.com/plone/plone.app.contenttypes/blob/2.2.3/docs/README.rst#migration) for details on the migration from Archetypes to Dexterity.
```


### Remove support for old style resource registries

This is [PLIP 1742](https://github.com/plone/Products.CMFPlone/issues/1742).


#### For end users

Nothing changes.


#### For developers

Support for old-style resource registries (`cssregistry.xml` and `jsregistry.xml`) was removed completely, along with the tools `portal_css` or `portal_javascript`.

You need to add resources using the new Resource Registry.
See https://5.docs.plone.org/adapt-and-extend/theming/resourceregistry.html#resources for detailed instructions.


### Restructure `CMFPlone` static resources

This is [PLIP 1653](https://github.com/plone/Products.CMFPlone/issues/1653).


#### For end users

Nothing changes.


#### For developers

All JavaScript related code is now located in `plone.staticresources`.
