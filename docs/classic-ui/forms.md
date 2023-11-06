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


(classic-ui-forms-autoform-label)=
## Controlling form presentation

Directives can be specified in the schema to control aspects of form presentation.

### Changing a field's display mode

A field's widget can be displayed in several "modes":

* input - allows the user to enter data into the field
* display - a read-only indication of the field's value
* hidden - a record of the field's value that is included only in the HTML source

The mode can be controlled using the `mode` directive.

```python
    from plone.supermodel import model
    from plone.autoform import directives as form

    class IMySchema(model.Schema):

        form.mode(secret='hidden')
        form.mode(IEditForm, secret='input')
        secret = schema.TextLine(
            title=u"Secret",
            default=u"Secret stuff (except on edit forms)"
            )
```

In this case the mode for the `secret` field is set to 'hidden' for most forms,
but 'input' for forms that provide the IEditForm interface.

The corresponding supermodel XML directive is `form:mode`:

```xml
    <field type="zope.schema.TextLine"
            name="secret"
            form:mode="z3c.form.interfaces.IForm:hidden z3c.form.interfaces.IEditForm:input">
        <title>Secret</title>
        <description>Secret stuff (except on edit forms)</description>
    </field>
```

The mode can be specified briefly if it should be the same for all forms:

```xml
    <field type="zope.schema.TextLine"
            name="secret"
            form:mode="hidden">
        <title>Secret</title>
        <description>Secret stuff</description>
    </field>
```

In other words, `form:mode` may be either a single mode, or a space-separated
list of form_interface:mode pairs.


### Omitting fields

A field can be omitted entirely from all forms, or from some forms,
using the `omitted` and `no_omit` directives. In this example,
the `dummy` field is omitted from all forms, and the `edit_only`
field is omitted from all forms except those that provide the
IEditForm interface:

```python
    from z3c.form.interfaces import IEditForm
    from plone.supermodel import model
    from plone.autoform import directives as form

    class IMySchema(model.Schema):

        form.omitted('dummy')
        dummy = schema.Text(
            title=u"Dummy"
            )

        form.omitted('edit_only')
        form.no_omit(IEditForm, 'edit_only')
        edit_only = schema.TextLine(
            title = u'Only included on edit forms',
            )
```

In supermodel XML, this can be specified as:

```xml
    <field type="zope.schema.TextLine"
           name="dummy"
           form:omitted="true">
        <title>Dummy</title>
    </field>

    <field type="zope.schema.TextLine"
           name="edit-only"
           form:omitted="z3c.form.interfaces.IForm:true z3c.form.interfaces.IEditForm:false">
        <title>Only included on edit form</title>
    </field>
```

`form:omitted` may be either a single boolean value, or a space-separated
list of form_interface:boolean pairs.


### Re-ordering fields

A field's position in the form can be influenced using the `order_before`
and `order_after` directives. In this example, the `not_last` field
is placed before the `summary` field even though it is defined afterward:

```python
    from plone.supermodel import model
    from plone.autoform import directives as form

    class IMySchema(model.Schema):

        summary = schema.Text(
            title=u"Summary",
            description=u"Summary of the body",
            readonly=True
            )

        form.order_before(not_last='summary')
        not_last = schema.TextLine(
            title=u"Not last",
            )
```

The value passed to the directive may be either '*' (indicating before or after
all fields) or the name of another field. Use `'.fieldname'` to refer to
field in the current schema or a base schema. Prefix with the schema name (e.g.
`'IDublinCore.title'`) to refer to a field in another schema. Use an
unprefixed name to refer to a field in the current or the default schema for
the form.

In supermodel XML, the directives are called `form:before` and `form:after`.
For example:

```xml
    <field type="zope.schema.TextLine"
           name="not_last"
           form:before="*">
        <title>Not last</title>
    </field>
```


### Organizing fields into fieldsets

Fields can be grouped into fieldsets, which will be rendered within an HTML
`<fieldset>` tag. In this example the `footer` and `dummy` fields
are placed within the `extra` fieldset:

```python
    from plone.supermodel import model
    from plone.autoform import directives as form

    class IMySchema(model.Schema):

        model.fieldset('extra',
            label=u"Extra info",
            fields=['footer', 'dummy']
            )

        footer = schema.Text(
            title=u"Footer text",
            )

        dummy = schema.Text(
            title=u"Dummy"
            )
```

In supermodel XML fieldsets are specified by grouping fields within a
`<fieldset>` tag:

```xml
  <fieldset name="extra" label="Extra info">
      <field name="footer" type="zope.schema.TextLine">
          <title>Footer text</title>
      </field>
      <field name="dummy" type="zope.schema.TextLine">
          <title>Dummy</title>
      </field>
  </fieldset>
```


### Changing a field's widget

Usually, z3c.form picks a widget based on the type of your field.
You can change the widget using the `widget` directive if you want
users to enter or view data in a different format. For example,
here we change the widget for the `human` field to use yes/no
radio buttons instead of a checkbox:

```python
    from plone.supermodel import model
    from plone.autoform import directives as form
    from z3c.form.browser.radio import RadioFieldWidget

    class IMySchema(model.Schema):
        form.widget('human', RadioFieldWidget)
        human = schema.Bool(
            title = u'Are you human?',
            )
```

You can also pass widget parameters to control attributes of the
widget. For example, here we keep the default widget, but
set a CSS class:

```python
    from plone.supermodel import model
    from plone.autoform import directives as form
    from z3c.form.browser.radio import RadioWidget

    class IMySchema(model.Schema):
        form.widget('human', klass='annoying')
        human = schema.Bool(
            title = u'Are you human?',
            )
```

In supermodel XML the widget is specified using a `<form:widget>` tag, which
can have its own elements specifying parameters::

```xml
    <field name="human" type="zope.schema.TextLine">
        <title>Are you human?</title>
        <form:widget type="z3c.form.browser.radio.RadioWidget">
            <klass>annoying</klass>
        </form:widget>
    </field>
```

Note: In order to be included in the XML representation of a schema,
widget parameters must be handled by a WidgetExportImportHandler utility.
There is a default one which handles the attributes defined in
`z3c.form.browser.interfaces.IHTMLFormElement`.

### Protect a field with a permission

By default, fields are included in the form regardless of the user's
permissions. Fields can be protected using the `read_permission`
and `write_permission` directives. The read permission is checked when
the field is in display mode, and the write permission is checked when
the field is in input mode. The permission should be given with its
Zope 3-style name (i.e. cmf.ManagePortal rather than 'Manage portal').

In this example, the `secret` field is protected by the
`cmf.ManagePortal` permission as both a read and write permission.
This means that in both display and input modes, the field will
only be included in the form for users who have that permission:

```python
    from plone.supermodel import model
    from plone.autoform import directives as form

    class IMySchema(model.Schema):
        form.read_permission(secret='cmf.ManagePortal')
        form.write_permission(secret='cmf.ManagePortal')
        secret = schema.TextLine(
            title = u'Secret',
            )
```

In supermodel XML the directives are `security:read-permission` and
`security:write-permission`:

```xml
    <field type="zope.schema.TextLine"
           name="secret"
           security:read-permission="cmf.ManagePortal"
           security:write-permission="cmf.ManagePortal">
        <title>Secret</title>
    </field>
```

## Display Forms


Sometimes rather than rendering a form for data entry, you want to display
stored values based on the same schema. This can be done using a "display form."
The display form renders each field's widget in "display mode," which means
that it shows the field value in read-only form rather than as a form input.

To use the display form, create a view that extends `WidgetsView` like this:

```python
    from plone.autoform.view import WidgetsView

    class MyView(WidgetsView):
        schema = IMySchema
        additionalSchemata = (ISchemaOne, ISchemaTwo,)

        # ...
```

To render the form, do not override `__call__()`. Instead, either implement
the `render()` method, set an `index` attribute to a page template or
other callable, or use the `template` attribute of the `<browser:page />`
ZCML directive when registering the view.

In the template, you can use the following variables:

* `view/w` is a dictionary of all widgets, including those from non-default
  fieldsets (by contrast, the `widgets` variable contains only those
  widgets in the default fieldset). The keys are the field names, and the
  values are widget instances. To render a widget (in display mode), you can
  do `tal:replace="structure view/w/myfield/render" />`.
* `view/fieldsets` is a dictionary of all fieldsets (not including the
  default fieldset, i.e. those widgets not placed into a fieldset). They keys
  are the fieldset names, and the values are the fieldset form instances,
  which in turn have variables like `widgets` given a list of all widgets.


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
