---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Using behaviors

**Finding and adding behaviors**

Dexterity introduces the concept of *behaviors* – re-usable bundles of
functionality and/or form fields which can be turned on or off on a
per-type basis.

Each behavior has a unique interface. When a behavior is enabled on a
type, you will be able to adapt that type to the behavior’s interface.
If the behavior is disabled, the adaptation will fail. The behavior
interface can also be marked as an `IFormFieldsProvider`, in which case
it will add fields to the standard add and edit forms. Finally, a
behavior may imply a sub-type: a marker interface which will be
dynamically provided by instances of the type for which the behavior is
enabled.

We will not cover writing new behaviors in this manual, but we will show
how to enable behaviors on a type. Writing behaviors is covered in the
[Behaviors manual](http://docs.plone.org/external/plone.app.dexterity/docs/behaviors/index.html).

In fact, we’ve already seen one
standard behavior applied to our example types, registered in the FTI
and imported using GenericSetup:

```xml
<property name="behaviors">
    <element value="plone.app.content.interfaces.INameFromTitle" />
</property>
```

Other behaviors are added in the same way, by listing additional
behavior interfaces as elements of the `behaviors` property.

Behaviors are normally registered with the `<plone:behavior />` ZCML
directive. When registered, a behavior will create a global utility
providing `IBehavior`, which is used to provide some metadata, such as a
title and description for the behavior.

You can find and apply behaviors via the {guilabel}`Dexterity Content Types`
control panel that is installed with [plone.app.dexterity]. For a list
of standard behaviors that ship with Dexterity, see the reference at the
end of this manual.

[plone.app.dexterity]: http://pypi.python.org/pypi/plone.app.dexterity
