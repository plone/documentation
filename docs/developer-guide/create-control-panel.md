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

This chapter describes how to create a control panel for Plone, either {ref}`automatically <create-a-control-panel-automated-method-label>` or {ref}`manually <create-a-control-panel-manual-method-label>`, whether accessed through the Classic UI or Volto frontend.
It continues with {ref}`common tasks and advanced topics <common-tasks-and-advanced-topics-label>`, including field grouping, schema reference, {ref}`troubleshooting <control-panel-troubleshooting-label>` tips, and {ref}`rest-api-compatibility-label`.


(create-a-control-panel-automated-method-label)=

## Automated method with `plonecli`

The automated method uses {term}`plonecli` and works only with backend add-ons.
It requires that you have already created a Plone backend add-on using one of the following methods.

-   {doc}`/install/create-project-cookieplone`
-   {doc}`create-backend-add-on`

From the root of your add-on, run the following command as described in {ref}`backend-add-on-subtemplates-label`.

```shell
plonecli add controlpanel
```

This creates Python modules in the folder {file}`src/collective/myaddon/controlpanel`, where you can define your control panel schema fields.

`plonecli` automatically performs all the manual steps described in the next approach.


(create-a-control-panel-manual-method-label)=

## Manual method

The manual method works for:

-   backend add-ons that were not created via `plonecli`
-   custom control panels created directly in a Plone site
-   any Plone project or installation

You'll need to complete the following steps, as described in the following sections.

1.  {ref}`define-the-settings-interface-and-form-label`.
1.  {ref}`register-the-control-panel-view-label`.
1.  {ref}`add-the-control-panel-entry-label`.
1.  {ref}`register-the-control-panel-label`.
1.  {ref}`set-default-values-in-the-registry-label`.

```{note}
The code examples below are for illustrative purposes and show the general structure.
Adapt the paths, names, and values to match your specific project or add-on.
```


(define-the-settings-interface-and-form-label)=

### Define the settings interface and form

Create a Python module, {file}`mypackage/controlpanel/settings.py`, that defines your control panel's settings interface and form class, or schema, as follows.

```python
# mypackage/controlpanel/settings.py
from zope import schema
from zope.interface import Interface
from plone.app.registry.browser.controlpanel import RegistryEditForm, ControlPanelFormWrapper
from plone.z3cform import layout

class IMyControlPanelSettings(Interface):
    """Schema for the control panel form."""
    
    my_setting = schema.TextLine(
        title="My Setting",
        description="Enter the value for my setting",
        required=False,
        default=""
    )
    
    my_choice = schema.Choice(
        title="My Choice",
        description="Select a value for my choice",
        required=False,
        default="value3",
        values=["value1", "value2", "value3"]
    )

class MyControlPanelForm(RegistryEditForm):
    """Control panel form."""
    
    schema = IMyControlPanelSettings
    schema_prefix = "my.addon"
    label = "My add-on settings"

# Wrap the form with plone.z3cform's ControlPanelFormWrapper to get the Plone
# control panel look and feel
MyControlPanelView = layout.wrap_form(MyControlPanelForm, ControlPanelFormWrapper)
```


(register-the-control-panel-view-label)=

### Register the control panel view

This step registers a view to display the control panel defined in the previous step.

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

Include the above file in your package's main {file}`mypackage/configure.zcml`, as shown by the highlighted line below.

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


(add-the-control-panel-entry-label)=

### Add the control panel entry

This step adds the control panel to the Plone control panel listing.

Create a {file}`mypackage/profiles/default/controlpanel.xml` in your package's GenericSetup profile with the following content to add your control panel to the Plone control panel listing.

```xml
<!-- mypackage/profiles/default/controlpanel.xml -->
<?xml version="1.0"?>
<object name="portal_controlpanel">
    <configlet
        title="My add-on settings"
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



(set-default-values-in-the-registry-label)=

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


(register-the-control-panel-label)=

### Register the control panel

To register the view as a control panel so that it appears in the {guilabel}`Site Setup`, add the following registration to your {file}`/profiles/default/controlpanel.xml`.

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


## Load your control panel

After performing the above steps, you must {ref}`import-the-generic-profile-label` and {ref}`restart-the-instance-label`, as they are important to load the profile, including the registry to the project.


(restart-the-instance-label)=

### Restart the instance

To stop a running Plone instance, press {kbd}`ctrl-c` in the terminal where Plone is running.
To start it again, use the appropriate command based on your installation method.

`````{tab-set}

````{tab-item} buildout
```shell
bin/instance fg
```
````

````{tab-item} pip
```shell
bin/runwsgi -v instance/etc/zope.ini
```
````

````{tab-item} Cookieplone
For a backend add-on only, use the following command.

```shell
make backend-start
```

For both a backend and frontend add-on project, open two separate terminal sessions.

In the first session, start the backend.

```shell
make backend-start
```

In the second session, start the frontent.

```shell
make frontend-start
```
````

`````


(import-the-generic-profile-label)=

### Import the generic profile

To apply your newly created control panel in a Plone project, you'll need to manually import the GenericSetup profile associated with your project.
Perform the following steps to do so.

1.  Navigate to your Plone site's URL and append `/manage` to access the {term}`Zope Management Interface` (ZMI).

    ```shell
    http://localhost:8080/Plone/manage
    ```

1.  Navigate to the {guilabel}`Setup Tool` by locating and clicking on {guilabel}`portal_setup`.
1.  Within {guilabel}`portal_setup`, go to the {guilabel}`Import` tab.
1.  From the {guilabel}`Profile` select menu, select your project's profile.
    This is typically named in the following format.

    ```text
    profile-your.projectname:default
    ```

1.  Click the {guilabel}`Import All Steps` button to apply the profile.

This process will register your control panel and any associated registry settings defined in your {file}`registry.xml` and {file}`controlpanel.xml` files.

Your control panel should now appear in {guilabel}`Site Setup`.


(common-tasks-and-advanced-topics-label)=

## Common tasks and advanced topics

The following sections apply to control panels created with either the automated or manual methods.


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


### Use `FieldSet` to group fields

For complex control panels, you can group fields together as in the following example.

```python
from plone.supermodel import model

class IMyControlPanelSettings(Interface):
    
    model.fieldset(
        "advanced",
        label="Advanced Settings",
        fields=["advanced_setting1", "advanced_setting2"]
    )
    
    # Basic settings
    my_setting = schema.TextLine(
        title="My Setting",
        description="Enter the value for my setting",
        required=False
    )
    
    # Advanced settings
    advanced_setting1 = schema.TextLine(
        title="Advanced Setting 1",
        required=False
    )
    
    advanced_setting2 = schema.Bool(
        title="Advanced Setting 2",
        default=False
    )
```


### Common schema fields

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


### Modify control panel fields

When you modify the fields in your control panel settings interface, the changes won't be automatically reflected in existing sites.
You'll need to perform one or more of the following steps.

-   Run the appropriate upgrade steps.
-   Reinstall your add-on.
-   Test with a fresh site installation.


(control-panel-troubleshooting-label)=

### Troubleshooting

If your control panel doesn't appear or doesn't work as expected, try the following troubleshooting tasks.

-   Verify that all ZCML is properly registered.
-   Check for errors in the Plone error log.
-   Ensure your GenericSetup profiles are correctly installed.
-   Validate that the interface path in {file}`registry.xml` matches your actual Python path.


### Example file structure

Below is a complete example file structure for a basic add-on with a control panel.

```text
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


(rest-api-compatibility-label)=

### REST API compatibility

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
    title = _("My add-on settings")
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

You'll still need to set up {file}`registry.xml` with default values as described earlier.

```{seealso}
See the chapter {ref}`training:controlpanel-label` from the Mastering Plone 6 Training.
```
