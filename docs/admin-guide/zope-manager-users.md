---
myst:
  html_meta:
    "description": "How to create a Zope manager user in an existing Zope instance"
    "property=og:description": "How to create a Zope manager user in an existing Zope instance"
    "property=og:title": "Zope manager users"
    "keywords": "Plone, Zope, users, admin user, emergency user, administration, pip, buildout"
---

(admin-guide-zope-manager-user-label)=

# Zope manager users

Zope manager users have full access to the whole Zope instance.

Some installation methods automatically create a zope `admin` user for you already.

This guide explains how to add a Zope manager user to an existing Zope instance.

There are multiple reasons why you might need to do that, such as:

- Your installation method did not create one.
- You lost access to your instance.
- You inherited a project without proper documentation.

```{note}
If you need to regain access to your instance, this user is also referred to as an **emergency user**.
```

```{note}
The emergency user is a superuser with full access to the Zope instance.
It is not limited to a specific Plone site.
Please be aware of the security implications.
You might want to change the passwords of the already existing manager users after you regained to your instance.
```

(admin-guide-adding-a-new-zope-manager-user-label)=

## Add a new Zope manager user

There are multiple ways to create a Zope manager user.
That depends on how you created and managed your Zope instance.

```{important}
If you are running a standalone instance, it must be stopped before adding the user.
```

(admin-guide-using-the-adduser-instance-command-label)=

### Using the `adduser` instance command

If your site was installed with `buildout` and `plone.recipe.zope2instance`, you can add a Zope manager user via an instance script.

Run the following command in the terminal:

```bash
$ bin/instance adduser username password
Created user: username
```

The name of the instance script might vary based on your installation.
Replace `username` and `password` with the desired values.

If the user already exists:

- No user will be created
- The password will not be changed

The command will return a message like this:

```bash
$ bin/instance adduser foo baz
Created user: None
```

(admin-guide-using-the-addzopeuser-command-label)=

### Using the `addzopeuser` command

For `pip` based installations, you will have a script called `addzopeuser` in the `bin` directory of your virtual environment.

The `addzopeuser` script might also be available in `buildout` based installations.

Run in the terminal:

```bash
$ .venv/bin/addzopeuser -c path/to/etc/zope.conf username password
User username created.
```

The `addzopeuser` script and `zope.conf` locations might vary based on your installations.
Replace `username` and `password` with the desired values.

If the user already exists:

- No user will be created
- The password will not be changed

The command will return a message like this:

```bash
$ .venv/bin/addzopeuser -c tmp/zeoclient/etc/zope.conf foo baz
Got no result back. User creation may have failed.
Maybe the user already exists and nothing is done then.
Or the implementation does not give info when it succeeds.
```
