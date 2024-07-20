---
myst:
  html_meta:
    "description": "Standard and common third party widgets for content types in Plone"
    "property=og:description": "Standard and common third party widgets for content types in Plone"
    "property=og:title": "Standard and common third party widgets for content types in Plone"
    "keywords": "Plone, standard, common, third party widgets, content types"
---

# Widgets

This chapter describes the standard and common third party widgets for content types in Plone.

Most of the time, you will use the standard widgets provided by `z3c.form`.
To learn more about `z3c.form` widgets, see the [z3c.form documentation](https://z3cform.readthedocs.io/en/latest/widgets/index.html).
To learn about setting custom widgets for Dexterity content types, see the {ref}`schema introduction <the-schema-label>`.

The table below shows some commonly used custom widgets.

| Widget | Imported from | Field | Description |
| ---------------------------- | ----------------------------- | ------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------- |
| WysiwygFieldWidget | plone.app.z3cform.wysiwyg | Text | Use Plone's standard WYSIWYG HTML editor on a standard text field. Note that if you used a `RichText` field, you will get the WYSIWYG editor automatically. |
| RichTextWidget | plone.app.textfield.widget | RichText | Use Plone's standard WYSIWYG HTML editor on a `RichText` field. This also allows text-based markup such as reStructuredText. |
| AutocompleteFieldWidget | plone.formwidget.autocomplete | Choice | Autocomplete widget based on jQuery Autocomplete. Requires a Choice field with a query source. See {doc}`../advanced/vocabularies`. |
| AutocompleteMultiFieldWidget | plone.formwidget.autocomplete | Collection | Multi-select version of the above. Used for a List, Tuple, Set, or Frozenset with a Choice `value_type`. |
| ContentTreeFieldWidget | plone.formwidget.contenttree | RelationChoice | Content browser. Requires a query source with content objects as values. |
| MultiContentTreeFieldWidget | plone.formwidget.contenttree | RelationList | Content browser. Requires a query source with content objects as values. |
| NamedFileFieldWidget | plone.formwidget.namedfile | NamedFile/NamedBlobFile | A file upload widget |
| NamedImageFieldWidget | plone.formwidget.namedfile | NamedImage/NamedBlobImage | An image upload widget |
| TextLinesFieldWidget | plone.z3cform.textlines | Collection | One-per-line list entry for List, Tuple, Set, or Frozenset fields. Requires a `value_type` of TextLine or ASCIILine. |
| SingleCheckBoxFieldWidget | z3c.form.browser.checkbox | Bool | A single checkbox for `True` or `False`. |
| CheckBoxFieldWidget | z3c.form.browser.checkbox | Collection | A set of checkboxes. Used for Set or Frozenset fields with a Choice `value_type` and a vocabulary. |
