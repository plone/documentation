Adding validation
=================

.. admonition:: Description

    Server-side form validation is vital to ensure data sanity and protect
    our site from malicious users.

Field validation
~~~~~~~~~~~~~~~~

Once you've understood the "hello form", let's move onto a more advanced
topic: validation.

The easiest way to manage validation in a formlib-based form is to
specify the validation rules in our schema. Actually, you've already
implemented some validation: the customer, subject and message fields
are required. If you leave the *subject* field empty, for example, and
click the *send* button, a pretty red error message will show up asking
you to fill that field.

Let's add email validation to the *customer* field using the constraint
keyword argument fot that attribute in our schema. For simplicity, the
mail address checker that comes with the CMFDefault utilities toolbox
will be used in this example, althought you could also use your own
regular expression checking. The constraint argument must be a callable
that returns ``True`` if the value submitted is valid, or raise an
exception inheriting from ``zope.schema.ValidationError``, whose
docstring will be used in the error message.

::

    from zope.schema import ValidationError

        class InvalidEmailAddress(ValidationError):
        "Invalid email address"

        from Products.CMFDefault.utils import checkEmailAddress
        from Products.CMFDefault.exceptions import EmailAddressInvalid

        def validateaddress(value):
        try:
        checkEmailAddress(value)
        except EmailAddressInvalid:
        raise InvalidEmailAddress(value)
        return True

    class IFeedbackForm(Interface):
        """
        A typical feedback schema
        """
        customer = TextLine(title=u'Customer',
                          description=u'Customer email',
                          required=True,
                          constraint=validateaddress)

        subject = TextLine(title=u'Subject',
                           required=True)

        message = Text(title=u'Message',
                       description=u'The message body',
                       required=True)

Now, if you type an invalid address into the *customer* field and click
*send*, a kind and colorful error message will be displayed:

.. figure:: /develop/plone/images/formlib_validation_error_pretty.png
   :align: center
   :alt: Simple validation error

That was too easy, wasn't it? 

Invariants validation
~~~~~~~~~~~~~~~~~~~~~

*zope.formlib* also supports the validation of schema invariants, e.g.
the min value entered must be smaller than the max value. In this
example the form will be extended to provide a set of predefined
subjects and a field named *other* which must be filled when selecting
the the *Other* option in the subject select dropdown. It's easier to
explain it in Python than in English:

::

    from zope.schema import Choice
    from zope.interface import invariant, Invalid

    class IFeedbackForm(Interface):
        """
        A typical feedback schema
        """
        customer = TextLine(title=u'Customer',
                          description=u'Customer email',
                          required=True,
                          constraint=validateaddress)

        subject = Choice(title=u'Subject',
                       vocabulary='Available Subjects',
                       required=True,
                       )

        other = TextLine(title=u'Other',
        description=u"""
        If you've specified Other above,
        please fill this this field too.""",
        required=False)

        message = Text(title=u'Message',
                       description=u'The message body',
                       required=True)

        @invariant
        def otherFilledIfSelected(feedback):
        if feedback.subject == u'Other' and not feedback.other:
        raise Invalid("Please specify the motivation of your request")

Here, the *subject* field type has been set to *Choice*, and the list of
available values has been indicated to be obtained from the *Available
Subjects* vocabulary, a named utility which will be defined shortly.

The form will call all the *invariant*-decorated functions of the schema
upon validation and catch any raised *Invalid* exceptions.

You still need to define the *Available Subjects* vocabulary:

::

    from zope.schema.vocabulary import SimpleVocabulary

    def availableSubjects(context):
        subjects = ('Comment',
                    'Feature Request',
                    'Technical Issue',
                    'Complaint',
                    'Other',
                    )
        return SimpleVocabulary.fromValues(subjects)

and register it as a named utility using ZCML in the ``configure.zcml``
file:

::

    <configure ... >
    ...
        <utility
                component=".browser.availableSubjects"
                name="Available Subjects"
                provides="zope.schema.interfaces.IVocabularyFactory"
                />
    </configure>

Restart your Zope instance for the changes to take effect and test your
new form. You'll see something similar to this:

.. figure:: /develop/plone/images/formlib_invariant_error.png
   :align: center
   :alt: Invariant error

Unfortunately, invariant errors descriptions are not shown in the
default template.
