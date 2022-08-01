---
html_meta:
  "description": "Translating content items in Plone, creating translations programmatically, and working with translators."
  "property=og:description": "Translating content items in Plone, creating translations programmatically, and working with translators."
  "property=og:title": "Translating content"
  "keywords": "Plone, Internationalization, i18n, language, translate, content, localization"
---

(translating-content-label)=

# Translating content

```{admonition} Description
Translating content items in Plone, creating translations programmatically, and working with translators.
```

```{note}
This chapter concerns only _user-generated content_ translations.

For *code-level* translations of text strings, see {doc}`translating-text-strings`.
```

## Introduction

To have content translation in Plone you need to activate the `plone.app.multilingual` addon which be installed by default in your Plone installation.

```{note}
This multilingual tool makes several assumptions on your content and you as a user have to live with them. Working *against the system* will be hard because Plone will want to continue working as it is expected to work and reconfiguring it in some other way is a hard work. You are warned :wink: !
```

## Configure languages in your site

As a first step, you will need to go to the `@@language-controlpanel` of your Plone site and configure which languages will be available for your site.

After selecting the langauges and saving the form, Plone will setup the multilingual configuration for you. This means that will do the following tasks:

- Create one folder per language selected in the root of the site. If you have selected English and French as available languages, it will create the `en` and `fr` folders. Those folders are of an specific content-type called Language Root Folders (LRF for short). Moreover these LRFs are marked as `INavigationRoot` objects, which means that all search, navigation and catalog queries will be automatically restricted to the content inside them, easing the automatic menu building and search.

- Plone will change the default layout of the Plone Site object to be the `@@language-switcher` view. This view will handle the language negotiation between the end-user and Plone when the user lands in the home page of your site. 

Plone and plone.app.multilingual will always assume that all your multilingual content lives inside those Language Root Folders, and no other thing should be outside them.

## Translate your content

After enabling multiple languages in your site, the Plone toolbar will provide menu items to translate your content to the available languages.

Be careful, Plone will not translate the content for you, it will "only" create the content in the other language folder and both contents will be linked to be translations.

Plone does not use any thirdparty tools to automatically translate content. If needed, you will need to develop such connector tools and hook into content creation process.

## Language independent content

In some cases it is justified to have so called "language independent content", which means content that you need to be available in several languages, usually this content is made of Files or Images. Plone provides the so called Language Independent Folders (LIF for short), that are automatically created when enabling languages in your site. 

In the root of your language folder you will find an 'assets' folder (if you have configured the English site is called `Assets`, in Spanish `Media`, it can have different names in different languages) where you can store those language independent contents. Plone will take care of showing you any content uploaded to those LIFs in all languages. LIFs are internally special Folders which are linked into all languages and share the internal structure that saves content objects.

```{note}
It is not possible to have more than one LIF per language. Plone will not correctly work if you try to manually add more LIFs. That's the reason behind not being able to add more LIFs by default.
```

## Language selector

After enabling several languages in your Plone site, Plone will show a language selector widget in the top of your site. This widget will link the actual page the user is browsing with its translated counterparts.

The language controlpanel provides several ways to configure this widget:

- Show language flags: it is quite common to use flags to identify languages and enabling this option will do it for you. Anyway this is not considered best practice because country flags do not represent language. Why should one use Spanish flag to identify the Spanish language when browsing a south-american english-spanish bilingual site? That's why usually it is recommended to disable the "Show language flags" option.

- Policy used to determine how the lookup for the available translation will be made. What to do when a given content is not translated to some other language? Which link should Plone show if any? Plone provides 2 policies to configure such scenario.
 
  - Search for closes translation in parent's content chain: this will send the user to the selected language and will try to find a translated parent of the actual content. This is the default policy.
  
  - Show "no translations for this content": this will sent the user to the selected language but it will present a "No translation for this content" page, allowing the user to go to some other language, or keep browsing that site but informing that there is no such content in that language.


### Marking objects as translatables


#### Dexterity

Users should mark a dexterity content type as translatable by assigning a multilingual behavior to the definition of the content type either via file system, supermodel, or through the web.


### Marking fields as language independent


#### Dexterity

There are three ways to translate Dexterity-based types.



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

In order to access and modify the language of a content type regardless of the type there is an interface/adapter, `plone.app.multilingual.interfaces.ILanguage`.

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
