==================
Translated content
==================

.. admonition:: Description

    Translating content items in Plone, creating translations
    programmatically and working with translators.


Introduction
============

Plone ships out of the box with a multilingual solution for translating user generated content.

For all practical purposes, you should use that package, plone.app.multilingual

.. note::

    For earlier Plone versions, there were other solutions like LinguaPlone and raptus.multilanguageplone.
    Refer to the `Plone 4 version of this document <http://docs.plone.org/4/en/develop/plone/i18n/translating_content.html>`_ if you need that information.



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

For more information see :doc:`plone.app.multilingual</external/plone.app.multilingual/README>`

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

The language independent fields on Archetype-based content are marked as follows (same as in previous version of Plone with LinguaPlone in place)::

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

    from plone.app.multilingual.dx import directives
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

    from plone.app.multilingual.dx.interfaces import ILanguageIndependentField
    alsoProvides(ISchema['myField'], ILanguageIndependentField)

Through the web
```````````````

Via the content type definition in the *Dexterity Content Types* control panel.

Language get/set via an unified adapter
---------------------------------------

In order to access and modify the language of a content type regardless the
type (Archetypes/Dexterity) there is a interface/adapter::

    plone.app.multilingual.interfaces.ILanguage

You can use::

    from plone.app.multilingual.interfaces import ILanguage
    language = ILanguage(context).get_language()

or in case you want to set the language of a content::

    language = ILanguage(context).set_language('ca')

ITranslationManager adapter
---------------------------

The most interesting adapter that p.a.m. provides is:
``plone.app.multilingual.interfaces.ITranslationManager``.

It adapts any ITranslatable object to provide convenience methods to manage
the translations for that object.

Add a translation
^^^^^^^^^^^^^^^^^

Given an object `obj` and we want to translate it to Catalan language ('ca')::

    from plone.app.multilingual.interfaces import ITranslationManager
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

For more information see: https://github.com/plone/plone.app.multilingual/blob/master/src/plone/app/multilingual/interfaces.py#L76



