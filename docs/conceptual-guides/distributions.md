---
myst:
  html_meta:
    "description": "A Plone distribution is a pre-packaged version of Plone that includes specific features, themes, modules, and configurations."
    "property=og:description": "A Plone distribution is a pre-packaged version of Plone that includes specific features, themes, modules, and configurations."
    "property=og:title": "Plone distributions"
    "keywords": "Plone 6, distribution, plone.distribution"
---

(plone-distributions-label)=

# Plone distributions

```{versionadded} Plone 6.1
```

A Plone {term}`distribution` is a pre-packaged version of Plone that includes specific features, themes, modules, and configurations.
It is a convenient way to get a specific type of website up and running quickly, as the distribution includes everything needed to run that type of site.

```{seealso}
To create your own distribution, see {doc}`/developer-guide/create-a-distribution`.
```


## Built-in distributions

Plone comes with two built-in distributions, which correspond to the two Plone user interfaces.

[`plone.volto`](https://github.com/plone/plone.volto)
:   Create a Plone site with the Volto frontend.

[`plone.classicui`](https://github.com/plone/plone.classicui) 
:   Create a Plone site with the Classic UI frontend.


## Third-party distributions

You can create your own distributions to suit your needs.

```{seealso}
For a how-to guide, see {doc}`/developer-guide/create-a-distribution`.
```

For example, a Plone consulting agency can create a distribution demonstrating its favorite setup for Plone.
This would contain the add-ons that they usually add in each project, including example content.
With this, the agency can create a fully configured Plone site filled with content for a potential client.

Alternatively, an agency or implementer can create a distribution for specific project.
This could create a site with all add-ons activated and configured for this project, including example content, and optionally users and groups.
During the development phase of a new project, all developers would use this to create a fresh site locally so that everyone has the same configuration and content.

Custom Plone distributions can be distributions for use by others.
Examples of third-party Plone distributions include:

- [SENAITE](https://www.senaite.com)
- [Quaive](https://quaive.com/)
- [Portal Modelo](https://www12.senado.leg.br/interlegis/produtos/portal-modelo)
- [Portal Padrão](https://identidade-digital-de-governo-plone.readthedocs.io/en/latest/)


## Related packages

The implementation of distributions in the Plone codebase is found in the following Python packages.

-   [`plone.distribution`](https://github.com/plone/plone.distribution) provides the framework for defining distributions.
-   [`plone.exportimport`](https://github.com/plone/plone.exportimport) imports and exports content, users, and other objects between Plone sites.
    `plone.distribution` uses it.
-   [`plone.volto`](https://github.com/plone/plone.volto) is the distribution to create a Plone site with the Volto frontend.
-   [`plone.classicui`](https://github.com/plone/plone.classicui) is the distribution to create a Plone site with the Classic UI frontend.

```{note}
For Plone 7, the [Plone roadmap](https://plone.org/why-plone/roadmap) guides development toward a clearer separation between the Classic UI frontend and the core `Products.CMFPlone` backend.
This means that in Plone 7, `Products.CMFPlone` will have less code and pull in fewer dependencies, whereas `plone.classicui` may have more code and pull in more dependencies.
This is the direction in which the backend is heading, and the introduction of the `plone.classicui` distribution package is an important step along this path.
```

## Comparison with other CMSs

Drupal
:   Drupal has distributions for blogs, e-commerce sites, and intranet portals.

WordPress
:   WordPress has a similar concept in the form of "WordPress Multisite," which allows users to run multiple websites from a single installation of WordPress.

Joomla
:   Joomla has a similar concept in the form of "Joomla Templates," which are pre-designed templates for Joomla websites.

TYPO3
:   TYPO3 has a similar concept in the form of "TYPO3 Distributions," which are pre-configured installations of TYPO3 for specific types of websites.
