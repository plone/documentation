---
myst:
  html_meta:
    "description": "Reference for the Plone testing API: layers, fixtures, helpers, and sandboxing, from plone.app.testing and plone.testing."
    "property=og:description": "Reference for the Plone testing API: layers, fixtures, helpers, and sandboxing, from plone.app.testing and plone.testing."
    "property=og:title": "Testing API reference"
    "keywords": "Plone, testing, plone.app.testing, plone.testing, layers, fixtures, helpers"
---

(testing-api-reference)=

# Testing API reference

Technical reference for Plone's testing API, drawn from two packages:

- [plone.app.testing](https://github.com/plone/plone.app.testing): the Plone-specific layers and helpers.
- [plone.testing](https://github.com/plone/plone.testing): the underlying layer model and the Zope-level tools.

You import from whichever package a symbol lives in, but from a test author's point of view they are one toolkit, so this page is organized by task rather than by package.
Each symbol is documented at its canonical location; where one package re-exports a symbol from the other, that is noted.

To use these to write a `testing.py`, see {doc}`write-a-testing-layer`.
For the model behind them, see {doc}`how-testing-layers-work`.
Signatures are generated from the source, so they always match the installed version.

## The layer model

The base class and the composition helper come from `plone.testing`; the Plone-specific layers build on them.

```{autodoc2-object} plone.testing.layer.Layer
render_plugin = "myst"
```

```{autodoc2-object} plone.testing.layer.layered
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.helpers.PloneSandboxLayer
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.helpers.PloneWithPackageLayer
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.layers.IntegrationTesting
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.layers.FunctionalTesting
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.layers.PloneFixture
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.layers.PloneTestLifecycle
render_plugin = "myst"
```

## Pre-built layers and fixtures

Ready-made layer instances.
The `PLONE_*` layers give you a plain Plone site; the `plone.testing` fixtures are lower-level building blocks you add to a layer's bases.

| Layer / fixture | Package | Use |
| --- | --- | --- |
| `PLONE_FIXTURE` | plone.app.testing | A plain Plone site. The base you build your own fixture on, not used in tests directly. |
| `PLONE_INTEGRATION_TESTING` | plone.app.testing | A ready integration layer for a plain Plone site. |
| `PLONE_FUNCTIONAL_TESTING` | plone.app.testing | A ready functional layer for a plain Plone site. |
| `MOCK_MAILHOST_FIXTURE` | plone.app.testing | Replaces the mail host so tests can capture outgoing email. |
| `STARTUP` | plone.testing.zope | Starts Zope. The root of most layer stacks. |
| `WSGI_SERVER_FIXTURE` | plone.testing.zope | Runs a real WSGI server, for tests that make requests over a socket. Add it to a functional layer's bases. |
| `UNIT_TESTING` | plone.testing.zca | An isolated component registry for tests that need one without a full site. |
| `EMPTY_ZODB` | plone.testing.zodb | An empty database. |
| `LAYER_CLEANUP` | plone.testing.zca | Runs the `zope.testing` cleanup handlers on tear-down. |

```{note}
`PLONE_ZSERVER` and `PLONE_FTP_SERVER` exist for the legacy ZServer.
Plone 6 runs on WSGI; use `WSGI_SERVER_FIXTURE` for a real HTTP server instead.
```

## Browser and HTTP

For end-to-end tests that drive Plone as a browser would.
See {doc}`drive-the-test-browser` for the task-oriented guide.

### `Browser`

```python
from plone.testing.zope import Browser

browser = Browser(app)
```

A [zope.testbrowser](https://github.com/zopefoundation/zope.testbrowser) browser wired to the Zope application under test.
It speaks to Zope in-process, over a special channel rather than a real socket, so it needs a functional layer but not `WSGI_SERVER_FIXTURE`.
`app` is the Zope root, the `app` resource from the layer.
See the [zope.testbrowser documentation](https://github.com/zopefoundation/zope.testbrowser) for the full browser API.

### `zopeApp`

```{autodoc2-object} plone.testing.zope.zopeApp
render_plugin = "myst"
```

## Helpers

### Users and roles

These are the `plone.app.testing` helpers; they wrap the lower-level `plone.testing.zope` versions and are the ones you normally import.

```{autodoc2-object} plone.app.testing.helpers.login
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.helpers.logout
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.helpers.setRoles
render_plugin = "myst"
```

### Products and profiles

`applyProfile` and `quickInstallProduct` install Plone add-ons; `installProduct` and `uninstallProduct` register a Zope product at the Zope level, which you usually only need in a layer's `setUpZope`.

```{autodoc2-object} plone.app.testing.helpers.applyProfile
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.helpers.quickInstallProduct
render_plugin = "myst"
```

```{autodoc2-object} plone.testing.zope.installProduct
render_plugin = "myst"
```

```{autodoc2-object} plone.testing.zope.uninstallProduct
render_plugin = "myst"
```

### Working with the site

```{autodoc2-object} plone.app.testing.helpers.ploneSite
render_plugin = "myst"
```

## Sandboxing primitives

Set-up code uses these to keep global state from leaking between layers.
`PloneSandboxLayer` calls them for you, so you rarely need them directly.
For why the sandboxing exists, see {ref}`the component-registry sandbox <zca-sandbox>`.

The component registry (populated by ZCML):

```{autodoc2-object} plone.testing.zca.pushGlobalRegistry
render_plugin = "myst"
```

```{autodoc2-object} plone.testing.zca.popGlobalRegistry
render_plugin = "myst"
```

```{note}
`plone.app.testing` re-exports `pushGlobalRegistry` and `popGlobalRegistry`, so `from plone.app.testing import pushGlobalRegistry` also works.
```

The security checkers:

```{autodoc2-object} plone.testing.security.pushCheckers
render_plugin = "myst"
```

```{autodoc2-object} plone.testing.security.popCheckers
render_plugin = "myst"
```

The database:

```{autodoc2-object} plone.testing.zodb.stackDemoStorage
render_plugin = "myst"
```

### Cleanup

```{autodoc2-object} plone.app.testing.helpers.tearDownMultiPluginRegistration
render_plugin = "myst"
```

```{autodoc2-object} plone.app.testing.cleanup.cleanUpMultiPlugins
render_plugin = "myst"
```

## Constants

Well-known values, safe to depend on in tests and fixtures.
All come from `plone.app.testing`.

| Constant | Value | Meaning |
| --- | --- | --- |
| `TEST_USER_ID` | `'test_user_1_'` | The default test user's id. |
| `TEST_USER_NAME` | `'test-user'` | The default test user's login name. |
| `TEST_USER_PASSWORD` | `'correct horse battery staple'` | The default test user's password. |
| `TEST_USER_ROLES` | `['Member']` | The default test user's roles. |
| `SITE_OWNER_NAME` | `'admin'` | The site owner (Manager) login name. |
| `SITE_OWNER_PASSWORD` | `'secret'` | The site owner's password. |
| `PLONE_SITE_ID` | `'plone'` | The id of the test Plone site. |
| `PLONE_SITE_TITLE` | `'Plone site'` | The title of the test Plone site. |
| `DEFAULT_LANGUAGE` | `'en'` | The default language of the test site. |
| `ROBOT_TEST_LEVEL` | `5` | The test level at which Robot Framework tests are registered. |

```{seealso}
- {doc}`write-a-testing-layer` — how to use these to build your `testing.py`.
- {doc}`how-testing-layers-work` — the model beneath these classes.
```
