---
myst:
  html_meta:
    "description": "Upgrade Plone add-on products"
    "property=og:description": "Upgrade Plone add-on products"
    "property=og:title": "Upgrade Plone add-on products"
    "keywords": "Upgrade, Plone, add-on, products"
---

(upgrade-add-on-products-label)=

# Upgrade add-on products

This chapter describes the steps to migrate your third party products.

-   Shut down your Plone server instance.
-   If you pinned versions of third-party products in your `buildout.cfg` or other configuration files, such as `Products.PloneFormGen = 1.7.17`, update these references to point to the new versions.

    ```{note}
    Without pinning, such as specifying `Products.PloneFormGen` without a version number, your build tool, buildout or make, will pick the newest version of the products by default.
    ```

-   Run your build tool.
    Wait until all new software is downloaded and installed.
-   Start Plone again.
    Your site may look weird, or even be inaccessible, until you perform the next step.
-   Navigate to the Add-on screen by adding `/prefs_install_products_form` to your site's URL.
    Upgrade products if you can.
    Upgradeable products would be those that support both your current and new versions of Plone.
-   Perform product-specific upgrade procedures, if any.
    You will find these in the documentation of each product.

If `/prefs_install_products_form` is unreachable, and you are using Plone 5.0.x or earlier, you should try doing the add-on upgrades from the Management Interface.
Navigate to the `portal_quickinstaller` in the Management Interface at `/portal_quickinstaller/manage_installProductsForm`, and reinstall or upgrade products that are shown to be outdated.

```{deprecated} 5.1
`portal_quickinstaller` was deprecated in Plone 5.1, and was removed in Plone 6.0.
See [PLIP 1775](https://github.com/plone/Products.CMFPlone/issues/1775) and {ref}`upgrade-5.1-do-not-use-portal_quickinstaller-label` for Plone 5.1 and later.
```

```{warning}
Be careful when updating add-ons through the Management Interface.
It may show outdated themes as well, with a hint to update.
If you do that, the updated theme will activate itself, overriding your current theme.
If this happens, re-enable your theme in the theming panel.
```
