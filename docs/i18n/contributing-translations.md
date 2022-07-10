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

You can fork the repository and work from there.


## Updating Translations

If you want to test your latest translation with unreleased packages containing i18n fixes, get the buildout as follows, updating it for your versions:

```shell
cd ~/buildouts # or wherever you want to put things
git clone -b 6.0 https://github.com/plone/buildout.coredev ./plone6devel
virtualenv --no-site-packages plone6devpy
cd plone6devel
../plone6devpy/bin/pip install -r requirements.txt
../plone6devpy/bin/buildout bootstrap
bin/buildout -c experimental/i18n.cfg
bin/instance fg
```

To update the buildout later, use the following commands:

```shell
git pull
bin/develop up -f
```

To update your translation, change your working directory to `locales`:

```shell
cd src/plone.app.locales/plone/app/locales/
```

Here you have the following directories:

-   `locales` used for core Plone translations.
-   `locales-addons` used for some add-ons packages.

Open the `.po` file with [poedit](https://poedit.net/), [Virtaal](http://virtaal.translatehouse.org/), or [any other i18n tool](https://docs.translatehouse.org/projects/localization-guide/en/latest/guide/tools/trans_editors.html).

For example for French:

```shell
poedit locales/fr/LC_MESSAGES/plone.po
```

Please do a `git pull` before editing a `.po` file to be sure you have the latest version.


### Committing Directly

You can commit your translation from the `locales` directory:

```shell
git commit -a -m "Updated French translation"
git push
```


### Creating a Pull Request

If you do not have commit access on GitHub [collective group](https://github.com/collective), you can do the following:

-   Login to GitHub.
-   Go to GitHub [plone.app.locales](https://github.com/collective/plone.app.locales).
-   Press {guilabel}`Fork`.
    GitHub creates a copy of `plone.app.locales` package for you.
-   Then on your computer in `plone.app.locales`, do a special git push to your own repository:

    ```shell
    git push git@github.com:YOURUSERNAMEHERE/plone.app.locales.git
    ```

-   Go to GitHub `https://github.com/YOURUSERNAME/plone.app.locales`.
-   Press {guilabel}`Create Pull request`.
    Fill it in.

The request will appear for `plone.app.locales` authors.

If it does not get merged in a timely manner, ask on the Plone Community Forum category [Translations and i18n/l10n](https://community.plone.org/c/development/i18nl10n).


## Resyncing translations

When an i18n fix is done in the code, you need to regenerate the `.pot` file and resync the `.po` files from this `.pot` file.

There is a `bin/i18n` command to resync the `.po` files for the different i18n domains.
[See its `README.txt` file for how to use it](https://github.com/collective/plone.app.locales/blob/master/utils/README.txt).

To release a new `plone.app.locales` version, [read `RELEASING.rst`](https://github.com/collective/plone.app.locales/blob/master/utils/RELEASING.rst).


## Support

Please ask questions on the Plone Community Forum category [Translations and i18n/l10n](https://community.plone.org/c/development/i18nl10n).
