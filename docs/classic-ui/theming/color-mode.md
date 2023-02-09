# Color theme toggler for Bootstrap 5
With Bootstrap 5.3 a color-theme toggler is possible. 
This is not provided by default and needs some custom code.
Here is a small guide how to implement it into Plone 6.

## Toggle Button
Add elements with `data-bs-theme-value`.
If you want to add a theme toggler to your site, you can use the following elements:

```html
<div class="btn-group">
  <button class="btn btn-secondary" data-bs-theme-value="light">
    Light
  </button>
  <button class="btn btn-secondary" data-bs-theme-value="dark">
    Dark
  </button>
</div>
```

## Javascript

The following Javascript is needed to make the toggler work. 
It is based on the [Bootstrap 5.3 documentation](https://getbootstrap.com/docs/5.3/customize/color-modes/).
The Javascript is added to the `browser/static` folder of your Plone 6 project and registered in the `browser/profiles/default/registry` of your Plone 6 project.
See [Registering Javascript and CSS](classic-ui-static-resources-registering-label) for more information.

```js
document.addEventListener('DOMContentLoaded', () => {
    'use strict'

    const storedTheme = localStorage.getItem('theme');

    const getPreferredTheme = () => {
        if (storedTheme) {
            return storedTheme;
        }

        return window.matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
    }

    const setTheme = function (theme) {
        if (theme === 'auto' && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            document.documentElement.setAttribute('data-bs-theme', 'dark');
        } else {
            document.documentElement.setAttribute('data-bs-theme', theme);
        }
        const e = new CustomEvent('data-bs-theme-changed');
        e.theme = theme;
        document.dispatchEvent(e);
    }

    setTheme(getPreferredTheme());

    const showActiveTheme = theme => {
        const btnToActive = document.querySelector(`[data-bs-theme-value="${theme}"]`)

        document.querySelectorAll('[data-bs-theme-value]').forEach(element => {
            element.classList.remove('active');
        });

        btnToActive.classList.add('active');
    }

    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
        if (storedTheme !== 'light' || storedTheme !== 'dark') {
            setTheme(getPreferredTheme());
        }
    });

    showActiveTheme(getPreferredTheme());

    document.querySelectorAll('[data-bs-theme-value]')
        .forEach(toggle => {
            toggle.addEventListener('click', (e) => {
            e.preventDefault();
            const theme = toggle.getAttribute('data-bs-theme-value');
            localStorage.setItem('theme', theme);
            setTheme(theme);
            showActiveTheme(theme);
        });
    });
});
```

## Customize single elements

You can customize single elements with the `data-bs-theme` attribute.
When set to a value the element will be rendered in the given theme, despite the global theme.
For example:

```html
<form data-bs-theme='light'>
  <div class="mb-3">
    <label for="exampleInputEmail1" class="form-label">Email address</label>
    <input type="email" class="form-control" id="exampleInputEmail1" aria-describedby="emailHelp">
  </div>
  <button type="submit" class="btn btn-primary">Submit</button>
</form>
```