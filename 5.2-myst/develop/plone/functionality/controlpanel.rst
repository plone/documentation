============================
Site setup and configuration
============================

.. admonition:: Description

    How to create settings for your add-on product and how to
    programmatically add new Plone control panel entries.


Introduction
============

This documentation tells you how to create new "configlets" to
Plone site setup control panel.

Configlets can be created in two ways:

* Using the ``plone.app.registry`` configuration framework for Plone
  (recommended);
* Using any :doc:`view code </develop/plone/views/browserviews>`.


``plone.app.registry``
======================

``plone.app.registry`` is the state of the art way to add settings for your
Plone 4.x+ add-ons.

For tutorial and more information please see the
`PyPi page <https://pypi.python.org/pypi/plone.app.registry>`_.

Example products:

* https://pypi.python.org/pypi/collective.gtags

* https://plone.org/products/collective.habla

* https://pypi.python.org/pypi/collective.xdv

Minimal example
---------------

Below is a minimal example for creating a configlet using ``plone.app.registry``.

It is based on the
`youraddon template <https://github.com/miohtama/sane_plone_addon_template/blob/master>`_.
The add-on package in this case is called
`silvuple <https://github.com/miohtama/silvuple>`_.

In ``buildout.cfg``, make sure you have the ``extends`` line for
Dexterity (see the
`Dexterity installation guide
<https://plone.org/products/dexterity/documentation/how-to/install>`_.

``setup.py``::

    install_requires = [..."plone.app.dexterity", "plone.app.registry"],

``configure.zcml``

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:plone="http://namespaces.plone.org/plone"
        i18n_domain="example.dexterityforms">

        ...

        <browser:page
            name="silvuple-settings"
            for="Products.CMFPlone.interfaces.IPloneSiteRoot"
            class=".settings.SettingsView"
            permission="cmf.ManagePortal"
            />

    </configure>


``settings.py``::

    """

        Define add-on settings.

    """

    from zope.interface import Interface
    from zope import schema
    from Products.CMFCore.interfaces import ISiteRoot
    from Products.Five.browser import BrowserView

    from plone.z3cform import layout
    from plone.directives import form
    from plone.app.registry.browser.controlpanel import RegistryEditForm
    from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

    class ISettings(form.Schema):
        """ Define settings data structure """

        adminLanguage = schema.TextLine(title=u"Admin language",
                description=u"Type two letter language code (admins always use this language)")

    class SettingsEditForm(RegistryEditForm):
        """
        Define form logic
        """
        schema = ISettings
        label = u"Silvuple settings"

    class SettingsView(BrowserView):
        """
        View which wrap the settings form using ControlPanelFormWrapper to a HTML boilerplate frame.
        """

        def render(self):
            view_factor = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
            view = view_factor(self.context, self.request)
            return view()

``profiles/default/controlpanel.xml``

.. code-block:: xml

    <?xml version="1.0"?>
    <object
        name="portal_controlpanel"
        xmlns:i18n="http://xml.zope.org/namespaces/i18n"
        i18n:domain="silvuple">

        <configlet
            title="Silvuple Settings"
            action_id="silvuple.settings"
            appId="silvuple"
            category="Products"
            condition_expr=""
            url_expr="string:${portal_url}/@@silvuple-settings"
            icon_expr=""
            visible="True"
            i18n:attributes="title">
                <permission>Manage portal</permission>
        </configlet>

    </object>

``profiles/default/registry.xml``

.. code-block:: xml

    <registry>
        <records interface="silvuple.settings.ISettings" prefix="silvuple">
            <!-- Set default values -->

            <!-- Leave to empty string -->
            <value key="adminLanguage"></value>
        </records>
    </registry>

Control panel widget settings
-----------------------------------

``plone.app.registry`` provides the ``RegistryEditForm``
class, which is a subclass of ``z3c.form.form.Form``.

It has two places to override which widgets
will be used for which field:

* ``updateFields()`` may set widget factories, i.e. widget type, to be used;

* ``updateWidgets()`` may play with widget properties and widget values
  shown to the user.

Example (``collective.gtags`` project, ``controlpanel.py``)::

    class TagSettingsEditForm(controlpanel.RegistryEditForm):

        schema = ITagSettings
        label = _(u"Tagging settings")
        description = _(u"Please enter details of available tags")

        def updateFields(self):
            super(TagSettingsEditForm, self).updateFields()
            self.fields['tags'].widgetFactory = TextLinesFieldWidget
            self.fields['unique_categories'].widgetFactory = TextLinesFieldWidget
            self.fields['required_categories'].widgetFactory = TextLinesFieldWidget

        def updateWidgets(self):
            super(TagSettingsEditForm, self).updateWidgets()
            self.widgets['tags'].rows = 8
            self.widgets['tags'].style = u'width: 30%;'

``plone.app.registry`` imports --- backwards compatibility
-----------------------------------------------------------

You need this if you started using ``plone.app.registry`` before April 2010.

There is a change concerning the 1.0b1 codebase::

    try:
        # plone.app.registry 1.0b1
        from plone.app.registry.browser.form import RegistryEditForm
        from plone.app.registry.browser.form import ControlPanelFormWrapper
    except ImportError:
        # plone.app.registry 1.0b2+
        from plone.app.registry.browser.controlpanel import RegistryEditForm
        from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper


Configlets without ``plone.registry``
============================================

Just add ``controlpanel.xml`` pointing to your custom form.


Content type choice setting
=====================================

Often you need to have a setting whether a certain functionality is enabled
on particular content types.

Here are the ingredients:

* A custom schema-defined interface for settings (``registry.xml`` schemas
  don't support multiple-choice widgets in ``plone.app.registry`` 1.0b2);

* a vocabulary factory to pull friendly type information out of ``portal_types`` .

``settings.py``::

    """

        Define add-on settings.

    """

    from zope import schema
    from five import grok
    from Products.CMFCore.interfaces import ISiteRoot
    from zope.schema.interfaces import IVocabularyFactory

    from z3c.form.browser.checkbox import CheckBoxFieldWidget


    from plone.z3cform import layout
    from plone.directives import form
    from plone.app.registry.browser.controlpanel import RegistryEditForm
    from plone.app.registry.browser.controlpanel import ControlPanelFormWrapper

    class ISettings(form.Schema):
        """ Define settings data structure """

        adminLanguage = schema.TextLine(title=u"Admin language", description=u"Type two letter language code and admins always use this language")

        form.widget(contentTypes=CheckBoxFieldWidget)
        contentTypes = schema.List(title=u"Enabled content types",
                                   description=u"Which content types appear on translation master page",
                                   required=False,
                                   value_type=schema.Choice(source="plone.app.vocabularies.ReallyUserFriendlyTypes"),
                                   )


    class SettingsEditForm(RegistryEditForm):
        """
        Define form logic
        """
        schema = ISettings
        label = u"Silvuple settings"

    class SettingsView(grok.CodeView):
        """

        """
        grok.name("silvuple-settings")
        grok.context(ISiteRoot)
        def render(self):
            view_factor = layout.wrap_form(SettingsEditForm, ControlPanelFormWrapper)
            view = view_factor(self.context, self.request)
            return view()

``profiles/default/registry.xml``:

.. code-block:: xml

    <registry>
        <records interface="silvuple.settings.ISettings" prefix="silvuple.settings.ISettings">
            <!-- Set default values -->


            <value key="contentTypes" purge="false">
                <element>Document</element>
                <element>News Item</element>
                <element>Folder</element>
            </value>
        </records>

    </registry>


Configuring Plone products from buildout
========================================

See a section in the `Buildout chapter <http://docs.plone.org/4/en/old-reference-manuals/buildout/additional.html#configuring-products-from-buildout>`_


Configuration using environment variables
=========================================

If your add-on requires "setting file"
for few simple settings you can change for each
buildout you can use operating system environment variables.

For example, see:

* https://pypi.python.org/pypi/Products.LongRequestLogger
