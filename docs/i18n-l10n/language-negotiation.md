---
html_meta:
  "description": "Accessing and changing the language state of Plone programmatically."
  "property=og:description": "Accessing and changing the language state of Plone programmatically."
  "property=og:title": "Language negotiation"
  "keywords": "Plone, Internationalization, i18n, language, negotiation, translation, localization"
---

(language-negotiation-label)=

# Language negotiation

```{note}
TODO: rework this section.
```

```{admonition} Description
Accessing and changing the language state of Plone programmatically.
```


## Introduction

Language negotiation is a function of the HTTP protocol which lets a server choose among several language versions of a page, based on the URL and on preference information sent by the browser.

Plone uses specific negotiation rules to negotiate the language in which provides the user interface to the end user. In any case, we have to distinguish two different cases here: when plone.app.multilingual is enabled and when not

### plone.app.multilingual is not enabled

When the referenced product is not installed but the Site Administrator configures multiple languages in Plone, Plone assumes that the user only wants to allow to change the user interface language. 

This means that the language change links on the top of the page will only have effect in the user interface presented to the user. For example: search form options, editing interface messages, portal message statuses, ...

Going to the @@language-controlpanel the site administrator has multiple options with which can influence the working of the site. 

For instance, by default the "Always show language selector" option is not enabled, but it is required if the user wants to offer the language change in the interface. Going to the "Negotiation scheme" in the same configuration page, the Site Administrator can influence how Plone will decide which language to present to each user. 

For instance, if the site is being presented in a subfolder with the language code (think of www.domain.com/en) or in subdomain (think of en.domain.com), Plone can be configured to take that subfolder or domain language code and select that language to present to the user.

Another common configuration is to use the browser language request negotiation. This means that Plone relies on the `Accept-Language` HTTP header sent by the user browser (which previously can be configured to set the list of the wanted languages in rank of preference). For example a user can configure her browser to request pages in German (de), French (fr), and English (en). In such a case Plone will compare Plone's language list with the user requirements, and will decide in which language to present the site.

The exact working of each of the negotiation options is implemented in the `LanguageUtility` which lies in `plone.i18n.utility.py`.

Plone also sets a language cookie with the language preference of the user. This cookie called `I18N_LANGUAGE` must be declared as a `Technical Cookie` and is a session cookie, which means that will be deleted after the user has leave the site. To obey the cookie the setting "Use cookie for manual override" should be set along with the "Set cookie for manual override".

In any case, building websites with user interfaces in multiple languages is a hard work due to the different expectations of the users and the difficulty of the configuration.

### plone.app.multilingual is enabled

When plone.app.multilingual is enabled, Plone creates the so called `Language Root Folder`s (LRFs for short) for each of the languages, so the language negotiation only applies for the users visiting the root domain of the site.

For example, if 'en' and 'es' are enabled, Plone will create www.domain.com/en and www.domain.com/es, and Plone will assume that all the content below 'en' is in English and all content below 'es' is in Spanish, so it will rely on that assumption to present the user interface in those languages when the user is browsing those parts of the site.

As we will see in the (translating-content-label)= section, Plone will set a special view for the Plone root object called `@@language-switcher` whose implementation lies on `plone.app.multilingual.browser.switcher.LanguageSwitcher`. This language switcher will only rely on the user preferred language to decide where to send the user when she visits the root of the site.

If an integrator wants to modify this behavior to always send a user to a given language, or wants to negotiate the language selection in some other way (using the domain, a cookie, or some other techniques), she will have to override that `@@language-swicher` view, or will have to write her own view and set it as the `default view method` in the `Plone Site` object configuration in `www.domain.com/portal_types/Plone Site/manage_workspace`


