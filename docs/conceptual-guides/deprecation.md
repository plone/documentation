---
myst:
  html_meta:
    "description": "Understanding deprecation in Plone - rationale, philosophy, and use cases"
    "property=og:description": "Understanding deprecation in Plone - rationale, philosophy, and use cases"
    "property=og:title": "Deprecation"
    "keywords": "deprecation, Plone, Python, Node.js, React, philosophy, rationale, use cases"
---

(conceptual-deprecation-label)=

# Deprecation

This chapter describes the rationale and philosophy of deprecations in Plone.
It is meant as a guide for how to think about deprecations in Plone core packages.

```{seealso}
For implementation details and code examples, see {doc}`/developer-guide/deprecation`.
```


(why-deprecation-label)=

## Why deprecation

Developers may need to get rid of old code, unify to a consistent API style, fix typos in names, move code or templates around, resolve technical debt, address security issues, or adapt to changes in external dependencies.

When refactoring code, it's often necessary to move modules, functions, classes, and methods.
It's critical not to break third party code imports from the old place.
It's also important that usage of old functions or methods must work for a while to allow developers to migrate or update their code.

Deprecated methods are usually removed with the next major release of Plone.
Plone follows the [semantic versioning guideline](https://semver.org).


## Help programmers without annoyance

Developers should use code deprecations to support the consumers of the code, that is, their fellow Plone developers.
From the consumer's point of view, Plone core code is an API.
Any change may annoy them, but they feel better when deprecation warnings tell them how to adapt their code to the changes.

Deprecations must always log at the level of warning.

Deprecations should always answer the following questions.

-   Why is the code gone from the old place?
-   What should the developer do instead?

A short message is enough, such as the following examples.

-   "Replaced by new API `xyz`, found at `abc.cde`".
-   "Moved to `xyz`, because of `abc`".
-   "Name had a typo, new name is `xyz`".

All logging must be done only once, in other words, on the first usage or import.
It must not flood the logs.


## Use cases

The following use cases describe when to deprecate.

Rename
:   Developers may want to rename classes, methods, functions, or global or class variables to get a more consistent API or because of a typo.
    Renaming alone is not enough to deprecate code.
    Always provide a deprecated version that logs a verbose deprecation warning with information for where to import from in the future.

Move objects
:   For reasons described in {ref}`why-deprecation-label`, developers may need to move code around.
    When imported from the old place, it logs a verbose deprecation warning with information of where to import from in the future.

Deprecation of a whole Python or npm package
:   A whole {ref}`Python package <python:tut-packages>` or [npm package](https://www.npmjs.com/) may be moved to a new location.

    -   All imports still work.
    -   Log deprecation warnings on first import.
    -   The ZCML still exists, but is empty or includes the ZCML from the new place, if there's no auto import for `meta.zcml`.

Deprecation of a whole released or installable package
:   Plone developers provide a major release with no "real" code, but only backward compatible imports of the public API.
    This should be done the way described above for a whole package.
    The README should clearly state why it was moved and where to find the code now.

Deprecation of a GenericSetup profile
:   These may have been renamed for consistency or are superfluous after an update.
    Code does not need to break to support this.
