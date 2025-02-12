---
myst:
  html_meta:
    "description": "Create an emergency user"
    "property=og:description": "Create an emergency user"
    "property=og:title": "Create an emergency user"
    "keywords": "Plone, users, groups, emergency user, pip, buildout"
---

(user-groups-emergency-user-label)=

# Emergency user

An emergency user is one that you can use to regain administrative access to a Plone site.
If you lose the administrator password, or you inherit a project without proper documentation, you can create an emergency user.

First of all, do the following steps not in a production environment!


(user-groups-create-an-emergency-user-label)=

## Create an emergency user

There are two procedures to create an emergency user, depending on how you created and manage the Plone site.
For both scenarios, the commands you run will stop the Plone site, add a new user, and start the Plone site.

```{important}
You should always stop your Plone site before adding a new user.
```

```{important}
The new username must not be an existing one.
Therefore you should avoid the username `admin`, but use another arbitrary name, such as `admin2`.
```


(user-groups-emergency-user-pip-installation-label)=

### pip based Plone instance

You can run the following shell commands to create an emergency user.

```shell
./venv/bin/instance stop
./venv/bin/addzopeuser -c instance/etc/zope.conf <user> <password>
./venv/bin/instance start
```

Now you can login with the created user.


(user-groups-emergency-user-buildout-installation-label)=

### Buildout based Plone instance

With buildout and `plone.recipe.zope2instance`, you can run the following shell commands to create an emergency user.

```shell
bin/instance stop
bin/instance adduser <user> <password>
bin/instance start
```

Now you can login with the created user.
