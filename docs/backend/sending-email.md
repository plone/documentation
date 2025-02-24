---
myst:
  html_meta:
    "description": "Guide on configuring and sending emails in Plone."
    "property=og:description": "Learn how to configure SMTP settings and send emails in Plone."
    "property=og:title": "Plone Email Configuration Guide"
    "keywords": "Plone, Email, SMTP, Notifications, Plone 6"
---

# Sending Email in Plone

Email functionality in Plone is essential for notifications, password resets, and user communication. This guide explains how to configure and test email settings in Plone.

## **1. Configuring SMTP Settings**

Plone uses **SMTP (Simple Mail Transfer Protocol)** to send emails. To configure SMTP:

1. Go to **Site Setup** → **Mail Settings** in the Plone Control Panel.
2. Enter your SMTP server details:
   - **SMTP Server:** (e.g., `smtp.gmail.com`)
   - **SMTP Port:** (e.g., `587` for TLS, `465` for SSL)
   - **Username & Password:** (Your email credentials)
   - **Sender Address:** (Default "From" address)
3. Click **Save** and then **Send Test Email** to verify.

## **2. Sending Emails Programmatically**

Plone provides APIs for sending emails via scripts or add-ons. You can use the `plone.api` package:

```python
from plone import api

api.portal.send_email(
    recipient="user@example.com",
    sender="admin@yourplonesite.com",
    subject="Welcome to Plone",
    body="Thank you for signing up!",
)
```

```{todo}
Contribute to this documentation!
```
