---
myst:
  html_meta:
    "description": "When translating content items in Plone, you can connect to an external translation service to translate your content."
    "property=og:description": "When translating content items in Plone, you can connect to an external translation service to translate your content."
    "property=og:title": "Use an external translation service to translate content"
    "keywords": "Plone, Internationalization, i18n, language, translate, content, localization, l10n"
---

(use-an-external-translation-service-label)=

# Use an external translation service to translate content

When translating content items in Plone, you can connect to an external translation service to translate your content.


The `plone.app.multilingual` product that turns Plone into a multilingual content site supports a pluggable way to hook any translation service into Plone.

To do so, one has to implement a utility that implements an `IExternalTranslationService` interface.

This utility class must implement the `IExternalTranslationService` interface from `plone.app.multilingual.interfaces` and it should provide at least these methods and an attribute:

`is_available()`
:   Returns `True` if the service is enabled and ready.

`available_languages()`
:   Returns a list of supported language codes or pairs that can be used (source, target).

`translate_content(content, source_language, target_language)`
:   Performs the translation and returns the translated text.

`order`
:   The order in which this utility will be executed.
    This way, one can prioritize some services over others with given conditions.

After doing so, as a content editor, when you edit a translation of a given content page, a translate icon <img alt="Translate icon" src="../_static/translate.svg" class="inline"> will display next to the original content.

When you click this icon, it will invoke the translation utility, and the translation obtained through the service will be entered automatically in the corresponding field.

Plone does not implement this interface by itself in any of its utilities.

You'll need to use an external package that offers this service as described in {ref}`pre-configured-services-label`, or create your own utility.

(pre-configured-services-label)=

## Using the translation service with pre-configured services

To use some external tools, the Plone community has implemented a package called [`collective.translators`](https://github.com/collective/collective.translators) that implements this functionality for AWS, Deepl, Deepseek, Google Translate, Libre Translate, and Ollama.

Each of those services provides a control panel to tweak the configuration, including API keys, languages, service endpoints, and other configuration items.

```{note}
The usage of some of those services may create extra cost for the site administrator.
Check the terms of use of each of the tools for details.
```
