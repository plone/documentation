---
myst:
  html_meta:
    "description": "TinyMCE customization in Plone 6"
    "property=og:description": "TinyMCE customization in Plone 6"
    "property=og:title": "TinyMCE customization in Plone 6"
    "keywords": "Plone 6, Classic UI, Bootstrap 5, TinyMCE, customization"
---

(classic-ui-tinymce-customization-label)=

# TinyMCE customization

This chapter is a developer reference manual for customizing {term}`TinyMCE`.


(tinymce-remove-formats-label)=

## Remove formats

In Plone 6, TinyMCE has a special logic that automatically reads registered files named {file}`tinymce-formats.css` and adds the CSS classes defined in those files to TinyMCE's {menuselection}`Format --> Formats` menu by using the [`importcss_file_filter` option](https://www.tiny.cloud/docs/tinymce/latest/importcss/#importcss_file_filter).

Plone 6 Classic UI ships with the Barceloneta theme which includes two custom formats,`highlight-inline` and `p.highlight-paragraph`, in the TinyMCE {menuselection}`Format --> Formats` menu.
You can remove these formats through the TinyMCE control panel.

1.  Navigate to {menuselection}`Site Setup --> TinyMCE --> Default`, or append `@@tinymce-controlpanel` to the root of your website in your browser's location bar.
1.  Scroll down to {guilabel}`Choose the CSS used in WYSIWYG Editor Area`.
1.  Remove the entry `++theme++barceloneta/tinymce/tinymce-formats.css`.
1.  Click the {guilabel}`Save` button.

Once removed, the custom formats will no longer appear in the menu.


## Add formats

To add custom formats, you can provide your own files.
The file must satisfy the following requirements.

1.  named {file}`tinymce-formats.css`
1.  registered as a resource in your Plone site
1.  included in the TinyMCE control panel in the textarea input {guilabel}`Choose the CSS used in WYSIWYG Editor Area`.
    See {ref}`tinymce-remove-formats-label`.

CSS styles defined in this file will automatically be added to the top level of TinyMCE's {menuselection}`Format --> Formats` menu.

Alternatively, you can customize TinyMCE by adding the styles through the [`formats` option in the JSON configuration](https://www.tiny.cloud/docs/tinymce/latest/content-formatting/).
