=======================
Widgets Reference
=======================

.. admonition:: Description

		This page is a syntax reference and general guide for defining and using Widgets.

.. raw:: html

	<table class="listing"><thead><tr><th align="center" colspan="3" style="cursor: pointer;">
	<table class="listing"><thead><tr><th align="center" colspan="3" style="cursor: pointer;">
	<h3>Widget Attribute Topics<br></h3>
	<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>
	<p><a href="#common_attributes">Common Widget Attributes</a></p>
	<p><a href="#BooleanWidget">BooleanWidget</a></p>
	<p><a href="#CalendarWidget">CalendarWidget</a></p>
	<p><a href="#ComputedWidget">ComputedWidget</a></p>
	<p><a href="#DecimalWidget">DecimalWidget</a></p>
	<p><a href="#FileWidget">FileWidget</a></p>
	<p><a href="#ImageWidget">ImageWidget</a></p>
	</td>
	<td>
	<p><a href="#InAndOutWidget">InAndOutWidget</a></p>
	<p><a href="#IntegerWidget">IntegerWidget</a></p>
	<p><a href="#KeywordWidget">KeywordWidget</a></p>
	<p><a href="#LabelWidget">LabelWidget</a></p>
	<p><a href="#LinesWidget">LinesWidget</a></p>
	<p><a href="#MultiSelectionWidget">MultiSelectionWidget</a></p>
	<p><a href="#PasswordWidget">PasswordWidget</a></p>
	</td>
	<td>
	<p><a href="#PicklistWidget">PicklistWidget</a></p>
	<p><a href="#ReferenceWidget">ReferenceWidget</a></p>
	<p><a href="#ReferenceBrowserWidget">ReferenceBrowserWidget</a></p>
	<p><a href="#RichWidget">RichWidget</a></p>
	<p><a href="#SelectionWidget">SelectionWidget</a></p>
	<p><a href="#StringWidget">StringWidget</a></p>
	<p><a href="#TextAreaWidget">TextAreaWidget</a></p>
	</td>
	</tr></tbody></table><h2 id="common_attributes">Common Widget Attributes</h2>
	<p>The table below describes attributes common to nearly all widgets. Illustrations
	and special attributes listings for each of the standard widgets follows.</p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Possible Values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>condition <br></td>
	<td>A string containing a TALES expression to determine whether or not a field/widget is
	included on a view or edit page.
	This does not distinguish between view and edit mode.<br></td>
	<td>Your TALES expression may referenc the current context as 'object' and the Plone site root as 'portal'<br></td>
	</tr><tr class="even"><td>description <br></td>
	<td>Help or explanatory text for the field. Usually shown on the edit form under the label and above the input field.</td>
	<td><br></td>
	</tr><tr class="odd"><td>description_msgid</td>
	<td>The i18n identifier for the description message. Used to translate the message. Should be unique within your product's i18n domain.</td>
	<td>'help_type_field'</td>
	</tr><tr class="even"><td>label</td>
	<td>The label that will appear in the field.</td>
	<td> Any string, for example, <em>Start Date</em> for a field <em>start_date</em>. Also <em>label_msgid</em> (takes string message ids for i18n.)</td>
	</tr><tr class="odd"><td>label_msgid</td>
	<td>The i18n identifier for the label message. Should be unique within your product's i18n domain.</td>
	<td>'label_type_field'</td>
	</tr><tr class="even"><td>i18n_domain</td>
	<td>The i18n domain specifier for your product. This should be unique for your product, and will be used to find the translation catalogs for your product.</td>
	<td>'productname'</td>
	</tr><tr class="odd"><td> modes</td>
	<td> The modes that this widget will be shown in; by default there are two modes: view and edit.</td>
	<td> A list of modes as strings; by default <em>("view", "edit")</em>.</td>
	</tr><tr class="even"><td> populate</td>
	<td> If this is enabled, the view and edit fields will be populated. Usually this is enabled, but for fields such as a password field, this shouldn't
	be the case. Usually this is true by default.</td>
	<td> <em>True</em> or <em>False</em></td>
	</tr><tr class="odd"><td> postback</td>
	<td> If this is enabled, then when an error is raised, the field is
	repopulated; for fields such as a password field, this shouldn't be the
	case. Usually this is True by default.</td>
	<td> <em>True</em> or <em>False</em></td>
	</tr><tr class="even"><td> visible</td>
	<td> Determines whether or not the field is visible view and edit mode.
	This is a
	dictionary mapping the view mode to a string describing the
	visibility.
	Choices are <em>visible</em>, <em>hidden</em> (rendered in an HTML hidden form value), <em>invisible</em> (not rendered at all).</td>
	<td>For example, <em>{'view': 'visible', 'edit': 'hidden' }</em> means that the view will show, but the edit page will hide the value.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h2>Standard Widgets</h2>
	<p>&nbsp;</p>
	<h3 id="BooleanWidget">BooleanWidget</h3>
	<p>Renders an HTML checkbox, from which users can choose between two values such as on/off, true/false, yes/no.</p>
	<blockquote>
	<p><img width="369" height="39" alt="booleanwidget.png" src="booleanwidget.png">&nbsp;</p>
	</blockquote>
	<h3 id="CalendarWidget">CalendarWidget</h3>
	<p>Renders a HTML input box with a helper popup box for choosing dates.</p>
	<blockquote>
	<p><img width="375" height="216" alt="datetimewidget.png" src="datetimewidget.png"></p>
	</blockquote>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>format</td>
	<td>string</td>
	<td>
	<br></td>
	<td>Defines the date/time format using strftime, e.g. '%d.%m.%Y', for the view.
	(See the strftime section of the <a href="http://docs.python.org/lib/module-time.html">Python time documentation</a>.
	<br>
	If this is not specified, the long form of the portal's local time format is used.</td>
	</tr><tr class="even"><td>future_years</td>
	<td>integer</td>
	<td>
	5</td>
	<td>Specifies the number of future years offered by the year drop-down portion
	of the date widget. Do not use both future_year and end_year.
	(Plone 2.5+)</td>
	</tr><tr class="odd"><td>starting_year</td>
	<td>integer</td>
	<td>1999</td>
	<td>The first year offered by the year drop-down. (Plone 2.5+)</td>
	</tr><tr class="even"><td>ending_year</td>
	<td>integer</td>
	<td>
	None</td>
	<td>The final year offered by the year drop-down.
	Do not use both future_years and end_year. (Plone 2.5+)</td>
	</tr><tr class="odd"><td>show_hm</td>
	<td>boolean</td>
	<td>True</td>
	<td>Should the widget ask for a time as well as a date? (Plone 2.5+)</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="ComputedWidget">ComputedWidget</h3>
	<p>Generally used for ComputedField field type, it renders the computed value.
	Note that if your field has a vocabulary, and the field value is a key in that
	vocabulary, the widget will lookup the key in the vocabulary and show the result.</p>
	<h4>Standard Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>modes</td>
	<td>tuple</td>
	<td>
	('view', 'edit')</td>
	<td>As ComputedField is a read-only field, this property can be used to prevent
	the widget from appearing in edit templates, by setting it to just ('view',).</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="DecimalWidget">DecimalWidget</h3>
	<p>In edit mode, renders an HTML text input box which accepts a fixed point value.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>thousands_commas</td>
	<td>boolean</td>
	<td>False</td>
	<td>In view mode, formats the value to shows commas for thousands.
	For example, when thousands_commas is True, "7632654849635.02" is displayed as "7,632,654,849,635.02".
	(Note: this feature is not localized; it uses commas independent of locale.</td>
	</tr><tr class="even"><td>whole_dollars</td>
	<td>boolean</td>
	<td>
	False</td>
	<td>Shows whole dollars in view, leaving out the cents. Enter "1.123", and "$1" is shown.
	(Note: this feature is not localized; it uses the dollar sign independent of locale.)</td>
	</tr><tr class="odd"><td>maxlength</td>
	<td><br></td>
	<td>
	255</td>
	<td>Maximum input size; sets the HTML input tag's maxlength attribute.</td>
	</tr><tr class="even"><td>dollars_and_cents</td>
	<td>boolean</td>
	<td>False</td>
	<td>In view mode, shows dollars and cents. Enter "123.123" and "$123.12" is shown.
	(Note: this feature is not localized; it always uses the dollar sign, period,
	and two digits precision.)</td>
	</tr><tr class="odd"><td>size</td>
	<td><br></td>
	<td>5</td>
	<td>Size of the input field; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="FileWidget">FileWidget</h3>
	<p>Renders an HTML widget so a user can upload a file.</p>
	<blockquote>
	<p><img width="263" height="137" alt="filewidget.png" src="filewidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h3 id="ImageWidget">ImageWidget</h3>
	<p>Renders an HTML widget that can be used to upload, display, delete, and
	replace images. You can provide a <em>display_threshold</em> that allows
	you to set the size of an image; if it's below this
	size, the image will display in the Web page.</p>
	<blockquote>
	<p><img width="265" height="269" alt="imagewidget.png" src="imagewidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>display_threshold</td>
	<td>integer</td>
	<td>102400</td>
	<td>Only display the image inline if img.getSize() &lt;= display_threshold</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="InAndOutWidget">InAndOutWidget</h3>
	<p>In edit mode, renders a widget for moving items from one list to another.
	Items are removed from the source list.
	This can be used to choose multiple values from a list. This provides a good
	alternative to the MultiSelectionWidget when the vocabulary is too long for checkboxes.</p>
	<blockquote>
	<p><img width="376" height="149" alt="inandoutwidget.png" src="inandoutwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<p>&nbsp;</p>
	<h3 id="IntegerWidget">IntegerWidget</h3>
	<p>A simple HTML input box for a string.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>size</td>
	<td><br></td>
	<td>
	6</td>
	<td>Size of the select widget; sets the HTML select tag's size attribute.</td>
	</tr></tbody></table><table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>maxlength</td>
	<td><br></td>
	<td>
	255</td>
	<td>Maximum input size; sets the HTML input tag's maxlength attribute</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>5</td>
	<td>Size of the input field; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="KeywordWidget">KeywordWidget</h3>
	<p>
	This widget allows the user to select keywords or categories from a list. It is
	used for the <em>Categories</em> field in the Categorization Schema (Plone 3+)
	or the equivalent <em>Keywords</em> field on the Properties Tab (Plone &lt; 3)
	of a content object.<br>
	Keywords are drawn from the field vocabulary and/or the unique values for the
	field in a specified catalog.<br>
	Additional keywords may be added unless the enforceVocabulary property of the
	field is True.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>vocab_source</td>
	<td><br></td>
	<td>
	portal_catalog</td>
	<td>Sets
	the catalog to search for additional vocabulary to be combined with the
	vocabulary defined for the field. Additional keywords from existing content are
	found using catalog.uniqueValuesFor(fieldName).</td>
	</tr><tr class="even"><td>roleBasedAdd</td>
	<td><br></td>
	<td>True</td>
	<td>Only
	shows the "New keywords" input for adding keywords if the current user
	has one of the roles stored in the allowRolesToAddKeywords property in
	the site_properties property sheet in portal_properties</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="LabelWidget">LabelWidget</h3>
	<p>Used to display labels on forms -- without values or form input elements.</p>
	<p>&nbsp;</p>
	<h3 id="LinesWidget">LinesWidget</h3>
	<p>Displays a text area so that users can enter a list of values, one per line.</p>
	<blockquote>
	<p><img width="367" height="113" alt="lineswidget.png" src="lineswidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>rows</td>
	<td>integer</td>
	<td>
	5</td>
	<td>Rows of the lines widget; sets the HTML textarea tag's rows attribute.</td>
	</tr><tr class="even"><td>cols</td>
	<td>integer</td>
	<td>
	40</td>
	<td>Columns of the lines widget; sets the HTML textarea tag's cols attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="MultiSelectionWidget">MultiSelectionWidget</h3>
	<p>A selection widget; by default it's an
	HTML select widget which can be used to choose multiple values. As a
	checkbox users can choose one or more values from a list (useful if the
	list is short).</p>
	<blockquote>
	<p><img width="330" height="122" alt="multiselectionwidget-listbox.png" src="multiselectionwidget-listbox.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<blockquote>
	<p><img width="374" height="177" alt="multiselectionwidget-checkbox.png" src="multiselectionwidget-checkbox.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>format</td>
	<td>string</td>
	<td>select</td>
	<td>Possible values: 'select' or 'checkbox'. Uses a either a series of checkboxes or
	a multi-selection list. Note that checkboxes have much better usability for short
	vocabularies. Consider using the InAndOutWidget for longer vocabularies.</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>
	5</td>
	<td>Defines the size of the multi-select list. Does not apply for checkboxes.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="PasswordWidget">PasswordWidget</h3>
	<p>Renders an HTML password input.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>maxlength</td>
	<td><br></td>
	<td>
	255</td>
	<td>Maximum input size; sets the HTML input tag's maxlength attribute.</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>20</td>
	<td>Size of the input field; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><h4>Standard Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>populate</td>
	<td>boolean</td>
	<td>False</td>
	</tr><tr class="even"><td>postback</td>
	<td>boolean</td>
	<td>False</td>
	</tr><tr class="odd"><td>modes</td>
	<td><br></td>
	<td>('edit',)</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="PicklistWidget">PicklistWidget</h3>
	<p>Similar to the InAndOutWidget, but the values stay in the source list after
	selection.</p>
	<blockquote>
	<p><img width="368" height="155" alt="picklistwidget.png" src="picklistwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>size</td>
	<td>integer</td>
	<td>6</td>
	<td>Size of the selection box; sets the HTML select tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="ReferenceWidget">ReferenceWidget</h3>
	<p>Renders an HTML text input box which accepts a list of possible reference
	 values. Used in combination with the Reference Field.<br><strong>Note:</strong> In Plone 2.5 and above, the ReferenceBrowserWidget is
	 a usually a better choice for a reference widget due to its ability to browse for content
	 referenceable objects.</p>
	<blockquote>
	<p><img width="381" height="110" alt="referencewidget.png" src="referencewidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>checkbox_bound</td>
	<td><br></td>
	<td>5</td>
	<td>When the number of items exceeds this value, multi-selection lists are used. Otherwise, radio buttons or checkboxes are used.</td>
	</tr><tr class="even"><td>destination</td>
	<td><br></td>
	<td>None</td>
	<td>May be:
	<ul><li>".", context object;</li><li>None, any place where Field.allowed_types can be added;</li><li>string path;</li><li>name of method on instance (it can be a combination list);</li><li>a list, combining all item above;</li><li>a dict, where {portal_type:} destination is relative to portal root</li></ul></td>
	</tr><tr class="odd"><td>addable</td>
	<td><br></td>
	<td>False</td>
	<td>Create createObject link for every addable type</td>
	</tr><tr class="even"><td>destination_types</td>
	<td><br></td>
	<td>None</td>
	<td>Either
	a single type given as a string, or a list of types given as a string,
	defining what types we allow adding to. Only applies when addable is
	set on the widget.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="ReferenceBrowserWidget">ReferenceBrowserWidget</h3>
	<p>A sophisticated widget for browsing, adding and deleting references.<br>Standard in Plone 2.5+, available for earlier versions as an add-on product.<br>Import from&nbsp;<em>Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget</em>&nbsp;in Plone 2.5 and 3. In Plone 4, this widget has been improved and now lives in<em>archetypes.referencebrowserwidget.ReferenceBrowserWidget</em>.<strong><strong></strong></strong></p>
	<blockquote>
	<p><img width="386" height="468" alt="" src="referencebrowserwidget.png"></p>
	</blockquote>
	<h4>Special Properties</h4>
	<table class="listing" style="text-align: left;"><thead><tr><th style="text-align: left; cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>size</td>
	<td>integer</td>
	<td><br></td>
	<td>Size of the field if not multiValued; sets the HTML input tag's size attribute.</td>
	</tr><tr class="even"><td>default_search_index</td>
	<td>string</td>
	<td>SearchableText</td>
	<td>when a user searches in the popup, this index is used by default</td>
	</tr><tr class="odd"><td>show_indexes</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, a drop-down list is shown in the popup to select the index used for searching. If set to False, default_search_index will be used.</td>
	</tr><tr class="even"><td>available_indexes</td>
	<td>dict</td>
	<td>{}</td>
	<td>Optional dictionary containing all the indexes that can be used for searching along with their friendly names. Format: {'catalogindex':'Friendly Name of Index', ... } The friendly names are shown in the widget.<br><strong>Caution:</strong>&nbsp;If you set show_indexes True, but do not use this property to specify indexes, then all the indexes will be shown.</td>
	</tr><tr class="odd"><td>allow_search</td>
	<td>boolean</td>
	<td>True</td>
	<td>If True, a search form is included in the popup.</td>
	</tr><tr class="even"><td>allow_browse</td>
	<td>True</td>
	<td>Allows the user to browse content to find referenceable content.</td>
	<td><br></td>
	</tr><tr class="odd"><td>startup_directory</td>
	<td>string</td>
	<td>''</td>
	<td>Directory shown when the popup opens. Optional. When empty, the current folder is used. See the ATReferenceBrowser readme.txt for advanced usage.</td>
	</tr><tr class="even"><td>base_query</td>
	<td>dict or name of method</td>
	<td><br></td>
	<td>Defines query terms that will apply to all searches, mainly useful to create specific restrictions when allow_browse=0. Can be either a dictonary with query parameters, or the name of a method or callable available in cotext that will return such a dictionary.</td>
	</tr><tr class="odd"><td>force_close_on_insert</td>
	<td>boolean</td>
	<td>False</td>
	<td>If true, closes the popup when the user choses insert. This overrides the default behavior in multiselect mode.</td>
	</tr><tr class="even"><td>search_catalog</td>
	<td>string</td>
	<td>'portal_catalog'</td>
	<td>Specifies the catalog used for searches</td>
	</tr><tr class="odd"><td>allow_sorting</td>
	<td>boolean</td>
	<td>False</td>
	<td>Allows changing the order of referenced objects (requires multiValued).</td>
	</tr><tr class="even"><td>show_review_state</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, popup will display the workflow state for objects.</td>
	</tr><tr class="odd"><td>show_path</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, display the relative path (relative to the portal object) of referenced objects.</td>
	</tr><tr class="even"><td>only_for_review_states</td>
	<td><br></td>
	<td>None</td>
	<td>If set, content items are only referenceable if their workflow state matches one of the specified states. If None there will be no filtering by workflow state.</td>
	</tr><tr class="odd"><td>image_portal_types</td>
	<td>sequence</td>
	<td>()</td>
	<td>Use to specify a list of image portal_types. Instances of these portal types are previewed within the popup widget</td>
	</tr><tr class="even"><td>image_method</td>
	<td>string</td>
	<td>None</td>
	<td>Specifies the name of a method that is added to the image URL to preview the image in a particular resolution (e.g. 'mini' for thumbnails).</td>
	</tr><tr class="odd"><td>history_length</td>
	<td>integer</td>
	<td>0</td>
	<td>If not zero, enables a history feature that show the paths of the last N visited folders.</td>
	</tr><tr class="even"><td>restrict_browsing_to_startup_directory</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, the user will not be able to browse above the starting directory.</td>
	</tr></tbody></table><p>The cited Plone 4 implementation of this widget includes the following additional properties:</p>
	<h4>Special Properties</h4>
	<table class="listing" style="text-align: left;"><thead><tr><th style="text-align: left; cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>startup_directory_method</td>
	<td>string</td>
	<td>''<br></td>
	<td>The name of a method or variable that, if available at the instance, will be used to obtain the path of the startup directory. If present, 'startup_directory' will be ignored.</td>
	</tr><tr class="even"><td valign="top">show_results_without_query</td>
	<td valign="top">bool<br></td>
	<td valign="top">False<br></td>
	<td valign="top">Don't ignore empty queries, but display results.</td>
	</tr><tr class="odd"><td valign="top">hide_inaccessible</td>
	<td valign="top">bool<br></td>
	<td valign="top">False<br></td>
	<td valign="top">Don't show inaccessible objects (no permission) in view mode.</td>
	</tr><tr class="even"><td valign="top">popup_width</td>
	<td valign="top">integer<br></td>
	<td valign="top">500<br></td>
	<td valign="top">Width of popup window in pixels.</td>
	</tr><tr class="odd"><td valign="top">popup_height</td>
	<td valign="top">integer<br></td>
	<td valign="top">550<br></td>
	<td valign="top">Height of popup window in pixels</td>
	</tr><tr class="even"><td valign="top">popup_name</td>
	<td valign="top">string<br></td>
	<td valign="top">'popup'<br></td>
	<td valign="top">Name of template to be used for popup. To use another template you have to register a named adapter for this template.</td>
	</tr></tbody></table><p id="RichWidget">Example of registering a popup in ZCML:</p>
	<pre id="RichWidget">&lt;zope:adapter<br>    for="Products.Five.BrowserView"<br>    factory=".view.default_popup_template"<br>    name="popup"<br>    provides="zope.formlib.namedtemplate.INamedTemplate" /&gt;<br></pre>
	<h3 id="ReferenceBrowserWidget">RichWidget</h3>
	<p>Allows the input of text, or upload of a file, in multiple formats
	that are then transformed as necessary for display.
	For example, allows you to type some content, choose formatting and/or upload a file.
	If available, the visual editor set in personal preferences is used for editing
	and formatting.</p>
	<blockquote>
	<p><img width="376" height="245" alt="richwidget.png" src="richwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>rows</td>
	<td>integer</td>
	<td>5</td>
	<td>Number of rows. (Since the visual mode of the RichWidget is controlled by JavaScript,
	this is not very useful.)</td>
	</tr><tr class="even"><td>cols</td>
	<td>integer</td>
	<td>40</td>
	<td>Number of columns. (Since the visual mode of the RichWidget is controlled by JavaScript,
	this is not very useful.)</td>
	</tr><tr class="odd"><td>allow_file_upload</td>
	<td>boolean</td>
	<td>True</td>
	<td>If True, a file upload option is included with the field.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="SelectionWidget">SelectionWidget</h3>
	<p>Renders an HTML selection widget, which can be represented as a dropdown, or as a group of radio buttons.</p>
	<blockquote>
	<p><img width="201" height="56" alt="selectionwidget-dropdown.png" src="selectionwidget-dropdown.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<blockquote>
	<p><img width="383" height="150" alt="selectionwidget-radio.png" src="selectionwidget-radio.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>format</td>
	<td>string</td>
	<td>'flex'</td>
	<td>Possible
	values: 'flex', 'select', 'radio'. Uses radio buttons when set to radio, and
	a single-selection list when set to select. Using flex will
	automatically use single-selection lists for more than three settings
	at a time, and a single-select list for up to three settings.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="StringWidget">StringWidget</h3>
	<p>Renders an HTML text input box which accepts a single line of text. For simple text lines such as author.</p>
	<blockquote>
	<p><img width="233" height="58" alt="stringwidget.png" src="stringwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<strong>Special Properties</strong>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>maxlength</td>
	<td>integer</td>
	<td>255</td>
	<td>Maximum input length in characters; sets the HTML input tag's maxlength attribute.</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>30</td>
	<td>Size of the input widget; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="TextAreaWidget">TextAreaWidget</h3>
	<p>Renders an HTML text area for typing a few lines of text. Also provides for the entry of
	the content in multiple formats when <em>allowed_content_types</em> in the enclosing TextField allows it.</p>
	<blockquote>
	<p><img width="367" height="118" alt="textareawidget.png" src="textareawidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>rows</td>
	<td>integer</td>
	<td>
	5</td>
	<td>Number of rows for the edit widget; sets the HTML textarea tag's rows attribute.</td>
	</tr><tr class="even"><td>cols</td>
	<td>integer</td>
	<td>
	40</td>
	<td>Column width of the edit widget; sets the HTML textarea tag's cols attribute.</td>
	</tr><tr class="odd"><td>append_only</td>
	<td>boolean</td>
	<td>
	False</td>
	<td>Set this attribute to True to make an append-only TextArea widget. New text gets
	added to the top of the existing text, dividing the new text from the
	existing text using the divider property. The existing text is shown
	below the TextArea, and is not editable. This currently works with
	TextArea widgets and using plain text format.</td>
	</tr><tr class="even"><td>divider</td>
	<td>string</td>
	<td>========================</td>
	<td>Divider text marker to use for append only text areas. Only used then the append_only property is True.</td>
	</tr><tr class="odd"><td>maxlength</td>
	<td>integer</td>
	<td>False</td>
	<td>
	If non-zero, sets a maximum input length in characters. Since the HTML textarea tag
	has no maxlength property, this is enforced via a JavaScript snippet. So, it is is
	not applicable when JavaScript is unavailable.</td>
	</tr></tbody></table><h2>Add-on Widgets</h2>
	<p>To find all available add-on widgets contributed by the community, <a href="../../../../search?path=%2Fplone.org%2Fproducts&amp;portal_type=PSCProject&amp;SearchableText=widget" class="external-link">follow this link</a>.</p><h3>Widget Attribute Topics<br></h3>
	<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>
	<p><a href="#common_attributes">Common Widget Attributes</a></p>
	<p><a href="#BooleanWidget">BooleanWidget</a></p>
	<p><a href="#CalendarWidget">CalendarWidget</a></p>
	<p><a href="#ComputedWidget">ComputedWidget</a></p>
	<p><a href="#DecimalWidget">DecimalWidget</a></p>
	<p><a href="#FileWidget">FileWidget</a></p>
	<p><a href="#ImageWidget">ImageWidget</a></p>
	</td>
	<td>
	<p><a href="#InAndOutWidget">InAndOutWidget</a></p>
	<p><a href="#IntegerWidget">IntegerWidget</a></p>
	<p><a href="#KeywordWidget">KeywordWidget</a></p>
	<p><a href="#LabelWidget">LabelWidget</a></p>
	<p><a href="#LinesWidget">LinesWidget</a></p>
	<p><a href="#MultiSelectionWidget">MultiSelectionWidget</a></p>
	<p><a href="#PasswordWidget">PasswordWidget</a></p>
	</td>
	<td>
	<p><a href="#PicklistWidget">PicklistWidget</a></p>
	<p><a href="#ReferenceWidget">ReferenceWidget</a></p>
	<p><a href="#ReferenceBrowserWidget">ReferenceBrowserWidget</a></p>
	<p><a href="#RichWidget">RichWidget</a></p>
	<p><a href="#SelectionWidget">SelectionWidget</a></p>
	<p><a href="#StringWidget">StringWidget</a></p>
	<p><a href="#TextAreaWidget">TextAreaWidget</a></p>
	</td>
	</tr></tbody></table><h2 id="common_attributes">Common Widget Attributes</h2>
	<p>The table below describes attributes common to nearly all widgets. Illustrations
	and special attributes listings for each of the standard widgets follows.</p>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Possible Values<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>condition <br></td>
	<td>A string containing a TALES expression to determine whether or not a field/widget is
	included on a view or edit page.
	This does not distinguish between view and edit mode.<br></td>
	<td>Your TALES expression may referenc the current context as 'object' and the Plone site root as 'portal'<br></td>
	</tr><tr class="even"><td>description <br></td>
	<td>Help or explanatory text for the field. Usually shown on the edit form under the label and above the input field.</td>
	<td><br></td>
	</tr><tr class="odd"><td>description_msgid</td>
	<td>The i18n identifier for the description message. Used to translate the message. Should be unique within your product's i18n domain.</td>
	<td>'help_type_field'</td>
	</tr><tr class="even"><td>label</td>
	<td>The label that will appear in the field.</td>
	<td> Any string, for example, <em>Start Date</em> for a field <em>start_date</em>. Also <em>label_msgid</em> (takes string message ids for i18n.)</td>
	</tr><tr class="odd"><td>label_msgid</td>
	<td>The i18n identifier for the label message. Should be unique within your product's i18n domain.</td>
	<td>'label_type_field'</td>
	</tr><tr class="even"><td>i18n_domain</td>
	<td>The i18n domain specifier for your product. This should be unique for your product, and will be used to find the translation catalogs for your product.</td>
	<td>'productname'</td>
	</tr><tr class="odd"><td> modes</td>
	<td> The modes that this widget will be shown in; by default there are two modes: view and edit.</td>
	<td> A list of modes as strings; by default <em>("view", "edit")</em>.</td>
	</tr><tr class="even"><td> populate</td>
	<td> If this is enabled, the view and edit fields will be populated. Usually this is enabled, but for fields such as a password field, this shouldn't
	be the case. Usually this is true by default.</td>
	<td> <em>True</em> or <em>False</em></td>
	</tr><tr class="odd"><td> postback</td>
	<td> If this is enabled, then when an error is raised, the field is
	repopulated; for fields such as a password field, this shouldn't be the
	case. Usually this is True by default.</td>
	<td> <em>True</em> or <em>False</em></td>
	</tr><tr class="even"><td> visible</td>
	<td> Determines whether or not the field is visible view and edit mode.
	This is a
	dictionary mapping the view mode to a string describing the
	visibility.
	Choices are <em>visible</em>, <em>hidden</em> (rendered in an HTML hidden form value), <em>invisible</em> (not rendered at all).</td>
	<td>For example, <em>{'view': 'visible', 'edit': 'hidden' }</em> means that the view will show, but the edit page will hide the value.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h2>Standard Widgets</h2>
	<p>&nbsp;</p>
	<h3 id="BooleanWidget">BooleanWidget</h3>
	<p>Renders an HTML checkbox, from which users can choose between two values such as on/off, true/false, yes/no.</p>
	<blockquote>
	<p><img width="369" height="39" alt="booleanwidget.png" src="booleanwidget.png">&nbsp;</p>
	</blockquote>
	<h3 id="CalendarWidget">CalendarWidget</h3>
	<p>Renders a HTML input box with a helper popup box for choosing dates.</p>
	<blockquote>
	<p><img width="375" height="216" alt="datetimewidget.png" src="datetimewidget.png"></p>
	</blockquote>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>format</td>
	<td>string</td>
	<td>
	<br></td>
	<td>Defines the date/time format using strftime, e.g. '%d.%m.%Y', for the view.
	(See the strftime section of the <a href="http://docs.python.org/lib/module-time.html">Python time documentation</a>.
	<br>
	If this is not specified, the long form of the portal's local time format is used.</td>
	</tr><tr class="even"><td>future_years</td>
	<td>integer</td>
	<td>
	5</td>
	<td>Specifies the number of future years offered by the year drop-down portion
	of the date widget. Do not use both future_year and end_year.
	(Plone 2.5+)</td>
	</tr><tr class="odd"><td>starting_year</td>
	<td>integer</td>
	<td>1999</td>
	<td>The first year offered by the year drop-down. (Plone 2.5+)</td>
	</tr><tr class="even"><td>ending_year</td>
	<td>integer</td>
	<td>
	None</td>
	<td>The final year offered by the year drop-down.
	Do not use both future_years and end_year. (Plone 2.5+)</td>
	</tr><tr class="odd"><td>show_hm</td>
	<td>boolean</td>
	<td>True</td>
	<td>Should the widget ask for a time as well as a date? (Plone 2.5+)</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="ComputedWidget">ComputedWidget</h3>
	<p>Generally used for ComputedField field type, it renders the computed value.
	Note that if your field has a vocabulary, and the field value is a key in that
	vocabulary, the widget will lookup the key in the vocabulary and show the result.</p>
	<h4>Standard Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>modes</td>
	<td>tuple</td>
	<td>
	('view', 'edit')</td>
	<td>As ComputedField is a read-only field, this property can be used to prevent
	the widget from appearing in edit templates, by setting it to just ('view',).</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="DecimalWidget">DecimalWidget</h3>
	<p>In edit mode, renders an HTML text input box which accepts a fixed point value.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>thousands_commas</td>
	<td>boolean</td>
	<td>False</td>
	<td>In view mode, formats the value to shows commas for thousands.
	For example, when thousands_commas is True, "7632654849635.02" is displayed as "7,632,654,849,635.02".
	(Note: this feature is not localized; it uses commas independent of locale.</td>
	</tr><tr class="even"><td>whole_dollars</td>
	<td>boolean</td>
	<td>
	False</td>
	<td>Shows whole dollars in view, leaving out the cents. Enter "1.123", and "$1" is shown.
	(Note: this feature is not localized; it uses the dollar sign independent of locale.)</td>
	</tr><tr class="odd"><td>maxlength</td>
	<td><br></td>
	<td>
	255</td>
	<td>Maximum input size; sets the HTML input tag's maxlength attribute.</td>
	</tr><tr class="even"><td>dollars_and_cents</td>
	<td>boolean</td>
	<td>False</td>
	<td>In view mode, shows dollars and cents. Enter "123.123" and "$123.12" is shown.
	(Note: this feature is not localized; it always uses the dollar sign, period,
	and two digits precision.)</td>
	</tr><tr class="odd"><td>size</td>
	<td><br></td>
	<td>5</td>
	<td>Size of the input field; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="FileWidget">FileWidget</h3>
	<p>Renders an HTML widget so a user can upload a file.</p>
	<blockquote>
	<p><img width="263" height="137" alt="filewidget.png" src="filewidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h3 id="ImageWidget">ImageWidget</h3>
	<p>Renders an HTML widget that can be used to upload, display, delete, and
	replace images. You can provide a <em>display_threshold</em> that allows
	you to set the size of an image; if it's below this
	size, the image will display in the Web page.</p>
	<blockquote>
	<p><img width="265" height="269" alt="imagewidget.png" src="imagewidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>display_threshold</td>
	<td>integer</td>
	<td>102400</td>
	<td>Only display the image inline if img.getSize() &lt;= display_threshold</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="InAndOutWidget">InAndOutWidget</h3>
	<p>In edit mode, renders a widget for moving items from one list to another.
	Items are removed from the source list.
	This can be used to choose multiple values from a list. This provides a good
	alternative to the MultiSelectionWidget when the vocabulary is too long for checkboxes.</p>
	<blockquote>
	<p><img width="376" height="149" alt="inandoutwidget.png" src="inandoutwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<p>&nbsp;</p>
	<h3 id="IntegerWidget">IntegerWidget</h3>
	<p>A simple HTML input box for a string.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>size</td>
	<td><br></td>
	<td>
	6</td>
	<td>Size of the select widget; sets the HTML select tag's size attribute.</td>
	</tr></tbody></table><table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>maxlength</td>
	<td><br></td>
	<td>
	255</td>
	<td>Maximum input size; sets the HTML input tag's maxlength attribute</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>5</td>
	<td>Size of the input field; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="KeywordWidget">KeywordWidget</h3>
	<p>
	This widget allows the user to select keywords or categories from a list. It is
	used for the <em>Categories</em> field in the Categorization Schema (Plone 3+)
	or the equivalent <em>Keywords</em> field on the Properties Tab (Plone &lt; 3)
	of a content object.<br>
	Keywords are drawn from the field vocabulary and/or the unique values for the
	field in a specified catalog.<br>
	Additional keywords may be added unless the enforceVocabulary property of the
	field is True.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>vocab_source</td>
	<td><br></td>
	<td>
	portal_catalog</td>
	<td>Sets
	the catalog to search for additional vocabulary to be combined with the
	vocabulary defined for the field. Additional keywords from existing content are
	found using catalog.uniqueValuesFor(fieldName).</td>
	</tr><tr class="even"><td>roleBasedAdd</td>
	<td><br></td>
	<td>True</td>
	<td>Only
	shows the "New keywords" input for adding keywords if the current user
	has one of the roles stored in the allowRolesToAddKeywords property in
	the site_properties property sheet in portal_properties</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="LabelWidget">LabelWidget</h3>
	<p>Used to display labels on forms -- without values or form input elements.</p>
	<p>&nbsp;</p>
	<h3 id="LinesWidget">LinesWidget</h3>
	<p>Displays a text area so that users can enter a list of values, one per line.</p>
	<blockquote>
	<p><img width="367" height="113" alt="lineswidget.png" src="lineswidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>rows</td>
	<td>integer</td>
	<td>
	5</td>
	<td>Rows of the lines widget; sets the HTML textarea tag's rows attribute.</td>
	</tr><tr class="even"><td>cols</td>
	<td>integer</td>
	<td>
	40</td>
	<td>Columns of the lines widget; sets the HTML textarea tag's cols attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="MultiSelectionWidget">MultiSelectionWidget</h3>
	<p>A selection widget; by default it's an
	HTML select widget which can be used to choose multiple values. As a
	checkbox users can choose one or more values from a list (useful if the
	list is short).</p>
	<blockquote>
	<p><img width="330" height="122" alt="multiselectionwidget-listbox.png" src="multiselectionwidget-listbox.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<blockquote>
	<p><img width="374" height="177" alt="multiselectionwidget-checkbox.png" src="multiselectionwidget-checkbox.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>format</td>
	<td>string</td>
	<td>select</td>
	<td>Possible values: 'select' or 'checkbox'. Uses a either a series of checkboxes or
	a multi-selection list. Note that checkboxes have much better usability for short
	vocabularies. Consider using the InAndOutWidget for longer vocabularies.</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>
	5</td>
	<td>Defines the size of the multi-select list. Does not apply for checkboxes.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="PasswordWidget">PasswordWidget</h3>
	<p>Renders an HTML password input.</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>maxlength</td>
	<td><br></td>
	<td>
	255</td>
	<td>Maximum input size; sets the HTML input tag's maxlength attribute.</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>20</td>
	<td>Size of the input field; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><h4>Standard Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>populate</td>
	<td>boolean</td>
	<td>False</td>
	</tr><tr class="even"><td>postback</td>
	<td>boolean</td>
	<td>False</td>
	</tr><tr class="odd"><td>modes</td>
	<td><br></td>
	<td>('edit',)</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="PicklistWidget">PicklistWidget</h3>
	<p>Similar to the InAndOutWidget, but the values stay in the source list after
	selection.</p>
	<blockquote>
	<p><img width="368" height="155" alt="picklistwidget.png" src="picklistwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>size</td>
	<td>integer</td>
	<td>6</td>
	<td>Size of the selection box; sets the HTML select tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="ReferenceWidget">ReferenceWidget</h3>
	<p>Renders an HTML text input box which accepts a list of possible reference
	 values. Used in combination with the Reference Field.<br><strong>Note:</strong> In Plone 2.5 and above, the ReferenceBrowserWidget is
	 a usually a better choice for a reference widget due to its ability to browse for content
	 referenceable objects.</p>
	<blockquote>
	<p><img width="381" height="110" alt="referencewidget.png" src="referencewidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>checkbox_bound</td>
	<td><br></td>
	<td>5</td>
	<td>When the number of items exceeds this value, multi-selection lists are used. Otherwise, radio buttons or checkboxes are used.</td>
	</tr><tr class="even"><td>destination</td>
	<td><br></td>
	<td>None</td>
	<td>May be:
	<ul><li>".", context object;</li><li>None, any place where Field.allowed_types can be added;</li><li>string path;</li><li>name of method on instance (it can be a combination list);</li><li>a list, combining all item above;</li><li>a dict, where {portal_type:} destination is relative to portal root</li></ul></td>
	</tr><tr class="odd"><td>addable</td>
	<td><br></td>
	<td>False</td>
	<td>Create createObject link for every addable type</td>
	</tr><tr class="even"><td>destination_types</td>
	<td><br></td>
	<td>None</td>
	<td>Either
	a single type given as a string, or a list of types given as a string,
	defining what types we allow adding to. Only applies when addable is
	set on the widget.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="ReferenceBrowserWidget">ReferenceBrowserWidget</h3>
	<p>A sophisticated widget for browsing, adding and deleting references.<br>Standard in Plone 2.5+, available for earlier versions as an add-on product.<br>Import from&nbsp;<em>Products.ATReferenceBrowserWidget.ATReferenceBrowserWidget</em>&nbsp;in Plone 2.5 and 3. In Plone 4, this widget has been improved and now lives in<em>archetypes.referencebrowserwidget.ReferenceBrowserWidget</em>.<strong><strong></strong></strong></p>
	<blockquote>
	<p><img width="386" height="468" alt="" src="referencebrowserwidget.png"></p>
	</blockquote>
	<h4>Special Properties</h4>
	<table class="listing" style="text-align: left;"><thead><tr><th style="text-align: left; cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>size</td>
	<td>integer</td>
	<td><br></td>
	<td>Size of the field if not multiValued; sets the HTML input tag's size attribute.</td>
	</tr><tr class="even"><td>default_search_index</td>
	<td>string</td>
	<td>SearchableText</td>
	<td>when a user searches in the popup, this index is used by default</td>
	</tr><tr class="odd"><td>show_indexes</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, a drop-down list is shown in the popup to select the index used for searching. If set to False, default_search_index will be used.</td>
	</tr><tr class="even"><td>available_indexes</td>
	<td>dict</td>
	<td>{}</td>
	<td>Optional dictionary containing all the indexes that can be used for searching along with their friendly names. Format: {'catalogindex':'Friendly Name of Index', ... } The friendly names are shown in the widget.<br><strong>Caution:</strong>&nbsp;If you set show_indexes True, but do not use this property to specify indexes, then all the indexes will be shown.</td>
	</tr><tr class="odd"><td>allow_search</td>
	<td>boolean</td>
	<td>True</td>
	<td>If True, a search form is included in the popup.</td>
	</tr><tr class="even"><td>allow_browse</td>
	<td>True</td>
	<td>Allows the user to browse content to find referenceable content.</td>
	<td><br></td>
	</tr><tr class="odd"><td>startup_directory</td>
	<td>string</td>
	<td>''</td>
	<td>Directory shown when the popup opens. Optional. When empty, the current folder is used. See the ATReferenceBrowser readme.txt for advanced usage.</td>
	</tr><tr class="even"><td>base_query</td>
	<td>dict or name of method</td>
	<td><br></td>
	<td>Defines query terms that will apply to all searches, mainly useful to create specific restrictions when allow_browse=0. Can be either a dictonary with query parameters, or the name of a method or callable available in cotext that will return such a dictionary.</td>
	</tr><tr class="odd"><td>force_close_on_insert</td>
	<td>boolean</td>
	<td>False</td>
	<td>If true, closes the popup when the user choses insert. This overrides the default behavior in multiselect mode.</td>
	</tr><tr class="even"><td>search_catalog</td>
	<td>string</td>
	<td>'portal_catalog'</td>
	<td>Specifies the catalog used for searches</td>
	</tr><tr class="odd"><td>allow_sorting</td>
	<td>boolean</td>
	<td>False</td>
	<td>Allows changing the order of referenced objects (requires multiValued).</td>
	</tr><tr class="even"><td>show_review_state</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, popup will display the workflow state for objects.</td>
	</tr><tr class="odd"><td>show_path</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, display the relative path (relative to the portal object) of referenced objects.</td>
	</tr><tr class="even"><td>only_for_review_states</td>
	<td><br></td>
	<td>None</td>
	<td>If set, content items are only referenceable if their workflow state matches one of the specified states. If None there will be no filtering by workflow state.</td>
	</tr><tr class="odd"><td>image_portal_types</td>
	<td>sequence</td>
	<td>()</td>
	<td>Use to specify a list of image portal_types. Instances of these portal types are previewed within the popup widget</td>
	</tr><tr class="even"><td>image_method</td>
	<td>string</td>
	<td>None</td>
	<td>Specifies the name of a method that is added to the image URL to preview the image in a particular resolution (e.g. 'mini' for thumbnails).</td>
	</tr><tr class="odd"><td>history_length</td>
	<td>integer</td>
	<td>0</td>
	<td>If not zero, enables a history feature that show the paths of the last N visited folders.</td>
	</tr><tr class="even"><td>restrict_browsing_to_startup_directory</td>
	<td>boolean</td>
	<td>False</td>
	<td>If True, the user will not be able to browse above the starting directory.</td>
	</tr></tbody></table><p>The cited Plone 4 implementation of this widget includes the following additional properties:</p>
	<h4>Special Properties</h4>
	<table class="listing" style="text-align: left;"><thead><tr><th style="text-align: left; cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="text-align: left; cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>startup_directory_method</td>
	<td>string</td>
	<td>''<br></td>
	<td>The name of a method or variable that, if available at the instance, will be used to obtain the path of the startup directory. If present, 'startup_directory' will be ignored.</td>
	</tr><tr class="even"><td valign="top">show_results_without_query</td>
	<td valign="top">bool<br></td>
	<td valign="top">False<br></td>
	<td valign="top">Don't ignore empty queries, but display results.</td>
	</tr><tr class="odd"><td valign="top">hide_inaccessible</td>
	<td valign="top">bool<br></td>
	<td valign="top">False<br></td>
	<td valign="top">Don't show inaccessible objects (no permission) in view mode.</td>
	</tr><tr class="even"><td valign="top">popup_width</td>
	<td valign="top">integer<br></td>
	<td valign="top">500<br></td>
	<td valign="top">Width of popup window in pixels.</td>
	</tr><tr class="odd"><td valign="top">popup_height</td>
	<td valign="top">integer<br></td>
	<td valign="top">550<br></td>
	<td valign="top">Height of popup window in pixels</td>
	</tr><tr class="even"><td valign="top">popup_name</td>
	<td valign="top">string<br></td>
	<td valign="top">'popup'<br></td>
	<td valign="top">Name of template to be used for popup. To use another template you have to register a named adapter for this template.</td>
	</tr></tbody></table><p id="RichWidget">Example of registering a popup in ZCML:</p>
	<pre id="RichWidget">&lt;zope:adapter<br>    for="Products.Five.BrowserView"<br>    factory=".view.default_popup_template"<br>    name="popup"<br>    provides="zope.formlib.namedtemplate.INamedTemplate" /&gt;<br></pre>
	<h3 id="ReferenceBrowserWidget">RichWidget</h3>
	<p>Allows the input of text, or upload of a file, in multiple formats
	that are then transformed as necessary for display.
	For example, allows you to type some content, choose formatting and/or upload a file.
	If available, the visual editor set in personal preferences is used for editing
	and formatting.</p>
	<blockquote>
	<p><img width="376" height="245" alt="richwidget.png" src="richwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>rows</td>
	<td>integer</td>
	<td>5</td>
	<td>Number of rows. (Since the visual mode of the RichWidget is controlled by JavaScript,
	this is not very useful.)</td>
	</tr><tr class="even"><td>cols</td>
	<td>integer</td>
	<td>40</td>
	<td>Number of columns. (Since the visual mode of the RichWidget is controlled by JavaScript,
	this is not very useful.)</td>
	</tr><tr class="odd"><td>allow_file_upload</td>
	<td>boolean</td>
	<td>True</td>
	<td>If True, a file upload option is included with the field.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="SelectionWidget">SelectionWidget</h3>
	<p>Renders an HTML selection widget, which can be represented as a dropdown, or as a group of radio buttons.</p>
	<blockquote>
	<p><img width="201" height="56" alt="selectionwidget-dropdown.png" src="selectionwidget-dropdown.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<blockquote>
	<p><img width="383" height="150" alt="selectionwidget-radio.png" src="selectionwidget-radio.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>format</td>
	<td>string</td>
	<td>'flex'</td>
	<td>Possible
	values: 'flex', 'select', 'radio'. Uses radio buttons when set to radio, and
	a single-selection list when set to select. Using flex will
	automatically use single-selection lists for more than three settings
	at a time, and a single-select list for up to three settings.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="StringWidget">StringWidget</h3>
	<p>Renders an HTML text input box which accepts a single line of text. For simple text lines such as author.</p>
	<blockquote>
	<p><img width="233" height="58" alt="stringwidget.png" src="stringwidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<strong>Special Properties</strong>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>maxlength</td>
	<td>integer</td>
	<td>255</td>
	<td>Maximum input length in characters; sets the HTML input tag's maxlength attribute.</td>
	</tr><tr class="even"><td>size</td>
	<td><br></td>
	<td>30</td>
	<td>Size of the input widget; sets the HTML input tag's size attribute.</td>
	</tr></tbody></table><p>&nbsp;</p>
	<h3 id="TextAreaWidget">TextAreaWidget</h3>
	<p>Renders an HTML text area for typing a few lines of text. Also provides for the entry of
	the content in multiple formats when <em>allowed_content_types</em> in the enclosing TextField allows it.</p>
	<blockquote>
	<p><img width="367" height="118" alt="textareawidget.png" src="textareawidget.png"></p>
	</blockquote>
	<p>&nbsp;</p>
	<h4>Special Properties</h4>
	<table class="listing"><thead><tr><th style="cursor: pointer;">Name<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Type<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Default<span class="sortdirection">&emsp;</span></th>
	<th style="cursor: pointer;">Description<span class="sortdirection">&emsp;</span></th>
	</tr></thead><tbody><tr class="odd"><td>rows</td>
	<td>integer</td>
	<td>
	5</td>
	<td>Number of rows for the edit widget; sets the HTML textarea tag's rows attribute.</td>
	</tr><tr class="even"><td>cols</td>
	<td>integer</td>
	<td>
	40</td>
	<td>Column width of the edit widget; sets the HTML textarea tag's cols attribute.</td>
	</tr><tr class="odd"><td>append_only</td>
	<td>boolean</td>
	<td>
	False</td>
	<td>Set this attribute to True to make an append-only TextArea widget. New text gets
	added to the top of the existing text, dividing the new text from the
	existing text using the divider property. The existing text is shown
	below the TextArea, and is not editable. This currently works with
	TextArea widgets and using plain text format.</td>
	</tr><tr class="even"><td>divider</td>
	<td>string</td>
	<td>========================</td>
	<td>Divider text marker to use for append only text areas. Only used then the append_only property is True.</td>
	</tr><tr class="odd"><td>maxlength</td>
	<td>integer</td>
	<td>False</td>
	<td>
	If non-zero, sets a maximum input length in characters. Since the HTML textarea tag
	has no maxlength property, this is enforced via a JavaScript snippet. So, it is is
	not applicable when JavaScript is unavailable.</td>
	</tr></tbody></table><h2>Add-on Widgets</h2>
	<p>To find all available add-on widgets contributed by the community, <a href="../../../../search?path=%2Fplone.org%2Fproducts&amp;portal_type=PSCProject&amp;SearchableText=widget" class="external-link">follow this link</a>.</p>
