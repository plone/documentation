---
myst:
  html_meta:
    "description": "Page templates in Plone Classic UI"
    "property=og:description": "Page templates in Plone Classic UI"
    "property=og:title": "Page templates in Plone Classic UI"
    "keywords": "Plone 6, Classic UI, page, templates, Twitter Bootstrap 5"
---

(classic-ui-page-templates-index-label)=

# Page templates

This chapter provides an tutorial of page templates in Classic UI.


## Background

When you visit the Plone backend with a web browser, you will view the Classic UI.
These pages are generated with classic Plone browser views and page templates.

Browser views are documented in depth in {doc}`views`.

Plone Classic UI uses {term}`Zope Page Template`s (ZPT).
These templates use well established and time-tested standards, {term}`Template Attribute Language` (TAL), {term}`Template Attribute Language Expression Syntax` (TALES), and {term}`Macro Expansion Template Attribute Language` (METAL).

From a Python programmer's point of view, page templates are a tool to display a Python object on the web, instead of what that object's `__repr__()` method would return.
These template files always have a file extension of `.pt`.

A normal full Plone HTML page consists of the following.

-   the _master template_ defining the overall layout of the page
-   METAL _slots_ defined by the master template, and filled by the object being published
-   _viewlets_ and _viewlet managers_
-   _tiles_

Page templates most frequently describe an HTML document.
They can also render XML, which is useful for RSS feeds or XML-based APIs.

Templates can render any media type you find useful, including Markdown, LaTeX, or plain text.
You could, if you wanted, create a page template that rendered a media type of `application/json`, but there are better ways to do that directly from a browser view.
The point here is that you are not limited to templates that only create HTML.


## Override existing templates

Your first journey in page templates could be to override a Plone backend core template or a template from an add-on.
The recommended approach is to use [`z3c.jbot`](https://pypi.org/project/z3c.jbot/), and to put your customized templates onto the filesystem and under a version control system.


### `z3c.jbot`

`z3c.jbot` can override page templates for views, viewlets, old style page templates and portlets.
In fact, it can override any `.pt` file in the Plone source tree.

To override a particular file, first determine its canonical filename.
It's defined as the path relative to the package within which the file is located.

```{tip}
See Customizing Existing Templates – Mastering Plone 5 development training, {ref}`training:plone5-zpt2-finding-label`.
```

```{todo}
@stevepiercy spun up a clean Plone site via buildout.
The paths that @flipcmf originally mentioned do not exist in the `eggs` directory.
@stevepiercy found the source `search.pt` file, but has no clue where to put it in the project file system.
The information in the next few paragraphs must be verified by someone who knows what they're doing.
```

As an example, to override the default search page in Plone Classic UI, first find the existing template.
In a fresh plone install, it's at {file}`src/Products.CMFPlone/Products/CMFPlone/browser/templates/search.pt`.
You will name the file by replacing the directory separators (`/`) with dots (`.`).
Thus the override file will be called `Products.CMFPlone.browser.templates.search.pt`.

Create a new directory inside your local Plone install for template overrides `mysite/template-overrides`.
Copy the Plone `search.pt` into that directory, and rename it to `Products.CMFPlone.browser.templates.search.pt`

```text
├─ myproject
│  ├─ src
│  │  └─ Products.CMFPlone
│  │     └─ Products
│  │        └─ CMFPlone
│  │           └─ browser
│  │              └─ templates
│  │                 └─ search.pt  ← override this 
│  └─ mysite
│     ├─ configure.zcml
│     └─ template-overrides 
│        └─ Products.CMFPlone.browser.templates.search.pt  ← with this
```

In your {file}`configure.zcml`, register the `template-overrides` directory with `z3c.jbot`.

```xml
<include package="z3c.jbot" file="meta.zcml" />

<browser:jbot
    directory="template-overrides"
    />
```

Now edit `Products.CMFPlone.browser.templates.search.pt`, and see your changes on the Plone search page.


### Override with ZCML

Although not best practice, you can also override templates by creating an {file}`override.zcml` and add your custom registration.
For the search page, use the ZCML entry for the search view in `Products/CMFPlone/browser/configure.zcml` and copy it into your own {file}`overrides.zcml`, but change the `template` attribute to point to your custom template.
You must also change the `class` attribute to become an absolute dotted path to the original class path.

```xml
 <browser:page
      name="search"
      class="Products.CMFPlone.browser.search.Search"
      permission="zope2.View"
      for="plone.app.layout.navigation.interfaces.INavigationRoot"
      template="template-overrides/search.pt"
      />
```

### Layer with ZCML

A better and much more flexible way to override templates, especially when developing add-ons, is to use a browser layer in your {file}`configure.zcml`.
This is _highly_ preferred to using an {file}`overrides.zcml` file, but involves using a `BrowserLayer` interface.

```xml
 <browser:page
      name="search"
      class="Products.CMFPlone.browser.search.Search"
      permission="zope2.View"
      for="plone.app.layout.navigation.interfaces.INavigationRoot"
      template="template-overrides/search.pt"
      layer="my.addon.interfaces.IMyAddonLayer"
      />
```


### Edit browser views

Sometimes when you look up a browser view's ZCML, it does not have a `template` attribute.
In this case, the template is frequently hard-coded into the Python browser view.
One example of this is in the control panel pages, where the templates are not added to {file}`configure.zcml`.
`@@actions-controlpanel` is found in `Products/CMFPlone/controlpanel/browser/actions.py`.

```python
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ActionListControlPanel(BrowserView):
    """Control panel for the portal actions."""

    template = ViewPageTemplateFile("actions.pt")
```

These are harder to override.
Best practice is to copy the Python file ({file}`actions.py` in this case) to your customizations folder, and override the entire `browser:page` as shown above, pointing to your own {file}`actions.py` and modifying that Python code to find your new template `.pt` file.


## Create your own templates

If you create your own content type object, you probably want to display it on a web browser.
Without a template, a default view will come up using Plone's built-in main template and default view for a content type.


### Stand-alone templates

```{warning}
Although templates can be stand alone templates that render a Plone object directly, this is not best practice.
A combination of a view and page template is the correct implementation.
```

The simplest possible template is an HTML document.

```html
<html>
<body>
<h1>hello custom template</h1>
</body>
</html>
```

Register it in ZCML. 

```xml
<browser:page
    for="*"
    name="custom_template"
    permission="zope.Public"
    template="template.pt"
    />
```

if you now go to any content item on your plone site, including the site itself, and add `custom_template` to the end of the url, the above html will display.

This isn't very useful, but does show how Plone basically works.

### Browser view templates

```{todo}
Todo
```


## Advanced Concepts

```{todo}
Todo
```


### Call templates in Python

```{todo}
Todo
```


### Pass data to templates

```{todo}
Todo
```


## Language reference

```{todo}
Todo
```


### Chameleon

[Chameleon](https://chameleon.readthedocs.io/en/latest/) is an HTML/XML template engine for Python.
It's designed to generate the document output of a web application, typically HTML markup or XML.

The language used is _page templates_, originally a Zope invention.

```{note}
The template language specifications and API for the page templates engine are based on Zope Page Templates (see in particular `zope.pagetemplate`).
However, the Chameleon compiler and page templates engine is an entirely new code base, packaged as a stand alone distribution.
It does not require a Zope software environment.
```

The template engine compiles templates into Python byte code, and is optimized for speed.
For a complex template language, the performance is very good.

The page templates language is used within your document structure as special element attributes and text markup.
Using a set of simple language constructs, you control the document flow, element repetition, text replacement, and translation.
The language is known as {term}`Template Attribute Language` or TAL.
The following snippet is a basic example.

```xml
<html>
  <body>
    <h1>Hello, ${'world'}!</h1>
    <table>
      <tr tal:repeat="row 'apple', 'banana', 'pineapple'">
        <td tal:repeat="col 'juice', 'muffin', 'pie'">
           ${row.capitalize()} ${col}
        </td>
      </tr>
    </table>
  </body>
</html>
```

The `${...}` notation is shorthand for text insertion.
The Python expression inside the braces is evaluated, and the result included in the output.
By default, the string is escaped before insertion.
To avoid this, use the `structure:` prefix:

```xml
<div>${structure: ...}</div>
```

Note that if the expression result is an object that implements an `__html__()` method, this method will be called and the result treated as "structure".
An example of such an object is the `Markup` class that's included as a utility.

```python
from chameleon.utils import Markup
username = Markup("<tt>%s</tt>" % username)
```

The macro language—known as the {term}`Macro Expansion Template Attribute Language` (METAL)—provides a means of filling in portions of a generic template.

The following two snippets work together.
First the macro template.

```xml
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
  <title>Example &mdash; ${document.title}</title>
</head>
<body>
  <h1>${document.title}</h1>
  <div id="content">
    <metal:content define-slot="content" />
  </div>
</body>
</html>
```

Next the template that loads and uses the macro, filling in the `content` slot.

```xml
<metal:main use-macro="load: main.pt">
  <p metal:fill-slot="content">${structure: document.body}<p/>
</metal:main>
```

In the example, the expression type `load` is used to retrieve a template from the file system using a path relative to the calling template.

The METAL system works with TAL such that you can, for instance, fill in a slot that appears in a `tal:repeat` loop, or refer to defined variables using `tal:define`.

The third language subset is the translation system, known as the internationalization language or {term}`i18n`.

```xml
<html i18n:domain="example">

  ...

  <div i18n:translate="">
   You have <span i18n:name="amount">${round(amount, 2)}</span> dollars in your account.
  </div>

...

</html>
```

Each translation message is marked up using `i18n:translate`, and values can be mapped using `i18n:name`.
Attributes are marked for translation using `i18n:attributes`.
The template engine generates `gettext <https://www.gnu.org/software/gettext/>` translation strings from the markup.

```text
  "You have ${amount} dollars in your account."
```

If you use a web framework, such as `Pyramid <https://trypyramid.com/>`, the translation system is set up automatically and will negotiate on a _target language_ based on the HTTP request or other parameter.
If not, then you need to configure this manually.
