---
myst:
  html_meta:
    "description": "Color modes in Plone Classic UI"
    "property=og:description": "Color modes in Plone Classic UI"
    "property=og:title": "Color modes in Plone Classic UI"
    "keywords": "Plone, Classic UI, theming, color modes, Bootstrap, Twitter"
---

(color-modes-label)=

# Color modes

Bootstrap 5.3 has introduced [color modes](https://getbootstrap.com/docs/5.3/customize/color-modes/).
This chapter is a guide for how to implement color modes in Plone 6.1.

```{versionadded} Plone 6.1
```



(preferred-color-modes-label)=

## Preferred color modes

You will need to add some JavaScript functionality to set the Bootstrap theme to the user's preferred color scheme.
Add the JavaScript file to the `browser/static` folder of your Plone 6.1 project.
Register it in the `browser/profiles/default/registry` of your Plone 6.1 project.
See {ref}`classic-ui-static-resources-registering-label` for more information.

```js
(() => {
    'use strict'

    // Set Bootstrap Theme to the preferred color scheme
    const setPreferredTheme = () => {
        if (window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-bs-theme', 'dark')
        } else {
            document.documentElement.setAttribute('data-bs-theme', 'light')
        }
    }

    window.addEventListener('DOMContentLoaded', () => {
        setPreferredTheme()
    })
})()
```


(toggle-button-label)=

## Toggle button

To switch color themes, corresponding elements with `data-bs-theme-value` attributes must be added to the DOM.
Default Bootstrap 5.3 color themes include `light`, `dark`, and `auto`.
If you want to add a theme toggler to your site, you can use the following example.

```html
<div class="btn-group btn-group-sm">
  <button class="btn btn-secondary" data-bs-theme-value="light">
    Light
  </button>
  <button class="btn btn-secondary" data-bs-theme-value="dark">
    Dark
  </button>
</div>
```


(register-the-toggle-button-label)=

## Register the toggle button

You will need to add some JavaScript functionality to the toggler.
The following code snippet is based on the [Bootstrap 5.3 documentation](https://getbootstrap.com/docs/5.3/customize/color-modes/#javascript).

Add the JavaScript file to the `browser/static` folder of your Plone 6.1 project.
Register it in the `browser/profiles/default/registry` of your Plone 6.1 project.
See {ref}`classic-ui-static-resources-registering-label` for more information.

```js
(() => {
    'use strict'

    const storedTheme = localStorage.getItem('theme')

    const getPreferredTheme = () => {
      if (storedTheme) {
        return storedTheme
      }
      return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light'
    }

    const setTheme = function (theme) {
      if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
        document.documentElement.setAttribute('data-bs-theme', 'dark')
      } else {
        document.documentElement.setAttribute('data-bs-theme', theme)
      }
    }

    const showActiveTheme = theme => {
      const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)

      document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
        element.classList.remove('active')
      })
      btnToActive.classList.add('active')
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
      if (storedTheme !== 'light' || storedTheme !== 'dark') {
        setTheme(getPreferredTheme())
      }
    })

    window.addEventListener('DOMContentLoaded', () => {
      setTheme(getPreferredTheme())
      showActiveTheme(getPreferredTheme())

      document.querySelectorAll('[data-bs-theme-value]')
        .forEach(toggle => {
          toggle.addEventListener('click', () => {
            const theme = toggle.getAttribute('data-bs-theme-value')
            localStorage.setItem('theme', theme)
            setTheme(theme)
            showActiveTheme(theme)
          })
        })
    })
})()
```


(customize-single-elements-label)=

## Customize single elements

Elements can be assigned a static theme using the `data-bs-theme` attribute.
When set to a value, the element will be rendered in the given theme, overriding the global theme.
See the following example.

```html
<form data-bs-theme='light'>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Email address</label>
    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```

## Using color modes in Plone 6.0

To use color modes in Plone 6.0, manually include `barceloneta=3.1.0` and `plone.staticresources=2.1.0`, as described in {ref}`manage-add-an-add-on`.
