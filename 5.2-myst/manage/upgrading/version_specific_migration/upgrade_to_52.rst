==========================
Upgrading Plone 5.1 to 5.2
==========================


.. admonition:: Description

   Instructions and tips for upgrading to Plone 5.2.


General Information
===================

- Before you upgrade read :doc:`../intro` and :doc:`../preparations`.
- Always upgrade from the latest version of 5.1.x to the latest version of 5.2.x.
  This will resolve many migration-specific issues.
- If you have problems, do not be afraid to ask for help on `Plone Community <https://community.plone.org>`_.


Upgrading
=========

This upgrade is different from previous upgrades because Plone 5.2 supports Python 2 and Python 3.
The upgrade to 5.2 needs to be done in Python 2.7 and is not different that previous migrations.
To run the upgrade to 5.2, follow the links on top of the control panel or the ZMI to the form ``/@@plone-upgrade``.

If you also want to upgrade from Python 2 to 3 with a existing database, you need to run a additional database migration while the site is not running.
See the section :ref:`python-3-support` below for details about that.


Changes Between Plone 5.1 And 5.2
=================================

The following PLIPs (Plone Improvement Proposals) have been implemented for 5.2:


.. _python-3-support:

Python 3 Support
----------------

Plone 5.2 supports Python 3.6 and 3.7 as well as Python 2.7.

This is `PLIP 2368 <https://github.com/plone/Products.CMFPlone/issues/2368>`_.

For End Users
~~~~~~~~~~~~~

Nothing changes.

For Developers
~~~~~~~~~~~~~~

All custom code and add-ons need to support Python 3.
Existing databases need to be upgraded as well.

The migration to Python 3 follows these steps:

#. Upgrade add-ons and code to Plone 5.2 while running Python 2.7.
#. Upgrade the Database to Plone 5.2 while running Python 2.7. To run that upgrade follow the links on top of the control panel or the ZMI to the form `/@@plone-upgrade`
#. Drop any remaining Archetypes-dependencies. Migrate these to Dexterity instead.
#. Port add-ons and custom code to Python 3 without the existing database.
#. Migrate the database using ``zodbupdate``. If you are working on a new project (i.e. without a existing database) you can skip the last step.

See :doc:`/manage/version-specific-migration/upgrade_to_python3` for details about porting code and database to Python 3.


Zope 4.0
--------

Plone runs on top of Zope 4.0 instead of Zope 2.13.x.

This is `PLIP 1351 <https://github.com/plone/Products.CMFPlone/issues/1351>`_.

For End Users
~~~~~~~~~~~~~

This has no changes for Editors. Admins will notice that the ZMI has a new bootstrap-based theme and some control panels have moved.

For Developers
~~~~~~~~~~~~~~

There are a lot of changes in Zope. For details please see:

* `What’s new in Zope 4.0 <https://zope.readthedocs.io/en/latest/zope4/news.html>`_
* `Changelog for alpha-versions <https://github.com/zopefoundation/Zope/blob/4.0a6/CHANGES.rst>`_
* `Changelog for beta-versions <https://zope.readthedocs.io/en/latest/changes.html>`_

Many of the changes in Zope had effects on Plone that had been addressed. For most add-ons though the changes have little to no effect.

Some tools from CMFCore are now utilities and can also be accessed as such. Example:

.. code-block:: python

    # old
    from Products.CMFCore.utils import getToolByName
    wf_tool = getToolByName(self.context, 'portal_workflow')

    # new
    from Products.CMFCore.interfaces import IWorkflowTool
    from zope.component import getUtility
    wf_tool = getUtility(IWorkflowTool)


The deprecated module ``Globals`` was removed. Example:

.. code-block:: python

    # old:
    import Globals
    develoment_mode = Globals.DevelopmentMode

    # new
    from App.config import getConfiguration
    develoment_mode = getConfiguration().debug_mode

Functional tests using the zope.testbrowser now use ``WebTest`` instead of ``mechanize``. That means that tests that used interal methods of mechanize need to be updated.


WSGI
----

This is a result of the PLIP for Python 3.
Plone 5.2 by default uses the WSGI-Server `waitress <https://docs.pylonsproject.org/projects/waitress/en/stable/>`_.

For End Users
~~~~~~~~~~~~~

Nothing changes.

For Developers
~~~~~~~~~~~~~~

By default Plone uses ``waitress`` instead of ``ZServer`` as a HTTP-server since ``ZServer`` will not ported to Python 3.
Only when running on Python 2 you can still decide to use ``ZServer`` by setting ``wsgi = off`` in the buildout-part that configures the instance with ``plone.recipe.zope2instance``.

Some options that used to configure ``ZServer`` are no longer available in ``plone.recipe.zope2instance`` when running on ``WSGI``.
Check https://pypi.org/project/plone.recipe.zope2instance for details.


plone.restapi
-------------

This is `PLIP 2177 <https://github.com/plone/Products.CMFPlone/issues/2177>`_.

For End Users
~~~~~~~~~~~~~

Nothing changes.

For Developers
~~~~~~~~~~~~~~

You can now use a RESTful hypermedia API for Plone to build modern JavaScript front-ends on top of Plone.
Also, the REST-api can be used to import or export data.

See https://plonerestapi.readthedocs.io/en/latest/ for details.


New navigation with dropdown
----------------------------

This is `PLIP 2516 <https://github.com/plone/Products.CMFPlone/issues/2516>`_.


For End Users
~~~~~~~~~~~~~

Site-Administrators can use the navigation control panel (``/@@navigation-controlpanel``) to configure the dropdown-navigation.


For Developers
~~~~~~~~~~~~~~

For upgraded sites the dropdown-navigation is disabled by default, for new sites it is set to display 3 levels.

The code for the global navigation has moved to ``plone.app.layout.navigation.navtree.NavTreeProvider`` and the template ``plone.app.layout/plone/app/layout/viewlets/sections.pt`` has changed.
Overrides of the previous navigation may no longer work and need to be updated.

Developers who used add-ons or custom code for a dropdown-navigation should consider migrating to the new navigation since it is extremely fast, accessible and implemented almost entirely with css and html.


Merge Products.RedirectionTool into core
----------------------------------------

This is `PLIP 1486 <https://github.com/plone/Products.CMFPlone/issues/1486>`_.

For End Users
~~~~~~~~~~~~~

Site-Administrators can use the :guilabel:`URL Management` control panel (``/@@redirection-controlpanel``) to manage and add alternative URLs including bulk upload of alternative urls.

As an Editor, you can see the :guilabel:`URL Management` link in the :guilabel:`actions` menu of a content item, and add or remove alternative URLs for this specific content item.


For Developers
~~~~~~~~~~~~~~

Since the add-on ``Products.RedirectionTool`` has been merged into Plone, you should remove it.
You can either uninstall it before upgrading to Plone 5.2, or remove the product from the eggs and let the upgrade code from Plone remove it.
Any alternative URLs (aliases) that you have added manually will be kept.


New Login
---------

This is `PLIP 2092 <https://github.com/plone/Products.CMFPlone/issues/2092>`_.


For End Users
~~~~~~~~~~~~~

Nothing changes.


For Developers
~~~~~~~~~~~~~~

Overrides of any templates or Python scripts that dealt with login or logout need to be changed.

The login has moved from skin-based system to browser views.
You can use ``z3c.jbot`` to override templates and use the component architecture to override the views.
The main code is now in ``Products.CMFPlone.browser.login.login.LoginForm``.

You can customize the location to which a user will be redirected after login with an adapter.
Here is an example:

.. code-block:: python

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

Then register the adapter through ZCML:

.. code-block:: xml

    <adapter
        factory="your.addon.adapters.RedirectAfterLoginAdapter"
        for="OFS.interfaces.ITraversable
             zope.publisher.interfaces.IRequest"
    />

This adapter adapts context and request, thus you can modify these according to your needs.
You can also write similar adapters for ``IInitialLogin`` and ``IForcePasswordChange``.


Deprecate Archetypes
--------------------

This is `PLIP 2390 <https://github.com/plone/Products.CMFPlone/issues/2390>`_.


For End Users
~~~~~~~~~~~~~

Nothing changes.

For Developers
~~~~~~~~~~~~~~

In Plone 5.2 Archetypes is only available if you run Python 2.7 and if you add it to your dependencies.

You can add it by either adding ``Products.ATContentTypes`` to the list of your add-ons or by using the "extra" ``archetypes`` with the egg ``Plone`` in your buildout:

.. code-block:: ini

    [instance]
    recipe = plone.recipe.zope2instance
    eggs =
        Plone[archetypes]
        your.addon

.. note::

    Instead of using Archetypes in Plone 5.2, you should consider migrating to Dexterity.
    Dexterity is also a hard requirement to be able to use Python 3.
    See `plone.app.contenttypes documentation on Migration <https://github.com/plone/plone.app.contenttypes#migration>`_ for details on the migration from Archetypes to Dexterity.


Remove support for old style resource registries
------------------------------------------------

This is `PLIP 1742 <https://github.com/plone/Products.CMFPlone/issues/1742>`_.


For End Users
~~~~~~~~~~~~~

Nothing changes.

For Developers
~~~~~~~~~~~~~~

Support for old-style resource registries (``cssregistry.xml`` and ``jsregistry.xml``) was removed completely along with the tools ``portal_css`` or ``portal_javascript``.

You need to add resources using the new Resource Registry.
See :ref:`resources <resource_registry_resources>` for detailed instructions.


Restructure CMFPlone static resources
-------------------------------------

This is `PLIP 1653 <https://github.com/plone/Products.CMFPlone/issues/1653>`_.


For End Users
~~~~~~~~~~~~~

Nothing changes.

For Developers
~~~~~~~~~~~~~~

All JavaScript related code is now located in ``plone.staticresources``.
