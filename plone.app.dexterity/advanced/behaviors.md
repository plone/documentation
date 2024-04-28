---
myst:
  html_meta:
    "description": "How to find and add behaviors in Plone content types"
    "property=og:description": "How to find and add behaviors in Plone content types"
    "property=og:title": "How to find and add behaviors in Plone content types"
    "keywords": "Plone, content types, behaviors"
---

# Behaviors

This chapter describes how to find and add behaviors.

Dexterity introduces the concept of *behaviors*, which are reusable bundles of functionality or form fields which can be turned on or off on a per-type basis.

Each behavior has a unique interface.
When a behavior is enabled on a type, you will be able to adapt that type to the behavior's interface.
If the behavior is disabled, the adaptation will fail.
The behavior interface can also be marked as an `IFormFieldsProvider`, in which case it will add fields to the standard add and edit forms.
Finally, a behavior may imply a sub-type: a marker interface which will be dynamically provided by instances of the type for which the behavior is enabled.

We will not cover writing new behaviors here, but we will show how to enable behaviors on a type.
Writing behaviors is covered in {doc}`/backend/behaviors`.

In fact, we've already seen one standard behavior applied to our example types, registered in the FTI and imported using GenericSetup.

```xml
<property name="behaviors">
    <element value="plone.app.content.interfaces.INameFromTitle" />
</property>
```

Other behaviors are added in the same way, by listing additional behavior interfaces as elements of the `behaviors` property.

Behaviors are normally registered with the `<plone:behavior />` ZCML directive.
When registered, a behavior will create a global utility providing `IBehavior`, which is used to provide some metadata, such as a title and description for the behavior.

You can find and apply behaviors via the {guilabel}`Dexterity Content Types` control panel that is installed with [`plone.app.dexterity`](https://pypi.org/project/plone.app.dexterity/).
For a list of standard behaviors that ship with Plone, see {ref}`backend-built-in-behaviors-label`.