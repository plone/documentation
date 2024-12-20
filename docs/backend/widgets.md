---
myst:
  html_meta:
    "description": "Widgets render HTML inputs in a form."
    "property=og:description": "Widgets render HTML inputs in a form."
    "property=og:title": "Widgets"
    "keywords": "Widgets"
---

(backend-widgets-label)=

# Widgets

```{seealso}
See the chapter {doc}`training:mastering-plone/dexterity_reference` from the Mastering Plone 6 Training.
```

Widgets render HTML code for input and parse the input from an HTTP `post` request in Plone.

Plone stores widgets as the `widgets` attribute of a form.
Plone presents widgets as an ordered dict-like `Widgets` class.

Widgets are only available after you call the form's `update()` and `updateWidgets()` methods.
`updateWidgets()` binds widgets to the form's context.
{doc}`vocabularies` defined by their names are resolved at this point.

The Zope publisher will also mangle widget names based on what kind of input the widget accepts.
When an HTTP `post` request comes in, Zope publisher automatically converts `<select>` dropdowns to lists.


## Widget reference

```{tip}
In VS Code editor, you can install the [Plone Snippets](https://marketplace.visualstudio.com/items?itemName=Derico.plone-vs-snippets) extension.
This will give you snippets for most fields, widgets, and autoform directives in Python and XML based schemas.
```

You can find the default widgets in the browser package in `z3c.form`.
The [`z3c.form` documentation](https://z3cform.readthedocs.io/en/latest/widgets/index.html) lists all the default widgets and shows the HTML output of each.

You can find more widgets in the [`plone.app.z3cform`](https://github.com/plone/plone.app.z3cform/tree/master) package.

The main widgets are:

-   Checkbox Widget
-   Radio Widget
-   Text Widget
-   TextArea Widget
-   TextLines Widget
-   Password Widget
-   Select Widget
-   Ordered-Select Widget
-   File Widget
-   File Testing Widget
-   Image Widget
-   Multi Widget
-   Object Widget
-   Button Widget
-   Submit Widget
-   Date Widget
-   DateTime Widget
-   Time Widget
-   DateTime Picker


(backend-widgets-change-a-fields-display-label)=

## Change a field's display mode

A field's widget can be displayed in several modes.

`input`
:   Allows the user to enter data into the field

`display`
:   A read-only indication of the field's value

`hidden`
:   A record of the field's value that is included only in the HTML source


### `plone.autoform` `mode` directive

In the following example, the mode for the `secret` field is set to `hidden` for most forms, but `input` for forms that provide the `IEditForm` interface.

```{code-block} python
:emphasize-lines: 6,7
:linenos:

from plone.supermodel import model
from plone.autoform import directives as form

class IMySchema(model.Schema):

    form.mode(secret="hidden")
    form.mode(IEditForm, secret="input")
    secret = schema.TextLine(
        title="Secret",
        default="Secret stuff (except on edit forms)"
        )
```

The corresponding supermodel XML directive is `form:mode`:

```{code-block} xml
:emphasize-lines: 3

<field type="zope.schema.TextLine"
        name="secret"
        form:mode="z3c.form.interfaces.IForm:hidden z3c.form.interfaces.IEditForm:input">
    <title>Secret</title>
    <description>Secret stuff (except on edit forms)</description>
</field>
```

The mode can be specified briefly, if it should be the same for all forms:

```{code-block} xml
:emphasize-lines: 3

<field type="zope.schema.TextLine"
        name="secret"
        form:mode="hidden">
    <title>Secret</title>
    <description>Secret stuff</description>
</field>
```

In other words, `form:mode` may be either a single mode, or a space-separated list of `<form_interface>:<mode>` pairs.


(backend-widgets-change-a-fields-widget-label)=

## Change a field's widget

You can change the widget that you use for a field in several ways.
This section describes these methods.


### `plone.autoform` `widget` directive

`plone.autoform` builds custom `z3c.form` forms based on a model (schema) of fields, and their widgets and options.
This model is defined as a `zope.schema` based schema, but extra hints can be supplied to control aspects of form display not normally specified in a Zope schema.

By default, `z3c.form` picks a widget based on the type of your field.
You can change the widget using the `widget` directive if you want users to enter or view data in a different format.
For example, you can change the widget for the `human` boolean field to use `yes` and `no` radio buttons instead of its default checkbox:

```{code-block} python
:emphasize-lines: 7
:linenos:

from plone.supermodel import model
from plone.autoform import directives as form
from z3c.form.browser.radio import RadioFieldWidget

class IMySchema(model.Schema):

    form.widget("human", RadioFieldWidget)
    human = schema.Bool(
        title = "Are you human?",
    )
```

You can also pass widget parameters to control attributes of the widget.
For example, you can set a CSS class:

```{code-block} python
:emphasize-lines: 7
:linenos:

from plone.supermodel import model
from plone.autoform import directives as form
from z3c.form.browser.radio import RadioWidget

class IMySchema(model.Schema):

    form.widget("human", klass="annoying")
    human = schema.Bool(
        title = "Are you human?",
    )
```

In supermodel XML, you can specify the widget using a `<form:widget>` tag, which can have its own elements specifying parameters:

```{code-block} xml
:emphasize-lines: 3,4,5

<field name="human" type="zope.schema.TextLine">
    <title>Are you human?</title>
    <form:widget type="z3c.form.browser.radio.RadioWidget">
        <klass>annoying</klass>
    </form:widget>
</field>
```

```{note}
To be included in the XML representation of a schema, you must handle widget parameters through a `WidgetExportImportHandler` utility.
For a generic interface that handles the attributes, see [`z3c.form.browser.interfaces.IHTMLFormElement`](https://github.com/zopefoundation/z3c.form/blob/42f387d105c305757c8c8c3737c39c960f452acb/src/z3c/form/browser/interfaces.py#L147).
```

### Set the widget for `z3c.form` plain forms

You can set a field's `widgetFactory` after fields have been declared in a form's class's body.

```{code-block} python
:emphasize-lines: 23
:linenos:

import zope.schema
import zope.interface

from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget


class IReportSchema(zope.interface.Interface):
    """ Define reporter form fields """

    variables = zope.schema.List(
        title="Variables",
        description="Choose which variables to include in the output report",
        required=False,
        value_type=zope.schema.Choice(vocabulary="output_variables"))


class ReportForm(form.Form):
    """ A form to output a HTML report from chosen parameters """

    fields = z3c.form.field.Fields(IReportSchema)

    fields["variables"].widgetFactory = CheckBoxFieldWidget
```


### Set a widget dynamically with `Form.updateWidgets()`

You can dynamically set the widget type based on external conditions.

```{code-block} python
:emphasize-lines: 9
:linenos:

class EditForm(form.Form):

    label = "Rendering widgets as blocks instead of cells"

    def updateWidgets(self, prefix=""):
        super().updateWidgets(prefix=prefix)

        # Set a custom widget for a field for this form instance only
        self.fields["address"].widgetFactory = BlockDataGridFieldFactory
```


## Access and modify widgets

From time to time, you might need to access widgets to get their information or modify them.
For example, when a user fills out one field, a second field may need to display options dependent on the first field.


### Access a widget

You can access a widget by its field's name.

```{code-block} python
:emphasize-lines: 8
:linenos:

from z3c.form import form


class MyForm(form.Form):

    def update(self):
        super().update()
        widget = form.widgets["my_field_name"] # Get one widget

        for w in widget.items(): print(w) # Dump all widgets
```

To access a widget that's part of a group, you can't use the `updateWidgets()` method.
The groups and their widgets get initialized after the widgets have been updated.
Before that, the `groups` attribute is just a list of group factories.
During the update method though, the groups have been initialized and have their own widget list each.
To access widgets in a group, you have to access the group in the update method:

```python
from z3c.form import form


class MyForm(form.Form):

    def update(self):
        for group in self.groups:
            if "my_field_name" in group.widgets:
                print(group.widgets["my_field_name"].label)
```


### Introspect form widgets

You can customize widget options in the `updateWidgets()` method.
Note that `fieldset` (which is a group) is a `subform`, and this method only affects the current `fieldset`.

```python
from z3c.form import form


class MyForm(form.Form):

    def updateWidgets(self, prefix=""):
        """ Customize widget options before rendering the form. """
        super().updateWidgets(prefix=prefix)

        # Dump out all widgets - note that each <fieldset> is a subform
        # and this function only affects the current fieldset
        for i in self.widgets.items():
            print(i)
```


### Reordering and hiding widgets

With `plone.z3cform`, you can reorder the field widgets by overriding the `update()` method of the form class.

```python
from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE
from plone.z3cform.fieldsets.utils import move


class MyForm(form.Form):

    def update(self):
        super().update()

        # Hide widget "sections"
        self.widgets["sections"].mode = HIDDEN_MODE

        # Set order
        move(self, "fullname", before="*")
        move(self, "username", after="fullname")
```

You also can use `plone.autoform` directives, as in this example used for forms:

```python
from plone.autoform import directives as form
from z3c.form.interfaces import IAddForm, IEditForm


class IFlexibleContent(form.Schema):
    """
    Description of the Example Type
    """

    # Set order
    form.order_before(sections="title")

    # Hide widget "sections"
    form.mode(sections="hidden")

    # set mode
    form.mode(IEditForm, sections="input")
    form.mode(IAddForm, sections="input")

    sections = schema.TextLine(title="Sections")
```


### Dynamic value for widgets

Sometimes you need to pre-load widget values to show when the form is requested.
The following example shows how to do that.

```python
from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope import schema
from zope.interface import Interface


class ICustomSchema(Interface):
    """ Define custom form fields """

    variables = schema.List(
        title="Variables",
        description="Choose which variables to include in the output report",
        required=False,
        value_type=zope.schema.Choice(vocabulary="output_variables"))


class ReportForm(form.Form):
    """ A form to output an HTML report from chosen parameters """

    fields = field.Fields(IReportSchema)

    def updateWidgets(self, prefix=""):
        super().updateWidgets(prefix=prefix)

        if self.request.get("METHOD") == "GET":
          self.widgets["variables"].value = ["02"]  # "02" is an item in the vocabulary
```

In the example, a value is dynamically assigned to the `variables` field.
As this field expects a list as input, the value must be a list.
This will result in a checked option value of `02`.


### Make widgets conditionally required

The following example shows how you can conditionally require widgets.

```python
class ReportForm(form.Form):
    """ A form to output an HTML report from chosen parameters """

    fields = field.Fields(IReportSchema)

    def updateWidgets(self, prefix=""):
        super().updateWidgets(prefix=prefix)

        self.widgets["announce_type"].required = False
```


### Add a CSS class to a widget

To add CSS classes to a widget, you can use the method `addClass()`.
This is useful when you have JavaScript associated with your form:

```python
widget.addClass("myspecialwidgetclass")
```

You can also override the widget CSS class by changing the `klass` attribute for a given widget:

```python
self.widgets["my_widget"].klass = "my-custom-css-class"
```

Or you can use the `plone.autoform` directives:

```{code-block} python
:emphasize-lines: 7
:linenos:

    from plone.supermodel import model
    from plone.autoform import directives as form
    from z3c.form.browser.radio import RadioWidget

    class IMySchema(model.Schema):

        form.widget("human", klass="annoying")
        human = schema.Bool(
            title = "Are you human?",
        )
```

Note that these classes are applied directly to `<input>`, `<select>`, and other HTML controls, and not to the wrapping `<div>` HTML element.


### Dynamically disable or enable a field

To disable a field, you can change a field's `disabled` attribute:

```python
self.widgets["ds_pregu_pers"].disabled = "disabled"
```


## Set widget templates

You might want to customize the template of a widget with custom HTML code.


### Set the template for an individual widget

To set the template for an individual widget, you can copy the existing page template code of the widget.
For basic widgets, you can find the template in the [`z3c.form`](https://github.com/zopefoundation/z3c.form/tree/master/src/z3c/form/browser) source tree.

The following code is an example of a custom template `yourwidget.pt` for an `input` of `type="text"` widget.

```html
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      tal:omit-tag="">
    <input id="" name="" class="" title="" lang="" disabled=""
           readonly="" alt="" tabindex="" accesskey="" size="" maxlength=""
           style="" value="" type="text"
           tal:attributes="id view/id;
                           name view/name;
                           class view/klass;
                           style view/style;
                           title view/title;
                           lang view/lang;
                           onclick view/onclick;
                           ondblclick view/ondblclick;
                           onmousedown view/onmousedown;
                           onmouseup view/onmouseup;
                           onmouseover view/onmouseover;
                           onmousemove view/onmousemove;
                           onmouseout view/onmouseout;
                           onkeypress view/onkeypress;
                           onkeydown view/onkeydown;
                           onkeyup view/onkeyup;
                           value view/value;
                           disabled view/disabled;
                           tabindex view/tabindex;
                           onfocus view/onfocus;
                           onblur view/onblur;
                           onchange view/onchange;
                           readonly view/readonly;
                           alt view/alt;
                           accesskey view/accesskey;
                           onselect view/onselect;
                           size view/size;
                           maxlength view/maxlength;
                           placeholder view/placeholder;
                           autocapitalize view/autocapitalize;" />
</html>
```

Now you can override the template factory in the `updateWidgets()` method of your form class.

```python
from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Z3ViewPageTemplateFile
from z3c.form.interfaces import INPUT_MODE


class AddForm(DefaultAddForm):

    def updateWidgets(self, prefix=None):
        """ """
        # Call parent to set-up initial widget data
        super().updateWidgets(self, prefix=prefix)

        # Please note that the different form modes (show, edit, hide) have to be taken into account.
        if self.widgets["sections"].mode == INPUT_MODE:

            # Modify a widget with certain name for our purposes
            widget = self.widgets["sections"]

            # widget.template is a template factory -
            # Widget.render() will associate later this factory with the widget
            widget.template = Z3ViewPageTemplateFile("templates/yourwidget.pt")
```

You can also interact with your `form` class instance from the widget template:

```html
<!-- Some hidden JSON data for our JavaScript by calling a method on our form class -->
<span style="display:none" tal:content="view/form/getBlockPlanJSON" />
```


### Set a template for your own widget type

You can set the template used by the widget with the `<z3c:widgetTemplate>` ZCML directive.

```xml
<z3c:widgetTemplate
    mode="display"
    widget=".interfaces.INamedFileWidget"
    layer="z3c.form.interfaces.IFormLayer"
    template="file_display.pt"
    />
```


### Widget frame override

You can override widget templates as instructed for `z3c.form`.
`plone.app.z3cform` renders [a frame around each widget](https://github.com/plone/plone.app.z3cform/blob/master/plone/app/z3cform/templates/widget.pt), which usually consists of:

-   Label
-   Required marker
-   Description

You might want to customize this widget frame for your own form.
Below is an example of how to do it.

Copy [`widget.pt`](https://github.com/plone/plone.app.z3cform/blob/master/plone/app/z3cform/templates/widget.pt) to your own package, rename it as `demo-widget.pt`, and edit it.

Then add the following code to `configure.zcml`.
Remember to fix the path of the template according to your own paths.

```xml
<browser:page
    name="ploneform-render-widget"
    for=".demo.IDemoWidget"
    class="plone.app.z3cform.templates.RenderWidget"
    permission="zope.Public"
    template="path/to/template/demo-widget.pt"
    />
```

Then create a new marker interface in Python code.

```python
from zope.interface import Interface


class IDemoWidget(Interface):
    pass
```

Then apply this marker interface to your widgets in `form.update()`.

```python
from zope.interface import alsoProvides

class MyForm(...):

    def update(self):
        super().update()
        # applies custom widget frame to all widgets in this form instance
        for widget in form.widgets.values():
            alsoProvides(widget, IDemoWidget)
```


## Combined widgets

You can combine several widgets into one with `z3c.form.browser.multi.MultiWidget` and `z3c.form.browser.object.ObjectWidget` classes.

The following example shows how to create an input widget with minimum and maximum values.

```python
import zope.interface
import zope.schema
from zope.schema.fieldproperty import FieldProperty

import z3c.form
from z3c.form.object import registerFactoryAdapter


class IMinMax(zope.interface.Interface):
    """ Helper schema for min and max fields """
    min = zope.schema.Float(required=False)
    max = zope.schema.Float(required=False)


@zope.interface.implementer(IMinMax)
class MinMax(object):
    """ Store min-max field values """
    min = FieldProperty(IMinMax["min"])
    max = FieldProperty(IMinMax["max"])


registerFactoryAdapter(IMinMax, MinMax)


class IMyFormSchema(zope.interface.Interface):

    my_combined_field = zope.schema.Object(
        __name__="minmax",
        title=label,
        schema=IMinMax,
        required=False
    )
```

Then you set the `my_combined_field` widget template in `updateWidgets()`:

``` {code-block} python
:emphasize-lines: 13, 14
:linenos:

class MyForm(form.Form):

    fields = field.Fields(IMyFormSchema)

    def updateWidgets(self, prefix=None):
        """
        """

        super().updateWidgets(prefix=prefix)

        # Add min and max CSS class rendering hints
        for widget in self.widgets.values():
            if isinstance(widget, z3c.form.browser.object.ObjectWidget):
                widget.template = Z3ViewPageTemplateFile("minmax.pt")
                zope.interface.alsoProvides(widget, IFilterWidget)
```

Then create the page template `minmax.pt` in the same directory as your form module.
Paste the following code in this file.
The code renders both widgets, {guilabel}`min` and {guilabel}`max`, in a single row.

```html
<div class="min-max-widget"
     tal:define="widget0 python:view.subform.widgets.values()[0];
                 widget1 python:view.subform.widgets.values()[1];">

    <tal:comment>
        <!-- Use label from the first widget -->
    </tal:comment>

    <div class="label">
      <label tal:attributes="for widget0/id">
        <span i18n:translate=""
            tal:content="widget0/label">label</span>
      </label>
    </div>

    <div class="widget-left" tal:define="widget widget0">
        <div tal:content="structure widget/render">
          <input type="text" size="24" value="" />
        </div>
    </div>

    <div class="widget-separator">
    -
    </div>

    <div class="widget-right" tal:define="widget widget1">
        <div class="widget" tal:content="structure widget/render">
          <input type="text" size="24" value="" />
        </div>
    </div>

    <div tal:condition="widget0/error"
         tal:replace="structure widget/error/render">error</div>
    <div class="error" tal:condition="widget1/error"
             tal:replace="structure widget1/error/render">error</div>
    <div style="clear: both"><!-- --></div>
    <input name="field-empty-marker" type="hidden" value="1"
           tal:attributes="name string:${view/name}-empty-marker" />

</div>
```
