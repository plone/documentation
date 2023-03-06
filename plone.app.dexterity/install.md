---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

# Installing Dexterity

How to install Dexterity and use it in your project.

```{note}
Dexterity is an **already installed part of Plone 5.x**, no action is needed here.
```

## Installing Dexterity on Plone 4.3

Dexterity is included with Plone 4.3, but must be activated via the "Add-ons" configlet in site setup.

```{important}
If you installed Dexterity on a Plone site that you upgraded to Plone 4.3, you must include the relations extra `plone.app.dexterity [relations]`.
Otherwise your site will have a broken intid utility.
```

Dexterity is distributed as a number of eggs, published on [PyPI](https://pypi.org).
The [plone.app.dexterity](https://pypi.org/project/plone.app.dexterity/) egg pulls in all the required dependencies and should get you up and running.
This how-to explains what you need to do to use Dexterity in a standard Plone buildout.
