---
myst:
  html_meta:
    "description": "How to add a custom content class implementation in Plone"
    "property=og:description": "How to add a custom content class implementation in Plone"
    "property=og:title": "How to add a custom content class implementation in Plone"
    "keywords": "Plone, custom, content, class"
---

# Custom content classes

This chapter describes how to add a custom content class implementation.

When we learned about configuring the Dexterity FTI, we saw the `klass` attribute and how it could be used to refer to either the `Container` or `Item` content classes.
These classes are defined in the [`plone.dexterity.content`](https://github.com/plone/plone.dexterity/blob/master/plone/dexterity/content.py) module, and represent container (folder) and item (non-folder) types, respectively.

For most applications, these two classes will suffice.
We will normally use behaviors, adapters, event handlers, and schema interfaces to build additional functionality for our types.
In some cases, however, it is useful or necessary to override the class, typically to override some method or property provided by the base class that cannot be implemented with an adapter override.
A custom class may also be able to provide marginally better performance by side-stepping some of the schema-dependent dynamic behavior found in the base classes.
In real life, you are very unlikely to notice, though.

To create a custom class, derive from one of the standard ones, as shown below

```python
from plone.dexterity.content import Item

class MyItem(Item):
    """A custom content class"""
```

For a container type, we'd do the following

```python
from plone.dexterity.content import Container

class MyContainer(Container):
    """A custom content class"""
```

You can now add any required attributes or methods to this class.

To make use of this class, set the `klass` attribute in the FTI to its dotted name, as shown in the following example.

```xml
<property name="klass">my.package.myitem.MyItem</property>
```

This will cause the standard Dexterity factory to instantiate this class when the user submits the add form.

```{note}
As an alternative to setting `klass` in the FTI, you may provide your own `IFactory` utility for this type in lieu of Dexterity's default factory (see [plone.dexterity.factory](https://github.com/plone/plone.dexterity/blob/master/plone/dexterity/factory.py)).
However, you need to be careful that this factory performs all necessary initialization, so it is normally better to use the standard factory.
```


## Custom class caveats

There are a few important caveats when working with custom content classes:

-   Make sure you use the correct base class: either `plone.dexterity.content.Item` or
  `plone.dexterity.content.Container`.
-   If you mix in other base classes, it is safer to put the `Item` or `Container` class first.
    If another class comes first, it may override the `__name__`, `__providedBy__`, `__allow_access_to_unprotected_subobjects__`, or `isPrincipiaFolderish` properties, and possibly the `__getattr__()` and `__getitem__()` methods, causing problems with the dynamic schemata or folder item security.
    In all cases, you may need to explicitly set these attributes to the ones from the correct base class.
-   If you define a custom constructor, make sure it can be called with no arguments, and with an optional `id` argument giving the name.
