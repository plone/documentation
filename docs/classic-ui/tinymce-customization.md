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


## Customize {menuselection}`Format` menu

There are several options to customize TinyMCE's {menuselection}`Format --> Formats` menu.

The first two options use TinyMCE's [`formats` JSON configuration](https://www.tiny.cloud/docs/tinymce/latest/content-formatting/).
They are less complicated to implement than the third option.


### Add-on GenericSetup configuration file

This option is best for system administrators and developers who write their own add-ons to ease reproducibility.

You can add a GenericSetup configuration file to your add-on, such as {file}`profiles/default/registry/tinymce.xml`, with the JSON configuration of the custom format.

```xml
<registry>
  <records interface="plone.base.interfaces.controlpanel.ITinyMCESchema"
            prefix="plone">
    <value key="formats"
           purge="true"
        >{
        "myformat": {
            "block": "div",
            "classes": "my-css-classes"
        }
    }</value>
  </records>
</registry>
```

```{important}
The contents of the `formats` record will overwrite the default content in the controlpanel.
If you want to preserve the default content, you will have to copy it into your xml.
```

The next step is to define, where the new format should be placed inside the format menu subcategories.
To do that, you can add your custom format to one of these fields: `Header styles`, `Inline styles`, `Block styles`, `Alignment styles` or `Table styles`.
The value of each line in those field is `Title|format`.

Example XML snippet for `Inline styles`:

```xml
<record field="inline_styles"
        interface="plone.base.interfaces.controlpanel.ITinyMCESchema"
        name="plone.inline_styles">
  <value>
    <element>My custom format|myformat</element>
  </value>
</record>
```

```{note}
This example adds your custom format to the default values of `Inline styles` field.
The default values are not removed.
```


### Edit the `Formats` option in the TinyMCE control panel

This option is good for quick edits, but is not as reproducible as the GenericSetup option.

You can manually customize the `Formats` value through-the-web in the TinyMCE control panel.

1.  Navigate to {menuselection}`Site Setup --> TinyMCE --> Default`, or append `@@tinymce-controlpanel` to the root of your website in your browser's location bar.
1.  Scroll down to {guilabel}`Formats`, and edit the JSON configuration.
1.  Insert your custom format to one of the fields mentioned above.
1.  Click the {guilabel}`Save` button.



### Inject formats with files named {file}`tinymce-formats.css`

This option is more complex to implement than the previous options.

In Plone 6, TinyMCE has a special logic that automatically reads registered files named {file}`tinymce-formats.css` and adds the CSS classes defined in those files to TinyMCE's {menuselection}`Format --> Formats` menu by using the [`importcss_file_filter` option](https://www.tiny.cloud/docs/tinymce/latest/importcss/#importcss_file_filter).

To add custom formats, you can provide your own files.

1.  Name the file {file}`tinymce-formats.css`.
1.  Register the file as a resource in your Plone site.
1.  Include the file in the TinyMCE control panel in the textarea input {guilabel}`Choose the CSS used in WYSIWYG Editor Area`.
    1.  Navigate to {menuselection}`Site Setup --> TinyMCE --> Default`, or append `@@tinymce-controlpanel` to the root of your website in your browser's location bar.
    1.  Scroll down to {guilabel}`Choose the CSS used in WYSIWYG Editor Area`.

CSS styles defined in this file will automatically be added to the top level of TinyMCE's {menuselection}`Format --> Formats` menu.


## Remove imported formats

Similar to adding formats, you can remove formats in a couple of ways.


### Add-on GenericSetup configuration file

Alternatively, you can use GenericSetup in your add-on.

```xml
<record field="content_css"
          interface="plone.base.interfaces.controlpanel.ITinyMCESchema"
          name="plone.content_css"
  >
    <value purge="true">
      <element>++theme++barceloneta/tinymce/tinymce-ui-content.css</element>
    </value>
  </record>
```


### Configure the TinyMCE control panel

Plone 6 Classic UI ships with the Barceloneta theme which includes two custom formats, `highlight-inline` and `p.highlight-paragraph`, in the TinyMCE {menuselection}`Format --> Formats` menu.
You can remove these formats through the TinyMCE control panel.

1.  Navigate to {menuselection}`Site Setup --> TinyMCE --> Default`, or append `@@tinymce-controlpanel` to the root of your website in your browser's location bar.
1.  Scroll down to {guilabel}`Choose the CSS used in WYSIWYG Editor Area`.
1.  Remove the entry `++theme++barceloneta/tinymce/tinymce-formats.css`.
1.  Click the {guilabel}`Save` button.

Once removed, the custom formats will no longer appear in the menu.
