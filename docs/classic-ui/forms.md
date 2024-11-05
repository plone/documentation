---
myst:
  html_meta:
    "description": "Create forms in Plone"
    "property=og:description": "Create forms in Plone"
    "property=og:title": "Create forms in Plone"
    "keywords": "Plone, forms"
---

(classic-ui-forms-label)=

# Forms

```{todo}
Describe how create forms with Plone's default form framework `z3c.form`.
{doc}`/backend/fields`, {doc}`/backend/widgets`, {doc}`/backend/vocabularies` are also described in detail in their own chapters, and will be referenced from examples here.
```

Plone uses the [`z3c.form`](https://z3cform.readthedocs.io/en/latest/) library to build its web forms.
The packages responsible for integrating `z3c.form` with Plone are [`plone.z3cform`](https://github.com/plone/plone.z3cform) and [`plone.app.z3cform`](https://github.com/plone/plone.app.z3cform), which contain most of the widgets and default templates.
To simplify the process of organizing a form and specifying its widgets and fields, Plone utilizes [`plone.autoform`](https://github.com/plone/plone.autoform), in particular its `AutoExtensibleForm` base class.
It is responsible for handling form hints and configuring `z3c.form` widgets and groups (fieldsets).

A form is a view that uses these libraries to generate forms.


(classic-ui-forms-general-forms-label)=

## General forms

The {term}`plonecli` provides you with an option to add a form to your Plone package.
Let's assume you created an add-on package with {term}`plonecli` called `collective.awesomeaddon`.

```shell
cd collective.awesomeaddon
plonecli add form
```

After using the {term}`plonecli` to add a form, you'll have a new sub folder `forms` in your package.
Here you will find a `configure.zcml` containing the registration of the form.

```xml
<!-- ZCML header and other ZCML here  -->
<browser:page
  name="my-form"
  for="*"
  class=".my_form.MyForm"
  permission="cmf.ManagePortal"
  layer="p6.theme5.interfaces.IP6Theme5Layer"
  />
  <!-- further ZCML and ZCML footer go inside the `browser:page` node  -->
```

And a Python file with the code.

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
        title="Your name",
    )


class MyForm(AutoExtensibleForm, form.EditForm):
    schema = IMyForm
    ignoreContext = True

    label = "What's your name?"
    description = "Simple, sample form"

    @button.buttonAndHandler("Ok")
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

    @button.buttonAndHandler("Cancel")
    def handleCancel(self, action):
        """User cancelled. Redirect back to the front page.
        """
```

Our form `MyForm` is a subclass of the `z3c.form` base class, `z3c.form.form.EditForm`, and `plone.autoform.form.AutoExtensibleForm`, which adds some convenient methods to organize the form fields and widgets.
Besides some basic properties such as `label` and `description`, the more interesting properties are `schema` and `ignoreContext`.


### Configure the form

In this section, you will configure the form's properties.


#### `schema`

The schema property points to a schema interface, which defines the fields of our form.

```python
schema = IMyForm
```


#### `ignoreContext`

If your form is not bound to an object (such as a Dexterity object), set `ignoreContext = True`.


(classic-ui-controlling-form-presentation-label)=

## Controlling form presentation

Directives can be specified in the schema to control aspects of form presentation.

### Control field and widget presentation

See the corresponding chapters to learn how to control field and widget presentation in a form.

```{seealso}
-   {ref}`backend-fields-schema-autoform-permission`
-   {ref}`backend-schemas-directives-label`
-   {ref}`backend-widgets-change-a-fields-display-label`
-   {ref}`backend-widgets-change-a-fields-widget-label`
```


### Display Forms

Sometimes rather than rendering a form for data entry, you want to display stored values based on the same schema.
This can be done using a "display form".
The display form renders each field's widget in "display mode", which means that it shows the field value in read-only form rather than as a form input.

To use the display form, create a view that extends `WidgetsView` like this:

```python
from plone.autoform.view import WidgetsView

class MyView(WidgetsView):
    schema = IMySchema
    additionalSchemata = (ISchemaOne, ISchemaTwo,)
```

To render the form, do not override `__call__()`.
Instead, either implement the `render()` method, set an `index` attribute to a page template or other callable, or use the `template` attribute of the `<browser:page />` ZCML directive when registering the view.

In the template, you can use the following variables:

-   `view/w` is a dictionary of all widgets, including those from non-default fieldsets.
    By contrast, the `widgets` variable contains only those widgets in the default fieldset.
    The keys are the field names, and the values are widget instances.
    To render a widget (in display mode), you can do `tal:replace="structure view/w/myfield/render" />`.
-   `view/fieldsets` is a dictionary of all fieldsets not including the default fieldset, in other words, those widgets not placed into a fieldset.
    The keys are the fieldset names, and the values are the fieldset form instances, which in turn have variables, such as `widgets`, given a list of all widgets.


(classic-ui-forms-dexterity-add-edit-forms-label)=

## Dexterity add and edit forms

Dexterity content types come with default add and edit forms.
You can build custom add and edit forms to adjust their behavior.

The implementation of the default edit and add forms is in [`plone.dexterity.browser.edit.py`](https://github.com/plone/plone.dexterity/blob/master/plone/dexterity/browser/edit.py) and [`plone.dexterity.browser.add.py`](https://github.com/plone/plone.dexterity/blob/master/plone/dexterity/browser/add.py).

```{todo}
Describe Add/Edit forms here and how to customize them.
Provide mutiple examples.
```


### Disable form tabbing

To disable the form tabbing, you have to override the edit and add forms, and provide a property `enable_form_tabbing` as `False`.

The Python code `custom_forms.py` should look like this:

```python
from plone.dexterity.browser import add
from plone.dexterity.browser import edit
from zope.interface import implementer
from zope.interface import Interface


class ICustomEditForm(Interface):
    """
    """

@implementer(ICustomEditForm)
class CustomEditForm(edit.DefaultEditForm):
    """ Custom edit form disabling form_tabbing
    """
    enable_form_tabbing = False


class ICustomAddForm(Interface):
    """
    """


@implementer(ICustomAddForm)
class CustomAddForm(add.DefaultAddForm):
    """ Custom add form disabling form_tabbing
    """
    enable_form_tabbing = False


class ICustomAddView(Interface):
    """ """


@implementer(ICustomAddView)
class CustomAddView(add.DefaultAddView):
    form = CustomAddForm
```

To activate them, you must override the registration of the forms for your desired content types.
In your `configure.zcml`:

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    i18n_domain="example.contenttypes">

  <!-- Edit form -->
  <browser:page
    name="edit"
    for="example.contenttypes.content.technical_facility.ITechnicalFacility"
    class=".custom_forms.CustomEditForm"
    permission="cmf.ModifyPortalContent"
    layer="example.contenttypes.interfaces.IExampleContenttypesLayer"
    />

  <!-- Edit form for TTW CT's -->
  <browser:page
    name="edit"
    for="plone.dexterity.interfaces.IDexterityContainer"
    class=".custom_forms.CustomEditForm"
    permission="cmf.ModifyPortalContent"
    layer="example.contenttypes.interfaces.IExampleContenttypesLayer"
    />

  <!-- Add form  -->
  <adapter
      factory=".custom_forms.CustomAddView"
      provides="zope.publisher.interfaces.browser.IBrowserPage"
      for="Products.CMFCore.interfaces.IFolderish
           example.contenttypes.interfaces.IExampleContenttypesLayer
           plone.dexterity.interfaces.IDexterityFTI"
      name="Technical Facility"
      />

  <class class=".custom_forms.CustomAddView">
    <require
        permission="cmf.AddPortalContent"
        interface="zope.publisher.interfaces.browser.IBrowserPage"
        />
  </class>

</configure>
```
