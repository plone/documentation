---
myst:
  html_meta:
    "description": "Convenience template global variables in Plone"
    "property=og:description": "Convenience template global variables in Plone"
    "property=og:title": "Convenience template global variables in Plone"
    "keywords": "Plone, Classic UI, global variables, templates"
---

# Template global variables 

For convenience Plone defines a couple of global variables often used in templates.

- {ref}`backend-global-utils-portal-state-label`
- {ref}`backend-global-utils-context-state-label`
- {ref}`backend-global-utils-plone-view-label`
- {ref}`icons <classic-ui-icons-icon-resolver-label>`
- `lang`
- {ref}`classic-ui-templates-global-variables-portal-url-label`
- {ref}`classic-ui-templates-global-variables-check-permissions`
- `ajax_include_head`
- `isAnon`


(classic-ui-templates-global-variables-portal-url-label)=

## `portal_url`

`portal_url` will return the portal URL.
It can be used as follows:

```xml
<a href="${portal_url}/@@overview-controlpanel>Overview Controlpanel</a>
```

It is basically a short cut for:

```xml
<div tal:define="portal_url python: portal_state.portal_url()">
  <a href="${portal_url}/@@overview-controlpanel">Overview Controlpanel</a>
</div>
```


(classic-ui-templates-global-variables-check-permissions)=

## `checkPermission`

`checkPermission` will return the `checkPermission` method from `portal_membership` tool.

It can be used as follows to check for user permissions in templates:

```xml
<div tal:condition="python: checkPermission('Modify portal content', context)">
  <span tal:omit-tag="">
    You see this page because you have permission to edit this.
  </span>
</div>
```