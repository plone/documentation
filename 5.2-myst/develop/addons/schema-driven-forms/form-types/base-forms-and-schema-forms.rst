Base forms and schema forms
===========================

**Understanding the two types of forms work with in this manual**

*z3c.form* comes with a few base classes for forms, covering common use
cases including page forms, edit forms, add forms and display forms. In
this manual, we are actually using some intermediary base classes from
*plone.directives.form*, which serve two purposes: they allow the forms
to be “grokked”, for example to associate a page template or register
the form as a view using directives like *grok.context()* and
*grok.name()*; some of them also provide a hook for *schema forms*,
which use form hints supplied in directives (like *form.widget()* as we
saw in the previous section) that are interpreted by *plone.autoform* to
configure the form’s fields. Whilst we can do everything in code using
the plain *z3c.form* API, many people may prefer the more declarative
style of configuration that comes with *plone.autoform* and
*plone.directives.form*, because it involves less code and keeps the
field-specific form configuration closer to the field definitions.

Over the next several sections, we will discuss the various form base
classes. A brief overview follows.

**z3c.form.form.BaseForm**
    This base class is not to be used directly, but is the ancestor of
    all *z3c.form* forms. It defines attributes like *label* (the form’s
    title), *mode* (the default mode for the form’s fields, usually
    *‘input’* in regular forms and *‘display’* in display forms),
    *ignoreContext*, *ignoreRequest* (see below) and
    *ignoreReadonly* (which omits readonly fields from the form). It
    also defines the basic *update()* and *render()* methods that are
    the basis of the form rendering cycle, which we will explain towards
    the end of this manual, and the *getContent()* helper method which
    can be used to tell the form about an alternative context - see
    below.
**plone.directives.form.Form (extending z3c.form.form.Form)**
    A basic full-page form. It supports actions (buttons), and will by
    default read field values from the request (unless *ignoreRequest*
    is *True*) or the context (unless *ignoreContext* is *True*).
**plone.directives.form.SchemaForm**
    This is identical to *Form*, except that it will construct its fields
    *plone.autoform* schema hints. The *schema* attribute is required,
    and must be a schema interface. The *additional\_schemata* attribute
    may be set to a tuple of additional schemata - see below.
**plone.directives.form.AddForm (extending z3c.form.form.AddForm)**
    A basic content add form with two actions - save and cancel. This
    implements default Plone semantics for adding content. Note that if
    you are using Dexterity, you should use the Dexterity add form
    instead. See the Dexterity documentation for details.
**plone.directives.form.SchemaAddForm**
    The schema form equivalent of *AddForm*.
**plone.directives.form.EditForm**
    A basic edit form with two actions - save and cancel. This operates
    on the context returned by the *getContent()* helper method. By
    default, that’s the context of the form view (*self.context*), but
    we can override *getContent()* to operate on something else. In
    particular, it is possible to operate on a dictionary. See the
    section on edit forms shortly. Note that if you are using Dexterity,
    you should use the Dexterity edit form instead. See the Dexterity
    documentation for details.
**plone.directives.form.SchemaEditForm**
    The schema form equivalent of *EditForm*.
**plone.directives.dexterity.DisplayForm**
    This is a display form view based on the *WidgetsView* base class
    from *plone.autoform*. You can use this much like *grok.View*,
    except that it must be initialised with a *schema*, and optionally a
    tuple of *additional\_schemata*. There are several helper variables
    set during the *update()* cycle which provide easy access to the
    form’s widgets in display mode.

Context and request
-------------------

When a form is first rendered, it will attempt to fill fields based on
the following rules:

-  If *ignoreRequest* is *False* (as is the default for all forms bar
   display forms), and a value corresponding to the field is in the
   request, this will be used. This normally means that the form was
   submitted, but that some validation failed, sending the user back to
   the form to correct their mistake.
-  If no request value was found and *ignoreContext* is *False* (as is
   the default for all forms bar add forms), the form will look for an
   associated interface for each widget. This is normally the schema
   interface of the field that the widget is rendering. It will then
   attempt to adapt the context to that interface (if the context
   provides the interface directly, as is often the case for edit and
   display forms, the context is used as-is). If no such adapter exists,
   form setup will fail. If this happens, you can either set
   *ignoreContext = True* (which is normally appropriate for
   free-standing forms like the examples earlier in this manual), supply
   an adapter (which is normally appropriate for forms that edit some
   aspect of the context), or override *getContent()* to return a
   content that is adaptable to the schema interface.
-  If no request or context value was found and the field has a default
   value, this will be used.

Primary and additional schemata in schema forms
-----------------------------------------------

When using a schema form, it is possible to set two form properties
supplying schemata for the form:

-  *schema* is required for all schema forms, and must point to a schema
   interface. This is known as the default or primary schema for the
   form.
-  *additional\_schemata* is optional, and can be set to a tuple or list
   of schema interfaces. These will also be included in the form.

.. note::
    If you want to make the schema dynamic, you can implement these as
    read-only properties. this is how Dexterity’s add and edit forms work,
    for example - they look up the primary schema from the type information
    in *portal\_types*, and additional schemata from behaviours.

Later in this manual, we will learn about creating tabbed fieldsets,
also known as groups. The schema forms support a property *autoGroups*
which default to *False*. When set to *True*, the primary schema will be
used as the primary fieldset, and each schema in *additional\_schemata*
will become its own fieldset. The schema name will become the fieldset
name, and its docstring will become its description. This is somewhat inflexible,
but can be useful for certain forms where the fieldsets need to be dynamically looked up.


