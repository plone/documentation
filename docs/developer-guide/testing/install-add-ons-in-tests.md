---
myst:
  html_meta:
    "description": "How to install add-ons and GenericSetup profiles in a Plone test, and verify the result."
    "property=og:description": "How to install add-ons and GenericSetup profiles in a Plone test, and verify the result."
    "property=og:title": "Install add-ons and profiles in a test"
    "keywords": "Plone, testing, applyProfile, quickInstallProduct, GenericSetup, add-on"
---

(install-add-ons-in-tests)=

# Install add-ons and profiles in a test

This guide shows you how to install a GenericSetup profile or an add-on inside a test, and how to check that the installation did what you expect.

It uses the helpers from {doc}`testing-api-reference`.
The examples assume a layer whose fixture already loaded your add-on's ZCML—see {doc}`write-a-testing-layer`.

If you use pytest, {doc}`pytest-plone </developer-guide/testing/pytest>` also offers an `installer` fixture and an `@pytest.mark.portal(profiles=[...])` marker that do the same thing with less boilerplate.

## Apply a profile

The preferred way to install an add-on's configuration is to apply its GenericSetup profile:

```python
from plone.app.testing import applyProfile

applyProfile(portal, "my.addon:default")
```

You would usually do this once in your layer's `setUpPloneSite`, so every test in the layer runs against the installed add-on.
Do it in an individual test only when you are testing the installation itself.

## Install through the add-ons control panel

To install exactly as a site administrator would, through the add-ons control panel:

```python
from plone.app.testing import quickInstallProduct

quickInstallProduct(portal, "my.addon")
```

To force a reinstall—uninstall, then install again:

```python
quickInstallProduct(portal, "my.addon", reinstall=True)
```

Both assume the add-on's ZCML has been loaded, which the layer set-up normally does.

## Verify the installation

When you write an add-on with an install profile, you usually want a test that the profile did its job.

Check the add-on is installed:

```python
from plone.base.utils import get_installer

installer = get_installer(portal)
assert installer.is_product_installed("my.addon")
```

Check a content type was registered (via `types.xml`):

```python
types_tool = portal.portal_types
assert types_tool.getTypeInfo("MyType") is not None
```

Check a catalog index was added (via `catalog.xml`):

```python
catalog = portal.portal_catalog
assert "my_index" in catalog.indexes()
```

Check a workflow was installed and assigned (via `workflows.xml`):

```python
workflow_tool = portal.portal_workflow
assert workflow_tool.getWorkflowById("my_workflow") is not None
assert dict(workflow_tool.listChainOverrides())["MyType"] == ("my_workflow",)
```

```{seealso}
- {doc}`testing-api-reference`—`applyProfile`, `quickInstallProduct`, and the rest.
- The uninstall side of this suite: pytest-plone's `uninstalled` fixture, in {doc}`pytest`.
```
