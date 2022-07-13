# Internationalization (i18n)

There are several layers involved in the processes that provide
internationalization capabilities to Plone. Basically they are divided in the
ones responsible to translate the user interface and the display of the
localization particularities (dates, etc):

- Translating user interface text strings by using term:`gettext`, like the
  [zope.i18n] and [zope.i18nmessageid] packages.
- Adapting locale-specific settings (such as the time format) for the site,
  like the [plone.i18n] package.

And the ones responsible for translating the user generated content.
Since Plone 5, this is done out of the box with plone.app.multilingual

- [plone.app.multilingual] (Archetypes and Dexterity content types, requires
  at least Plone 4.1)

## Contents

```{toctree}
:maxdepth: 1

internationalisation
language
translating_content
contribute_to_translations
```

[plone.app.multilingual]: https://pypi.python.org/pypi/plone.app.multilingual
[plone.i18n]: https://pypi.python.org/pypi/plone.i18n
[zope.i18n]: https://pypi.python.org/pypi/zope.i18n
[zope.i18nmessageid]: https://pypi.python.org/pypi/zope.i18nmessageid
