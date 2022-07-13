==========
 Dexterity
==========

.. admonition:: Description

    Dexterity content subsystem for Plone: info for the developers.


Introduction
============

Dexterity is a subsystem for content objects. It is the standard content type for Plone 5 and onward and can be already used
with Plone 4.


* :doc:`Dexterity developer manual </external/plone.app.dexterity/docs/index>`

* :doc:`How Dexterity is related to Archetypes </external/plone.app.dexterity/docs/intro>`

mr.bob templates
================

Please see :doc:`bobtemplates.plone page </develop/addons/bobtemplates.plone/README>` for project skeleton templates for Dexterity.

Content creation permissions
=============================

Please read :doc:`dexterity and permissions </external/plone.app.dexterity/docs/advanced/permissions>`

Exclusion from navigation
===========================

This must be enabled separately for Dexterity content types with a behavior.

.. code-block:: xml

    <property name="behaviors">
        <element value="plone.app.content.interfaces.INameFromTitle" />
        <element value="plone.app.dexterity.behaviors.metadata.IBasic"/>
        <element value="plone.app.dexterity.behaviors.exclfromnav.IExcludeFromNavigation"/>
    </property>

Then you can manually also check this property::

    for t in self.tabs:
        nav = None
        try:
            nav = IExcludeFromNavigation(t)
        except:
            pass
        if nav:
            if nav.exclude_from_nav == True:
                # FAQ page - do not show in tabs
                continue


Custom add form/view
======================

Dexterity relies on ``++add++yourcontent.type.name`` traverser hook defined
in ``Products/CMFCore/namespace.py``.

It will look up a multi-adapter using this expression::

    if ti is not None:
        add_view = queryMultiAdapter((self.context, self.request, ti),
                                     name=ti.factory)
        if add_view is None:
            add_view = queryMultiAdapter((self.context, self.request, ti))

The ``name`` parameter is the ``portal_types`` id of your content type.

You can register such an adapter in ``configure.zcml``

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        >

        <adapter
            for="Products.CMFCore.interfaces.IFolderish
                 plone.dexterity.interfaces.IDexterityFTI"
            provides="zope.publisher.interfaces.browser.IBrowserPage"
            factory=".flexicontent.AddView"
            name="your.app.flexiblecontent"
            />

    </configure>


Then you can inherit from the proper ``plone.dexterity`` base classes::

    from plone.dexterity.browser.add import DefaultAddForm, DefaultAddView

    class AddForm(DefaultAddForm):

        def update(self):
            DefaultAddForm.update(self)

        def updateWidgets(self):
            """ """
            # Some custom code here

        def getBlockPlanJSON():
            return getBlockPlanJSON()

    class AddView(DefaultAddView):
        form = AddForm

See also:

* :doc:`FTI </develop/plone/content/types>`

* :doc:`z3c.form </develop/plone/forms/z3c.form>`


Custom edit form
====================

Example::

    from five import grok
    from plone.directives import dexterity

    class EditForm(dexterity.EditForm):

        grok.context(IFlexibleContent)

        def updateWidgets(self):
            """ """
            dexterity.EditForm.updateWidgets(self)

            # XXX: customize widgets here

Registering an edit form works by registering a normal browser page.

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        >

        <browser:page
            for="your.app.flexiblecontent"
            class=".flexicontent.EditView"
            name="edit"
            />

    </configure>

In the example above it is important, that you give the browser page the name "edit".
