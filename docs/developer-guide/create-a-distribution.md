---
myst:
  html_meta:
    "description": "How to create a custom Plone distribution"
    "property=og:description": "How to create a custom Plone distribution"
    "property=og:title": "Create a Plone distribution"
    "keywords": "Plone 6, distribution, plone.distribution"
---

(create-a-plone-distribution-label)=

# Create a Plone distribution

A Plone distribution is a pre-packaged version of Plone that includes specific features, themes, modules, and configurations.
This section explains how a developer can create a custom Plone distribution.

```{seealso}
For a conceptual guide, see {doc}`/conceptual-guides/distributions`.
```

## Create a backend add-on

These instructions assume that you already have created a Plone backend add-on package,
and now you want to add a distribution to it.

A Plone distribution exists inside a Python Package that can be installed by `pip`.

## Update `setup.py`

The package will follow some conventions to make it "discoverable" by others.

In `setup.py`, always add the correct Trove classifiers:

```python
        "Framework :: Plone",
        "Framework :: Plone :: 6.1",
        "Framework :: Plone :: Distribution",
```

and also require `plone.distribution` to be available:

```python
    install_requires=[
        "Products.CMFPlone",
        "setuptools",
        "plone.distribution",
    ],
```

## Update `configure.zcml`

In your main `configure.zcml`, make sure to have the `plone` XML namespace declared:

```xml
<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    >
```

And also include `plone.distribution`:

```xml
<include package="plone.distribution" />
```

Then declare the distributions included in your package:

```xml
  <plone:distribution
      name="blog"
      title="Personal Blog"
      description="A Plone site already configured to host a personal Blog."
      directory="distributions/blog"
      />
```

This example registers a distribution that will configure a Personal Blog, with some default content.

## Add distribution handlers

When registering a distribution, you can provide a `pre_handler`, a `handler` and a `post_handler` which must be
functions with the following signatures.

```python
def pre_handler(answers: dict) -> dict:
    return answers

def handler(distribution: Distribution, site, answers: dict):
    return site

def post_handler(distribution: Distribution, site, answers: dict):
    return site
```

Each of those handlers will be called in this way:

- `pre_handler`: it will process the answers to do modifications on them before creating the site
- `handler`: it will be run after the bare Plone site will be created, but instead of the default handler that installs the required GenericSetup profiles and creates the content.
- `post_handler`: it will be run after the site is set up.

If you have added some extra fields in the Plone site creation form and want to do some extra configuration in the
Plone site, you can add your own handler and register as follows:

```xml
  <plone:distribution
      name="blog"
      title="Personal Blog"
      description="A Plone site already configured to host a personal Blog."
      directory="distributions/blog"
      post_handler=".handlers.blog.post_handler"
      />
```

## Add a distribution folder

A convention is to use the `distributions/<distribution_name>`folder in the root of your package to organize your distribution configuration.

In that folder, you will need to provide:

### `image.png`

A 1080x768 image of your distribution. It could be the default page of a new site, your logo, or any other way of representing this distribution.

### `profiles.json`

A `JSON` file with the GenericSetup profiles that are used by your distribution during installation.

This file needs to contain two keys:

- **base**: List of profiles installed in every new site using this distribution.

- **content**: List of profiles installed when the user decides to create a site with example content.

The configuration for a new Volto site is:

```json
{
  "base": [
    "plone.app.contenttypes:default",
    "plone.app.caching:default",
    "plonetheme.barceloneta:default",
    "plone.volto:default"
  ],
  "content": [
    "plone.volto:default-homepage"
  ]
}
```

### `schema.json`

In case you require additional input from the user during site creation, you can customize the form using the `schema.json` file.

The file should contain two keys:

- **schema**: A JSON Schema definition.
- **uischema**: A [react-jsonschema-form](https://rjsf-team.github.io/react-jsonschema-form/docs/) configuration to modify how the form is displayed.

The **schema** should have at least the following keys:

- site_id
- title
- description
- default_language
- portal_timezone
- setup_content

The `schema.json` used for the default site creation is:

```json
{
  "schema": {
    "title": "Create a Plone site",
    "description": "Adds a new Plone content management system site to the underlying application server.",
    "type": "object",
    "required": [
      "site_id",
      "title"
    ],
    "properties": {
      "site_id": {
        "type": "string",
        "title": "Path Identifier",
        "default": "Plone",
        "description": "The ID of the site. No special characters or spaces are allowed. This ends up as part of the URL unless hidden by an upstream web server."
      },
      "title": {
        "type": "string",
        "title": "Title",
        "default": "Site",
        "description": "A short title for the site. This will be shown as part of the title of the browser window on each page."
      },
      "description": {
        "type": "string",
        "title": "Site Description",
        "default": "A Plone Site"
      },
      "default_language": {"$ref": "#/definitions/languages"},
      "portal_timezone": {"$ref": "#/definitions/timezones"},
      "setup_content": {
        "type": "boolean",
        "title": "Create Content",
        "description": "Should example content be added during site creation?",
        "default": false
      }
    }
  },
  "uischema": {
  }
}
```

:::{note}
You probably noticed the entries for `default_language`:

```json
{"$ref": "#/definitions/languages"}
```

and `portal_timezone`:

```json
{"$ref": "#/definitions/timezones"}
```

Both definitions are added in runtime by `plone.distribution` to provide a list of languages and timezones available on the installation.
:::

## Add a dependency on an add-on

If you want to add a Plone backend add-on to your Plone distribution, then you must perform the following steps.

Add your add-on, such as `collective.person`, to your `setup.py`:

```python
    install_requires=[
        "setuptools",
        "Plone",
        "plone.distribution>=1.0.0b2",
        "plone.api",
        "collective.person",
    ],
```

Add it to your `dependencies.zcml`:

```xml
  <!-- List all packages you depend here -->
  <include package="plone.volto" />
  <include package="plone.restapi" />
  <include package="collective.person" />
  <include package="plone.distribution" />

</configure>
```

Add it to your `profiles.json`:

```json
  "base": [
    "plone.app.contenttypes:default",
    "plone.app.caching:default",
    "plone.restapi:default",
    "plone.volto:default",
    "collective.person:default",
    "plonetheme.barceloneta:default"
  ],
```

## Add example content

The distribution's content is loaded from JSON data in the `content` folder.

To export content from a site into this folder, use the `bin/export-distribution` script.

```shell
bin/export-distribution path/to/zope.conf Plone
```

In the example above, "Plone" is the ID of the Plone site to export.

## Limit available distributions

By default, Plone 6.1 ships with two ready-to-use distributions:

- **default**: Plone Site (Volto frontend)
- **classic**: Plone Site (Classic UI)

If you want to limit the choice of distributions when creating a new site, it is possible to set the environment variable `ALLOWED_DISTRIBUTIONS` with fewer options:

```shell
ALLOWED_DISTRIBUTIONS=default
```
