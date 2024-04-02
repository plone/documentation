---
myst:
  html_meta:
    "description": "Validators"
    "property=og:description": "Validators"
    "property=og:title": "Validators"
    "keywords": "Plone, Validators, constraints, content types"
---

# Validators

This chapter describes how to create custom validators for your type.

Many applications require some form of data entry validation.
The simplest form of validation you get for free, the [z3c.form](https://pypi.org/project/z3c.form/) library ensures that all data entered in Dexterity add and edit forms is valid for the field type.

It is also possible to set certain properties on the fields to add further validation, or even create your own fields with custom validation logic, although that is a lot less common.
These properties are set as parameters to the field constructor when the schema interface is created.
You should see the [zope.schema](https://pypi.org/project/zope.schema/) package for details.

The most common constraints are:

`required=True/False`
: to make a field required or optional;

`min` and `max`
: used for `Int`, `Float`, `Datetime`, `Date`, and `Timedelta` fields, specify the minimum and maximum (inclusive) allowed values of the given type.

`min_length` and `max_length`
: used for collection fields (`Tuple`, `List`, `Set`, `Frozenset`, `Dict`) and text fields (`Bytes`, `BytesLine`, `ASCII`, `ASCIILine`, `Text`, `TextLine`), set the minimum and maximum (inclusive) length of a field.


## Constraints

If this does not suffice, you can pass your own constraint function to a field.
The constraint function should take a single argument: the value that is to be validated.
This will be the field's type.
The function should return a boolean `True` or `False`.

```python
def checkForMagic(value):
    return 'magic' in value
```

```{note}
The constraint function does not have access to the context, but if you need to acquire a tool, you can use the `zope.component.hooks.getSite()` method to obtain the site root.
```

To use the constraint, pass the function as the `constraint` argument to the field constructor, for example:

```python
my_field = schema.TextLine(title=_("My field"), constraint=checkForMagic)
```

Constraints are easy to write, but do not necessarily produce very friendly error messages.
It is possible to customize these error messages using `z3c.form` error view snippets.
See the [z3c.form documentation](https://z3cform.readthedocs.io/en/latest/) for more details.


## Invariants

You'll also notice that constraints only check a single field value.
If you need to write a validator that compares multiple values, you can use an invariant.
Invariants use exceptions to signal errors, which are displayed at the top of the form rather than next to a particular field.

To illustrate an invariant, let's make sure that the start date of a `Program` is before the end date.
In `program.py`, we add the following.

```python
from zope.interface import invariant, Invalid

class StartBeforeEnd(Invalid):
    __doc__ = _("The start or end date is invalid")

class IProgram(model.Schema):

    start = schema.Datetime(
        title=_("Start date"),
        required=False,
    )

    end = schema.Datetime(
        title=_("End date"),
        required=False,
    )

    @invariant
    def validateStartEnd(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise StartBeforeEnd(_("The start date must be before the end date."))
```


## Form validators

Finally, you can write more powerful validators by using the `z3c.form` widget validators.
For details see [`z3c.form` validators](https://5.docs.plone.org/develop/plone/forms/z3c.form.html#validators).
