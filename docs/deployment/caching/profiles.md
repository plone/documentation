---
myst:
  html_meta:
    "description": "Caching profiles for Plone"
    "property=og:description": "Caching profiles for Plone"
    "property=og:title": "Caching profiles for Plone"
    "keywords": "Plone, deployment, automation, caching"
---

(caching-profiles-label)=

# Caching profiles

All persistent configuration for the caching machinery is stored in the configuration registry, as managed by `plone.app.registry`.

This can be modified using the `registry.xml` GenericSetup import step.

The *Import settings* tab of the control panel allows you to import these caching profiles.


## Default caching profiles

`plone.app.caching` includes two default caching profiles.
These  profiles encapsulate the cache settings that are known to work well with a typical default Plone installation:

### Without caching proxy

Settings useful for setups without a caching proxy.

### With caching proxy

Settings useful for setups with a caching proxy such Varnish or a CDN.
The only difference from the "without caching proxy" profile are some settings to enable proxy caching of files/images in content space and content feeds.

## Custom caching profiles

Caching policies are often a compromise between speed and freshness.
More aggressive caching often comes at the cost of increased risk of stale responses.
The default profiles provided tend to err on the side of freshness over speed so there is some room for tweaking if greater speed is desired.

Customization may also be needed if third-party products are installed which require special treatment.
Examine the HTTP response headers to determine whether the third-party product requires special treatment.
Most simple cases probably can be solved by adding the content type or template to the appropriate mapping.
More complicated cases, may require custom caching operations.

A GenericSetup profile used for caching should be registered for the `ICacheProfiles` marker interface to distinguish it from more general profiles used to install a product.
This also hides the profile from Plone's Add-ons control panel.

Here is an example from this package:

```xml
    <genericsetup:registerProfile
        name="with-caching-proxy"
        title="With caching proxy"
        description="Settings useful for setups with a caching proxy such as Squid or Varnish"
        directory="profiles/with-caching-proxy"
        provides="Products.GenericSetup.interfaces.EXTENSION"
        for="plone.app.caching.interfaces.ICacheProfiles"
        />
```

The directory `profiles/with-caching-proxy` contains a single import step, `registry.xml`,
containing settings to configure the ruleset to operation mapping,
and setting options for various operations.

At the time of writing, this includes:

```xml
    <record name="plone.caching.interfaces.ICacheSettings.operationMapping">
        <value purge="False">
            <element key="plone.resource">plone.app.caching.strongCaching</element>
            <element key="plone.stableResource">plone.app.caching.strongCaching</element>
            <element key="plone.content.itemView">plone.app.caching.weakCaching</element>
            <element key="plone.content.feed">plone.app.caching.moderateCaching</element>
            <element key="plone.content.folderView">plone.app.caching.weakCaching</element>
            <element key="plone.content.file">plone.app.caching.moderateCaching</element>
            <element key="plone.content.dynamic">plone.app.caching.terseCaching</element>
        </value>
    </record>
```

Default options for the various standard operations are found in the `registry.xml` file that is part of the standard installation profile for this product, in the directory `profiles/default`.

The custom profile overrides a number of operation settings for specific rulesets (see below).

For example:

```xml
    <record name="plone.app.caching.weakCaching.plone.content.itemView.ramCache">
        <field ref="plone.app.caching.weakCaching.ramCache" />
        <value>True</value>
    </record>
```

This enables RAM caching for the "weak caching" operation for resources using the ruleset `plone.content.itemView`.
The default is defined in the main `registry.xml` as::

```xml
    <record name="plone.app.caching.weakCaching.ramCache">
        <field type="plone.registry.field.Bool">
            <title>RAM cache</title>
            <description>Turn on caching in Zope memory</description>
            <required>False</required>
        </field>
        <value>False</value>
    </record>
```

Notice how we use a *field reference* to avoid having to re-define the field.

It may be useful looking at these bundled `registry.xml` for inspiration if you are building your own caching profile.
Alternatively, you can export the registry from the `portal_setup` tool and pull out the records under the prefixes `plone.caching` and `plone.app.caching`.

Typically, `registry.xml` is all that is required, but you are free to add additional import steps if required.
You can also add a `metadata.xml` and use the GenericSetup dependency mechanism to install other profiles on the fly.
