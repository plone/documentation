Fail-safe email sending
-------------------------

By default if SMTP server rejects the message sent by PloneFormGen
the page will crash with an exception. Possible reasons for SMTP failure are

* SMTP server is down

* SMTP server is overloaded

* SMTP server spam protection is giving false positives for your email sending attempts

If you have a situation where gathering the data is critical,
the following process is appropriate:

* Use save data adapter to save results

* Use a custom email sender script adapter to send email and even if this
  step fails then the data is saved and no exception is given to the user

Example PloneFormGen script adapter (using proxy role Manager)::


    # -*- coding: utf-8 -*-
    from Products.CMFCore.utils import getToolByName

    # This script will send email to several recipients
    # each written down to its own email field
    # whose id starts with "email-"
    emails = []

    for key in fields:
      if key.startswith('email-'):
        if fields[key] != '':
          emails.append(fields[key])


    mailhost = getToolByName(ploneformgen, 'MailHost')

    subject = "Huuhaa"

    # Custom message with a name filled in
    message = u"""Hello,

    Thanks for participating %s !
    Cheers,
    http://www.opensourcehacker.com
    """ % (fields['etunimi'])

    source = "info@opensourcehacker.com"

    for email in emails:
      try:
        mailhost.send(message, email, source, subject=subject, charset="utf-8", )
      except Exception:
        pass
