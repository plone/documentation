====================
Translated content
====================

.. admonition:: Description

    Translating content items in Plone, creating translations
    programmatically and working with translators.

.. contents:: :local:

Introduction
=============

Plone doesn't ships (yet) out of the box with a multilingual solution for
translating user generated content. There are several add-on products that add
multilingual support to Plone. Each of them has its own features and drawbacks,
so be careful when you choose one for your project and be sure that it fulfills
your needs.

LinguaPlone
===========

`LinguaPlone add-on product <https://plone.org/products/linguaplone>`_ has been
the defacto standard multilingual product for Plone for almost a decade. It's
well stablished, proven, tested and reliable solution. However, it has no
support for Dexterity based content types and nowadays it's on legacy mode (only
bugfixes).

For an example of a content type using LinguaPlone, see the `LinguaItem
example type
<https://github.com/plone/Products.LinguaPlone/blob/07c754012e942fe5e12834b51af06246932ce420/Products/LinguaPlone/examples/LinguaItem.py>`_.


Translation-aware content types
-------------------------------

LinguaPlone makes it possible to mark fields *language independent* or
*language dependent*.

.. note::

    To have language-aware behavior, you need to use the
    ``Products.LinguaPlone.public.*`` API, instead of
    ``Products.Archetypes.atapi.*``.

Example::

    try:
        from Products.LinguaPlone import public as atapi
    except ImportError:
        # No multilingual support
        from Products.Archetypes import atapi

    class MyContent(atapi.ATContent):
        pass

    atapi.registerType(MyContent, ...)


For more information, see:

* https://pypi.python.org/pypi/Products.LinguaPlone/3.1a2#language-independent-fields

* http://n2.nabble.com/languageIndependent-fields-not-updated-td2430489.html

Getting content items in another language
-----------------------------------------

Possible use cases:

- Getting translated content items by known path. E.g. you could have a
  content item called ``portal/footer``, which dynamically shows translated
  text for different languages.

- Displaying content in many languages simultaneously.

To show some content translated into the chosen language of the current
user, you can use ``ITranslatable.getTranslation(language='language')``:
Return the object corresponding to a translated version or None.
If called without arguments it returns the translation in the currently
selected language, or self.

Example::

    from zope.component.hooks import getSite

    from Products.LinguaPlone.interfaces import ITranslatable


    def get_root_relative_item_in_current_language(path):
        """
        Traverses to a site item from the portal root
        and then returns a translated copy of it in the current language.

        Returns None if the item does not exist.

        Example::

            get_root_relative_item_in_current_language(self.context, "subfolder/item")

        """

        site = getSite()

        try:
            obj = site.restrictedTraverse("path")
        except:
            return None

        if ITranslatable.providedBy(obj):
            translated = obj.getTranslation()
            if translated:
                return translated

        return obj


Translating content
-------------------

LinguaPlone contains some unit test code which shows how to create
translations.  You can use the ``context.addTranslation(language_code)`` and
``context.getTranslation(language_code)`` methods.

Example::

    from Products.LinguaPlone.I18NBaseObject import AlreadyTranslated

    try:
        object.addTranslation(lang)
    except AlreadyTranslated:
        # Note: AlreadyTranslated is always raised if Products.Linguaplone is not installed
        pass

    translated = object.getTranslation(lang)


See https://github.com/plone/Products.LinguaPlone/blob/07c754012e942fe5e12834b51af06246932ce420/Products/LinguaPlone/tests/translate_edit.txt

.. todo:: Why link to a particular (ancient) tag?

Language neutral links
----------------------

In many cases you want to create links to a different language content.
For example, fallback to English content when the native version of content is not available.

Plone's reference and link widgets often fail to create links between language barriers.

Here is a workaround

* Create a folder in the site root

* Set the folder language neutral on Edit > Metadata tab

* In this folder, create Link content items where the Link target is the
  English content. Also, on the link item Metadata set its Language to neutral.

* These links are searcable regardless of the edited content language and can be
  used in references in the widgets

* When the end user, not editor, clicks link the Link content type takes
  him/her to the actual English content

You may also find `redturtle.smartlink <https://pypi.python.org/pypi/redturtle.smartlink/>`_
as useful add-on.

Serving translated content from a correct domain name
-----------------------------------------------------

The following applies if:

* You use one Plone instance to host a site translated into several
  languages;
* the Plone instance is mapped to different domain names;
* the language is resolved based on the top-level domain name or the
  subdomain.

For SEO and usability reasons, you might want to force certain content to
show up at a certain domain.  Plone does not prevent you from accessing a
path such as ``/news`` on the Finnish domain, or ``/uutiset`` on English
domain.  If these URLs leak to search engines, they cause confusion.

Below is a complex post-publication hook which redirects users to the
proper domain for the language being served::

    """ Domain-aware language redirects.

        Redirect the user to the domain where the language should be
        served from, if they have been mixing and matching different domain
        names and language versions.

        http://mfabrik.com
    """

    import urlparse

    from zope.interface import Interface
    from zope.component import adapter, getUtility, getMultiAdapter
    from plone.postpublicationhook.interfaces import IAfterPublicationEvent

    from gomobile.mobile.utilities import get_host_domain_name
    from gomobile.mobile.interfaces import IMobileRequestDiscriminator, MobileRequestType

    from Products.CMFCore.interfaces import IContentish

    def get_contentish(object):
        """ Traverse acquisition upwards until we get a contentish object used for the HTTP response.
        """

        contentish = object

        while not IContentish.providedBy(contentish):
            if not hasattr(contentish, "aq_parent"):
                break
            contentish = contentish.aq_parent

        return contentish


    def redirect_domain(request, response, new_domain):
        """ Redirect user to a new domain, with the URI intact.

        It also keeps the port.

        @param new_domain: New domain name to redirect, without port.
        """

        url = request["ACTUAL_URL"]
        parts = urlparse.urlparse(url)

        # Replace domain name
        parts = list(parts)
        netloc = parts[1]

        # TODO: Handle @ and HTTP Basic auth here
        if ":" in netloc:
            domain, port = netloc.split(":")
            netloc = new_domain + ":" + port
        else:
            netloc = new_domain

        parts[1] = netloc
        new_url = urlparse.urlunparse(parts)

        # Make 301 Permanent Redirect response
        response.redirect(new_url, status=301)
        response.body = ""
        response.setHeader("Content-length", 0)


    def ensure_in_domain(request, response, language_now, wanted_language, wanted_domain):
        """ Make sure that a certain language gets served from the correct domain.

        If the user tries to access URI of page, and the page language
        does not match the domain we expect, redirect the user to the
        correct domain.
        """

        domain_now = get_host_domain_name(request)

        if language_now == wanted_language:
            if domain_now != wanted_domain:
                # print "Fixing language " + language_now + " to go to " + wanted_domain + " from " + domain_now
                redirect_domain(request, response, wanted_domain)


    @adapter(Interface, IAfterPublicationEvent)
    def language_fixer(object, event):
        """ Redirect mobile users to mobile site using gomobile.mobile.interfaces.IRedirector.

        Note: Plone does not provide a good hook for doing this before
        traversing, so we must do it in post-publication. This adds extra
        latency, but is doable.
        """

        # print "language_fixer"

        request = event.request
        response = request.response
        context = get_contentish(object)

        if hasattr(context, "Language"):
            # Check whether the context has a Language() accessor, to get
            # the original language:
            language_now = context.Language()

            #print "Resolving mobility"
            discriminator = getUtility(IMobileRequestDiscriminator)
            flags = discriminator.discriminate(context, request)

            if MobileRequestType.MOBILE in flags:
                # Do mobile
                ensure_in_domain(request, response, language_now, "fi", "m.mfabrik.fi")
                ensure_in_domain(request, response, language_now, "en", "mfabrik.mobi")
            else:
                # Do web
                ensure_in_domain(request, response, language_now, "fi", "mfabrik.fi")
                ensure_in_domain(request, response, language_now, "en", "mfabrik.com")

        # print "Done"

Translated navigation tabs
--------------------------

Below is an example code which allows you to translate
portal_tabs to the current language.

* All translatable navigation tabs must be explicitly declared in portal_actions / portal_tabs
  using site root relative paths

* You must set ``disable_folder_sections`` to ``False`` in navtree_properties

* Source is modified from `The default sections viewlet <https://github.com/plone/plone.app.layout/blob/master/plone/app/layout/viewlets/common.py#L151>`_

* The viewlet is created using :doc:`Grok </appendices/grok>` framework

Viewlet code::

    """

        For more information see

        * http://collective-docs.readthedocs.org/en/latest/views/viewlets.html

    """

    import logging

    # Zope imports
    from zope.component import getMultiAdapter, getUtility, queryMultiAdapter
    from five import grok
    from AccessControl import getSecurityManager
    from AccessControl import Unauthorized

    # Plone imports
    from plone.app.layout.viewlets.interfaces import IPortalHeader

    # Add-ons
    from Products.LinguaPlone.interfaces import ITranslatable

    grok.templatedir("templates")
    grok.layer(IThemeSpecific)

    # By default, set context to zope.interface.Interface
    # which matches all the content items.
    # You can register viewlets to be content item type specific
    # by overriding grok.context() on class body level
    grok.context(Interface)

    logger = logging.getLogger("Sections")


    class Sections(grok.Viewlet):
        """
        Override tabs navigation to support multilingual items.

        - All items in portal_actions / portal_tabs are mapped to their native langauge version
          thru LinguaPlone translation linking

        - To skip the generatd default top level navigation content (automatically generated from the site root)
          set disable_folder_sections to False in navtree_properties

        """

        # Override existing plone.global_sections
        grok.name("plone.global_sections")
        grok.viewletmanager(IPortalHeader)

        def translateTabs(self, tabs):
            """
            Check with LinguaPlone to get the tab item in the target language
            """

            portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")

            portal = portal_state.portal()

            new_tabs = []

            for action in tabs:
                url = action["url"]

                if url.startswith("/"):
                    # Assume site root relative link
                    url = url[1:]
                    try:
                        context = portal.restrictedTraverse(url)
                    except Unauthorized:
                        # No permission - filter out
                        logger.warn("Unauthorized item:" + url)
                        pass
                    except AttributeError:
                        # Item does not exist
                        logger.warn("Navigation item does not exist:" + url)
                        continue

                    translatable = ITranslatable(context)

                    # Get item in the current language
                    translation = translatable.getTranslation()
                    if translation:
                        # Override menu item with translatd version URL
                        action["url"] = translation.absolute_url()
                        # Get the translated title directly from the content
                        action["title"] = translation.Title()
                    else:
                        # No translation - filter out
                        continue

                new_tabs.append(action)

            return new_tabs

        def update(self):
            context = self.context.aq_inner
            portal_tabs_view = getMultiAdapter((context, self.request),
                                               name='portal_tabs_view')
            self.portal_tabs = portal_tabs_view.topLevelTabs()

            self.portal_tabs = self.translateTabs(self.portal_tabs)

            self.selected_tabs = self.selectedTabs(portal_tabs=self.portal_tabs)
            self.selected_portal_tab = self.selected_tabs['portal']

        def selectedTabs(self, default_tab='index_html', portal_tabs=()):
            """
            """

            portal_state = getMultiAdapter((self.context, self.request), name="plone_portal_state")

            plone_url = portal_state.portal_url()
            plone_url_len = len(plone_url)
            request = self.request
            valid_actions = []

            url = request['URL']
            path = url[plone_url_len:]

            for action in portal_tabs:
                if not action['url'].startswith(plone_url):
                    # In this case the action url is an external link. Then, we
                    # avoid issues (bad portal_tab selection) continuing with next
                    # action.
                    continue
                action_path = action['url'][plone_url_len:]
                if not action_path.startswith('/'):
                    action_path = '/' + action_path
                if path.startswith(action_path + '/'):
                    # Make a list of the action ids, along with the path length
                    # for choosing the longest (most relevant) path.
                    valid_actions.append((len(action_path), action['id']))

            # Sort by path length, the longest matching path wins
            valid_actions.sort()
            if valid_actions:
                return {'portal': valid_actions[-1][1]}

        return {'portal': default_tab}


Page template code

.. code-block:: html

    <tal:sections tal:define="portal_tabs viewlet/portal_tabs"
         tal:condition="portal_tabs"
         i18n:domain="plone">
        <h5 class="hiddenStructure" i18n:translate="heading_sections">Sections</h5>

        <ul id="portal-globalnav"
            tal:define="selected_tab python:viewlet.selected_portal_tab"
            ><tal:tabs tal:repeat="tab portal_tabs"
            ><li tal:define="tid tab/id"
                 tal:attributes="id string:portaltab-${tid};
                                class python:selected_tab==tid and 'selected' or 'plain'"
                ><a href=""
                   tal:content="tab/name"
                   tal:attributes="href tab/url;
                                   title tab/description|nothing;">
                Tab Name
                </a></li></tal:tabs></ul>
    </tal:sections>

plone.app.multilingual
======================

plone.app.multilingual was designed originally to provide Plone a whole
multilingual story. Using ZCA technologies, enables translations to Dexterity
and Archetypes content types as well managed via an unified UI.

This module provides the user interface for managing content translations. It's
the app package of the next generation Plone multilingual engine. It's designed
to work with Dexterity content types and the *old fashioned* Archetypes based
content types as well. It only works with Plone 4.1 and above due to the use of
UUIDs for referencing the translations.

For more information see :doc:`plone.app.multilingual</external/plone.app.multilingual/docs/index>`

Installation
------------

To use this package with both Dexterity and Archetypes based content types you
should add the following line to your *eggs* buildout section::

    eggs =
        plone.app.multilingual[archetypes, dexterity]

If you need to use this package only with Archetypes based content types you
only need the following line::

    eggs =
        plone.app.multilingual[archetypes]

While archetypes is default in Plone for now, you can strip ``[archetypes]``.
This may change in future so we recommend adding an appendix as shown above.

Setup
-----

After re-running your buildout and installing the newly available add-ons, you
should go to the *Languages* section of your site's control panel and select
at least two or more languages for your site. You will now be able to create
translations of Plone's default content types, or to link existing content as
translations.

Marking objects as translatables
--------------------------------

Archetypes
^^^^^^^^^^

By default, if PAM is installed, Archetypes-based content types are marked as
translatables

Dexterity
^^^^^^^^^

Users should mark a dexterity content type as translatable by assigning a the
multilingual behavior to the definition of the content type either via file
system, supermodel or through the web.


Marking fields as language independent
--------------------------------------

Archetypes
^^^^^^^^^^

The language independent fields on Archetype-based content are marked the same
way as in LinguaPlone::

    atapi.StringField(
        'myField',
        widget=atapi.StringWidget(
        ....
        ),
        languageIndependent=True
    ),

Dexterity
^^^^^^^^^

There are four ways of achieve it.

Grok directive
``````````````

In your content type class declaration::

    from plone.multilingualbehavior import directives
    directives.languageindependent('field')

Supermodel
``````````

In your content type XML file declaration::

    <field name="myField" type="zope.schema.TextLine" lingua:independent="true">
        <description />
        <title>myField</title>
    </field>

Native
``````

In your code::

    from plone.multilingualbehavior.interfaces import ILanguageIndependentField
    alsoProvides(ISchema['myField'], ILanguageIndependentField)

Through the web
```````````````

Via the content type definition in the *Dexterity Content Types* control panel.

Language get/set via an unified adapter
---------------------------------------

In order to access and modify the language of a content type regardless the
type (Archetypes/Dexterity) there is a interface/adapter::

    plone.multilingual.interfaces.ILanguage

You can use::

    from plone.multilingual.interfaces import ILanguage
    language = ILanguage(context).get_language()

or in case you want to set the language of a content::

    language = ILanguage(context).set_language('ca')

ITranslationManager adapter
---------------------------

The most interesting adapter that p.a.m. provides is:
``plone.multilingual.interfaces.ITranslationManager``.

It adapts any ITranslatable object to provide convenience methods to manage
the translations for that object.

Add a translation
^^^^^^^^^^^^^^^^^

Given an object `obj` and we want to translate it to Catalan language ('ca')::

    from plone.multilingual.interfaces import ITranslationManager
    ITranslationManager(obj).add_translation('ca')

Register a translation for an already existing content
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given an object `obj` and we want to add `obj2` as a translation for Catalan language ('ca')::

    ITranslationManager(obj).register_translation('ca', obj2)

Get translations for an object
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given an object `obj`::

    ITranslationManager(obj).get_translations()

and if we want a concrete translation::

    ITranslationManager(obj).get_translation('ca')

Check if an object has translations
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Given an object `obj`::

    ITranslationManager(obj).get_translated_languages()

or::

    ITranslationManager(obj).has_translation('ca')

For more information see: https://github.com/plone/plone.multilingual/blob/master/src/plone/multilingual/interfaces.py#L66

raptus.multilanguageplone
=========================

Another extension for multilingual content in Plone is
``raptus.multilanguageplone``.  This is not meant to be a fully-fledged tool
for content translaton, unlike LinguaPlone. Translation is done directly in
the edit view of a content type, and provides a widget to use google's
translation API to translate the different fields.

Unlike LinguaPlone, ``raptus.multilanguageplone`` doesn't create an object
for each translation. Instead, it stores the translation on the object
itself and therefor doesn't support translation workflows and language-aware
object paths.

If you have non-default content types, you have to provide your own
``multilanguagefields`` adapter.

See https://svn.plone.org/svn/collective/raptus.multilanguagefields/trunk/raptus/multilanguagefields/samples/

Installation
------------

Installation of ``raptus.multilanguageplone`` is straight-forward with
buildout. If the site already contains articles then you have to migrate
them.

See https://pypi.python.org/pypi/raptus.multilanguagefields

Switching from Linguaplone
--------------------------

If you want to switch from Linguaplone to ``raptus.multilanguageplone`` be
aware that you will lose already translated content.

1. Uninstall ``Products.Linguaplone``.
2. Unfortunately Linguaplone does not uninstall cleanly. Two utilities
   remain in your database. You can remove them in an interactive session
   from your site (in this example, the site has the id ``plone``)::

       (Pdb) site = plone.getSiteManager()
       (Pdb) from plone.i18n.locales.interfaces import IContentLanguageAvailability
       (Pdb) utils = site.getAllUtilitiesRegisteredFor(IContentLanguageAvailability)
       (Pdb) utils
       [<plone.i18n.locales.languages.ContentLanguageAvailability object at 0xb63c4cc>,
       <ContentLanguages at /plone/plone_app_content_languages>,
       <Products.LinguaPlone.vocabulary.SyncedLanguages object at 0xfa32e8c>,
       <Products.LinguaPlone.vocabulary.SyncedLanguages object at 0xfa32eac>]
       (Pdb) utils = utils[:-2]
       (Pdb) del site.utilities._subscribers[0][IContentLanguageAvailability]

   Repeat the procedure for ``IMetadataLanguageAvailability`` and commit the
   transaction::

       (Pdb) import transaction
       (Pdb) site._p_changed = True
       (Pdb) site.utilities._p_changed = True
       (Pdb) transaction.commit()
       (Pdb) app._p_jar.sync()   # if zeo setup

3. Run buildout without Linguaplone and restart.
4. Run the *import* step of the Plone Language Tool. Otherwise language
   switching will not work.
5. Install ``raptus.multilanguageplone`` using buildout and
   ``portal_quickinstaller``.
6. Migrate the content.
