---
myst:
  html_meta:
    "description": "Render HTML pages in Plone using the Zope view pattern."
    "property=og:description": "Render HTML pages in Plone using the Zope view pattern."
    "property=og:title": "Views in Plone 6"
    "keywords": "views, browser view, templates, plonecli, acquisition, permissions, content, slots, Zope, Plone"
---

(classic-ui-views-label)=

# Views

Views are the basic elements of modern Python web frameworks.
A {term}`view` runs code to set up Python variables for a rendering template.
The output is not limited to HTML pages and snippets, but may contain {term}`JSON`, file download payloads, or other data formats.

Views are usually a combination of:

-   a Python class, which performs the user interface logic setup, and
-   corresponding {ref}`plone:classic-ui-templates-label`, or direct Python string output.

```{eval-rst}
.. graphviz::
    :align: center

    digraph viewstructure {
      {
        node [margin=5,shape=box]
      }
      ZCML -> {Python, Template};
    }
```

Templates should be kept simple.
Logic should be kept in a separate Python file.
This enhances readability and makes components more reusable.
You can override the Python logic, the template file, or both.

When you work with Plone, the most common view type is `BrowserView` from the package [`Products.Five`](https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/doc/manual.txt).
Other view types include `DefaultView` from [`plone.dexterity`](https://github.com/plone/plone.dexterity/blob/master/plone/dexterity/browser/view.py) and `CollectionView` from [`plone.app.contenttypes`](https://github.com/plone/plone.app.contenttypes/blob/master/plone/app/contenttypes/browser/collection.py).

Each `BrowserView` class is a Python callable.
The `BrowserView.__call__()` method acts as an entry point to executing the view code.
From Zope's point of view, even a function would be sufficient, as it is a callable.


(classic-ui-create-and-register-a-view-label)=

## Create and register a view

This section shows how to create and register a view in Plone.


(classic-ui-create-a-view-label)=

### Create a view

Create your add-on package using {term}`plonecli`:

```shell
plonecli create addon collective.awesomeaddon
```

Then change the working directory into the created package, and add a view:

```shell
cd collective.awesomeaddon
plonecli add view
```


(classic-ui-python-logic-code-label)=

#### Python logic code

Depending on how you answered the questions when invoking `plonecli`, it generated a Python file at the location `src/collective/awesomeaddon/views/my_view.py` with the following content.

```python
# from p6.docs import _
from Products.Five.browser import BrowserView
from zope.interface import Interface

# from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class IMyView(Interface):
    """Marker Interface for IMyView"""


class MyView(BrowserView):
    # If you want to define a template here, please remove the template attribute from
    # the configure.zcml registration of this view.
    # template = ViewPageTemplateFile('my_view.pt')

    def __call__(self):
        # your code here

        # render the template
        return self.index()
```

```{warning}
Do not attempt to run any code in the `__init__()` method of a view.
If this code fails and an exception is raised, the `zope.component` machinery remaps this to a "View not found" exception or traversal error.

Additionally, a view class may be instantiated in other places than where you intended to render the view.
For example, `plone.app.contentmenu` does this when creating the menu to select a view layout.
This will result in the `__init__()` being called on unexpected contexts, probably wasting a lot of time.

Instead, use a pattern where you have a `setup()` or similar method which `__call__()` or view users can explicitly call.
```


(classic-ui-register-a-view-label)=

#### Register a view

Zope 3 views are registered in {term}`ZCML`, an XML-based configuration language.
`plonecli` did the following registration in `src/collective/awesomeaddon/views/configure.zcml` for you.

The following example registers a new view.
See below for comments about what the code does.

```xml
<configure
      xmlns="http://namespaces.zope.org/zope"
      xmlns:browser="http://namespaces.zope.org/browser"
      >

    <browser:page
          for="*"
          name="myview"
          permission="zope2.Public"
          class=".views.MyView"
          />

  <browser:page
    name="my-view"
    for="*"
    class=".my_view.MyView"
    template="my_view.pt"
    permission="zope2.View"
    layer="collective.awesomeaddon.interfaces.ICollectiveAwesomeaddonLayer"
    />

</configure>
```

`for`
:   Specifies which content types receive this view.
    `for="*"` means that this view can be used for any content type.
    This is the same as registering views to the `zope.interface.Interface` base class.

`name`
:   The name by which the view is exposed to traversal and `getMultiAdapter()` look-ups.
    If your view's name is `myview`, then you can render it in the browser by calling `http://yourhost/site/page/@@myview`.

`permission`
:   This is the permission needed to access the view.
    When an HTTP request comes in, the currently authenticated user's access rights in the current context are checked against this permission.
    See {ref}`backend-security-permissions-label` for Plone's out-of-the-box permissions.
    Usually you want to use `zope2.View`, `cmf.ModifyPortalContent`, `cmf.ManagePortal`, or `zope2.Public` here.

`class`
:   This is a Python dotted name for a class based on `BrowserView`, which is responsible for managing the view.
    The class's `__call__()` method is the entry point for view processing and rendering.

```{note}
You need to declare the `browser` namespace in your `configure.zcml` to use `browser` configuration directives.
```

The view in question is registered against a {doc}`layer </classic-ui/layers>`.
It will be available after restart and running the {ref}`GenericSetup profile <backend-configuration-registry-generic-setup-label>`, or enabling the add-on.


(classic-ui-page-template-label)=

#### Page template

Depending on how you answered the questions when you invoked `plonecli`, it created a {doc}`template </classic-ui/templates>` at `src/collective/awesomeaddon/views/my_view.pt` with the following content.

```html
<html xmlns="http://www.w3.org/1999/xhtml"
      xmlns:metal="http://xml.zope.org/namespaces/metal"
      xmlns:tal="http://xml.zope.org/namespaces/tal"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      i18n:domain="p6.docs"
      metal:use-macro="context/main_template/macros/master">
<body>
  <metal:content-core fill-slot="content-core">
  <metal:block define-macro="content-core">

      <h2 i18n:translate="">Sample View</h2>
      <!--<div tal:replace="view/my_custom_view_method" />-->
      <!--<div tal:replace="context/my_custom_field" />-->

  </metal:block>
  </metal:content-core>
</body>
</html>
```

When you restart Plone, and activate your add-on, the view should be available through your browser.


(classic-ui-access-your-newly-created-view-label)=

#### Access your newly created view

Now you can access your view within the news folder by visiting the following URL.

```text
http://localhost:8080/Plone/news/my-view
```

Or on a site root:

```text
http://localhost:8080/Plone/my-view
```

Or on any other content item.

You can also use the `@@` notation at the front of the view name to make sure that you are looking up a *view*, and not a content item that happens to have the same ID as a view:

```text
http://localhost:8080/Plone/news/@@my-view
```


#### Add a view to a content type

A {doc}`content type </backend/content-types/index>` can have more than one view, which a user can choose from in the display menu.
In section {ref}`classic-ui-register-a-view-label` above, you registered a view.
If the view is registered with the wild card, it will be available on any content type.
It is also possible to restrict this to certain content type interfaces.
Please verify that your desired content type is allowed here and you can access it, as described in the previous section.

The list of available views for a content type is configured in its {doc}`/backend/content-types/fti`.

Add the name of the new view `my-view` to the following list:

```xml
<property name="default_view">document_view</property>
<property name="view_methods">
  <element value="document_view" />
  <element value="my-view" />
</property>
```


(classic-ui-template-slots-label)=

### Template slots

In the generated template above, we have a `fill-slot` attribute.
This will fill the slot with the name `content-core`, which is defined in Plone's [`main_template`](https://github.com/plone/Products.CMFPlone/blob/master/Products/CMFPlone/browser/templates/main_template.pt).
The following list shows the available options for `<metal fill-slot="">` in your template.

```{note}
Our template above inherits from `<html metal:use-macro="context/main_template/macros/master">`.
```


#### Metadata in `head`

`top_slot`
:   Used to set parameters on the request, for example to deactivate the left and right columns or caching.

    ```xml
    <metal:block
    fill-slot="top_slot"
       tal:define="dummy python:request.set('disable_border',1);
                   disable_column_one python:request.set('disable_plone.leftcolumn',1);
                   disable_column_two python:request.set('disable_plone.rightcolumn',1);" />
    ```

`head_slot`
:   Used to define HTML `head` elements, such as `link` tags for RSS and CSS.

`style_slot`
:   Used to define `style` tags to load CSS files.

`javascript_head_slot`
:   Used to define `script` tags to load JavaScript in the HTML `head` tag.

```{note}
Even though you can include CSS and JavaScript this way, most of the time you should register it in the {doc}`resource registry </classic-ui/static-resources>`.
```


#### Global status message

`global_statusmessage`
:   Used to fill in global status messages.


#### Content slots

`content`
:   The content area, including the `title`, `description`, `content-core`, and viewlets around them.

`body`
:   A slot inside the content macro.

`main`
:   Overrides the `main` slot in the main template.
    You must render `title` and `description` yourself.

`content-title`
:   `title` and `description` prerendered.

`content-description`
:   Content description for your view.

`content-core`
:   Content body specific to your view for Plone version 4.x or greater.


#### Asides and portlets

-   `column_one_slot`

    -   `portlets_one_slot`

-   `column_two_slot`

    -   `portlets_two_slot`


(classic-ui-relationship-between-views-and-templates-label)=

### Relationship between views and templates

The ZCML `<browser:view template="">` directive will set the `index` class attribute.

The default view's `__call__()` method will return the value returned by a call to `self.index()`.

For example, the following ZCML configuration:

```xml
<browser:page
    for="*"
    name="myview"
    permission="zope2.Public"
    class=".views.MyView"
    />
```

Together with the following Python code:

```python
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MyView(BrowserView):

    index = ViewPageTemplateFile("my-template.pt")
```

Is equal to the following ZCML configuration:

```xml
<browser:page
    for="*"
    name="myview"
    permission="zope2.Public"
    class=".views.MyView"
    template="my-template.pt"
    />
```

Together with this Python code:

```python
class MyView(BrowserView):
    pass
```

You can then render the view as follows:

```python
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class MyView(BrowserView):

    # This may be overridden in ZCML
    index = ViewPageTemplateFile("my-template.pt")

    def render(self):
        return self.index()

    def __call__(self):
        return self.render()
```


(classic-ui-several-templates-per-view-label)=

### Several templates per view

You can bind several templates to one view and render them individually.
This is useful for reusable templating, or when you subclass your functional views.

```python
from Products.Five.browser import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile


class CourseTimetables(BrowserView):

    template1 = ViewPageTemplateFile("template1.pt")
    template2 = ViewPageTemplateFile("template2.pt")

    def render_template1(self):
        return self.template1.render(self)

    def render_template2(self):
        return self.template2.render(self)
```

And then in the template call:

```xml
<div tal:replace="structure view/render_template1">

<div tal:replace="structure view/render_template2">
```


(classic-ui-view-init-method-special-cases-label)=

#### View `__init__()` method special cases

The Python constructor method of the view, `__init__()`, is special.
You should almost never try to put your code there.
Instead, use the `_call__()` method or further helper methods called from it.

The `__init__()` method of the view might not have an {ref}`acquisition chain <backend-traversal-label>` available, meaning that it does not know where is its parent or hierarchy.
This also means that you don't have user information and permissions for the view.

This information is set after the constructor has been run.
All Plone code relies on the acquisition chain, which means almost all Plone helper code does not work in `__init__()`.
Thus, the called Plone API methods return `None` or tend to throw exceptions.


(classic-ui-views-layers-label)=

### Layers

Views can be registered against a specific {doc}`layer </classic-ui/layers>` interface.
This means that views are only looked up if the specified layer is in use.
Since one Zope application server can contain multiple Plone sites, layers are used to determine which Python code is in effect for a given Plone site.

A layer is in use when either:

-   a theme which defines that layer is active, or
-   if a specific add-on product which defines that layer is installed in the Plone site.

You should register your views against a certain layer in your own code.

For more information, read the {doc}`/classic-ui/layers` chapter.


(classic-ui-register-and-unregister-a-view-directly-using-zope.component-architecture-label)=

### Register and unregister a view directly using `zope.component` architecture

The following is an example of how to register a view directly using the `zope.component` architecture:

```python
import zope.component
import zope.publisher.interfaces.browser

zope.component.provideAdapter(
    # Our class
    factory=TestingRedirectHandler,
    # (context, request) layers for multiadapter lookup
    # We provide None as layers are not used
    adapts=(None, None),
    # All views are registered as IBrowserView interface
    provides=zope.publisher.interfaces.browser.IBrowserView,
    # View name
    name="redirect_handler")
```

The following is an example of how to unregister the same view:

```python
# Dynamically unregister a view
gsm = zope.component.getGlobalSiteManager()
gsm.unregisterAdapter(factory=TestingRedirectHandler,
                      required=(None, None),
                      provided=zope.publisher.interfaces.browser.IBrowserView,
                      name="redirect_handler")
```


(classic-ui-customize-views-label)=

## Customize views

To customize existing Plone core or add-on views, you have different options.

-   Usually you can override the related page template file (`.pt`).
-   Sometimes you also need to change the related Python view class code.
    In this case, you override the Python class by using your own add-on, which installs a view class replacement using an add-on specific {term}`browser layer`.


(classic-ui-override-view-template-label)=

### Override view template

The recommended approach to customize `.pt` files for Plone is to use a little helper called [`z3c.jbot`](https://pypi.org/project/z3c.jbot/).

If you need to override templates in core Plone or in an existing add-on, you can do the following:

-   Create your own add-on with {term}`plonecli`, which you can use to contain your page templates on the file system.
-   The created package already contains an overrides folder for `z3c.jbot` in `browser/overrides`.
    Here you can place your template overrides.
-   `z3c.jbot` can override page templates (`.pt` files) for views, viewlets, old style page templates, and portlets.
    In fact, it can override any `.pt` file in the Plone source tree, except the `main_template.pt`.


(classic-ui-override-a-template-using-z3c-jbot-label)=

### Override a template using `z3c.jbot`

1.  First of all, make sure that your customization add-on supports `z3c.jbot`.
    Add-on packages created by `plonecli` have an `overrides` folder in the `browser` folder where you can drop in your new `.pt` files.

2.  Locate the template you need to override in the Plone source tree.
    You can do this by searching in all the installed packages for `.pt` files.
    If you use buildout with the `collective.recipe.omelette` recipe, a good folder to search in is `./parts/omelette`.

    The following is an example UNIX `find` command to find `.pt` files.
    You can also use Windows Explorer file search or similar tools:

    ```shell
    find -L ./parts/omelette -name "*.pt"
    ```
    ```console
    ./parts/omelette/plone/app/contenttypes/browser/templates/listing_album.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/listing.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/newsitem.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/full_view.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/full_view_item.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/document.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/image_view_fullscreen.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/link.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/file.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/listing_summary.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/listing_tabular.pt
    ./parts/omelette/plone/app/contenttypes/browser/templates/image.pt
    ./parts/omelette/plone/app/contenttypes/behaviors/richtext_gettext.pt
    ./parts/omelette/plone/app/contenttypes/behaviors/leadimage.pt
    ./parts/omelette/plone/app/contentrules/browser/templates/manage-elements.pt
    ./parts/omelette/plone/app/contentrules/browser/templates/controlpanel.pt
    ./parts/omelette/plone/app/contentrules/browser/templates/contentrules-pageform.pt
    ./parts/omelette/plone/app/contentrules/browser/templates/manage-assignments.pt
    ./parts/omelette/plone/app/contentrules/actions/templates/mail.pt
    ./parts/omelette/plone/app/viewletmanager/manage-viewlets.pt
    ./parts/omelette/plone/app/viewletmanager/manage-viewletmanager.pt
    ```

3.  Make a copy of the `.pt` file you want to override.
    To override a particular file, first determine its canonical filename.
    It is defined as the path relative to the package within which the file is located.
    Directory separators are replaced with dots.

    Suppose you want to override `plone/app/layout/viewlets/logo.pt`.

    You would use the filename `plone.app.layout.viewlets.logo.pt`.

    Place the file in the registered `overrides` folder in your add-on.

    Make your changes in the new `.pt` file.

    ```{note}
    After overriding the template for the first time (adding the file to the `overrides` folder), you need to restart Plone.
    `z3c.jbot` scans new overrides only during the restart.
    ```

After the file is in place, changes to the file are instantly picked up.
The template code is re-read on every HTTP request.

If you want to override an already overridden template, read [How can I override an already overridden template by `jbot`?](https://stackoverflow.com/questions/16209392/how-can-i-override-an-already-overridden-template-by-jbot).


(classic-ui-override-a-view-class-label)=

## Override a view class

In this example, we will override the `@@register` form from the `plone.app.users` package, creating a custom form which subclasses the original.
We assume you already have created a Plone add-on package with {term}`plonecli`.
As such, you will have the following browser layer interface and its registration in `profiles/default/browserlayer.xml`.

1.  Create an interface in `interfaces.py`:

    ```python
    from plone.theme.interfaces import IDefaultPloneLayer

    class ICollectiveAwesomeaddon(IDefaultPloneLayer):
        """ A marker interface for the theme layer
        """
    ```

1.  Then create `profiles/default/browserlayer.xml`:

    ```xml
    <layers>
      <layer
        name="collective.awesomeaddon"
        interface="collective.awesomeaddon.interfaces.ICollectiveAwesomeaddon"
      />
    </layers>
    ```

1.  Create `views/configure.zcml`:

    ```xml
    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        i18n_domain="collective.awesomeaddon">

      <browser:page
          name="register"
          class=".customregistration.CustomRegistrationForm"
          permission="cmf.AddPortalMember"
          for="plone.app.layout.navigation.interfaces.INavigationRoot"
          layer="collective.awesomeaddon.interfaces.ICollectiveAwesomeaddon"
          />

    </configure>
    ```

    ```{note}
    We have retained the permissions and marker interface of the original view.
    You may provide a specific permission or marker interface instead of these as your product requires.
    ```

1.  Create `views/customregistration.py`:

    ```
    from plone.app.users.browser.register import RegistrationForm

    class CustomRegistrationForm(RegistrationForm):
        """ Subclass the standard registration form
        """
    ```

```{tip}
You can also add a view to your package via {term}`plonecli` and place the Python code and ZCML registration in the generated view files as shown above.
This way you will also have a test for the generated view.
```


(classic-ui-guided-information-label)=

## Guided information

The Mastering Plone 5 Training has several chapters on views.

-   {doc}`training:mastering-plone-5/views_1`
-   {doc}`training:mastering-plone-5/views_2`
-   {doc}`training:mastering-plone-5/views_3`


(classic-ui-anatomy-of-a-view-label)=

## Anatomy of a view

Views are {term}`Zope Component Architecture` (ZCA) multi-adapter registrations.

Views are looked up by name.
The Zope publisher always does a view lookup, instead of traversing, if the name to be traversed is prefixed with `@@`.

Views are resolved with three inputs:

`context`
:   Any class or interface for which the view applies.
    If not given, `zope.interface.Interface` is used (corresponds to a registration `for="*"`).
    Usually this is a content item instance.

`request`
:   The current HTTP request.
    The interface `zope.publisher.interfaces.browser.IBrowserRequest` is used.

`layer`
:   Theme layer and add-on layer interface.
    If not given, `zope.publisher.interfaces.browser.IDefaultBrowserLayer` is used.

Views return an HTTP request payload as the output.
Returned strings are turned into HTML page responses.

Views can be any Python class taking in `(context, request)` construction parameters.
A minimal view would be the following.

```python
class MyView(object):

     def __init__(self, context, request):
          self.context = context
          self.request = request

     def __call__(self):
          return "Hello. This view is rendered in the context of %s" % self.context
```

However, in most cases:

```{todo}
Replace links to Plone 5.2 docs with links to Plone 6 docs.
Specifically:

-   [TAL page template](https://5.docs.plone.org/adapt-and-extend/theming/templates_css/template_basics)
-   [interface](https://5.docs.plone.org/develop/addons/components/interfaces)
```

-   Full Plone page views are a subclass of [`Products.Five.browser.BrowserView`](https://github.com/zopefoundation/Zope/blob/d1814d0a6bddb615629b552de10e9aa5ad30a6da/src/Products/Five/browser/__init__.py#L20) which is a wrapper class.
    It wraps [`zope.publisher.browser.BrowserView`](https://github.com/zopefoundation/zope.publisher/blob/dea3d4757390d04f6a5b53e696f08d0cab5f6023/src/zope/publisher/browser.py#L958), and adds an acquisition (parent traversal) support for it.
-   Views have an attribute `index`, which points to a [TAL page template](https://5.docs.plone.org/adapt-and-extend/theming/templates_css/template_basics) that is responsible for rendering the HTML code.
    You get the HTML output with `self.index()`.
    The page template gets a context argument `view`, pointing to the view class instance.
    The `index` value is usually an instance of [`Products.Five.browser.pagetemplate.ViewPageTemplateFile`](https://github.com/zopefoundation/Zope/blob/d1814d0a6bddb615629b552de10e9aa5ad30a6da/src/Products/Five/browser/pagetemplatefile.py#L35) for full Plone pages or [`zope.pagetemplate.pagetemplatefile.PageTemplateFile`](https://github.com/zopefoundation/zope.pagetemplate/blob/14ba59c98e12517b9f8abcdb24bc882bb435ed7c/src/zope/pagetemplate/pagetemplatefile.py#L43) for HTML snippets without using acquisition.
-   View classes should implement the [interface](https://5.docs.plone.org/develop/addons/components/interfaces)
  [`zope.browser.interfaces.IBrowserView`](https://github.com/zopefoundation/zope.browser/blob/1239c75e4e190df992bf34a88b4ead2c952afe86/src/zope/browser/interfaces.py#L27).

Views that render page snippets and parts can be direct subclasses of `zope.publisher.browser.BrowserView`, as snippets might not need acquisition support which adds some overhead to the rendering process.


(classic-ui-helper-views-label)=

## Helper views

Not all views need to return HTML output, or output at all.
Views can be used as helpers in the code to provide APIs to objects.
Since views can be overridden using layers, a view is a natural plug-in point which an add-on product can customize or override in a conflict-free manner.

View methods are exposed to page templates.
As such, you can call view methods directly from a page template, not only from Python code.

```{todo}
Replace links to Plone 5.2 docs with links to Plone 6 docs.
Specifically:

-   [Helper views and tools](https://5.docs.plone.org/develop/plone/misc/context)
-   [Expressions](https://5.docs.plone.org/develop/plone/functionality/expressions)
```

```{seealso}
-   [Helper views and tools](https://5.docs.plone.org/develop/plone/misc/context)
-   [Expressions](https://5.docs.plone.org/develop/plone/functionality/expressions)
```


(classic-ui-historical-perspective-label)=

### Historical perspective

Often, the point of using helper views is that you can have reusable functionality which can be plugged in as one-line code around the system.
Helper views also get around the following limitations:

-   TAL security
-   Limiting Python expression to one line
-   Not being able to import Python modules

```{caution}
Using `RestrictedPython` scripts (creating Python through the Management Interface) and Zope Extension modules is discouraged.
The same functionality can be achieved with helper views, with fewer potential pitfalls.
```


(classic-ui-reuse-view-template-snippets-macros-or-embed-another-view-label)=

## Reuse view template snippets (macros) or embed another view

To use the same template code several times you can either:

-   create a separate `BrowserView` for it, and then call this view (see {ref}`classic-ui-access-a-view-instance-in-code-label`), or
-   share a `ViewPageTemplate` instance between views and using it several times.

```{caution}
The old way of providing reusable functionality in your add-on product with TAL template language macros is discouraged.
This is because macros are hardwired to the TAL template language, and referring to them outside templates is difficult.
If you ever need to change the template language, or mix in other template languages, you can do better when templates are a feature of a pure Python based view, and not vice versa.
```

The following code snippet is an example of how to have a view snippet which can be used by subclasses of a base view class.
Subclasses can refer to this template at any point of the view rendering, making it possible for subclasses to have fine-tuned control over how the template snippet is represented.

```python
from Products.Five import BrowserView
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

class ProductCardView(BrowserView):
    """
    End user visible product card presentation.
    """
    implements(IProductCardView)

    # Nested template which renders address box + buy button
    summary_template = ViewPageTemplateFile("summarybox.pt")


    def renderSummary(self):
        """ Render summary box

        @return: Resulting HTML code as Python string
        """
        return self.summary_template()
```

Then you can render the summary template in the main template associated with `ProductCardView` by calling the method `renderSummary()` and TAL non-escaping HTML embedding.

```html
<h1 tal:content="context/Title" />

<div tal:replace="structure view/renderSummary" />

<div class="description">
    <div tal:condition="python:context.Description().decode('utf-8') != 'None'" tal:replace="structure context/Description" />
</div>
```

The `summarybox.pt` itself is a piece of HTML code without the Plone decoration frame (`main_template/master`, and other macros).
Make sure that you declare the `i18n:domain` again, or the strings in this template will not be translated.

```html
<div class="summary-box" i18n:domain="your.package">
    ...
</div>
```


(classic-ui-access-a-view-instance-in-code-label)=

## Access a view instance in code

You need to get access to the view in your code if you call a view from either: 

-   inside another view
-   your unit test code

Below are several different approaches for that.
You can choose the approach most suitable for your situation.


(classic-ui-view-use-plone-api)=

### Use `plone.api.content.get_view()`

The `plone.api` provides a method to get a view by its registered name, the context, and the current request.

```python
from plone import api

portal = api.portal.get()
view = api.content.get_view(
    name="plone",
    context=portal["about"],
    request=request,
)
```

```{versionchanged} 2.0.0
Since `plone.api` version 2.0.0, the request argument can be omitted.
In that case, the global request will be used.

For more details see {ref}`content-get-view-example`.
```

```{note}
The usage of `plone.api` in Plone core is limited.
If in doubt, please use the following methods instead.
```

(classic-ui-use-getmultiadapter-label)=

### Use `getMultiAdapter()`

This is the most efficient way in Python.

Example:

```python
from Acquisition import aq_inner
from zope.component import getMultiAdapter

def getView(context, request, name):
    # Remove the acquisition wrapper (prevent false context assumptions)
    context = aq_inner(context)
    # May raise ComponentLookUpError
    view = getMultiAdapter((context, request), name=name)
    # Add the view to the acquisition chain
    view = view.__of__(context)
    return view
```


(classic-ui-use-traversal-label)=

### Use traversal

Traversal is slower than directly calling `getMultiAdapter()`.
However, traversal is readily available in templates and `RestrictedPython` modules.

Example:

```python
def getView(context, name):
    """ Return a view associated with the context and current HTTP request.

    @param context: Any Plone content object.
    @param name: Attribute name holding the view name.
    """

    try:
        view = context.unrestrictedTraverse("@@" + name)
    except AttributeError:
        raise RuntimeError("Instance %s did not have view %s" % (str(context), name))

    view = view.__of__(context)

    return view
```

You can also do direct view look-ups and method calls in your template by using the `@@` notation in traversal.

```html
<div tal:attributes="lang context/@@plone_portal_state/current_language">
    We look up the `lang` attribute by using `BrowserView` whose name is `plone_portal_state`.
</div>
```


(classic-ui-use-a-skin-based-template-in-a-five-view-label)=

### Use a skin-based template in a `Five` view

You can use a skin-based template in a `Five` view with `aq_acquire(object, template_name)`.

For example, you can get an object by its path, and render it using its default template in the current context.

```python
from Acquisition import aq_base, aq_acquire
from Products.Five.browser import BrowserView

class TelescopeView(BrowserView):
    """
    Renders an object in a different location of the site when passed the
    path to it in the querystring.
    """
    def __call__(self):
        path = self.request["path"]
        target_obj = self.context.restrictedTraverse(path)
        # Strip the target_obj of context with aq_base.
        # Put the target in the context of self.context.
        # getDefaultLayout returns the name of the default
        # view method from the factory type information
        return aq_acquire(aq_base(target_obj).__of__(self.context),
                          target_obj.getDefaultLayout())()
```


(classic-ui-advanced-label)=

## Advanced

This section describes advanced techniques for working with view.


(classic-ui-list-available-views-label)=

### List available views

The following example is useful for debugging purposes.

```python
from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest

# views is generator of zope.component.registry.AdapterRegistration objects
views = registration.getViews(IBrowserRequest)
```


(classic-ui-list-all-views-of-a-given-type-label)=

#### List all views of a given type

The following example filters out views which provide a given interface:

```python
from plone.app.customerize import registration
from zope.publisher.interfaces.browser import IBrowserRequest

# views is generator of zope.component.registry.AdapterRegistration objects
views = registration.getViews(IBrowserRequest)

# Filter out all classes which implement a certain interface
views = [ view.factory for view in views if IBlocksView.implementedBy(view.factory) ]
```


(classic-ui-default-view-of-a-content-item-label)=

### Default view of a content item

Objects have views for `default`, `view`, `edit`, and other views.

The distinction between the `default` and `view` views are that, for files, the default can be `download`.

-   The `default` view is configured in {doc}`/backend/content-types/index`.
-   The `default` view is rendered when a content item is called.
    Even though they are objects, they have the `__call__()` Python method defined.

If you need to explicitly get a content item's view for page rendering, you can do it as follows:

```python
def viewURLFor(item):
    cstate = getMultiAdapter((item, item.REQUEST),
                             name="plone_context_state")
    return cstate.view_url()
```

```{todo}
Replace links to Plone 5.2 docs to Plone 6 docs.
Specifically:

-   [Helper views and tools](https://5.docs.plone.org/develop/plone/misc/context)
```

```{seealso}
-   [Helper views and tools](https://5.docs.plone.org/develop/plone/misc/context)
-   [URL to content view](https://web.archive.org/web/20110529043150/http://plone.293351.n2.nabble.com/URL-to-content-view-td6028204.html)
```


(classic-ui-allow-the-contentmenu-on-non-default-views-label)=

### Allow the `contentmenu` on non-default views

In general, the {guilabel}`contentmenu` (where the actions, display views, factory types, workflow, and other select menus are located) is not shown on non-default views.
There are some exceptions, though.

If you want to display the {guilabel}`contentmenu` in non-default views, you have to mark them with the `IViewView` interface from `plone.app.layout`, either by letting the class provide `IViewView` by declaring it with `zope.component.implements` or by configuring it via ZCML as follows:

```xml
<class class="dotted.path.to.browser.view.class">
  <implements interface="plone.app.layout.globals.interfaces.IViewView" />
</class>
```


(classic-ui-zope-viewpagetemplatefile-vs-five-viewpagetemplatefile-label)=

## Zope `ViewPageTemplateFile` versus `Five` `ViewPageTemplateFile`

```{warning}
There are two different classes that share the same name `ViewPageTemplateFile`.
```

-   Zope [`BrowserView` source code](https://github.com/zopefoundation/zope.publisher/blob/dea3d4757390d04f6a5b53e696f08d0cab5f6023/src/zope/publisher/browser.py#L958).
-   [`Five` version](https://github.com/zopefoundation/Zope/blob/d1814d0a6bddb615629b552de10e9aa5ad30a6da/src/Products/Five/browser/__init__.py#L20) with [`Products.Five`](https://github.com/zopefoundation/Zope/blob/master/src/Products/Five/doc/manual.txt) is a way to access some Zope 3 technologies from the Zope codebase, which is used by Plone.

Compare the differences in code.

```python
from zope.app.pagetemplate import ViewPageTemplateFile
```

versus:

```python
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
```

The difference is that the `Five` version supports:

-   acquisition
-   the `provider:` TAL expression
-   other Plone-specific TAL expression functions, such as `test()`
-   Usually, Plone code needs the `Five` version of `ViewPageTemplateFile`.
-   Some subsystems, notably the `z3c.form` package, expect the Zope 3 (not `Five`) version of `ViewPageTemplateFile` instances.


(classic-ui-views-and-automatic-member-variable-acquisition-wrapping-label)=

### Views and automatic member variable acquisition wrapping

View class instances will automatically assign themselves as a parent for all member variables.
This is because `Five`-based views inherit from the `Acquisition.Implicit` base class.

For example, say you have a content item `Basket` with an `absolute_url()` of:

```console
http://localhost:9666/isleofback/sisalto/matkasuunnitelmat/d59ca034c50995d6a77cacbe03e718de
```

Then if you use this object in a view code's member variable assignment, such as in the method `Viewlet.update()`:

```python
self.basket = my_basket
```

…it will mess up the Basket content item's acquisition chain:

```console
<Basket at /isleofback/sisalto/yritykset/katajamaan_taksi/d59ca034c50995d6a77cacbe03e718de>
```

This concerns views, viewlets, and portlet renderers.
It will, for example, make the following code fail:

```python
self.obj = self.context.reference_catalog.lookupObject(value)
return self.obj.absolute_url()  # Acquistion chain messed up, getPhysicalPath() fails
```

One workaround to avoid this mess is to use `aq_inner` when accessing `self.obj` values, as described in [Dealing with view implicit acquisition problems in Plone](https://stackoverflow.com/questions/11753940/dealing-with-view-implicit-acquisition-problems-in-plone/11755348#11755348).
