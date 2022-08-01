---
html_meta:
  "description": "How to contribute to the Plone translations."
  "property=og:description": "How to contribute to the Plone translations."
  "property=og:title": "Contributing Plone Core Translations"
  "keywords": "Plone, Internationalization, i18n, language, translation, localization"
---

(contributing-plone-core-translations-label)=

# Contributing Plone Core Translations

```{admonition} Description
How to contribute to the Plone translations.
```


## Introduction

Request write access to https://github.com/collective/plone.app.locales to be able to commit your translation directly.

To do so, [join the collective GitHub organization](https://collective.github.io/).

You can fork the repository and work from there or create a new branch and work in that branch.

## Translate Plone

The process of translating Plone UI is the following:

1. Go to https://github.com/collective/plone.app.locales and clone it into your computer

2. Create a new branch to work on your translations. Name the branch with something identifiable. For example: {language}-{date} (ex. fr-20220731)

3. Translate the `po` files under your language of choice at plone/app/locales/locales/{language_code}/LC_MESSAGES/*.po. In Classic UI we have several language files because some of the original messages are spread over several language domains and products.

4. Commit your changes and add a Pull Request with them. Try to have a review from a colleague, specially in case you are translating a file with already some translations. This is just to have coherent translations all over Plone.


## Translate Volto

The process of translating Volto UI is the following:

1. Go to https://github.com/plone/volto 3 and clone it into your computer
2. Create a new branch to prepare the translations. Name the branch with something identifiable. For example: {language}-{date} (ex. fr-20220731)

3.a Translate your language `po` file found at locales/{language_code}/LC_MESSAGES/volto.po

3.b Alternatively, if your language file doesn't exist, create a new folder at locales/{language_code}/LC_MESSAGES/, copy over the volto.pot file there as volto.po and start translating.

4. Commit your changes and add a Pull-Request.

## Support

Please ask questions on the Plone Community Forum category [Translations and i18n/l10n](https://community.plone.org/c/development/i18nl10n/42).
