---
myst:
  html_meta:
    "description": "When translating content items in Plone you can connect to an external translation service to have your content translated."
    "property=og:description": "When translating content items in Plone you can connect to an external translation service to have your content translated."
    "property=og:title": "Use an external translation service to translate content"
    "keywords": "Plone, Internationalization, i18n, language, translate, content, localization"
---

(use-an-external-translation-service-label)=

# Use an external translation service to translate content

When translating content items in Plone you can connect to an external translation service to have your content translated.


## Using Google Cloud Translation API

The plone.app.multilingual product that turns Plone into a multilingual-content site, supports [Google Cloud Translation API](https://cloud.google.com/translate/docs/reference/rest), which allows the content editor to use its translations.

The site administrator, needs to create a project in Google Cloud, enable the Cloud Translation API, and create an API key under the Credentials of the Google Cloud Console.

This API key, can be entered in the Multilingual Settings Control Panel in Plone.

After doing so, when the content editor is editing a translation of a given content page, an icon will be shown next to the original content.

When clickin on such icon, the Google Cloud Translation API will be invoked, and the translation obtained through the service entered automatically in the corresponding field.

```{note}
The usage of Google Cloud Translation API may create extra cost for the site administrator.
```


## Using other translation services

If the site administrator doesn't want to use Google Cloud Translation API but some other service, they can provide an adapter that calls an some other service.

To do so, a new adapter needs to be registered, to provide the `IExternalTranslationService` interface.

This interface describes an object that needs to have the following attribute and methods:

- order: the order in which this adapter will be executed. This way, one can prioritize some services,
- is_available(): to return whether the adapter is available (for instance, is the Google translation API key entered into the control panel?)
- available_languages(): a list of language pairs (source, target), that this adapter supports.
- translate_content(): the actual function that does the translation call

Add-on authors can look at `{file}plone.app.multilingual.google_translate.py` where they can find an example of such an implementation.

The adapter, needs to be registered in `ZCML`. Add-on authors can look at `{file}plone.app.multilingual.configure.zcml` where they can find an example of such registration.
