---
myst:
  html_meta:
    "description": "Create an emergency user"
    "property=og:description": "Create an emergency user"
    "property=og:title": "Create an emergency user"
    "keywords": "Plone, user and groups, emergency user, pip, buildout"
---


(user-groups-emergency-user-label)=

# Emergency user

sometimes it is needed to create an emergency user. the password of admin ist lost or you have inherit a project without a proper documentation. The usecase: you will login as admin to your, but you can't.

First of all, do the following steps not in a production environment! Shutdown your instance.

(user-groups-emergency-user-pip-installation-label)=

## Create an emergency user in a pip based Plone instance

```bash
./venv/bin/addzopeuser -c instance/etc/zope.conf <user> <password>
```

start your instance and login with the created user.

(user-groups-emergency-user-buildout-installation-label)=

## Create an emergency user in a buildout based Plone instance

With buildout and plone.recipe.zope2instance you can do

```bash
bin/instance adduser <user> <password>
```

start your instance and login with the created user.

