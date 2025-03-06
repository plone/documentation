---
myst:
  html_meta:
    "description": "Theming of Plone 6 Classic UI"
    "property=og:description": "Theming of Plone 6 Classic UI"
    "property=og:title": "Theming of Plone 6 Classic UI"
    "keywords": "Theming, Plone 6, Classic UI, Barceloneta, Diazo, scratch, through-the-web"
---

(classic-ui-theming-index-label)=

# Theming Classic UI 

This section of the documentation describes how to theme Classic UI.


## TTW or add-on?

Small theme changes—such as the site logo and favicon and minimal CSS changes—can be made by {doc}`changing theme settings through the web (TTW) <settings-ttw>`.
This method is especially useful for short-lived or prototype sites.
It allows you to make minor adjustments without needing to dive into code or production-level setups.
TTW can be convenient for quick experiments, websites that don't require complex theming, or short-lived websites.

An add-on allows you to keep your customization modular, and it provides a more structured approach to larger-scale theming.
This method is ideal for more permanent or complex customizations since it enables easier maintenance and portability.

The customized Barceloneta theme, creating a theme from scratch, and Diazo offer even more flexibility.

Barceloneta theme
:   Ideal for a starting point, especially if you want to tweak it as an existing, solid theme.
    You can customize its components and styles without starting from zero.

From scratch
:   If your project requires something completely unique and none of the existing themes fit, building a theme from scratch would be the way to go.
    This is most appropriate for highly customized websites with distinct design requirements.

Diazo
:   Diazo can be used where designers create a self-contained HTML page with CSS and JavaScript without customizing templates.
    It can be used for simple themes or for more advanced methods.

    Its advantages include allowing more complex themes where content needs to remain flexible, and you want full control over the markup.
    
    Its disadvantages include a possible negative performance impact from the rendering process, and a more complex and difficult to maintain theme.

To summarize:

-   Use {doc}`TTW <settings-ttw>` for minor changes or testing.
-   Use {doc}`add-ons <create-add-on>` for production-level theming that needs scalability, maintainability, and modularity to customize Barceloneta or to write themes from scratch.
-   Use {doc}`Diazo <diazo>` in your add-on if you need to modify the markup without touching the page templates.


## How-to guides

```{toctree}
:maxdepth: 2

settings-ttw
create-add-on
color-modes
diazo
```

## Reference

```{toctree}
:maxdepth: 2

scss-structure
css-custom-properties
```
