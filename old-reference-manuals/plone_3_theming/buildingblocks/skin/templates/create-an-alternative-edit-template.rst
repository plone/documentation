Create an Alternative Edit Template
===================================

Suppose you've a content type and you want to keep the default "edit"
template, but you want also to create another edit template suited for
editing only some particular metadata.

Think of the standard edit as a "full" edit, while your new edit is a
custom version. They co-exist together. This method also works if you've
already a mycustomtype\_edit edit template, and you want to have another
one.

Limiting the Fields Available to Edit
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Step 1: Copy the base\_edit and the edit\_macros (you can do it by
simply customizing them) and change their id (rename) to mynewedit and
mynewmacros

Step 2: Modify mwynewedit to point to mynewmacros:

-  edit\_template python:'newemacros';
-  edit\_macros python:path('here/newemacros/macros \| nothing');

so this edit template will pick up the macros from your custom version.

Step 3: Modify mynewmacros as you need. For example, if you want to
display only some fields, you can (in<metal:block define-slot="widgets">
which manages widgets display) change the template as below:

::

    <tal:fields repeat="field 
    python:schematas[fieldset].editableFields(here, visible_only=True)">

       <div tal:omit-tag="" 
             tal:condition="python:field.getName() 
             in ['title','myfield1','myfield2','myfield3','myfield4']">

           <metal:fieldMacro use-macro="python:here.widget(field.getName(),
            mode='edit')" />

         </div>

    </tal:fields>

So only 'title','myfield1','myfield2','myfield3','myfield4' will be
displayed and you will avoid people editing unwanted fields (even if
they can).

Step 4: If there's a failure, the user should go back to your form, so
in mynewedit -> actions, change failure from string:edit to
string:mynewedit 

Dealing with Validation
~~~~~~~~~~~~~~~~~~~~~~~

Suppose you've some validated fields, or you want to run custom code
when the user saves the form. The validation will kick in when you'll
press "save". If you've some required fields, but they're not in the
fields listed above, you'll get the red warning and your data will not
be saved. So you have to bypass it, and we need to do it in two places:

Step 1:

-  edit mwynewedit -> validation -> delete the validation step.
-  edit mwynewedit -> actions -> change string:content\_edit to
   string:mycontent\_edit (a custom content edit)

Step 2:

-  Find content\_edit in portal\_skins/archetypes and customize it. Then
   rename it to mycontent\_edit. Here you can add custom code, sending
   mail and so on.
-  Edit it -> actions -> delete the validate\_integrity step
-  Edit it -> actions -> change any string:edit to string:mynewedit , so
   after saving you'll go to your edit form if there are any failures
   (should not if you remove the validation)

Now your form can edit your content type without any restrictions. If
you need some restrictions, just don't delete the validation steps above
and customize the validation scripts validate\_base and
validate\_integrity (renaming them and pointing to them in the
validation steps above).

This is enough to perform your "very" own custom edit, with custom
saving and custom validation, leaving the default one untouched.
