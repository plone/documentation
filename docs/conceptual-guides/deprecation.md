---
myst:
  html_meta:
    "description": "Understanding deprecation in Plone - rationales, philosophy, and use cases."
    "property=og:description": "Understanding deprecation in Plone - rationales, philosophy, and use cases."
    "property=og:title": "Deprecation"
    "keywords": "deprecation, Plone, Python, philosophy"
---

(conceptual-deprecation-label)=

# Deprecation

This chapter describes rationales and philosophy of deprecations in Plone, Zope, and Python.
It is meant as a guide on how to think about deprecations in Plone core packages.

```{seealso}
For implementation details and code examples, see {doc}`/developer-guide/deprecation`.
```


## Why deprecation

At some point we:

- need to get rid of old code,
- want to unify API style (consistent API),
- fix typos in namings,
- move code or templates around (inside package or to another package).

While refactoring code, moving modules, functions, classes and methods is often needed.
To not break third party code imports from the old place or usage of old functions/ methods must work for while.
Deprecated methods are usually removed with the next major release of Plone.

Following the [semantic versioning guideline](https://semver.org) is recommended.


## Help programmers, no annoyance

The developers should use code deprecations to support the consumers of the code.
From their point of view, Plone core code is an API to them.
Any change is annoying to them anyway, but they feel better if deprecation warnings are telling them what to do.

Deprecations must always log at level *warning* and have to answers the question:

**"Why is the code gone from the old place? What to do instead?"**

A short message is enough., i.e.:

- "Replaced by new API xyz, found at abc.cde".,
- "Moved to xyz, because of abc.",
- "Name had a typo, new name is "xyz".

All logging has to be done once, i.e. on first usage or first import.
It must not flood the logs.


## Use cases

Renaming

: We may want to rename classes, methods, functions or global or class variables in order to get a more consistent API or because of a typo, etc.
  We never just rename, we always provide a deprecated version logging a verbose deprecation warning with information where to
  import from in future.

Moving a module, class, function, etc to another place

: For some reason, i.e. merging packages, consistent API or resolving cirular import problems, we need to move code around.
  When imported from the old place it logs a verbose deprecation warning with information where to import from in future.

Deprecation of a whole package

: A whole [package](https://docs.python.org/3/tutorial/modules.html#packages)

  - all imports still working, logging deprecation warnings on first import
  - ZCML still exists, but is empty (or includes the zcml from the new place if theres no auto import (i.e. for meta.zcml).

Deprecation of a whole released/ installable package.

: We will provide a last major release with no 'real' code, only backward compatible (bbb) imports of public API are provided.
  This will be done the way described above for a whole package.
  The README clearly states why it was moved and where to find the code now.

Deprecation of a GenericSetup profile

: They may got renamed for consistency or are superfluos after an update.
  Code does not need to break to support this.
