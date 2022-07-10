---
html_meta:
  "description": "Internationalization (i18n) and localization (l10n) in Plone 6"
  "property=og:description": "Internationalization (i18n) and localization (l10n) in Plone 6"
  "property=og:title": "Internationalization (i18n)"
  "keywords": "Plone, Internationalization, i18n, language, translation, localization"
---

(i18n-label)=

# Internationalization (i18n)

There are several layers involved in the processes that provide internationalization capabilities to Plone.
They are separated into two parts:
 
1.  Code-level elements.
    This includes translations of the user interface and the display of the localization particularities, such as dates and decimal numbers.

    -   Translating user interface text strings uses {term}`gettext`, as in the packages [`zope.i18n`](https://pypi.org/project/zope.i18n/) and [`zope.i18nmessageid`](https://pypi.org/project/zope.i18nmessageid/).
    -   Adapting locale-specific settings, such as the time format, for a Plone site, as in the package [`plone.i18n`](https://pypi.org/project/plone.i18n/).

2.  User-generated content.

    -   For translating user-generated content, Plone uses the package [`plone.app.multilingual`](https://pypi.org/project/plone.app.multilingual/).


(i18n-contents-label)=

## Contents

```{toctree}
:maxdepth: 1

internationalization
language
translating-content
contributing-translations
```

