---
myst:
  html_meta:
    "description": "Fields are objects that have properties and types, and comprise a schema."
    "property=og:description": "Fields are objects that have properties and types, and comprise a schema."
    "property=og:title": "Fields"
    "keywords": "Fields, widgets, schema, autoform, supermodel, XML"
---

(backend-fields-label)=

# Field, widget, schema

```{todo}
Contribute to this documentation!
See issue [Backend > Fields needs content](https://github.com/plone/documentation/issues/1305).
```

(backend-fields-schema-label)=

## schema


(backend-fields-schema-autoform-label)=

### autoform (directives) schema ordering, filtering, and permissions


(backend-fields-supermodel-label)=

## supermodel (xml)


(backend-fields-supermodel-autoform-label)=

### autoform (directives) supermodel ordering, filtering, and permissions


(backend-fields-reference-label)=

## Reference

This reference documents all fields, widgets, directives that you can use with content types.
Content types are often called dexterity types which refers to the rework of the content type concept by dexterity and abandoning the Archetypes system.

```{seealso}
[Example content type](https://github.com/collective/example.contenttype) A Plone content type with all available fields
``````


### Fields included in Plone

This is a schema with examples for all field-types that are shipped with Plone by default.
They are arranged in fieldsets:

Default

: Textline, Text, Boolean, Richtext (html), Email

Number fields

: Integer, Float

Date and time fields

: Datetime,
Date,
Time,
Timedelta

Choice and Multiple Choice fields

: Choice,
Choice with radio widget,
Choice with Select2 widget,
Choice with named vocabulary,
List,
List with checkboxes,
List with Select2 widget,
List with values from a named vocabulary but open to additions,
Tuple,
Set,
Set with checkboxes

Relation fields

: Relationchoice, Relationlist

File fields

: File, Image

Other fields

: Uri, Sourcetext, Ascii, Bytesline, Asciiline, Pythonidentifier, Dottedname, Dict, Dict with Choice

% TODO Check from time to time the completnes of implementation of widgets in Volto (Time, Timedelta, Dict , using a callable for basePath in relationfields.


```{code-block} python
:linenos:

from plone.app.multilingual.browser.interfaces import make_relation_root_path
from plone.app.textfield import RichText
from plone.app.z3cform.widget import AjaxSelectFieldWidget
from plone.app.z3cform.widget import RelatedItemsFieldWidget
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.dexterity.content import Container
from plone.namedfile.field import NamedBlobFile
from plone.namedfile.field import NamedBlobImage
from plone.schema.email import Email
from plone.supermodel import model
from plone.supermodel.directives import fieldset
from plone.supermodel.directives import primary
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from z3c.form.browser.radio import RadioFieldWidget
from z3c.relationfield.schema import Relation
from z3c.relationfield.schema import RelationChoice
from z3c.relationfield.schema import RelationList
from zope import schema
from zope.interface import implementer


class IExample(model.Schema):
    """Dexterity-Schema with all field-types."""

    # The most used fields
    # textline, text, bool, richtext, email

    fieldset(
        'numberfields',
        label='Number fields',
        fields=('int_field', 'float_field'),
    )

    fieldset(
        'datetimefields',
        label='Date and time fields',
        fields=('datetime_field', 'date_field', 'time_field', 'timedelta_field'),
    )

    fieldset(
        'choicefields',
        label='Choice and Multiple Choice fields',
        fields=(
            'choice_field',
            'choice_field_radio',
            'choice_field_select',
            'choice_field_voc',
            'list_field',
            'list_field_checkbox',
            'list_field_select',
            'list_field_voc_unconstrained',
            'tuple_field',
            'set_field',
            'set_field_checkbox',
        ),
    )

    fieldset(
        'relationfields',
        label='Relation fields',
        fields=('relationchoice_field', 'relationlist_field'),
    )

    fieldset(
        'filefields',
        label='File fields',
        fields=('file_field', 'image_field'),
    )

    fieldset(
        'otherfields',
        label='Other fields',
        fields=(
            'uri_field',
            'sourcetext_field',
            'ascii_field',
            'bytesline_field',
            'asciiline_field',
            'pythonidentifier_field',
            'dottedname_field',
            'dict_field',
            'dict_field_with_choice',
        ),
    )

    primary('title')
    title = schema.TextLine(
        title='Primary Field (Textline)',
        required=True,
    )

    text_field = schema.Text(
        title='Text Field',
        required=False,
        missing_value='',
    )

    textline_field = schema.TextLine(
        title='Textline field',
        description='A simple input field',
        required=False,
    )

    bool_field = schema.Bool(
        title='Boolean field',
        required=False,
    )

    choice_field = schema.Choice(
        title='Choice field',
        values=['One', 'Two', 'Three'],
        required=True,
    )

    directives.widget(choice_field_radio=RadioFieldWidget)
    choice_field_radio = schema.Choice(
        title='Choice field with radio boxes',
        values=['One', 'Two', 'Three'],
        required=True,
    )

    choice_field_voc = schema.Choice(
        title='Choicefield with values from named vocabulary',
        vocabulary='plone.app.vocabularies.PortalTypes',
        required=False,
    )

    directives.widget(choice_field_select=SelectFieldWidget)
    choice_field_select = schema.Choice(
        title='Choicefield with select2 widget',
        vocabulary='plone.app.vocabularies.PortalTypes',
        required=False,
    )

    list_field = schema.List(
        title='List field',
        value_type=schema.Choice(
            values=['Beginner', 'Advanced', 'Professional'],
        ),
        required=False,
        missing_value=[],
    )

    directives.widget(list_field_checkbox=CheckBoxFieldWidget)
    list_field_checkbox = schema.List(
        title='List field with checkboxes',
        value_type=schema.Choice(
            values=['Beginner', 'Advanced', 'Professional'],
        ),
        required=False,
        missing_value=[],
    )

    directives.widget(list_field_select=SelectFieldWidget)
    list_field_select = schema.List(
        title='List field with select widget',
        value_type=schema.Choice(
            values=['Beginner', 'Advanced', 'Professional'],
        ),
        required=False,
        missing_value=[],
    )

    list_field_voc_unconstrained = schema.List(
        title='List field with values from vocabulary but not constrained to them.',
        value_type=schema.TextLine(),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'list_field_voc_unconstrained',
        AjaxSelectFieldWidget,
        vocabulary='plone.app.vocabularies.Users',
    )

    tuple_field = schema.Tuple(
        title='Tuple field',
        value_type=schema.Choice(
            values=['Beginner', 'Advanced', 'Professional'],
        ),
        required=False,
        missing_value=(),
    )

    set_field = schema.Set(
        title='Set field',
        value_type=schema.Choice(
            values=['Beginner', 'Advanced', 'Professional'],
        ),
        required=False,
        missing_value=set(),
    )

    directives.widget(set_field_checkbox=CheckBoxFieldWidget)
    set_field_checkbox = schema.Set(
        title='Set field with checkboxes',
        value_type=schema.Choice(
            values=['Beginner', 'Advanced', 'Professional'],
        ),
        required=False,
        missing_value=set(),
    )

    # File fields
    image_field = NamedBlobImage(
        title='Image field',
        description='A upload field for images',
        required=False,
    )

    file_field = NamedBlobFile(
        title='File field',
        description='A upload field for files',
        required=False,
    )

    # Date and Time fields
    datetime_field = schema.Datetime(
        title='Datetime field',
        description='Uses a date and time picker',
        required=False,
    )

    date_field = schema.Date(
        title='Date field',
        description='Uses a date picker',
        required=False,
    )

    time_field = schema.Time(
        title='Time field',
        required=False,
    )

    timedelta_field = schema.Timedelta(
        title='Timedelta field',
        required=False,
    )

    # Relation Fields
    relationchoice_field = RelationChoice(
        title='Relationchoice field',
        vocabulary='plone.app.vocabularies.Catalog',
        required=False,
    )
    directives.widget(
        'relationchoice_field',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Document'],
            'basePath': make_relation_root_path,
        },
    )

    relationlist_field = RelationList(
        title='Relationlist Field',
        default=[],
        value_type=RelationChoice(vocabulary='plone.app.vocabularies.Catalog'),
        required=False,
        missing_value=[],
    )
    directives.widget(
        'relationlist_field',
        RelatedItemsFieldWidget,
        pattern_options={
            'selectableTypes': ['Document'],
            'basePath': make_relation_root_path,
        },
    )

    # Number fields
    int_field = schema.Int(
        title='Integer Field (e.g. 12)',
        description='Allocated (maximum) number of objects',
        required=False,
    )

    float_field = schema.Float(
        title='Float field (e.g. 12.2)',
        required=False,
    )

    # Text fields
    email_field = Email(
        title='Email field',
        description='A simple input field for a email',
        required=False,
    )

    uri_field = schema.URI(
        title='URI field',
        description='A simple input field for a URLs',
        required=False,
    )

    richtext_field = RichText(
        title='RichText field',
        description='This uses a richtext editor.',
        max_length=2000,
        required=False,
    )

    sourcetext_field = schema.SourceText(
        title='SourceText field',
        required=False,
    )

    ascii_field = schema.ASCII(
        title='ASCII field',
        required=False,
    )

    bytesline_field = schema.BytesLine(
        title='BytesLine field',
        required=False,
    )

    asciiline_field = schema.ASCIILine(
        title='ASCIILine field',
        required=False,
    )

    pythonidentifier_field = schema.PythonIdentifier(
        title='PythonIdentifier field',
        required=False,
    )

    dottedname_field = schema.DottedName(
        title='DottedName field',
        required=False,
    )

    dict_field = schema.Dict(
        title='Dict field',
        required=False,
        key_type=schema.TextLine(
            title='Key',
            required=False,
        ),
        value_type=schema.TextLine(
            title='Value',
            required=False,
        ),
    )

    dict_field_with_choice = schema.Dict(
        title='Dict field with key and value as choice',
        required=False,
        key_type=schema.Choice(
            title='Key',
            values=['One', 'Two', 'Three'],
            required=False,
        ),
        value_type=schema.Set(
            title='Value',
            value_type=schema.Choice(
                values=['Beginner', 'Advanced', 'Professional'],
            ),
            required=False,
            missing_value={},
        ),
    )


@implementer(IExample)
class Example(Container):
    """Example instance class"""

```

```{seealso}
- [Dexterity Developer Manual](https://5.docs.plone.org/external/plone.app.dexterity/docs/index.html)
- [All available Fields](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/fields.html#field-types)
- [Schema-driven types with Dexterity](https://5.docs.plone.org/external/plone.app.dexterity/docs/schema-driven-types.html#schema-driven-types)
- [The standard behaviors](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/standard-behaviours.html)
```

### How fields look like

#### Backend

This is how these fields look like when editing content in the backend:

```{figure} /_static/backend/fields/dexterity_reference_default_fields.png
:alt: Default fields

Default fields
```

```{figure} /_static/backend/fields/dexterity_reference_number_fields.png
:alt: Number fields

Number fields
```

```{figure} /_static/backend/fields/dexterity_reference_datetime_fields.png
:alt: Date and time fields

Date and time fields
```

```{figure} /_static/backend/fields/dexterity_reference_choice_and_list_fields.png
:alt: Choice and multiple choice fields

Choice and multiple choice fields
```

```{figure} /_static/backend/fields/dexterity_reference_file_fields.png
:alt: File fields

File fields
```

```{figure} /_static/backend/fields/dexterity_reference_relation_fields.png
:alt: Reference fields

Reference fields
```

```{figure} /_static/backend/fields/dexterity_reference_other_fields.png
:alt: Other fields including the dict field

Other fields including the dict field
```

#### Frontend

This is how these fields look like when editing content in Volto:

```{figure} /_static/backend/fields/dexterity_reference_volto_default_fields.png
:alt: Default fields

Default fields
```

```{figure} /_static/backend/fields/dexterity_reference_volto_number_fields.png
:alt: Number fields

Number fields
```

```{figure} /_static/backend/fields/dexterity_reference_volto_datetime_fields.png
:alt: Date and time fields

Date and time fields
```

```{figure} /_static/backend/fields/dexterity_reference_volto_choice_and_list_fields.png
:alt: Choice and multiple choice fields

Choice and multiple choice fields
```

```{figure} /_static/backend/fields/dexterity_reference_volto_file_fields.png
:alt: File fields

File fields
```

```{figure} /_static/backend/fields/dexterity_reference_volto_relation_fields.png
:alt: Reference fields

Reference fields
```

```{figure} /_static/backend/fields/dexterity_reference_volto_other_fields.png
:alt: Other fields including the dict field

Other fields
```

### 3rd party fields

- To control the available values of other fields or hide/show them based on user input use the [Masterselect Field](https://pypi.org/project/plone.formwidget.masterselect/).
- For spam-protection use [collective.z3cform.norobots](https://pypi.org/project/collective.z3cform.norobots/).
- Color-Picker [collective.z3cform.colorpicker](https://github.com/collective/collective.z3cform.colorpicker)
- There is no Computedfield but most use-cases can be achieved with a readonly-field and a property. See the [discussion](https://community.plone.org/t/computed-field-for-dexterity/11405)

(dexterity-reference-datagridfield-label)=

### Datagrid Field

The [datagrid field](https://pypi.org/project/collective.z3cform.datagridfield/) allows you to enter multiple values at once as rows in a table. Each row is a sub form defined in a separate schema.

```{note}
The *datagrid field* is for Plone Classic. See the *mixedfield* below, if you are working with Plone.
```

Here is an example:

```{code-block} python
:linenos:

from collective.z3cform.datagridfield import DataGridFieldFactory
from collective.z3cform.datagridfield import DictRow
from plone.app.z3cform.widget import SelectFieldWidget
from plone.autoform import directives
from plone.supermodel import model
from zope import schema
from zope.interface import Interface


class IMyRowSchema(Interface):

    choice_field = schema.Choice(
        title='Choice Field',
        vocabulary='plone.app.vocabularies.PortalTypes',
        required=False,
        )
    directives.widget('objective', SelectFieldWidget)

    textline_field = schema.TextLine(
        title='Textline field',
        required=False,
        )

    bool_field = schema.Bool(
        title='Boolean field',
        required=False,
    )


class IExampleWithDatagrid(model.Schema):

    title = schema.TextLine(title='Title', required=True)

    datagrid_field = schema.List(
        title='Datagrid field',
        value_type=DictRow(title='Table', schema=IMyRowSchema),
        default=[],
        required=False,
    )
    directives.widget('datagrid_field', DataGridFieldFactory)
```

The edit-form looks like this:

```{figure} /_static/backend/fields/dexterity_reference_datagridfield_edit.png

```

The output looks like this:

```{figure} /_static/backend/fields/dexterity_reference_datagridfield_view.png

```

### mixedfield

The mixedfield empowers your user to create a list of objects of mixed value types sharing the same schema.
If you are familliar with the Plone Classic datagrid field this is the complementary field / widget combo for Plone.
**mixedfield** is a combination of a Plone Classic JSONField and a widget for Plone. Nothing new, just a term to talk about linking backend and frontend.

Example is a custom history:

```{figure} /_static/backend/fields/mixedfield_view.png
:alt: view mixedfield values
```

#### Backend

Add a field _history_field_ to your content type schema.

```{code-block} python
:emphasize-lines: 1-6, 33, 37, 38
:linenos:

MIXEDFIELD_SCHEMA = json.dumps(
    {
        'type': 'object',
        'properties': {'items': {'type': 'array', 'items': {'type': 'object', 'properties': {}}}},
    }
)

class IExample(model.Schema):
    """Dexterity-Schema"""

    fieldset(
        'datagrid',
        label='Datagrid field',
        fields=(
            # 'datagrid_field',
            'mixed_field',
            ),
    )

    primary('title')
    title = schema.TextLine(
        title='Primary Field (Textline)',
        description='zope.schema.TextLine',
        required=True,
        )

    description = schema.TextLine(
        title='Description (Textline)',
        description='zope.schema.TextLine',
        required=False,
        )

    history_field = JSONField(
        title='Mixedfield: datagrid field for Plone',
        required=False,
        schema=MIXEDFIELD_SCHEMA,
        widget='history_widget',
        default={'items': []},
        missing_value={'items': []},
        )
```

#### Frontend

Provide a widget in your favorite add-on with a schema of elementary fields you need.

```{code-block} jsx
:emphasize-lines: 3,37,39
:linenos:

import React from 'react';

import ObjectListWidget from '@plone/volto/components/manage/Widgets/ObjectListWidget';

const ItemSchema = {
    title: 'History-Entry',
    properties: {
        historydate: {
            title: 'Date',
            widget: 'date',
        },
        historytopic: {
            title: 'What',
        },
        historyversion: {
            title: 'Version',
        },
        historyauthor: {
            title: 'Who',
        },
    },
    fieldsets: [
        {
            id: 'default',
            title: 'History-Entry',
            fields: [
                'historydate',
                'historytopic',
                'historyversion',
                'historyauthor',
            ],
        },
    ],
    required: [],
};

const HistoryWidget = (props) => {
    return (
        <ObjectListWidget
            schema={ItemSchema}
            {...props}
            value={props.value?.items || props.default?.items || []}
            onChange={(id, value) => props.onChange(id, { items: value })}
        />
    );
};

export default HistoryWidget;
```

Keeping this example as simple as possible we skipped the localization. Please see Volto documentation for details.

Register this widget for the backend field of your choice in your **apps** configuration {file}`config.js`.
The following config code registers the custom Plone _HistoryWidget_ for Plone Classic fields with widget "history_widget".

```{code-block} js
:emphasize-lines: 12
:linenos:

import { HistoryWidget } from '@rohberg/voltotestsomevoltothings/components';

// All your imports required for the config here BEFORE this line
import '@plone/volto/config';

export default function applyConfig(config) {
    config.settings = {
        ...config.settings,
        supportedLanguages: ['en', 'de', 'it'],
        defaultLanguage: 'en',
    };
    config.widgets.widget.history_widget = HistoryWidget;

    return config;
}
```

Please be sure to use `plone.restapi` version >= 7.3.0. If you cannot upgrade `plone.restapi` then a registration per field id instead of a registration per field widget name is needed.

```js
export default function applyConfig(config) {
  config.widgets.id.history_field = HistoryWidget;
  return config;
}
```

The user can now edit the values of the new field _history_field_.

Thats what you did to accomplish this:

- You added a new field of type JSONField with widget "history_widget" and default schema to your content type schema.
- You registered the custom Plone widget for widget name "history_widget".

```{figure} /_static/backend/fields/mixedfield_edit.png
:alt: edit mixedfield values
```

A view ({file}`ExampleView`) of the content type integrates a component to display the values of the field _history_field_.

```{code-block} jsx
:emphasize-lines: 40
:linenos:

import React from 'react';
import moment from 'moment';
import { Container, Table } from 'semantic-ui-react';

const MyHistory = ({ history }) => {
    return (
        _CLIENT__ && (
        <Table celled className="history_list">
            <Table.Header>
            <Table.Row>
                <Table.HeaderCell>Date</Table.HeaderCell>
                <Table.HeaderCell>What</Table.HeaderCell>
                <Table.HeaderCell>Version</Table.HeaderCell>
                <Table.HeaderCell>Who</Table.HeaderCell>
            </Table.Row>
            </Table.Header>

            <Table.Body>
            {history?.items?.map((item) => (
                <Table.Row>
                <Table.Cell>
                    {item.historydate && moment(item.historydate).format('L')}
                </Table.Cell>
                <Table.Cell>{item.historytopic}</Table.Cell>
                <Table.Cell>{item.historyversion}</Table.Cell>
                <Table.Cell>{item.historyauthor}</Table.Cell>
                </Table.Row>
            ))}
            </Table.Body>
        </Table>
        )
    );
};

const ExampleView = ({ content }) => {
    return (
        <Container>
        <h2>I am an ExampleView</h2>
        <h3>History</h3>
        <MyHistory history={content.history_field} />
        </Container>
    );
 };

 export default ExampleView;
```

Et voilà.

```{figure} /_static/backend/fields/mixedfield_view.png
:alt: view mixedfield values
```


### Widgets

Volto makes suggestions which widget to use, based on the fields type, backend widget and id.

All widgets are listed here:

- [frontend widgets](https://6.docs.plone.org/storybook)
- [backend widgets](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/widgets.html)

#### Determine frontend widget

If you want to register a frontend widget for your field, you can define your field such as:

```python
directives.widget(
    "specialfield",
    frontendOptions={
        "widget": "specialwidget"
    })
specialfield = schema.TextLine(title="Field with special frontend widget")
```

Then register your frontend widget in your apps configuration.

```jsx
import { MySpecialWidget } from './components';

const applyConfig = (config) => {
  config.widgets.widget.specialwidget = MySpecialWidget;
  return config;
}
```

You can also pass additional props to the frontend widget using the `widgetProps` key:

```python
directives.widget(
    "specialfield",
    frontendOptions={
        "widget": "specialwidget",
        "widgetProps": {"isLarge": True, "color": "red"}
    })
specialfield = schema.TextLine(title="Field with special frontend widget")
```

The props will be injected into the corresponding widget component, configuring it as specified.


### Directives

Directives can be placed anywhere in the class body (annotations are made directly on the class). By convention they are kept next to the fields they apply to.

For example, here is a schema that omits a field:

```python
from plone.autoform import directives
from plone.supermodel import model
from zope import schema


class ISampleSchema(model.Schema):

    title = schema.TextLine(title='Title')

    directives.omitted('additionalInfo')
    additionalInfo = schema.Bytes()
```

You can also handle multiple fields with one directive:

```python
directives.omitted('field_1', 'field_2')
```

With the directive "mode" you can set fields to 'input', 'display' or 'hidden'.

```python
directives.mode(additionalInfo='hidden')
```

You can apply directives to certain forms only. Here we drop a field from the add-form, it will still show up in the edit-form.

```python
from z3c.form.interfaces import IAddForm

class ITask(model.Schema):

    title = schema.TextLine(title='Title')

    directives.omitted(IAddForm, 'done')
    done = schema.Bool(
        title='Done',
        required=False,
    )
```

The same works for custom forms.

With the directive {py:meth}`widget` you can not only change the widget used for a field. With {py:data}`pattern_options` you can pass additional parameters to the widget. Here, we configure the datetime widget powered by the JavaScript library [pickadate](https://amsul.ca/pickadate.js/) by adding options that are used by it. Plone passes the options to the library.

```python
class IMeeting(model.Schema):

    meeting_date = schema.Datetime(
        title='Date and Time',
        required=False,
    )
    directives.widget(
        'meeting_date',
        DatetimeFieldWidget,
        pattern_options={
            'time': {'interval': 60, 'min': [7, 0], 'max': [19, 0]}},
    )
```

#### Validation and default values

In the following example we add a validator and a default value.

```python
from zope.interface import Invalid
import datetime


def future_date(value):
    if value and not value.date() >= datetime.date.today():
        raise Invalid('Meeting date can not be before today.')
    return True


def meeting_date_default_value():
    return datetime.datetime.today() + datetime.timedelta(7)


class IMeeting(model.Schema):

    meeting_date = schema.Datetime(
        title='Date and Time',
        required=False,
        constraint=future_date,
        defaultFactory=meeting_date_default_value,
    )
```

Validators and defaults can be also be made aware of the context (i.e. to check against the values of other fields).

For context aware defaults you need to use a {py:class}`IContextAwareDefaultFactory`. It will be passed the container for which the add form is being displayed:

```python
from zope.interface import provider
from zope.schema.interfaces import IContextAwareDefaultFactory


@provider(IContextAwareDefaultFactory)
def get_container_id(context):
    return context.id.upper()


class IMySchema(model.Schema):

    parent_id = schema.TextLine(
        title='Parent ID',
        required=False,
        defaultFactory=get_container_id,
    )
```

For context-aware validators you need to use {py:meth}`invariant`:

```python
from zope.interface import Invalid
from zope.interface import invariant
from zope.schema.interfaces import IContextAwareDefaultFactory


class IMyEvent(model.Schema):

    start = schema.Datetime(
        title='Start date',
        required=False,
    )

    end = schema.Datetime(
        title='End date',
        required=False,
    )

    @invariant
    def validate_start_end(data):
        if data.start is not None and data.end is not None:
            if data.start > data.end:
                raise Invalid('Start must be before the end.')
```

```{seealso}
To learn more about directives, validators and default values, refer to the following:

- [Form schema hints and directives](https://5.docs.plone.org/external/plone.app.dexterity/docs/reference/form-schema-hints.html)
- [Validation](https://5.docs.plone.org/develop/addons/schema-driven-forms/customising-form-behaviour/validation.html) (this documentation unfortunately still uses the obsolete grok technology)
- [z3c.form documentation](https://z3cform.readthedocs.io/en/latest/advanced/validator.html)
- [Default values for fields on add forms](https://5.docs.plone.org/external/plone.app.dexterity/docs/advanced/defaults.html)
```
