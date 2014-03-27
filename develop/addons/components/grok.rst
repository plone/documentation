================
 Grok framework
================

.. admonition:: Description

        Using Grok framework in Plone programming. Grok
        provides  Dont-Repeat-Yourself API to create
        Zope 3 components easier.

.. contents:: :local:

Introduction
=============

Grok is a project to give sane, easy to use, API to Zope 3 systems.
It exists as standalone, but Plone compatible port five.grok is available for Plone 3.3 and onwards.

Benefits over using pure Zope 3 APIs

* No ZCML files or XML sit-ups needed (except bootstrapping one configure.zcml file)

* More things are automatic and less explicit hand-written code needed. E.g. template file and view class are automatically matched.

* Less code generation

Grok will automatically scan all .py files in your product and
run registration code in them. This way you can use Python decorators
and magical classes to perform tasks which before needed to have
hand written registration code.

More info

* http://grok.zope.org/

* http://pypi.python.org/pypi/five.grok

Tutorial
========

* http://plone.org/products/dexterity/documentation/manual/five.grok

* http://www.martinaspeli.net/articles/using-grok-techniques-in-plone

Using Grok in your package
===========================

configure.zcml - register your package for grokking
------------------------------------------------------

To enable grok'ing for your package:

* The top-level ``configure.zcml`` must include the ``grok`` namespace and
  the ``grok:grok`` directive. You do not need to put
  this directive subpackages. This directive scans your package source tree
  recursively for grok'ed files.

* The package must be loaded using ``setup.py`` auto-include, NOT using a
  ``zcml =`` section in ``buildout.cfg``.
  Otherwise templates are not loaded.

* Optionally, add ``templates`` and ``static`` folders to your package root.

* You still need to include subpackages for old-fashioned :term:`ZCML`
  configurations.

Example

.. code-block:: xml

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:cmf="http://namespaces.zope.org/cmf"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        xmlns:grok="http://namespaces.zope.org/grok"
        i18n_domain="plonetheme.xxx">

      <include package="five.grok" />

      <five:registerPackage package="." initialize=".initialize" />

      <!-- Grok the package to initialise schema interfaces and content classes -->
      <grok:grok package="." />

      <include package=".browser" />

    </configure>

If you are using components from other packages you might also want to add

.. code-block:: xml

    <includeDependencies package="." />

This makes the ``configure.zcml`` and thus Python code
of all modules listed in ``setup.py`` *install_requires*
section is loaded before your module is being processed.

setup.py - include five.grok package dependency for download
--------------------------------------------------------------

You still need to get ``five.grok`` package to your buildout.

Edit your Python egg ``setup.py`` file and list ``five.grok`` as dependency::

    install_requires = ["five.grok", ...],

Re-run buildout. Now buildout should download ``five.grok`` for PyPi and activate it for you.

If you are using Plone 4.1 or older you also need `Dexterity extends = line pindowns in your buildout <http://plone.org/products/dexterity/documentation/how-to/install>`_.
Otherwise you may get *Version Conflict* errors when running buildout.

Plone 4.3 migration and five.grok dependency
=======================================================

Please see `Plone 4.2 -> 4.3 Dexterity upgrade guide <http://plone.org/documentation/manual/upgrade-guide/version/upgrading-plone-4.2-to-4.3/dexterity-optional-extras>`_ first.

Migrating Dexterity and z3c.forms to Plone 4.3
--------------------------------------------------

Plone 4.3 ships with Dexterity. ``five.grok`` is a huge dependency with a lot of
code of which maintenance cannot be guaranteed in the future (`See grok.zope.org <http://grok.zope.org>`_,
`discussion <http://plone.293351.n2.nabble.com/The-grokless-madness-and-unable-to-create-a-simple-form-tp7564179p7564184.html>`_).
Because Plone community cannot commit to maintain this code, but we still want to use the best goodies
of grok based development, some compromises was made for Plone 4.3 regarding grok style forms and directives.

* You can include ``five.grok`` as a dependency, as you have done this far, but it is not going to be
  in Plone default installation in foreseeable future. Please see migration notes.

* ``grok()`` declarations, like ``grok.name()`` in classes are not supported by Plone 4.3 out of the box

* ``plone.directives.form`` goodies distributed to two supported packages: ``plone.supermodel`` and
  ``plone.autoform``

To make your code Plone 4.3 compatible, grokless way do imports as following::

    import z3c.form.form

    from plone.supermodel import model
    from plone.autoform import directives as form
    from plone.autoform.form import AutoExtensibleForm

And you can use them like::

    class IChoiceExamples(model.Schema):
        """ Single choice and multiple choice examples """

        form.widget(multiChoiceCheckbox=CheckBoxFieldWidget)
        multiChoiceCheckbox = zope.schema.List(
            title=u"Checkbox multiple choices",
            ...)


    # Different form base classes are provided:
    # XXX: Fill in here what you should use with Dexterity content types
    class ChoiceExamples(AutoExtensibleForm, z3c.form.form.Form):
        """
        """
        schema = IChoiceExamples

Migrating views from five.grok to plain Plone
------------------------------------------------

If you further want to break the dependency with ``five.grok``
and get rid of ``grok.xxx()`` directives in your classes
here are further dependency.

Remove ``five.grok`` from the dependency list of your egg and remove ``<grok:grok>`` ZCML directive in ``configure.zcml``.

Remove ``from five import grok`` in all of your package modules.

Manually :doc:`register static media folder of your egg </adapt-and-extend/theming/templates_css/resourcefolders>`

Declare views and forms using `configure.zcml <http://developer.plone.org/views/browserviews.html#creating-a-view-using-zcml>`_

Remove ``grok.templatedir()`` and map view classes to templates using ``<browser:page>`` ZCML directive.

Grok migration source example::

    class Demos(grok.View):
        """ Render all demo forms with their widgets in a nice view.

        Read forms which implements IWidgetDemo marke via @widget_demo
        class decocator. Build a nice and useful description string
        for each field in those forms.

        """

        grok.context(ISiteRoot)
        grok.name("widgets-demo")


ZCML migration ``configuration.zcml`` target example::

    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:five="http://namespaces.zope.org/five"
        xmlns:cmf="http://namespaces.zope.org/cmf"
        xmlns:i18n="http://namespaces.zope.org/i18n"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="plone.app.widgets">

      <browser:page
          name="widgets-demo"
          for="Products.CMFCore.interfaces.ISiteRoot"
          class=".demo.Demos"
          permission="zope2.View"
          template="widgets-demo.pt"
          />

    </configure>

.. note ::

    Forms handle ``update()`` themselves - this concerns only non-form views

If your view has ``update()`` method you need to call it manually in ``__call__()``
because ``BrowserView`` base class doesn't do this.

    class MyView(BrowserView):

        def update(self):
            ...

        def __call__(self):
            self.update()
            return self.index()  # Or self.render() for grok.CodeView

More info
===========

Tutorials

* http://plone.org/products/dexterity/documentation/manual/five.grok/background/adding-five.grok-as-a-dependency

Steps:

* Add dependencies to your ``setup.py``.

* Edit ``buildout.cfg`` to include the good known version set.

* Add the ``grok`` :term:`ZCML` directive to ``configure.zcml``.

