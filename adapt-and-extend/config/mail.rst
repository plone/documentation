Mail Configuration
==================

.. figure:: ../../_robot/mail-setup.png
   :align: center
   :alt: Mail setup configuration


Completing this configuration allows your Plone site to send email.
If the mail settings are not configured properly, you will not be able to receive form submissions via email from your site, and users can't be contacted for an email reset link.

Using localhost for email
-------------------------

One common way to configure mail for your Plone site is to use a mail server on the same machine that is hosting Plone.
To do this, you'll first need to configure a mail server, like `Postfix <http://www.postfix.org/BASIC_CONFIGURATION_README.html>`_.

| **SMTP Server:** localhost
| **SMTP Port:** 25
| **ESMTP Username:** Leave this blank
| **ESMTP Password:** Leave this blank
| **Site 'From' Name:** [This will appear as the "From" address name]
| **Site 'From' Address:** [emailaddress]@[yourdomain]

Using an external host
----------------------

The following settings are an example of how you can configure your site to use your Gmail address.
You can also use any external mail server, such as your business or institution email (you can get your SMTP settings from your in-house IT department).

| **SMTP Server:** smtp.gmail.com
| **SMTP Port:** 587
| **ESMTP Username:** [username]@gmail.com
| **ESMTP Password:** [Your Gmail Password]
| **Site 'From' Name:** [This will appear as the "From" address name]
| **Site 'From' Address:** [Your Gmail Address]



Testing the Configuration
-------------------------

You can test the configuration by clicking the "Save and send test e-mail" button at the bottom of the form.
You should receive an email from the email address you specified with the subject "Test email from Plone."
