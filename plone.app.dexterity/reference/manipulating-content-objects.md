---
myst:
  html_meta:
    "description": "Manipulating content objects in Plone"
    "property=og:description": "Manipulating content objects in Plone"
    "property=og:title": "Manipulating content objects in Plone"
    "keywords": "Plone, manipulating, content objects"
---

# Manipulating content objects

This chapter describes common APIs used to manipulate Dexterity content objects.

```{note}
Here the low level API is shown.
When writing Plone add-ons, consider using `plone.api` because it covers several standard cases and is a simple, future-proof, and stable API.
```

In this section, we will describe some of the more commonly used APIs that can be used to inspect and manipulate Dexterity content objects.
In most cases, the content object is referred to as `context`, its parent folder is referred to as `folder`, and the type name is `example.type`.
Relevant imports are shown with each code snippet, though of course you are more likely to place those at the top of the relevant code module.


## Content object creation and folder manipulation

This section describes the means to create objects and manipulate folders.


### Creating a content object

The simplest way to create a content item is via its factory:

```python
from zope.component import createObject
context = createObject("example.type")
```

At this point, the object is not wrapped with an acquisition.
You can wrap it explicitly by calling the following.

```python
wrapped = context.__of__(folder)
```

However, it's normally better to add the item to a folder and then re-get it from the folder.

Note that the factory is normally installed as a local utility, so the `createObject()` call will only work once you've traversed over the Plone site root.

There is a convenience method that can be used to create a Dexterity object.
It is mostly useful in tests.

```python
from plone.dexterity.utils import createContent
context = createContent("example.type", title="Foo")
```

Any keyword arguments are used to set properties on the new instance via `setattr()` on the newly created object.
This method relies on being able to look up the FTI as a local utility, so again you must be inside the site for it to work.


### Adding an object to a container

Once an object has been created, it can be added to a container.
If the container is a Dexterity container, or another container that supports a dict API (for example, a `Large Plone Folder` in Plone 3, or a container based on `plone.folder`), you can do the following.

```python
folder["some_id"] = context
```

You should normally make sure that the `id` property of the object is the same as the ID used in the container.

If the object only supports the basic OFS API (as is the case with standard Plone `Folders` in Plone 3), you can use the `_setObject()` method.

```python
folder._setObject("some_id") = context
```

Note that both of these approaches bypass any type checks, in other words, you can add items to containers that would not normally allow this type of content.
Dexterity comes with a convenience function, useful in tests, to simulate the checks performed when content is added through the web.

```python
from plone.dexterity.utils import addContentToContainer
addContentToContainer(folder, context)
```

This will also invoke a name chooser and set the object's ID accordingly.
Things such as the `title-to-id` behavior should work.
As before, this relies on local components, so you must have traversed into a Plone site.
`PloneTestCase` takes care of this for you.

To bypass folder constraints, you can use this function and pass `checkConstraints=False`.

You can also both create and add an object in one call.

```python
from plone.dexterity.utils import createContentInContainer
createContentInContainer(folder, "example.type", title="Foo")
```

Again, you can pass `checkConstraints=False` to bypass folder constraints, and pass object properties as keyword arguments.

Finally, you can use the `invokeFactory()` API, which is similar but more generic, in that it can be used for any type of content, not just Dexterity content.

```python
new_id = folder.invokeFactory("example.type", "some_id")
context = folder["new_id"]
```

This always respects add constraints, including add permissions and the current user's roles.


### Getting items from a folder

Dexterity containers and other containers based on `plone.folder` support a dict-like API to obtain and manipulate items in folders.
For example, to obtain an acquisition-wrapped object by name.

```python
context = folder["some_id"]
```

Folders can also be iterated over.
You can call `items()`, `keys()`, `values()`, and so on, treating the folder as a dict with string keys and content objects as values.

Dexterity containers also support the more basic OFS API.
You can call `objectIds()` to get keys, `objectValues()` to get a list of content objects, `objectItems()` to get an `items()`-like dict, and `hasObject(id)` to check if an object exists in a container.


### Removing items from a folder

Again, Dexterity containers act like dictionaries, and thus implement `__delitem__`.

```python
del folder["some_id"]
```

The OFS API uses the `_delObject()` function for the same purpose.

```python
folder._delObject("some_id")
```


## Object introspection

This section describes the means of getting information about an object.


### Obtaining an object's schema interface

A content object's schema is an interface, in other words, an object of type `zope.interface.interface.InterfaceClass`.

```python
from zope.app.content import queryContentType
schema = queryContentType(context)
```

The schema can now be inspected.

```python
from zope.schema import getFieldsInOrder
fields = getFieldsInOrder(schema)
```


### Finding an object's behaviors

To find all behaviors supported by an object, use the `plone.behavior` API.

```python
from plone.behavior.interfaces import IBehaviorAssignable
assignable = IBehaviorAssignable(context)
for behavior in assignable.enumerateBehaviors():
 behavior_schema = behavior.interface
 adapted = behavior_schema(context)
 # ...
```

The objects returned are instances providing `plone.behavior.interfaces.IBehavior`.
To get the behavior schema, use the `interface` property of this object.
You can inspect this and use it to adapt the context if required.


### Getting the FTI

To obtain a Dexterity FTI, look it up as a local utility.

```python
from zope.component import getUtility
from plone.dexterity.interfaces import IDexterityFTI
fti = getUtility(IDexterityFTI, name="example.type")
```

The returned object provides `plone.dexterity.interfaces.IDexterityFTI`.
To get the schema interface for the type from the FTI, you can do the following.

```python
schema = fti.lookupSchema()
```


### Getting the object's parent folder

A Dexterity item in a Dexterity container should have the `__parent__` property set, pointing to its containing parent.

```python
folder = context.__parent__
```

Items in standard Plone folders won't have this property set, at least not in Plone 3.x.

The more general approach relies on acquisition.

```python
from Acquisition import aq_inner, aq_parent
folder = aq_parent(aq_inner(context))
```


## Workflow

This section describes ways to inspect an object's workflow state and invoke transitions.


### Obtaining the workflow state of an object

To obtain an object's workflow state, ask the `portal_workflow` tool:

```python
from Products.CMFCore.utils import getToolByName
portal_workflow = getToolByName(context, "portal_workflow")
review_state = portal_workflow.getInfoFor(context, "review_state")
```

This assumes that the workflow state variable is called `review_state`, as is the case for almost all workflows.


### Invoking a workflow transition

To invoke a transition, use the following.

```python
portal_workflow.doActionFor(context, "some_transition")
```

The transition must be available in the current workflow state, for the current user.
Otherwise, an error will be raised.


## Cataloging and indexing

This section describes ways of indexing an object in the `portal_catalog` tool.


### Reindexing the object

Objects may need to be reindexed if they are modified in code.
The best way to reindex them is to send an event, and let Dexterity's standard event handlers take care of this.

```python
from zope.lifecycleevent import modified
modified(context)
```

In tests, it is sometimes necessary to reindex explicitly.
This can be done with the following.

```python
context.reindexObject()
```

You can also pass specific index names to reindex, if you don't want to reindex everything.

```python
context.reindexObject(idxs=["Title", "sortable_title"])
```

This method comes from the `Products.CMFCore.CMFCatalogAware.CMFCatalogAware` mix-in class.


## Security

This section describes ways to check and modify permissions.
For more information, see the section on {doc}`../advanced/permissions`.


### Checking a permission

To check a permission by its Zope 3 name, use the following.

```python
from zope.security import checkPermission
checkPermission("zope2.View", context)
```

```{note}
In a test, you may get an `AttributeError` when calling this method.
To resolve this, call `newInteraction()` from `Products.Five.security` in your test setup (for example, the `afterSetUp()` method).
```

Use the Zope 2 permission title.

```python
from AccessControl import getSecurityManager
getSecurityManager().checkPermission("View", context)
```

Sometimes, normally in tests, you want to know which roles have a particular permission.
To do this, use the following.

```python
roles = [r["name"] for r in context.rolesOfPermission("View") if r["selected"]]
```

Again, note that this uses the Zope 2 permission title.


### Changing permissions

Normally, permissions should be set with workflow, but in tests it is often useful to manipulate security directly.

```python
context.manage_permission("View", roles=["Manager", "Owner"], acquire=True)
```

Again note that this uses the Zope 2 permission title.


## Content object properties and methods

The following table shows the more important properties and methods available on Dexterity content objects.
In addition, any field described in the type's schema will be available as a property, and can be read and set using normal attribute access.

| Property/method | Type | Description |
| -------------------- | ----------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| __name__ | unicode | The name (ID) of the object in its container. This is a Unicode string to be consistent with the Zope 3 `IContained` interface, although in reality it will only ever contain ASCII characters, since Zope 2 does not support non-ASCII URLs. |
| id | str | The name (ID) of the object in its container. This is an ASCII string encoding of the `__name__`. |
| getId() | str | Returns the value of the `id` `property`.
| isPrincipiaFolderish | bool/int | `True` (or `1`) if the object is a folder. `False` (or `0`) otherwise. |
| portal_type | str | The `portal_type` of this instance. Should match an FTI in the `portal_types` tool. For Dexterity types, should match a local utility providing `IDexterityFTI`. Note that the `portal_type` is a per-instance property set upon creation (by the factory), and should not be set on the class. |
| meta_type | str | A Zope 2 specific way to describe a class. Rarely, if ever, used in Dexterity. Do not set it on your own classes unless you know what you're doing. |
| title_or_id() | str | Returns the value of the `title` property or, if this is not set, the `id` property. |
| absolute_url() | str | The full URL to the content object. Will take virtual hosting and the current domain into account. |
| getPhysicalPath() | tuple | A sequence of string path elements from the application root. Stays the same regardless of virtual hosting and domain. A common pattern is to use `'/'.join(context.getPhysicalPath())` to get a string representing the path to the Zope application root. Note that it is *not* safe to construct a relative URL from the path, because it does not take virtual hosting into account. |
| title | unicode/str | Property representing the title of the content object. Usually part of an object's schema or provided by the `IBasic` behavior. The default is an empty string. |
| Title() | unicode/str | Dublin Core accessor for the `title` property. Set the title by modifying this property. You can also use `setTitle()`. |
| listCreators() | tuple | A list of user IDs for object creators. The first creator is normally the owner of the content object. You can set this list using the `setCreators()` method. |
| Creator() | str | The first creator returned by the `listCreators()` method. Usually the owner of the content object. |
| Subject() | tuple | Dublin Core accessor for item keywords. You can set this list using the `setSubject()` method. |
| Description() | unicode/str | Dublin Core accessor for the `description` property, which is usually part of an object's schema or provided by the `IBasic` behavior. You can set the description by setting the `description` attribute, or using the `setDescription()` method. |
| listContributors() | tuple | Dublin Core accessor for the list of object contributors. You can set this with `setContributors()`. |
| Date() | str | Dublin Core accessor for the default date of the content item, in ISO format. Uses the effective date is set, falling back on the modification date. |
| CreationDate() | str | Dublin Core accessor for the creation date of the content item, in ISO format. |
| EffectiveDate() | str | Dublin Core accessor for the effective publication date of the content item, in ISO format. You can set this by passing a DateTime object to `setEffectiveDate()`. |
| ExpirationDate() | str | Dublin Core accessor for the content expiration date, in ISO format. You can set this by passing a DateTime object to `setExpirationDate()`. |
| ModificationDate() | str | Dublin Core accessor for the content last-modified date, in ISO format. |
| Language() | str | Dublin Core accessor for the content language. You can set this using `setLanguage()`. |
| Rights() | str | Dublin Core accessor for content copyright information. You can set this using `setRights()`. |
| created() | DateTime | Returns the Zope 2 DateTime for the object's creation date. If not set, returns a "floor" date of January 1, 1970. |
| modified() | DateTime | Returns the Zope 2 DateTime for the object's modification date. If not set, returns a "floor" date of January 1, 1970. |
| effective() | DateTime | Returns the Zope 2 DateTime for the object's effective date. If not set, returns a "floor" date of January 1, 1970. |
| expires() | DateTime | Returns the Zope 2 DateTime for the object's expiration date. If not set, returns a "floor" date of January 1, 1970. |
