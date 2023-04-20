---
myst:
  html_meta:
    "description": "Schema-driven types in Plone"
    "property=og:description": "Schema-driven types in Plone"
    "property=og:title": "Schema-driven types in Plone"
    "keywords": "Plone, schema-driven, types"
---

# Schema-driven types

This chapter describes how to create a minimal type based on a schema.


(the-schema-label)=

## The schema

A simple Dexterity type consists of a schema and a Factory Type Information (FTI), the object configured in {guilabel}`portal_types` in the ZMI.
We'll create the schemata here, and the FTI on the next page.

Each schema is typically in a separate module.
Thus, we will add three files to our product: `presenter.py`, `program.py`, and `session.py`.
Each will start off with a schema interface.


## Creating base files

`mr.bob` created some support for our initial content type, `Program`.
Let's clean it up a bit, then add another content type.

```{note}
The template's original setup assumed we added a single content type.
In fact, we're going to add three.
We'll separate their support files in order to keep our code clean.
```

In your package's `src/example/conference` directory, you should find a file named `interfaces.py`.
Copy that file to `program.py` in the same directory.
In `interfaces.py`, delete the `IProgram` class.
In `program.py`, delete the `IExampleConferenceLayer` class.

In your package's `src/example/conference/profiles/default/types` directory, you should find a file named `Program.xml`.
Find the line that reads:

```xml
<property name="schema">example.conference.interfaces.IProgram</property>
```

and change it to read:

```xml
<property name="schema">example.conference.program.IProgram</property>
```

That makes our setup profile point to our renamed schema file.


(adding-sessions-label)=

## Adding sessions

Now let's add another content type for our conference sessions.

First return to the `program.py` file.
Copy it to `session.py`.
In `session.py`, rename the `IProgram` class to `ISessions`.

Copy the `Program.xml` file in the `types/` subdirectory to `Session.xml`.

Change `example.conference.program.IProgram` to `example.conference.program.ISession` in the new XML file.
Change `Program` anywhere it appears to `Session`.
Do the same for `program` and `session`.

Find the `src/example/conference/profiles/types.xml` file, add a new object declaration:

```xml
<object name="portal_types" meta_type="Plone Types Tool">
  <object name="Program" meta_type="Dexterity FTI"/>
  <object name="Session" meta_type="Dexterity FTI"/>
</object>
```

Repeat the {ref}`adding-sessions-label` steps for `presenter.py`, `IPresenter`, and `presenter.xml`.


### Setting the schema

Start with `program.py`.
Add schema declarations for our `start`, `end`, and `details` fields.

The top part of the file should look like the following.

```python
from example.conference import _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema


class IProgram(model.Schema):

    """A conference program. Programs can contain Sessions."""

    title = schema.TextLine(
        title=_('Program name'),
    )

    description = schema.Text(
        title=_('Program summary'),
    )

    start = schema.Datetime(
        title=_('Start date'),
        required=False,
    )

    end = schema.Datetime(
        title=_('End date'),
        required=False,
    )

    details = RichText(
        title=_('Details'),
        description=_('Details about the program.'),
        required=False,
    )
```

If you haven't developed for Plone before, take special note of the `from example.conference import MessageFactory as _` code.
This is to aid future internationalization of the package.
Every string that is presented to the user should be wrapped in `_()`, as shown with the titles and descriptions below.

The `_` lives in the package root `__init__.py` file.

```python
from zope.i18nmessageid import MessageFactory

_ = MessageFactory('example.conference')
```

Notice how we use the package name as the translation domain.

Notice how we use the field names `title` and `description` for the name and summary.
We do this to provide values for the default title and description metadata used in Plone's folder listings and searches, which defaults to these fields.
In general, every type should have a `title` field, although it could be provided by behaviors (more on those later).

Save `program.py`.

`session.py` for the Session type should look like the following.

```python
from example.conference import _
from plone.app.textfield import RichText
from plone.supermodel import model
from zope import schema


class ISession(model.Schema):

    """A conference session. Sessions are managed inside Programs."""

    title = schema.TextLine(
        title=_('Title'),
        description=_('Session title'),
    )

    description = schema.Text(
        title=_('Session summary'),
    )

    details = RichText(
        title=_('Session details'),
        required=False
    )
```

Note that we haven't added information about speakers or tracks yet.
We'll do that when we cover vocabularies and references later.


## Schema interfaces versus other interfaces

As you may have noticed, each schema is basically just an interface (`zope.interface.Interface`) with fields.
The standard fields are found in the [`zope.schema`](https://pypi.org/project/zope.schema/) package.
You should look at its interfaces (`parts/omelette/zope/schema/interfaces.py`) to learn about the various schema fields available, and review [`zope.schema`'s documentation](https://zopeschema.readthedocs.io/en/latest/) for the package.
You may also want to look up [`plone.namedfile`](https://pypi.org/project/plone.namedfile/), which you can use if you require a file field, [`plone.app.relationfield`](https://pypi.org/project/plone.app.relationfield/), which can be used for references, and [`plone.app.textfield`](https://pypi.org/project/plone.app.textfield/), which supports rich text with a WYSIWYG editor.
We will cover these field types later in this manual.
They can also be found in the reference at the end.

Unlike a standard interface, however, we are deriving from `model.Schema` (actually, `plone.supermodel.model.Schema`).
This is just a marker interface that allows us to add some form hints to the interface, which are then used by Dexterity (actually, the [`plone.autoform`](https://pypi.org/project/plone.autoform/) package) to construct forms.
Take a look at the [`plone.autoform` documentation](https://pypi.org/project/plone.autoform/#introduction) to learn more about the various hints that are possible.
The most common ones are from `plone.autoform.directives`.
Use `fieldset()` to define groups of fields, `widget()` to set widgets for particular fields and `omitted()` to hide one or more fields from the form.
We will see examples of these later in the manual.


(zope-schema)=

## Factory Type Information (FTI)

This section describes how to add a Factory Type Information (FTI) object for the type.

When we created the files `types/session.xml` and `types/presenter.xml`, and added object declarations to `types.xml`, we made our new content types installable.
These XML configuration files are referred to as Generic Setup Profiles.

Look in the `types.xml` file in your package's `example/conference/profiles/default` directory.

```xml
<object name="portal_types">
  <object name="Program" meta_type="Dexterity FTI" />
  <object name="Session" meta_type="Dexterity FTI" />
  <object name="Presenter" meta_type="Dexterity FTI" />
</object>
```

Note that the type name should be unique.
If it isn't, use the package name as a prefix and the type name to create a unique name.
It is important that the `meta_type` is `Dexterity FTI`.
The FTI specification is what makes this a Dexterity file type.
The `types/` file name must match the type's name.

Let's take a look at a `types/` XML file.
The `Session` type, in `session.xml`, should look like the following.

```xml
<?xml version="1.0" encoding="UTF-8"?>
<object name="Session" meta_type="Dexterity FTI" i18n:domain="example.conference"
   xmlns:i18n="http://xml.zope.org/namespaces/i18n">
  <property name="title" i18n:translate="">Session</property>
  <property name="description"
    i18n:translate="">Conference Session</property>

  <!-- content-type icon -->
  <property name="icon_expr">string:${portal_url}/document_icon.png</property>

  <!-- factory name; usually the same as type name -->
  <property name="factory">Session</property>

  <!-- URL TALES expression to add an item TTW -->
  <property name="add_view_expr">string:${folder_url}/++add++Session</property>

  <property name="link_target"></property>
  <property name="immediate_view">view</property>

  <!-- Is this item addable globally, or is it restricted? -->
  <property name="global_allow">False</property>

  <!-- If we're a container, should we filter addable content types? -->
  <property name="filter_content_types">True</property>
  <!-- If filtering, what's allowed -->
  <property name="allowed_content_types">
  </property>

  <property name="allow_discussion">False</property>

  <!-- what are our available view methods, and what's the default? -->
  <property name="default_view">view</property>
  <!-- the view methods below will be selectable via the display tab -->
  <property name="view_methods">
    <element value="view"/>
  </property>
  <property name="default_view_fallback">False</property>

  <!-- permission required to add an item of this type -->
  <property name="add_permission">cmf.AddPortalContent</property>

  <!-- Python class for content items of this sort -->
  <property name="klass">plone.dexterity.content.Item</property>

  <!-- Dexterity behaviours for this type -->
  <property name="behaviors">
    <element value="plone.app.content.interfaces.INameFromTitle"/>
  </property>

  <!-- If defined by a schema interface, dotted name of schema class -->
  <property name="schema">example.conference.session.ISession</property>

  <!-- Or, we could have the supermodel XML here in escaped XML -->
  <property name="model_source"></property>

  <!-- Or, we could point to a supermodel XML file -->
  <property name="model_file"></property>

  <!-- Action aliases; rarely changed -->
  <alias from="(Default)" to="(dynamic view)"/>
  <alias from="edit" to="@@edit"/>
  <alias from="sharing" to="@@sharing"/>
  <alias from="view" to="(selected layout)"/>
  <action title="View" action_id="view" category="object" condition_expr=""
    description="" icon_expr="" link_target="" url_expr="string:${object_url}"
    visible="True">
    <permission value="View"/>
  </action>
  <action title="Edit" action_id="edit" category="object" condition_expr=""
    description="" icon_expr="" link_target=""
    url_expr="string:${object_url}/edit" visible="True">
    <permission value="Modify portal content"/>
  </action>
</object>
```

Note that the `icon_expr` and `global_allow` declarations have changed from the original.

There is a fair amount of boilerplate here which could actually be omitted, because the Dexterity FTI defaults will take care of most of this.
However, it is useful to see the options available so that you know what you can change.

The important lines here are:

-   The `name` attribute on the root element must match the name in `types.xml` and the filename.
-   We use the package name as the translation domain again, via `i18n:domain`.
-   We set a title and description for the type
-   We specify an icon.
    Here, we use a standard icon from Plone's `plone_images` skin layer.
    You'll learn more about static resources later.
-   We set `global_allow` to `False`, since these objects should only be addable inside a `Program`.
-   The schema interface is referenced by the `schema` property.
-   The `klass` property designates the base class of the content type.
    Use `plone.dexterity.content.Item` or `plone.dexterity.content.Container` for a basic Dexterity `Item` (non-container) or `Container` for a type that acts like a folder.
    You may also use your own class declarations if you wish to add class members or methods.
    These are usually derived from `Item` or `Container`.
-   We specify the name of an add permission.
    The default `cmf.AddPortalContent` should be used unless you configure a custom permission.
    Custom permissions are convered later in this manual.
-   We add a behavior.
    Behaviors are reusable aspects providing semantics or schema fields.
    Here we add the `INameFromTitle` behavior, which will give our content object a readable ID based on the `title` property.
    We'll cover other behaviors later.

The `Program`, in `program.xml`, looks like the following.

```xml
<?xml version="1.0"?>
<object name="example.conference.program" meta_type="Dexterity FTI"
    xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="example.conference">

  <!-- ... -->

  <property name="title" i18n:translate="">Program</property>
  <property name="description" i18n:translate="">Conference Program</property>
  <property name="icon_expr">string:${portal_url}/folder_icon.png</property>
  <property name="factory">Program</property>
  <property name="global_allow">True</property>

  <!-- This is a container that holds only sessions -->
  <property name="filter_content_types">True</property>
  <property name="allowed_content_types">
    <element value="Session" />
  </property>

  <!-- schema and class used for content items -->
  <property name="schema">example.conference.program.IProgram</property>
  <property name="klass">plone.dexterity.content.Container</property>

  <!-- ... -->

</object>
```

We've edited this one a little from the boilplate.
The difference here is that we make this a `Container`, and filter the containable types (`filter_content_types` and `allowed_content_types`) to allow only `Sessions` to be added inside this folder.


## Testing the type

This section describes how to start up Plone and test the type.
It also provides some trouble-shooting tips.

With a schema and FTI for each type, and our `GenericSetup` profile registered in `configure.zcml`, we should be able to test our type.
Make sure that you have run buildout, and then start `./bin/instance fg` as normal.
Add a Plone site, and go to the {guilabel}`Add-ons` control panel.
You should see your package there, and be able to install it.

Once installed, you should be able to add objects of the new content types.

If Zope doesn't start up:

-   Look for error messages on the console, and make sure you start in the foreground with `./bin/instance fg`.
    You could have a syntax error or a ZCML error.

If you don't see your package in the {guilabel}`Add-ons` control panel:

-   Ensure that the package is either checked out by `mr.developer`, or that you have a `develop` line in `buildout.cfg` to load it as a development egg.
    `develop = src/*` should suffice, but you can also add the package explicitly, for example with `develop = src/example.conference`.
-   Ensure that the package is actually loaded as an egg.
    It should be referenced in the `eggs` section under `[instance]`.
-   You can check that the package is correctly configured in the buildout by looking at the generated `bin/instance` script (`bin\instance-script.py` on Windows).
    There should be a line for your package in the list of eggs at the top of the file.
-   Make sure that the package's ZCML is loaded.
    You can do this by installing a ZCML slug (via the `zcml` option in the `[instance]` section of `buildout.cfg`), or by adding an `<include />` line in another package's `configure.zcml`.
    However, the easiest way with Plone 3.3 and later is to add the `z3c.autoinclude.plugin` entry point to `setup.py`.
-   Ensure that you have added a `<genericsetup:registerProfile />` stanza to `configure.zcml`.

If the package fails to install in the {guilabel}`Add-ons` control panel:

-   Look for errors in the `error_log` at the root of the Plone site, in your console, or in your log files.
-   Check the syntax and placement of the profile files.
    Remember that you need a `types.xml` listing your types, and corresponding files in `types/*.xml`.

If your forms do not look right, for example custom widgets are missing, then:

-   Make sure your schema derives from `model.Schema`.
-   Remember that the directives require you to specify the correct field name, even if they are placed before or after the relevant field.
