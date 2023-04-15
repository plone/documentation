---
myst:
  html_meta:
    "description": "Content type defaults"
    "property=og:description": "Content type defaults"
    "property=og:title": "Content type defaults"
    "keywords": "Plone, Content type, defaults"
---

# Defaults

This chapter describes the default values for fields on add forms.

It is often useful to calculate a default value for a field.
This value will be used on the add form before the field is set.

To continue with our conference example, let's set the default values for the `start` and `end` dates to one week in the future and ten days in the future, respectively.
We can do this by adding the following to {file}`program.py`.

```python
import datetime

def startDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(7)

def endDefaultValue():
    return datetime.datetime.today() + datetime.timedelta(10)
```

We also need to modify `IProgram` so the `start` and `end` fields use these functions as their `defaultFactory`.

```python
class IProgram(model.Schema):

    start = schema.Datetime(
        title=_("Start date"),
        required=False,
        defaultFactory=startDefaultValue,
    )

    end = schema.Datetime(
        title=_("End date"),
        required=False,
        defaultFactory=endDefaultValue,
    )
```

The `defaultFactory` is a function that will be called when the add form is loaded to determine the default value.

The value returned by the method should be a value that's allowable for the field.
In the case of `Datetime` fields, that's a Python `datetime` object.

It is also possible to write a context-aware default factory that will be passed the container for which the add form is being displayed.

```python
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory

@provider(IContextAwareDefaultFactory)
def getContainerId(context):
    return context.getId()
```

It is possible to provide different default values depending on the type of context, a request layer, the type of form, or the type of widget used.
See the [z3c.form](https://z3cform.readthedocs.io/en/latest/advanced/validator.html#look-up-value-from-default-adapter) documentation for more details.

We'll cover creating custom forms later in this manual.
