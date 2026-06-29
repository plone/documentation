---
myst:
  html_meta:
    "description": "Page Templates in Plone Classic UI using TAL, TALES, and METAL"
    "property=og:description": "Page Templates in Plone Classic UI using TAL, TALES, and METAL"
    "property=og:title": "Templates"
    "keywords": "Plone, Classic UI, templates, TAL, TALES, METAL, Chameleon, page templates"
---

(classic-ui-templates-label)=

# Templates

Page Templates are the primary way to generate HTML output in Plone Classic UI.
They are HTML files enhanced with special attributes written in TAL (Template Attribute Language), TALES (TAL Expression Syntax), and METAL (Macro Expansion for TAL).

Plone uses [Chameleon](https://chameleon.readthedocs.io/) as its template engine, integrated through the Zope framework.
Chameleon is a fast HTML/XML template engine that implements the ZPT (Zope Page Templates) specification with additional features.


(templates-basics-label)=

## Template basics

A Page Template is a valid HTML or XML file with special `tal:`, `metal:`, and `i18n:` attributes that control how the template is rendered.

Here is a minimal example:

```html
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      i18n:domain="my.package"
      metal:use-macro="context/main_template/macros/master">
<body>

<metal:content-core fill-slot="content-core">
  <h2>Hello, World!</h2>
  <p tal:content="context/title">Placeholder title</p>
</metal:content-core>

</body>
</html>
```

The three parts serve different purposes:

TAL (Template Attribute Language)
:   Controls the structure and content of the output.
    TAL attributes like `tal:content`, `tal:repeat`, and `tal:condition` modify how elements are rendered.

TALES (TAL Expression Syntax)
:   Defines the syntax for expressions used in TAL attributes.
    TALES supports path expressions, Python expressions, string expressions, and more.

METAL (Macro Expansion for TAL)
:   Enables template reuse through macros and slots.
    Use METAL to inherit from base templates and define reusable template fragments.


(templates-filesystem-vs-ttw-label)=

## Filesystem vs. TTW templates

Templates in Plone can be stored in two locations, with important security implications:

**Filesystem templates** (recommended)
:   Templates stored in your add-on package's directory structure, typically in `browser/templates/` or `views`.
    These templates run as **trusted code** with full Python capabilities, just like any other code in your package.
    They have no security restrictions on Python expressions.

**TTW (Through-The-Web) templates**
:   Templates created and stored in the ZODB through the Zope Management Interface (ZMI).
    These templates run with **RestrictedPython** sandboxing for security.
    They have limited Python functionality: no `import` statements, restricted builtins, and security-checked attribute access.

```{note}
Always develop templates on the filesystem in your add-on package.
TTW templates are discouraged for production code because they are harder to maintain, version control, and test.
```


(templates-tal-label)=

## TAL statements

TAL uses special attributes to control template rendering.
When an element has multiple TAL attributes, they execute in this order:

1. `tal:define`
2. `tal:condition`
3. `tal:repeat`
4. `tal:content` or `tal:replace`
5. `tal:attributes`
6. `tal:omit-tag`


(templates-tal-define-label)=

### `tal:define`

Defines one or more variables for use in the template.

```html
<div tal:define="portal_url context/@@plone_portal_state/portal_url;
                 user context/@@plone_portal_state/member">
  <p>Portal URL: ${portal_url}</p>
  <p>User: ${user/getId}</p>
</div>
```

Use semicolons to define multiple variables.
Variables are available within the element and its children.

For global variables accessible throughout the template, use `tal:define="global varname expression"`.


(templates-tal-condition-label)=

### `tal:condition`

Conditionally includes or excludes an element and its children.

```html
<p tal:condition="context/description">
  ${context/description}
</p>

<p tal:condition="python:len(items) > 0">
  Found ${python:len(items)} items.
</p>

<!-- Use not: to negate -->
<p tal:condition="not:context/description">
  No description available.
</p>
```

If the condition evaluates to a false value, the entire element and all its children are removed from the output.


(templates-tal-repeat-label)=

### `tal:repeat`

Repeats an element for each item in a sequence.

```html
<ul>
  <li tal:repeat="item python:range(5)">
    Item ${item}
  </li>
</ul>

<table>
  <tr tal:repeat="brain context/@@folderListing">
    <td>${brain/Title}</td>
    <td>${brain/Description}</td>
  </tr>
</table>
```

Inside a repeat loop, you have access to the `repeat` variable which provides information about the current iteration:

| Variable | Description |
|----------|-------------|
| `repeat/item/index` | Zero-based index (0, 1, 2, ...) |
| `repeat/item/number` | One-based index (1, 2, 3, ...) |
| `repeat/item/even` | True for even indices |
| `repeat/item/odd` | True for odd indices |
| `repeat/item/start` | True for the first item |
| `repeat/item/end` | True for the last item |
| `repeat/item/length` | Total number of items |
| `repeat/item/letter` | Lowercase letter (a, b, c, ...) |
| `repeat/item/Letter` | Uppercase letter (A, B, C, ...) |

Example using repeat variables:

```html
<table>
  <tr tal:repeat="item items"
      tal:attributes="class python:'odd' if repeat['item'].odd else 'even'">
    <td>${repeat/item/number}</td>
    <td>${item/title}</td>
  </tr>
</table>
```


(templates-tal-content-label)=

### `tal:content`

Replaces the content of an element with the expression result.

```html
<h1 tal:content="context/title">Placeholder Title</h1>

<p tal:content="context/description">
  This placeholder text will be replaced.
</p>
```

By default, content is HTML-escaped.
To insert raw HTML, use the `structure` keyword:

```html
<div tal:content="structure context/text/output">
  Raw HTML will be inserted here.
</div>
```


(templates-tal-replace-label)=

### `tal:replace`

Replaces the entire element (not just its content) with the expression result.

```html
<span tal:replace="context/title">Placeholder</span>
<!-- Results in just the title text, no <span> tags -->

<span tal:replace="structure context/text/output" />
<!-- Inserts raw HTML without the <span> wrapper -->
```


(templates-tal-attributes-label)=

### `tal:attributes`

Sets or modifies HTML attributes dynamically.

```html
<a tal:attributes="href context/absolute_url;
                   title context/description">
  ${context/title}
</a>

<img tal:attributes="src string:${context/absolute_url}/@@images/image/preview;
                     alt context/title" />

<tr tal:attributes="class python:'selected' if item == current else None">
  ...
</tr>
```

Setting an attribute to `None` removes it from the output.


(templates-tal-omit-tag-label)=

### `tal:omit-tag`

Removes the element tag but keeps its content.

```html
<span tal:omit-tag="">
  This text appears without any wrapper.
</span>

<!-- Conditionally omit -->
<div tal:omit-tag="not:show_wrapper">
  Content here
</div>
```


(templates-tal-on-error-label)=

### `tal:on-error`

Provides error handling for template expressions.

```html
<div tal:on-error="string:An error occurred">
  <p tal:content="context/might_fail">
    This might raise an exception.
  </p>
</div>
```


(templates-tal-block-label)=

### Pure TAL blocks

When you need TAL logic without generating HTML elements, use the `tal:block` style elements:

```html
<tal:block define="items context/@@folderListing">
  <tal:block repeat="item items">
    <p>${item/Title}</p>
  </tal:block>
</tal:block>
```

You can use any tag name with the `tal:` prefix:

```html
<tal:items repeat="item items">
  <p>${item/Title}</p>
</tal:items>
```


(templates-tal-switch-label)=

### `tal:switch` and `tal:case` (Chameleon extension)

Chameleon provides switch/case statements as an extension to standard TAL:

```html
<div tal:switch="context/portal_type">
  <p tal:case="'Document'">This is a document.</p>
  <p tal:case="'News Item'">This is a news item.</p>
  <p tal:case="'Event'">This is an event.</p>
  <p tal:case="default">This is something else.</p>
</div>
```


(templates-tales-label)=

## TALES expressions

TALES (TAL Expression Syntax) defines how expressions are evaluated in templates.
Plone uses **path expressions** as the default expression type.


(templates-tales-path-label)=

### Path expressions

Path expressions traverse object attributes and items using `/` as a separator.

```html
<!-- Access attributes -->
<p tal:content="context/title">Title</p>

<!-- Chain traversals -->
<p tal:content="context/REQUEST/form/search_term">Search term</p>

<!-- Call methods (parentheses optional for no-argument methods) -->
<p tal:content="context/absolute_url">URL</p>

<!-- Access view methods -->
<p tal:content="view/get_items">Items from view</p>
```

The pipe operator `|` provides fallback values:

```html
<!-- Use id if title is empty/missing -->
<p tal:content="context/title | context/id">Fallback</p>

<!-- Use nothing (None) as fallback -->
<p tal:replace="context/optional_field | nothing">Optional</p>

<!-- Use a default string -->
<p tal:content="context/description | string:No description">Desc</p>
```

```{warning}
The `|` operator catches missing attributes and `None` values, but it also catches other errors.
Use it sparingly to avoid hiding bugs.
A typo like `context/ttle` (missing 'i') will silently use the fallback.
```


(templates-tales-python-label)=

### Python expressions

Python expressions allow full Python syntax.
They must be prefixed with `python:`.

```html
<p tal:content="python:context.title.upper()">TITLE</p>

<p tal:condition="python:len(items) > 10">
  Showing first 10 of ${python:len(items)} items.
</p>

<ul>
  <li tal:repeat="item python:sorted(items, key=lambda x: x.title)">
    ${item/title}
  </li>
</ul>

<!-- Complex expressions -->
<p tal:content="python:'{} ({})'.format(context.title, context.portal_type)">
  Title (Type)
</p>
```

In filesystem templates, you have full Python access.
In TTW templates, RestrictedPython limits what you can do.

```{important}
In Plone templates, the default expression type is `path:`, not `python:`.
You must explicitly use the `python:` prefix for Python expressions.
This differs from standalone Chameleon where Python is the default.
```


(templates-tales-string-label)=

### String expressions

String expressions create formatted strings with variable interpolation.

```html
<a tal:attributes="href string:${context/absolute_url}/edit">
  Edit
</a>

<p tal:content="string:Hello, ${user/fullname}!">
  Greeting
</p>

<img tal:attributes="src string:${portal_url}/++resource++my.package/logo.png" />
```

Inside `${...}` you can use any TALES expression, but the default is path.


(templates-tales-not-label)=

### The `not:` expression

Negates a boolean expression.

```html
<p tal:condition="not:context/description">
  No description available.
</p>

<div tal:condition="not:python:items">
  No items found.
</div>
```


(templates-tales-exists-label)=

### The `exists:` expression

Tests whether a path exists without evaluating it.

```html
<p tal:condition="exists:context/custom_field">
  Custom field exists: ${context/custom_field}
</p>
```


(templates-tales-nocall-label)=

### The `nocall:` expression

Returns an object without calling it.

```html
<!-- Get the method object itself, don't call it -->
<tal:block define="method nocall:context/some_method">
  Method: ${python:method.__name__}
</tal:block>
```


(templates-built-in-variables-label)=

## Built-in variables

Plone templates have access to several built-in variables:

| Variable | Description |
|----------|-------------|
| `context` | The content object the view is called on |
| `view` | The browser view instance |
| `request` | The current HTTP request object |
| `template` | The template object itself |
| `options` | Additional options passed to the template |
| `nothing` | Equivalent to Python's `None` |
| `default` | Special value to keep the original content |
| `repeat` | Dictionary of repeat variables in loops |
| `attrs` | Original attributes of the current element (in METAL) |

Additional variables available through helper views:

```html
<tal:block define="
    portal_state context/@@plone_portal_state;
    context_state context/@@plone_context_state;
    plone_view context/@@plone;
    portal_url portal_state/portal_url;
    portal portal_state/portal;
    user portal_state/member;
    is_anon portal_state/anonymous;
    current_url context_state/current_page_url;
">
  <p>Portal URL: ${portal_url}</p>
  <p>User: ${user/getId}</p>
  <p tal:condition="is_anon">Please log in.</p>
</tal:block>
```


(templates-metal-label)=

## METAL macros

METAL enables template reuse through macros and slots.


(templates-metal-define-macro-label)=

### Defining macros

Create a reusable template fragment:

```html
<!-- In macros.pt -->
<metal:macro define-macro="user-info">
  <div class="user-info">
    <span class="name">${user/fullname}</span>
    <span class="email">${user/email}</span>
  </div>
</metal:macro>
```


(templates-metal-use-macro-label)=

### Using macros

Include a macro in another template:

```html
<!-- Reference macro from another template -->
<div metal:use-macro="context/@@macros/user-info">
  Placeholder for user info
</div>

<!-- Reference macro from main_template -->
<html metal:use-macro="context/main_template/macros/master">
  ...
</html>
```


(templates-metal-slots-label)=

### Defining and filling slots

Slots allow customization of macro content:

```html
<!-- In the macro definition -->
<metal:macro define-macro="card">
  <div class="card">
    <div class="card-header">
      <metal:slot define-slot="header">Default Header</metal:slot>
    </div>
    <div class="card-body">
      <metal:slot define-slot="body">Default Body</metal:slot>
    </div>
  </div>
</metal:macro>

<!-- When using the macro -->
<div metal:use-macro="context/@@macros/card">
  <metal:fill fill-slot="header">
    <h3>Custom Header</h3>
  </metal:fill>
  <metal:fill fill-slot="body">
    <p>Custom body content here.</p>
  </metal:fill>
</div>
```


(templates-main-template-label)=

### The `main_template`

Plone's `main_template` provides the full page structure.
Most views fill slots in this template:

```html
<html xmlns="http://www.w3.org/1999/xhtml"
      metal:use-macro="context/main_template/macros/master"
      i18n:domain="my.package">
<body>

<metal:content-core fill-slot="content-core">
  <!-- Your content here -->
  <h2>My Custom Content</h2>
  <p tal:content="context/description">Description</p>
</metal:content-core>

</body>
</html>
```

Common slots in `main_template`:

| Slot | Description |
|------|-------------|
| `top_slot` | For setting request parameters (e.g., disabling columns) |
| `head_slot` | Additional content in the HTML `<head>` |
| `style_slot` | For additional CSS |
| `javascript_head_slot` | For additional JavaScript in head |
| `content` | The entire content area |
| `content-core` | The main content area (most commonly used) |
| `content-title` | The page title area |
| `content-description` | The description area |

Example disabling columns:

```html
<metal:block fill-slot="top_slot">
  <tal:block define="
      dummy python:request.set('disable_plone.leftcolumn', True);
      dummy python:request.set('disable_plone.rightcolumn', True);
  " />
</metal:block>
```


(templates-interpolation-label)=

## Expression interpolation

Chameleon supports `${...}` syntax for inline expression interpolation in text and attribute values.


(templates-interpolation-text-label)=

### Text interpolation

```html
<p>Welcome, ${user/fullname}!</p>

<p>The current time is ${python:datetime.now().strftime('%H:%M')}.</p>

<p>You have ${python:len(items)} items in your cart.</p>
```

```{important}
In Plone, `${...}` uses path expressions by default.
Use `${python:...}` for Python expressions.
```


(templates-interpolation-attributes-label)=

### Attribute interpolation

```html
<a href="${context/absolute_url}/edit">Edit</a>

<img src="${portal_url}/++resource++my.package/logo.png"
     alt="${context/title}" />

<div class="item ${python:'active' if item.active else 'inactive'}">
  ...
</div>
```


(templates-interpolation-structure-label)=

### Structure interpolation

To insert raw HTML without escaping:

```html
<div>${structure:context/text/output}</div>

<tal:block content="structure python:view.render_widget()" />
```


(templates-code-blocks-label)=

### Python code blocks

Chameleon allows inline Python code blocks (filesystem templates only):

```html
<div>
  <?python
  from datetime import datetime
  now = datetime.now()
  greeting = "Good morning" if now.hour < 12 else "Good afternoon"
  ?>
  <p>${greeting}, ${user/fullname}!</p>
</div>
```

```{warning}
Python code blocks work only in filesystem templates.
TTW templates may skip or restrict these blocks for security.
Use sparingly—complex logic belongs in the view class.
```


(templates-i18n-label)=

## Internationalization (i18n)

Templates support translation markup for internationalization.


(templates-i18n-domain-label)=

### Setting the translation domain

```html
<html i18n:domain="my.package">
  ...
</html>
```


(templates-i18n-translate-label)=

### Translating text

```html
<!-- Static text -->
<p i18n:translate="">Welcome to our site!</p>

<!-- With a message ID -->
<p i18n:translate="welcome_message">Welcome to our site!</p>

<!-- Element content as message -->
<label i18n:translate="">Username</label>
```


(templates-i18n-attributes-label)=

### Translating attributes

```html
<input type="submit"
       value="Submit"
       i18n:attributes="value" />

<img alt="Company Logo"
     title="Click to go home"
     i18n:attributes="alt; title" />
```


(templates-i18n-name-label)=

### Variable substitution in translations

```html
<p i18n:translate="">
  Welcome, <span i18n:name="username">${user/fullname}</span>!
</p>

<!-- Results in translation string: "Welcome, ${username}!" -->
```


(templates-best-practices-label)=

## Best practices


(templates-best-practices-logic-label)=

### Keep logic in Python

Templates should focus on presentation.
Move complex logic to view classes:

```python
# In your view class
class MyView(BrowserView):

    def get_formatted_items(self):
        items = self.context.get_items()
        return [
            {
                'title': item.title,
                'url': item.absolute_url(),
                'css_class': 'featured' if item.featured else 'normal',
            }
            for item in items
            if item.is_published()
        ]
```

```html
<!-- In your template -->
<ul>
  <li tal:repeat="item view/get_formatted_items"
      class="${item/css_class}">
    <a href="${item/url}">${item/title}</a>
  </li>
</ul>
```


(templates-best-practices-readable-label)=

### Write readable templates

Use meaningful variable names:

```html
<tal:block define="
    catalog context/portal_catalog;
    recent_news python:catalog(
        portal_type='News Item',
        sort_on='effective',
        sort_order='reverse',
        review_state='published',
    )[:5];
">
  <ul class="news-listing">
    <li tal:repeat="brain recent_news">
      <a href="${brain/getURL}">${brain/Title}</a>
    </li>
  </ul>
</tal:block>
```


(templates-best-practices-escape-label)=

### Always escape user content

Content is escaped by default.
Only use `structure` when you trust the content:

```html
<!-- Safe: content is escaped -->
<p tal:content="context/user_input">User input</p>

<!-- Only for trusted HTML content -->
<div tal:content="structure context/text/output">Rich text</div>
```


(templates-best-practices-fallbacks-label)=

### Provide fallbacks

Handle missing or empty values gracefully:

```html
<p tal:content="context/description | string:No description available">
  Description
</p>

<img tal:condition="exists:context/image"
     tal:attributes="src string:${context/absolute_url}/@@images/image/preview" />
```


(templates-debugging-label)=

## Debugging templates


(templates-debugging-variables-label)=

### Inspecting available variables

Use `context` to see all available variables:

```html
<dl tal:repeat="name python:sorted(context.keys())">
  <dt>${name}</dt>
  <dd>${python:repr(context[name])[:100]}</dd>
</dl>
```


(templates-debugging-pdb-label)=

### Using the debugger

In filesystem templates, you can use pdb:

```html
<?python
import pdb; pdb.set_trace()
?>
```


(templates-debugging-errors-label)=

### Common errors

**`KeyError` or `AttributeError`**
:   Check for typos in path expressions.
    Use `exists:` to test if a path exists.

**Unexpected output**
:   Remember that `tal:content` replaces content, `tal:replace` replaces the entire element.

**Expression not evaluated**
:   Ensure you're using the correct expression type prefix (`python:`, `string:`).

**Encoding errors**
:   Ensure your template files are saved as UTF-8.


(templates-reference-label)=

## Quick reference


(templates-reference-tal-label)=

### TAL statements

| Statement | Purpose | Example |
|-----------|---------|---------|
| `tal:define` | Define variables | `tal:define="title context/title"` |
| `tal:condition` | Conditional rendering | `tal:condition="context/description"` |
| `tal:repeat` | Loop over items | `tal:repeat="item items"` |
| `tal:content` | Replace element content | `tal:content="context/title"` |
| `tal:replace` | Replace entire element | `tal:replace="context/title"` |
| `tal:attributes` | Set HTML attributes | `tal:attributes="href context/absolute_url"` |
| `tal:omit-tag` | Remove element, keep content | `tal:omit-tag=""` |
| `tal:on-error` | Error handling | `tal:on-error="string:Error"` |


(templates-reference-tales-label)=

### TALES expression types

| Type | Prefix | Default in Plone | Example |
|------|--------|------------------|---------|
| Path | `path:` | Yes | `context/title` |
| Python | `python:` | No | `python:len(items)` |
| String | `string:` | No | `string:Hello ${name}` |
| Not | `not:` | No | `not:context/description` |
| Exists | `exists:` | No | `exists:context/image` |
| Nocall | `nocall:` | No | `nocall:context/method` |


(templates-reference-metal-label)=

### METAL statements

| Statement | Purpose | Example |
|-----------|---------|---------|
| `metal:define-macro` | Define reusable macro | `metal:define-macro="card"` |
| `metal:use-macro` | Use a macro | `metal:use-macro="context/@@macros/card"` |
| `metal:define-slot` | Define customizable slot | `metal:define-slot="content"` |
| `metal:fill-slot` | Fill a slot | `metal:fill-slot="content"` |


## See also

- {doc}`views`
- {doc}`viewlets`
- {doc}`template-global-variables`
- [Chameleon documentation](https://chameleon.readthedocs.io/)
- [Plone Training: Page Templates](https://training.plone.org/mastering-plone-5/zpt.html)
