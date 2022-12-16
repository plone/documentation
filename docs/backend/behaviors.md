---
myst:
  html_meta:
    "description": "Behaviors are reusable bundles of functionality that can be enabled or disabled on a per-content type basis."
    "property=og:description": "Behaviors are reusable bundles of functionality that can be enabled or disabled on a per-content type basis."
    "property=og:title": "Behaviors"
    "keywords": "Behaviors"
---

(backend-behaviors-label)=

# Behaviors

## What are Behaviors in Plone

In Plone, behaviors are a way to add reusable functionality to content objects without modifying the objects themselves.
Behaviors are essentially small chunks of code that can be plugged onto content types to provide new features or capabilities.

A Plone behavior could be used to

- add a set of form fields (on standard add and edit forms),
- add logic as part of the adapter,
- enable a particular event handler,
- enable one or more views, viewlets, or other UI components,
- do anything else which may be expressed in code via an adapter and/or marker interface.

Behaviors can be added to content types on an as-needed basis, allowing for a high degree of flexibility and customization.

Plone already provides lots of behaviors for the built-in content types.

Other behaviors are implemented as add-on products, which can be installed and configured through the Plone control panel.
Once a behavior has been installed, it can be applied to any content type by selecting it in the {guilabel}`Content Types` control panel.
This allows items of this content type to gain the additional functionality provided by the behavior.

A key feature of behaviors is that they allow encapsulating functionality so that it can be reused for multiple content types without needing to reimplement it.
Overall, behaviors are an important part of the Plone content management system and allow for powerful customization and extensibility of content objects.


## Built-in behaviors

| short name  | Title            | Desription                    |
|-------------|------------------|-------------------------------|
| plone.allowdiscussion  | Allow discussion | Allow discussion on this item |
| plone.basic  | Basic metadata | Adds title and description fields. |
| plone.categorization  | Categorization | Adds keywords and language fields. |
| plone.collection  | Collection | Adds collection behavior |
| plone.publication  | Date range | Adds effective date and expiration date fields. |
| plone.dublincore | Dublin Core metadata | Adds standard metadata fields (equals Basic metadata +    Categorization + Effective range + Ownership  |
| plone.eventattendees  | Event Attendees | Attendees extension for Events. |
| plone.eventbasic  | Event Basic | Basic Event schema. |
| plone.eventcontact  | Event Contact | Contact extension for Events. |
| plone.eventlocation  | Event Location | Location extension for Events. |
| plone.eventrecurrence  | Event Recurrence | Recurrence extension for Events. |
| plone.excludefromnavigation  | Exclude From navigation | Allow items to be excluded from navigation |
| plone.constraintypes| Folder Addable Constrains | Restrict the content types that can be added to folderish   content |
| plone.textindexer | Full-Text Indexing | Enables the enhanced full-text indexing for a content type. If a field in the schema is marked with the `searchable` directive, its content gets added to the `SearchableText` index in the catalog |
| plone.leadimage  | Lead Image | Adds image and image caption fields |
| plone.locking  | Locking | Locking support for dexterity |
| plone.translatable  | Multilingual Support | Make this content type multilingual aware. Multilingual support must be installed. |
| plone.namefromfilename | Name from file name | Automatically generate short URL name for content based on its    primary field file name
| plone.namefromtitle | Name from title | Automatically generate short URL name for content based on its initial    title
| plone.navigationroot  | Navigation root | Make all items of this type a navigation root |
| plone.nextpreviousenabled  | Next previous navigation | Enable next previous navigation for all items of this type |
| plone.nextprevioustoggle  | Next previous navigation toggle | Allow items to have next previous navigation enabled |
| plone.ownership  | Ownership | Adds creator, contributor, and rights fields. |
| plone.relateditems  | Related items | Adds the ability to assign related items |
| plone.richtext  | RichText | Adds richtext behavior |
| plone.shortname  | Short name | Gives the ability to rename an item from its edit form. |
| plone.tableofcontents  | Table of contents | Adds a table of contents |
| plone.thumb_icon | Thumbs and icon handling | Options to suppress thumbs and/or icons and to override thumb   size in listings, tables etc.
| plone.versioning  | Versioning | Versioning support with CMFEditions |
| volto.blocks  | Blocks | Enables Volto Blocks support |
| volto.blocks.editable.layout  | Blocks (Editable Layout) | Enables Volto Blocks (editable layout) support |
| volto.head_title  | Head title field | Adds Head title field |
| volto.navtitle  | Navigation title | Navigation title used in sections, menus and doormats |
| volto.preview_image  | Preview Image | Preview image for listings |
| volto.preview_image_link | Preview Image Link | Preview image for listings based on links |

## Adding or removing a behavior from a content type

There are two ways to add or remove a behavior on a content type:

- Through the web using the {guilabel}`Content Types` control panel.
- Using a custom add-on GenericSetup profile.

### Through the Web

1. Go to the {guilabel}`Site Setup` and chose the {guilabel}`Content Types` control panel.
2. Select the content type to which you want to add or remove a behavior.
3. Then click on the {guilabel}`Behaviors` tab of the settings of the content type.
4. A list of all available behaviors appears.
   Select or deselect the checkbox of the behavior you want to add to or remove from the type.
5. Save the form by clicking on the {guilabel}`Save` button at the bottom of the page.

### Using a GenericSetup profile

Given you already have a custom add-on with a `profiles/default` directory, and you created a custom behavior named `mybehavior.subtitle`.

If you want to enable a behavior on an existing content type, create a new directory `types` under `profiles/default`.
In the `types` directory, create a file named the same as the content type you want to change.
In the example here, you want to add a behavior to the built-in Event content type.
The file to create is named `Event.xml` and it is a {term}`Factory Type Information` (FTI) definition.
You need to change only the behaviors configuration.
All other parts can be ignored.
This looks like so:

```xml
<?xml version="1.0"?>
<object
    i18n:domain="plone"
    meta_type="Dexterity FTI"
    name="Event"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n">
  <property name="behaviors" purge="false">
    <element value="myproject.subtitle" />
  </property>
</object>
```

After you apply the profile (or uninstall and install the custom add-on), the behavior is effective on the Event content type.


## Custom behaviors

There are two types of behaviors:

Schema-only behaviors
: These behaviors have only a schema with fields.

Full behaviors
: A python class containing the logic of the behavior, an interface or schema defining the contract of the behavior, and a marker interface applicable to a content type.

### Creating a schema-only behavior

Given you want to add a field `subtitle` to some existing content types of your custom add-on.

You need to create a file `subtitle.py` in your add-on:

```python
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class ISubtitleBehavior(model.Schema):
    """Subtitle behavior."""

    subtitle = schema.Text(
        title="Subtitle",
        description="A title to be displayed below the title",
        default="",
        required=False,
    )
```

You need to add a ZCML snippet to the `configure.zcml` next to `subtitle.py`:

```xml
<plone:behavior
      name="myproject.subtitle"
      provides=".subtitle.ISubtitleBehavior"
      title="Subtitle"
  />
```

After a restart of Plone, the behavior can be added to the content type in the {guilabel}`Content Types` control panel.
The add and edit forms contain a new field `Subtitle`.

This field is not displayed in most views.
To display the data entered in this field, you need to modify the page template by adding the field `context.subtitle`.

### Creating a behavior with an adapter and factory

Given you want to display a price with different content types.
The price is stored as the net value on the type as a floating point number.
For display, you need at several places the value added tax (VAT) and the gross value.

You create a schema with the net value for the form and attributes for the calculated values.
You create an adapter to calculate the VAT and gross values.
You need a marker interface to distinguish between context and adapter.

Add Python code in the file `price.py`:

```python
from plone.autoform.interfaces import IFormFieldProvider
from plone.supermodel import model
from zope import schema
from zope.interface import Attribute
from zope.interface import implementer
from zope.interface import Interface
from zope.interface import provider


@provider(IFormFieldProvider)
class IPriceBehavior(model.Schema):
    """Behavior: a price, VAT and gross."""

    price_net = schema.Float(
        title="Price (net)",
        required=True,
    )
    price_vat = Attribute("VAT 20% of net price")
    price_gross = Attribute("Price gross (net + VAT 20%")


class IPriceMarker(Interface):
    """Marker for content that has a price."""


@implementer(IPriceBehavior)
class PriceAdapter:
    def __init__(self, context):
        self.context = context

    @property
    def price_net(self):
        """Getter, read from context and return back"""
        return self.context.price_net

    @price_net.setter
    def price_net(self, value):
        """Setter, called by the form, set on context"""
        self.context.price_net = value

    @property
    def price_vat(self):
        return self.price_net * 0.2

    @property
    def price_gross(self):
        return self.price_net + self.price_vat

```

The registration in the `configure.zcml` looks like so:

```XML
  <plone:behavior
      factory=".price.PriceAdapter"
      for=".price.IPriceMarker"
      marker=".price.IPriceMarker"
      name="myproject.price"
      provides=".price.IPriceBehavior"
      title="Price with net, VAT and gross"
  />
  ```

After a restart of Plone, the behavior can be added to the content type in the {guilabel}`Content Types` control panel.
The add and edit forms contain a new field `Price (net)`.

This field is not displayed in most views.
To display the data entered in this field, you need to modify the page template by adding the `price_net` field as `context.price_net`.
To access the `price_vat` and `price_gross` fields, you need to get the adapter in your view class:

```Python
from .price import IPriceBehavior

class SomeViewClass:

    def vat(self):
        adapter = IPriceBehavior(context)
        return adapter.price_vat

    def gross(self):
        adapter = IPriceBehavior(context)
        return adapter.price_gross
```

### Creating a behavior with PloneCLI

To add a behavior to your add-on, you can use PloneCLI as follows:

```shell
plonecli add behavior
```

This will create the behavior Python file in the `behaviors` folder, where you can define your behaviors schema fields, and registers the behavior in the `configure.zcml`.

### Further reading on working with behaviors

```{seealso}
See the chapter {ref}`training:behaviors1-label` from the Mastering Plone 6 Training.
```

## How behaviors work

```{note}
Skip this section if you do not want to dive deeper into the internals of behaviors.
You do not *need* to know this, but it may help if you run into problems.
```

In Plone, behaviors can be globally enabled on content types at runtime.
With add-ons, behaviors can even be enabled even on a single content object or for a whole subtree in the content hierarchy.

### Interfaces and adapters

When a behavior is enabled for a particular object, it will be possible to adapt that object to the behavior's interface.
Otherwise, when the behavior is disabled, adaptation will fail or falls back to a more generic adapter, if any is registered.

A behavior is at least a combination of an interface (also as a form field provider); metadata such as a name, title, and description; and sometimes an adapter factory with a marker interface.
When a behavior is enabled, an interface is added to the content object to indicate its presence.
In other words, the content object now provides the interface.

Behaviors without an adapter factory can be used either as a simple marker or to provide additional form fields.
In this case, adapting a content object with this interface returns the content object itself, because adapting an object that already provides the exact same interface returns the very same object.
Based on the now-provided interface, specific views can be registered with the content type, or event handlers can be registered to respond to specific actions.

In other cases, there is also an adapter factory (usually a Python class), which will be invoked (initialized) to get an appropriate adapter when requested.
If an adapter factory is used, an explicit marker interface is required.

With an adapter factory in place, custom getters and setters for form fields can be implemented, or even new methods.
For example, calculations or the combination of data can be added.

### Registration

Behaviors are registered globally using the `<plone.behavior />` {term}`ZCML` directive.
Internally, this directive registers a named utility that provides `plone.behavior.interfaces.IBehavior`.
This utility contains combined information about the behavior, such as its name, interface, factory or marker interface, and metadata.

```{seealso}
The [README file of `plone.behavior`](https://github.com/plone/plone.behavior/blob/master/README.rst) explains the concepts and different ways to register a behavior in detail.
```

### Lookup and provide

Plone content objects have logic to look up the behaviors' names registered from their types' configuration, the Factory Type Information (FTI).
At runtime, the logic provides the interface (or marker) from the behavior to the object.
This dynamically provided interface enables the component architecture to react to this new interface by adding additional form fields, bindings events, enabling more specific views, and more.
