---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(classic-ui-forms-label)=

# Forms

```{todo}
Describe how create forms with Plone's default form framework z3c.form.
Fields, Widgets, Vocabularies aso are descripted in detail in there own chapter and will be referenced frome examples here.
```

Plone uses the [z3c.form](http://pythonhosted.org/z3c.form) library to build its forms, via the [plone.z3cform](http://pypi.python.org/pypi/plone.z3cform) integration package.

For an easy way to structure a form and define its widgets and fields, Plone relies on [plone.autoform](http://pypi.python.org/pypi/plone.autoform), in particular its AutoExtensibleForm base class.
Which is responsible for processing form hints and setting up [z3c.form](http://pythonhosted.org/z3c.form) widgets and groups (fieldsets).

A form, therefore, is simply a view that uses these libraries, although [plone.autoform](http://pypi.python.org/pypi/plone.autoform) provides some helpful base classes that make it easier to construct forms based on the form schema or {ref}`Dexterity behaviors <backend-behaviors-label>`.


(classic-ui-forms-general-forms-label)=
## General forms

The plonecli provides you with an option to add a form to your Plone package.


```shell
cd collective.awesomeaddon
plonecli add form
```

After using the `plonecli` to add a form, we should have a new sub folder `forms` in our package.
Here we will find a `configure.zcml` containing the registration of the form,

```xml
<browser:page
  name="my-form"
  for="*"
  class=".my_form.MyForm"
  permission="cmf.ManagePortal"
  layer="p6.theme5.interfaces.IP6Theme5Layer"
  />
```

and a Python file with the code.

```python
from plone import schema
from plone.autoform.form import AutoExtensibleForm
from z3c.form import button, form
from zope.interface import Interface


class IMyForm(Interface):
    """ Schema Interface for IMyForm
        Define your form fields here.
    """
    name = schema.TextLine(
        title=u"Your name",
    )


class MyForm(AutoExtensibleForm, form.EditForm):
    schema = IMyForm
    ignoreContext = True

    label = u"What's your name?"
    description = u"Simple, sample form"

    @button.buttonAndHandler(u'Ok')
    def handleApply(self, action):
        data, errors = self.extractData()
        if errors:
            self.status = self.formErrorsMessage
            return

        # Do something with valid data here

        changes = self.applyChanges(data)
        # Set status on this form page
        # (this status message is not bind to the session and does not go thru redirects)
        if changes:
            self.status = "Settings saved"

    @button.buttonAndHandler(u"Cancel")
    def handleCancel(self, action):
        """User canceled. Redirect back to the front page.
        """

```


(classic-ui-forms-dexterity-add-edit-forms-label)=
## Dexterity Add- and Edit forms

Dexterity content types are coming with default add and edit forms.
You can build custom add and edit forms if you need.


```{todo}
Describe Add/Edit forms here and how to customize them.
```


### Disable form tabbing

To disable the form tabbing, you have to override the form and provide a property enable_form_tabbing which is False.

The Python code `custom_edit_form.py` should look like this:

```python
class ICustomEditForm(Interface):
    """
    """

@implementer(ICustomEditForm)
class CustomEditForm(edit.DefaultEditForm):
    """ Custom edit form disabling form_tabbing
    """
    enable_form_tabbing = False

```

to activate it, you have to override the registration of the edit form for your desired content types.
In your configure.zcml:

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    i18n_domain="example.contenttypes">

  <!-- for TTW CT's -->
  <browser:page
    name="edit"
    for="plone.dexterity.interfaces.IDexterityContainer"
    class=".custom_edit_form.CustomEditForm"
    permission="cmf.ModifyPortalContent"
    layer="example.contenttypes.interfaces.IExampleContenttypesLayer"
    />

  <browser:page
    name="edit"
    for="example.contenttypes.content.technical_facility.ITechnicalFacility"
    class=".custom_edit_form.CustomEditForm"
    permission="cmf.ModifyPortalContent"
    layer="example.contenttypes.interfaces.IExampleContenttypesLayer"
    />
</configure>
```
