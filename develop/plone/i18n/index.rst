============================
Internationalization (i18n)
============================

There are several layers involved in the processes that provide
internationalization capabilities to Plone. Basically they are divided in the
ones responsible to translate the user interface and the display of the
localization particularities (dates, etc):

* Translating user interface text strings by using term:`gettext`, like the
  `zope.i18n`_ and `zope.i18nmessageid`_ packages.

* Adapting locale-specific settings (such as the time format) for the site,
  like the `plone.i18n`_ package.

And the ones responsible for translating the user generated content. There are
several add-on products that provides multilingual support to Plone:

* `Products.LinguaPlone`_ (Archetypes content types based only)

* `plone.app.multilingual`_ (Archetypes and Dexterity content types, requires
  at least Plone 4.1)

.. _zope.i18n: http://pypi.python.org/pypi/zope.i18n
.. _zope.i18nmessageid: http://pypi.python.org/pypi/zope.i18nmessageid
.. _plone.i18n: http://pypi.python.org/pypi/plone.i18n
.. _Products.LinguaPlone: http://pypi.python.org/pypi/Products.LinguaPlone
.. _plone.app.multilingual: http://pypi.python.org/pypi/plone.app.multilingual

Contents
========
.. toctree::
    :maxdepth: 1

    internationalisation
    language
    translating_content
    contribute_to_translations
    cache
