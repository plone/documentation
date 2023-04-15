---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Permissions

**Setting up add permissions, view permissions and field view/edit permissions**

Plone’s security system is based on the concept of
*permissions* protecting *operations*
(like accessing a view,
viewing a field,
modifying a field,
or adding a type of content)
that are granted to *roles*,
which in turn are granted to *users* and/or *groups*.
In the context of developing content types,
permissions are typically used in three different ways:

- A content type or group of related content types often has a custom
  *add permission* which controls who can add this type of content.
- Views (including forms) are sometimes protected by custom
  permissions.
- Individual fields are sometimes protected by permissions,
  so that some users can view and edit fields that others can’t see.

It is easy to create new permissions.
However, be aware that it is considered good practice to use the standard permissions wherever possible and use *workflow* to control which roles are granted these permissions on a per-instance basis.

For more basic information on permissions and how to create custom permissions read the [Security Section] in the Plone documentation.

## Performing permission checks in code

It is sometimes necessary to check permissions explicitly in code, for
example in a view. A permission check always checks a permission on a
context object, since permissions can change with workflow.

:::{note}
Never make security dependent on users’ roles directly.
Always check for a permission, and assign the permission to the appropriate role or roles.
:::

As an example,
let’s display a message on the view of a `Session` type
if the user has the `cmf.RequestReview` permission.
In `session.py`, we update the `View` class with the following:

```
from zope.security import checkPermission

class View(BrowserView):

    def canRequestReview(self):
        return checkPermission('cmf.RequestReview', self.context)
```

And in the `session_templates/view.pt` template, we add:

```html
<div class="discreet"
     tal:condition="view/canRequestReview"
     i18n:translate="suggest_review">
    Please submit this for review.
</div>
```

## Content type add permissions

Dexterity content types’ add permissions are set in the FTI,
using the `add_permission` property.
This can be changed through the web
or in the GenericSetup import step for the content type.

To make the `Session` type use our new permission, we modify the
`add_permission` line in
`profiles/default/example.conference.session.xml`:

```xml
<property name="add_permission">example.conference.AddSession</property>
```

## Protecting views and forms

Access to views and other browser resources (like viewlets or portlets)
can be protected by permissions, either using the `permission` attribute
on ZCML statements like:

```
<browser:page
    ...
    permission="zope.Public"
    ...
    />
```

We could also use the special `zope.Public` permission name to make the view accessible to anyone.

## Protecting form fields

Individual fields in a schema may be associated with a *read* permission
and a *write* permission.
The read permission is used to control access to the field’s value via protected code
(e.g. scripts or templates created through the web)
and URL traversal,
and can be used to control the appearance of fields when using display forms
(if you use custom views that access the attribute directly, you’ll need to perform your own checks).
Write permissions can be used to control whether or not a given field appears on a type’s add and edit forms.

In both cases,
read and write permissions are annotated onto the schema using directives similar to those we’ve already seen for form widget hints.
The `read_permission()` and `write_permission()` directives are found in the [plone.autoform] package.

If XML-schemas are used for defintion see {ref}`Dexterity XML: security attributes <dexterity-xml-security>`.

Simple example protecting a field to be readable for Site Administrators only:

```
from zope import schema
from plone.supermodel import model
from plone.autoform.directives import read_permission, write_permission

class IExampleProtectedInformation(model):

    read_permission(info='cmf.ManagePortal')
    write_permission(info='cmf.ManagePortal')
    info = schema.Text(
        title=_("Information"),
    )
```

As a complex example, let’s add a field for *Session* reviewers to record the track for a session.
We’ll store the vocabulary of available tracks on the parent `Program` object in a text field,
so that the creator of the `Program` can choose the available tracks.

First, we add this to the `IProgram` schema in `program.py`:

```
form.widget(tracks=TextLinesFieldWidget)
tracks = schema.List(
        title=_("Tracks"),
        required=True,
        default=[],
        value_type=schema.TextLine(),
    )
```

The `TextLinesFieldWidget` is used to edit a list of text lines in a
text area. It is imported as:

```
from plone.z3cform.textlines.textlines import TextLinesFieldWidget
```

Next, we’ll add a vocabulary for this to `session.py`:

```
from Acquisition import aq_inner, aq_parent
from zope.component import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary
...

@provider(IContextSourceBinder)
def possibleTracks(context):

    # we put the import here to avoid a circular import
    from example.conference.program import IProgram
    while context is not None and not IProgram.providedBy(context):
        context = aq_parent(aq_inner(context))

    values = []
    if context is not None and context.tracks:
        values = context.tracks

    return SimpleVocabulary.fromValues(values)
```

This vocabulary finds the closest `IProgram`
(in the add form, the `context` will be the `Program`,
but on the edit form, it will be the `Session`,
so we need to check the parent)
and uses its `tracks` variable as the vocabulary.

Next, we add a field to the `ISession` interface in the same file and
protect it with the relevant write permission:

```
write_permission(track='example.conference.ModifyTrack')
track = schema.Choice(
        title=_("Track"),
        source=possibleTracks,
        required=False,
    )
```

With this in place, users with the `example.conference: Modify track`
permission should be able to edit tracks for a session. For everyone
else, the field will be hidden in the edit form.

[plone.autoform]: http://pypi.python.org/pypi/plone.autoform
[security section]: http://docs.plone.org/develop/plone/security/index.html
