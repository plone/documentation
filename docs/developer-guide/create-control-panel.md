---
myst:
  html_meta:
    "description": "How to create a control panel in Plone for Classic UI and Volto"
    "property=og:description": "How to create a control panel in Plone for Classic UI and Volto"
    "property=og:title": "Create a control panel in Plone for Classic UI and Volto"
    "keywords": "Plone, create, control panel, plonecli, registry, Classic UI, Volto, frontend, backend"
---

(backend-controlpanels-label)=

# Create a control panel

This chapter describes how to create a control panel for your Plone add-on, whether accessed through either the Classic UI or Volto frontend.

It also covers advanced topics—including how to group fields in your control panel—and provides a schema field reference, troubleshooting tips, control panel file structure, and a Plone REST API compatibility reference.


## Creation approaches

There are two approaches to create a control panel for your Plone add-on:

-   [`plonecli`](https://pypi.org/project/plonecli/)
-   manual


## `plonecli`

To add a control panel to your add-on, you can use [`plonecli`](https://pypi.org/project/plonecli/) as follows.

```shell
plonecli add controlpanel
```

This creates the control panel Python file in the control panel's folder where you can define your control panel schema fields.


## Manual

To manually create a control panel, go through the following steps.

-   Define the settings interface and form.
-   Register the control panel view in ZCML.
-   Add the control panel to the Plone control panel listing.
-   Set default values in the registry.

### Define the settings interface and form

Create a Python module, {file}`mypackage/controlpanel/settings.py`, that defines your control panel's settings interface and form class as follows.

```python
# mypackage/controlpanel/settings.py
from zope import schema
from zope.interface import Interface
from plone.app.registry.browser.controlpanel import RegistryEditForm, ControlPanelFormWrapper
from plone.z3cform import layout

class IMyControlPanelSettings(Interface):
    """Schema for the control panel form."""
    
    my_setting = schema.TextLine(
        title=u'My Setting',
        description=u'Enter the value for my setting',
        required=False,
        default=u''
    )
    
    my_choice = schema.Choice(
        title=u'My Choice',
        description=u'Select a value for my choice',
        required=False,
        default=u'value3',
        values=['value1', 'value2', 'value3']
    )

class MyControlPanelForm(RegistryEditForm):
    """Control panel form."""
    
    schema = IMyControlPanelSettings
    schema_prefix = "my.addon"
    label = u"My Addon Settings"

# Wrap the form with plone.z3cform's ControlPanelFormWrapper to get the Plone
# control panel look and feel
MyControlPanelView = layout.wrap_form(MyControlPanelForm, ControlPanelFormWrapper)
```


### Register the control panel view

Create a file {file}`mypackage/controlpanel/configure.zcml` with the following content to register the control panel view in ZCML.

```xml
<!-- mypackage/controlpanel/configure.zcml -->
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    i18n_domain="mypackage">

    <browser:page
        name="my-controlpanel"
        for="Products.CMFPlone.interfaces.IPloneSiteRoot"
        class=".settings.MyControlPanelView"
        permission="cmf.ManagePortal"
        />

</configure>
```

Make sure to include the above file in your package's main {file}`mypackage/configure.zcml` as shown by the highlighted line below.

{emphasize-lines="9"}
```xml
<!-- mypackage/configure.zcml -->
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:i18n="http://namespaces.zope.org/i18n"
    i18n_domain="mypackage">
    
    <!-- Other configuration -->
    
    <include package=".controlpanel" />
    
</configure>
```

### Add the control panel entry

Create a {file}`mypackage/profiles/default/controlpanel.xml` in your package's GenericSetup profile with the following content to add your control panel to the Plone control panel listing.

```xml
<!-- mypackage/profiles/default/controlpanel.xml -->
<?xml version="1.0"?>
<object name="portal_controlpanel">
    <configlet
        title="My Addon Settings"
        action_id="my-controlpanel"
        appId="my.addon"
        category="plone-general"
        condition_expr=""
        icon_expr="string:puzzle"
        url_expr="string:${portal_url}/@@my-controlpanel"
        visible="True">
        <permission>Manage portal</permission>
    </configlet>
</object>
```

The category attribute can be one of the following values.
These values correspond to the groups in {guilabel}`Site Setup`.

`plone-general`
:   {guilabel}`General`

`plone-content`
:   {guilabel}`Content`

`plone-users`
:   {guilabel}`Users`

`plone-security`
:   {guilabel}`Security`

`plone-advanced`
:   {guilabel}`Advanced`


### Set default values in the registry

Define default values for your settings in {file}`mypackage/profiles/default/registry.xml`.

```xml
<!-- mypackage/profiles/default/registry.xml -->
<?xml version="1.0"?>
<registry>
    <records interface="mypackage.controlpanel.settings.IMyControlPanelSettings"
             prefix="my.addon">
        <value key="my_setting">default value</value>
        <value key="my_choice">value3</value>
    </records>
</registry>
```


### Access your settings in code

You can access your settings in Python code as follows.

```python
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

registry = getUtility(IRegistry)
settings = registry.forInterface(IMyControlPanelSettings, prefix="my.addon")

# Now you can access the settings
my_setting_value = settings.my_setting
my_choice_value = settings.my_choice
```


### Register a control panel

To manually register a view as a control panel, add the following registration to your {file}`/profiles/default/controlpanel.xml`.

```xml
<?xml version="1.0"?>
  <object
      name="portal_control-panel"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      i18n:domain="lmu.behavior">
    <configlet
      title="Some Control Panel"
      action_id="collective.example.some_control-panel"
      appId="collective.example"
      category="Products"
      condition_expr=""
      url_expr="string:${portal_url}/@@some_view"
      icon_expr=""
      visible="True"
      i18n:attributes="title">
          <permission>Manage portal</permission>
    </configlet>
  </object>
```

Your control panel should now appear in {guilabel}`Site Setup`.


## Use `FieldSet` to group fields

For complex control panels, you can group fields together as in the following example.

```python
from plone.supermodel import model

class IMyControlPanelSettings(Interface):
    
    model.fieldset(
        'advanced',
        label=u"Advanced Settings",
        fields=['advanced_setting1', 'advanced_setting2']
    )
    
    # Basic settings
    my_setting = schema.TextLine(
        title=u'My Setting',
        description=u'Enter the value for my setting',
        required=False
    )
    
    # Advanced settings
    advanced_setting1 = schema.TextLine(
        title=u'Advanced Setting 1',
        required=False
    )
    
    advanced_setting2 = schema.Bool(
        title=u'Advanced Setting 2',
        default=False
    )
```


## Common schema fields

The following is a list of commonly used schema field types.

`schema.TextLine`
:   For single-line text

`schema.Text`
:   For multi-line text

`schema.Bool`
:   For boolean values

`schema.Int`
:   For integer values

`schema.Float`
:   For floating-point values

`schema.Choice`
:   For selection from a list of values

`schema.Datetime`
:   For date and time values

`schema.List`
:   For list of values


## Modify control panel fields

When you modify the fields in your control panel settings interface, the changes won't be automatically reflected in existing sites.
You'll need to perform one or more of the following steps.

-   Run the appropriate upgrade steps.
-   Reinstall your add-on.
-   Test with a fresh site installation.


## Troubleshooting

If your control panel doesn't appear or doesn't work as expected:

-   Verify that all ZCML is properly registered.
-   Check for errors in the Plone error log.
-   Ensure your GenericSetup profiles are correctly installed.
-   Validate that the interface path in {file}`registry.xml` matches your actual Python path.


## Example file structure

Below is a complete example file structure for a basic add-on with a control panel.

```
mypackage/
├── __init__.py
├── configure.zcml
├── controlpanel/
│   ├── __init__.py
│   ├── configure.zcml
│   └── settings.py
└── profiles/
    └── default/
        ├── controlpanel.xml
        ├── metadata.xml
        └── registry.xml
```

## REST API compatibility

For better integration between Plone's backend and its frontend Volto, you can create REST API compatible control panels using the adapter pattern.
This approach is particularly useful when developing control panels that need to work seamlessly with Volto.

Create a Python module {file}`mypackage/controlpanel.py` as follows.

```python
from plone.restapi.controlpanels import RegistryConfigletPanel
from zope.component import adapter
from zope.interface import Interface
from zope.i18nmessageid import MessageFactory

_ = MessageFactory("mypackage")

@adapter(Interface, Interface)
class MyAddonControlPanel(RegistryConfigletPanel):
    """Volto-compatible REST API control panel for my add-on settings."""

    schema = IMyControlPanelSettings
    schema_prefix = "my.addon"
    configlet_id = "my-controlpanel"
    configlet_category_id = "plone-general"
    title = _("My Addon Settings")
    group = "General"
```

Then register the adapter in your ZCML configuration file.

```xml
<!-- mypackage/configure.zcml or mypackage/controlpanel/configure.zcml -->
<configure
    xmlns="http://namespaces.zope.org/zope"
    i18n_domain="mypackage">

    <adapter
        factory=".controlpanel.MyAddonControlPanel"
        name="my-controlpanel"
    />

</configure>
```

The `group` property in the control panel class corresponds to the control panel category in Volto.

`General`
:   General settings (corresponds to `plone-general`)

`Content`
:   Content-related settings (corresponds to `plone-content`)

`Users`
:   Users and groups settings (corresponds to `plone-users`)

`Security`
:   Security settings (corresponds to `plone-security`)

`Advanced`
:   Advanced settings (corresponds to `plone-advanced`)

With this approach, your control panel will be automatically available through the REST API at the endpoint `@controlpanels/my-controlpanel`, making it easy to integrate with Volto without additional configuration.

You will still need to set up {file}`registry.xml` with default values as described earlier.

```{seealso}
See the chapter {ref}`training:controlpanel-label` from the Mastering Plone 6 Training.
```