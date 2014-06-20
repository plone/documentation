====================
Fields Reference
====================

.. admonition:: Description

		Attributes of standard Archetypes fields.

.. raw:: html

	<table align="center" class="listing"><tbody><tr class="odd"><th colspan="3">
	<h2>Topics</h2>
	</th>
	</tr><tr class="even"><td>
	<p><a title="Common Field Attributes" href="#common-field-attributes">Common Field Attributes</a></p>
	<p><a href="#boolean_field">BooleanField</a></p>
	<p><a href="#computed_field">ComputedField</a></p>
	<p><a href="#cmf_object_field">CMFObjectField</a></p>
	<p><a href="#datetime_field">DateTimeField</a></p>
	</td>
	<td>
	<p><a href="#file_field">FileField</a></p>
	<p><a href="#fixedpoint_field">FixedPointField</a></p>
	<p><a href="#float_field">FloatField</a></p>
	<p><a href="#image_field">ImageField</a></p>
	<p><a href="#integer_field">IntegerField</a></p>
	</td>
	<td>
	<p><a href="#lines_field">LinesField</a></p>
	<p><a href="#reference_field">ReferenceField</a></p>
	<p><a href="#string_field">StringField</a></p>
	<p><a href="#text_field">TextField</a></p>
	<p>&nbsp;</p>
	</td>
	</tr></tbody></table><p>&nbsp;</p>
	<ul></ul><h2 id="common_attributes"><a id="common-field-attributes" name="common-field-attributes"></a>Common Field Attributes</h2>
	<p>These attributes are common to nearly all fields. Field-specific attributes follow, and are listed by field. Particular fields have different defaults, types, and some  other specialized attributes.</p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Possible Values<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>accessor</td>
	<td>The name of a class method that will return the value of the field. Use this to change how the field is retrieved. If you don't provide a custom method  name here, a default accessor, named getYourFieldName, is going to be created  that just returns the value of the Field.<br></td>
	<td>A class method name; for example, <em>specialGetMethod</em></td>
	<td>None</td>
	</tr><tr class="even"><td>default <br></td>
	<td>The default value for the field. <br></td>
	<td>Type should be appropriate to the field.<br></td>
	<td>None</td>
	</tr><tr class="odd"><td>default_method <br></td>
	<td>The name of a class method returning a value for the field.</td>
	<td>A class method name; for example, <em>getSpecialDescription</em>. <br></td>
	<td>None</td>
	</tr><tr class="even"><td>edit_accessor</td>
	<td>The name of a class method that returns the raw value of a field.</td>
	<td>Any method name (for example, <em>rawGetMethod</em>). <br></td>
	<td>None</td>
	</tr><tr class="odd"><td>enforceVocabulary</td>
	<td>Determines whether or not values outside the vocabulary will be accepted. If True, Archetypes will validate input for the field against the vocabulary. Only values already in the vocabulary will be accepted.<br></td>
	<td><em>True</em> or <em>False</em>. <br></td>
	<td>False</td>
	</tr><tr class="even"><td>index<br>(Plone &lt; 3 only)<br></td>
	<td>If you want this field to be placed in its own catalog index, then specify the type of index here as a string. If you append <em>:schema</em> onto the end of the schema, then this will also be added as a metadata column. (The actual index will be on the field accessor, typically "getFieldName".)<br>Ignored in Plone 3+; use GenericSetup profile for similar functionality.<br></td>
	<td>The name of any index, such as <em>KeywordIndex</em> or <em>KeywordIndex:schema</em>.<br></td>
	<td>None</td>
	</tr><tr class="odd"><td>index_method</td>
	<td>May be used to specify the method called when indexing a field. Use '_at_accessor' to use the default accessor, '_at_edit_accessor' to use the edit accessor, or the name of a method returning the value to be indexed.</td>
	<td><em>_at_accessor</em>, <em>_at_edit_accessor, getIndexAccessor</em> and <em>getIndexAccessorName</em><br></td>
	<td>_at_accessor</td>
	</tr><tr class="even"><td>languageIndependent<br></td>
	<td>Flag for Fields that are independent of the language, such as dates. True tells LinguaPlone that no translation is necessary for this field.</td>
	<td><em>True</em> or <em>False</em></td>
	<td>False</td>
	</tr><tr class="odd"><td>isMetadata <br></td>
	<td>Marks metadata fields. This is currently only needed as a convenience for  the filterFields method of Schema.  Fields marked as metadata are not displayed in the uncustomized base view.</td>
	<td><em>True</em> or <em>False</em></td>
	<td>False</td>
	</tr><tr class="even"><td>mode<br></td>
	<td>The read/write mode of field, as a string; the default is to be read and write. Accessors will not be created without the read mode, and Mutators will not be created without the write mode.<br></td>
	<td>For read only: <em>r</em>, for write only: <em>w</em>, for read and write: <em>rw</em>. <br></td>
	<td>rw</td>
	</tr><tr class="odd"><td>multiValued <br></td>
	<td>Set this to True if the field can have multiple values. This is the case for fields like multiple-selection lists that allow the  selection of multiple values.</td>
	<td><em>True</em> or <em>False</em>. <br></td>
	<td>False</td>
	</tr><tr class="even"><td>mutator <br></td>
	<td>The string name of a class method that changes the value of the Field. If you don't provide a special method name here, a default mutator is generated with the name 'setYourFieldName' to simply store the value.</td>
	<td>A class method name; for example, <em>specialSetMethod</em>.  <br></td>
	<td>None</td>
	</tr><tr class="odd"><td>name</td>
	<td>A unique name for this field. Usually specified as the first item in the field definition. <br></td>
	<td>Any string. Strongly recommended: lowercase, no punctuation or spaces, conforming to standard Python identifier rules. For example, <em>description</em>, <em>user_name</em>, or <em>coffee_bag_6</em>. <br></td>
	<td>No default.</td>
	</tr><tr class="even"><td>primary</td>
	<td>If True, this will be the field that used for  File Transfer Protocol (FTP) and WebDAV requests.  There can be only field that does this; if multiple are defined,  the first one in the schema will be used. You normally set this for the main body attribute.  Only used for TextField and FileField field types.</td>
	<td><em>True</em> or <em>False</em></td>
	<td>False</td>
	</tr><tr class="odd"><td>read_permission<br></td>
	<td>The permission required for the current user to allowed to view or access the field. Only useful if the read mode is activated. This read permission is checked when rendering the widget in read mode.</td>
	<td>A permission identifier imported from Products.CMFCore.permissions</td>
	<td>View</td>
	</tr><tr class="even"><td>required <br></td>
	<td>Specifies that some value for this field required.</td>
	<td><em>True</em> or <em>False</em>.</td>
	<td>False</td>
	</tr><tr class="odd"><td>schemata<br></td>
	<td>Use named schematas to organize fields into grouped views.</td>
	<td>A short string that labels the group.<br></td>
	<td>default</td>
	</tr><tr class="even"><td>searchable <br></td>
	<td>Specifies whether or not the field value will be indexed as part of the SearchableText for the content object. <em>SearchableText</em> is what is checked by the portal's main search.</td>
	<td><em>True</em> or <em>False</em>.</td>
	<td>False</td>
	</tr><tr class="odd"><td>storage<br></td>
	<td>The storage mechanism for the field. The default is <em>Attribute Storage</em>,  which stores the field as an attribute of the object.</td>
	<td>Any valid storage object such as <em>AttributeStorage</em> or <em>SQLStorage</em>.  You can find these in the Archetypes Application Programming Interface (API).<br></td>
	<td>AttributeStorage</td>
	</tr><tr class="even"><td>type<br></td>
	<td>Provided by the field class.. Should never be changed in a Schema.</td>
	<td>None<br></td>
	<td>None</td>
	</tr><tr class="odd"><td>validators<br></td>
	<td>A list or tuple of strings naming validators that will check field input. If you only have one validator, you may specify it as a string.<br> Validators may also be instances of a class implementing the IValidator interface  from from Products.validation.interfaces.IValidator. Providing a class instance  allows you more flexibility as you may set additional parameters.<br> Validators are checked in order specified.</td>
	<td>The names of validators registered via Products.validation; for example, isEmail.</td>
	<td>()</td>
	</tr><tr class="even"><td>vocabulary <br></td>
	<td>Provides the values shown in selection and multi-selection inputs. This may be specified as a static list or as the name of a class method returning the choice list.<br></td>
	<td>A list of strings (in which case keys and values will be the same); a list of 2-tuples of strings [("key1","value 1"),("key 2","value 2"),...]; a Products.Archetypes.utils.DisplayList. Or, the name of a class method returning any of the above.</td>
	<td>()</td>
	</tr><tr class="odd"><td>vocabulary_factory</td>
	<td>Like the vocabulary attribute, in Plone 3 provides the values shown in selection and multi-selection inputs.</td>
	<td>A string name of a Zope 3 style vocabulary factory (a named utility providing zope.schema.interfaces.IVocabularyFactory)</td>
	<td>None</td>
	</tr><tr class="even"><td>widget</td>
	<td>The widget that will be used to render the field for viewing and editing. See the widget reference for a list of available widgets. <br></td>
	<td>An instance of a widget; for example, StringWidget(). <br></td>
	<td>StringWidget()</td>
	</tr><tr class="odd"><td>write_permission<br></td>
	<td>The permission required for the current user to edit the field value. Only interesting if the write mode is activated. The write permission is checked when rendering the widget in write mode.</td>
	<td>A permission identifier imported from Products.CMFCore.permissions</td>
	<td>ModifyPortalContent</td>
	</tr></tbody></table><h2>Standard Fields</h2>
	<p>&nbsp;</p>
	<h3 id="boolean_field">BooleanField</h3>
	<p>Simple storage of <em>True</em> or <em>False</em> for a field.</p>
	<p><strong>Standard properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">example values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>BooleanWidget</td>
	<td>Implemented as a check box.</td>
	<td>
	<ul><li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	<li> <a href="widgets_reference.html#BooleanWidget">BooleanWidget</a></li>
	</ul></td>
	</tr><tr class="even"><td>default</td>
	<td>boolean</td>
	<td>False</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>boolean</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p><strong>Note:</strong> The <em>required</em> attribute for the boolean field is often confusing. It does <em>not</em> require that the box be checked. Use a validator if you need to require the box be checked.</p>
	<h3 id="computed_field">ComputedField</h3>
	<p>Read-only field, whose content cannot be edited directly by users, but is  computed instead from a Python expression. For example, it can be the result of  an operation on the contents from some other fields in the same schema,  e.g. calculating the sum of two or more currency amounts, or composing a  full name from first name and surname.<br> This field is usually not stored in the database, because its content is  calculated on the fly when the object is viewed.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values<br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>ComputedWidget</td>
	<td><br></td>
	<td>
	<ul><li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	<li> <a href="widgets_reference.html#ComputedWidget">ComputedWidget</a></li>
	</ul></td>
	</tr><tr class="even"><td>storage</td>
	<td>storage</td>
	<td>ReadOnlyStorage</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>computed</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>mode</td>
	<td>string</td>
	<td>r</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;"> some possible values<br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>expression</td>
	<td><br></td>
	<td><br></td>
	<td>Evaluated on the object to compute a value.</td>
	<td><br></td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="cmf_object_field">CMFObjectField</h3>
	<p>Used for storing values inside a CMF Object, which can have workflow. Can only be used for BaseFolder-based content objects.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values<br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>FileWidget</td>
	<td><br></td>
	<td>
	<ul><li><a href="widgets_reference.html#LabelWidget">LabelWidget</a></li>
	<li><a href="widgets_reference.html#FileWidget">FileWidget</a></li>
	</ul></td>
	</tr><tr class="even"><td>storage</td>
	<td>storage</td>
	<td>ObjectManagedStorage</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>object</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>portal_type</td>
	<td><br></td>
	<td>File</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>workflowable</td>
	<td><br></td>
	<td>True</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>default_mime_type</td>
	<td><br></td>
	<td>application/octet-stream</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><h3 id="datetime_field">DateTimeField</h3>
	<p>Used for storing dates and times.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>CalendarWidget</td>
	<td><br></td>
	<td>
	<ul><li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	<li> <a href="widgets_reference.html#CalendarWidget">CalendarWidget</a> </li>
	</ul></td>
	</tr><tr class="even"><td>default</td>
	<td>DateTime</td>
	<td><br></td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>datetime</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p><strong>Note:</strong> The default for the DateTimeField needs to be specified as a DateTime object. If you need to set the current date/time as the default, you'll need to use the default_method attribute to specify a class method returning the current date/time as a DateTime object.</p>
	<p>Example:</p>
	<pre>from DateTime.DateTime import DateTime

	# inside the schema definiton
	&nbsp;&nbsp;&nbsp; DateTimeField('dateAdded',
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; searchable = 1,
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; required = 0,
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; <strong>default_method = 'getDefaultTime',</strong>
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; widget = CalendarWidget(
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; label = 'Date Added'
	&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ),
	&nbsp;&nbsp;&nbsp; ),

	...

	#inside the content class definition
	    def getDefaultTime(self):  # function to return the current date and time
	        return DateTime()</pre>
	<h3 id="file_field"></h3>
	<h3 id="file_field"><a id="filefield" name="filefield"></a>FileField</h3>
	<p>Storage for large chunks of data such as plain-text files, office-automation documents, and so on. If you're using Plone 4 or newer, consider using <em>plone.app.blob.field.BlobField</em> instead, that stores the file data outside of the ZODB and accepts the same parameters as <em>atapi.FileField</em>.&nbsp;See&nbsp;<a href="../../../upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/use-plone.app.blob-based-blob-storage">this page</a> for info about migration.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>FileWidget</td>
	<td><br></td>
	<td>
	<ul><li> <a href="widgets_reference.html#FileWidget">FileWidget</a> </li>
	<li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	</ul></td>
	</tr><tr class="even"><td>default</td>
	<td>string</td>
	<td><br></td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>file</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>primary</td>
	<td><br></td>
	<td>False</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>default_content_type</td>
	<td><br></td>
	<td>application/octet</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>primary</td>
	<td>boolean</td>
	<td>False</td>
	<td>Set this <em>True</em> to mark the field as primary for FTP or WebDAV.</td>
	<td><br></td>
	</tr></tbody></table><p><strong>Note:</strong> File field values are stored as strings. It's a common practice to use streams to read/write the values as if they were files.</p>
	<p>&nbsp;</p>
	<h3 id="fixedpoint_field">FixedPointField</h3>
	<p>For storing numerical data with fixed points.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;"> some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>DecimalWidget</td>
	<td><br></td>
	<td>
	<ul><li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a></li>
	<li><a href="widgets_reference.html#DecimalWidget">DecimalWidget</a></li>
	</ul></td>
	</tr><tr class="even"><td>validators</td>
	<td>validators</td>
	<td>isDecimal</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>default</td>
	<td>string</td>
	<td>0.00</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>type</td>
	<td><br></td>
	<td>fixedpoint</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>precision</td>
	<td><br></td>
	<td>2</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="float_field">FloatField</h3>
	<p>For storing numerical data with floating points.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>default</td>
	<td>string</td>
	<td>0.0</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>type</td>
	<td><br></td>
	<td>float</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="image_field"><a id="imagefield" name="imagefield"></a>ImageField</h3>
	<p>Stores an image and allows dynamic resizing of the image. If you're using Plone 4 or newer, consider using <em>plone.app.blob.field.ImageField</em> instead, that stores the image data outside of the ZODB, and accepts the same parameters as <em>atapi.ImageField</em>. See <a href="../../../upgrade-guide/version/upgrading-plone-3-x-to-4.0/updating-add-on-products-for-plone-4.0/use-plone.app.blob-based-blob-storage">this page</a> for info about migration.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;"> some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>ImageWidget</td>
	<td><br></td>
	<td>
	<ul><li> <a href="widgets_reference.html#ImageWidget">ImageWidget</a> </li>
	<li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	</ul></td>
	</tr><tr class="even"><td>default</td>
	<td>string</td>
	<td><br></td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>image</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>allowable_content_types</td>
	<td>tuple of MIME strings</td>
	<td>Specifies the types of images that will be allowed.</td>
	<td>('image/gif','image/jpeg','image/png')</td>
	<td>('image/jpeg','image/png')</td>
	</tr></tbody></table><p><strong>Note:</strong> Archetypes Image field values are stored as strings. It's a common practice to use streams to read/write the values as if they were files.</p>
	<p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>original_size</td>
	<td>tuple (w,h)</td>
	<td>None</td>
	<td>The size to which the original image will be scaled. If it's None, then no scaling will take place; the original size will be retained. Caution: the aspect ratio of the image may be changed.</td>
	<td>(640,480)</td>
	</tr><tr class="even"><td>max_size</td>
	<td>tuple (w,h)</td>
	<td>None</td>
	<td>If specified then the image is scaled to be no bigger than either of the given  values of width or height. Aspect ratio is preserved. Useful to prevent storage  of megabytes of unnecessary image data.</td>
	<td>(1024,768)</td>
	</tr><tr class="odd"><td>sizes</td>
	<td>dict</td>
	<td>{'thumb':(80,80)}</td>
	<td>A dictionary specifying any additional scales in which the image will be available. Dictionary entries should be of the form 'scaleName':(width,height). The scaled versions will be accessible as object/&lt;imagename&gt;_&lt;scalename&gt;, e.g. object/image_mini.<br></td>
	<td>{ 'mini' : (80,80),     'normal' : (200,200),     'big' : (300,300),     'maxi' : (500,500)}</td>
	</tr><tr class="even"><td>pil_quality</td>
	<td>integer</td>
	<td>88</td>
	<td>A JPEG quality setting (range 0 to 100). Lower numbers yield high compression  and low image quality. High numbers yield low compression and better quality.</td>
	<td>50 (a medium quality)</td>
	</tr></tbody></table><h4>Using Image Scales</h4>
	<p>To display the original image (possibly rescaled if you used original_size or  max_size attributes), you may use a URL like "http://url_of_content_object/imageFieldName" as the SRC attribute of an IMG tag where <em>url_of_content_object</em> is the URL of the content object and <em>imageFieldName</em> is the name of the image field.</p>
	<p>To display one of the scales, use a URL like "http://url_of_content_object/imageFieldName_scale",<br> where <em>scale</em> is one of the keys of the <em>sizes</em> dictionary.</p>
	<p><em>Attention</em>: The direct attribute access as shown above works only together with AttributeStorage, which will be used by default. To avoid heavy memory consumption on sites with many images it is recommended to use AnnotationStorage for the ImageField.</p>
	<p>You may also generate a ready-to-insert IMG tag with the python code:</p>
	<pre>obj.getField('image').tag(obj, scale='mini')</pre>
	<p>if <em>obj</em> is your content object, <em>image</em> the name of your image  field, and <em>mini</em> the name of your scale.</p>
	<p>You may rescale to other sizes than those in the sizes field attribute with code like:</p>
	<pre>obj.getField('image').tag(obj, height=480, width=640, alt='alt text',
	            css_class='css_class_selector', title='html title attribute')</pre>
	<p>From Plone 4 on, the plone.app.imaging package introduces a new way to control image scales, factoring this functionality out of Archetypes for reutilization. For example:</p>
	<pre>&lt;img tal:define="scales context/@@images;
	                 thumbnail python: scales.scale('image', width=64, height=64);"
	     tal:condition="thumbnail"
	     tal:attributes="src thumbnail/url;
	                     width thumbnail/width;
	                     height thumbnail/height" /&gt;</pre>
	<p>Would create an up to 64 by 64 pixel scaled down version of the image stored in the "image" field of the context. For further info, check the <a href="http://dev.plone.org/plone/browser/plone.app.imaging/trunk/README.txt" class="external-link">plone.app.imaging README file</a>.</p>
	<h3 id="integer_field">IntegerField</h3>
	<p>For storing numerical data as integers.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>IntegerWidget</td>
	<td><br></td>
	<td>
	<ul><li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	<li> IntegerWidget </li>
	</ul></td>
	</tr><tr class="even"><td>default</td>
	<td>integer</td>
	<td>0</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>integer</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;"> some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>size</td>
	<td><br></td>
	<td>10</td>
	<td>Sets the size of the input field.</td>
	<td><br></td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="lines_field">LinesField</h3>
	<p>Used for storing text as a list, for example a list of data such as keywords.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>LinesWidget</td>
	<td><br></td>
	<td>
	<ul><li> <a href="widgets_reference.html#KeywordWidget">KeywordWidget</a> </li>
	<li> <a href="widgets_reference.html#LinesWidget">LinesWidget</a> </li>
	<li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	<li> <a href="widgets_reference.html#MultiSelectionWidget">MultiSelectionWidget</a> </li>
	<li> <a href="widgets_reference.html#PicklistWidget">PicklistWidget</a> </li>
	<li> <a href="widgets_reference.html#InAndOutWidget">InAndOutWidget</a> </li>
	</ul></td>
	</tr><tr class="even"><td>default</td>
	<td>string</td>
	<td>()</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>lines</td>
	<td><br></td>
	<td><br></td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="reference_field">ReferenceField</h3>
	<p>Used for storing references to other Archetypes Objects.</p>
	<p><strong>Standard properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>ReferenceWidget</td>
	<td><br></td>
	<td>
	<ul><ul><li> <a href="widgets_reference.html#ReferenceWidget">ReferenceWidget</a> </li>
	</ul><ul><li> <a href="widgets_reference.html#ReferenceBrowserWidget">ReferenceBrowserWidget</a> </li>
	<li> <a href="widgets_reference.html#LabelWidget">LabelWidget</a> </li>
	<li> <a href="widgets_reference.html#InAndOutWidget">InAndOutWidget</a> </li>
	</ul></ul></td>
	</tr><tr class="even"><td>index_method</td>
	<td><br></td>
	<td>_at_edit_accessor</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>type</td>
	<td><br></td>
	<td>reference</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="event even"><td>multiValued</td>
	<td>boolean</td>
	<td>False</td>
	<td>Set multiValued True to allow multiple references (one-to-many), or False to allow only a single reference (one-to-one).</td>
	<td><br></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values <br><span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>relationship</td>
	<td><br></td>
	<td><br></td>
	<td>Specifes an identifier for the type of relationships associated with the field. This should be unique within your content type, but has no larger meaning. A ReferenceField allows you to edit the set of references with a  particular relationship identifier from the current content object to other objects.</td>
	<td>'KnowsAbout', 'Owns', 'WorksWith'</td>
	</tr><tr class="even"><td>allowed_types</td>
	<td>tuple of portal types</td>
	<td>()</td>
	<td>Determines all the portal types that will be searched to find objects that the user can make a reference to. It also specifies the Types that should be allowed to be added directly from the reference widget. This is only activated if the addable property is set. An empty list or tuple will allow references to all portal types.</td>
	<td>('Document', 'File')</td>
	</tr><tr class="odd"><td>allowed_types_method</td>
	<td>string</td>
	<td>None</td>
	<td>A string containing the name of a class method that will return a list of portal types to which references are allowed.</td>
	<td><br></td>
	</tr><tr class="even"><td>vocabulary_display_path_bound</td>
	<td>integer</td>
	<td>5</td>
	<td>Sets a limit for presentation of reference items. Up to this limit, only titles are displayed. Above the limit, the path to the referenced object is also displayed. The idea is that if there are a large number of referenced items, the user will  need help to differentiate them.</td>
	<td><br></td>
	</tr><tr class="odd"><td>vocabulary_custom_label</td>
	<td>string</td>
	<td>None</td>
	<td>A string containing a python expression that will be evaluated to get the displayed text for a referenced item. Your expression may use the variable "b" which will be a reference to the catalog brain returned by the reference lookup.</td>
	<td>"b.getObject().title_or_id()"</td>
	</tr></tbody></table><p>&nbsp;</p>
	<p><strong>More about References</strong></p>
	<p>Archetypes References work with any object providing the IReferenceable interface. They are mantained in the uid_catalog and reference_catalog catalogs. You can find both at the root of your Plone site. Check them to see their indexes and metadata.</p>
	<p>Althought you could use the ZCatalogs API to manage Archetypes references, these catalogs are rarely used directly. A ReferenceField and its API is used instead.</p>
	<p>To set a reference, you can use the setter method with either a list of UIDs or one UID string, or one object or a list of objects (in the case the ReferenceField is multi-valued) to which you want to add a reference to. Note that <em>Non</em>e and <em>[]</em> are equal.<br>For example, to set a reference from the <em>myct1</em> object to the <em>areferenceableobjec</em>t object using the <em>MyReferenceField</em> field:</p>
	<pre>&nbsp;&nbsp;&nbsp; &gt;&gt;&gt; myct1.setMyReferenceField(areferenceableobject)</pre>
	<p>To get the referenced object(s), just use the getter method. Note that what you get are<br>the objects themselves, not their catalog brains.</p>
	<pre>&nbsp;&nbsp;&nbsp; &gt;&gt;&gt; myct1.getMyReferenceField()</pre>
	<h3 id="string_field"></h3>
	<h3 id="string_field">StringField</h3>
	<p>A field for plain-text, unformatted strings.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>default</td>
	<td>string</td>
	<td><br></td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>type</td>
	<td><br></td>
	<td>string</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>StringWidget</td>
	<td><br></td>
	<td>
	<ul><li><a href="widgets_reference.html#LabelWidget">LabelWidget</a></li>
	<li><a href="widgets_reference.html#StringWidget">StringWidget</a></li>
	<li><a href="widgets_reference.html#SelectionWidget">SelectionWidget</a></li>
	</ul></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>default_content_type</td>
	<td>string MIME type</td>
	<td>text/plain</td>
	<td><br></td>
	<td>Rarely changed.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="text_field">TextField</h3>
	<p>A string field typically used for longer, multi-line strings. The string may also be transformed into alternative formats.</p>
	<p><strong>Standard</strong><strong> properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>default</td>
	<td>string</td>
	<td><br></td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="even"><td>type</td>
	<td><br></td>
	<td>text</td>
	<td><br></td>
	<td><br></td>
	</tr><tr class="odd"><td>widget</td>
	<td>widget</td>
	<td>StringWidget</td>
	<td><br></td>
	<td>
	<ul><li><a href="widgets_reference.html#LabelWidget">LabelWidget</a></li>
	<li><a href="widgets_reference.html#TextAreaWidget">TextAreaWidget</a></li>
	<li><a href="widgets_reference.html#RichWidget">RichWidget</a></li>
	</ul></td>
	</tr></tbody></table><p><strong>Special properties</strong></p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th> <th style="cursor: pointer;">some possible values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>primary</td>
	<td>boolean</td>
	<td>False</td>
	<td>Set this <em>True</em> to mark the field as primary for FTP or WebDAV. <br></td>
	<td><br></td>
	</tr><tr class="even"><td>default_content_type</td>
	<td>string MIME type</td>
	<td>text/plain</td>
	<td>A string designating MIME the default input type for the field.</td>
	<td>text/plain, text/html</td>
	</tr><tr class="odd"><td>allowable_content_types</td>
	<td>tuple of MIME-type strings</td>
	<td>('text/plain',)</td>
	<td>Used in the TextArea and Rich widgets to let the user choose between different text formats in which the content is entered.</td>
	<td>('text/plain', 'text/html',)</td>
	</tr><tr class="even"><td>default_output_type</td>
	<td>string MIME type</td>
	<td>text/plain</td>
	<td>This is used by the accessor (get) method to and decides which MIME-Type the content should be transformed into if no special MIME-Type is demanded.</td>
	<td>'text/html', 'text/x-html-safe'</td>
	</tr></tbody></table>
