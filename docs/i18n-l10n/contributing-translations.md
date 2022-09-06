---
myst:
  html_meta:
    "description": "How to contribute to Plone core translations."
    "property=og:description": "How to contribute to Plone core translations."
    "property=og:title": "Contributing Plone Core Translations"
    "keywords": "Plone, Internationalization, i18n, language, translation, localization"
---

(contributing-plone-core-translations-label)=

# Contributing Plone Core Translations

```{admonition} Description
How to contribute to the Plone translations.
```

This chapter of the documentation describes how to contribute to Plone's translations.
Plone fully supports {term}`internationalization` and {term}`localization`.
Plone Classic UI comes with 65 local language translations, and the new default frontend Volto comes with 12, at the time of this writing.
However, some translations are incomplete, or certain languages have not yet been added.
Translations can be added or updated as needed by the citizens of Earth.
You will need to work in one repository for Plone core, and optionally another one for Volto.


(contributing-plone-core-translations-pre-requisites-label)=

## Pre-requisites

Request write access to https://github.com/collective/plone.app.locales to be able to commit your translation directly.

To do so, [join the collective GitHub organization](https://collective.github.io/).

Optionally sign the [Plone Contributor Agreement](https://plone.org/foundation/contributors-agreement) for translating Volto.


(contributing-plone-core-translations-translate-plone-classic-ui-label)=

## Translate Plone Classic UI

The process of translating Plone Classic UI is the following.

1.  Go to https://github.com/collective/plone.app.locales and clone it into your computer.

2.  Create a new branch to work on your translations.
    Name the branch with something identifiable.
    For example: `{language}-{date}` (`fr-20220731`).

3.  Either update or create a translation.

    -   To _update_ an existing translation, translate the {term}`po` files under your language of choice at `plone/app/locales/locales/{language_code}/LC_MESSAGES/*.po`.
    In Classic UI, we have several language files because some of the original messages are spread over several language domains and products.
    -   To _create_ a translation, create a new directory at `plone/app/locales/locales/{language_code}/LC_MESSAGES`, copy all the `.pot` files in `plone/app/locales/locales` to your new directory, rename the files in your directory by changing the file extension to `.po`, and start translating.

4.  Commit your changes, and create a pull request with them.
    Request a review from a colleague, especially if you are translating a file that already has some translations.
    You can check the file's commit history with `git blame <filename>` to see previous contributors and request a review from them.
    This is to ensure coherent translations throughout Plone.


(contributing-plone-core-translations-translate-volto-label)=

## Translate Volto

The process of translating the Volto frontend is the following.

1.  Go to https://github.com/plone/volto and clone it into your computer.

2.  Create a new branch to prepare the translations.
    Name the branch with something identifiable.
    For example: `{language}-{date}` (`fr-20220731`).

3.  Either update or create a translation.

    -  To update a translation, translate your language's `po` file found at `locales/{language_code}/LC_MESSAGES/volto.po`.
    -  To create a new translation, create a new directory at `locales/{language_code}/LC_MESSAGES/`, copy the file `locales/volto.pot` to `locales/{language_code}/LC_MESSAGES/volto.po` (note to drop the trailing `t`), and start translating.

4. Commit your changes, and create a pull request.


(contributing-plone-core-translations-support-label)=

## Support

Please ask questions on the Plone Community Forum category [Translations and i18n/l10n](https://community.plone.org/c/development/i18nl10n/42).
