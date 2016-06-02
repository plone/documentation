================================================
Custom mailer script
================================================

.. admonition :: Description

    Customizing email output from PloneFormGen

Introduction
------------

Below is an email script example to customize how PloneFormGen generates the email output.

Installation instructions
---------------------------

Go to form, on the contents tab remove the existing Mailer item.

Choose create new... Custom script adapter. Pick any name.

For the script, set Proxy role: Manager.

Fix the email addresses in the script below.

Paste the code to the script body field.

Save.

Test.

Example script
----------------

::

    from Products.CMFCore.utils import getToolByName

    mailhost = getToolByName(ploneformgen, 'MailHost')

    subject = "Email subject"

    # Use this logger to output debug info from this script if needed
    import logging
    logger = logging.getLogger("mailer-logger")


    # Create a message body by appending all the fields after each another
    # This includes non-functional fields like labels too
    message=""
    for field in ploneformgen.fgFields():
       label = field.widget.label.encode("utf-8")
       value = str(fields[field.getName()])

       # For non-functional fields draw a custom separator line
       if not field.widget.blurrable:
            value = "-------------------------------"

       # Format lists on the same row
       try:
          if (value[0] == "["):
             value = value.replace("'", "")[1:-1]
       except IndexError:
          # Skip formatting on error
          pass

       #remove last ':' from label
       if (label[-1] == ":"):
          label = label[0:-1]

       message += label + ": " + value + "\n\n"


    source = "noreply@example.com"
    receipt = "info@example.com"

    mailhost.send(message, receipt, source, subject=subject, charset="utf-8", )
