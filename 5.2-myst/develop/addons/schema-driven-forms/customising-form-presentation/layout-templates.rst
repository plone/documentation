=================
Layout templates
=================

**Creating a custom layout for our form**

To this point, we have relied on Plone (in fact, *plone.app.z3cform*) to supply
a default template for our forms. This uses the default Plone form
markup, which is consistent with that used in other forms in Plone. For
many forms, this is all we need. However, it is sometimes useful to
create a custom template.

Custom templates are normally needed for one of two reasons: Either, to
insert some additional markup around or inside the form itself; or to
radically change the form markup itself. The former is more common,
since changing the form look-and-feel is normally done better with CSS.
For that reason, *plone.app.z3cform* registers a view called
*@@ploneform-macros*, which provides useful macros for rendering forms
using the standard markup. We will illustrate how to use this below.

The easiest way to associate a template with a form is to use the
default grokked template association. Our form is called *OrderForm* and
lives a module called *order.py*, so the grokker will look for a
template in *order\_templates/orderform.pt*.

.. note::
    With the exception of *DisplayForms*, there is always a default template
    for forms extending the grokked base classes in *plone.directives.form*.
    Therefore, the template is optional. Unlike *grok.View* views, there is
    no need to override *render()* if the template is omitted.

As an example, let’s create such a template and add some content before
the form tag:

::

    <html xmlns="http://www.w3.org/1999/xhtml"
          xmlns:metal="http://xml.zope.org/namespaces/metal"
          xmlns:tal="http://xml.zope.org/namespaces/tal"
          xmlns:i18n="http://xml.zope.org/namespaces/i18n"
          i18n:domain="example.dexterityforms"
          metal:use-macro="context/main_template/macros/master">

        <metal:block fill-slot="main">

            <h1 class="documentFirstHeading" tal:content="view/label | nothing" />

            <p>Welcome to Backgammon Pizza! We hope you enjoy our food.</p>

            <div id="content-core">
                <metal:block use-macro="context/@@ploneform-macros/titlelessform" />
            </div>

        </metal:block>

    </html>

Notice how the *@@ploneform-macros* view does most of the work. This
contains a number of useful macros:

-  *form* is a full page form, including the label
-  *titlelessform* includes the form *status* at the top, the *<form />*
   element, and the contents of the *fields* and *actions* macros. It
   also defines three slots: *formtop*, just inside the *<form>* opening
   tag; *formbottom*, just before the *</form>* closing tag; and
   *beforeactions*, just before the form actions (buttons) are output.
-  *fields* iterates over all widgets in the form and renders each,
   using the contents of the *field* macro.
-  *field* renders a single field. It expects the variable *widget* to
   be defined in the TAL scope, referring to a *z3c.form* widget
   instance. It will output an error message if there is a field
   validation error, a label, a marker to say whether the field is
   required, the field description, and the widget itself (normally just
   an *<input />* element).
-  *actions* renders all actions on the form. This normally results in a
   row of *<input type=“submit” … />* elements.

.. note::
    If you require more control, you can always create your form from
    scratch. Take a look at *macros.pt* in *plone.app.z3cform* for
    inspiration.

If you don’t require tabbed fieldsets or “inline” field validation, the
template can be simplified substantially. See *macros.pt* in
*plone.z3cform* for a cleaner example.

The most important variables used in the template are:

-  *view.id*, a unique id for the form
-  *view.enctype*, the form’s *enctype* attribute
-  *view.label*, the form’s title
-  *view.description*, the forms’ description
-  *view.status*, a status message that is often set in action handlers.
-  *view.groups,* a list of fieldsets (groups), as represented by
   *Group* instances.
-  *view.widgets*, which contains all widgets. *view.widgets.errors*
   contains a list of error snippet views. Otherwise, *widgets* behaves
   like an ordered dictionary. Iterating over its *values()* will yield
   all widgets in order. The widgets have been updated, and can be
   output using their *render()* method.
-  *view.actions,* contains an ordered dictionary of actions (buttons).
   Iterating over its *values()* will yield all actions in order. The
   actions have been updated, and can be output using their *render()*
   method.
