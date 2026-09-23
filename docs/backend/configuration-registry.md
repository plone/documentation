---
myst:
  html_meta:
    "description": "The Configuration Registry in Plone provides a central system for storing and managing site-wide settings using plone.registry and plone.app.registry."
    "property=og:description": "The Configuration Registry in Plone provides a central system for storing and managing site-wide settings using plone.registry and plone.app.registry."
    "property=og:title": "Configuration Registry"
    "keywords": "Plone 6, Configuration Registry, plone.registry, plone.app.registry, GenericSetup, settings, control panel"
---

(backend-configuration-registry-label)=

# Configuration Registry

The Configuration Registry in Plone is a central system for storing and managing site-wide settings and configuration options.
It allows developers and administrators to define, store, and retrieve configuration data in a structured way.

If you have the Manager role, you can directly view and change many variables that influence Plone through the {guilabel}`Configuration Registry` control panel in {guilabel}`Site Setup`.
Because there is a large number of settings, you can filter them or select a prefix to find the right one.
Add-on packages can create their own prefixes for their settings.

```{warning}
Setting variables directly in the Configuration Registry is not recommended as part of regular maintenance.
It is a useful tool for inspecting variables for expert users.
```

The Configuration Registry is built on two main packages:

[`plone.registry`](https://pypi.org/project/plone.registry/)
:   The core package that provides the low-level registry implementation for storing settings.

[`plone.app.registry`](https://pypi.org/project/plone.app.registry/)
:   The Plone integration layer that provides control panel support, GenericSetup integration, and user interface components.


(backend-configuration-registry-plone-registry-label)=

## `plone.registry`

The `plone.registry` package provides a debatably simple, persistent (ZODB-based) system for managing configuration settings.
It uses `zope.schema` fields to define the types and constraints for settings.

### Key concepts

Registry
:   The main storage container for all settings.
    In Plone, you access it as a utility: `from plone.registry import getUtility; registry = getUtility(IRegistry)`.

Records
:   Individual settings stored in the registry.
    Each record has a name (a dotted name string), a field (a `zope.schema` field), and a value.

Interfaces
:   You can register a `zope.interface` Interface with the registry.
    The registry will then contain one record for each field in the interface.


### Accessing registry values

You can access registry values programmatically in several ways.

#### Direct access by record name

```python
from plone.registry.interfaces import IRegistry
from zope.component import getUtility

registry = getUtility(IRegistry)

# Get a value directly
value = registry["my.package.setting"]

# Set a value
registry["my.package.setting"] = "new value"
```

#### Access through an interface

When you register an interface with the registry, you can use `registry.forInterface()` to get a proxy object that provides attribute access to the settings.

```python
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from my.package.interfaces import IMySettings

registry = getUtility(IRegistry)
settings = registry.forInterface(IMySettings)

# Access settings as attributes
value = settings.my_setting
settings.my_setting = "new value"
```


(backend-configuration-registry-plone-app-registry-label)=

## `plone.app.registry`

The `plone.app.registry` package integrates `plone.registry` with Plone.
It provides:

-   GenericSetup import and export handlers for registry settings
-   A control panel base class for creating settings forms
-   The {guilabel}`Configuration Registry` control panel for viewing and editing settings
-   Browser views for managing the registry


### Creating settings for your add-on

To create settings for your add-on, you need to:

1.  Define a schema interface for your settings
2.  Register the interface with the registry using GenericSetup
3.  Optionally create a control panel to edit the settings


#### Define a settings interface

Create an interface that defines your settings using `zope.schema` fields.

```python
# In your package's interfaces.py
from zope import schema
from zope.interface import Interface


class IMyPackageSettings(Interface):
    """Settings for my package."""

    enable_feature = schema.Bool(
        title="Enable feature",
        description="Turn this feature on or off",
        default=True,
    )

    max_items = schema.Int(
        title="Maximum items",
        description="The maximum number of items to display",
        default=10,
        min=1,
        max=100,
    )

    admin_email = schema.TextLine(
        title="Admin email",
        description="Email address for notifications",
        required=False,
    )
```


#### Register settings with GenericSetup

Create a `registry.xml` file in your package's `profiles/default` directory.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<registry>
    <records interface="my.package.interfaces.IMyPackageSettings"
             prefix="my.package">
        <!-- Set default values (optional) -->
        <value key="enable_feature">True</value>
        <value key="max_items">10</value>
        <value key="admin_email"></value>
    </records>
</registry>
```

The `prefix` attribute determines the dotted name prefix for the records.
With `prefix="my.package"`, the `enable_feature` field becomes `my.package.enable_feature` in the registry.


#### Access settings in your code

```python
from plone.registry.interfaces import IRegistry
from zope.component import getUtility
from my.package.interfaces import IMyPackageSettings


def get_settings():
    registry = getUtility(IRegistry)
    return registry.forInterface(IMyPackageSettings)


def is_feature_enabled():
    settings = get_settings()
    return settings.enable_feature
```


## GenericSetup integration

GenericSetup is an XML-based framework for importing and exporting Plone site configurations.
The Configuration Registry integrates with GenericSetup through the `registry.xml` import and export step.


### The `registry.xml` file

The `registry.xml` file in a GenericSetup profile allows you to:

-   Register interfaces and their fields as registry records
-   Set values for existing records
-   Create individual records without an interface


#### Register an interface

```xml
<?xml version="1.0" encoding="UTF-8"?>
<registry>
    <records interface="my.package.interfaces.IMySettings"
             prefix="my.package.settings">
        <value key="some_setting">default value</value>
    </records>
</registry>
```


#### Create individual records

You can create records without defining an interface first.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<registry>
    <record name="my.package.simple_setting">
        <field type="plone.registry.field.TextLine">
            <title>Simple Setting</title>
            <description>A simple text setting</description>
        </field>
        <value>default value</value>
    </record>
</registry>
```


#### Modify existing records

To modify a record that already exists, reference it by name.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<registry>
    <record name="plone.site_title">
        <value>My New Site Title</value>
    </record>
</registry>
```


### The `purge` attribute

The `purge` attribute controls whether existing values are cleared before importing new ones.
This is especially important for list fields.

```xml
<!-- Replace all existing values -->
<value key="enabled_types" purge="true">
    <element>Document</element>
</value>

<!-- Add to existing values -->
<value key="enabled_types" purge="false">
    <element>News Item</element>
</value>
```

By default, `purge` is `true`, which means existing values are replaced.
Set `purge="false"` to add to existing list values instead of replacing them.


### The `remove` attribute

You can remove records or values using the `remove` attribute.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<registry>
    <!-- Remove a record entirely -->
    <record name="my.package.old_setting" remove="true" />

    <!-- Remove a value from a list -->
    <records interface="my.package.interfaces.IMySettings">
        <value key="enabled_types">
            <element remove="true">OldType</element>
        </value>
    </records>
</registry>
```


### Exporting registry settings

You can export the current registry configuration using the {guilabel}`Management Interface`.

1.  Navigate to the {guilabel}`Management Interface` (add `/manage_main` to your site URL).
2.  Go to `portal_setup`.
3.  Click the {guilabel}`Export` tab.
4.  Select {guilabel}`Configuration Registry` from the list of export steps.
5.  Click {guilabel}`Export selected steps`.

This generates a `registry.xml` file with all current settings that you can use in your GenericSetup profile.


### Uninstall profile

When creating an uninstall profile for your add-on, you should clean up any registry records you created.

In `profiles/uninstall/registry.xml`:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<registry>
    <records interface="my.package.interfaces.IMySettings"
             prefix="my.package"
             remove="true" />
</registry>
```


(backend-configuration-registry-field-types-label)=

## Available field types

The registry supports various field types from `plone.registry.field` and `zope.schema`.

| Field Type | Description |
|------------|-------------|
| `Bool` | Boolean (true/false) value |
| `Int` | Integer value |
| `Float` | Floating-point number |
| `TextLine` | Single line of text |
| `Text` | Multi-line text |
| `ASCIILine` | Single line of ASCII text |
| `ASCII` | Multi-line ASCII text |
| `Bytes` | Binary data |
| `BytesLine` | Single line of binary data |
| `Choice` | Selection from a vocabulary |
| `List` | List of values |
| `Tuple` | Tuple of values |
| `Set` | Set of unique values |
| `FrozenSet` | Immutable set of unique values |
| `Dict` | Dictionary of key-value pairs |
| `Date` | Date value |
| `Datetime` | Date and time value |
| `Time` | Time value |
| `Timedelta` | Time duration |
| `URI` | URI/URL value |
| `SourceText` | Source code text |
| `Object` | Nested object with its own schema |

When defining fields in XML, use the full dotted name for the field type.

```xml
<record name="my.package.setting">
    <field type="plone.registry.field.Int">
        <title>My Integer Setting</title>
        <min>0</min>
        <max>100</max>
    </field>
    <value>50</value>
</record>
```


(backend-configuration-registry-best-practices-label)=

## Best practices

### Use meaningful prefixes

Always use a meaningful prefix for your registry records, typically your package name.
This prevents conflicts with other packages and makes it easy to identify which package owns a setting.

```python
# Good
prefix = "my.package"

# Bad
prefix = "settings"
```


### Provide default values

Always provide sensible default values for your settings in `registry.xml`.
This ensures your add-on works correctly immediately after installation.


### Use interfaces for related settings

Group related settings into an interface rather than creating individual records.
This makes the settings easier to manage and access programmatically.


### Document your settings

Add clear titles and descriptions to your schema fields.
These appear in the control panel and help administrators understand what each setting does.

```python
class IMySettings(Interface):
    """Settings for my package."""

    cache_timeout = schema.Int(
        title="Cache timeout",
        description="How long (in seconds) to cache results. Set to 0 to disable caching.",
        default=300,
        min=0,
    )
```


### Handle missing settings gracefully

When accessing registry settings, handle the case where the setting might not exist, especially during upgrades.

```python
from plone.registry.interfaces import IRegistry
from zope.component import getUtility


def get_setting_safely():
    registry = getUtility(IRegistry)
    try:
        return registry["my.package.new_setting"]
    except KeyError:
        return "default_value"
```


## Related content

-   [`plone.registry` on PyPI](https://pypi.org/project/plone.registry/)
-   [`plone.app.registry` on PyPI](https://pypi.org/project/plone.app.registry/)