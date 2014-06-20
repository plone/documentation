.. _agx-tagged-values:

=============
Tagged Values
=============

.. contents :: :local:

.. admonition:: Description

        All tagged values available in its context.

*This file was generated 2009-05-12 with bin/agx_taggedvalues 2.4.1.*

action
======

action
   For a stereotype 'action', this tagged value can be used to overwrite the default URL ('..../name_of_method') into '..../tagged_value'.

category
   The category for the action. Defaults to 'object'.

condition
   A TALES expression defining a condition which will be evaluated to determine whether the action should be displayed.

id
   The id of the action. Use 'id',

label
   The label of the action - displayed to the user.

permission
   The permission used for the action, a string or comma separated list of strings, default to 'View'.

visible
   Sets the visible property, default to 'True'

association
===========

association_class
   You can use associations classes to store content on the association itself. The class used is specified by this setting. Don't forget to import the used class properly.

association_vocabulary
   Switch, defaults to False. Needs Product 'ATVocabularyManager'. Generates an empty vocabulary with the name of the relation.

back_reference_field
   Use a custom field instead of ReferenceField.

field
   Synonymous with either reference_field or relation_field, depending on whether you use it on the *from* end or the *to* end of a relation. Works only together with 'Relations' Product and relation_implementation set to 'relations'.

inverse_relation_name
   Together with 'Relations' Product you have inverse relations. the name default to 'name_of_your_relation_inverse', but you can overrrule it using this tagged value.

label
   Sets the readable name.

reference_field
   Use a custom field instead of ReferenceField.

relation_field
   Use a custom field instead of RelationField. Works only together with 'Relations' Product and relation_implementation set to 'relations'.

relation_implementation
   Sets the type of implementation is used for an association: 'basic' (used as default) for classic style archetypes references or 'relations' for use of the 'Relations' Product.

relationship
   Standard relationship for ReferenceField

attribute
=========

accessor
   Set the name of the accessor (getter) method. If you are overriding one of the DC metadata fields such as 'title' or 'description' be sure to set the correct accessor names such as 'Title' and 'Description'; by default these accessors would be generated as getTitle() or getDescription().

allowed_types
   Sets the types allowed for a ReferenceField. Default is []

array:widget
   specify which custom ArrayWidget should be used for a field (only applies if the field has cardinality >1.

catalog:index
   Add the field (or all fields of a class, package, model) to the index. Boolean, 1 or 0. Default is 0. If set, you may need to provide ``index:*`` tagged values too.

catalog:metadata
   Adds the field to the metadata record on the query result. Boolean, 1 or 0. If you do not provide 'index:attributes', the name of the accessor of the field is the default. If 'catalog:attributes' is given for each attribute one field at the record will be created.

catalog:name
   Sometimes you need to add an index to a other catalog than 'portal_catalog' and its XML-File 'catalog.xml'. Provide a tuple of comma separated strings, id of the catalog and the filename of its configuration file. default is "portal_catalog, Plone Catalog Tool'.

collection:criteria
   Add the index to the Collection (aka Smart Folder) Indexes available for defining Criteria. Provide a comma separated list of criteria that will be available by default. Available criterias are: ATBooleanCriterion, ATDateCriteria, ATDateRangeCriterion, ATListCriterion, ATPortalTypeCriterion, ATReferenceCriterion, ATSelectionCriterion, ATSimpleIntCriterion, ATSimpleStringCriterion, ATSortCriterion, ATCurrentAuthorCriterion, ATPathCriterion, ATRelativePathCriterion. You must provide an index:type as well.

collection:criteria_description
   A help text (string), used for collection:criteria. Its added to the generated.pot as a literal. If not provided the widget:description is used.

collection:criteria_label
   The display name of the collection:criteria, called friendly name (string). Its added to the generated.pot as a literal. If not given the widget:label is taken if provided.

collection:metadata
   register the catalog:metadata as an available column in a Collection. Can be used as an alternative for catalog:metadata. catalog:metadata_accessor is used if given.

collection:metadata_description
   A help text (string), used for collection:criteria. Its added to the generated.pot as a literal. If not provided the collection:criteria_help or - if not provided - widget:description is used.

collection:metadata_label
   the display name of the collection:metadata, called friendly name (string), used for index:criteria. Its added to the generated.pot as a literal. If not given the widget:label is taken if provided.

copy_from
   To copy an attribute from another schema, give it the type 'copy'. The tagged value 'copy_from' is then used to specify which schema to copy it from (for instance, 'BaseSchema' when copying Description from the base schema). For copying your own schemas, add an 'imports' tagged value to import your class (say 'MyClass') and then put 'MyClass.schema' in your 'copy_from' value.

default
   Set a value to use as the default value of the field.

default_method
   Set the name of a method on the object which will be called to determine the default value of the field.

enforceVocabulary
   Set to true (1) to ensure that only items from the vocabulary are permitted.

expression
   evaluation expression for computed fields.

i18ncontent
   Enables the content type(s) for LinguaPlone. Only allowed value is 'linguaplone'.

index
   DEPRECATED: Add an index to the attribute. Use catalog:index and the index:* tagged value instead.

index:attributes
   The attributes to use for index or metadata (string or comma separated list of strings). This are the methods called at indexing time. Normally it is enough to provide one index method, but for some specific use cases you might need to provide alternatives. If you don not provide this tagged value, the name of the accessor of the field is the default.

index:extras
   Some indexes are using so called 'extras' on installation as configuration. If the index need extras you'll need to declare them here. Provide a comma separated list.

index:name
   the name of the index used (string). Use this name in your queries. If you do not provide a name, the name of the accessor of the field is the default.

index:properties
   Some indexes are using 'properties' on installation as configuration. If the index need properties you'll need to declare them here. Provide a comma separated list.

index:type
   the type of index used as (string), for example 'FieldIndex', 'KeywordIndex', 'DateIndex' or any available index in your portal. For known types a default is guessed, such as FieldIndex for StringFields or DateIndex for DateFields. If no guess is possible, we assume a FieldIndex.

indexMethod
   DEPRECATED: Declares method used for indexing.

label
   Sets the readable name.

move:after
   Move the current field after the given field (put the field name between quote).

move:before
   Move the current field before the given field (put the field name between quote).

move:bottom
   Move the current field to the bottom (put 1 for the value).

move:pos
   Move the current field at the given position (an int).

move:top
   Move the current field to the top (put 1 for the value).

multiValued
   Certain fields, such as reference fields, can optionally accept more than one value if multiValued is set to true (1)

mutator
   Similarly, set the name of the mutator (setter) method.

original_size
   Sets the maximum size for the original for an ImageField widget.

read_permission
   Defines archetypes fields read-permission. Use it together with workflow to control ability to view fields based on roles/permissions.

required
   Set to true (1) to make the field required

schemata
   If you want to split your form with many, many attibutes in multiple schemata ("sub-forms"), add a tagged value 'schemata' to the attributes you want in a different schemata with the name of that schemata (for instance "personal data"). The default schemata is called "default", btw.

searchable
   Whether or not the field should be searchable when performing a search in the portal.

sizes
   Sets the allowed sizes for an ImageField widget.

source_name
   With attribute type 'copy' sometimes schema-recycling is fun, together with copy_from you can specify the source name of the field in the schema given by copy_from.

validation_expression
   Use an ExpressionValidator and sets the by value given expression.

validation_expression_errormsg
   Sets the error message to the ExpressionValidator (use with validation_expression to define the validation expression to which this error message applies).

validators
   .. TODO:: Not supported for now.

vocabulary
   Set to a python list, a DisplayList or a method name (quoted) which provides the vocabulary for a selection widget.

vocabulary:name
   Together with Products 'ATVocabularyManager' this sets the name of the vocabulary.

vocabulary:term_type
   For use with 'ATVocabularyManager'. Defaults to 'SimplevocabularyTerm'. Let you define the portal_type of the vocabularyterm used for the default term that is created in Install.py.

vocabulary:type
   Enables support for Products 'ATVocabularyManager' by setting value to 'ATVocabularyManager'.

widget
   Allows you to set the widget to be used for this attribute.

widget:description
   Set the widget's description.

widget:description_msgid
   Set the description i18n message id. Defaults to a name generated from the field name.

widget:i18n_domain
   Set the i18n domain. Defaults to the product name.

widget:label
   Set the widget's label.

widget:label_msgid
   Set the label i18n message id. Defaults to a name generated from the field name.

widget:type
   Set the name of the widget to use. Each field has an associated default widget, but if you need a different one (e.g. a SelectionWidget for a string field), use this value to override.

write_permission
   Defines archetypes fields write-permission. Use it together with workflow to control ability to write data to a field based on roles/permissions.

class
=====

active_workflow_states
   The active workflow states for a remember type. MUST be set on ``<<remember>>`` types. Format is ['state', 'anotherstate'].

additional_parents
   A comma-separated list of the names of classes which should be used as additional parents to this class, in addition to the Archetypes BaseContent, BaseFolder or OrderedBaseFolder. Usually used in conjunction with 'imports' to import the class before it is referenced.

alias
   FTI Alias definition in the form alias=fromvalue,tovalue

allow_discussion
   Whether or not the content type should be discussable in the portal by default.

allowable_content_types
   A comma-separated list of allowed test format for a textarea widget.

allowed_content_types
   A comma-separated list of allowed sub-types for a (folderish) content type. Note that allowed content types are automatically set when using aggregation and composition between classes to specify containment.

archetype_name
   The name which will be shown in the "add new item" drop-down and other user-interface elements. Defaults to the class name, but whilst the class name must be valid and unique python identifier, the archetype_name can be any string.

author
   You can set the author project-wide with the '--author' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a class level.

base_actions
   Sets the base actions in the class's factory type information (FTI).

base_class
   Explicitly set the base class of a content type, overriding the automatic selection of BaseContent, BaseFolder or OrderedBaseFolder as well as any parent classes in the model. What you specify here ends up as the first item (or items: comma-separate them) in the classes it inherits from. So this is also a handy way to place one class explicitly in front of the other. See also additional_parents.

base_schema
   Explicitly set the base schema for a content type, overriding the automatic selection of the parent's schema or BaseSchema, BaseFolderSchema or OrderedBaseFolderSchema.

catalog:index
   Add the field (or all fields of a class, package, model) to the index. Boolean, 1 or 0. Default is 0. If set, you may need to provide ``index:*`` tagged values too.

catalog:metadata
   Adds the field to the metadata record on the query result. Boolean, 1 or 0. If you do not provide 'index:attributes', the name of the accessor of the field is the default. If 'catalog:attributes' is given for each attribute one field at the record will be created.

catalog:name
   Sometimes you need to add an index to a other catalog than 'portal_catalog' and its XML-File 'catalog.xml'. Provide a tuple of comma separated strings, id of the catalog and the filename of its configuration file. default is "portal_catalog, Plone Catalog Tool'.

catalogmultiplex:black
   Remove an archetypes class (identified by meta_type) from one or more catalogs to be cataloged in. Comma-separated list of catalogs. Example-value: 'portal_catalog, another_catalog'. Explaination: Instances of the class wont be catalogged in portal_catalog anymore.

catalogmultiplex:white
   Add an archetypes class (identified by meta_type) to one or more catalogs to be cataloged in. Comma-separated list of catalogs. Example-value: 'myfancy_catalog, another_catalog'. Explaination: Additionally to the default 'portal_catalog' the instances of this class will be catalogged in the two given catalogs.

content_icon
   The name of an image file, which must be found in the skins directory of the product. This will be used to represent the content type in the user interface.

copyright
   You can set the copyright project-wide with the '--copyright' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a class level.

creation_permission
   Sets the creation permission for the class. Example: 'Add portal content'.

creation_roles
   You can set an own role who should be able to add a type. Use an Tuple of Strings. Default and example for this value: '("Manager", "Owner", "Member")'.

default_interface_type
   default type of interfaces (z2 or z3).

default_view
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The default_view value sets the default one. Defaults to 'base_view'. Only relevant if you use TemplateMixin.

description
   A description of the type, a sentence or two in length. Used to describe the type to the user.

detailed_creation_permissions
   Give the content-type (types in the package, model) own creation permissions, named automagically 'ProductName: Add ClassName'.

disable_polymorphing
   Normally, archgenxml looks at the parents of the current class for content types that are allowed as items in a folderish class. So: parent's allowed content is also allowed in the child. Likewise, subclasses of classes allowed as content are also allowed on this class. Classic polymorphing. In case this isn't desired, set the tagged value 'disable_polymorphing' to 1.

display_in_navigation
   Setting this boolean value adds the type to 'Displayed content types' in the portals navigation settings. Default is True

doctest_name
   In a tests package, setting the stereotype ``<<doc_testcase>>`` on a class turns it into a doctest. The doctest itself is placed in the doc/ subdirectory. The 'doctest_name' tagged value overwrites the default name for the file (which is the name of the doctestcase class + '.txt'). ArchGenXML appends the '.txt' extension automatically, so you don't need to specify it.

email
   You can set the email project-wide with the '--email' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a class level.

filter_content_types
   If set to true (1), explicitly turn on the filter_content_types factory type information value. If this is off, all globally addable content types will be addable inside a (folderish) type; if it is on, only those values in the allowed_content_types list will be enabled. Note that when aggregation or composition is used to define containment, filtered_content_types will be automatically turned on.

folder_base_class
   Useful when using the '<<folder>>' stereotype in order to set the folderish base class.

generate_reference_fields
   Per default (True) navigable reference (or relation) ends are resulting in a ReferenceField (or RelationField). Setting this value to False results in not generating ReferenceFields automagically.

global_allow
   Overwrite the AGX-calculated 'global_allow' setting of class. Setting it to '1' makes your content type addable everywhere (in principle), setting it to '0' limits it to places where it's explicitly allowed as content.

hide_actions
   A comma- or newline-separated list of action ids to hide on the class. For example, set to 'metadata, sharing' to turn off the metadata (properties) and sharing tabs.

hide_folder_tabs
   When you want to hide the folder tabs (mostly the "contents" tab, just set this tagged value to 1.

i18ncontent
   Enables the content type(s) for LinguaPlone. Only allowed value is 'linguaplone'.

immediate_view
   Set the immediate_view factory type information value. This should be the name of a page template, and defaults to 'base_view'. Note that Plone at this time does not make use of immediate_view, which in CMF core allows you to specify a different template to be used when an object is first created from when it is subsequently accessed.

import_from
   If you wish to include a class in your model (as a base class or aggregated class, for example) which is actually defined in another product, add the class to your model and set the import_from tagged value to the class that should be imported in its place. You probably don't want the class to be generated, so add a stereotype '<<stub>>' as well.

imports
   A list of python import statements which will be placed at the top of the generated file. Use this to make new field and widget types available, for example. Note that in the generated code you will be able to enter additional import statements in a preserved code section near the top of the file. Prefer using the imports tagged value when it imports something that is directly used by another element in your model. You can have several import statements, one per line, or by adding several tagged values with the name 'imports'.

index:type
   the type of index used as (string), for example 'FieldIndex', 'KeywordIndex', 'DateIndex' or any available index in your portal. For known types a default is guessed, such as FieldIndex for StringFields or DateIndex for DateFields. If no guess is possible, we assume a FieldIndex.

inherit_allowed_types
   By default, a child type will inherit the allowable content types from its parents. Set this property to false (0) to turn this off.

label
   Sets the readable name.

license
   You can set the license project-wide with the '--license' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a class level.

marshaller
   Specify a marshaller to use for the class' schema.

module
   Like 'module_name', it overwrites the name of the directory it'd be normally placed in.

module_name
   Like 'module', it overwrites the name of the directory it'd be normally placed in.

parentclass_first
   if this tgv is set to true generalization parents are used before the standard base classes (e.g. BaseContent) this option is sometimes necessary when inheriting from some special parents (e.g. 'remember' style classes).

parentclasses_first
   if this tgv is set to true generalization parents are used before the standard base classes (e.g. BaseContent) this option is sometimes necessary when inheriting from some special parents (e.g. 'remember' style classes).

portal_type
   Sets the CMF portal-type this class will be registered with, defaults to the class-name.

read_permission
   Defines archetypes fields read-permission. Use it together with workflow to control ability to view fields based on roles/permissions.

register
   'Remember' related. Set as default member type.

searchable
   Per default a fields 'searchable' property is set to False. Sometimes you want it for all fields True. This TGV let you define the default for a class, package or model.

searchable_type
   Setting this boolean value adds the type to 'types to be searched' in the portals search settings. Default is True

strict
   On a class with the ``<<interface_doctest>>`` stereotype: check for inherited interfaces as well.

suppl_views
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The suppl_views value sets the available views. Example: '("my_view", "myother_view")'. Defaults to '()'. Only relevant if you use TemplateMixin.

typeDescription
   DEPRECATED. Use 'description' instead.

use_dynamic_view
   Controles wether CMFDynamicViewFTI is used for a type/class. Boolean, default is True.

use_portal_factory
   This boolean value controls the registration of the type for use with portal_factory. Default: True.

use_workflow
   Tie the class to the named workflow. A state diagram (=workflow) attached to a class in the UML diagram is automatically used as that class's workflow; this tagged value allows you to tie the workflow to other classes.

version_info
   Add ArchGenXML version information to the generated file (default is 1).

vocabulary:type
   Enables support for Products 'ATVocabularyManager' by setting value to 'ATVocabularyManager'.

vocabulary:vocabulary_type
   For use with 'ATVocabularyManager'. Defaults to 'Simplevocabulary'. Let you define the portal_type of the vocabulary used as initial vocabulary at Product install time. If VdexVocabulary is used, the install-script tries to install a vocabulary from a vdex file names 'Products/PRODUCTNAME/data/VOCABULARYNAME.vdex'.

write_permission
   Defines archetypes fields write-permission. Use it together with workflow to control ability to write data to a field based on roles/permissions.

field
=====

description
   Sets a description for this field. It's used for field documentation while registering inside Archetypes.

label
   Sets the readable name.

validation_expression
   Use an ExpressionValidator and sets the by value given expression.

validation_expression_errormsg
   Sets the error message to the ExpressionValidator (use with validation_expression to define the validation expression to which this error message applies).

method
======

code
   The actual python code of the method. Only use this for simple one-liners. Code filled into the generated file will be preserved when the model is re-generated.

documentation
   You can add documention via this tag; it's better to use your UML tool's documentation field.

label
   Sets the readable name.

permission
   For method with public visibility only, if a permission is set, declare the method to be protected by this permission. Methods with private or protected visiblity are always declared private since they are not intended for through-the-web unsafe code to access. Methods with package visibility use the class default security and do not get security declarations at all.

model
=====

alias
   FTI Alias definition in the form alias=fromvalue,tovalue

association_class
   You can use associations classes to store content on the association itself. The class used is specified by this setting. Don't forget to import the used class properly.

association_vocabulary
   Switch, defaults to False. Needs Product 'ATVocabularyManager'. Generates an empty vocabulary with the name of the relation.

author
   You can set the author project-wide with the '--author' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a model level.

catalog:index
   Add the field (or all fields of a class, package, model) to the index. Boolean, 1 or 0. Default is 0. If set, you may need to provide ``index:*`` tagged values too.

catalog:metadata
   Adds the field to the metadata record on the query result. Boolean, 1 or 0. If you do not provide 'index:attributes', the name of the accessor of the field is the default. If 'catalog:attributes' is given for each attribute one field at the record will be created.

catalog:name
   Sometimes you need to add an index to a other catalog than 'portal_catalog' and its XML-File 'catalog.xml'. Provide a tuple of comma separated strings, id of the catalog and the filename of its configuration file. default is "portal_catalog, Plone Catalog Tool'.

catalogmultiplex:black
   Remove an archetypes class (identified by meta_type) from one or more catalogs to be cataloged in. Comma-separated list of catalogs. Example-value: 'portal_catalog, another_catalog'. Explaination: Instances of the class wont be catalogged in portal_catalog anymore.

catalogmultiplex:white
   Add an archetypes class (identified by meta_type) to one or more catalogs to be cataloged in. Comma-separated list of catalogs. Example-value: 'myfancy_catalog, another_catalog'. Explaination: Additionally to the default 'portal_catalog' the instances of this class will be catalogged in the two given catalogs.

copyright
   You can set the copyright project-wide with the '--copyright' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a model level.

creation_permission
   Sets the creation permission for the class. Example: 'Add portal content'.

creation_roles
   You can set an own role who should be able to add a type. Use an Tuple of Strings. Default and example for this value: '("Manager", "Owner", "Member")'.

default_interface_type
   default type of interfaces (z2 or z3).

default_view
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The default_view value sets the default one. Defaults to 'base_view'. Only relevant if you use TemplateMixin.

dependency_step_qi
   Generate Quickinstaller dependency installation for your product. Boolean (1 or 0), default 0 (off). Dependencies can be declared in AppConfig.py in a variable DEPENDENCIES.

dependend_profiles
   GenericSetup profiles your product depends on. A list of profile names separated by commas. This list is used for the dependencies tag inside the metadata.xml file of the product's profile

detailed_creation_permissions
   Give the content-type (types in the package, model) own creation permissions, named automagically 'ProductName: Add ClassName'.

display_in_navigation
   Setting this boolean value adds the type to 'Displayed content types' in the portals navigation settings. Default is True

email
   You can set the email project-wide with the '--email' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a model level.

fixtools
   Generate fixTools function in setuphandlers.py. It calls initializeArchetypes for generated tools, thus reset existing data in the tools. Boolean (1 or 0), default 0 (off).

generate_reference_fields
   Per default (True) navigable reference (or relation) ends are resulting in a ReferenceField (or RelationField). Setting this value to False results in not generating ReferenceFields automagically.

global_allow
   Overwrite the AGX-calculated 'global_allow' setting of class. Setting it to '1' makes your content type addable everywhere (in principle), setting it to '0' limits it to places where it's explicitly allowed as content.

i18ncontent
   Enables the content type(s) for LinguaPlone. Only allowed value is 'linguaplone'.

immediate_view
   Set the immediate_view factory type information value. This should be the name of a page template, and defaults to 'base_view'. Note that Plone at this time does not make use of immediate_view, which in CMF core allows you to specify a different template to be used when an object is first created from when it is subsequently accessed.

imports
   A list of python import statements which will be placed at the top of the generated file. Use this to make new field and widget types available, for example. Note that in the generated code you will be able to enter additional import statements in a preserved code section near the top of the file. Prefer using the imports tagged value when it imports something that is directly used by another element in your model. You can have several import statements, one per line, or by adding several tagged values with the name 'imports'.

index:type
   the type of index used as (string), for example 'FieldIndex', 'KeywordIndex', 'DateIndex' or any available index in your portal. For known types a default is guessed, such as FieldIndex for StringFields or DateIndex for DateFields. If no guess is possible, we assume a FieldIndex.

label
   Sets the readable name.

license
   You can set the license project-wide with the '--license' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a model level.

module
   Like 'module_name', it overwrites the name of the directory it'd be normally placed in.

module_name
   Like 'module', it overwrites the name of the directory it'd be normally placed in.

plone_target_version
   The target version of Plone. Defaults to 3.0 Possible values are 2.5 and 3.0

product_description
   The description of the Product. This is placed as description tag in the metadata.xml file of the product's profile

read_permission
   Defines archetypes fields read-permission. Use it together with workflow to control ability to view fields based on roles/permissions.

relation_implementation
   Sets the type of implementation is used for an association: 'basic' (used as default) for classic style archetypes references or 'relations' for use of the 'Relations' Product.

searchable
   Per default a fields 'searchable' property is set to False. Sometimes you want it for all fields True. This TGV let you define the default for a class, package or model.

searchable_type
   Setting this boolean value adds the type to 'types to be searched' in the portals search settings. Default is True

skin_directories
   A comma separated list of subdirectories to be generated inside the product skins directory. Each of this directories is prefixed with productname in lowercase. The default value is "'templates', 'styles', 'images'".

suppl_views
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The suppl_views value sets the available views. Example: '("my_view", "myother_view")'. Defaults to '()'. Only relevant if you use TemplateMixin.

use_dynamic_view
   Controles wether CMFDynamicViewFTI is used for a type/class. Boolean, default is True.

use_portal_factory
   This boolean value controls the registration of the type for use with portal_factory. Default: True.

use_workflow
   Tie the class to the named workflow. A state diagram (=workflow) attached to a class in the UML diagram is automatically used as that class's workflow; this tagged value allows you to tie the workflow to other classes.

version_info
   Add ArchGenXML version information to the generated file (default is 1).

vocabulary:type
   Enables support for Products 'ATVocabularyManager' by setting value to 'ATVocabularyManager'.

vocabulary:vocabulary_type
   For use with 'ATVocabularyManager'. Defaults to 'Simplevocabulary'. Let you define the portal_type of the vocabulary used as initial vocabulary at Product install time. If VdexVocabulary is used, the install-script tries to install a vocabulary from a vdex file names 'Products/PRODUCTNAME/data/VOCABULARYNAME.vdex'.

write_permission
   Defines archetypes fields write-permission. Use it together with workflow to control ability to write data to a field based on roles/permissions.

package
=======

alias
   FTI Alias definition in the form alias=fromvalue,tovalue

association_class
   You can use associations classes to store content on the association itself. The class used is specified by this setting. Don't forget to import the used class properly.

association_vocabulary
   Switch, defaults to False. Needs Product 'ATVocabularyManager'. Generates an empty vocabulary with the name of the relation.

author
   You can set the author project-wide with the '--author' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a package level.

catalog:index
   Add the field (or all fields of a class, package, model) to the index. Boolean, 1 or 0. Default is 0. If set, you may need to provide ``index:*`` tagged values too.

catalog:metadata
   Adds the field to the metadata record on the query result. Boolean, 1 or 0. If you do not provide 'index:attributes', the name of the accessor of the field is the default. If 'catalog:attributes' is given for each attribute one field at the record will be created.

catalog:name
   Sometimes you need to add an index to a other catalog than 'portal_catalog' and its XML-File 'catalog.xml'. Provide a tuple of comma separated strings, id of the catalog and the filename of its configuration file. default is "portal_catalog, Plone Catalog Tool'.

catalogmultiplex:black
   Remove an archetypes class (identified by meta_type) from one or more catalogs to be cataloged in. Comma-separated list of catalogs. Example-value: 'portal_catalog, another_catalog'. Explaination: Instances of the class wont be catalogged in portal_catalog anymore.

catalogmultiplex:white
   Add an archetypes class (identified by meta_type) to one or more catalogs to be cataloged in. Comma-separated list of catalogs. Example-value: 'myfancy_catalog, another_catalog'. Explaination: Additionally to the default 'portal_catalog' the instances of this class will be catalogged in the two given catalogs.

copyright
   You can set the copyright project-wide with the '--copyright' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a package level.

creation_permission
   Sets the creation permission for the class. Example: 'Add portal content'.

creation_roles
   You can set an own role who should be able to add a type. Use an Tuple of Strings. Default and example for this value: '("Manager", "Owner", "Member")'.

default_view
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The default_view value sets the default one. Defaults to 'base_view'. Only relevant if you use TemplateMixin.

detailed_creation_permissions
   Give the content-type (types in the package, model) own creation permissions, named automagically 'ProductName: Add ClassName'.

display_in_navigation
   Setting this boolean value adds the type to 'Displayed content types' in the portals navigation settings. Default is True

email
   You can set the email project-wide with the '--email' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a package level.

generate_reference_fields
   Per default (True) navigable reference (or relation) ends are resulting in a ReferenceField (or RelationField). Setting this value to False results in not generating ReferenceFields automagically.

global_allow
   Overwrite the AGX-calculated 'global_allow' setting of class. Setting it to '1' makes your content type addable everywhere (in principle), setting it to '0' limits it to places where it's explicitly allowed as content.

i18ncontent
   Enables the content type(s) for LinguaPlone. Only allowed value is 'linguaplone'.

immediate_view
   Set the immediate_view factory type information value. This should be the name of a page template, and defaults to 'base_view'. Note that Plone at this time does not make use of immediate_view, which in CMF core allows you to specify a different template to be used when an object is first created from when it is subsequently accessed.

imports
   A list of python import statements which will be placed at the top of the generated file. Use this to make new field and widget types available, for example. Note that in the generated code you will be able to enter additional import statements in a preserved code section near the top of the file. Prefer using the imports tagged value when it imports something that is directly used by another element in your model. You can have several import statements, one per line, or by adding several tagged values with the name 'imports'.

index:type
   the type of index used as (string), for example 'FieldIndex', 'KeywordIndex', 'DateIndex' or any available index in your portal. For known types a default is guessed, such as FieldIndex for StringFields or DateIndex for DateFields. If no guess is possible, we assume a FieldIndex.

label
   Sets the readable name.

license
   You can set the license project-wide with the '--license' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a package level.

module
   Like 'module_name', it overwrites the name of the directory it'd be normally placed in.

module_name
   Like 'module', it overwrites the name of the directory it'd be normally placed in.

read_permission
   Defines archetypes fields read-permission. Use it together with workflow to control ability to view fields based on roles/permissions.

relation_implementation
   Sets the type of implementation is used for an association: 'basic' (used as default) for classic style archetypes references or 'relations' for use of the 'Relations' Product.

searchable
   Per default a fields 'searchable' property is set to False. Sometimes you want it for all fields True. This TGV let you define the default for a class, package or model.

searchable_type
   Setting this boolean value adds the type to 'types to be searched' in the portals search settings. Default is True

suppl_views
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The suppl_views value sets the available views. Example: '("my_view", "myother_view")'. Defaults to '()'. Only relevant if you use TemplateMixin.

use_dynamic_view
   Controles wether CMFDynamicViewFTI is used for a type/class. Boolean, default is True.

use_portal_factory
   This boolean value controls the registration of the type for use with portal_factory. Default: True.

use_workflow
   Tie the class to the named workflow. A state diagram (=workflow) attached to a class in the UML diagram is automatically used as that class's workflow; this tagged value allows you to tie the workflow to other classes.

version_info
   Add ArchGenXML version information to the generated file (default is 1).

vocabulary:type
   Enables support for Products 'ATVocabularyManager' by setting value to 'ATVocabularyManager'.

vocabulary:vocabulary_type
   For use with 'ATVocabularyManager'. Defaults to 'Simplevocabulary'. Let you define the portal_type of the vocabulary used as initial vocabulary at Product install time. If VdexVocabulary is used, the install-script tries to install a vocabulary from a vdex file names 'Products/PRODUCTNAME/data/VOCABULARYNAME.vdex'.

write_permission
   Defines archetypes fields write-permission. Use it together with workflow to control ability to write data to a field based on roles/permissions.

portlet
=======

label
   Sets the readable name.

template_name
   Specify a template for the portlet (without .pt). Default is the class name. (on classes with the stereotype ``<<portlet_class>>``)

state
=====

access
   Shortcut for 'Access contents information'.

add
   Shortcut for 'Add portal content'.

delete
   Shortcut for 'Delete objects'.

description
   Sets the state description.

inactive
   Shortcut for 'Access inactive portal content'.

initial_state
   Sets this state to be the initial state. This allows you to use a normal state in your UML diagram instead of the special round starting-state symbol.

label
   Sets the readable name.

list
   Shortcut for 'List folder contents'.

modify
   Shortcut for 'Modify portal content'.

review
   Shortcut for 'Review portal content'.

role
   Shortcut for 'Change local roles'.

view
   Shortcut for 'View'.

worklist
   Attach objects in this state to the named worklist. An example of a worklist is the to-review list.

worklist:guard_permissions
   Sets the permissions needed to be allowed to view the worklist. Default value is 'Review portal content'. Set to 'False' for no guard_permission.

worklist:guard_roles
   Sets the roles needed to be allowed to view the worklist. No default value

state action
============

after:binding
   Interface to bind the after effect to.

before:binding
   Interface to bind the before effect to.

label
   Sets the readable name.

state machine
=============

bindings
   List of portal-types this workflow should be bound to. Comma-separated, i.e. 'Document, Image, File'.

default
   A workflow id to be set as the default workflow.

label
   Sets the readable name.

state transition
================

label
   Sets the readable name.

trigger_type
   Sets the trigger type, following what is defined by DCWorkflow: automatic user action (default) workflow method

url
   Action URL, need 'PloneWorkflowTransitions' to see it in Plone.

tool
====

author
   You can set the author project-wide with the '--author' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a tool level.

autoinstall
   Controls, wether the tool is automatically installed when your product is installed. Boolean, default is True.

configlet
   Set to true (1) to set up a configlet in the Plone control panel for your tool.

configlet:condition
   A TALES expression defining a condition which will be evaluated to determine whether the configlet should be displayed.

configlet:description
   A description of the configlet.

configlet:icon
   The name of an image file, which must be in your product's skin directory, used as the configlet icon.

configlet:permission
   A permission which is required for the configlet to be displayed.

configlet:section
   The section of the control panel where the configlet should be displayed. One of 'Plone', 'Products' (default) or 'Member'. **warning**: older documentation versions mentioned 'Members' here.

configlet:title
   The name of the configlet.

configlet:view
   The id of the view template to use when first opening the configlet. By default, the 'view' action of the object is used (which is usually base_view)

copyright
   You can set the copyright project-wide with the '--copyright' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a tool level.

creation_permission
   Sets the creation permission for the class. Example: 'Add portal content'.

creation_roles
   You can set an own role who should be able to add a type. Use an Tuple of Strings. Default and example for this value: '("Manager", "Owner", "Member")'.

default_view
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The default_view value sets the default one. Defaults to 'base_view'. Only relevant if you use TemplateMixin.

email
   You can set the email project-wide with the '--email' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a tool level.

immediate_view
   Set the immediate_view factory type information value. This should be the name of a page template, and defaults to 'base_view'. Note that Plone at this time does not make use of immediate_view, which in CMF core allows you to specify a different template to be used when an object is first created from when it is subsequently accessed.

imports
   A list of python import statements which will be placed at the top of the generated file. Use this to make new field and widget types available, for example. Note that in the generated code you will be able to enter additional import statements in a preserved code section near the top of the file. Prefer using the imports tagged value when it imports something that is directly used by another element in your model. You can have several import statements, one per line, or by adding several tagged values with the name 'imports'.

label
   Sets the readable name.

license
   You can set the license project-wide with the '--license' commandline parameter (or in the config file). This TGV allows you to use/ overwrite it on a tool level.

module
   Like 'module_name', it overwrites the name of the directory it'd be normally placed in.

module_name
   Like 'module', it overwrites the name of the directory it'd be normally placed in.

suppl_views
   The TemplateMixin class in Archetypes allows your class to present several alternative view templates for a content type. The suppl_views value sets the available views. Example: '("my_view", "myother_view")'. Defaults to '()'. Only relevant if you use TemplateMixin.

tool_instance_name
   The id to use for the tool. Defaults to 'portal_<name>', where ``<name>`` is the class name in lowercase.

toolicon
   The name of an image file, which must be found in the skins directory of the product. This will be used to represent your tool in the Zope Management Interface.

unknown
=======

Modify


access


allow_empty_rows


columns


default:widget:Reference


default_content_type


default_output_type


default_page_type


i18ncontent


index_method


languageIndependent


max_size


mode


pil_quality


pil_resize_algo


rename_after_creation


storage


swallowResizeExceptions


widget:addable


widget:allow_brightness


widget:allow_browse


widget:allow_file_upload


widget:allow_search


widget:allow_sorting


widget:append_only


widget:auto_insert


widget:available_indexes


widget:base_query


widget:checkbox_bound


widget:cols


widget:columns


widget:default_search_index


widget:destination


widget:destination_types


widget:divider


widget:dollars_and_cents


widget:ending_year


widget:force_close_on_insert


widget:format


widget:future_years


widget:history_length


widget:image_method


widget:image_portal_types


widget:maxlength


widget:nullValueTitle


widget:omitCountries


widget:only_for_review_states


widget:provideNullValue


widget:restrict_browsing_to_startup_directory


widget:rows


widget:search_catalog


widget:show_hm


widget:show_indexes


widget:show_path


widget:show_review_state


widget:show_ymd


widget:size


widget:starting_year


widget:startup_directory


widget:thousands_commas


widget:visible


widget:whole_dollars


view
====

label
   Sets the readable name.

name
   Specify a name for the zope3 view.. Default is the class name. (on classes with the stereotype ``<<view_class>>``)

widget
======

description
   Sets a description for this widget. It's used for widget documentation while registering inside Archetypes.

label
   Sets the readable name.

macro
   Sets the macro used by the widget. This will be used as the name of the auto-created page template for the widget.

title
   Sets the widget title. It's used for widget documentation while registering inside Archetypes.

used_for
   Sets the possible fields which can use this widget. It's used for widget documentation while registering inside Archetypes. The list has the form: '"Products.Archetypes.Field.Field1Name", "Products.Archetypes.Field.FieldName2"'.
