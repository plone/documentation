---
myst:
  html_meta:
    "description": "How to install, operate, configure, and deploy Plone 6"
    "property=og:description": "How to install, operate, configure, and deploy Plone 6"
    "property=og:title": "Admin guide"
    "keywords": "Plone 6, admin, install, configuration, deploy"
---

(admin-index-label)=

# Admin guide

In this part of the documentation, you can find how to install, operate, and configure Plone.


```{toctree}
:caption: Install
:maxdepth: 1

/install/create-project-cookieplone
install-buildout
install-pip
/install/create-project
```

```{toctree}
:caption: Operate
:maxdepth: 1

run-plone
add-site
configure-zope
add-ons
import-export
override-core
/upgrade/index
```
% TODO: uncomment and add the following link to the Operate toctree when https://github.com/plone/volto/pull/6397 is merged.
% https://volto--6397.org.readthedocs.build/development/add-ons/install-an-add-on.html
% /volto/development/add-ons/index


```{toctree}
:maxdepth: 1
:caption: Deploy

/install/containers/index
```
