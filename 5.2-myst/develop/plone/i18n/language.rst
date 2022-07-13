==================
Language functions
==================

.. note::

    TODO: rework this section.

.. admonition:: Description

    Accessing and changing the language state of Plone programmatically.


Introduction
============

Each page view has a language associated with it.

The active language is negotiated by the ``plone.i18n.negotiator`` module.
Several factors may be involved in determining what the language should be:

* Cookies (setting from the language selector)

* The top-level domain name (e.g. ``.fi`` for Finnish, ``.se`` for Swedish)

* Context (current content) language

* Browser language headers

Language is negotiated at the beginning of the page view.

Languages are managed by `portal_languagetool <https://github.com/plone/Products.PloneLanguageTool/blob/master/Products/PloneLanguageTool/LanguageTool.py>`_.

Getting the current language
============================

Example view/viewlet method of getting the current language.

.. code-block:: python

    from Products.Five.browser import BrowserView
    from zope.component import getMultiAdapter

    class MyView(BrowserView):

        ...

        def language(self):
            """
            @return: Two-letter string, the active language code
            """
            context = self.context.aq_inner
            portal_state = getMultiAdapter((context, self.request), name=u'plone_portal_state')
            current_language = portal_state.language()
            return current_language


Getting language of content item
================================

All content objects don't necessarily support the ``Language()`` look-up defined by the ``IDublinCore`` interface.
Below is the safe way to extract the served language on the content.

Example BrowserView method::

    from Acquisition import aq_inner

    def language(self):
        """ Get the language of the context.

        Useful in producing <html> tag.
        You need to output language for every HTML page, see http://www.w3.org/TR/xhtml1/#strict

        @return: The two letter language code of the current content.
        """
        portal_state = self.context.unrestrictedTraverse("@@plone_portal_state")

        return aq_inner(self.context).Language() or portal_state.default_language()

Getting available site languages
===================================

Example below::

    # Python 2.6 compatible ordered dict
    # NOTE: API is not 1:1, but for normal dict access of
    # set member, iterate keys and values this is enough
    try:
        from collections import OrderedDict
    except ImportError:
        from odict import odict as OrderedDict

    def getLanguages(self):
        """
        Return list of active langauges as ordered dictionary, the preferred first language as the first.

        Example output::

             {
                u'fi': {u'id' : u'fi', u'flag': u'/++resource++country-flags/fi.gif', u'name': u'Finnish', u'native': u'Suomi'},
                u'de': {u'id' : u'de', u'flag': u'/++resource++country-flags/de.gif', u'name': u'German', u'native': u'Deutsch'},
                u'en': {u'id' : u'en', u'flag': u'/++resource++country-flags/gb.gif', u'name': u'English', u'native': u'English'},
                u'ru': {u'id' : u'ru', u'flag': u'/++resource++country-flags/ru.gif', u'name': u'Russian', u'native': u'\u0420\u0443\u0441\u0441\u043a\u0438\u0439'}
              }
        """
        result = OrderedDict()

        portal_languages = self.context.portal_languages

        # Get barebone language listing from portal_languages tool
        langs = portal_languages.getAvailableLanguages()

        preferred = portal_languages.getPreferredLanguage()

        # Preferred first
        for lang, data in langs.items():
            if lang == preferred:
                result[lang] = data

        # Then other languages
        for lang, data in langs.items():
            if lang != preferred:
                result[lang] = data

        # For convenience, include the language ISO code in the export,
        # so it is easier to iterate data in the templates
        for lang, data in result.items():
            data["id"] = lang

        return result

Simple language conditions in page templates
===============================================

You can do this if full translation strings are not worth the trouble:

.. code-block:: xml

   <div class="main-text">
     <a tal:condition="python:context.restrictedTraverse('@@plone_portal_state').language() == 'fi'" href="http://www.saariselka.fi/sisalto?force-web">Siirry täydelle web-sivustolle</a>
     <a tal:condition="python:context.restrictedTraverse('@@plone_portal_state').language() != 'fi'" href="http://www.saariselka.fi/sisalto?force-web">Go to full website</a>
   </div>


Set site language settings
==========================

Manually::

    # Setup site language settings
    portal = context.getSite()
    ltool = portal.portal_languages
    defaultLanguage = 'en'
    supportedLanguages = ['en','es']
    ltool.manage_setLanguageSettings(defaultLanguage, supportedLanguages,
                                          setUseCombinedLanguageCodes=False)

For unit testing, you need to run this in ``afterSetUp()`` after setting up
the languages::

    # THIS IS FOR UNIT TESTING ONLY
    # Normally called by pretraverse hook,
    # but must be called manually for the unit tests
    # Goes only for the current request
    ltool.setLanguageBindings()

Using ``GenericSetup`` and ``propertiestool.xml``

.. code-block:: xml

    <object name="portal_properties" meta_type="Plone Properties Tool">
       <object name="site_properties" meta_type="Plone Property Sheet">
          <property name="default_language" type="string">en</property>
       </object>
    </object>


Customizing language selector
=============================

Making language flags point to different top level domains
----------------------------------------------------------

If you use multiple domain names for different languages it is often desirable to make the language selector point to a different domain.
Search engines do not really like the dynamic language switchers and will index switching links, messing up your site search results.

Example: TODO


Login-aware language negotiation
================================

By default, language negotiation happens before authentication.
Therefore, if you wish to use authenticated credentials in the negotiation,
you can do the following.

Hook the after-traversal event.

Example event registration

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:zcml="http://namespaces.zope.org/zcml"
        >
        <subscriber handler=".language_negotiation.Negotiator"/>
    </configure>

Corresponding event handler::

    from zope.interface import Interface
    from zope.component import adapter
    from ZPublisher.interfaces import IPubEvent,IPubAfterTraversal
    from Products.CMFCore.utils import getToolByName
    from AccessControl import getSecurityManager
    from zope.app.component.hooks import getSite

    @adapter(IPubAfterTraversal)
    def Negotiator(event):

        # Keep the current request language (negotiated on portal_languages)
        # untouched

        site = getSite()
        ms = getToolByName(site, 'portal_membership')
        member = ms.getAuthenticatedMember()
        if member.getUserName() == 'Anonymous User':
            return

        language = member.language
        if language:
            # Fake new language for all authenticated users
            event.request['LANGUAGE'] = language
            event.request.LANGUAGE_TOOL.LANGUAGE = language
        else:
            lt = getToolByName(site, 'portal_languages')
            event.request['LANGUAGE'] = lt.getDefaultLanguage()
            event.request.LANGUAGE_TOOL.LANGUAGE = lt.getDefaultLanguage()

Other
=====

* http://reinout.vanrees.org/weblog/2007/12/14/translating-schemata-names.html

* http://maurits.vanrees.org/weblog/archive/2007/09/i18n-locales-and-plone-3.0

* http://blogs.ingeniweb.com/blogs/user/7/tag/i18ndude/

* https://plone.org/products/archgenxml/documentation/how-to/handling-i18n-translation-files-with-archgenxml-and-i18ndude/view?searchterm=



