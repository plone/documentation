---
myst:
  html_meta:
    "description": "How to add a Control Panel"
    "property=og:description": "How to add a Control Panel"
    "property=og:title": "Control panels"
    "keywords": "Plone, Add, Control Panel"
---

(backend-controlpanels-label)=

# Control panels

## Adding a control panel
To add a control panel to your add-on, you can use [`plonecli`](https://pypi.org/project/plonecli/) as follows:

```shell
plonecli add controlpanel
```

This will create the control panel Python file in the control panel's folder where you can define your control panel schema fields. 

## Registering a Control panel
To manually register a view as a control panel, add the following registration to your `/profiles/default/controlpanel.xml`.

```xml
  <?xml version="1.0"?>
  <object
      name="portal_control-panel"
      xmlns:i18n="http://xml.zope.org/namespaces/i18n"
      i18n:domain="lmu.behavior">
    <configlet
      title="Some Control Panel"
      action_id="collective.example.some_control-panel"
      appId="collective.example"
      category="Products"
      condition_expr=""
      url_expr="string:${portal_url}/@@some_view"
      icon_expr=""
      visible="True"
      i18n:attributes="title">
          <permission>Manage portal</permission>
    </configlet>
  </object>
```

```{seealso}
See the chapter {ref}`training:controlpanel-label` from the Mastering Plone 6 Training.
```

```{todo}
Contribute to this documentation!
See issue [Backend > Control Panels needs content](https://github.com/plone/documentation/issues/1304).
```