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
See the chapter {ref}`training:dexterity-reference-label` from the Mastering Plone 6 Training.
```

(backend-widgets-autoform-label)=

Widgets are responsible for:

1. rendering HTML code for input
2. parsing HTTP post input

Widgets are stored as the `widgets` attribute of a form. It's presented by an ordered dict-like `Widgets` class.

Widgets are only available after the form's `update()` and `updateWidgets()` methods have been called. `updateWidgets()` will bind widgets to the form context. For example, vocabularies defined by name are resolved at this point.

The Zope publisher will also mangle widget names based on what kind of input the widget takes. When an HTTP `POST` request comes in, Zope publisher automatically converts `<select>` dropdowns to lists.

## Widget reference
You can find the default widgets in the browser package in ``z3c.form``. The ``z3c.form`` [documentation](https://z3cform.readthedocs.io/en/latest/widgets/index.html) has a listing of all the default widgets that shows the HTML output of each.

More widgets can be found in the [plone.app.z3cform](https://github.com/plone/plone.app.z3cform/tree/master) package.

The main widgets are:

- Checkbox Widget
- Radio Widget
- Text Widget
- TextArea Widget
- TextLines Widget
- Password Widget
- Select Widget
- Ordered-Select Widget
- File Widget
- File Testing Widget
- Image Widget
- Multi Widget
- Object Widget
- Button Widget
- Submit Widget
- Date Widget
- DateTime Widget
- Time Widget
- DateTime Picker

## Changing a field's widget

### Using plone.autoform `widget` directive

``plone.autoform`` builds custom `z3c.form` forms based on a model (schema) of what fields to include and what widgets and options should be used for each field. This model is defined as a `zope.schema` based schema, but extra hints can be supplied to control aspects of form display not normally specified in a Zope schema.

Usually, z3c.form picks a widget based on the type of your field. You can change the widget using the ``widget`` directive if you want users to enter or view data in a different format. For example, change the widget for the ``human`` field to use yes/no radio buttons instead of a checkbox:

```{code-block} python
:emphasize-lines: 7
:linenos:

    from plone.supermodel import model
    from plone.autoform import directives as form
    from z3c.form.browser.radio import RadioFieldWidget

    class IMySchema(model.Schema):

        form.widget('human', RadioFieldWidget)
        human = schema.Bool(
            title = u'Are you human?',
            )
```
You can also pass widget parameters to control attributes of the widget. For example, set a CSS class:

```{code-block} python
:emphasize-lines: 7
:linenos:

    from plone.supermodel import model
    from plone.autoform import directives as form
    from z3c.form.browser.radio import RadioWidget

    class IMySchema(model.Schema):

        form.widget('human', klass='annoying')
        human = schema.Bool(
            title = u'Are you human?',
            )
```
In supermodel XML the widget is specified using a ``<form:widget>`` tag, which can have its own elements specifying parameters:

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
In order to be included in the XML representation of a schema, widget parameters must be handled by a WidgetExportImportHandler utility.
There is a default one which handles the attributes defined in ``z3c.form.browser.interfaces.IHTMLFormElement``.
```

### Setting widget for z3c.form plain forms

You can set field’s ``widgetFactory`` after fields have been declared in form class body.

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

### Setting widget dynamically ``Form.updateWidgets()``

Widget type can be set dynamically based on external conditions.

```{code-block} python
:emphasize-lines: 9
:linenos:

class EditForm(form.Form):

    label = "Rendering widgets as blocks instead of cells"

    def updateWidgets(self, prefix=""):
        super().updateWidgets(prefix=prefix)

        # Set a custom widget for a field for this form instance only
        self.fields['address'].widgetFactory = BlockDataGridFieldFactory
```

## Accessing and modifying widgets

### Accessing a widget
A widget can be accessed by its field’s name.

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

If you want to access a widget that's part of a group, you can't use the ``updateWidgets()`` method. The groups and their widgets get initialized after the widgets have been updated. Before that, the groups variable is just a list of group factories. During the update method though, the groups have been initialized and have their own widget list each. For accessing widgets there, you have to access the group in the update method like so:

```{code-block} python
:linenos:

from z3c.form import form


class MyForm(form.Form):

    ...

    def update(self):
        for group in self.groups:
            if "my_field_name" in group.widgets:
                print(group.widgets['my_field_name'].label)

```

### Introspecting form widgets
You can customize widget options in the ``updateWidgets()`` method. Note that `fieldset` (Group) is a `subform` and this method only concerns to the current `fieldset`.

```{code-block} python
:linenos:

from z3c.form import form


class MyForm(form.Form):

    def updateWidgets(self, prefix=""):
        """ Customize widget options before rendering the form. """
        super().updateWidgets(prefix=prefix)

        # Dump out all widgets - note that each <fieldset> is a subform
        # and this function only concerns the current fieldset
        for i in self.widgets.items():
            print(i)
```

### Reordering and hiding widgets
With ``plone.z3cform `` you can reorder the field widgets by overriding the ``update()`` method of the form class.

```{code-block} python
:linenos:

from z3c.form import form
from z3c.form.interfaces import HIDDEN_MODE
from plone.z3cform.fieldsets.utils import move


class MyForm(form.Form):

    def update(self):
        super().update()

        # Hide widget 'sections'
        self.widgets["sections"].mode = HIDDEN_MODE

        # Set order
        move(self, 'fullname', before='*')
        move(self, 'username', after='fullname')
```

 You also can use ``plone.autoform`` directives, in this example used for dexterity forms:

```{code-block} python
:linenos:

from plone.autoform import directives as form
from z3c.form.interfaces import IAddForm, IEditForm


class IFlexibleContent(form.Schema):
    """
    Description of the Example Type
    """

    # Set order
    form.order_before(sections='title')

    # Hide widget 'sections'
    form.mode(sections='hidden')

    # set mode  
    form.mode(IEditForm, sections='input')
    form.mode(IAddForm, sections='input')

    sections = schema.TextLine(title="Sections")

```

### Dynamic value for widgets

Sometimes you need to pre-load widget values to be shown when the form is requested:


```{code-block} python
:linenos:

from z3c.form import field
from z3c.form import form
from z3c.form.browser.checkbox import CheckBoxFieldWidget

from zope import schema
from zope.interface import Interface


class ICustomSchema(Interface):
    """ Define a custom form fields """

    variables = schema.List(
        title="Variables",
        description="Choose which variables to include in the output report",
        required=False,
        value_type=zope.schema.Choice(vocabulary="output_variables"))


class ReportForm(form.Form):
    """ A form to output a HTML report from chosen parameters """

    fields = field.Fields(IReportSchema)

    def updateWidgets(self, prefix=""):
        super().updateWidgets(prefix=prefix)

        if self.request.get("METHOD") == "GET":
          self.widgets["variables"].value = ["02"]  # being "02" a item in the vocabulary
```
In the example, a value is dynamically assigned to the variables field. As this field expects a list as input, the value has to be a list. This will result in a checked option value ``02"``.

### Making widgets required conditionally

```{code-block} python
:linenos:

class ReportForm(form.Form):
    """ A form to output a HTML report from chosen parameters """

    fields = field.Fields(IReportSchema)

    def updateWidgets(self, prefix=""):
        super().updateWidgets(prefix=prefix)

        self.widgets["announce_type"].required = False
```

### Adding a CSS class
Widgets have a method `addClass()` to add extra CSS classes. This is useful if you have JavaScript/JQuery associated with your special form:

```{code-block} python
widget.addClass("myspecialwidgetclass")
```

You can also override the widget CSS class by changing the `klass` attribute:

```{code-block} python
self.widgets["my_widget"].klass = "my-custom-css-class"
```

Or using the `plone.autoform` directives:

```{code-block} python
:emphasize-lines: 7
:linenos:

    from plone.supermodel import model
    from plone.autoform import directives as form
    from z3c.form.browser.radio import RadioWidget

    class IMySchema(model.Schema):

        form.widget('human', klass='annoying')
        human = schema.Bool(
            title = u'Are you human?',
            )
```

Note that these classes are directly applied to `<input>`, `<select>`, etc. itself, and not to the wrapping `<div>` element.

### Dynamically disable or enable a field

As you can imagine disabling a field can be done by changing an attribute:

```{code-block} python
    self.widgets["ds_pregu_pers"].disabled = "disabled"
```

## Setting widget templates
You might want to customize the template of a widget to have custom HTML code for a specific use case.

### Setting the template of an individual widget
First copy the existing page template code of the widget. For basic widgets you can find the template in the [`z3c.form`](https://github.com/zopefoundation/z3c.form/tree/master/src/z3c/form/browser) source tree.

`yourwidget.pt` (text widget copied over an example text)

``` {code-block} html
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
Now you can override the template factory in the updateWidgets() method of your form class

```{code-block} python
:linenos:

from zope.browserpage.viewpagetemplatefile import ViewPageTemplateFile as Z3ViewPageTemplateFile
from z3c.form.interfaces import INPUT_MODE

class AddForm(DefaultAddForm):

    def updateWidgets(self, prefix=None):
        """ """
        # Call parent to set-up initial widget data
        super().updateWidgets(self, prefix=prefix)

        # Note we need to be discreet to different form modes (view, edit, hidden)
        if self.fields["sections"].mode == INPUT_MODE:

            # Modify a widget with certain name for our purposes
            widget = self.widgets["sections"]

            # widget.template is a template factory -
            # Widget.render() will associate later this factory with the widget
            widget.template = Z3ViewPageTemplateFile("templates/sections.pt")

```
You can also interact with your `form` class instance from the widget template:

```{code-block} html
<!-- Some hidden JSON data for our Javascripts by calling a method on our form class -->
<span style="display:none" tal:content="view/form/getBlockPlanJSON" />
```


### Setting template for your own widget type

You can set the template used by the widget with the `<z3c:widgetTemplate>` ZCML directive

```{code-block} xml
    <z3c:widgetTemplate
        mode="display"
        widget=".interfaces.INamedFileWidget"
        layer="z3c.form.interfaces.IFormLayer"
        template="file_display.pt"
        />
```

### Widget frame override

You can override widget templates as instructed for ``z3c.form``.
``plone.app.z3cform`` renders [a frame around each widget](<https://github.com/plone/plone.app.z3cform/blob/master/plone/app/z3cform/templates/widget.pt>)
which usually consists of

* Label
* Required marker
* Description

You might want to customize this widget frame for your own form.
Below is an example how to do it.

Copy [widget.pt](<https://github.com/plone/plone.app.z3cform/blob/master/plone/app/z3cform/templates/widget.pt>) to your own package and customize it in way you wish.

Add the following to ``configure.zcml``

```{code-block} xml
    <browser:page
        name="ploneform-render-widget"
        for=".demo.IDemoWidget"
        class="plone.app.z3cform.templates.RenderWidget"
        permission="zope.Public"
        template="demo-widget.pt"
        />

```
Create a new marker interface in Python code

```{code-block} python
:linenos:

    from zope.interface import Interface

    class IDemoWidget(Interface):
        pass
```

Then apply this marker interface to your widgets in ``form.update()``

```{code-block} python
:linenos:

    from zope.interface import alsoProvides

    class MyForm(...):
        ...
        def update(self):
            super().update()
            # applies custom widget frame to all widgets in this form instance
            for widget in form.widgets.values():
                alsoProvides(widget, IDemoWidget)
```

## Combined widgets
You can combine several widgets to one with`` z3c.form.browser.multil.MultiWidget`` and ``z3c.form.browser.object.ObjectWidget`` classes.

Example how to create a min max input widget.

Python code to setup the widget:

```{code-block} python
:linenos:

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
    min = FieldProperty(IMinMax['min'])
    max = FieldProperty(IMinMax['max'])


registerFactoryAdapter(IMinMax, MinMax)

....

field = zope.schema.Object(
    __name__='mixmax',
    title=label,
    schema=IMinMax,
    required=False
)
```

Then you do some widget marking in ``updateWidgets()``:

```{code-block} python
:linenos:

def updateWidgets(self):
    """
    """

    super(FilteringGroup, self).updateWidgets()

    # Add min and max CSS class rendering hints
    for widget in self.widgets.values():
        if isinstance(widget, z3c.form.browser.object.ObjectWidget):
            widget.template = Z3ViewPageTemplateFile("templates/minmax.pt")
            widget.addClass("min-max-widget")
            zope.interface.alsoProvides(widget, IFilterWidget)
```

And then the page template which renders both 0. widget (min) and 1. widget (max) on the same line.

``` {code-block} html
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
