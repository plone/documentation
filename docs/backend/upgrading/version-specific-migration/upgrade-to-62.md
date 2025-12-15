---
myst:
  html_meta:
    "description": "How to upgrade to Plone 6.2"
    "property=og:description": "How to upgrade to Plone 6.2"
    "property=og:title": "How to upgrade to Plone 6.2"
    "keywords": "Upgrade, Plone 6"
---

(backend-upgrade-plone-v62-label)=

# Upgrade Plone 6.1 to 6.2

Plone 6.2 has seen the following major changes.
Some may require changes in your setup.


## Replaced Google Translate integration with generic translation integration

`plone.app.multilingual` had an integration to use only Google Translate to translate the content in the `babel_view`, where the content in two languages is shown side-by-side.
This integration was limited to only Google Translate.
In Plone 6.2, this integration has been replaced with a generic translation service integration hook.

[`collective.translators`](https://github.com/collective/collective.translators) provides some implementations for that hook, supporting AWS, Deepl, Deepseek, Google Translate, Libre Translate, and Ollama.
It can be extended to support more translation providers.

It is not mandatory to use `collective.translator`.
Any developer can write the integration with the tool of their choice.

See the {doc}`/i18n-l10n/use-an-external-translation-service` chapter for details.

To achieve that integration, the previously existing `gtranslation_service` browser view has been removed from `plone.app.multilingual`.

Due to not needing it anymore, the `plone.google_translation_key` registry entry has been removed, and it will be removed when performing the upgrade step to Plone 6.2.

The `babel_view` has been modified to call a new REST API endpoint instead of the old `gtranslation_service` browser view.
