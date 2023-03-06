---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Vocabularies

**Creating your own static and dynamic vocabularies**

Vocabularies are normally used in conjunction with selection fields,
and are supported by the [zope.schema] package,
with widgets provided by [z3c.form].

Selection fields use the `Choice` field type.
To allow the user to select a single value,
use a `Choice` field directly:

```python
class IMySchema(model.Schema):
    myChoice = schema.Choice(...)
```

For a multi-select field, use a `List`, `Tuple`, `Set` or `Frozenset` with a `Choice` as the `value_type`:

```python
class IMySchema(model.Schema):

    myList = schema.List(
        ...,
        value_type=schema.Choice(...)
    )
```

The choice field must be passed one of the following arguments:

- `values` can be used to give a list of static values;
- `vocabulary` can be used to refer to an `IVocabulary` instance or (more commonly) a string giving the name of an `IVocabularyFactory` named utility.
- `source` can be used to refer to an `IContextSourceBinder` or `ISource` instance;

In the remainder of this section,
we will show the various techniques for defining vocabularies through several iterations of a new field added to the Program type allowing the user to pick the organiser responsible for the program.

## Static vocabularies

Our first attempt uses a static list of organisers.
We use the message factory to allow the labels (term titles) to be translated.
The values stored in the `organizer` field will be a unicode object representing the chosen label,
or `None` if no value is selected:

```python
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

organizers = SimpleVocabulary(
    [
        SimpleTerm(value=u'Bill', title=_(u'Bill')),
        SimpleTerm(value=u'Bob', title=_(u'Bob')),
        SimpleTerm(value=u'Jim', title=_(u'Jim'))
    ]
)

organizer = schema.Choice(
    title=_(u"Organiser"),
    vocabulary=organizers,
    required=False,
)
```

Since `required` is `False`, there will be a {guilabel}`no value` option in the drop-down list.

## Dynamic sources

The static vocabulary is obviously a bit limited,
since it is hard-coded in Python.

We can make a one-off dynamic vocabulary using a context source binder.
This is simply a callable (usually a function or an object with a `__call__` method).
It provides the `IContextSourceBinder` interface and takes a `context` parameter.
The `context` argument is the context of the form
(i.e. the folder on an add form, and the content object on an edit form).
The callable should return a vocabulary,
which is most easily achieved by using the `SimpleVocabulary` class from [zope.schema].

Here is an example using a function to return all users in a particular group:

```python
from Products.CMFCore.utils import getToolByName
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleVocabulary

@provider(IContextSourceBinder)
def possibleOrganizers(context):
    acl_users = getToolByName(context, 'acl_users')
    group = acl_users.getGroupById('organizers')
    terms = []

    if group is not None:
        for member_id in group.getMemberIds():
            user = acl_users.getUserById(member_id)
            if user is not None:
                member_name = user.getProperty('fullname') or member_id
                terms.append(
                    SimpleVocabulary.createTerm(
                        member_id,
                        str(member_id),
                        member_name
                    )
                )

    return SimpleVocabulary(terms)
```

We use the PluggableAuthService API to get the group and its members.
A list of `terms` is created.
The list is passed to the constructor of a `SimpleVocabulary`.
The `SimpleVocabulary` object is returned.

When working with vocabularies,
you’ll come across some terminology that is worth explaining:

- A *term* is an entry in the vocabulary.
  The term has a value.
  Most terms are *tokenised* terms which also have a token,
  and some terms are *titled*,
  meaning they have a title that is different to the token.
- The *token* must be an ASCII string.
  It is the value passed with the request when the form is submitted.
  A token must uniquely identify a term.
- The *value* is the actual value stored on the object.
  This is not passed to the browser or used in the form.
  The value is often a unicode object, but can be any type of object.
- The *title* is a unicode object or translatable message (`zope.i18nmessageid`).
  It is used in the form.

The `SimpleVocabulary` class contains two class methods that can be used to create vocabularies from lists:

`fromValues()`

: takes a simple list of values and returns a tokenised vocabulary where
  the values are the items in the list, and the tokens are created by
  calling `str()` on the values.

`fromItems()`

: takes a list of `(token, value)` tuples and creates a tokenised
  vocabulary with the token and value specified.

You can also instantiate a `SimpleVocabulary` yourself and pass a list
of terms in the initialiser.
The `createTerm()` class method can be used to create a term from a
`value`, `token` and `title`. Only the value is required.

Also to mention, `plone.app.vocabularies` has some helpers creating unicode safe vocabularies.

In the example above, we have chosen to create a `SimpleVocabulary` from
terms with the user id used as value and token, and the user’s full name
as a title.

To use this context source binder, we use the `source` argument to the `Choice` constructor:

```python
organizer = schema.Choice(
    title=_(u"Organiser"),
    source=possibleOrganizers,
    required=False,
)
```

## Parameterised sources

We can improve this example by moving the group name out of the function,
allowing it to be set on a per-field basis.
To do so, we turn our `IContextSourceBinder` into a class that is initialised with the group name:

```python
from zope.interface import implementer

@implementer(IContextSourceBinder)
class GroupMembers(object):
    """Context source binder to provide a vocabulary of users in a given
    group.
    """

    def __init__(self, group_name):
        self.group_name = group_name

    def __call__(self, context):
        acl_users = getToolByName(context, 'acl_users')
        group = acl_users.getGroupById(self.group_name)
        terms = []

        if group is not None:
            for member_id in group.getMemberIds():
                user = acl_users.getUserById(member_id)
                if user is not None:
                    member_name = user.getProperty('fullname') or member_id
                    terms.append(
                        SimpleVocabulary.createTerm(
                            member_id,
                            str(member_id),
                            member_name
                        )
                    )

        return SimpleVocabulary(terms)
```

Again, the source is set using the `source` argument to the `Choice`
constructor:

```python
organizer = schema.Choice(
    title=_(u"Organiser"),
    source=GroupMembers('organizers'),
    required=False,
)
```

When the schema is initialised on startup, a `GroupMembers` object
is instantiated, storing the desired group name. Each time the
vocabulary is needed, this object will be called (i.e. the
`__call__()` method is invoked) with the context as an argument,
expected to return an appropriate vocabulary.

## Named vocabularies

Context source binders are great for simple dynamic vocabularies.
They are also re-usable, since you can import the source from a single location and use it in multiple instances.

Sometimes, however, we want to provide an additional level of decoupling, by using *named* vocabularies.
These are similar to context source binders,
but are components registered as named utilities,
referenced in the schema by name only.
This allows local overrides of the vocabulary via the Component Architecture,
and makes it easier to distribute vocabularies in third party packages.

:::{note}
Named vocabularies cannot be parameterised in the way as we did with the `GroupMembers` context source binder,
since they are looked up by name only.
:::

We can turn our first "members in the *organizers* group" vocabulary into a named vocabulary by creating a named utility providing `IVocabularyFactory`.
Create a vocabulary factory in `vocabularies.py`:

```python
from zope.schema.interfaces import IVocabularyFactory

@provider(IVocabularyFactory)
def organizers_vocabulary_factory(context):
    acl_users = getToolByName(context, 'acl_users')
    group = acl_users.getGroupById('organizers')
    terms = []

    if group is not None:
        for member_id in group.getMemberIds():
            user = acl_users.getUserById(member_id)
            if user is not None:
                member_name = user.getProperty('fullname') or member_id
                terms.append(
                    SimpleVocabulary.createTerm(
                        member_id,
                        str(member_id),
                        member_name
                    )
                )

    return SimpleVocabulary(terms)
```

The add to your `configure.zcml`.
By convention, the vocabulary name is prefixed with the package name, to ensure uniqueness.

```xml
<utility
    name="example.conference.organisers"
    component="example.conference.vocabularies.organizers_vocabulary_factory"
/>
```

We can make use of this vocabulary in any schema by passing its name to
the `vocabulary` argument of the `Choice` field constructor:

```python
organizer = schema.Choice(
    title=_(u"Organiser"),
    vocabulary=u"example.conference.organizers",
    required=False,
)
```

## Using common vocabularies

As you might expect,
there are a number of standard vocabularies that come with Plone.
These are found in the [plone.app.vocabularies] package.
A resent and complete list can be found in the README of the package.

For our example we could use `plone.app.vocabularies.Users`,
that lists the users of the portal.

The `organizer` field now looks like:

```python
organizer = schema.Choice(
    title=_(u"Organiser"),
    vocabulary=u"plone.app.vocabularies.Users",
    required=False,
)
```

## The autocomplete selection widget

The `organizer` field now has a query-based source.
The standard selection widget (a drop-down list) is not capable of rendering such a source.
Instead, we need to use a more powerful widget.
For a basic widget, see [z3c.formwidget.query].
But, in a Plone context, you will more likely want to use [plone.formwidget.autocomplete],
which extends `z3c.formwidget.query` to provide friendlier user interface.

The widget is provided with [plone.app.dexterity],
so we do not need to configure it ourselves.
We only need to tell Dexterity to use this widget instead of the default,
using a form widget hint as shown earlier.
At the top of `program.py`, we add the following import:

```python
from plone.formwidget.autocomplete import AutocompleteFieldWidget
```

:::{note}
If we were using a multi-valued field,
such as a `List` with a `Choice` `value_type`,
we would use the `AutocompleteMultiFieldWidget` instead.
:::

In the `IProgram` schema (which, recall, derives from `model.Schema` and is therefore processed for form hints at startup),
we then add the following:

```python
from plone.autoform import directives

directives.widget(organizer=AutocompleteFieldWidget)
organizer = schema.Choice(
    title=_(u'Organiser'),
    vocabulary=u'plone.app.vocabularies.Users',
    required=False,
)
```

You should now see a dynamic auto-complete widget on the form,
so long as you have JavaScript enabled.
Start typing a user name and see what happens.
The widget also has fall-back for non-JavaScript capable browsers.

[plone.app.dexterity]: http://pypi.python.org/pypi/plone.app.dexterity
[plone.app.vocabularies]: http://pypi.python.org/pypi/plone.app.vocabularies
[plone.formwidget.autocomplete]: http://pypi.python.org/pypi/plone.formwidget.autocomplete
[plone.principalsource]: http://pypi.python.org/pypi/plone.principalsource
[z3c.form]: http://pypi.python.org/pypi/z3c.form
[z3c.formwidget.query]: http://pypi.python.org/pypi/z3c.formwidget.query
[zope.schema]: http://pypi.python.org/pypi/zope.schema
