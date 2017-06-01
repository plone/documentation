====================================
Upgrade a custom add-on to Plone 5.0
====================================

Archetypes
==========

If your add-on depends on Archetypes, you will need some parts of ``Products.ATContentTypes``.
Those parts will be declared by the profile "Archetypes-tools without content types". It must be added to your ``profiles/default/metadata.xml`` that way::

    <dependencies>
        <dependency>profile-Products.ATContentTypes:base</dependency>
        ...
    </dependencies>

JS/CSS bundle
=============

Plone 5 does not use ``portal_css`` and ``portal_javascript`` anymore.
The add-on resources will have to be provided into a bundle.

Add a file named ``registry.xml`` in your profile, containing:

.. code-block:: xml

    <?xml version="1.0"?>
    <registry>

      <records prefix="plone.bundles/ouraddon"
                interface='Products.CMFPlone.interfaces.IBundleRegistry'>
        <value key="enabled">True</value>
        <value key="jscompilation">++resource++mycustom.js</value>
        <value key="csscompilation">++resource++mycustom.css</value>

        <value key="last_compilation">2019-11-26 00:00:00</value>
        <value key="compile">False</value>
        <value key="depends">plone</value>
      </records>

    </registry>

.. note::

    This example assumes our JS and CSS are provided as browser resources, but if they are in our old ``skins`` folder, that would work too::

    <value key="csscompilation">portal_skins/MyAddon/mycustom.css</value>


CSRF protection
===============

Plone 5 provides a CSRF protection mechanism. This mechanism is integrated into the different Plone frameworks.
If your add-on only uses default Dexterity or Archetypes features, you are safe.

But any custom redirection or form submission will have to include a token provided by ``plone.protect``.

- in a template::

    <span tal:replace="structure context/@@authenticator/authenticator"/>

- in a script::

    authenticator = context.restrictedTraverse("@@authenticator")
    url = url + "?_authenticator="  + authenticator.token()
    state.set(..., next_action='redirect_to:string:%s' % url)

- in a method::

    from plone.protect.utils import addTokenToUrl
    url = addTokenToUrl(url)


plone.app.stagingbehavior
=========================

plone.app.stagingbehavior was used to enable versioning functionality for Dexterity-based content types.
It allowed you to perform the checkout and checkin operations to work on a copy of your original content on Plone 4.

The version of plone.app.iterate used in Plone 5 implements this already making that package obsolete

You should remove any hard dependency on plone.app.stagingbehavior from your add-on to avoid issues.

See https://github.com/collective/collective.cover/pull/577/files for an example on how to achieve that.

Content type icons
==================

A major breaking change from Plone 4.x to Plone 5 is how content type icons are handled.
See :ref:content-type-icons-changed` for details. 