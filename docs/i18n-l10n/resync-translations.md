---
html_meta:
  "description": "How to create po files from source code."
  "property=og:description": "How to create po files from source code."
  "property=og:title": "Resync translations"
  "keywords": "Plone, Internationalization, i18n, language, translate, content, localization"
---

(resync-translations-label)=

## Resync translations

Plone po files need to be updated each time a new string is added into Plone interface, or each time one of those strings is updated.

Usually Translations team handles the update of those po files so you don't need to worry about it. Here we will explain the procedure to update such files.

1. Clone the relevant branch of [buildout.coredev](https://github.com/plone/buildout.coredev) corresponding to the Plone version you want to update.

2. Initialize the buildout.

```bash
./bootstraph.sh
```

3. Run buildout using the `experimental/i18n.cfg` file:

```bash
./bin/buildout -c experimental/i18n.cfg
```

4. Run the `i18n-update-all` script:

```bash
./bin/i18n-update-all
```

The script will go through Plone source code and will update all `pot` and `po` files in the plone.app.locales package.

5. Commit the changes and push back to GitHub:

```bash
cd src/plone.app.locales
git add plone
git commit -m "Update translation files"
git push origin
```

## Create a new plone.app.locales release

Translators will take care of translating `po` files into their languages. When the release manager requests to create a new plone.app.locales release, the procedure is the following:

1. Create a virtualenv with zest.releaser and zest.pocompile installed:

```bash
`which python3.8` -m venv .
./bin/pip install zest.releaser zest.pocompile
source bin/activate
```

2. Go to plone.app.locales directory and pull the changes:

```bash
cd src/plone.app.locales
git pull
```

3. Verify there is a changelog entry for each change, add any missing entries if necessary.


4. Verify there is no errors in the po files:

```bash
    for po in `find . -name "*.po"` ; do msgfmt --no-hash -o `dirname $po`/`basename $po .po`.mo $po; done
```

You can ignore the errors "'msgid' and 'msgstr' entries do not both end with '\n'". If there are other errors, please fix them.

5. Release:

```bash
fullrelease
```

6. Check that the release is published on pypi: https://pypi.org/project/plone.app.locales/

7. Inform the release manager about the new version
