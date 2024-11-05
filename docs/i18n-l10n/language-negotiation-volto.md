---
myst:
  html_meta:
    "description": "Accessing and changing the language state of Plone programmatically."
    "property=og:description": "Accessing and changing the language state of Plone programmatically."
    "property=og:title": "Language negotiation in Volto"
    "keywords": "Plone, Internationalization, i18n, language, negotiation, translation, localization, volto"
---

(language-negotiation-volto-label)=

# Language negotiation in Volto

Volto does not rely on the configuration set in Plone's Language Control Panel to handle the redirection from the root of the site to the Language Root Folder.

Volto has a setting in its own configuration stating whether a site is multilingual or not: `isMultilingual`.

First of all, you need to set that setting to `true`.

Then you need to add the list of supported languages to the `supportedLanguages` setting, and match them with the languages configured in Plone's Language Control Panel.

As a last thing, you need to set your site's `defaultLanguage` to one of the `supportedLanguages`.

When all these settings are configured, Volto's [`MultilingualRedirector`](https://github.com/plone/volto/blob/main/packages/volto/src/components/theme/MultilingualRedirector/MultilingualRedirector.jsx) will handle the language negotiation and the redirect.

In its configuration, the component tries to match the `I18N_LANGUAGE` cookie set in the user's browser with the list of supported languages, and if the match does not succeed, it selects the default language configured in Volto.

After that it does the redirection to the matched Language Root Folder.

If the site is not configured to be multilingual, Volto doesn't do any redirect.

## Overriding the default behavior

To do so, you need to provide your own `MultilingualRedirector` component {doc}`customizing it </volto/development/customizing-components>`.
