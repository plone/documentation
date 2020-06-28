======================
Adding CAPTCHA Support
======================

.. admonition :: Description

    PloneFormGen has built-in support for Re-Captcha. This how-to tells you how to enable it.

PloneFormGen and CAPTCHA Fields
===============================

When PFG is installed in a Plone instance via add/remove products, it will look for evidence that either collective.captcha or collective.recaptcha are available. If that's found, the CAPTCHA Field will be added to the available field list.

If you are using collective.recaptcha, you need to take the additional step of setting your public/private keypair. You get these by setting up an account at recaptcha.net. The account is free. You may specify your keypair in the PFG configlet in your site settings.

If you add a CAPTCHA facility *after* installing PFG, to enable CAPTCHA support you will need to add ``FormCaptchaField`` as an allowed content type to ``FormFolder`` in ``portal_types`` or reinstall PFG via :menuselection:`Site Setup > Add-ons`.

.. note::

    If you add a captcha facility *after* installing PFG, you will need to reinstall PFG (via add/remove products) to enable captcha support.

Installing collective.recaptcha
===============================

Add the following code to your buildout.cfg to install collective.recaptcha and Products.PloneformGen together:

.. code-block:: ini

    [buildout]
    ...
    eggs =
        Plone
        ...
        collective.recaptcha
        Products.PloneFormGen
        ...

* Re-run bin/buildout and relaunch your zope/plone instance.
* Open the PortalQuickInstaller or plone control panel and install (or reinstall if already installed) PloneFormGen.
* Open the PloneFormGen configlet in the Plone control Panel and fill in the fields with your Public and Private Keys of your ReCaptcha Account. Obtain keys from `reCaptcha.net <https://www.google.com/recaptcha/intro/invisible.html>`_.
