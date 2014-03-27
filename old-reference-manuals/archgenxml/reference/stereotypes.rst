===========
Stereotypes
===========

.. contents :: :local:

.. admonition:: Description

        All stereotypes available in its context.

*This file was generated 2009-05-12 with bin/agx_stereotypes 2.4.1.*

abstraction
-----------
adapts
   On a realization, specify a class (``<<adapter>>``, ``<<named_adapter>>``, ``<<extender>>``) adapts another class (``<<stub>>``, ``<<interface>>``).

class
-----
adapter
   Is a (non-named) adapter.

archetype
   Explicitly specify that a class represents an Archetypes type. This may be necessary if you are including a class as a base class for another class and ArchGenXML is unable to determine whether the parent class is an Archetype or not. Without knowing that the parent class in an Archetype, ArchGenXML cannot ensure that the parent's schema is available in the derived class.

atblob
   Turns the class into an plone.app.blob.content.ATBlob subclass.

atdocument
   Turns the class into an Atdocument subclass.

atevent
   Turns the class into an ATEvent subclass.

atfile
   Turns the class into an ATFile subclass.

atfolder
   Turns the class into an ATFolder subclass.

atimage
   Turns the class into an ATImage subclass.

atlink
   Turns the class into an ATLink subclass.

atnewsitem
   Turns the class into an ATNewsItem subclass.

btree
   Like ``<<folder>>``, it generates a folderish object. But it uses a BTree folder for support of large amounts of content. The same as ``<<large>>``.

content_class
   .. TODO:: Complete

doc_testcase
   Turns a class into a doctest class. It must subclass a ``<<plone_testcase>>``.

extender
   Is a schema extender supported by archetypes.schemaextender.

field
   Class will target in a ObjectField or CompoundField (latter if Attributes are provided)

flavor
   Generates a ContentFlavors flavor from this class.

folder
   Turns the class into a folderish object. When a UML class contains or aggregates other classes, it is automatically turned into a folder; this stereotype can be used to turn normal classes into folders, too.

functional_doc_testcase
   Turns a class into a functional doctest class. It must subclass a ``<<plone_testcase>>``.

functional_testcase
   Turns a class into a functional testcase. It must subclass a ``<<functional_testcase>>``. Adding an interface arrow to another class automatically adds that class's methods to the testfile for testing.

hidden
   Generate the class, but turn off "global_allow", thereby making it unavailable in the portal by default. Note that if you use composition to specify that a type should be addable only inside another (folderish) type, then "global_allow" will be turned off automatically, and the type be made addable only inside the designated parent. (You can use aggregation instead of composition to make a type both globally addable and explicitly addable inside another folderish type).

interface
   Is an interface.

interface_testcase
   Turns a class into a testcase for the interfaces.

large
   Like ``<<folder>>``, it generates a folderish object. But it uses a BTree folder for support of large amounts of content. The same as ``<<large>>``.

mixin
   Don't inherit automatically from "BaseContent" and so. This makes the class suitable as a mixin class. See also ``<<archetype>>``.

named_adapter
   Is a named adapter.

odStub
   Prevents a class/package/model from being generated. Same as ``<<stub>>``.

ordered
   For folderish types, include folder ordering support. This will allow the user to re-order items in the folder manually.

plone_testcase
   Turns a class into the (needed) base class for all other ``<<testcase>>`` and ``<<doc_testcase>>`` classes inside a ``<<test>>`` package.

plonefunctional_testcase
   Turns a class into the base class for all other ``<<functionaltestcase>>`` classes inside a ``<<test>>`` package.

portal_tool
   Turns the class into a portal tool.

portlet_class
   Generate this class as a zope3 portlet class instead of as an Archetypes class.

python_class
   Generate this class as a plain python class instead of as an Archetypes class.

remember
   The class will be treated as a remember member type. It will derive from remember's Member class and be installed as a member data type. Note that you need to install the separate remember product.

setup_testcase
   Turns a class into a testcase for the setup, with pre-defined common checks.

stub
   Prevents a class/package/model from being generated.

testcase
   Turns a class into a testcase. It must subclass a ``<<plone_testcase>>``. Adding an interface arrow to another class automatically adds that class's methods to the testfile for testing.

tool
   Turns the class into a portal tool. Similar to ``<<portal_tool>>``.

variable_schema
   Include variable schema support in a content type by deriving from the VariableSchema mixin class.

view_class
   Generate this class as a zope3 view class instead of as an Archetypes class.

vocabulary
   .. TODO:: Complete

vocabulary_term
   .. TODO:: Complete

widget
   A simple stub archetypes-widget class will be created.

zope_class
   Generate this class as a plain Zope class instead of as an Archetypes class.

dependency
----------
value_class
   Declares a class to be used as value class for a certain field class (see ``<<field>>`` stereotype).

interface
---------
stub
   Prevents a class/package/model from being generated.

z3
   Generate this interface class as zope 3 interface. This will inherit from zope.interface.Interface.

method
------
action
   Generate a CMF action which will be available on the object. The tagged values "action" (defaults to method name), "id" (defaults to method name), "category" (defaults to "object"), "label" (defaults to method name), "condition" (defaults to empty), and "permission" (defaults to empty) set on the method and mapped to the equivalent fields of any CMF action can be used to control the behaviour of the action.

form
   Generate an action like with the ``<<action>>`` stereotype, but also copy an empty controller page template to the skins directory with the same name as the method and set this up as the target of the action. If the template already exists, it is not overwritten.

noaction
   Disables standard actions, applied to a method out of 'view', 'edit', 'metadata', 'references.

view
   Generate an action like with the ``<<action>>`` stereotype, but also copy an empty page template to the skins directory with the same name as the method and set this up as the target of the action. If the template exists, it is not overwritten.

model
-----
odStub
   Prevents a class/package/model from being generated. Same as ``<<stub>>``.

stub
   Prevents a class/package/model from being generated.

operation
---------
action
   Generate a CMF action which will be available on the object. The tagged values "action" (defaults to method name), "id" (defaults to method name), "category" (defaults to "object"), "label" (defaults to method name), "condition" (defaults to empty), and "permission" (defaults to empty) set on the method and mapped to the equivalent fields of any CMF action can be used to control the behaviour of the action.

form
   Generate an action like with the ``<<action>>`` stereotype, but also copy an empty controller page template to the skins directory with the same name as the method and set this up as the target of the action. If the template already exists, it is not overwritten.

noaction
   Disables standard actions, applied to a method out of 'view', 'edit', 'metadata', 'references.

view
   Generate an action like with the ``<<action>>`` stereotype, but also copy an empty page template to the skins directory with the same name as the method and set this up as the target of the action. If the template exists, it is not overwritten.

package
-------
odStub
   Prevents a class/package/model from being generated. Same as ``<<stub>>``.

stub
   Prevents a class/package/model from being generated.

tests
   Treats a package as test package. Inside such a test package, you need at a ``<<plone_testcase>>`` and a ``<<setup_testcase>>``.
