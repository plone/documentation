---
myst:
  html_meta:
    "description": "Custom add and edit forms in Plone"
    "property=og:description": "Custom add and edit forms in Plone"
    "property=og:title": "Custom add and edit forms in Plone"
    "keywords": "Plone, custom, add, edit, forms"
---

# Custom add and edit forms

This chapter describes how to use `z3c.form` to build custom forms.

Until now, we have used Dexterity's default content add and edit forms, supplying form hints in our schemata to influence how the forms are built.
For most types, that is all that's ever needed.
In some cases, however, we want to build custom forms, or supply additional forms.

Dexterity uses the [`z3c.form`](https://z3cform.readthedocs.io/en/latest/) library to build its forms, via the [`plone.z3cform`](https://pypi.org/project/plone.z3cform/) integration package.

Dexterity also relies on [`plone.autoform`](https://pypi.org/project/plone.autoform/), in particular its `AutoExtensibleForm` base class, which is responsible for processing form hints and setting up `z3c.form` widgets and groups (fieldsets).
A custom form, therefore, is simply a view that uses these libraries, although Dexterity provides some helpful base classes that make it easier to construct forms based on the schema and behaviors of a Dexterity type.

```{note}
If you want to build standalone forms not related to content objects, see the [`z3c.form` documentation](https://z3cform.readthedocs.io/en/latest/).
```


## Edit forms

An edit form is just a form that is registered for a particular type of content and knows how to register its fields.
If the form is named `edit`, it will replace the default edit form, which is registered with that name for the more general `IDexterityContent` interface.

Dexterity provides a standard edit form base class that provides sensible defaults for buttons, labels, and so on.
This should be registered for a type schema (not a class).
To create an edit form that is identical to the default, we could do the following.

```python
from plone.dexterity.browser import edit

class EditForm(edit.DefaultEditForm):
    pass
```

And register it in {file}`configure.zcml`.

```xml
<browser:page
    for=".fs_page.IFSPage"
    name="edit"
    class=".fs_page.EditForm"
    permission="cmf.ModifyPortalContent"
    />
```

This form is of course not terribly interesting, since it is identical to the default.
However, we can now start changing fields and values.
For example, we could do any of the following.

-   Override the `schema` property to tell `plone.autoform` to use a different schema interface (with different form hints) than the content type schema.
-   Override the `additionalSchemata` property to tell `plone.autoform` to use different supplemental schema interfaces.
    The default is to use all behavior interfaces that provide the `IFormFieldProvider` marker from `plone.autoform`.
-   Override the `label` and `description` properties to provide a different title and description for the form.
-   Set the `z3c.form` `fields` and `groups` attributes directly.
-   Override the `updateWidgets()` method to modify widget properties, or one of the other `update()` methods, to perform additional processing on the fields.
    In most cases, these require us to call the `super` version at the beginning.
    See the [`plone.autoform`](https://pypi.org/project/plone.autoform/#introduction) and [`z3c.form` documentation](https://z3cform.readthedocs.io/en/latest/) to learn more about the sequence of calls that emanate from the form `update()` method in the `z3c.form.form.BaseForm` class.
-   Override the `template` attribute to specify a custom template.


## Content add sequence

Add forms are similar to edit forms in that they are built from a type's schema and the schemata of its behaviors.
However, for an add form to be able to construct a content object, it needs to know which `portal_type` to use.

You should realize that the FTIs in the `portal_types` tool can be modified through the web.
It is even possible to create new types through the web that reuse existing classes and factories.

For this reason, add forms are looked up via a namespace traversal adapter called `++add++`.
You may have noticed this in the URLs to add forms already.
What actually happens is the following.

-   Plone renders the {guilabel}`add` menu.

    -   To do so, it looks, among other places, for actions in the `folder/add` category.
        This category is provided by the `portal_types` tool.
    -   The `folder/add` action category is constructed by looking up the `add_view_expr` property on the FTIs of all addable types.
        This is a TALES expression telling the add menu which URL to use.
    -   The default `add_view_expr` in Dexterity (and CMF 2.2) is `string:${folder_url}/++add++${fti/getId}`.
        That is, it uses the `++add++` traversal namespace with an argument containing the FTI name.

-   A user clicks on an entry in the menu, and is taken to a URL using the parttern `/path/to/folder/++add++my.type`.

    -   The `++add++` namespace adapter looks up the FTI with the given name, and gets its `factory` property.
    -   The `factory` property of an FTI gives the name of a particular `zope.component.interfaces.IFactory` utility, which is used later to construct an instance of the content object.
        Dexterity automatically registers a factory instance for each type, with a name that matches the type name, although it is possible to use an existing factory name in a new type.
        This allows administrators to create new "logical" types that are functionally identical to an existing type.
    -   The `++add++` namespace adapter looks up the actual form to render as a multi-adapter from `(context, request, fti)` to `Interface` with a name matching the `factory` property.
        Recall that a standard view is a multi-adapter from `(context, request)` to `Interface` with a name matching the URL segment for which the view is looked up.
        As such, add forms are not standard views, because they get the additional `fti` parameter when constructed.
    -   If this fails, there is no custom add form for this factory, as is normally the case.
        The fallback is an unnamed adapter from `(context, request, fti)`.
        The default Dexterity add form is registered as such an adapter, specific to the `IDexterityFTI` interface.

-   The form is rendered like any other `z3c.form` form instance, and is subject to validation, which may cause it to be loaded several times.

-   Eventually, the form is successfully submitted.
    At this point:

    -   The standard `AddForm` base class will look up the factory from the FTI reference it holds and call it to create an instance.
    -   The default Dexterity factory looks at the `klass` [^id2] attribute of the FTI to determine the actual content class to use, creates an object and initializes it.
    -   The `portal_type` attribute of the newly created instance is set to the name of the FTI.
        Thus, if the FTI is a "logical type" created through the web, but using an existing factory, the new instance's `portal_type` will be set to the "logical type".
    -   The object is initialized with the values submitted in the form.
    -   An `IObjectCreatedEvent` is fired.
    -   The object is added to its container.
    -   The user is redirected to the view specified in the `immediate_view` property of the FTI.

[^id2]: `class` is a reserved word in Python, so we use `klass`.

This sequence is pretty long, but thankfully we rarely have to worry about it.
In most cases, we can use the default add form, and when we can't, creating a custom add form is only a bit more difficult than creating a custom edit form.


## Custom add forms

As with edit forms, Dexterity provides a sensible base class for add forms that knows how to deal with the Dexterity FTI and factory.

A custom form replicating the default would be the following.

```python
from plone.dexterity.browser import add

class AddForm(add.DefaultAddForm):
    portal_type = 'example.fspage'

class AddView(add.DefaultAddView):
    form = AddForm
```

And be registered in ZCML as follows.

```xml
<adapter
    for="Products.CMFCore.interfaces.IFolderish
         zope.publisher.interfaces.browser.IDefaultBrowserLayer
         plone.dexterity.interfaces.IDexterityFTI"
    provides="zope.publisher.interfaces.browser.IBrowserPage"
    factory=".fs_page.AddView"
    name="example.fspage"
    />
<class class=".fs_page.AddView">
    <require
        permission="cmf.AddPortalContent"
        interface="zope.publisher.interfaces.browser.IBrowserPage"
        />
</class>
```

The name here should match the *factory* name.
By default, Dexterity types have a factory called the same as the FTI name.
If no such factory exists (in other words, you have not registered a custom `IFactory` utility), a local factory utility will be created and managed by Dexterity when the FTI is installed.

Also note that we do not specify a context here.
Add forms are always registered for any `IFolderish` context.

```{note}
If the permission used for the add form is different from the `add_permission` set in the FTI, the user needs to have *both* permissions to be able to see the form and add content.
For this reason, most add forms will use the generic `cmf.AddPortalContent` permission.
The {guilabel}`add` menu will not render links to types where the user does not have the add permission stated in the FTI, even if this is different to `cmf.AddPortalContent`.
```

As with edit forms, we can customize this form by overriding `z3c.form` and `plone.autoform` properties and methods.
See the [`z3c.form` documentation](https://z3cform.readthedocs.io/en/latest/) on add forms for more details.
