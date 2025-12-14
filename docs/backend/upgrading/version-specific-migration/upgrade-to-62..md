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


## Drop of Google Translate integration

`plone.app.multilingual` had an integration to use Google Translate to translate the content in the `babel_view`, where the content in two languages is shown side-by-side.

This integration has been removed in Plone 6.2, and has been exchanged by a generic translation service integration. See the {ref}`use-an-external-translation-service-label` section for details.

To achieve that integration the previously existing `gtranslation_service` browser view has been removed from plone.app.multilingual.

Due to not needing it anymore, the `plone.google_translation_key` registry entry has been removed and will be removed by the upgrade step to Plone 6.2.

The `babel_view` has been modified to call a new REST API endpoint instead of the old `gtranslation_service` browser view.

To keep using the previously existing Google Translate integation, site administrators have to install a new package that provides those (and more) services, the package is called `collective.translators`.
