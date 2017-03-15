========================
Translating text strings
========================

.. admonition:: Description

    Translating Python and TAL template source code text strings using
    the term:`gettext` framework and other Plone/Zope term:`i18n` facilities.


Introduction
============

Internationalization is a process to make your code locale- and language-aware.
Usually this means supplying translation files for text strings used in the code.

Plone internally uses the UNIX standard term:`gettext` tool to perform :term:`i18n`.

There are two separate gettext systems. Both use the :term:`.po` file format to describe translations.

Note that this chapter concerns only *code-level* translations.
*Content* translations are managed by the :doc:`plone.app.multilingual </external/plone.app.multilingual/README>` add-on product.

zope.i18n
=========

See also `zope.i18n on pypi <https://pypi.python.org/pypi/zope.i18n>`_

* Follows term:`gettext` best practices

* Translations are stored in the ``locales`` folder of your application.
  Example: ``locales/fi/LC_MESSAGES/your.app.po``

* Has `zope.i18nmessageid <https://pypi.python.org/pypi/zope.i18nmessageid>`_ package, which provides a string-like class which allows storing the translation domain with translatable text strings.

* ``.po`` files must usually be manually converted to ``.mo`` binary files every time the translations are updated.  See :term:`i18ndude`. (It is also possible to set an environment variable to trigger recompilation of ``.mo`` files; see below.)

Plone (at least 3.3) uses only filename and path to search for the translation files.
Information in the ``.po`` file headers is ignored.

Generating a ``.pot`` template file for your package(s)
--------------------------------------------------------

`infrae.i18nextract <https://pypi.python.org/pypi/infrae.i18nextract>`_ can be used in your buildout to create a script which searches particular packages for translation strings.
This can be particularly useful for creating a single *translations* package which contains the translations for the set of packages which make up your application.

Add the following to your ``buildout.cfg``:

.. code-block:: ini

    [translation]
    recipe = infrae.i18nextract
    packages =
       myapplication.policy
       myapplication .theme
    output = ${buildout:directory}/src/myapplication.translation/myapplication/translation/locales
    output-package = myapplication.translations
    domain = mypackage

Running the ``./bin/translation-extract`` script will produce a ``.pot`` file in the specified output directory which can then be used to create the ``.po`` files for each translation:

.. code-block:: console

   msginit --locale=fr --input=locales/mypackage.pot --output=locales/fr/LC_MESSAGES/mypackage.po

The ``locales`` directory should contain a directory for each language, and a directory called ``LC_MESSAGES`` within each of these, followed by the corresponding ``.po`` files containing the translation strings:

.. code-block:: sh

   ./locales/en/LC_MESSAGES/mypackage.po
   ./locales/fi/LC_MESSAGES/mypackage.po
   ./locales/ga/LC_MESSAGES/mypackage.po


Marking translatable strings in Python
---------------------------------------

Each module declares its own ``MessageFactory`` which is a callable and marks strings with translation domain.
``MessageFactory`` is declared in the main ``__init__.py`` file of your package.

.. code-block:: python

    from zope.i18nmessageid import MessageFactory

    # your.app.package must match domain declaration in .po files
    MessageFactory = MessageFactory('youpackage.name')

You also need to have the following ZCML entry:

.. code-block:: xml

    <configure xmlns:i18n="http://namespaces.zope.org/i18n">
        <i18n:registerTranslations directory="locales" />
    </configure>

After the setup above you can use message factory to mark strings with translation domains.
``i18ndude`` translation utilities use underscore ``_`` to mark translatable strings (term:`gettext` message ids).
Message ids must be unicode strings.

.. code-block:: python

    from your.app.package import yourAppMessageFactory as _
    my_translatable_text = _(u"My text")

The object will still look like a string::

    >>> my_translatable_text
    u'My text'

But in reality it is a ``zope.i18nmessageid.message.Message`` object::

    >>> my_translatable_text.__class__
    <type 'zope.i18nmessageid.message.Message'>

    >>> my_translatable_text.domain
    'your.app.package'

To see the translation::

    >>> from zope.i18n import translate
    >>> translate(my_translatable_text)
    u"The text of the translation." # This is the corresponding msgstr from the .po file


Marking translatable strings in TAL page templates
---------------------------------------------------

Declare XML namespace ``i18n`` and translation domain at the beginning of your template, at the first element

.. code-block:: html

    <div id="mobile-header" xmlns:i18n="http://xml.zope.org/namespaces/i18n" i18n:domain="plomobile">

Translate element content text using ``i18n:translate=""``. It will use the text content of the
element as msgid.

.. code-block:: html

          <li class="heading" i18n:translate="">
              Sections
          </li>

* Use attributes i18n:translate, i18n:attributes and so on

For examples look at any core Plone .pt files

Automatically translated message ids
-------------------------------------

Plone will automatically perform translation for message ids which are output in page templates.

The following code would translate ``my_translateable_text`` to the native language activated for the current page.

.. code-block:: xml

    <span tal:content="view/my_translateable_text">

.. Note:: Since ``my_translateable_text`` is a
    ``zope.i18nmessageid.message.Message`` instance containing its own
    gettext domain information, the ``i18n:domain`` attribute in page
    templates does not affect message ids declared through message
    factories.

Manually translated message ids
-------------------------------

If you need to manipulate translated text outside page templates, you need to perform the final translation manually.

Translation always needs context (i.e. under which site the translation happens), as the active language and other preferences are read from the HTTP request object and site object settings.

Translation can be performed using the ``context.translate()`` method::

    # Translate some text
    msgid = _(u"My text") # my_text is zope.

    # Use inherited translate() function to get the final text string
    translated = self.context.translate(msgid)

    # translated is now u"Käännetty teksti" (in Finnish)

``context.translate()`` uses the ``translate.py`` Python script from
``LanguageTool``.

It has the signature::

    def translate(self, domain, msgid, mapping=None, context=None,
          target_language=None, default=None):

and does the trick::

    from Products.CMFCore.utils import getToolByName

    # get tool
    tool = getToolByName(context, 'translation_service')

    # this returns type unicode
    value = tool.translate(msgid,
                            domain,
                            mapping,
                            context=context,
                            target_language=target_language,
                            default=default)

.. note::

    Translation needs HTTP request object and thus may not work correctly from command-line scripts.


Non-python message ids
----------------------

There are also other message id markers in code outside the Python domain, that have their own mechanisms:

* ZCML entries
* GenericSetup XML
* TAL page templates


Translating browser view names
------------------------------

Often you might want to translate browser view names, so that the "Display" contentmenu shows something more human readable than, for example,
"my_awesome_view".

These are the steps needed to get it translated:

* Use the "plone" domain for your browser view name translations. Wether put the whole ZCML in the plone domain of just the view definitions with
  i18n:domain="plone".

* The msgids for the views are their names. Translate them in a plone.po override file in your locales folder.

Please note, i18ndude does not parse the zcml files for translation strings
(see below "Translating other ZCML").


Translating other ZCML
----------------------

http://stackoverflow.com/questions/6899708/do-zcml-files-get-parsed-i18n-wise


Testing translations
======================

Here is a simple way to check if your gettext domains are correctly loaded.

Plone 4
--------

You can start the Plone debug shell and manually check if translations can
be performed.

First start Plone in debug shell:

.. code-block:: console

    bin/instance debug

and then call translation service, in your site, manually::

    >>> site = app.yoursiteid
    >>> translation_service = site.translation_service
    >>> translation_service.translate("Add Events Portlet", domain="plone", target_language="fi")
    u'Lis\xe4\xe4 Tapahtumasovelma'


Translation string substitution
===============================

*Translation string substitutions* must be used when the final translated
message contains *variable strings*.

Plone content classes inherit the ``translate()`` function which can be used
to get the final translated string.  It will use the currently activate
language.  Translation domain will be taken from the msgid object itself,
which is a string-like ``zope.i18nmessageid`` instance.

Message ids are immutable (read-only) objects so you need to always create a new message id if you use different variable substitution mappings.

Python code::

    from saariselka.app import appMessageFactory as _

    class SomeView(BrowserView):

        def do_stuff(self):

            msgid = _(u"search_results_found_msg", default=u"Found ${results} results", mapping={u"results": len(self.contents)})

            # Use inherited translate() function to get the final text string
            translated = self.context.translate(msgid)

            # Show the final result count to the user as a portal status message
            messages = IStatusMessage(self.request)
            messages.addStatusMessage(translated, type="info")

Corresponding ``.po`` file entry::

    #. Default: "Found ${results} results"
    #: ./browser/accommondationsummaryview.py:429
    msgid "search_results_found_msg"
    msgstr "Löytyi ${results} majoituskohdetta"


For more information, see

* http://wiki.zope.org/zope3/TurningMessageIDsIntoRocks

i18ndude
========

:term:`i18ndude` is a developer-oriented command-line utility to manage
``.po`` and ``.mo`` files.

Usually you build our own shell script wrapper around ``i18ndude`` to automate generation of ``.mo`` files of your product ``.po`` files.

.. note::

    Plone 3.3 and onwards do not need manual ``.po`` -> ``.mo``
    compilation. It is done on start up. Plone 4 has a special switch
    for this: in your ``buildout.cfg`` in the part using
    ``plone.recipe.zope2instance`` you can set an environment variable
    for this::

      environment-vars =
          zope_i18n_compile_mo_files true

    Note that the value does not matter: the code in ``zope.i18n``
    simply looks for the existence of the variable and does not
    care what its value is.

.. Note:: If you use i18ndude make sure to use ``_`` as an alias for
    your ``MessageFactory`` else i18ndude won't find your message strings
    in python code and report that "no entries for domain" were found.

See:

* http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4

Examples:

* `i18ndude Python package <https://pypi.python.org/pypi/i18ndude>`_

* `i18ndude example for Plone 3.0 and later <http://maurits.vanrees.org/weblog/archive/2007/09/i18n-locales-and-plone-3.0>`_

* `i18ndude example for Plone 2.5 <http://blogs.ingeniweb.com/blogs/user/7/tag/i18ndude/>`_

Installing i18ndude
-------------------

The recommended method is to have term:`i18ndude` installed via your `buildout <http://www.buildout.org/docs/index.html>`_.

Add the following to your buildout.cfg:

.. code-block:: cfg

    parts =
        ...
        i18ndude

    [i18ndude]
    unzip = true
    recipe = zc.recipe.egg
    eggs = i18ndude

After this ``i18ndude`` is available in your ``buildout/bin`` folder


.. code-block:: console

        bin/i18ndude -h
        Usage: i18ndude command [options] [path | file1 file2 ...]]

You can also call it relative to your current package source folder

.. code-block:: console

        server:home moo$  cd src/mfabrik.plonezohointegration/
        server:mfabrik.plonezohointegration moo$ ../../bin/i18ndude

.. warning::

    Do not ``easy_install i18ndude``. ``i18ndude`` depends on various Zope packages and pulling them to your system-wide Python configuration could be dangerous, due to potential conflicts with corresponding, but different versions, of the same packages used with Plone.

More information

* http://markmail.org/message/gru5oaxdl452ekh6#query:+page:1+mid:m22a2ap4xwtwogs5+state:results


Setting up folder structure for Finnish and English
---------------------------------------------------

Example:

.. code-block:: console

    mkdir locales
    mkdir locales/fi
    mkdir locales/en
    mkdir locales/fi/LC_MESSAGES
    mkdir locales/en/LC_MESSAGES

Creating ``.pot`` base file
----------------------------

Example:

.. code-block:: console

    i18ndude rebuild-pot --pot locales/mydomain.pot --create your.app.package .


Manual ``.po`` entries
------------------------

``i18ndude`` scans source ``.py`` and ``.pt`` files for translatable text strings.
On some occasions this is not enough - for example if you dynamically generate message ids in your code.
Entries which cannot be detected by automatic code scan are called *manual po entries*.
They are managed in ``locales/manual.pot`` which is merged to generated ``locales/yournamespace.app.pot`` file.

Here is a sample ``manual.pot`` file::

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


Managing ``.po`` files
-----------------------

Example shell script to manage i18n files. Change ``CATALOGNAME`` to reflect the actual package of your product:

The script will:

* pick up all changes to i18n strings in code and reflect them back to the
  translation catalog of each language;

* pick up changes in ``manual.pot`` file and reflect them back to the
  translation catalog of each language.

.. code-block:: sh

    #!/bin/sh
    #
    # Shell script to manage .po files.
    #
    # Run this file in the folder main __init__.py of product
    #
    # E.g. if your product is yourproduct.name
    # you run this file in yourproduct.name/yourproduct/name
    #
    #
    # Copyright 2010 mFabrik http://mfabrik.com
    #
    # https://plone.org/documentation/manual/plone-community-developer-documentation/i18n/localization
    #

    # Assume the product name is the current folder name
    CURRENT_PATH=`pwd`
    CATALOGNAME="yourproduct.app"

    # List of languages
    LANGUAGES="en fi de"

    # Create locales folder structure for languages
    install -d locales
    for lang in $LANGUAGES; do
        install -d locales/$lang/LC_MESSAGES
    done

    # Assume i18ndude is installed with buildout
    # and this script is run under src/ folder with two nested namespaces in the package name (like mfabrik.plonezohointegration)
    I18NDUDE=../../../../bin/i18ndude

    if test ! -e $I18NDUDE; then
            echo "You must install i18ndude with buildout"
            echo "See https://github.com/collective/collective.developermanual/blob/master/source/i18n/localization.txt"
            exit
    fi

    #
    # Do we need to merge manual PO entries from a file called manual.pot.
    # this option is later passed to i18ndude
    #
    if test -e locales/manual.pot; then
            echo "Manual PO entries detected"
            MERGE="--merge locales/manual.pot"
    else
            echo "No manual PO entries detected"
            MERGE=""
    fi

    # Rebuild .pot
    $I18NDUDE rebuild-pot --pot locales/$CATALOGNAME.pot $MERGE --create $CATALOGNAME .


    # Compile po files
    for lang in $(find locales -mindepth 1 -maxdepth 1 -type d); do

        if test -d $lang/LC_MESSAGES; then

            PO=$lang/LC_MESSAGES/${CATALOGNAME}.po

            # Create po file if not exists
            touch $PO

            # Sync po file
            echo "Syncing $PO"
            $I18NDUDE sync --pot locales/$CATALOGNAME.pot $PO


            # Plone 3.3 and onwards do not need manual .po -> .mo compilation,
            # but it will happen on start up if you have
            # registered the locales directory in ZCML
            # For more info see http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4

            # Compile .po to .mo
            # MO=$lang/LC_MESSAGES/${CATALOGNAME}.mo
            # echo "Compiling $MO"
            # msgfmt -o $MO $lang/LC_MESSAGES/${CATALOGNAME}.po
        fi
    done

.. note::

    Remember to register the ``locales`` directory in ``configure.zcml``
    for automatic ``.mo`` compilation as instructed above.

More information

* http://plataforma.cenditel.gob.ve/browser/proyectosInstitucionales/eGov/ppm/trunk/rebuild_i18n

* http://encolpe.wordpress.com/2008/04/28/manage-your-internationalization-with-i18ndude/

Distributing compiled translations
===================================

The rule for compiled .mo files is that

* Source code repositories (SVN, Git) must not contain compiled .mo files

* Released eggs on PyPi, however, **must** contain compiled .mo files

The easiest way to manage this is to use the `zest.releaser <https://pypi.python.org/pypi/zest.releaser>`_ tool together with `zest.pocompile package <https://pypi.python.org/pypi/zest.pocompile>`_ to release your eggs.

Dynamic content
===============

If your HTML template contains dynamic content such as

.. code-block:: html

    <h1 i18n:translate="search_form_heading">Search from <span tal:content="context/@@plone_portal_state/portal_title" /></h1>

it will produce ``.po`` entry::

    msgstr "Hae sivustolta <span>${DYNAMIC_CONTENT}</span>"

You need to give the name to the dynamic part

.. code-block:: html

    <h1 i18n:translate="search_form_heading">
    Search from
    <span i18n:name="site_title"
          tal:content="context/@@plone_portal_state/portal_title" /></h1>

... and then you can refer the dynamic part by a name::

    #. Default: "Search from <span>${site_title}</span>"
    #: ./skins/gomobiletheme_basic/search.pt:46
    #: ./skins/gomobiletheme_plone3/search.pt:46
    msgid "search_form_heading"
    msgstr "Hae sivustolta ${site_title}

More info


* http://permalink.gmane.org/gmane.comp.web.zope.plone.collective.cvs/111531

Overriding translations
========================

If you need to change a translation from a ``.po`` file, you could create a new python package and register your own ``.po`` files.

To do this, create the package and add a ``locales`` directory in there, along the lines of what `plone.app.locales`_ does.
Then you can add your own translations in the language that you need; for example ``locales/fr/LC_MESSAGES/plone.po`` to override French messages in the ``plone`` domain.

Reference the translation in ``configure.zcml`` of your package:

.. code-block:: xml

    <configure xmlns:i18n="http://namespaces.zope.org/i18n"
               i18n_domain="my.package">
        <i18n:registerTranslations directory="locales" />
    </configure>

Your ZCML needs to be included *before* the one from `plone.app.locales <https://pypi.python.org/pypi/plone.app.locales>`_: the first translation of a msgid wins.
To manage this, you can include the ZCML in the buildout:

.. code-block:: cfg

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

See the *Overriding Translations* section of Maurits van Rees's `blog entry on Plone i18n <http://maurits.vanrees.org/weblog/archive/2010/10/i18n-plone-4>`_, and Vincent Fretin's `posting <http://article.gmane.org/gmane.comp.web.zope.plone.user/109580>`_ on the Plone-Users mailing list.


Other
=====

* http://reinout.vanrees.org/weblog/2007/12/14/translating-schemata-names.html

* https://plone.org/products/archgenxml/documentation/how-to/handling-i18n-translation-files-with-archgenxml-and-i18ndude/view?searchterm=

* http://vincentfretin.ecreall.com/articles/my-translation-doesnt-show-up-in-plone-4


