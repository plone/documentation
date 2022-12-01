==========================
Frequently Asked Questions
==========================


Q. How can I make a date/time field default to current time?
============================================================

In the field's "overrides" fieldset, specify as Default Expression::

    python:DateTime()

Note that you may do some simple date arithmetic. To set the default a week after server time, use::

    python:DateTime() + 7


Q. I've made an error in a TALES expression, and now I can't view or edit my form!
==================================================================================

An error in a TALES override may prevent you from viewing the form, but it shouldn't stop you from editing it.

To edit, navigate to the form (you'll see your error).

* If the error is in a form override, add "/atct_edit" to the end of the URL to reach the editor. That will allow you to reach the form editor; now go to the overrides fieldset and fix the problem.
* If the error is in a field override, add "/folder_contents" to the end of the URL to reach the folder contents. Click on the troubled field; you'll again get an error. Now, add "/atct_edit" to the end of the URL to reach the editor.

Q. How do I make a field default to the member's name/address/id?
=================================================================

In the field's override fieldset, set the Default Expression to::

    here/memberEmail

memberEmail is a method of the form folder which will return a member's e-mail address, if one is available, and an empty string otherwise.

You may also use "here/memberFullName" to get the member's name, and "here/memberId" to get the login id.

.. note::

    memberEmail, memberFullName and memberId are a convenience facility of PloneFormGen. They are not part of the Plone API.

Q. Where is the encryption option?
==================================

I understood PFG could GPG encrypt mail, but can't find the option to do it.

Navigate to your mail adapter and edit it. Look in the fieldset list (the list of bracketed sub-forms at the top of the form).
Do you see an encryption field set title? If so, you've found the option. If not, it means that PFG was unable to find the gpg binary when it started. Read the README_GPG.txt file in the PFG product folder for details on how to solve this problem.

Don't forget that after you install GnuPG, you'll need to restart Zope or refresh your PFG product.
Where is the save-data adapter?

Q. I've added a form folder, and the action adapter list includes "None" and "Mailer". Where is the save-data adapter?
======================================================================================================================

You need to add it to the folder via the add-item drop-down.

A mailer adapter is in the "sample" form created when you add a form folder because it's probably the most common use. Other adapters need to be added.

Q. Why are these action adapters content types? Why aren't they built into the form folder?
===========================================================================================

There are several reasons. One is that doing it this way makes it easy to copy configured action adapters from one form to another.

Q. When I attempt to submit a form, I get an AssertionError "You must specify a recipient e-mail address in the mail adapter."
==============================================================================================================================

The error is occurring because PloneFormGen doesn't have a recipient address to which to mail the form input.

To fix this, choose the contents tab of your PFG form folder. Navigate to the mailer and use its edit tab. Choose the "addressing" fieldset and specify a recipient address.

By the way, if the recipient address isn't specified, PFG tries to use the e-mail address of the form folder's owner. You'll see this error if you've failed to set an e-mail address in personal preferences.

PloneFormGen missing from Add list?
===================================

I installed the release of PloneFormGen in my Products directory in Plone 2.5.x, and neither the Management Interface (/Control_Panel/Products) nor Plone (Quick Installer) seemed to recognize it after restarting my Zope.

Zope has probably encountered an error in the course of loading the product.

Try checking your event.log for related error messages. You may wish to try starting Zope in foreground mode (bin/zopectl fg for a standalone zope) for more diagnostics.

How do I add a hidden field with the username?
==============================================

Create a string field and mark it hidden.

On the overrides tab, set "here/memberId" for the Default Expression.

.. note::

    To follow this recipe, you'll need to have permission to edit TALES fields.

Q. Dynamically populate selection fields?
=========================================

Can I dynamically populate selection and/or multi-selection fields in PloneFormGen?

Yes, use the [overrides] panel of the field's edit view to set an Options Vocabulary.

It should be a TALES expression that evaluates as a list of value/label lists (tuples are also OK).

For example, let's say that we wanted a selection field populated with option values '1', '2', '3', '4' and matching visible labels 'one', 'two', three', 'four'. The TALES code for this would be::

    python: (('1','one'), ('2','two'), ('3','three'), ('4','four'))

It's unlikely, though, that you'll be able to do what you need in a single line of TALES. A more typical use would be to create a python script that returns a sequence of value/label sequences. If you put that script in your form folder, you can fill in::

    here/myscriptid

in your Options Vocabulary field.

Q. Could a selection field in a FormFolder be used to redirect?
===============================================================

I have created a custom FormFolder, using PloneFormGen. Within the FormFolder, I have created a page and added a selection field with value/label pairs equivalent to: path (url) | company department --> i.e. http://my.site/reports/accounting|Accounting I am wondering if it is possible to create an action override that would 'redirect_to' the 'selected' value in the selection field, something like: 'redirect_to:string: ' If so, how might I access the value from the selection field?

For the redirection, just put something like::

    redirect_to: request/form/my-selection-field

in the Custom Success Action field on the form folder's [override] panel.

If you need to do something more complicated, you can use the "Custom
Script Adapter" in the 1.1 alpha and end your code with::

    request.response.redirect(request.form['my-selection-field'])

Use a "From" address other than the site address?
=================================================

One stock-field is called replyto and contains a valid email address. I want this address to be in the From: line - not just in Reply-To:. I could fill in a TALES expression to overwrite the default sender-address. But what's the correct TALES expression for that?

By default, PloneFormGen's mailer sends mail with the "From" address set to the site's global "From" address (specified in site setup / Portal Settings). That's the standard return address for portal-generated mail, but you may wish to use another.

In the mailer's overrides sub-form, set the Sender Expression to::

    request/form/replyto

to use the address filled in for the "replyto" form field.

You could also specify a literal::

    string:test@mysite.org

Be cautious about using user-submitted addresses for the "From" address. It's important that the "From" address be a real one, owned by a responsible person.

Q. Can I integrate my favorite field/widget?
============================================

I'd like to integrate a new field/widget into PloneFormGen so that it will be useful as a form field in a PFG form.

PFG is designed to allow this, but it's going to take some programming by you or the field developer. See the PFG "examples" directory for a heavily commented, really working, example of integrating a third-party field into PloneFormGen without touching the PFG or field code.


Q. Captcha field is not accessible?
===================================

Or, not always readable for some people with low vision, or when using mobile phones this type of control is strongly blocking

To effectively replace a Captcha, just add a mandatory text field (must match the size of two chars. max.) That can be called e.g. 'Filter' as help text with the following question: "to avoid spam can you answer this question: 7+2-1 = ?

Next, modify the object and choose the menu 'overrides' and fill in the "custom validator" by this expression::

    python: value != '8' and 'the answer is false'
