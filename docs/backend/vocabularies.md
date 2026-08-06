---
myst:
  html_meta:
    "description": "How to create and use vocabularies in Plone"
    "property=og:description": "How to create and use vocabularies in Plone"
    "property=og:title": "Vocabularies"
    "keywords": "Plone, vocabularies, zope.schema, Choice, plonecli"
---

(vocabularies-label)=

# Vocabularies

Vocabularies are lists of value/title pairs that provide options for selection fields.
They are commonly used with `zope.schema.Choice` fields to populate dropdown menus, checkboxes, and radio buttons in forms.

The `zope.schema` package provides tools to programmatically construct vocabularies using `SimpleVocabulary` and `SimpleTerm` objects.


## Vocabulary Terms

A vocabulary consists of terms. Each term represents one selectable option and has three key attributes:

`SimpleTerm.token`
:   Must be an ASCII string.
    This is the value passed with the request when the form is submitted.
    A token must uniquely identify a term.

`SimpleTerm.value`
:   The actual value stored on the object.
    This is not passed to the browser or used in the form.
    The value is often a unicode string, but can be any type of object.

`SimpleTerm.title`
:   A unicode string or translatable message.
    It is used for display in the form.

```{note}
If you need internationalized texts, only the `title` should be translated.
The `value` and `token` must always carry the same value.
```


## Creating a Static Vocabulary

### From a List of Tuples

```python
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary

items = [
    ('value1', 'This is label for item'),
    ('value2', 'This is label for value 2'),
]

terms = [
    SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
    for pair in items
]

my_vocabulary = SimpleVocabulary(terms)
```

### From a List of Values

For simple cases where value, token, and title are the same:

```python
from zope.schema.vocabulary import SimpleVocabulary

values = ['foo', 'bar', 'baz']
my_vocabulary = SimpleVocabulary.fromValues(values)
```

### Using the Vocabulary in a Schema

```python
from plone.supermodel import model
from zope import schema

class ISampleSchema(model.Schema):

    content_type = schema.Choice(
        title='Content Type',
        vocabulary=my_vocabulary,
        required=True,
    )
```


## Registering a Named Vocabulary

To make a vocabulary reusable across your application, register it as a named utility.

### Creating a Vocabulary Factory

```python
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def priority_vocabulary_factory(context):
    """A vocabulary of priority levels."""
    items = [
        ('low', 'Low Priority'),
        ('normal', 'Normal Priority'),
        ('high', 'High Priority'),
        ('urgent', 'Urgent'),
    ]
    terms = [
        SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
        for pair in items
    ]
    return SimpleVocabulary(terms)
```

### Registering in ZCML

Register the vocabulary factory in your `configure.zcml`:

```xml
<utility
    provides="zope.schema.interfaces.IVocabularyFactory"
    component=".vocabularies.priority_vocabulary_factory"
    name="example.vocabularies.priority"
/>
```

### Using a Named Vocabulary in a Schema

Reference the vocabulary by its registered name:

```python
from plone.supermodel import model
from zope import schema


class ITask(model.Schema):

    priority = schema.Choice(
        title='Priority',
        vocabulary='example.vocabularies.priority',
        required=True,
    )
```


## Retrieving a Vocabulary Programmatically

```python
from zope.component import getUtility
from zope.schema.interfaces import IVocabularyFactory

factory = getUtility(IVocabularyFactory, 'example.vocabularies.priority')
vocabulary = factory(context)
```


## Working with Vocabulary Terms

### Getting a Term by Value

```python
term = vocabulary.getTerm('high')
print(term.value)  # 'high'
print(term.token)  # 'high'
print(term.title)  # 'High Priority'
```

### Getting a Term by Token

```python
term = vocabulary.getTermByToken('high')
```

### Iterating Over a Vocabulary

```python
for term in vocabulary:
    print(f"Value: {term.value}, Token: {term.token}, Title: {term.title}")
```

### Checking if a Value Exists

```python
if 'high' in vocabulary:
    print("Value exists in vocabulary")
```


## Dynamic Vocabularies

Dynamic vocabularies generate their values at runtime based on context data, such as catalog queries or registry settings.

### Context Source Binder

Use `IContextSourceBinder` when your vocabulary depends on the current context:

```python
from zope.interface import provider
from zope.schema.interfaces import IContextSourceBinder
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IContextSourceBinder)
def available_documents_source(context):
    """Return a vocabulary of documents in the current folder."""
    # Get the portal catalog
    catalog = context.portal_catalog
    
    # Query for documents
    brains = catalog.searchResults(
        portal_type='Document',
        path={
            'query': '/'.join(context.getPhysicalPath()),
            'depth': 1,
        },
    )
    
    # Build vocabulary terms
    terms = [
        SimpleTerm(
            value=brain.UID,
            token=brain.UID,
            title=brain.Title,
        )
        for brain in brains
    ]
    
    return SimpleVocabulary(terms)
```

### Using a Source in a Schema

Use `source` instead of `vocabulary` when using a context source binder:

```python
from plone.supermodel import model
from zope import schema


class IMyContent(model.Schema):

    related_document = schema.Choice(
        title='Related Document',
        source=available_documents_source,
        required=False,
    )
```

### Dynamic Vocabulary from Registry

A common pattern is to populate vocabulary options from the Plone registry:

```python
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def talk_types_vocabulary_factory(context):
    """Vocabulary of talk types from registry."""
    types = api.portal.get_registry_record(
        'example.conference.talk_types',
        default=['Talk', 'Keynote', 'Workshop'],
    )
    terms = [
        SimpleTerm(value=t, token=t, title=t)
        for t in types
    ]
    return SimpleVocabulary(terms)
```


## Built-in Plone Vocabularies

Plone provides many useful vocabularies in the `plone.app.vocabularies` package.

### Common Vocabularies

| Vocabulary Name | Description |
|----------------|-------------|
| `plone.app.vocabularies.PortalTypes` | All portal types installed |
| `plone.app.vocabularies.ReallyUserFriendlyTypes` | User-friendly content types |
| `plone.app.vocabularies.UserFriendlyTypes` | Types filtered by the Types Tool |
| `plone.app.vocabularies.Workflows` | All installed workflows |
| `plone.app.vocabularies.WorkflowStates` | All workflow states |
| `plone.app.vocabularies.WorkflowTransitions` | All workflow transitions |
| `plone.app.vocabularies.AvailableContentLanguages` | Available content languages |
| `plone.app.vocabularies.SupportedContentLanguages` | Supported content languages |
| `plone.app.vocabularies.Roles` | User roles available in the site |
| `plone.app.vocabularies.Groups` | All groups in the site |
| `plone.app.vocabularies.Users` | All users in the site |
| `plone.app.vocabularies.Skins` | Available skins/themes |
| `plone.app.vocabularies.Actions` | All action category ids |
| `plone.app.vocabularies.Timezones` | Common timezones from pytz |
| `plone.app.vocabularies.AvailableEditors` | Configured WYSIWYG editors |
| `plone.app.vocabularies.ImagesScales` | All available image scales |
| `plone.app.vocabularies.Permissions` | All available permissions |
| `plone.app.vocabularies.Catalog` | All catalog indexes |

### Using Built-in Vocabularies

```python
from plone.supermodel import model
from zope import schema


class IMyContent(model.Schema):

    allowed_types = schema.List(
        title='Allowed Content Types',
        value_type=schema.Choice(
            vocabulary='plone.app.vocabularies.ReallyUserFriendlyTypes',
        ),
        required=False,
    )

    workflow = schema.Choice(
        title='Workflow',
        vocabulary='plone.app.vocabularies.Workflows',
        required=False,
    )
```


## Creating a Vocabulary with plonecli

The easiest way to create a vocabulary in a Plone add-on is using `plonecli` with `bobtemplates.plone`.

### Installation

```bash
UV tool install plonecli
```

### Creating an Add-on with a Vocabulary

First, create a new Plone add-on:

```bash
plonecli create addon src/collective.myaddon
```

Then, navigate to the package directory and add a vocabulary:

```bash
cd src/collective.myaddon
plonecli add vocabulary
```

The CLI will prompt you for the vocabulary class name. Enter a name like `MyCustomVocabulary`.

### Generated File Structure

The `plonecli add vocabulary` command creates the following structure:

```
src/collective.myaddon/
└── src/
    └── collective/
        └── myaddon/
            ├── configure.zcml          # Updated with vocabulary registration
            └── vocabularies/
                ├── __init__.py
                ├── configure.zcml      # Vocabulary ZCML configuration
                └── my_custom_vocabulary.py  # Your vocabulary implementation
```

### Generated Vocabulary Code

The generated vocabulary file looks like this:

```python
# -*- coding: utf-8 -*-
from collective.myaddon import _
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def MyCustomVocabularyFactory(context):
    """Vocabulary factory for my custom vocabulary."""
    # TODO: Replace with your vocabulary terms
    values = [
        ('value1', _('Title 1')),
        ('value2', _('Title 2')),
        ('value3', _('Title 3')),
    ]
    terms = [
        SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
        for pair in values
    ]
    return SimpleVocabulary(terms)
```

### Generated ZCML Registration

The vocabulary is automatically registered in `vocabularies/configure.zcml`:

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    i18n_domain="collective.myaddon">

  <utility
      component=".my_custom_vocabulary.MyCustomVocabularyFactory"
      name="collective.myaddon.MyCustomVocabulary"
      provides="zope.schema.interfaces.IVocabularyFactory"
      />

</configure>
```

### Using the Generated Vocabulary

After building and installing your add-on, use the vocabulary in your schemas:

```python
from plone.supermodel import model
from zope import schema


class IMyContent(model.Schema):

    my_field = schema.Choice(
        title='My Field',
        vocabulary='collective.myaddon.MyCustomVocabulary',
        required=True,
    )
```

The vocabulary will also appear in the Dexterity schema editor in your browser.


## Multiple Choice Fields

For fields that allow multiple selections, use `schema.List` or `schema.Set` with a `Choice` value type:

### List with Multiple Choices

```python
from plone.supermodel import model
from zope import schema


class IArticle(model.Schema):

    categories = schema.List(
        title='Categories',
        description='Select one or more categories',
        value_type=schema.Choice(
            vocabulary='example.vocabularies.categories',
        ),
        required=False,
    )
```

### Set with Multiple Choices (No Duplicates)

```python
from plone.supermodel import model
from zope import schema


class IArticle(model.Schema):

    tags = schema.Set(
        title='Tags',
        description='Select one or more tags',
        value_type=schema.Choice(
            vocabulary='example.vocabularies.tags',
        ),
        required=False,
    )
```


## Customizing Vocabulary Widgets

### Using Checkboxes for Multiple Choice

```python
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.checkbox import CheckBoxFieldWidget
from zope import schema


class IMyContent(model.Schema):

    directives.widget('options', CheckBoxFieldWidget)
    options = schema.List(
        title='Options',
        value_type=schema.Choice(
            vocabulary='example.vocabularies.options',
        ),
        required=False,
    )
```

### Using Radio Buttons for Single Choice

```python
from plone.autoform import directives
from plone.supermodel import model
from z3c.form.browser.radio import RadioFieldWidget
from zope import schema


class IMyContent(model.Schema):

    directives.widget('priority', RadioFieldWidget)
    priority = schema.Choice(
        title='Priority',
        vocabulary='example.vocabularies.priority',
        required=True,
    )
```


## Translated Vocabulary Titles

For internationalized vocabulary titles, use message factories:

```python
from collective.myaddon import _
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def status_vocabulary_factory(context):
    """Vocabulary with translated titles."""
    items = [
        ('draft', _('Draft')),
        ('pending', _('Pending Review')),
        ('published', _('Published')),
        ('archived', _('Archived')),
    ]
    terms = [
        SimpleTerm(value=pair[0], token=pair[0], title=pair[1])
        for pair in items
    ]
    return SimpleVocabulary(terms)
```

Don't forget to add translations to your `.po` files for each supported language.


## Vocabulary with Catalog Query

A complete example showing a vocabulary populated from a catalog query:

```python
from plone import api
from zope.interface import provider
from zope.schema.interfaces import IVocabularyFactory
from zope.schema.vocabulary import SimpleTerm
from zope.schema.vocabulary import SimpleVocabulary


@provider(IVocabularyFactory)
def authors_vocabulary_factory(context):
    """Vocabulary of authors from existing content."""
    catalog = api.portal.get_tool('portal_catalog')
    
    # Get unique creators from all content
    brains = catalog.searchResults(
        portal_type=['Document', 'News Item', 'Event'],
    )
    
    # Collect unique authors
    authors = set()
    for brain in brains:
        if brain.Creator:
            authors.add(brain.Creator)
    
    # Build terms sorted alphabetically
    terms = []
    for author_id in sorted(authors):
        # Try to get the user's full name
        user = api.user.get(author_id)
        if user:
            fullname = user.getProperty('fullname') or author_id
        else:
            fullname = author_id
        
        terms.append(
            SimpleTerm(
                value=author_id,
                token=author_id,
                title=fullname,
            )
        )
    
    return SimpleVocabulary(terms)
```


## REST API Access

Vocabularies are accessible via the Plone REST API at the `@vocabularies` endpoint.

### List All Vocabularies

```bash
curl -X GET http://localhost:8080/Plone/@vocabularies \
     -H "Accept: application/json" \
     --user admin:secret
```

### Get Vocabulary Terms

```bash
curl -X GET http://localhost:8080/Plone/@vocabularies/plone.app.vocabularies.ReallyUserFriendlyTypes \
     -H "Accept: application/json" \
     --user admin:secret
```

The response includes the `token` and `title` for each term:

```json
{
  "@id": "http://localhost:8080/Plone/@vocabularies/plone.app.vocabularies.ReallyUserFriendlyTypes",
  "items": [
    {"token": "Document", "title": "Page"},
    {"token": "News Item", "title": "News Item"},
    {"token": "Event", "title": "Event"}
  ],
  "items_total": 3
}
```


## Best Practices

1. **Use named vocabularies** for reusable options that appear in multiple schemas.

2. **Use context source binders** when the vocabulary values depend on the current context.

3. **Keep tokens ASCII-safe** since they are passed via HTTP requests.

4. **Make titles translatable** using message factories for internationalization.

5. **Cache expensive vocabularies** if they query the catalog or external services.

6. **Use plonecli** to scaffold vocabularies in your add-ons to follow best practices.

7. **Document your vocabularies** with docstrings explaining what they contain and when to use them.


## See Also

- {ref}`fields-label` for field types that use vocabularies
- {doc}`../forms/index` for form handling
- [zope.schema documentation](https://zopeschema.readthedocs.io/)
- [plone.app.vocabularies source code](https://github.com/plone/plone.app.vocabularies)
- [bobtemplates.plone documentation](https://bobtemplatesplone.readthedocs.io/)


## Related content

-   {doc}`/backend/fields`
-   {doc}`/backend/schemas`
-   {doc}`/backend/content-types/index`
