====================================
Upgrade a custom add-on to Plone 5.1
====================================


Installation code
=================

See `PLIP 1340 <https://github.com/plone/Products.CMFPlone/issues/1340>`_ for a discussion of this change.


From CMFQuickInstallerTool to GenericSetup
------------------------------------------

The add-ons control panel in Plone 5.1 no longer supports installation or uninstallation code in ``Extensions/install.py`` or  ``Extensions/Install.py``.
If you have such code, you must switch to a GenericSetup profile.

GenericSetup is already the preferred way of writing installation code since Plone 3.
If you must use the old way, you can still use the ``portal_quickinstaller`` in the Management Interface.

In a lot of cases, you can configure ``xml`` files instead of using Python code.
In other cases you may need to write custom installer code (setuphandlers.py).
See the :doc:`GenericSetup documentation </develop/addons/components/genericsetup>`.


default profile
---------------

Historically, when your add-on had multiple profiles, their names would be sorted alphabetically and the first one would be taken as the installation profile.
It was always recommended to use ``default`` as name of this first profile.

Since Plone 5.1, when there is a ``default`` profile, it is always used as the installation profile, regardless of other profile names.
Exception: when this ``default`` profile is marked in an ``INonInstallable`` utility, it is ignored and Plone falls back to using the first from the alphabetical sorting.


Uninstall
---------

An uninstall profile is not required, but it is highly recommended.

Until Plone 5.0 the CMFQuickInstallerTool used to do an automatic partial cleanup,
for example removing added skins and css resources.
This was always only partial, so you could not rely on it to fully cleanup the site.

Since Plone 5.1 this cleanup is no longer done.
Best practice is to create an uninstall profile for all your packages.

If you were relying on this automatic cleanup, you need to add extra files to clean it up yourself.
You need to do that when your default profile contains one of these files:

- ``actions.xml``
- ``componentregistry.xml``
- ``contenttyperegistry.xml``.
  This seems rarely used.
  Note: the `contenttyperegistry import step <https://github.com/zopefoundation/Products.CMFCore/blob/2.2.10/Products/CMFCore/exportimport/contenttyperegistry.py#L73>`_ only supports adding, not removing.
  You may need to improve that code based on the old `CMFQuickInstallerTool code <https://github.com/plone/Products.CMFQuickInstallerTool/blob/3.0.13/Products/CMFQuickInstallerTool/InstalledProduct.py#L364>`_.
- ``cssregistry.xml``
- ``jsregistry.xml``
- ``skins.xml``
- ``toolset.xml``
- ``types.xml``
- ``workflows.xml``

When there is no uninstall profile, the add-ons control panel will give a warning.
An uninstall profile is a profile that is registered with the name ``uninstall``.
For an example, see https://github.com/plone/plone.app.multilingual/tree/master/src/plone/app/multilingual/profiles/uninstall


Don't use portal_quickinstaller
-------------------------------

Old code:

.. code-block:: python

    qi = getToolByName(self.context, name='portal_quickinstaller')

or:

.. code-block:: python

    qi = self.context.portal_quickinstaller

or:

.. code-block:: python

    qi = getattr(self.context, 'portal_quickinstaller')

or:

.. code-block:: python

    qi = getUtility(IQuickInstallerTool)

New code:

.. code-block:: python

    from Products.CMFPlone.utils import get_installer
    qi = get_installer(self.context, self.request)

or if you do not have a request:

.. code-block:: python

    qi = get_installer(self.context)

Alternatively, since it is a browser view, you can get it like this:

.. code-block:: python

    qi = getMultiAdapter((self.context, self.request), name='installer')

or with ``plone.api``:

.. code-block:: python

    from plone import api
    api.content.get_view(
        name='installer',
        context=self.context,
        request=self.request)

If you need it in a page template:

.. code-block:: python

   tal:define="qi context/@@installer"

.. warning::

   Since the code really does different things than before, the method names were changed and they may accept less arguments or differently named arguments.


Products namespace
------------------

There used to be special handling for the Products namespace.
Not anymore.

Old code:

.. code-block:: python

    qi.installProduct('CMFPlacefulWorkflow')

New code:

.. code-block:: python

    qi.install_product('Products.CMFPlacefulWorkflow')


isProductInstalled
------------------

Old code:

.. code-block:: python

    qi.isProductInstalled(product_name)

New code:

.. code-block:: python

    qi.is_product_installed(product_name)


installProduct
--------------

Old code:

.. code-block:: python

    qi.installProduct(product_name)

New code:

.. code-block:: python

    qi.install_product(product_name)

Note that no keyword arguments are accepted.


installProducts
---------------

This was removed.
You should iterate over a list of products instead.

Old code:

.. code-block:: python

    product_list = ['package.one', 'package.two']
    qi.installProducts(product_list)

New code:

.. code-block:: python

    product_list = ['package.one', 'package.two']
    for product_name in product_list:
       qi.install_product(product_name)


uninstallProducts
-----------------

Old code:

.. code-block:: python

    qi.uninstallProducts([product_name])

New code:

.. code-block:: python

    qi.uninstall_product(product_name)

Note that we only support passing one product name.
If you want to uninstall multiple products, you must call this method multiple times.


reinstallProducts
-----------------

This was removed.
Reinstalling is usually not a good idea: you should use an upgrade step instead.
If you need to, you can uninstall and install if you want.


getLatestUpgradeStep
--------------------

Old code:

.. code-block:: python

    qi.getLatestUpgradeStep(profile_id)

New code:

.. code-block:: python

    qi.get_latest_upgrade_step(profile_id)


upgradeProduct
--------------

Old code:

.. code-block:: python

    qi.upgradeProduct(product_id)

New code:

.. code-block:: python

    qi.upgrade_product(product_id)


isDevelopmentMode
-----------------

This was a helper method that had got nothing to with the quick installer.

Old code:

.. code-block:: python

    qi = getToolByName(aq_inner(self.context), 'portal_quickinstaller')
    return qi.isDevelopmentMode()

New code:

.. code-block:: python

    from Globals import DevelopmentMode
    return bool(DevelopmentMode)

.. note::

   The new code works already since Plone 4.3.


All deprecated methods
----------------------

Some of these were mentioned already.

Some methods are no longer supported.
These methods are still there, but they do nothing:

- ``listInstallableProducts``

- ``listInstalledProducts``

- ``getProductFile``

- ``getProductReadme``

- ``notifyInstalled``

- ``reinstallProducts``

Some methods have been renamed.
The old method names are kept for backwards compatibility.
They do roughly the same as before, but there are differences.
And all keyword arguments are ignored.
You should switch to the new methods instead:

- ``isProductInstalled``, use ``is_product_installed`` instead

- ``isProductInstallable``, use ``is_product_installable`` instead

- ``isProductAvailable``, use ``is_product_installable`` instead

- ``getProductVersion``, use ``get_product_version`` instead

- ``upgradeProduct``, use ``upgrade_product`` instead

- ``installProducts``, use ``install_product`` with a single product instead

- ``installProduct``, use ``install_product`` instead

- ``uninstallProducts``, use ``uninstall_product`` with a single product instead.


INonInstallable
---------------

There used to be one ``INonInstallable`` interface in ``CMFPlone`` (for hiding profiles) and another one in ``CMFQuickInstallerTool`` (for hiding products).
In the new situation, these are combined in the one from CMFPlone.

Sample usage:

In configure.zcml:

.. code-block:: xml

    <utility factory=".setuphandlers.NonInstallable"
        name="your.package" />

In setuphandlers.py:

.. code-block:: python

    from Products.CMFPlone.interfaces import INonInstallable
    from zope.interface import implementer

    @implementer(INonInstallable)
    class NonInstallable(object):

        def getNonInstallableProducts(self):
            # (This used to be in CMFQuickInstallerTool.)
            # Make sure this package does not show up in the add-ons
            # control panel:
            return ['collective.hidden.package']

        def getNonInstallableProfiles(self):
            # (This was already in CMFPlone.)
            # Hide the base profile from your.package from the list
            # shown at site creation.
            return ['your.package:base']

When you do not need them both, you can let the other return an empty list, or you can leave that method out completely.

.. note::

    If you need to support older Plone versions at the same time, you can let your class implement the old interface as well:

    .. code-block:: python

        from Products.CMFQuickInstallerTool.interfaces import (
            INonInstallable as INonInstallableProducts)

        @implementer(INonInstallableProducts)
        @implementer(INonInstallable)
        class NonInstallable(object):
            ...


Retina image scales
===================

In the Image Handling Settings control panel in Site Setup, you can configure Retina mode for extra sharp images.
When you enable this, it will result in image tags like this, for improved viewing on Retina screens:

.. code-block:: html

    <img src="....jpeg" alt="alt text" title="some title" class="image-tile"
         srcset="...jpeg 2x, ...jpeg 3x" height="64" width="48">

To benefit from this new feature, you must use the ``tag`` method of image scales:

.. code-block:: html

    <img tal:define="images obj/@@images"
         tal:replace="structure python:images.scale('image', scale='tile').tag(css_class='image-tile')">

If you are iterating over a list of image brains, you should use the new ``@@image_scale`` view of the portal or the navigation root.
This will cache the result in memory, which avoids waking up the objects the next time.

.. code-block:: html

    <tal:block define="image_scale portal/@@image_scale">
        <tal:results tal:repeat="brain batch">
            <img tal:replace="structure python:image_scale.tag(item, 'image', scale='tile', css_class='image-tile')">
        </tal:results>
    </tal:block>
