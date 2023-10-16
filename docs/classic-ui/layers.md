---
myst:
  html_meta:
    "description": "Layers allow you to enable and disable views and other site functionality based on installed add-ons and themes."
    "property=og:description": "Layers allow you to enable and disable views and other site functionality based on installed add-ons and themes."
    "property=og:title": "Layers in Plone 6"
    "keywords": "layer, layers, browser layer, views, viewlets, portlets"
---

(classic-ui-layers-label)=

# Layers

Layers allow you to activate different code paths and modules depending on the external configuration.
Layers are useful in the following scenarios.

-   Code belonging to a theme is only active when that theme has been selected.
-   Mobile browsing code is only active when the site is being browsed on a mobile phone.

Layers are marker interfaces applied to the {term}`HTTPRequest` object.
They are usually used in conjunction with Zope Configuration Mark-up Language ({term}`ZCML`) directives to dynamically activate various parts of the configuration, such as theme files or add-on product functionality.

Layers ensure that only one add-on product can override the specific Plone instance functionality in your site at a time, while still allowing you to have possibly conflicting add-on products in your buildout and ZCML.
Multiple Plone site instances can share the same ZCML and code files.

Many ZCML directives take the optional `layer` parameter.
Layers are activated when an add-on product is installed or a certain theme is activated.
You can find an example of the layer attribute in the Chapter {ref}`classic-ui-using-layers-label`.


(classic-ui-using-layers-label)=

## Using layers

Some ZCML directives take a `layer` attribute, such as `browser:page`.

Given the following:

-   A layer interface defined in Python code, `plonetheme.yourthemename.interfaces.IThemeSpecific`.
-   Your add-on or theme package installed through the add-on product installer on your site instance.

Then views and viewlets from your product can be enabled on the site instance using the following ZCML:

```xml
<!-- Site actions override in YourTheme -->
<browser:viewlet
    name="plone.site_actions"
    manager="plone.app.layout.viewlets.interfaces.IPortalHeader"
    class=".siteactions.SiteActionsViewlet"
    layer="plonetheme.yourthemename.interfaces.IThemeSpecific"
    permission="zope2.View"
    />
```


(classic-ui-unconditional-overrides-label)=

### Unconditional overrides

If you want to override a view or a viewlet unconditionally for all sites without the add-on product installer support, you need to use `overrides.zcml`.
You can override classes and templates in this file.
To do this, you put the ZCML registration in a file called `overrides.zcml` in the package root, next to the top-most `configure.zcml`.


(classic-ui-creating-a-layer-label)=

## Creating a layer

Developers can create layers for themes, extensions, behaviors, and other functions.


(classic-ui-theme-layer-label)=

### Theme layer

Theme layers can be created through the following steps.

1.  Subclass an interface from `IDefaultPloneLayer`:

    ```python
    from plone.theme.interfaces import IDefaultPloneLayer


    class IThemeSpecific(IDefaultPloneLayer):
        """
        Marker interface that defines a Zope 3 skin layer bound to a Skin
        Selection in portal_skins.
        If you need to register a viewlet only for the "YourSkin"
        skin, this is the interface that must be used for the layer attribute
        in YourSkin/browser/configure.zcml.
        """
    ```

2.  Register it in ZCML.
    The name must match the theme name.

    ```xml
    <interface
        interface=".interfaces.IThemeSpecific"
        type="zope.publisher.interfaces.browser.IBrowserSkinType"
        name="SitsSkin"
        />
    ```

3.  Register and set your theme as the default theme in `profiles/default/skins.xml`.
    Theme layers require that they are set as the default theme and not just activated on your Plone site.
    Example:

    ```xml
    <object name="portal_skins" allow_any="False" cookie_persistence="False"
        default_skin="SitsSkin">

        <!-- define skins-based folder objects here if any -->

        <skin-path name="SitsSkin" based-on="Plone Default">
            <layer name="plone_skins_style_folder_name"
                insert-before="*"/>
        </skin-path>

    </object>
    ```


(classic-ui-add-on-layer-for-clean-extensions-label)=

### Add-on layer for clean extensions

An add-on product layer is enabled when an add-on product is installed.
Since one Zope application server may contain several Plone sites, you need to keep enabled code paths separate by using add-on layers.
Otherwise, all views and viewlets apply to all sites in one Zope application server.

-   You can enable views and viewlets specific to functional add-ons.
-   Unlike theme layers, add-on layers depend on the activated add-on products, not on the selected theme.

An add-on layer is a marker interface which is applied on the {term}`HTTPRequest` object by Plone core logic.

First create an {term}`interface` for your layer in `your.product.interfaces.py`:

```python
""" Define interfaces for your add-on.
"""

import zope.interface

class IAddOnInstalled(zope.interface.Interface):
    """ A layer specific for this add-on product.

    This interface is referred in browserlayer.xml.

    All views and viewlets register against this layer will appear on
    your Plone site only when the add-on installer has been run.
    """
```

You then need to refer to this in the `profile/default/browserlayer.xml` file of your add-on installer to use it:

```xml
<layers>
    <layer
        name="your.product"
         interface="your.product.interfaces.IAddOnInstalled"
         />
</layers>
```

```{note}
The add-on layer registry is persistent and stored in the database.
The changes to add-on layers are applied only when add-ons are installed or uninstalled.
```

```{seealso}
https://pypi.org/project/plone.browserlayer/
```


(classic-ui-add-on-layer-for-changing-existing-behavior-label)=

### Add-on layer for changing existing behavior

You can also use layers to modify the behavior of Plone or another add-on.

To make sure that your own view is used, your layer must be more specific than the layer where the original view is registered.

For example, some `z3cform` things register their views on the `IPloneFormLayer` from `plone.app.z3cform.interfaces`.

If you want to override the `ploneform-macros` view that is registered on the `IPloneFormLayer`, your own layer must be a subclass of `IPloneFormLayer`.

If a view does not declare a specific layer, it becomes registered on the `IDefaultBrowserLayer` from `zope.publisher.interfaces.browser.IDefaultBrowserLayer`.


(classic-ui-manual-layers-label)=

### Manual layers

Apply your layer to the {term}`HTTPRequest` in the `before_traverse` hook, or before you call the code which looks up the interfaces.

In the example below, we turn on a layer for the request, which is later checked by the rendering code.
This way some pages can ask for special View/Viewlet rendering.

```python
# Defining layer

from zope.publisher.interfaces.browser import IBrowserRequest

class INoHeaderLayer(IBrowserRequest):
    """ When applied to HTTP request object, header animations
    or images are not rendered on this layer.

    If this layer is on a request, do not render header images.
    This allows uncluttered editing of header animations and images.
    """

# Applying layer for some requests (manually done in view)
# The browser page which renders the form
class EditHeaderAnimationsView(FormWrapper):

    form = HeaderCRUDForm

    def __call__(self):
        """ """

        # Signal viewlet layer that we are rendering
        # edit view for header animations and it is not meaningful
        # to try to render the big animation on this page
        zope.interface.alsoProvides(self.request, INoHeaderLayer)

        # Render the edit form
        return FormWrapper.__call__(self)
```


(classic-ui-troubleshooting-instructions-for-layers-label)=

## Troubleshooting instructions for layers

-   Check that your view is working without a layer assigned globally.
-   Check that `configure.zcml` has a layer entry.
    Put some garbage to trigger a syntax error in `configure.zcml` to make sure that it is being loaded.
-   Add-on layer: check that `profiles/default/browserlayer.xml` has a matching entry with a matching name.
-   Theme layer: if it is a theme layer, check that there is a matching `skins.xml` entry.
-   Check that the layer name is spelled correctly in the view declaration.


(classic-ui-checking-active-layers-label)=

## Checking active layers

This section describes a few strategies for developers to check active layers according to their type.


(classic-ui-layers-are-activated-on-the-current-request-object-label)=

### Layers are activated on the current request object

Example:

```python
if INoHeaderLayer.providedBy(self.request):
    # The page has asked to suspend rendering of the header animations
    return ""
```


(classic-ui-active-themes-and-add-on-products-label)=

### Active themes and add-on products

The `registered_layers()` method returns a list of all layers active on the site.
Note that this is different from the list of layers which are applied on the current HTTP request object.
The request object may contain manually activated layers.

Example:

```python
from interfaces import IThemeSpecific
from plone.browserlayer.utils import registered_layers

if IThemeSpecific in registered_layers():
    # Your theme specific code
    pass
else:
    # General code
    pass
```


(classic-ui-getting-active-theme-layer-label)=

### Getting active theme layer

Only one theme layer can be active at once.

The active theme name is defined in `portal_skins` properties.
This name can be resolved to a theme layer.


(classic-ui-debugging-active-layers-label)=

### Debugging active layers

You can check the activated layers from the HTTP request object by looking at `self.request.__provides__.__iro__`.
Layers are evaluated from zero index (highest priority) to the last index (lowest priority).


(classic-ui-testing-layers-label)=

## Testing layers

Plone testing tool kits will not register layers for you.
You have to do it yourself somewhere in the boilerplate code, as shown in the following example.

```python
from zope.interface import directlyProvides

directlyProvides(self.portal.REQUEST, IThemeLayer)
```
