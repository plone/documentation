---
myst:
  html_meta:
    "description": "Translating text strings in Plone"
    "property=og:description": "Translating text strings in Plone"
    "property=og:title": "Translating text strings"
    "keywords": "Plone, Internationalization, i18n, language, translation, localization"
---

(translating-text-strings-label)=

# Translating text strings

```{todo}
This chapter may contains outdated or incorrect information.
Please submit a pull request to make a correction.
```

```{note}
This chapter concerns only *code-level* translations of text strings.

For *user-generated content* translations, see {doc}`translating-content`.
```

This chapter describes how to translate Python and TAL template source code text strings using the {term}`gettext` framework and other Plone/Zope {term}`i18n` facilities.

Plone internally uses the UNIX standard {term}`gettext` tool to perform {term}`i18n`.


(translating-text-strings-zope.i18n-label)=

## `zope.i18n`

The package `zope.i18n` implements several APIs related to internationalization and localization.

-   Follows {term}`gettext` best practices.
-   Translations are stored in the `locales` folder of your application, such as `locales/fi/LC_MESSAGES/your.app.po`.
-   Uses the package [`zope.i18nmessageid`](https://pypi.org/project/zope.i18nmessageid/).
    This provides a string-like class which allows storing the translation domain with translatable text strings.
-   {term}`PO file`s must usually be manually converted to binary {term}`MO file`s every time the translations are updated.
    See {term}`i18ndude`.
    It is also possible to set an environment variable to trigger recompilation of MO files.
    See {ref}`translating-text-strings-i18ndude-label` below for details.

```{seealso}
[`zope.i18n` on PyPI](https://pypi.org/project/zope.i18n/)
```

Plone searches only the filename and path for the translation files.
Information in the PO file headers is ignored.


(translating-text-strings-generating-a-.pot-template-file-for-your-packages-label)=

### Generating a `.pot` template file for your packages

[`i18ndude`](https://pypi.org/project/i18ndude/) should be used to create a script which searches particular packages for translation strings.

If you have created your add-on using [bobtemplates.plone](https://pypi.org/project/bobtemplates.plone/), then you will already have a script `update.sh` inside your package and a script `update_locale` in your buildout to extract the messages from your code.

After running that script, a new `domain.pot` file will be created in your `locales` directory where all the messages will be saved. 

To have those messages translated into some languages, you will need to create a language directory inside the `locales` directory, and a `LC_MESSAGES` directory inside it.
This follows the gettext standard.
After doing that, the directory structure will be as follows.

```console
./locales/en/LC_MESSAGES/domain.po
./locales/fi/LC_MESSAGES/domain.po
./locales/ga/LC_MESSAGES/domain.po
```

You will need to provide your translations in those `domain.po` files. 

If you add, update, or remove strings in your package, you will need to run only the `update.sh` script to update all language files.

You also need to have the following ZCML entry to signal Plone that the files stored in the `locales` folder follow the gettext standard and that it needs to use them when requesting translated strings.

```xml
<configure xmlns:i18n="http://namespaces.zope.org/i18n">
    <i18n:registerTranslations directory="locales" />
</configure>
```


(translating-text-strings-marking-translatable-strings-in-python-label)=

### Marking translatable strings in Python

You will need to declare you own `MessageFactory`.
This is a callable that marks strings with a translation domain.
`MessageFactory` is usually declared in the main `__init__.py` file of your package.
It is imported from wherever it is needed in your package.
`_` is the standard name that is used in gettext to identify the translation function, and the previous scripts will use that assumption to identify translatable strings.

```python
from zope.i18nmessageid import MessageFactory

# your.app.package must match domain declaration in .po files
_ = MessageFactory('youpackage.name')
```

Now you can use the message factory to mark strings with translation domains.

```python
from your.app.package import _
my_translatable_text = _("My text")
```

The object will still look like a string:

```pycon
>>> my_translatable_text
u'My text'
```

But in reality, it is a `zope.i18nmessageid.message.Message` object:

```pycon
>>> my_translatable_text.__class__
<type 'zope.i18nmessageid.message.Message'>

>>> my_translatable_text.domain
'your.app.package'
```

To see the translation in Python code you will need to manually call the `translate` function in `zope.i18n`:

```pycon
>>> from zope.i18n import translate
>>> translate(my_translatable_text)
u"The text of the translation." # This is the corresponding msgstr from the .po file
```


(translating-text-strings-marking-translatable-strings-in-tal-page-templates-label)=

### Marking translatable strings in TAL page templates

Declare the XML namespace `i18n` and translation domain at the beginning of your template, in the first element.

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

The `i18n:translate` attribute will {term}`hook` into the translation machinery, and will look up the corresponding translated string to the one stated there, while looking in the relevant `domain.po` file corresponding to the `i18n:domain` stated in the file and the language negotiated by Plone.


(translating-text-strings-automatically-translated-message-ids-label)=

### Automatically translated message IDs

Plone will automatically perform translation for message IDs which are output in page templates.

The following code translates `my_translateable_text` to the native language activated for the current page.

```xml
<span tal:content="view/my_translateable_text">
```

```{note}
Since `my_translateable_text` is a `zope.i18nmessageid.message.Message` instance containing its own gettext domain information, the `i18n:domain` attribute in page templates does not affect message IDs declared through message factories.
```


(translating-text-strings-manually-translated-message-ids-label)=

### Manually translated message IDs

If you need to manipulate translated text outside page templates, then you need to perform the final translation manually.
This is needed when you are building human-readable strings in Python code, for example when creating some messages that are sent by email to the end user.

Translation always needs context.
That means under which site the translation happens.
The active language and other preferences are read from the HTTP request object and site object settings.

Translation should be performed using the `zope.i18n.translate()` method:

```python
from zope.i18n import translate
from zope.globalrequest import getRequest
# Translate some text
msgid = _("My text") # my_text is zope.

# Use inherited translate() function to get the final text string
translated = translate(msgid, context=getRequest())

# translated is now u"Käännetty teksti" (in Finnish)
```


(translating-text-strings-non-python-message-ids-label)=

### Non-Python message IDs

There are other message ID markers in code outside the Python domain that have their own mechanisms:

-   ZCML entries
-   GenericSetup XML
-   TAL page templates


(translating-text-strings-translation-string-substitution-label)=

## Translation string substitution

Translation string substitutions must be used when the final translated message contains variable strings.

The translation domain will be taken from the `msgid` object itself, which is a string-like `zope.i18nmessageid` instance.

Message IDs are immutable (read-only) objects.
You need to always create a new message ID if you use different variable substitution mappings.
For example, in your view code, you would do the following.

```python
from saariselka.app import _
from zope.i18n import translate
from zope.globalrequest import getRequest

class SomeView(BrowserView):

    def do_stuff(self):

        msgid = _("search_results_found_msg", default=u"Found ${results} results", mapping={u"results": len(self.contents)})

        # Use inherited translate() function to get the final text string
        translated = translate(msgid, context=getRequest())

        # Show the final result count to the user as a portal status message
        messages = IStatusMessage(self.request)
        messages.addStatusMessage(translated, type="info")
```


(translating-text-strings-i18ndude-label)=

## `i18ndude`

{term}`i18ndude` is a developer-oriented command-line utility to manage PO and MO files.

Usually you build our own shell script wrapper around `i18ndude` to automate generation of MO files from your package's PO files.

Plone will automatically compile all PO files to MO files on start up if a specific environment variable is enabled.

In your `buildout.cfg` in the part using `plone.recipe.zope2instance`, you can set an environment variable for this.

```ini
environment-vars =
    zope_i18n_compile_mo_files true
```

Note that the value does not matter.
The code in `zope.i18n` looks for the mere existence of the variable, and does not care what is its value.

If you do not add that environment variable, you will need to provide the MO files in your package.
To make this easier, and if you use [zest.releaser](https://pypi.org/project/zest.releaser/) to publish your packages, you can use [zest.pocompile](https://pypi.org/project/zest.pocompile/).
This script hooks into the release process and builds the MO files for you.


(translating-text-strings-installing-i18ndude-label)=

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


(translating-text-strings-setting-up-folder-structure-for-finnish-and-english-label)=

### Setting up folder structure for Finnish and English

Start by creating folders to hold the translation files.

```console
mkdir locales
mkdir locales/fi
mkdir locales/en
mkdir locales/fi/LC_MESSAGES
mkdir locales/en/LC_MESSAGES
```


(translating-text-strings-creating-.pot-base-file-label)=

### Creating `.pot` base file

Example:

```console
i18ndude rebuild-pot --pot locales/mydomain.pot --create your.app.package .
```


(translating-text-strings-manual-.po-entries-label)=

### Manual PO entries

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


(translating-text-strings-dynamic-content-label)=

## Dynamic content

If your HTML template has dynamic content similar to the following:

```html
<h1 i18n:translate="search_form_heading">Search from <span tal:content="context/@@plone_portal_state/portal_title" /></h1>
```

…then it will produce a PO entry like this:

```po
msgstr "Hae sivustolta <span>${DYNAMIC_CONTENT}</span>"
```

You need to give the name to the dynamic part so the PO file can handle it like a variable:

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
msgstr "Hae sivustolta ${site_title}"
```

```{seealso}
https://web.archive.org/web/20131018150303/http://permalink.gmane.org/gmane.comp.web.zope.plone.collective.cvs/111531
```


(translating-text-strings-overriding-translations-label)=

## Overriding translations

If you need to change a translation from a PO file, you could create a new Python package and register your own PO files.

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

When doing so, you may need to add the following zcml stanza in your package's `configure.zcml` file:

```xml

<include package="Products.CMFPlone" />

```

This **must** go *after* the `registerTranslations` stanza, before any other registration you may have in your package.

It should look like this:

```xml
<configure xmlns:i18n="http://namespaces.zope.org/i18n"
           i18n_domain="my.package">
    <i18n:registerTranslations directory="locales" />
    
    <include package="Products.CMFPlone" />

    <!-- any other registration -->

</configure>
```


See the *Overriding Translations* section of Maurits van Rees's [blog entry on Plone i18n](https://maurits.vanrees.org/weblog/archive/2010/10/i18n-plone-4#overriding-translations).


## Additional resources

-   https://reinout.vanrees.org/weblog/2007/12/14/translating-schemata-names.html
-   https://web.archive.org/web/20100830122331/http://plone.org/products/archgenxml/documentation/how-to/handling-i18n-translation-files-with-archgenxml-and-i18ndude/view?searchterm=
-   https://web.archive.org/web/20170810113554/http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4
