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

This section explains how a developer can create a custom Plone {term}`distribution`.
A Plone distribution is a pre-packaged version of Plone that includes specific features, themes, modules, and configurations.

```{seealso}
For a conceptual guide, see {doc}`/conceptual-guides/distributions`.
```


## Create a backend add-on

These instructions assume that you already have created a Plone backend add-on package,
and now you want to add a distribution to it.

A Plone distribution exists inside a Python package that can be installed by `pip`.


## Update `setup.py`

Your package should follow conventions that make it discoverable by other developers.

In your {file}`setup.py` file, always add the correct [Python Trove classifiers](https://pypi.org/classifiers/).

```python
"Framework :: Plone",
"Framework :: Plone :: 6.1",
"Framework :: Plone :: Distribution",
```

Add `plone.distribution` to your `install_requires` stanza in your {file}`setup.py` file.

```{code-block} python
:emphasize-lines: 4

install_requires=[
    "Products.CMFPlone",
    "setuptools",
    "plone.distribution",
],
```


## Update `configure.zcml`

In your main {file}`configure.zcml` file, add the `plone` XML namespace with the following declaration.

```{code-block} xml
:emphasize-lines: 3

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:plone="http://namespaces.plone.org/plone"
    >
```

Register `plone.distribution` as a package to include with the following `<include>` directive.

```xml
<include package="plone.distribution" />
```

Then declare the distributions you want to include in your package.

```xml
<plone:distribution
    name="blog"
    title="Personal Blog"
    description="A Plone site already configured to host a personal blog."
    directory="distributions/blog"
    />
```

The above example registers a distribution that will configure a personal blog with some default content.


## Add distribution handlers

When registering a distribution, you can provide a `pre_handler`, a `handler`, and a `post_handler`, each of which must be a function with their respective signature, as shown in the following example.

```python
def pre_handler(answers: dict) -> dict:
    return answers

def handler(distribution: Distribution, site, answers: dict):
    return site

def post_handler(distribution: Distribution, site, answers: dict):
    return site
```

Each of those handlers will be called as follows.

`pre_handler`
:   Processes the answers to prepare the distribution before creating the site.

`handler`
:   Runs after creating the bare Plone site instead of the default handler.
    It installs the required GenericSetup profiles and creates the content.

`post_handler`
:   Runs after the site is set up.

To add extra configuration to your Plone site, and assuming you added extra inputs to the Plone site creation form, then you can add your own handler, registering it as shown in the following example.

```{code-block} xml
:emphasize-lines: 6

<plone:distribution
    name="blog"
    title="Personal Blog"
    description="A Plone site already configured to host a personal Blog."
    directory="distributions/blog"
    post_handler=".handlers.blog.post_handler"
    />
```


## Add a distribution folder
 
To organize your distribution configuration, you can follow the convention to use the {file}`distributions/<distribution_name>` folder in the root of your package.
In that folder, you need to provide the items described in the following sections.


### `image.png`

A 1080 pixels wide by 768 pixels tall image in PNG format representing your distribution.
It could be the default page of a new site, your logo, or any other way of representing your distribution.


### `profiles.json`

A file {file}`profiles.json` containing the GenericSetup profiles that your distribution uses during installation.

This file needs to contain two keys.

`base`
:   List of profiles to install in every new site using this distribution.

`content`
:   List of profiles to install when the user decides to create a site with example content.

As an example, the configuration for a new Plone site with Volto as its frontend would be the following.

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

If you require additional input from the user during site creation, you can customize the form using the {file}`schema.json` file.

The file should contain two keys.

`schema`
:   A {term}`JSON Schema` definition.

`uischema`
:   A [`react-jsonschema-form`](https://rjsf-team.github.io/react-jsonschema-form/docs/) configuration to modify the display of the form.

The `schema` should have at least the following keys.

-   `site_id`
-   `title`
-   `description`
-   `default_language`
-   `portal_timezone`
-   `setup_content`

The following code example is the content of the {file}`schema.json` file for creating the site.

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

````{note}
You may have noticed the entries for both `default_language` and `portal_timezone`.

```json
      "default_language": {"$ref": "#/definitions/languages"},
      "portal_timezone": {"$ref": "#/definitions/timezones"},
```

`plone.distribution` adds both definitions at runtime, providing a list of languages and timezones available on the installation.
````

If you want to hide fields in the form, you can use the `uischema`.
This is especially useful for fields that must be in the schema, but for which you always want the default value.
The next lines hide three fields:

```json
{
  "schema": {
    "…": "…"
  },
  "uischema": {
    "description": {
      "ui:widget": "hidden"
    },
    "default_language": {
      "ui:widget": "hidden"
    },
    "portal_timezone": {
      "ui:widget": "hidden"
    }
  }
}
```


## Add a dependency on an add-on

If you want to add a Plone backend add-on to your Plone distribution, then you must perform the following steps.

Add your add-on, such as `collective.person`, to your {file}`setup.py` file's `install_requires` stanza.

```{code-block} python
:emphasize-lines: 6

install_requires=[
    "setuptools",
    "Plone",
    "plone.distribution>=1.0.0b2",
    "plone.api",
    "collective.person",
],
```

Then add it to your {file}`dependencies.zcml` file.

```{code-block} xml
:emphasize-lines: 5

  <!-- List all packages your distribution depends on here -->
  <include package="plone.volto" />
  <include package="plone.restapi" />
  <include package="collective.person" />
  <include package="plone.distribution" />

</configure>
```

Finally, add it to your {file}`profiles.json` file.

```{code-block} json
:emphasize-lines: 6

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

The distribution loads its content from JSON data in the `content` folder.

To export content from a site into this folder, use the `bin/export-distribution` script.

```shell
bin/export-distribution path/to/zope.conf Plone
```

In the example above, `Plone` is the ID of the Plone site to export.


## Limit available distributions

By default, Plone 6.1 ships with two ready-to-use distributions.

`default`
:   Create a Plone site with the Volto frontend.

`classic` 
:   Create a Plone site with the Classic UI frontend.

If you want to limit the choice of distributions when creating a new site, you can set the environment variable `ALLOWED_DISTRIBUTIONS` to a comma-separated sting of only those distributions' names.

```shell
ALLOWED_DISTRIBUTIONS=default
```
