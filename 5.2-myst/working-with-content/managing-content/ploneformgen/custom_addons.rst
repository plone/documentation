=====================================================
Adding Custom Fields, Action Adapters or Thanks Pages
=====================================================

.. admonition:: Description

    You may add custom fields, action adapters and thanks pages
    to PloneFormGen. By far the easiest way to do this is to derive
    a subclass from one of the field types in fieldsBase or an
    action adapter from actionAdapter.FormActionAdapter.

When PFG is installed, or reinstalled, it will automatically add
to its available fields, adapters and thanks pages list any installed
Archetypes content type that implements one of:

* Products.PloneFormGen.interfaces.actionAdapter.IPloneFormGenActionAdapter

* Products.PloneFormGen.interfaces.field.IPloneFormGenField

* Products.PloneFormGen.interfaces.thanksPage.IPloneFormGenThanksPage

Also, the Archetypes class *must* specify a meta_type in the class definition
that matches the meta_type defined in its GS type declaration. Otherwise, it
won't be found.