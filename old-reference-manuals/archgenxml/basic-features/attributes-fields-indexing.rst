==============================
Attributes / Fields / Indexing
==============================

.. contents :: :local:

.. admonition:: Description

        How to control the fields of your schema.

Archetypes are using *schemas* (also called *schemata*) with *fields* to define the form-fields on your content. The schema and its fields of your content types is generated from the *attributes* of your classes in your model and their tagged values. Each field has a type and a widget.

The `Archetypes documentation <http://plone.org/documentation/manual/archetypes-developer-manual>`_ and the quick reference at the end of this document describes which fields are available and what parameters they take as configuration.

Usage of tagged values
----------------------
If you set a tagged value on an attribute of your class, in general that tagged value will be passed through as a parameter to the generated Archetypes field. Hence, if you set a tagged value ``enforceVocabulary`` to the value ``1`` on an attribute, you will get ``enforceVocabulary=1`` for that field in the generated schema. Similarly, you can set a field's widget properties by prefixing the tagged value with ``widget:``. ``widget:label`` sets the label of a widget, for instance.

Non-string tagged values
------------------------
As before, when reading tagged values, ArchGenXML will generally treat them as strings, with a few exceptions where only non-string values are permitted, such as the 'required' tagged value. If you do not wish your value to be quoted as a string, prefix it with ``python:``. For example, if you set the tagged value ``default`` to ``python:["high", "low"]`` on a ``lines`` attribute, you will get ``default=["high", "low"]`` in a LinesField in your schema.

field recycling - copy from parents schema or another source schema and modify
------------------------------------------------------------------------------
This feature alows you to copy a field from another source schema and rename the field.

Rather than subclass an entire class then delete unwanted fields, you can explicitly copy just the fields you need. You can keep the copied field "as-is" or modify it by overriding properties with tag values as needed.

For example you may need a ``Description`` field that is usually defined in your parent classes (BaseContent, BaseFolder) Schema. You would create a new attribute in your class named ``description`` with a type of ``copy.`` If you want it to appear in your base_edit form rather then the default of properties/metadata page you just need to change one property of the field by adding the tag ``schemata = "default"``.

You may also copy from any other schema or from within the same schema. You need to specify the source schema using the tag ``copy_from`` and if you need to rename the field use the ``source_name`` tag to indicate the source field Id, otherwise the Id of the field in you schema is used.

Index and metadata in catalogs and Collection
---------------------------------------------
ArchgenXML can create configuration files to create an index and/or metadata entries in the catalog such as portal_catalog.

Available are the following tagged values:

``catalog:index`` -- add the field to the index. Boolean, 1 or 0. Default is 0. If set, you may need to provide ``index:*`` tagged values too.

``catalog:metadata`` -- add the field to the metadata record on the query result? Boolean, 1 or 0. If you do not provide ``index:attributes``, the name of the accessor of the field is the default. If ``catalog:metadata_accessor`` is given it will be used instead.

``catalog:metadata_accessor`` -- the accessor used for the metadata (string).

``catalog:name`` -- sometimes you need to add an index to a other catalog than ``portal_catalog`` and its XML-File ``catalog.xml``. Provide a tuple of comma separated strings, id of the catalog and the filename of its configuration file. default is "portal_catalog, Plone Catalog Tool'.

``index:type`` -- the type of index used as (string), for example ``FieldIndex``, ``KeywordIndex``, ``DateIndex`` or any available index in your portal. For known types a default is guessed, such as FieldIndex for StringFields or DateIndex for DateFields. If no guess is possible, we assume a FieldIndex.

``index:attributes`` -- the attributes to use for index (string or comma separated list of strings). This are the methods called at indexing time. Normally it is enough to provide one index method, but for some specific use cases you might need to provide alternatives. If you do not provide this tagged value, the name of the accessor of the field is the default.

``index:name`` -- the name of the index used (string). Use this name in your queries. If you do not provide a name, the name of the accessor of the field is the default.

``index:extras`` -- some indexes are using so called *extras* on installation as configuration. If the index need extras you'll need to declare them here. provide a comma separated list.

``index:properties`` -- some indexes are using *properties* on installation as configuration. If the index need properties you'll need to declare them here. Provide a comma separated list.

``collection:criteria`` -- add the index to the Collection (aka Smart Folder) Indexes available for defining Criteria. Provide a comma seprated list of criteria that will be available by default. Available criterias are: ATBooleanCriterion, ATDateCriteria, ATDateRangeCriterion, ATListCriterion, ATPortalTypeCriterion, ATReferenceCriterion, ATSelectionCriterion, ATSimpleIntCriterion, ATSimpleStringCriterion, ATSortCriterion, ATCurrentAuthorCriterion, ATPathCriterion, ATRelativePathCriterion. You must provide an ``index:type`` as well.

``collection:criteria_label`` -- the display name of the ``collection:criteria``, called *friendly name* (string). Its added to the ``generated.pot`` as a literal. If not given the ``widget:label`` is taken if provided.

``collection:criteria_description`` -- a help text (string), used for ``collection:criteria``. Its added to the ``generated.pot`` as a literal. if not provided the ``widget:description`` is used.

``collection:metadata`` -- register the ``catalog:metadata`` as an available column in a Collection. Can be used as an alternative for ``catalog:metadata``. ``catalog:metadata_accessor`` is used if given.

``collection:metadata_label`` -- the display name of the ``collection:metadata``, called *friendly name* (string), used for index:criteria. Its added to the ``generated.pot`` as a literal. If not given the ``widget:label`` is taken if provided.

``collection:metadata_description`` -- a help text (string), used for ``collection:criteria``. Its added to the ``generated.pot`` as a literal. If not provided the ``collection:criteria_help`` or - if not provided - ``widget:description`` is used.

**DEPRECATED** For backward compatibility reasons we support a sub part of the old style in ArchGenxML Version 1.6 and earlier using the tagged value ``index``. This is deprecated and will be removed in one of the next version of ArchGenXML. A tagged value ``index`` with value like ``index:type`` above creates an index with the accessor. To include the index in catalog metadata (and have the attribute ready to use in the brain objects), append ``:brains`` (same as older ``:schema``), (e.g. ``FieldIndex:brains``). ArchGenXML does longer provides the ability to define multiple indexes using the old declaration style.
