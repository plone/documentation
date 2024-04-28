# Page Templates in Plone Classic UI

These instructions and resources will help you develop classic-ui pages.

When you visit the Plone backend with a web browser, you will reach the classic-ui.  These pages are generated with classic Plone browser views and page templates.

This chapter covers developing page templates.   Browser views are documented in-depth in [views](../views.md)


## Contents

* Page Templates
   * Introduction
   * Overriding existing templates
     * z3c.jbot
     * overriding with zcml
     * layering with zcml
     * editing browser views 
   * Creating your own templates
     * stand-alone templates
     * browser view templates
   * Advanced Concepts
     *  calling templates in python
* Language Reference
   * Template Expression Language (TAL)
   * Expressions (TALES)
       * Python expressions
       * Path Expressions
   * Macros (METAL)
   * ${..} Operator
   * 

* Skin Layers
* [DTML](dtml.md)


## Page Templates
### Introduction

Plone Classic uses Zope Page Templates (ZPT or just PT).  These templates use well established and time-tested standards:   The *Template Attribute Language* (TAL),  *TAL Expression Syntax* (TALES), *Macro Expansion TAL* (METAL).

From a python programmer's point of view, page templates are a tool to display a python object on the web, instead of simply what that object's `__repr__()` method would return. These template files always have a `.pt` file extension

A normal full Plone HTML page consists of:
* the *master template* defining the overall layout of the page
* METAL *slots* defined by the master template, and filled by the object being published.
* *viewlets* and *viewlet managers*
* *tiles*

Page templates are most frequently describing an HTML document, but they can also render XML (useful for RSS feeds or XML-based API's).

Templates can actually render any mime type you find useful: markdown `.md` files, or latex, or `text/plain`

You could, if you wanted, create a page template that rendered `application/json` but there are better ways to do that directly from a browser view.  

The point here is that you are not limited to templates creating only HTML.


### Overriding Existing Templates

Your first journey in page templates will likely be overriding a Plone backend core template or a template from an add-on.  The recommended approach is to use [z3c.jbot](https://pypi.org/project/z3c.jbot/) and to put your customized templates onto the filesystem and version controlled.


#### z3c.jbot


`z3c.jbot` (https://pypi.org/project/z3c.jbot/ ) can override page templates (``.pt`` files) for views, viewlets, old style page templates and portlets. In fact, it can override any ``.pt`` file in the Plone source tree.

To override a particular file, first determine its canonical filename. It’s defined as the path relative to the package within which the file is located; directory separators are replaced with dots.

As a simple example, to edit the default search page in Plone Classic we first find the existing template. In a fresh plone install, it's in the Products.CMFPlone  `/Products/CMFPlone/browser/templates/search.pt`  so our override file will be called `Products.CMFPlone.browser.templates.search.pt`

Create a new directory inside your local plone install for template overrides and copy the system `search.pt` into that directory, and rename it to  `Products.CMFPlone.browser.templates.search.pt`

```
├─ PloneSite
│  ├─ bin
│  ├─ eggs
│  │   └─Products.CMFPlone-version
│  │     └Products
│  │      └CMFPlone
│  │       └browser
│  │         └templates
│  │           └search.pt  <--- override this 
│  ├─ parts
│  └─ mysite
      ├─ configure.zcml
      └─ template-overrides 
         └─ Products.CMFPlone.browser.templates.search.pt <--- with this
```

In your configure.zcml, register the `template-overrides` directory with jbot

```xml+genshi
<include package="z3c.jbot" file="meta.zcml" />

<browser:jbot
    directory="template-overrides"
    />
```

Now, edit your `Products.CMFPlone.browser.templates.search.pt` and see your changes on the plone search page.

```{note}
   The `<browser:jbot>` zcml should also contain a `layer` attribute for best practice.  see the z3c.jbot documentation and browser layers documentation
```

#### overriding with zcml

Although not best practice, you can also quickly override templates by creating an `override.zcml` and adding your custom registration.  For the search page, this would be finding the ZCML entry for the search view in `Products/CMFPlone/browser/configure.zcml` and copying it into your own `overrides.zcml`, but change the `template=` attribute to point to your custom template.  The `class` also must change to become an absolute path to the original class path

overrides.zcml
```xml+genshi
 <browser:page
      name="search"
      class="Products.CMFPlone.browser.search.Search"
      permission="zope2.View"
      for="plone.app.layout.navigation.interfaces.INavigationRoot"
      template="template-overrides/search.pt"
      />
```

#### layering with zcml

A better and much more flexable way to override templates, especially when developing add-ons, is to use a browser layer in your configure.zcml.  This is *highly* preferred to using an overrides.zcml file, but involves using a BrowserLayer Interface.  This is extremely easy and is best practice.

configure.zcml
```xml+genshi
 <browser:page
      name="search"
      class="Products.CMFPlone.browser.search.Search"
      permission="zope2.View"
      for="plone.app.layout.navigation.interfaces.INavigationRoot"
      template="template-overrides/search.pt"
      layer="my.addon.interfaces.IMyAddonLayer"
      />
```

#### editing browser views

Sometimes, when you look up a browser view's ZCML it does not have a `template` attribute.  In this case, the template is frequently hard-coded into the python browser view.  One example of this is in the control panel pages, where the templates are not added to `configure.zcml`  

`@@actions-controlpanel` is found in `Products/CMFPlone/controlpanel/browser/actions.py`  

```python
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ActionListControlPanel(BrowserView):
    """Control panel for the portal actions."""

    template = ViewPageTemplateFile("actions.pt")
```

These are harder to override.  Best practice is to copy the python file (`actions.py` in this case) to your customizations folder and override the entire browser:page like above, pointing to your own `actions.py` and modifying that python code to find your new template `.pt` file


### Creating your own Templates

If you create your own dexterity object, you probably want to display it on a web browser.  Without a template, a default view will come up using plone's built-in main template and default view for a content type.


#### stand-alone templates

```{warning}
Although templates can be 'stand alone' templates that render a Plone object directly, this is not best practice. A combination of a View and Page Template is the correct implementation.
```

The simplest possible template is an html document:

template.pt
```html
<html>
<body>
<h1> hello custom template </h1>
</body>
</html>
```

and registering it in ZCML: 

```xml+genshi
   <browser:page
        for="*"
        name="custom_template"
        permission="zope.Public"
        template="template.pt"
    />
```

if you now go to any content item on your plone site, including the site itself, and add `custom_template` to the end of the url, the above html will display.

This isn't very useful, but does show how Plone basically works.

#### browser view templates


### Advanced Concepts

#### calling templates in python

#### passing data to templates

### Language Reference
## Chameleon

Chameleon is an HTML/XML template engine for Python.

It’s designed to generate the document output of a web application, typically HTML markup or XML.

```{seealso}
[Chameleon documentation](https://chameleon.readthedocs.io/en/latest/)
```

The language used is *page templates*, originally a Zope invention[^1].

The template engine compiles templates into Python byte-code and is optimized for speed. For a complex template language, the performance is very good.

The *page templates* language is used within your document structure as special element attributes and text markup. Using a set of simple language constructs, you control the document flow, element repetition, text replacement and translation.

The basic language (known as the *template attribute language* or TAL)
is simple enough to grasp from an example:

```xml+genshi
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

The ``${...}`` notation is shorthand for text insertion. The
Python-expression inside the braces is evaluated and the result
included in the output. By default, the string is escaped before
insertion. To avoid this, use the ``structure:`` prefix:

```xml+genshi
  <div>${structure: ...}</div>
```

Note that if the expression result is an object that implements an
``__html__()`` method [4]_, this method will be called and the result
treated as "structure". An example of such an object is the
``Markup`` class that's included as a utility

```python
  from chameleon.utils import Markup
  username = Markup("<tt>%s</tt>" % username)
```

The macro language (known as the *macro expansion language* or METAL)
provides a means of filling in portions of a generic template.

On the left, the macro template; on the right, a template that loads
and uses the macro, filling in the "content" slot:

```xml+genshi

  <html xmlns="http://www.w3.org/1999/xhtml">             <metal:main use-macro="load: main.pt">
    <head>                                                   <p metal:fill-slot="content">${structure: document.body}<p/>
      <title>Example &mdash; ${document.title}</title>    </metal:main>
    </head>
    <body>
      <h1>${document.title}</h1>

      <div id="content">
        <metal:content define-slot="content" />
      </div>
    </body>
  </html>
```

In the example, the expression type [load](load reference) is
used to retrieve a template from the file system using a path relative
to the calling template.

The METAL system works with TAL such that you can for instance fill in
a slot that appears in a ``tal:repeat`` loop, or refer to variables
defined using ``tal:define``.

The third language subset is the translation system (known as the
*internationalization language* or I18N):

```xml+genshi

  <html i18n:domain="example">

    ...

    <div i18n:translate="">
       You have <span i18n:name="amount">${round(amount, 2)}</span> dollars in your account.
    </div>

    ...

  </html>
```

Each translation message is marked up using ``i18n:translate`` and
values can be mapped using ``i18n:name``. Attributes are marked for
translation using ``i18n:attributes``. The template engine generates
`gettext <http://www.gnu.org/s/gettext/>` translation strings from
the markup::

  "You have ${amount} dollars in your account."

If you use a web framework such as `Pyramid <https://trypyramid.com/>`, the
translation system is set up automatically and will negotiate on a *target
language* based on the HTTP request or other parameter. If not, then
you need to configure this manually.


[^1]: The template language specifications and API for the Page Templates engine are based on Zope Page Templates (see in particular zope.pagetemplate). However, the Chameleon compiler and Page Templates engine is an entirely new codebase, packaged as a standalone distribution. It does not require a Zope software environment.
