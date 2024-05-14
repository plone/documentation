---
myst:
  html_meta:
    "description": "Internationalization (i18n) and localization (l10n) in Plone 6"
    "property=og:description": "Internationalization (i18n) and localization (l10n) in Plone 6"
    "property=og:title": "Internationalization (i18n) and localization (l10n) in Plone 6"
    "keywords": "Plone, Internationalization, i18n, language, translation, localization"
---

(i18n-l10n-label)=

# Internationalization and Localization

{term}`Internationalization` is the process of preparing an application for displaying content in languages and formats specifically to the audience.
Developers and template authors usually internationalize the application.
"i18n" is shorthand for "internationalization" (the letter "I", a run of 18 letters, the letter "N").

{term}`Localization` is the process of writing the translations of text and local formats for an application that has already been internationalized.
Formats include dates, times, numbers, time zones, units of measure, and currency.
Translators usually localize the application.
"l10n" is shorthand for "localization" (the letter "L", a run of 10 letters, the letter "N").

Plone fully supports internationalization and localization.

```{seealso}
Wikipedia article [Internationalization and localization](https://en.wikipedia.org/wiki/Internationalization_and_localization)
```


(i18n-l10n-supported-languages)=

## Supported languages

Plone supports many language translations in its two frontends.
For Volto, see [`plone/volto`](https://github.com/plone/volto/tree/main/packages/volto/locales).
For Classic UI, see [`collective/plone.app.locales`](https://github.com/collective/plone.app.locales/tree/master/plone/app/locales/locales).

You can contribute new languages to both frontends.


(i18n-l10n-code-versus-content-label)=

## Code versus content

We categorize the things that we want to internationalize and localize in a Plone application into two groups:

1.  **Code-level elements.**
    This includes translations of the user interface elements' text strings and localization.
    The tools used in this group include {term}`gettext`, Plone and Zope {term}`i18n` facilities, and {term}`react-intl`.
    See the chapter {doc}`translating-text-strings`.
2.  **User-generated content.**
    For translating user-generated content, Plone uses the package [`plone.app.multilingual`](https://pypi.org/project/plone.app.multilingual/).
    See the chapter {doc}`translating-content`.


(i18n-l10n-common-concepts-label)=

## Common concepts

When you internationalize and localize a Plone application, there are some common concepts used throughout these processes.


(i18n-l10n-terms-label)=

### Terms

The following terms are used in this documentation.

locale
:   A locale is an identifier, such as a {term}`language tag`, for a specific set of cultural preferences for some country, together with all associated translations targeted to the same native language.

language tag
:   A language tag is a string used as an identifier for a language.
    A language tag may have one or more subtags.
    The basic form of a language tag is `LANGUAGE-[SUBTAG]`.

    ```{seealso}
    -   W3C article [Language tags in HTML and XML](https://www.w3.org/International/articles/language-tags/)
    -   W3C Working Draft [Language Tags and Locale Identifiers for the World Wide Web](https://www.w3.org/TR/ltli/)
    ```

`.po`
:   Portable Object (PO) file.
    The message file format used by the {term}`gettext` translation system.
    See https://www.gnu.org/savannah-checkouts/gnu/gettext/manual/html_node/PO-Files.html.

`.pot`
:   Portable Object (PO) template file, not yet oriented towards any particular language.

`.mo`
:   Machine Object file.
    The binary message file compiled from the {term}`.po` message file.


(i18n-l10n-locale-and-language-tag-conventions-label)=

### Locale and language tag conventions

Plone uses certain conventions for its locales and language tags.

-   When identifying a language only, use two lowercase letters.
    Examples: `en`, `de`.
-   When identifying a language and a country, use two lowercase letters, an underscore (`_`), and two uppercase letters.
    Examples: `en_GB`, `pt_BR`.
-   When identifying a language and script or character set, use two lowercase letters, an at sign (`@`), and four title case letters.
    Example: `sr@Cyrl`.


(i18n-l10n-general-procedure-label)=

### General procedure

```{note}
This section concerns only *code-level* translations of text strings.

For *user-generated content* translations, see {doc}`translating-content`.
```

In general, the process of internationalization and localization of a Plone application follows these steps.

1.  Create translatable strings in your code.
    Plone has already done this step within its core code.
    However, when developing new features or add-ons, you will need to perform this step.
2.  Find and extract all translatable strings from your code with a script, and create a `.pot` template file out of all these.
3.  Create the `.po` files for all locales.
4.  Edit the `.po` files, adding the translated messages into them.
5.  Turn the `.po` files into `.mo` files.
6.  Compile and link the `.mo` files with the gettext library.

```{seealso}
[Overview of GNU `gettext`](https://www.gnu.org/software/gettext/manual/html_node/Overview.html)
```


(i18n-l10n-implementation-details-label)=

## Implementation details

Depending on which part of your Plone application that you internationalize and localize, there are different implementation details and tools that are used.
These differences depend upon the programming language, either Python or JavaScript, being used by that part.

-   For the Plone 6 frontend {term}`Volto`, see {doc}`/volto/development/i18n`.
    Volto is based on the JavaScript library React, and uses both {term}`react-intl` and {term}`gettext`.
-   For the rest of Plone 6, see {doc}`translating-text-strings`.
    This is based on Python, and uses {term}`gettext`.
-   For user-generated content translations, see {doc}`translating-content`.



(i18n-l10n-contents-label)=

## Contents

```{toctree}
:maxdepth: 1

translating-text-strings
language-negotiation
language-negotiation-volto
translating-content
contributing-translations
resync-translations
```

