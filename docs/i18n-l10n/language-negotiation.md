---
myst:
  html_meta:
    "description": "Accessing and changing the language state of Plone programmatically."
    "property=og:description": "Accessing and changing the language state of Plone programmatically."
    "property=og:title": "Language negotiation in Classic UI"
    "keywords": "Plone, Internationalization, i18n, language, negotiation, translation, localization"
---

(language-negotiation-label)=

# Language negotiation in Classic UI

```{todo}
This section may contain incorrect information.
If you find errors, please submit a pull request to correct them.
```

Language negotiation is a function of the HTTP protocol.
It lets a server choose among several language versions of a page based on the URL and preference information sent by the browser.

Plone Classic UI uses specific rules to select the language in which the user interface is presented to the end user.
There are two distinct use cases: when `plone.app.multilingual` is not enabled and when it is.


(language-negotiation-plone.app.multilingual-is-not-enabled-label)=

## `plone.app.multilingual` is not enabled

When `plone.app.multilingual` is not installed, but the site administrator configures multiple languages in Plone, Plone only allows changing the language of the user interface.
This means that the language chooser links on the top of the page will only have effect for the user interface elements presented to the user.
These user interface elements may include search form options, editing interface messages, portal message statuses, and so on.

By visiting the URI `@@language-controlpanel` ({guilabel}`Site Setup > General > Language`), the site administrator may configure language options for the site.

```{image} /_static/i18n-l10n/language-controlpanel-general.png
:alt: Language Control Panel, General
```

```{todo}
Should we document all the options?
Currently this is incomplete.
```

```{todo}
The next sentence might not be true.
When I toggled it, nothing changed.
Does it actually do anything?
```

By default, the {guilabel}`Always show language selector` option is not enabled, but it is required if the user wants to offer the language change in the interface.

By selecting the {guilabel}`Negotiation scheme` tab, the site administrator can configure how Plone will select a language to present to each user.

```{image} /_static/i18n-l10n/language-controlpanel-negotiation-scheme.png
:alt: Language Control Panel, Negotiation scheme
```

For instance, if the site is being presented in a sub-folder (`www.domain.com/en`) or in a subdomain (`en.domain.com`), with either example using a language code such as `en`, then Plone can be configured to take that sub-folder or subdomain as the language code, and select that language to present to the user.

Another common configuration is to use the browser language request negotiation.
This means that Plone relies on the `Accept-Language` HTTP header sent by the user's browser.
The user can configure the list of languages to use in their preferred order, such as German (de), French (fr), and English (en).
In this scenario, Plone will compare its language list with the user's preferences, and will determine in which language to present the site.

The exact working of each of the negotiation options is implemented in the class [`LanguageUtility`](https://github.com/plone/plone.i18n/blob/fc05eb4c131574fd8a4353d5346e17866b3a5e2c/plone/i18n/utility.py#L73) in the module `utility.py` in the package `plone/plone.i18n`.

Plone also sets a cookie with the language preference of the user.
This cookie is called `I18N_LANGUAGE`.
It must be declared as a "technical cookie".
It is a session cookie, which means that it will be deleted after the user leaves the site.
To obey the cookie setting, {guilabel}`Use cookie for manual override` should be set along with {guilabel}`Set the language cookie always`.

Building websites with user interfaces in multiple languages is complicated due to the different expectations of the users and the difficulty of the configuration.

As we will see in the {doc}`translating-content` chapter, Plone will set a special view for the Plone root object called `@@language-switcher` whose implementation relies on `plone.app.multilingual.browser.switcher.LanguageSwitcher`.
This language switcher will only rely on the user preferred language to decide where to send the user when they visit the root of the site.


(language-negotiation-plone.app.multilingual-is-enabled-label)=

## `plone.app.multilingual` is enabled

When `plone.app.multilingual` is enabled, Plone creates the `Language Root Folder`s (LRFs) for each of the languages.
Thus, the language negotiation only applies for the users visiting the root domain of the site.

For example, if `en` and `es` are enabled, Plone will create `www.domain.com/en` and `www.domain.com/es`.
Plone will assume that all the content below `en` is in English, and all content below `es` is in Spanish.
It will rely on that assumption to present the user interface in those languages when the user is browsing those parts of the site.

As we will see in the {doc}`translating-content` chapter, Plone will set a special view for the Plone root object called `@@language-switcher` whose implementation relies on `plone.app.multilingual.browser.switcher.LanguageSwitcher`.
This language switcher will only rely on the user preferred language to decide where to send the user when they visit the root of the site.

An integrator may want to modify this behavior to always send a user to a given language, or to negotiate the language selection in some other way, such as using the domain, a cookie, or some other techniques.
As such, there are two options.

-   They may override the `@@language-switcher` view.
-   They may write their own view, and configure the ZMI.
    To configure the ZMI, visit `www.domain.com/portal_types/Plone%20Site/manage_propertiesForm` or navigate there as an Admin user, {guilabel}`username > Site Setup`, {guilabel}`Advanced > Management Interface`, {guilabel}`portal_types`, and finally {guilabel}`Plone Site`.
    Set the value of `Default view method` to the name of the view.


## Changing the default behavior

If for any reason you want to change the default behavior set when using `plone.app.multilingual`, you have two options.

1.  Override the `language-switcher` view.
    Plone has a view called `language-switcher` defined in [plone.app.multilingual.browser.switcher.py](https://github.com/plone/plone.app.multilingual/blob/master/src/plone/app/multilingual/browser/switcher.py) which handles the redirection from the root of the Plone site to the proper Language Root Folder.
    You can override this view using the usual techniques to provide your own implementation.

1.  Create a new view.
    You can create your own view with your own implementation, configure it properly, and then set it as a `default view` for `Plone Site` objects.
    To do so, you may need to provide your own installation profile with a {file}`Plone Site.xml` file and with the proper configuration.
