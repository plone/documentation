======================
Validator Reference
======================

.. admonition:: Description

	A quick reference to the built-in Archetypes validators.

Using Validators
----------------

Archetypes fields may have validators specified in the Field schema. For
example, the schema for the basic page type includes the stanza:

::

    ATDocumentSchema = ATContentTypeSchema.copy() + Schema((
        TextField('text',
    ...
                  validators = ('isTidyHtmlWithCleanup',),
    ...
        ),

This specifies that the *isTidyHtmlWithCleanup* test will be applied to
validate form input.

You may specify a sequence of validators:

::

    validators = ('isMaxSize', 'isTidyHtmlWithCleanup',),

and the validators will tested in order.

The validators sequence may contain two kinds of entries:

-  The string names of validators registered with the validation service
   (see Products.validation);
-  Instances of classes implementing the IValidator interface
   (Products.validation.interfaces.IValidator.IValidator).

A validation specification using a validator class instance can look
like:

::

    validators = ( ExpressionValidator('python: int(value) == 5'), )

 

Registered Validators
---------------------

These are validators pre-registered with the validation service. They
may be specified by name.