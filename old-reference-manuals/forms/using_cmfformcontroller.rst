Using CMFFormController
=======================

.. admonition:: Description

    How to create and validate forms in Plone using its CMFFormController.
    Be sure to also read the CMFFormController tutorial in the
    Products/CMFFormController/documentation directory, included with your
    copy of Plone. This how-to is also available in
    Products/CMFFormController/www/ as the file docs.stx, included with Plone.

The CMFFormController package helps developers by simplifying the
process of validating forms. It also makes it easier for site
administrators to override some of the behavior of packages without
modifying code, making it easier to upgrade packages without disturbing
the modifications.

How it works:

-  Developers associate a set of default variables for their Page
   Templates. These variables control the validation that takes place
   after the form is submitted and the actions that occur after
   validation. The variables are stored on the filesystem in the
   .metadata properties file.
-  Site administrators can override the default validations and actions
   using the ZMI. Once a set of validations or actions has been
   specified in the ZMI, the default validations and actions will be
   ignored.

Forms
-----

To take advantage of CMFFormController, you need to use Controller Page
Templates rather than ordinary Page Templates. Controller Page Templates
act just like ordinary Page Templates, but they do some extra work when
they are viewed.

Here is a basic form that uses CMFFormController:

::

         <form tal:define="errors options/state/getErrors"
               tal:attributes="action string:${here/absolute_url}/${template/id};"
              method="post">
            <input type="hidden" name="form.submitted" value="1" />
            <p tal:define="err errors/foo|nothing" tal:condition="err" tal:content="err" />
            <input type="text"
                   name="foo"
                   tal:define="val request/foo|nothing"
                   tal:attributes="value val" />
            <input type="submit" name="submit" value="submit" />
         </form>

Let's take a look.

-  First, we note that the form is set up to submit to itself. *Forms
   must submit to themselves.*
-  Second, we see the special hidden variable ``form.submitted``. The
   controlled page template checks the REQUEST for form.submitted to see
   if the form has been submitted or if, instead, it has just been
   accessed, e.g. via a link. *Forms must contain the hidden variable
   ``form.submitted``*
-  At the beginning of the form we set the variable errors. The errors
   dictionary comes from the state object which is passed in the
   template options. The state object lets validators and scripts pass
   information to each other and to forms. For our purposes, the most
   important information is the errors dictionary, which has entries of
   the form ``{field_name:error_message}``.

Before we can use this form we need to specify the validators that will
be used to check the form values, and we need to specify the action that
will occur after validation.

Specifying Validators
---------------------

There are two basic ways to specify a form's validators.
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

#. You can specify the validators in the .metadata properties for
   filesystem-based Controller Page Templates.
#. You can specify the validators via the ZMI (or programmatically).
   These values will be stored in the ZODB as attributes of the
   ``portal_form_controller`` object.

If you specify validators in both places, the validators specified in
the ZMI will take precedence over those specified in the .metadata file.

Specifying Validators on the Filesystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify validators on the filesystem using an objects .metadata
properties file.

To create a .metadata file, simply create a file with the same name as
your page template, and then append .metadata to the end of the name of
the file. For instance, you might have a Controller Page Template called
``document_edit_form.cpt``. The properties for that file would be stored
in a file called ``document_edit_form.cpt.metadata``

The .metadata file uses the standard python ConfigParser syntax. The
validator section of the .metadata file would look like:

::

            [validators]
            validators = validate_script1, validate_script2

The validation scripts ``validate_script1`` and ``validate_script2``
will be called in order.

Type-Specific Validators
^^^^^^^^^^^^^^^^^^^^^^^^

Suppose you want different validators to be called, depending on the
type of context the form has.

You can do so as follows:

::

             [validators]
             validators = validate_script1
             validators.Document = validate_script2

In the above example, if the context is a Document object,
``validate_script2`` will be called for validation; for everything else,
only ``validate_script1`` will be called.

Note that the order in which the variables are specified does not
matter; the type-specific validators override non-specific validators if
both are applicable.

Button-Specific Validators
^^^^^^^^^^^^^^^^^^^^^^^^^^

Suppose instead that you have two different buttons on your form, and
you want different validation sequences to occur depending on which
button is pressed. You can accomplish this as follows:

First, name your buttons button1 and button2:

::

                <input type="submit"
                       name="form.button.button1"
                       value="First Button" />
                <input type="submit"
                       name="form.button.button2"
                       value="Second Button" />

Next, specify validators in the .metadata file for button1 and for
button2:

::

                [validators]
                validators..button1 = validate_script1, validate_script3
                validators..button2 = validate_script2, validate_script4

Note the presence of the ``..``. This is a placeholder for a type
specifier. You could further specify that ``validate_script5`` is called
if ``button2`` is pressed and the context is a Document by adding:

::

                [validators]
                validators.Document.button2 = validate_script5

Remember that button specific validators take precedence over
non-specific validators.

Specifying Validators in the ZMI
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If you look at a Controller Page Template in the ZMI, you will see that
it looks just like an ordinary Page Template with two extra tabs,
Validation and Actions. Click on the Validation tab.

The Validation tab shows all the validators for the page template in
question. You can specify validators with the same kind of
specialization options as above via a web form.

The validator information for all forms is stored in the
``portal_form_controller`` tool in your portal. This means that you can
specify validators for filesystem objects with no problems, since the
information is persisted in the ZODB. Note that the validator
information is bound to the form's Id, so all forms with the same Id use
the same validators. This keeps things simple when you have multiple
skins:

*Forms with the same Id use the same validators, no matter what skin
they are in.*

When a form is submitted, it first checks to see if there are any
applicable validators that have been specified via the ZMI. If it finds
one, it uses it. If it does not find a validator via the ZMI, it then
checks the REQUEST object to see if validators have been specified in
hidden variables. As a result, validators specified in the ZMI take
precedence over those specified in forms.

Specifying Validators Programmatically
''''''''''''''''''''''''''''''''''''''

The portal's ``portal_form_controller`` tool has methods you can use to
specify the validators for a given ControllerPageTemplate. The API is as
follows:

::

               portal_form_controller.addFormValidators(id,
                                                        context_type,
                                                        button,
                                                        validators)

Here ``id`` is the Id of the ControllerPageTemplate, ``context_type`` is
the class name for the class of the context object, ``button`` is the
name of the button pressed, and validators is a comma-delimited string
or a list of strings. If you want a validator to act for any class, set
context\_type to None. Similarly, you want a validator to act for any
button, set button to None.

Specifying Actions
------------------

The sequence of validators that is executed returns a status in the
state object. The default status is ``success``, i.e. if no validators
are executed, the status will be ``success``. If a validator encounters
an error, it will typically set the status to ``failure``. The next
thing we need to do in your form is to specify what happens when a given
status is returned.

As with validators, there are two basic ways to specify a form's
actions.

#. You can specify the actions in the .metadata properties for
   filesystem-based Controller Page Templates and Controller Python
   Scripts.
#. You can specify the actions via the ZMI (or programmatically). These
   values will be stored in the ZODB as attributes of the
   ``portal_form_controller`` object.

If you specify actions in both places, the actions specified in the ZMI
will take precedence over those specified in the form.

Specifying Actions on the Filesystem
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

You can specify actions on the filesystem using an objects .metadata
properties file.

Actions are stored in the same .metadata file as the validators. The
syntax for the actions section of your file would look like:

::

            [actions]
            action.success = traverse_to:string:script1

In the above example, when the form is submitted and the validation
scripts return a status of ``success``, the ``traverse_to`` action is
called with the argument ``string:script1``, i.e. if the form data is
valid, we run the script ``script1``. Alternatively, we could specify
``action.success = redirect_to:string:http://my_url_here``, which would
cause the browser to be redirected to ``http://my_url_here``.

The default action for the ``failure`` status is to reload the current
form. The form will have access to all the error messages, via the state
object in its options.

Type-Specific Actions
~~~~~~~~~~~~~~~~~~~~~

Suppose you want different actions to occur depending on the type of
context the form has.

You can do so as follows:

::

                   [actions]
                   action.success = traverse_to:string:script1
                   action.success.Document = traverse_to:string:document_script

In the above example, if the context is a Document object,
document\_script will be executed upon successful validation; for
everything else, script1 will be executed. Note that the order in which
the variables are specified does not matter; the type-specific actions
will override non-specific actions if both are applicable.

Button-Specific Actions
~~~~~~~~~~~~~~~~~~~~~~~

Suppose instead that you have two different buttons on your form, and
you want different actions to occur depending on which button is
pressed. You can accomplish this as follows:

First, name your buttons button1 and button2:

::

                <input type="submit"
                       name="form.button.button1"
                       value="First Button" />
                <input type="submit"
                       name="form.button.button2"
                       value="Second Button" />

Next, specify actionss for button1 and for button2:

::

                [actions]
                action.success..button1 = traverse_to:string:script1
                action.success..button2 = traverse_to:string:script2

Note the presence of the ``..``. This is a placeholder for a type
specifier. You could further specify that ``document_script2`` is called
if button2 is pressed and the context is a Document by adding:

::

                [actions]
                action.success.Documnet.button2 = traverse_to:string:document_script2

Specifying Actions in the ZMI
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

If you look at a Controller Page Template in the ZMI, you will see that
it looks just like an ordinary Page Template with two extra tabs,
Validation and Actions. Click on the Actions tab.

The Actions tab shows all the actions for the page template in question.
You can specify actions with the same kind of specialization options as
above via a web form.

The action information for all forms is stored in the
``portal_form_controller`` tool in your portal. This means that you can
specify actions for filesystem objects with no problems, since the
information is persisted in the ZODB. Note that the action information
is bound to the form's Id, so all forms with the same Id use the same
actions. This keeps things simple when you have multiple skins: forms
with the same Id use the same actions, no matter what skin they are in.

When a form is submitted, it first checks to see if there are any
applicable actions that have been specified via the ZMI. If it finds
one, it uses it. If it does not find an action via the ZMI, it then
checks the REQUEST object to see if actions have been specified in
hidden variables. As a result, actions specified in the ZMI take
precedence over those specified in forms.

Specifying Actions Programmatically
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The portal's ``portal_form_controller`` tool has methods you can use to
specify the actions for a given ControllerPageTemplate. The API is as
follows:

::

                portal_form_controller.addFormAction(id,
                                                     status,
                                                     context_type,
                                                     button,
                                                     action_type,
                                                     args)

Here ``id`` is the Id of the ControllerPageTemplate, ``status`` is the
status for which the action will be executed, ``context_type`` is the
class name for the class of the context object, ``button`` is the name
of the button pressed, ``action_type`` is the type of action that will
occur, and ``args`` is a string (typically a TALES expression) that will
be passed to the action. If you want an action to be executed for any
class, set context\_type to None. Similarly, you want an action to be
executed for any button, set button to None.

Validation Scripts
------------------

When writing validation scripts, use Controller Validators instead of
Python Scripts. Controller Validators are just like ordinary Scripts
with the addition of a ZMI Actions tab. On the file system, Controller
Validators use the extension .vpy rather than .py.

Let's take a look at a basic validation script that tests the REQUEST
value ``n`` to see if it is an integer:

::

          n = context.REQUEST.get('n', None)
          if not n:
             state.setError('n', 'Please enter a value', new_status='failure')
          else:
             try:
                int(n)
             except ValueError:
                state.setError('n', 'Please enter an integer',
                               new_status='failure')

          if state.getErrors():
             state.set(portal_status_message='Please correct the errors shown.')
          return state

The first thing to note is that Controller Validators have a built-in
state object called ``state``. This state object (of class
ControllerState) contains basic information about what has happened
during the validation chain.

The state object has a ``status`` attribute which contains the current
validation status. The initial status is ``success``. If errors are
detected by validators, they set the status to something else, typically
``failure``.

The state object also stores errors that have been detected. The
``setError`` method is used to set an error message for a particular
variable. The setError method has the optional ``new_status`` argument
that can be used to both set an error message as well as to update the
status. You can see if an error message has already been stored for a
particular variable by calling ``state.getError(variable_name)``.

The set method lets you set multiple attributes of the state object all
at once, e.g.:

::

          state.set(status='my_new_status')

You can also pass keyword arguments to the state object via the set
method. These arguments will get passed along by the action. The
``traverse_to`` action places these keyword arguments in the REQUEST.
The ``redirect_to`` action adds them to the query string of the URL to
which it is redirecting.

Finally, we return the state object.

Another interesting example is email validation:

::

        from Products.CMFDefault.utils import checkEmailAddress
        from Products.CMFDefault.exceptions import EmailAddressInvalid

        email = context.REQUEST.get('email', None)
        if not email:
            state.setError('email', 'No e-mail address')
        else:
        # Do try-catch here because checkEmailAddress will throw an exception
        # instead of saying "no, not valid".
        try:
            checkEmailAddress(email)
            email_ok = True
        except EmailAddressInvalid:
            email_ok = False
        if not email_ok:
            state.setError('email', 'Invalid e-mail address.')

Scripts
-------

When writing scripts that do some processing after a validated form, you
can use Controller Python Scripts instead of ordinary Python Scripts to
let site managers override their actions via the ZMI. On the file
system, Controller Python Scripts use the extension .cpy rather than
.py. Note that Controller Validators and Controller Python Scripts
differ in signficant ways. Be sure to use the appropriate script type
(Controller Validator or Controller Python Script) and/or the
appropriate file extension (.cpy or .vpy).

Let's take a look at a basic script that sets a context attribute to the
value ``n`` that is passed in via the 'REQUEST':

::

       context.n = context.REQUEST.get('n')

       # Optionally set the default next action (this can be overridden
       # in the ZMI)

       state.setNextAction('redirect_to:string:view')

       # Optionally pass a message to display to the user
       state.setKwargs({'portal_status_message':'You set context.n to %s.' % str(context.n)})
       return state

Note that you will usually want to use the ``traverse_to`` action to
call your script. This will ensure that form variables set in the
REQUEST object are available to your script.

This script sets its action to redirect to the relative url ``view`` for
the current context object. The status has not been set, so it is the
default status, ``success``.

The ``state.setNextAction`` directive above is analogous to having the
following line in your .metadata file:

::

         [actions]
         action.success = redirect_to:string:view

As with the .metadata file, the default action specified in the script
can be overridden via the ZMI. This allows site managers to override
post-script actions without having to customize your code.

Finally, we return the state object.

Validation for Scripts
----------------------

Having separate validation scripts typically means that validation is
moved out of scripts. This simplifies scripts, but means that it is
possible to call them directly with invalid data. We can prevent this
problem by adding validators to scripts. Controller Python Scripts use
the same ZMI and/or .metadata file mechanisms for adding validators as
do Controller Page Templates.

Each time a validator is called, it logs the call in the state object.
Validation is smart enough that if a validator is called by a form, it
will not be called again by the script.

Note that if you associate validators with a script, you will need to
set a sensible ``failure`` status action, since scripts do not set such
an action by default. You may wish to define a different failure status
for failures that occur within your script, e.g. ``script_failure``.
Then you can specify a behavior for failures that occur as a result of
invalid parameters coming in and for failures that occur within the
script.
