================================================
Creating forms without programming: PloneFormGen
================================================

.. admonition :: Description

   PloneFormGen allows you to build and maintain convenience forms through Plone edit interface.

Introduction
============

*PloneFormGen* is a Plone add-on Product that provides a generic Plone form generator using fields, widgets and validators from Archetypes.
Use it to build, one-of-a-kind, web forms that save or mail form input.

To build a web form, create a form folder, then add form fields as contents.
Individual fields can display and validate themselves for testing purposes.
The form folder creates a form from all the contained field content objects.

Final disposition of form input is handled via plug-in action products.

Action adapters included with this release include a mailer, a save-data adapter that saves input in tab-separated format for later download,
and a custom-script adapter that makes it possible to script simple actions without recourse to the Management Interface.

To make it easy to get started, newly created form folders are pre-populated to act as a simple e-mail response form.

* `PloneFormGen product page <https://plone.org/products/ploneformgen>`_

Getting started with PloneFormGen
---------------------------------

.. toctree::
    :maxdepth: 2

    getting_started

PloneFormGen topics
-------------------

.. toctree::
    :maxdepth: 1

    installation
    override_defaults
    custom_validators
    select_mail
    restyle
    javascript
    custom_thanks
    request
    multipage
    captcha
    faq

Advanced topics
---------------

.. toctree::
    :maxdepth: 1

    sql_crud
    gpg
    embedding
    custom_addons
    creating_content
    custom_mailer
    failsafe_email
