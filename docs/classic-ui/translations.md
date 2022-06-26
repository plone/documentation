---
html_meta:
  "description": "A guide to help contributors to translate Plone into their language"
  "property=og:description": "A guide to help contributors to translate Plone into their language"
  "property=og:title": "Translate Plone into your language"
  "keywords": ""
---

(classic-ui-translations-label)=

# Translations

Plone public interface is translated into a lot of languages, but not all of them are complete because sometimes the development goes faster than the translation editing effort. This guide will help to you contribute translation to Plone core.


1. Go to https://github.com/collective/plone.app.locales and clone it into your computer
1. Create a new branch to work on your translations
1. Translate the PO files under your language of choice at plone/app/locales/locales/{language_code}/LC_MESSAGES/*.po. In Classic UI there are several language files because some of the original messages are spread over several language domains and products.
1. Commit your changes and add a Pull Request with them. Try to have a review from a colleague, specially in case you are translating a file with already some translations. This is just to have coherent translations all over Plone.
