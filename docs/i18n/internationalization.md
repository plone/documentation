---
html_meta:
  "description": "Translating text strings in Plone"
  "property=og:description": "Translating text strings in Plone"
  "property=og:title": "Translating text strings"
  "keywords": "Plone, Internationalization, i18n, language, translation, localization"
---

(translating-text-strings-label)=

# Translating text strings

```{todo}
This entire chapter contains cruft dating back to Plone 3 in some parts.
It is perfectly fine to purge obsolete information.
```

This chapter describes how to translate Python and TAL template source code text strings using
the {term}`gettext` framework and other Plone/Zope {term}`i18n` facilities.

Internationalization is a process to make your code locale- and language-aware.
Usually this means supplying translation files for text strings used in the code.

Plone internally uses the UNIX standard {term}`gettext` tool to perform {term}`i18n`.

There are two separate gettext systems.
Both use the {term}`.po` file format to describe translations.
This chapter concerns only *code-level* translations.
*Content* translations are managed by the add-on product [plone.app.multilingual](https://pypi.org/project/plone.app.multilingual/).


## `zope.i18n`

The package `zope.i18n` implements several APIs related to internationalization and localization.

-   Follows {term}`gettext` best practices.
-   Translations are stored in the `locales` folder of your application.
    Example: `locales/fi/LC_MESSAGES/your.app.po`
-   Uses the package [`zope.i18nmessageid`](https://pypi.org/project/zope.i18nmessageid/)
    This provides a string-like class which allows storing the translation domain with translatable text strings.
-   `.po` files must usually be manually converted to `.mo` binary files every time the translations are updated.
    See {term}`i18ndude`.
    It is also possible to set an environment variable to trigger recompilation of `.mo` files.
    See {ref}`i18n-i18ndude-label` below for details.

```{seealso}
[`zope.i18n` on PyPI](https://pypi.org/project/zope.i18n/)
```

Plone searches only the filename and path for the translation files.
Information in the `.po` file headers is ignored.


### Generating a `.pot` template file for your packages

[`infrae.i18nextract`](https://pypi.org/project/infrae.i18nextract/) can be used in your buildout to create a script which searches particular packages for translation strings.
This can be particularly useful for creating a single *translations* package which contains the translations for the set of packages which make up your application.

Add the following to your `buildout.cfg`:

```ini
[translation]
recipe = infrae.i18nextract
packages =
  myapplication.policy
  myapplication .theme
output = ${buildout:directory}/src/myapplication.translation/myapplication/translation/locales
output-package = myapplication.translations
domain = mypackage
```

Running the `./bin/translation-extract` script will produce a `.pot` file in the specified output directory, which can then be used to create the `.po` files for each translation:

```shell
msginit --locale=fr --input=locales/mypackage.pot --output=locales/fr/LC_MESSAGES/mypackage.po
```

The `locales` directory should contain a directory for each language, and a directory called `LC_MESSAGES` within each of these, followed by the corresponding `.po` files containing the translation strings:

```console
./locales/en/LC_MESSAGES/mypackage.po
./locales/fi/LC_MESSAGES/mypackage.po
./locales/ga/LC_MESSAGES/mypackage.po
```


### Marking translatable strings in Python

Each module declares its own `MessageFactory` which is a callable and marks strings with a translation domain.
`MessageFactory` is declared in the main `__init__.py` file of your package.

```python
from zope.i18nmessageid import MessageFactory

# your.app.package must match domain declaration in .po files
MessageFactory = MessageFactory('youpackage.name')
```

You also need to have the following ZCML entry:

```xml
<configure xmlns:i18n="http://namespaces.zope.org/i18n">
    <i18n:registerTranslations directory="locales" />
</configure>
```

After the setup above, you can use the message factory to mark strings with translation domains.
`i18ndude` translation utilities use an underscore (`_`) to mark translatable strings ({term}`gettext` message IDs).
Message IDs must be Unicode strings.

```python
from your.app.package import yourAppMessageFactory as _
my_translatable_text = _(u"My text")
```

The object will still look like a string:

```pycon
>>> my_translatable_text
u'My text'
```

But in reality it is a `zope.i18nmessageid.message.Message` object:

```pycon
>>> my_translatable_text.__class__
<type 'zope.i18nmessageid.message.Message'>

>>> my_translatable_text.domain
'your.app.package'
```

To see the translation:

```pycon
>>> from zope.i18n import translate
>>> translate(my_translatable_text)
u"The text of the translation." # This is the corresponding msgstr from the .po file
```


### Marking translatable strings in TAL page templates

Declare the XML namespace `i18n` and translation domain at the beginning of your template, at the first element.

```html
<div id="mobile-header" xmlns:i18n="http://xml.zope.org/namespaces/i18n" i18n:domain="plomobile">
```

Translate an element's text using `i18n:translate=""`.
It will use the text content of the element as `msgid`.

```html
<li class="heading" i18n:translate="">
    Sections
</li>
```

Use attributes `i18n:translate`, `i18n:attributes`, and so on.
For examples, look at any core Plone `.pt` files.


### Automatically translated message IDs

Plone will automatically perform translation for message IDs which are output in page templates.

The following code translates `my_translateable_text` to the native language activated for the current page.

```xml
<span tal:content="view/my_translateable_text">
```

```{note}
Since `my_translateable_text` is a `zope.i18nmessageid.message.Message` instance containing its own gettext domain information, the `i18n:domain` attribute in page templates does not affect message IDs declared through message factories.
```


### Manually translated message IDs

If you need to manipulate translated text outside page templates, you need to perform the final translation manually.

Translation always needs context.
That means under which site the translation happens.
The active language and other preferences are read from the HTTP request object and site object settings.

Translation can be performed using the `context.translate()` method:

```python
# Translate some text
msgid = _(u"My text") # my_text is zope.

# Use inherited translate() function to get the final text string
translated = self.context.translate(msgid)

# translated is now u"Käännetty teksti" (in Finnish)
```

`context.translate()` uses the `translate.py` Python script from `LanguageTool`.
It has the following signature.

```python
def translate(self, domain, msgid, mapping=None, context=None,
      target_language=None, default=None):
```

Here is sample usage.

```python
from Products.CMFCore.utils import getToolByName

# get tool
tool = getToolByName(context, 'translation_service')

# this returns type Unicode
value = tool.translate(domain,
                        msgid,
                        mapping,
                        context=context,
                        target_language=target_language,
                        default=default)
```

```{note}
Translation needs an HTTP request object, and thus may not work correctly from command-line scripts.
```


### Non-Python message IDs

There are other message ID markers in code outside the Python domain that have their own mechanisms:

-   ZCML entries
-   GenericSetup XML
-   TAL page templates


### Translating browser view names

Often you might want to translate browser view names.
For example, the "display" content menu could show something more readable than "my_awesome_view".

These are the steps to translate it:

-   Use the `plone` domain for your browser view name translations.
    Put the whole ZCML in the `plone` domain of just the view definitions, such as
  `i18n:domain="plone"`.
-   The msgids for the views are their names.
    Translate them in a `plone.po` override file in your `locales` folder.

Please note, `i18ndude` does not parse the ZCML files for translation strings.
See https://stackoverflow.com/questions/6899708/do-zcml-files-get-parsed-i18n-wise for details.


## Testing translations

Here is a simple way to check if your gettext domains are correctly loaded.


### Plone 4

You can start the Plone debug shell and manually check if translations can be performed.

First start Plone in debug shell:

```shell
bin/instance debug
```

and then call translation service, in your site, manually:

```pycon
>>> site = app.yoursiteid
>>> translation_service = site.translation_service
>>> translation_service.translate("Add Events Portlet", domain="plone", target_language="fi")
u'Lis\xe4\xe4 Tapahtumasovelma'
```


## Translation string substitution

Translation string substitutions must be used when the final translated message contains variable strings.

Plone content classes inherit the `translate()` function, which can be used to get the final translated string.
It will use the currently active language.
The translation domain will be taken from the `msgid` object itself, which is a string-like `zope.i18nmessageid` instance.

Message IDs are immutable (read-only) objects.
You need to always create a new message ID if you use different variable substitution mappings.
For example, in your view code, you would do the following.

```python
from saariselka.app import appMessageFactory as _

class SomeView(BrowserView):

    def do_stuff(self):

        msgid = _(u"search_results_found_msg", default=u"Found ${results} results", mapping={u"results": len(self.contents)})

        # Use inherited translate() function to get the final text string
        translated = self.context.translate(msgid)

        # Show the final result count to the user as a portal status message
        messages = IStatusMessage(self.request)
        messages.addStatusMessage(translated, type="info")
```

And make a corresponding `.po` file entry.

```po
#. Default: "Found ${results} results"
#: ./browser/accommondationsummaryview.py:429
msgid "search_results_found_msg"
msgstr "Löytyi ${results} majoituskohdetta"
```

```{seealso}
https://web.archive.org/web/20120202220423/http://wiki.zope.org/zope3/TurningMessageIDsIntoRocks
```


(i18n-i18ndude-label)=

## `i18ndude`

{term}`i18ndude` is a developer-oriented command-line utility to manage `.po` and `.mo` files.

Usually you build our own shell script wrapper around `i18ndude` to automate generation of `.mo` files of your package's `.po` files.

````{note}
Plone 3.3 and onwards do not need manual `.po` -> `.mo` compilation.
It is done on start up.
Plone 4 has a special switch for this.
In your `buildout.cfg` in the part using `plone.recipe.zope2instance`, you can set an environment variable for this.

```ini
environment-vars =
    zope_i18n_compile_mo_files true
```

Note that the value does not matter.
The code in `zope.i18n` looks for the existence of the variable and does not care what is its value.
````

```{note}
If you use `i18ndude`, make sure to use `_` as an alias for your `MessageFactory`.
Else `i18ndude` will not find your message strings in Python code and report that "no entries for domain" were found.
```

```{seealso}
https://web.archive.org/web/20170810113554/http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4
```


### Installing i18ndude

The recommended method is to have {term}`i18ndude` installed via your [buildout](https://www.buildout.org/en/latest/).

Add the following to your `buildout.cfg`:

```cfg
parts =
    ...
    i18ndude

[i18ndude]
unzip = true
recipe = zc.recipe.egg
eggs = i18ndude
```

After running buildout, `i18ndude` will be available in your `buildout/bin` folder.

```console
bin/i18ndude -h
Usage: i18ndude command [options] [path | file1 file2 ...]]
```

You can also call it relative to your current package source folder.

```console
server:home moo$  cd src/mfabrik.plonezohointegration/
server:mfabrik.plonezohointegration moo$ ../../bin/i18ndude
```

````{warning}
Do not use `easy_install i18ndude`.
`i18ndude` depends on various Zope packages, and pulling them in to your system-wide Python configuration could be dangerous, due to potential conflicts with corresponding, but different, versions of the same packages used with Plone.

```{seealso}
https://markmail.org/message/gru5oaxdl452ekh6#query:+page:1+mid:m22a2ap4xwtwogs5+state:results
```
````


### Setting up folder structure for Finnish and English

Example:

```console
mkdir locales
mkdir locales/fi
mkdir locales/en
mkdir locales/fi/LC_MESSAGES
mkdir locales/en/LC_MESSAGES
```


### Creating `.pot` base file

Example:

```console
i18ndude rebuild-pot --pot locales/mydomain.pot --create your.app.package .
```


### Manual `.po` entries

`i18ndude` scans source `.py` and `.pt` files for translatable text strings.
On some occasions this is not enough, for example, when you dynamically generate message IDs in your code.
Entries which cannot be detected by an automatic code scan are called {term}`manual .po entries`.
They are managed in `locales/manual.pot`, which is merged into the generated `locales/yournamespace.app.pot` file.

Here is a sample `manual.pot` file.

```po
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=utf-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Plural-Forms: nplurals=1; plural=0\n"
"Preferred-Encodings: utf-8 latin1\n"
"Domain: mfabrik.app\n"

# This entry is used in gomobiletheme.mfabrik  templates for the campaign page header
# It is not automatically picked, since it is referred from external package
#. Default: "Watch video"
msgid "watch_video"
msgstr ""
```


### Managing `.po` files

The following is an example shell script to manage i18n files.
Change `CATALOGNAME` to reflect the actual package of your product.

The script will:

- pick up all changes to i18n strings in code, and reflect them back to the translation catalog of each language;
- pick up changes in `manual.pot` files, and reflect them back to the translation catalog of each language.

```sh
#!/bin/sh
#
# Shell script to manage .po files.
#
# Run this file in the folder main __init__.py of product
#
# E.g. if your product is yourproduct.name
# you run this file in yourproduct.name/yourproduct/name
#
#
# Copyright 2010 mFabrik https://pypi.org/project/mfabrik.webandmobile/
#
# https://docs.plone.org/develop/plone/i18n/index.html
#

# Assume the product name is the current folder name
CURRENT_PATH=`pwd`
CATALOGNAME="yourproduct.app"

# List of languages
LANGUAGES="en fi de"

# Create locales folder structure for languages
install -d locales
for lang in $LANGUAGES; do
    install -d locales/$lang/LC_MESSAGES
done

# Assume i18ndude is installed with buildout
# and this script is run under src/ folder with two nested namespaces in the package name (like mfabrik.plonezohointegration)
I18NDUDE=../../../../bin/i18ndude

if test ! -e $I18NDUDE; then
        echo "You must install i18ndude with buildout"
        echo "See https://github.com/collective/collective.developermanual/blob/master/source/i18n/localization.txt"
        exit
fi

#
# Do we need to merge manual PO entries from a file called manual.pot.
# this option is later passed to i18ndude
#
if test -e locales/manual.pot; then
        echo "Manual PO entries detected"
        MERGE="--merge locales/manual.pot"
else
        echo "No manual PO entries detected"
        MERGE=""
fi

# Rebuild .pot
$I18NDUDE rebuild-pot --pot locales/$CATALOGNAME.pot $MERGE --create $CATALOGNAME .


# Compile po files
for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do

    if test -d $lang/LC_MESSAGES; then

        PO=$lang/LC_MESSAGES/${CATALOGNAME}.po

        # Create po file if not exists
        touch $PO

        # Sync po file
        echo "Syncing $PO"
        $I18NDUDE sync --pot locales/$CATALOGNAME.pot $PO


        # Plone 3.3 and onwards do not need manual .po -> .mo compilation,
        # but it will happen on start up if you have
        # registered the locales directory in ZCML
        # For more info see http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4

        # Compile .po to .mo
        # MO=$lang/LC_MESSAGES/${CATALOGNAME}.mo
        # echo "Compiling $MO"
        # msgfmt -o $MO $lang/LC_MESSAGES/${CATALOGNAME}.po
    fi
done
```

```{note}
Remember to register the `locales` directory in `configure.zcml` for automatic `.mo` compilation as instructed above.
```

```{seealso}
-   https://web.archive.org/web/20120618093810/http://plataforma.cenditel.gob.ve/browser/proyectosInstitucionales/eGov/ppm/trunk/rebuild_i18n
-   https://web.archive.org/web/20140824100121/http://encolpe.wordpress.com/2008/04/28/manage-your-internationalization-with-i18ndude/
```


## Distributing compiled translations

Source code repositories (SVN, Git) must not contain compiled `.mo` files.
Released eggs on PyPI, however, _must_ contain compiled `.mo` files.

The easiest way to manage this is to use the [zest.releaser](https://pypi.org/project/zest.releaser/) tool together with [zest.pocompile package](https://pypi.org/project/zest.pocompile/) to release your eggs.


## Dynamic content

If your HTML template contains dynamic content similar to the following:

```html
<h1 i18n:translate="search_form_heading">Search from <span tal:content="context/@@plone_portal_state/portal_title" /></h1>
```

…then it will produce a `.po` entry:

```po
msgstr "Hae sivustolta <span>${DYNAMIC_CONTENT}</span>"
```

You need to give the name to the dynamic part.

```html
<h1 i18n:translate="search_form_heading">
Search from
<span i18n:name="site_title"
      tal:content="context/@@plone_portal_state/portal_title" /></h1>
```

And then you can refer to the dynamic part by its name:

```po
#. Default: "Search from <span>${site_title}</span>"
#: ./skins/gomobiletheme_basic/search.pt:46
#: ./skins/gomobiletheme_plone3/search.pt:46
msgid "search_form_heading"
msgstr "Hae sivustolta ${site_title}
```

```{seealso}
https://web.archive.org/web/20131018150303/http://permalink.gmane.org/gmane.comp.web.zope.plone.collective.cvs/111531
```


## Overriding translations

If you need to change a translation from a `.po` file, you could create a new Python package and register your own `.po` files.

To do this, create the package and add a `locales` directory in there, along the lines of what [plone.app.locales](https://pypi.org/project/plone.app.locales/) does.
Then you can add your own translations in the language that you need.
For example, `locales/fr/LC_MESSAGES/plone.po` overrides French messages in the `plone` domain.

Reference the translation in `configure.zcml` of your package:

```xml
<configure xmlns:i18n="http://namespaces.zope.org/i18n"
           i18n_domain="my.package">
    <i18n:registerTranslations directory="locales" />
</configure>
```

Your ZCML needs to be included *before* the one from [plone.app.locales](https://pypi.org/project/plone.app.locales/).
The first translation of a `msgid` wins.
To manage this, you can include the ZCML in the buildout:

```cfg
[instance]
recipe = plone.recipe.zope2instance
user = admin:admin
http-address = 8280
eggs =
    Plone
    my.package
    ${buildout:eggs}
environment-vars =
    zope_i18n_compile_mo_files true
# my.package is needed here so its configure.zcml
# is loaded before plone.app.locales
zcml = my.package
```

See the *Overriding Translations* section of Maurits van Rees's [blog entry on Plone i18n](https://maurits.vanrees.org/weblog/archive/2010/10/i18n-plone-4#overriding-translations).


## Additional resources

-   https://reinout.vanrees.org/weblog/2007/12/14/translating-schemata-names.html
-   https://web.archive.org/web/20100830122331/http://plone.org/products/archgenxml/documentation/how-to/handling-i18n-translation-files-with-archgenxml-and-i18ndude/view?searchterm=
-   https://web.archive.org/web/20170810113554/http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4
