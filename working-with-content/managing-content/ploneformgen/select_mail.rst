================================================
Using a selection field to pick mail destination
================================================

.. admonition :: Description

    You may allow form users to use a selection field to choose a destination address for their form input.

        I'm trying to use a PloneFormGen form as a support center for my project and I would like to have the mail sent to different email addresses based on a choice from a selection field.

        How can I do it?

The form
========

First, create a selection field in your form

In the Options field, specify your set of possible destination addresses in a "value|label" format where the e-mail address is the value and its readable name the label. For example::

    softwarehelp@example.org|Software Support Desk
    hardwarehelp@example.org|Hardware Support Desk

Then, pick the address (the actual e-mail address value,  not the label) you wish selected by default. Put it in the Default field. Make sure the Required checkbox is selected.

Save the form field.

Configuring the mailer
======================

Now, edit the mail adapter for your form. (Navigate to the form folder, click on contents, find your mail adapter and follow the link; select the edit tab.)

Choose the `[addressing]` sub-form and find the Extract Recipient From field. You should see a None choice and a list of all of the selection fields in your form. Select the field you just created and save your changes.