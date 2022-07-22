---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": "Mockup patterns"
    "keywords": "Plone6 Theming"
---

# Mockup patterns

```{todo}
- What's the purpose of patterns?
- Show me an example (where is it applied? how does the code look like?)
- How do I write a pattern? plonecli, bobtemplates...
- How do I register resouces (Javascript, CSS)?
- Do I have to minify or does Plone minify?
- What's about JQuery?
- Does Module Federation affect me?
- Is this chapter about patterns located correctly in classic-ui or classic-ui/theming?
```

https://github.com/Patternslib/pat-PATTERN_TEMPLATE is a patterns generator and a starting point.
However, it does not provide a plone integration (registering of resources, etc) - this is what the bobtemplates PR‌ is about. https://github.com/plone/bobtemplates.plone/pull/507

We assume you have a theme package.
If not, you can create one with {term}`plonecli`

```shell
plonecli create addon abc.mythemefromscratch
cd abc.mythemefromscratch
plonecli add theme_basic
```

In the future:
https://github.com/plone/bobtemplates.plone/pull/507

```shell
plonecli add mockup_pattern
```

See also info in {ref}`v60-mockup-resource-registry-label`.

