===================
Methods and Actions
===================

.. contents :: :local:

.. admonition:: Description

        Defining Methods and Actions

To create a method in your class, add a method to the UML diagram, with the desired parameters. The types of the parameters and the type of the return value are ignored, since Python does not support this.

Methods can different access specifiers (also called visibilities) These are:

* public (shown by a + before the method name) -- The method is part of the class' public interface. It will be declared public (accessible from unsafe/through-the-web code) by default. If you add a tagged value 'permission' (see below), it will be declared as protected by this permission.
* protected (#) -- The method is not part of the class' public interface, but is meant for use by sub-classes. It will be declared private to prevent unsafe code from accessing it.
* private (-) -- The method is internal to the class. It will be declared private to prevent unsafe code from accessing it.
* package (~) -- The method is intended to be accessed by other code in the same module as the class. It will not gain any Zope security assertions, relying instead on the class/module defaults.

There are a few tagged values you can use to alter how the code is generated:

* code -- Sets the python code body of the method. Only use this for short one-liners. If you fill in code manually in the generated files, method bodies will be preserved when you re-generate the product from the UML model.
* documentation -- Content of the python doc-string of the method. You can also use the documentation feature of most UML modellers to set documentation strings.
* permission -- Applies to methods with 'public' visiblity only. If you set the permission tagged value to ``My custom permission`` results in ``security.declareProtected("""My custom permission""",'methodname')`` - that is, access to your method is protected by the permission with the name ``My custom permission``.

If you want to use the CMF core permissions, add an ``imports`` tagged value to the method's class containing ``from Products.CMFCore import permissions``, and then set the permission tagged value of your method to ``python:permissions.View``, ``python:permissions.ModifyPortalContent`` or any other core permission. You can also use the common paradigm of defining permissions in config.py as constants with names like EDIT_PERMISSION. A config.py is automatically generated and its contents imported, so you can just set the permission tagged value to, for example, ``python:EDIT_PERMISSION``.

Archetypes uses actions for generating custom tabs to access some view of an Archetype object. ArchGenXML can generate actions for you: Just define a method without any parameters and set its stereotype to ``<<action>>``.

Once again tagged values can be set on the sterotyped methods in order to set some properties of the action:

* action -- The TAL expression representing the action to be executed when the user invokes the action. Defaults to the methodname.
* category -- The category of an action, view or form. Defaults to ``object``.
* id -- The id of an action, view or form. Defaults to the methodname.
* label -- The label of an action, view or form. Defaults to the methodname.
* permission -- ``permission=My permission`` results in ``permissions: ('''My Permission''',)``. See the description of the general ``permission`` tagged value above for more.
* condition -- A TALES expression giving a condition to control when the action is to be made available.

You can override the default Archetypes actions by using special names for the id. These are:

* view -- for overriding the default view action.
* edit -- for overriding the default edit action.
* contents -- for overriding the default contents action.
