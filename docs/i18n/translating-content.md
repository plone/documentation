---
html_meta:
  "description": "Translating content items in Plone, creating translations programmatically, and working with translators."
  "property=og:description": "Translating content items in Plone, creating translations programmatically, and working with translators."
  "property=og:title": "Translated content"
  "keywords": "Plone, Internationalization, i18n, language, translated, content, localization"
---

(translated-content-label)=

# Translated content

```{admonition} Description
Translating content items in Plone, creating translations programmatically, and working with translators.
```


## Introduction

Plone ships out of the box with a multilingual solution for translating user generated content.
For all practical purposes, you should use that package, `plone.app.multilingual`.

```{note}
For earlier Plone versions, there were other solutions like `LinguaPlone` and `raptus.multilanguageplone`.
Refer to the [Plone 4 version of this document](https://docs.plone.org/4/en/develop/plone/i18n/translating_content.html) if you need that information.
```


## `plone.app.multilingual`

`plone.app.multilingual` was designed originally to provide Plone a whole multilingual story.
Using ZCA technologies, it enables translations to Dexterity and Archetypes content types, as well managed via a unified user interface.

This module provides the user interface for managing content translations.
It is the application package of the next generation Plone multilingual engine.
It is designed to work with Dexterity content types and the *old fashioned* Archetypes based content types as well.
It only works with Plone 4.1 and above, due to the use of UUIDs for referencing the translations.

For more information see [`plone.app.multilingual`](https://github.com/plone/plone.app.multilingual).


### Installation

To use this package with both Dexterity and Archetypes based content types, you should add the following line to your `eggs` buildout section:

```cfg
eggs =
    plone.app.multilingual[archetypes, dexterity]
```

If you need to use this package only with Archetypes based content types, you only need the following line:

```cfg
eggs =
    plone.app.multilingual[archetypes]
```

While Archetypes is default in Plone for now, you can strip `[archetypes]`.
This may change in the future, so we recommend adding an appendix as shown above.


### Setup

After re-running your buildout and installing the newly available add-ons, you should go to the {guilabel}`Languages` section of your site's control panel, and select at least two or more languages for your site.
You will now be able to create translations of Plone's default content types, or to link existing content as translations.


### Marking objects as translatables


#### Archetypes

By default, if `plone.app.multilingual` is installed, Archetypes-based content types are marked as translatables.


#### Dexterity

Users should mark a dexterity content type as translatable by assigning a multilingual behavior to the definition of the content type either via file system, supermodel, or through the web.


### Marking fields as language independent


#### Archetypes

The language independent fields on Archetype-based content are marked as follows.
This is the same as in previous version of Plone with `LinguaPlone` in place:

```python
atapi.StringField(
    'myField',
    widget=atapi.StringWidget(
    #...
    ),
    languageIndependent=True
)
```

#### Dexterity

There are four ways to translate Dexterity-based types.


##### Grok directive

In your content type class declaration:

```python
from plone.app.multilingual.dx import directives
directives.languageindependent('field')
```


##### Supermodel

In your content type XML file declaration:

```xml
<field name="myField" type="zope.schema.TextLine" lingua:independent="true">
    <description />
    <title>myField</title>
</field>
```


##### Native

In your code:

```python
from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
alsoProvides(ISchema['myField'], ILanguageIndependentField)
```


##### Through the web

Via the content type definition in the {guilabel}`Dexterity Content Types` control panel.


### Language get/set via a unified adapter

In order to access and modify the language of a content type regardless of the type (Archetypes/Dexterity) there is an interface/adapter, `plone.app.multilingual.interfaces.ILanguage`.

In your code, you can use the following.

```python
from plone.app.multilingual.interfaces import ILanguage
language = ILanguage(context).get_language()
```

If you want to set the language of a content type:

```python
language = ILanguage(context).set_language('ca')
```


### ITranslationManager adapter

The most interesting adapter that `plone.app.multilingual` provides is `plone.app.multilingual.interfaces.ITranslationManager`.

It adapts any `ITranslatable` object to provide convenience methods to manage the translations for that object.


#### Add a translation

Given an object `obj`, and we want to translate it to the Catalan language ('ca'):

```python
from plone.app.multilingual.interfaces import ITranslationManager
ITranslationManager(obj).add_translation('ca')
```


#### Register a translation for an already existing content

Given an object `obj`, and we want to add `obj2` as a translation for the Catalan language ('ca'):

```python
ITranslationManager(obj).register_translation('ca', obj2)
```


#### Get translations for an object

Given an object `obj`:

```python
ITranslationManager(obj).get_translations()
```

and if we want a concrete translation:

```python
ITranslationManager(obj).get_translation('ca')
```


#### Check if an object has translations

Given an object `obj`:

```python
ITranslationManager(obj).get_translated_languages()
```

or:

```python
ITranslationManager(obj).has_translation('ca')
```

For more information, see https://github.com/plone/plone.app.multilingual/blob/ee81a3015ac3f26505e82638030a95d786a1a444/src/plone/app/multilingual/interfaces.py#L76.
