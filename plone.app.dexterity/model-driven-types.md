---
myst:
  html_meta:
    "description": "Model-driven types"
    "property=og:description": "Model-driven types"
    "property=og:title": "Model-driven types"
    "keywords": "Plone, model, content types"
---

# Model-driven types

In the previous section, we defined two types by using Zope schema.
In this section, we're going to define a type's fields using an XML model file.

The advantage of using a model file is that we can prototype the content type in Dexterity's through-the-web field editor, then export the XML model file for incorporation into our package.

XML may be used to do pretty much anything you could do via Zope schema.
Many users not already schooled in Zope schema will find this by far the easiest and fastest way to create Dexterity content types.


## Setting the field model

Create an `example/conference/models` directory.
In it, add a `presenter.xml` file with the following content.

```xml
<model xmlns:form="http://namespaces.plone.org/supermodel/form"
       xmlns:security="http://namespaces.plone.org/supermodel/security"
       xmlns="http://namespaces.plone.org/supermodel/schema">
  <schema>
    <field name="name" type="zope.schema.TextLine">
      <description/>
      <title>Name</title>
    </field>
    <field name="description" type="zope.schema.Text">
      <description/>
      <title>A short summary</title>
    </field>
    <field name="bio" type="plone.app.textfield.RichText">
      <description/>
      <required>False</required>
      <title>Bio</title>
    </field>
    <field name="photo" type="plone.namedfile.field.NamedBlobImage">
      <description>Please upload an image.</description>
      <required>False</required>
      <title>Photo</title>
    </field>
  </schema>
</model>
```

The XML name spaces we use are described in the {doc}`reference/dexterity-xml` reference chapter.

Open {file}`presenter.py` that we created in the previous chapter, which is a copy of our original {file}`program.py`.
Delete the field declarations from the `IPresenter` class, and edit as shown below:

```python
from example.conference import MessageFactory as _
from plone.supermodel import model
from zope import schema


class IPresenter(model.Schema):
    """Schema for Conference Presenter content type."""

    model.load("models/presenter.xml")
```

Note the `model.load` directive.
This will automatically load our model file to provide the content type field schema.


## Setting factory type information

This part of the process is identical to what we explained in {doc}`schema-driven-types`.

Look in the {file}`types.xml` file in your package's `example/conference/profiles/default` directory.
It should now contain the following code.

```xml
<object name="portal_types">
  <object name="Program" meta_type="Dexterity FTI" />
  <object name="Session" meta_type="Dexterity FTI" />
  <object name="Presenter" meta_type="Dexterity FTI" />
</object>
```

For the `Presenter` type, we have `example.conference.presenter.xml`.

```xml
<?xml version="1.0"?>
<object name="example.conference.presenter" meta_type="Dexterity FTI"
     xmlns:i18n="http://xml.zope.org/namespaces/i18n"
    i18n:domain="example.conference">

  <!-- Basic metadata -->
  <property name="title" i18n:translate="">Presenter</property>
  <property name="description" i18n:translate="">Conference Presenter</property>
  <property name="icon_expr">string:file-earmark-text</property>
  <property name="factory">Presenter</property>
  <property name="global_allow">True</property>
  <property name="filter_content_types">True</property>
  <property name="allowed_content_types" />
  <property name="allow_discussion">False</property>

  <!-- schema and class used for content items -->
  <property name="schema">example.conference.presenter.IPresenter</property>
  <property name="klass">plone.dexterity.content.Item</property>

  <!-- ... -->

</object>
```

Note that this is may be added anywhere.
