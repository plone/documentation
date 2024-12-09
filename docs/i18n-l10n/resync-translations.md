---
myst:
  html_meta:
    "description": "How to create po files from source code."
    "property=og:description": "How to create po files from source code."
    "property=og:title": "Resync translations"
    "keywords": "Plone, Internationalization, i18n, language, translate, content, localization"
---

(resync-translations-label)=

# Resync translations

This chapter discussions how to resynchronize translations in both the backend and frontend, and how to make releases for each.


## Resync translations in the Plone backend

Plone {term}`PO file`s need to be updated each time a new string is added into the Plone interface or each time one of those strings is updated.
Those translations are not only used in Plone Classic UI, but many of them are also exposed through the REST API to Volto.

Usually the Plone Translations Team updates these PO files.
Here we will explain the procedure to update them.

1.  Clone the relevant branch of [buildout.coredev](https://github.com/plone/buildout.coredev) corresponding to the Plone version you want to update.

2.  Initialize the buildout.

    ```shell
    ./bootstrap.sh
    ```

3.  Run buildout using the `experimental/i18n.cfg` file:

    ```shell
    ./bin/buildout -c experimental/i18n.cfg
    ```

4.  Run the `i18n-update-all` script:

    ```shell
    ./bin/i18n-update-all
    ```

    The script will go through Plone source code and will update all `pot` and `po` files in the `plone.app.locales` package.

5.  Commit the changes and push back to GitHub:

    ```shell
    cd src/plone.app.locales
    git add plone
    git commit -m "Update translation files"
    git push origin
    ```


(create-new-plone.app.locales-release-label)=

## Create a new `plone.app.locales` release

Translators will take care of translating `po` files into their languages.
When the release manager requests to create a new `plone.app.locales` release, the procedure is the following:

1.  Create a virtualenv with `zest.releaser` and `zest.pocompile` installed:

    ```shell
    `which python3.10` -m venv .
    ./bin/pip install zest.releaser zest.pocompile
    source bin/activate
    ```

2.  Go to the `plone.app.locales` directory and pull the changes:

    ```shell
    cd src/plone.app.locales
    git pull
    ```

3.  Verify there is a changelog entry for each change, adding any missing entries if necessary.

4.  Verify there are no errors in the PO files:

    ```shell
        for po in `find . -name "*.po"` ; do msgfmt --no-hash -o `dirname $po`/`basename $po .po`.mo $po; done
    ```

    You can ignore the errors `'msgid' and 'msgstr' entries do not both end with '\n'`.
    If there are other errors, please fix them.

5.  Release.

    ```shell
    fullrelease
    ```

6.  Check that the release is published on PyPI at https://pypi.org/project/plone.app.locales/.

7.  Inform the release manager about the new version.


(resync-translations-volto-label)=

## Resync translations in Volto

In Volto, the GitHub test setup warns a developer when their new contributions require regenerating the translation file.
This is done by running a make command as follows:

```shell
make i18n
```

This will update the PO files and will leave them ready to be translated by translators.


(create-release-volto-translations)=

## Create a release of Volto with the new translations

The Volto release process requires running the same make command as in the previous step.
It will convert the translations in PO files to the JSON files that Volto uses to render the user interface.

```shell
make i18n
```
