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

This guide explains how to add a Zope user with the "manager" role—called a "Zope manager user"—to an existing Zope instance.

Zope manager users have full access to the whole Zope instance.

Some installation methods automatically create a Zope manager user named `admin` for you already.

There are multiple reasons why you might need to add a Zope manager user, including the following.

-   Your installation method did not create one.
-   You lost access to your instance.
-   You inherited a project without proper documentation.

```{note}
If you need to regain access to your instance, this user is also referred to as an "emergency user" in this context only.

The emergency user is a superuser with full access to the Zope instance.
It is not limited to a specific Plone site.
Please be aware of the security implications.
Consider changing the passwords of the existing Zope manager users after you regain access to your instance.
```

(admin-guide-add-a-new-zope-manager-user-label)=

## Add a new Zope manager user

There are multiple methods to create a Zope manager user.
The method depends on how you created and manage your Zope instance, either via {term}`buildout` or {term}`pip`.

```{important}
If you are running a standalone instance, you must stop it before adding the user.
```

(admin-guide-adduser-instance-command-label)=

### `adduser` instance command

If your site was installed with `buildout` and `plone.recipe.zope2instance`, you can add a Zope manager user via the instance script.

Run the following command.

```shell
bin/instance adduser username password
```

The name of the instance script might vary based on your installation.
Replace `username` and `password` with the desired values.

If the command is successful, then it will return the following console output.

```console
Created user: username
```

When you run the script, if the user already exists:

-   No user will be created.
-   The password will not be changed. 
-   The command will return a message such as the following.

    ```console
    Created user: None
    ```

(admin-guide-addzopeuser-command-label)=

### `addzopeuser` script

For `pip` based installations, you will have a script called `addzopeuser` in the {file}`bin` directory of your virtual environment.
The `addzopeuser` script might also be available in `buildout` based installations.

Run the following command.

```shell
$ .venv/bin/addzopeuser -c path/to/etc/zope.conf username password
```

The `addzopeuser` script and {file}`zope.conf` locations might vary based on your installation.
Replace `username` and `password` with the desired values.

If the command is successful, then it will return the following console output.

```console
User username created.
```

When you run the script, if the user already exists:

-   No user will be created.
-   The password will not be changed.
-   The command will return a message such as the following.

    ```console
    Got no result back. User creation may have failed.
    Maybe the user already exists and nothing is done then.
    Or the implementation does not give info when it succeeds.
    ```
