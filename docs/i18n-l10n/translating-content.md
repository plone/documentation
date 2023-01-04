---
myst:
  html_meta:
    "description": "Translating content items in Plone, creating translations programmatically, and working with translators."
    "property=og:description": "Translating content items in Plone, creating translations programmatically, and working with translators."
    "property=og:title": "Translating content"
    "keywords": "Plone, Internationalization, i18n, language, translate, content, localization"
---

(translating-content-label)=

# Translating content

```{note}
This chapter concerns only _user-generated content_ translations.

For _code-level_ translations of text strings, see {doc}`translating-text-strings`.
```

To have content translation in Plone you need to activate the `plone.app.multilingual` add-on.
This add-on is installed by default in your Plone site.

```{warning}
This multilingual tool makes several assumptions about your content.
It is recommended to work with these assumptions, not against them.
You may choose to work against these assumptions, but be warned that along this path, "here be dragons".
```


(translating-content-configure-languages-label)=

## Configure languages in your site

Start by visiting the `@@language-controlpanel` of your Plone site.
Configure which languages will be available for your site.

After selecting the languages and saving the form, Plone will initialize the multilingual configuration for you.
It will perform the following tasks:

-   Create one folder per language selected in the root of the site.
    If you selected English and French as available languages, it will create the `en` and `fr` folders.
    Those folders are a specific content type called {term}`Language Root Folder`s (LRFs).
    Moreover, these LRFs are marked as `INavigationRoot` objects.
    That means all search, navigation, and catalog queries will be automatically restricted to the content inside them, making it easier to automatically build menus and search within a site's specified language.

-   Plone will change the default layout of the Plone Site object to be the `@@language-switcher` view.
    This view will handle the language negotiation between the end user and Plone when the user lands in the home page of your site. 

Plone and `plone.app.multilingual` will always assume that all your multilingual content lives inside those Language Root Folders.
No other thing should be outside them.


(translating-content-translating-your-content-label)= 

## Translate your content

After enabling multiple languages in your site, the Plone toolbar will provide menu items to translate your content to the available languages.

Be careful!
Plone will not translate the content for you.
It will only create the content in the other language folders, and both LRFs' contents will be linked to the translations.

Plone does not use any third party tools to automatically translate content.
If needed, you will need to develop such connector tools and {term}`hook` into a content creation process.


(translating-content-language-independent-content)=

## Language independent content

In some cases it is justified to have "language independent content".
This means content that you need to be available in several languages, such as files or images.
Plone provides the {term}`Language Independent Folder`s (LIF), that are automatically created when enabling languages in your site. 

In the root of your language folder you will find a folder containing static assets.
If you have configured the English site, this folder is called `Assets`.
In Spanish, it is called `Media`.
It can have different names in different languages.
You can store assets in those language independent folders.
Plone will take care of showing you any content uploaded to those LIFs in all languages.
LIFs are internally special folders that are linked to all languages and share the internal structure that saves content objects.

```{note}
It is not possible to have more than one LIF per language.
Plone will not correctly work if you try to manually add more LIFs.
That's the reason behind not being able to add more LIFs by default.
```


(translating-content-language-selector-label)=

## Language selector

After enabling several languages in your Plone site, Plone will show a language selector widget in the top of your site.
This widget will link the actual page the user is browsing with its translated counterparts.

The language control panel provides several ways to configure this widget:

-   {guilabel}`General > Show language flags`.
    It is common to use flags to identify languages.
    Enabling this option will do it for you.
    However, this is not considered a best practice because country flags do not necessarily represent a language.
    Why should one use a Spanish flag to identify the Spanish language when browsing a South American, English-Spanish bilingual site?
    It is recommended to disable the {guilabel}`Show language flags` option.

-   {guilabel}`Multilingual > The policy used to determine how the lookup for available translations will be made by the language selector.`
    What to do when a given content is not translated to another language?
    Which link should Plone show, if any?
    Plone provides two policy options to choose from to configure such scenarios.
 
    -   {guilabel}`Search for closest translation in parent's content chain.`
        This option will send the user to the selected language, and will try to find a translated parent of the actual content.
        This is the default policy.
  
    -   {guilabel}`Show user dialog with information about the available translations.`
        This option will send the user to the selected language, but it will present a "No translation for this content" page, allowing the user to go to some other language or keep browsing that site, while informing the user that there is no such content in that language.

        ```{todo}
        This option appears to not work as documented in the Plone 6 Classic UI demo's Language control panel.
        ```


(translating-content-marking-objects-as-translatables-label)=

### Marking objects as translatables


#### Dexterity

Users should mark a Dexterity content type as translatable by assigning a multilingual behavior to the definition of the content type either via file system, supermodel, or through the web.


(translating-content-marking-fields-as-language-independent-label)=

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

Via the content type definition in the {guilabel}`Content Types` control panel.

```{versionchanged} 6.0
Changed the name from "Dexterity Content Types" to just "Content Types". 
```


(translating-content-language-getset-via-unified-adapter-label)=

### Language get/set via a unified adapter

In order to access and modify the language of a content type, regardless of whether the type is an interface or adapter, we use `plone.app.multilingual.interfaces.ILanguage`.

In your code, you can use the following.

```python
from plone.app.multilingual.interfaces import ILanguage
language = ILanguage(context).get_language()
```

If you want to set the language of a content type:

```python
language = ILanguage(context).set_language('ca')
```


(translating-content-itranslationmanager-adapter-label)=

### `ITranslationManager` adapter

The most interesting adapter that `plone.app.multilingual` provides is `plone.app.multilingual.interfaces.ITranslationManager`.
It adapts any `ITranslatable` object to provide convenience methods to manage the translations for that object.


(translating-content-add-a-translation-label)=

#### Add a translation

Given an object `obj`, translate it to the Catalan language (`ca`):

```python
from plone.app.multilingual.interfaces import ITranslationManager
ITranslationManager(obj).add_translation('ca')
```


(translating-content-register-a-translation-for-existing-content-label)=

#### Register a translation for existing content

Given an object `obj`, and we want to add `obj2` as a translation for the Catalan language (`ca`):

```python
ITranslationManager(obj).register_translation('ca', obj2)
```


(translating-content-get-translations-for-an-object-label)=

#### Get translations for an object

Given an object `obj`, get all the translated objects (including the context):

```python
ITranslationManager(obj).get_translations()
```

To get a specific translation, such as Catalan (`ca`):

```python
ITranslationManager(obj).get_translation('ca')
```


(translating-content-check-an-object-for-translations-label)=

#### Check an object for translations

Given an object `obj`, get a list of all of its translated languages:

```python
ITranslationManager(obj).get_translated_languages()
```

Or to check for a specific translated language:

```python
ITranslationManager(obj).has_translation('ca')
```

For all available methods, see the source code of the [`plone.app.multilingual.interfaces.ITranslationManager` class](https://github.com/plone/plone.app.multilingual/blob/5363b90c8adf90eb9bd6aeaebf6fe6b03a4e866f/src/plone/app/multilingual/interfaces.py#L75).
