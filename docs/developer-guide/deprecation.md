---
myst:
  html_meta:
    "description": "How to implement deprecations in Plone, including Python, ZCML and templates."
    "property=og:description": "How to implement deprecations in Plone, including Python, ZCML and templates."
    "property=og:title": "Implement deprecations"
    "keywords": "deprecation, zcml, template, jbot, Plone, Python"
---

(developer-deprecation-label)=

# Deprecate code

This chapter describes how to enable deprecation warnings and best practices for deprecating code in Plone, Zope, and Python.

```{seealso}
For background on deprecation philosophy and use cases, see {doc}`/conceptual-guides/deprecation`.
```


## Enable deprecation warnings

This section describes how to enable deprecation warnings in Python, both in an interpreter and code, and when running tests.




(deprecation-warning-python-label)=

### Python

Enable warnings

:   Warnings are written to `stderr` by default, but `DeprecationWarning` output is surpressed by default.
    
    Output can be enabled by starting the Python interpreter with the {ref}`-W[all|module|once] <python:using-on-warnings>` argument.
    
    As an alternative, the environment variable {envvar}`python:PYTHONWARNINGS` can be set to `default`, in other words, `PYTHONWARNINGS=default`.
 
    It's possible to enable output in code, too.
    
    ```python
    import warnings
    warnings.simplefilter("module")
    ```

Configure logging

:   Once output is enabled, it's possible to use {func}`python:logging.captureWarnings` to redirect warnings to the logger.

    ```python
    import logging
    logging.captureWarnings(True)
    ```

### Running tests

In Plone, test deprecation warnings are not shown by default.
The {file}`zope.conf` setting is not taken into account.

To enable deprecation warnings, use the `-W` command.

Given you're using a modern buildout with a virtual environment as recommended, the command would be the following.

```shell
./bin/python -W module ./bin/test
```


## Deprecation best practices

It's recommended to follow these best practices when deprecating code.


### Vanilla deprecation messages

Python offers a built-in exception {exc}`DeprecationWarning` which can be issued using the standard library's {mod}`warnings` module.

Its basic usage is the following example.

```python
import warnings
warnings.warn("deprecated", DeprecationWarning)
```


### Move an entire module

Given a package {file}`old.pkg` with a module {file}`foo.py`, to move it to a package {file}`new.pkg` as {file}`bar.py`, go through the following steps.

[`zope.deprecation` Moving modules](https://zopedeprecation.readthedocs.io/en/latest/api.html#moving-modules) offers a helper.

1.  Move the {file}`foo.py` as {file}`bar.py` to the {file}`new.pkg`.
1.  At the old place, create a new {file}`foo.py`, and add to it the following lines of code.

    ```python
    from zope.deprecation import moved
    moved("new.pkg.bar", "Version 2.0")
    ```

1.  Now you can still import the module at the old place, but get a deprecation warning.

    ```console
    DeprecationWarning: old.pkg.foo has moved to new.pkg.bar.
    Import of old.pkg.foo will become unsupported in Version 2.0
    ```


### Move an entire package

To move an entire package, the process is exactly the same as moving a module, but instead, create a file for each module in the package.


### Deprecate methods and properties

Use the `@deprecate` decorator from [`zope.deprecation` Deprecating methods and properties](https://zopedeprecation.readthedocs.io/en/latest/api.html#deprecating-methods-and-properties) to deprecate methods in a module.

```python
from zope.deprecation import deprecate

@deprecate("Old method is no longer supported, use new_method instead.")
def old_method():
    return "some value"
```

The `@deprecated` wrapper method deprecates properties.

```python
from zope.deprecation import deprecated

foo = None
foo = deprecated(foo, "foo is no more, use bar instead")
```


### Move functions and classes

This example describes how to move some classes or functions from a Python file at {file}`old/foo/bar.py` to {file}`new/baz/baaz.py`.
Here, `zope.deferredimport` offers a deprecation helper.
It also avoids circular imports at initialization time.

```python
import zope.deferredimport
zope.deferredimport.initialize()

zope.deferredimport.deprecated(
    "Import from new.baz.baaz instead",
    SomeOldClass="new.baz:baaz.SomeMovedClass",
    some_old_function="new.baz:baaz.some_moved_function",
)

def some_function_which_is_not_touched_at_all():
    pass
```

### Deprecate a GenericSetup profile

In GenericSetup, the `post_handler` attribute in ZCML can be used to call a function after the profile was applied.
Use this feature to issue a warning.

First, register the same profile twice, under both the new name and old.

```xml
<genericsetup:registerProfile
    name="default"
    title="My Fancy Package"
    directory="profiles/default"
    description="..."
    provides="Products.GenericSetup.interfaces.EXTENSION"
    />

<genericsetup:registerProfile
    name="some_confusing_name"
    title="My Fancy Package (deprecated)"
    directory="profiles/some_confusing_name"
    description="... (use profile default instead)"
    provides="Products.GenericSetup.interfaces.EXTENSION"
    post_handler=".setuphandlers.deprecate_profile_some_confusing_name"
    />
```

Then in {file}`setuphandlers.py`, add a function.

```python
import warnings

def deprecate_profile_some_confusing_name(tool):
    warnings.warn(
        'The profile with id "some_confusing_name" was renamed to "default".',
        DeprecationWarning
    )
```

### Deprecate a template location

Sometimes you need to move templates to new locations.
Since add-ons often use [`z3c.jbot`](https://github.com/zopefoundation/z3c.jbot) to override templates by their location, you'll need to point them to the new location as well as make sure that the override still works with the old location.

To deprecate a template, follow these steps.

1.  In the old package folder's {file}`__init__.py`, add a dictionary `jbot_deprecations` that maps the old template locations to their new counterparts.

    ```python
    jbot_deprecations = {
        "plone.locking.browser.info.pt": "plone.app.layout.viewlets.info.pt"
    }
    ```

1.  Add this deprecation snippet to the package {file}`configure.zcml` file.

    ```{code-block} xml
    :emphasize-lines: 7-15
    :linenos:
    
    <configure
        xmlns="http://namespaces.zope.org/zope"
        xmlns:browser="http://namespaces.zope.org/browser"
        xmlns:zcml="http://namespaces.zope.org/zcml"
        >
    
      <include
          package="z3c.jbot"
          file="meta.zcml"
          zcml:condition="installed z3c.jbot"
          />
      <browser:jbotDeprecated
          zcml:condition="have jbot-deprecations"
          dictionary=".jbot_deprecations"
          />
    
    </configure>
    ```

If a `z3c.jbot` version that supports deprecation is found, trying to override the template with the old location will trigger a deprecation warning that will instruct the user to rename its override file.
