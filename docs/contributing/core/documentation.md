---
myst:
  html_meta:
    "description": "Writing documentation of Plone"
    "property=og:description": "Writing documentation of Plone"
    "property=og:title": "Writing documentation of Plone"
    "keywords": "documentation, Plone"
---

# Writing documentation

For general guidance for contributing documentation, see {doc}`/contributing/documentation/index`.

For documentation authors, see {doc}`/contributing/documentation/authors`.

## Documentation of Plone

The comprehensive resource for Plone documentation is https://6.docs.plone.org/.
The documentation repository is on [GitHub](https://github.com/plone/documentation).
Information for how to contribute to documentation can be found at {doc}`/contributing/documentation/index`.


## Documenting a package

At the very least, your package should include the following forms of documentation.

### `README.md`

The `README.md` is the first entry point for most people to your package.
It will be included on the PyPI page for your package, and on the front page of its GitHub repository.
It should be formatted using [GitHub flavored Markdown](https://github.github.com/gfm/) to get formatted properly by those systems.

`README.md` should include:

-   A brief description of the package's purpose
-   Installation information
-   Version compatibility information
-   Links to other sources of documentation
-   Links to issue trackers, mailing lists, and other ways to get help

```{seealso}
{ref}`github-community-health-files-label`
```


### The manual (narrative documentation)

The manual should go into further depth for people who want to know all about how to use the package.

It should include topics like:

-   What are its features
-   How to use them (in English—not doctests!)
-   Information about architecture
-   Common gotchas

The manual should address various audiences who may need different types of information:

-   End users who use Plone for content editing, but don't manage the site.
-   Site administrators who install and configure the package.
-   Integrators who need to extend the functionality of the package in code.
-   System administrators who need to maintain the server running the software.

Simple packages with limited functionality can get by with a single page of narrative documentation.
In this case, it's simplest to include it in an extended `README.md`.
Some excellent examples of a single-page README are https://pypi.org/project/plone.outputfilters/ and https://github.com/plone/plone.app.caching.

If your project is moderately complex, you may want to set up your documentation with multiple pages.
The preferred way to do this is to add Sphinx to your project, and host your docs on [readthedocs.org](https://about.readthedocs.com/), so that it rebuilds the documentation whenever you push to GitHub.
If you do this, your `README.md` must link off site to the documentation.


### Reference or API documentation

An API reference provides information about the package's public API (that is, the code that the package exposes for use from external code).
It is meant for random access to remind the reader of how a particular class or method works, rather than for reading in its entirety.

If the code base is written with docstrings, API documentation can be automatically generated using Sphinx.


### Changes or history

```{seealso}
-   {ref}`contributing-change-log-label`
-   Volto's [`towncrier.toml`](https://github.com/plone/volto/blob/main/packages/volto/towncrier.toml) as an example towncrier configuration file.
```


### Licenses

Information about the open source license used for the package should be placed where GitHub can pick it up and display it as one of its [community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
The preferred location is at the root of the repository.

For Plone core packages, this includes `LICENSE.md` and {file}`LICENSE.GPL`.


(github-community-health-files-label)=

### GitHub community health files

If your Plone core package lacks a specific community health file, then GitHub will pick up the one configured in the Plone GitHub organization repository [`.github`](https://github.com/plone/.github).
You can override the default files by placing your health file as described in the documentation of [GitHub community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file).
