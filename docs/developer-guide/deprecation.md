---
myst:
  html_meta:
    "description": "How to implement deprecations in Plone, including Python, ZCML and templates."
    "property=og:description": "How to implement deprecations in Plone, including Python, ZCML and templates."
    "property=og:title": "Implement deprecations"
    "keywords": "deprecation, zcml, template, jbot, Plone, Python"
---

(developer-deprecation-label)=

# Implement deprecations

This chapter describes how to enable deprecation warnings and best practices for implementing deprecations in Plone, Zope, and Python.

```{seealso}
For background on deprecation philosophy and use cases, see {doc}`/conceptual-guides/deprecation`.
```


## Enable deprecation warnings

### Zope

Zope does configure logging and warnings, so the steps below (under section Python) are not needed.

Using `plone.recipe.zope2instance` add the option `deprecation-warnings = on` to the buildouts `[instance]` section.

```ini
[buildout]
parts = instance

[instance]
recipe = plone.recipe.zope2instance
...
deprecation-warnings = on
...
```

This adds this line to the `zope.conf` file:

```
debug-mode on
```

Without the recipe this can be set manually as well:
In `zope.conf` custom filters for warnings can be defined.

```xml
...
<warnfilter>
    action always
    category exceptions.DeprecationWarning
</warnfilter>
...
```

### Python

Enable Warnings

: Warnings are written to `stderr` by default, but `DeprecationWarning` output is surpressed by default.

  Output can be enabled by starting the Python interpreter with the [-W \[all|module|once\]](https://docs.python.org/3/using/cmdline.html#cmdoption-W) option.

  It is possible to enable output in code too:

  ```python
  import warnings
  warnings.simplefilter("module")
  ```

Configure Logging

: Once output is enabled it is possible to [redirect warnings to the logger](https://docs.python.org/3/library/logging.html#logging.captureWarnings):

  ```python
  import logging
  logging.captureWarnings(True)
  ```

### Running tests

In Plone tests deprecation warnings are not shown by default.
The `zope.conf` setting is not taken into account.

In order to enable deprecation warnings,
the Python way with the `-W` command option must to be used.

Given youre using a modern buildout with virtualenv as recommended,
the call looks like so:

```bash
./bin/python -W module ./bin/test
```


## Deprecation best practice

### Vanilla deprecation messages

Python offers a built-in `DeprecationWarning` which can be issued using standard libraries `warnings` module.

For details read the [official documentation about warnings](https://docs.python.org/3/library/warnings.html).

In short it works like so

```python
import warnings
warnings.warn('deprecated', DeprecationWarning)
```

### Moving whole modules

Given a package `old.pkg` with a module `foo.py` need to be moved to a package `new.pkg` as `bar.py`.

[zope.deprecation Moving modules](https://zopedeprecation.readthedocs.io/en/latest/api.html#moving-modules) offers a helper.

1. Move the `foo.py` as `bar.py` to the `new.pkg`.
2. At the old place create a new `foo.py` and add to it

```python
from zope.deprecation import moved
moved('new.pkg.bar', 'Version 2.0')
```

Now you can still import the namespace from `bar` at the old place, but get a deprecation warning:

> DeprecationWarning: old.pkg.foo has moved to new.pkg.bar.
> Import of old.pkg.foo will become unsupported in Version 2.0

### Moving whole packages

This is the same as moving a module, just create for each module a file.

### Deprecating methods and properties

You can use the `@deprecate` decorator from [zope.deprecation Deprecating methods and properties](https://zopedeprecation.readthedocs.io/en/latest/api.html#deprecating-methods-and-properties) to deprecate methods in a module:

```python
from zope.deprecation import deprecate

@deprecate('Old method is no longer supported, use new_method instead.')
def old_method():
    return 'some value'
```

The `deprecated` wrapper method is for deprecating properties:

```python
from zope.deprecation import deprecated

foo = None
foo = deprecated(foo, 'foo is no more, use bar instead')
```

### Moving functions and classes

Given we have a Python file at `old/foo/bar.py` and want to move some classes or functions to `new/baz/baaz.py`.

Here `zope.deferredimport` offers a deprecation helper.
It also avoids circular imports on initialization time.

```python
import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Import from new.baz.baaz instead",
    SomeOldClass='new.baz:baaz.SomeMovedClass',
    some_old_function='new.baz:baaz.some_moved_function',
)

def some_function_which_is_not_touched_at_all():
    pass
```

### Deprecating a GenericSetup profile

Starting with GenericSetup 1.8.2 (part of Plone > 5.0.2) the `post_handler` attribute in ZCML can be used to call a function after the profile was applied.
We use this feature to issue a warning.

First we register the same profile twice. Under the new name and under the old name:

```xml
<genericsetup:registerProfile
    name="default"
    title="My Fance Package"
    directory="profiles/default"
    description="..."
    provides="Products.GenericSetup.interfaces.EXTENSION"
    />

<genericsetup:registerProfile
    name="some_confusing_name"
    title="My Fance Package (deprecated)"
    directory="profiles/some_confusing_name"
    description="... (use profile default instaed)"
    provides="Products.GenericSetup.interfaces.EXTENSION"
    post_handler=".setuphandlers.deprecate_profile_some_confusing_name"
    />
```

And in `setuphandlers.py` add a function:

```python
import warnings

def deprecate_profile_some_confusing_name(tool):
    warnings.warn(
        'The profile with id "some_confusing_name" was renamed to "default".',
        DeprecationWarning
    )
```

### Deprecating a template position

Sometimes we need to move templates to new locations. Since addons often use [z3c.jbot](https://github.com/zopefoundation/z3c.jbot) to override templates by their position, we need to point them to the new position as well as make sure that the override still works with the old position.


To deprecate a package:

1. In the old package folders `__init__.py` add a dictionary `jbot_deprecations` that maps the old template locations to their new counterparts, e.g.:

```python
jbot_deprecations = {
    "plone.locking.browser.info.pt": "plone.app.layout.viewlets.info.pt"
}
```

2. Add this deprecation snippet to the package `configure.zcml` file:

```{code-block} xml
:emphasize-lines: 6,9-12
:linenos:

<configure
    xmlns="http://namespaces.zope.org/zope"
    xmlns:browser="http://namespaces.zope.org/browser"
    xmlns:zcml="http://namespaces.zope.org/zcml"
    >

  <include
      zcml:condition="installed z3c.jbot"
      package="z3c.jbot"
      />
  <browser:jbotDeprecated
      zcml:condition="have jbot-deprecations"
      dictionary=".jbot_deprecations"
      />

</configure>
```

If a `z3c.jbot` version that supports deprecation is found, trying to override the template with the old location will trigger a deprecation warning that will instruct the user to rename its override file.
