---
myst:
  html_meta:
    "description": "When translating content items in Plone you can connect to an external translation service to have your content translated."
    "property=og:description": "When translating content items in Plone you can connect to an external translation service to have your content translated."
    "property=og:title": "Use an external translation service to translate content"
    "keywords": "Plone, Internationalization, i18n, language, translate, content, localization"
---

(use-an-external-translation-service-label)=

# Use an external translation service to translate content

When translating content items in Plone you can connect to an external translation service to have your content translated.


## Using Google Cloud Translation API

The plone.app.multilingual product that turns Plone into a multilingual-content site, supports [Google Cloud Translation API](https://cloud.google.com/translate/docs/reference/rest), which allows the content editor to use its translations.

The site administrator, needs to create a project in Google Cloud, enable the Cloud Translation API, and create an API key under the Credentials of the Google Cloud Console.

This API key, can be entered in the Multilingual Settings Control Panel in Plone.

After doing so, when the content editor is editing a translation of a given content page, an icon will be shown next to the original content.

When clickin on such icon, the Google Cloud Translation API will be invoked, and the translation obtained through the service entered automatically in the corresponding field.

```{note}
The usage of Google Cloud Translation API may create extra cost for the site administrator.
```


## Using other translation services

If the site administrator doesn't want to use Google Cloud Translation API but some other service, they will need to override the view that makes the call to Google Cloud Translation API.

To do so plone.app.multilingual registers a view called `gtranslation_service`, its code lies on [plone.app.multilingual.brwoser.translate.gtranslation_service_dexterity](https://github.com/plone/plone.app.multilingual/blob/master/src/plone/app/multilingual/browser/translate.py#L52)

This view gets 3 parameters:

- context_uid: the UID of the object to be translated.
- field: the name of the field of the object that needs to be translated. It's this view's job to extract the value of that field from the object.
- lang_source: the source language code.

The first part of the view (the one that gets the object and the field content to be translated), can be copied from the original code, only the call to the translation service will need to be written.

The required code would be something like this:

```python

class TranslateUsingMyService(BrowserView):
    def __call__(self):
        if self.request.method != "POST" and not (
            "field" in self.request.form.keys()
            and "lang_source" in self.request.form.keys()
        ):
            return _("Need a field")
        else:
            manager = ITranslationManager(self.context)
            context_uid = self.request.form.get("context_uid", None)
            if context_uid is None:
                # try with context if no translation uid is present
                manager = ITranslationManager(self.context)
            else:
                catalog = getToolByName(self.context, "portal_catalog")
                brains = catalog(UID=context_uid)
                if len(brains):
                    context = brains[0].getObject()
                    manager = ITranslationManager(context)
                else:
                    manager = ITranslationManager(self.context)

            registry = getUtility(IRegistry)
            settings = registry.forInterface(
                IMultiLanguageExtraOptionsSchema, prefix="plone"
            )
            lang_target = ILanguage(self.context).get_language()
            lang_source = self.request.form["lang_source"]
            orig_object = manager.get_translation(lang_source)
            field = self.request.form["field"].split(".")[-1]
            if hasattr(orig_object, field):
                question = getattr(orig_object, field, "")
                if hasattr(question, "raw"):
                    question = question.raw
            else:
                return _("Invalid field")

            # And here do the call to the external translation service
            return call_to_my_service(question, lang_target, lang_source)
```


```{note}
Due to the way that the Google Translate integration is built in plone.app.multilingual, you will need to enter something in the Google Translate API Key field, in the Multilingual Settings of your site. It doesn't need to be a valid Google Translate API Key, it can be a random string.
```
