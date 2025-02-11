---
myst:
  html_meta:
    "description": "How to add an emergency user to an existing Zope instance"
    "property=og:description": "How to add an emergency user to an existing Zope instance"
    "property=og:title": "Add an emergency user"
    "keywords": "Plone 6, create, add, factory, distributions"
---

(add-an-emergency-user)=

# How to add an emergency user

This section explains how to add an emergency user to an existing Zope instance.

It assumes that you have already {doc}`installed </install/index>` Plone.

Some installation methods automatically create an emergency user for you already.

The credentials for the emergency user are usually:

- username: `admin`
- password: `admin`

Follow these instructions if you used an installation method that did not do this, or if you need to create a new emergency user for some reason.

```{note}
The emergency user is a superuser with full access to the Zope instance. It is not limited to a specific Plone site.
```

There are two ways to add an emergency user, depending on how your site was installed.

## Add an emergency user via an instance script

If your site was installed with `buildout`, you can add an emergency user via an instance script.

Run in the terminal:

```bash
$ bin/instance adduser username password
Created user: username
```

The name of the instance script might vary based on your installation.
Replace `username` and `password` with the desired values.

If the user already exists, no user will be created. The password will not be changed, e.g.:

```bash
$ bin/instance adduser foo baz
Created user: None
```

## Add an emergency user via the addzopeuser script

For `pip` based installations will have a script called `addzopeuser` in the `bin` directory.

The `addzopeuser` script might also be available in `buildout` based installations.

Run in the terminal:

```bash
$ .venv/bin/addzopeuser -c path/to/etc/zope.conf username password
User username created.
```

The `addzopeuser` script and `zope.conf` locations might vary based on your installations.
Replace `username` and `password` with the desired values.

If the user already exists, no user will be created. The password will not be changed, e.g.:

```bash
$ .venv/bin/addzopeuser -c tmp/zeoclient/etc/zope.conf foo baz
Got no result back. User creation may have failed.
Maybe the user already exists and nothing is done then.
Or the implementation does not give info when it succeeds.
```
