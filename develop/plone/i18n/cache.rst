====================================
Internationalization and cache
====================================

.. admonition:: Description

    Using Plone translation facilities in the presence of caching.

.. contents:: :local:

Introduction
============

You need to have the following monkey-patch in place if you intend to use
LinguaPlone (translated content) with front-end caching servers. Otherwise
CSS, JS and media files will have a language cookie set on them, preventing
cache from working.

.. note::

    This is a well-known Plone issue.

Example::

    from ZPublisher.HTTPRequest import HTTPRequest

    LanguageTool._old___call__ = LanguageTool.__call__

    def LanguageTool__call__(self, container, req):
        """The __before_publishing_traverse__ hook.

        Patched to *not* set the language cookie, as this breaks the site model.

        """
        self._old___call__(container, req)
        if not isinstance(req, HTTPRequest):
            return None
        response = req.response
        if 'I18N_LANGUAGE' in response.cookies:
            if 'set_language' in req.form:
                return None
            del response.cookies['I18N_LANGUAGE']

    LanguageTool.__call__ = LanguageTool__call__

More info

* http://stackoverflow.com/questions/5715216/why-plone-3-sets-language-cookie-to-css-js-registry-files-and-how-to-get-rid-of
