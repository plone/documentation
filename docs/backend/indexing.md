---
myst:
  html_meta:
    "description": "Using Plone's catalog to index content and make it searchable."
    "property=og:description": "Using Plone's catalog to index content and make it searchable."
    "property=og:title": "Indexing"
    "keywords": "Plone, indexing, indexes, indexer, catalog, searching, FieldIndex, KeywordIndex, DateIndex, DateRangeIndex, BooleanIndex, ZCTextIndex, SearchableText, textindexer"
---

(backend-indexing-label)=

# Indexing

To make Plone content searchable, one can use different indexes to index content.

The most important index types are the following.

- `FieldIndex`
- `KeywordIndex`
- `DateIndex`
- `DateRangeIndex`
- `BooleanIndex`
- `ZCTextIndex`

The most important indexes are described in the following sections.


(backend-indexing-searchabletext-label)=

## `SearchableText`

The `SearchableText` is a `ZCTextIndex` for indexing full text.
It is used by default for Dublin Core fields such as `Title`, `Description`, and `Text`.


(backend-indexing-textindexer-label)=

## `TextIndexer`

To add other fields to the `SearchableText`, one can use the `plone.app.dexterity.textindexer`.

For enabling the indexer, add the behavior to the list of behaviors of your content types.

In your `profiles/default/types/YOURTYPE.xml` add the behavior.

```xml
<?xml version="1.0"?>
<object name="example.conference.presenter" meta_type="Dexterity FTI"
   xmlns:i18n="http://xml.zope.org/namespaces/i18n"
   i18n:domain="example.conference">

 <!-- enabled behaviors -->
 <property name="behaviors" purge="false">
     <element value="plone.textindexer" />
 </property>
</object>
```

Now you need to mark the fields you want to have in your SearchableText. 
This can be done with the `searchable` directive.

```python
from plone.app.dexterity import textindexer
from plone.supermodel.model import Schema
from plone import schema

class IMyBehavior(Schema):

    textindexer.searchable('specialfield')
    specialfield = schema.Text(title=u'Special field')

```

If you want to mark fields of an existing third party behavior, it can be done using the following utility function.

```python
from plone.app.dexterity.behaviors.metadata import ICategorization
from plone.app.dexterity.textindexer import utils

utils.searchable(ICategorization, 'categorization')
```

The `title` and `description` on `plone.app.dexterity`'s `IBasic` behavior are marked as searchable by default.
For marking them as no longer searchable, there is a utility function.

```python
from plone.app.dexterity.behaviors.metadata import IBasic
from plone.app.dexterity.textindexer import utils

utils.no_longer_searchable(IBasic, 'title')
```

Alternatively, if you specified your model as a `plone.supermodel` XML model, you can mark the field searchable by using `indexer:searchable="true"`.

```xml
<model xmlns="http://namespaces.plone.org/supermodel/schema"
        xmlns:indexer="http://namespaces.plone.org/supermodel/indexer">
    <schema based-on="plone.supermodel.model.Schema">

        <field name="specialfield" type="zope.schema.TextLine"
                indexer:searchable="true">
        <title>Special field</title>
        </field>

    </schema>
</model>
```

The `SearchableText` indexer now includes your custom field on your behavior.
The field of your content type is indexed if the `plone.textindexer` behavior is enabled on your content type.


(backend-indexing-registering-custom-field-converter-label)=

## Registering a custom field converter

By default a field is converted to a searchable text by rendering the widget in display mode and transforming the result to `text/plain`. 
However if you need to convert your custom field in a different way, you have to provide a more specific converter multi-adapter.


(backend-indexing-convert-multi-adapter-specification-label)=

### Convert multi-adapter specification

Interface
: `plone.app.dexterity.textindexer.IDexterityTextIndexFieldConverter`

Discriminators
: context, field, widget

Example:

```python
from plone.app.dexterity.textindexer.converters import DefaultDexterityTextIndexFieldConverter
from plone.app.dexterity.textindexer.interfaces import IDexterityTextIndexFieldConverter
from my.package.interfaces import IMyFancyField
from plone.dexterity.interfaces import IDexterityContent
from z3c.form.interfaces import IWidget
from zope.component import adapter
from zope.interface import implementer

@implementer(IDexterityTextIndexFieldConverter)
@adapter(IDexterityContent, IMyFancyField, IWidget)
class CustomFieldConverter(DefaultDexterityTextIndexFieldConverter):

    def convert(self):
            # implement your custom converter
            # which returns a string at the end
            return ''
```

ZCML:

```xml
<configure xmlns="http://namespaces.zope.org/zope">

    <adapter factory=".converters.CustomFieldConverter" />

</configure>
```

There is already an adapter for converting files properly.


(backend-indexing-extending-indexed-data-label)=

## Extending indexed data

Sometimes you need to extend the `SearchableText` with additional data which is not stored in a field.
It is possible to register a named adapter which provides additional data.

```python
from plone.app.dexterity import textindexer
from zope.component import adapter
from zope.interface import implementer


@implementer(textindexer.IDynamicTextIndexExtender)
@adapter(IMyBehavior)
class MySearchableTextExtender(object):

    def __init__(self, context):
        self.context = context

    def __call__(self):
        """Extend the searchable text with a custom string"""
        return 'some more searchable words'
```

ZCML:

```xml
<configure xmlns="http://namespaces.zope.org/zope">

    <adapter factory=".indexer.MySearchableTextExtender"
                name="IMyBehavior"
                />

</configure>
```

This is a **named** adapter!
The named registration allows registering multiple extenders on different behavior interfaces applying to the same object.
The name of the adapter does not matter, but it's recommended to use the name of the behavior to reduce potential conflicts.

If your behavior has a defined factory (which is not attribute storage), then you need to define a marker interface and register the adapter on this marker interface. 
Dexterity objects do not provide behavior interfaces of behaviors, which are not using attribute storage.


(backend-indexing-portal-type-fieldindex-label)=

## `portal_type` (`FieldIndex`)

Indexes the `portal_type` field and contains values such as `Folder`.


(backend-indexing-path-pathindex-label)=

## `path` (`PathIndex`)

Indexes the object path, such as `/news/news-item-1`.


(backend-indexing-subject-keywordindex-label)=

## `Subject` (`KeywordIndex`)

Indexes the `Subject` field which contains a list of object categories.
