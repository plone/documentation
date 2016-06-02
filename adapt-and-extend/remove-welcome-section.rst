Remove "Welcome!" section from splash page
==========================================

Two methods to remove the auto-generated Welcome! section from root splash page.


The Basics
----------

In Plone 5, an auto-generated Welcome! section is created on a root splash page if its short name is "front-page". This happens because of a `Diazo theme rule`_ tied with a condition to Plone's default home page, something like this:

::

    <!-- include view @@hero on homepage only -->
    <after css:theme="#mainnavigation-wrapper" css:content=".principal" href="/@@hero"
        css:if-content="body.template-document_view.section-front-page" />


Two ways to remove this section include:

1. Creating a new splash page with different name
-------------------------------------------------

#. Simply add a new page in the root folder and give it a short name other than "front-page". Easier yet: you can just rename default homepage's shortname with ``Edit > Settings``.
#. Upon saving this new page (or renaming old one), you can then press "Display" from the toolbar and select "Change content item as default view…"
#. Finally select the radio button of your new page and press Save.

2. Duplicating theme and removing line of code
----------------------------------------------

#. Go to site setup
#. Press "Theming"
#. Press "Copy" on the Barceloneta theme, give it any short title and description and you can activate it now or later. Press Create.
#. Click on "rules.xml" to open this file in the browser.
#. Find and delete the rule mentioned above:
   <after css:theme="#mainnavigation-wrapper" css:content=".principal" href="/@@hero" css:if-content="body.template-document_view.section-front-page" />

Then to finish up...

#. Press the blue "Save" button, then press "Back to control panel".
#. If you’ve not already activated it, press "Activate", then "Clear Cache" on your new theme.

.. _`Diazo theme rule`: https://github.com/plone/plonetheme.barceloneta/blob/master/plonetheme/barceloneta/theme/rules.xml
