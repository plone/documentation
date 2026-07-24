---
myst:
  html_meta:
    "description": "How to drive Plone with zope.testbrowser in a functional test: open URLs, follow links, submit forms."
    "property=og:description": "How to drive Plone with zope.testbrowser in a functional test: open URLs, follow links, submit forms."
    "property=og:title": "Drive the test browser"
    "keywords": "Plone, testing, zope.testbrowser, functional test, browser"
---

(drive-the-test-browser)=

# Drive the test browser

This guide shows you how to write an end-to-end functional test that drives Plone through `zope.testbrowser`, which acts as a web browser connected to Zope in-process.

```{important}
`zope.testbrowser` runs entirely in Python and does **not** run JavaScript.
Use it for server-rendered pages (Classic UI). To test a Volto frontend, use the Volto documentation's end-to-end testing tools instead.
```

You need a **functional** layer, either `PLONE_FUNCTIONAL_TESTING` or your own layer built with `FunctionalTesting`.
The test browser cannot see an integration layer's uncommitted transaction; see {ref}`how-testing-layers-work` for why.

## Get a browser

```python
from plone.testing.zope import Browser

browser = Browser(app)
```

`app` is the Zope root (the `app` resource from the layer).

## Make content visible to the browser

The browser runs in a separate transaction, so it sees only **committed** data.
If a test creates content and then visits it, commit first:

```python
import transaction
from plone.app.testing import setRoles, TEST_USER_ID

setRoles(portal, TEST_USER_ID, ["Manager"])
portal.invokeFactory("Folder", "f1", title="Folder 1")
setRoles(portal, TEST_USER_ID, ["Member"])

transaction.commit()   # now the browser can see f1
```

## Open a page and inspect it

```python
browser.open(portal.absolute_url())

assert "Welcome" in browser.contents
assert browser.headers["content-type"] == "text/html; charset=utf-8"
```

## Follow links

```python
browser.getLink("Edit").click()          # by link text
browser.getLink(id="edit-link").click()  # by HTML id

assert browser.url == portal.absolute_url() + "/edit"
```

## Fill in and submit a form

```python
browser.getControl("Age").value = "30"        # by the control's label
browser.getControl(name="age:int").value = "30"  # by form variable name

browser.getControl("Save").click()             # submit by button label
```

See the [zope.testbrowser documentation](https://github.com/zopefoundation/zope.testbrowser) for selecting and manipulating every control type.

## Debugging

When a submission does not do what you expect, print the response to see what the browser actually got:

```python
print(browser.contents)
```

An unhandled exception on the server is re-raised in the test by default, so you get the real traceback rather than a rendered error page.

```{seealso}
- {ref}`how-testing-layers-work`—why functional layers commit and integration layers do not.
- pytest users testing the REST API rather than HTML: {doc}`pytest` and pytest-plone's request fixtures.
```
