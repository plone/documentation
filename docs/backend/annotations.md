---
myst:
  html_meta:
    "description": "How to use annotations to store arbitrary values on Python objects in Plone"
    "property=og:description": "How to use annotations to store arbitrary values on Python objects in Plone"
    "property=og:title": "Annotations"
    "keywords": "Plone, annotations, zope.annotation, storage, caching"
---

(backend-annotations-label)=

# Annotations

Annotations provide a conflict-free way to attach arbitrary attributes to Python objects in Plone.
They are used for storage and caching purposes throughout the system.


## Introduction

The annotation pattern allows you to store additional data on objects without modifying their class definitions.
This is particularly useful when you need to extend existing content types with custom data or settings.

Plone uses annotations for:

- Storing behavior data from `plone.behavior` package
- Caching values on HTTP request objects (`plone.memoize` cache decorators)
- Storing settings information on the portal or content objects (various add-on products)
- Assigned portlets and their settings

The [`zope.annotation`](https://pypi.org/project/zope.annotation/) package provides the core implementation.


## HTTP request example

Store cached values on an HTTP request during the lifecycle of a single request.
This allows you to cache computed values when the same computation function might be called from different, unrelated code paths.

```python
from zope.annotation.interfaces import IAnnotations

# Use a non-conflicting key based on your package name
KEY = "mypackage.something"

annotations = IAnnotations(request)

value = annotations.get(KEY, None)
if value is None:
    # Compute value and store it on request object for further look-ups
    value = annotations[KEY] = something()
```

You can also use the global request from `zope.globalrequest`:

```python
from zope.annotation.interfaces import IAnnotations
from zope.globalrequest import getRequest


def get_cached_data():
    """Get data, using request annotation as cache."""
    request = getRequest()
    KEY = "mypackage.cached_data"
    
    annotations = IAnnotations(request)
    data = annotations.get(KEY, None)
    if data is None:
        data = annotations[KEY] = expensive_computation()
    return data
```


## Content annotations

### Overview and basic usage

Annotations are the recommended way to extend Plone content with custom settings.

- Your add-on can store its settings on the Plone site root object using local utilities or annotations.
- You can store custom settings on individual content objects using annotations.

By default, annotations store:

- Behavior data from `plone.behavior` package
- Assigned portlets and their settings

Example of storing a simple value:

```python
from zope.annotation.interfaces import IAnnotations

# Assume context variable refers to some content item

# Use a non-conflicting key based on your company and package name
KEY = "yourcompany.packagename.magicalcontentnavigationsetting"

annotations = IAnnotations(context)

# Store a setting on the content item
annotations[KEY] = True

# Retrieve the setting
value = annotations.get(KEY, False)
```


### Advanced content annotation

The above example works for storing simple values.
For more complex data, you can create custom annotation classes.
This example shows how to add a simple "Like / Dislike" counter to a content object.

```python
class LikeDislike:
    """Track likes and dislikes for a content item."""
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        self._likes = set()
        self._dislikes = set()
    
    def liked_by(self, user_id):
        """Record that a user liked this item."""
        self._dislikes.discard(user_id)
        self._likes.add(user_id)
    
    def disliked_by(self, user_id):
        """Record that a user disliked this item."""
        self._likes.discard(user_id)
        self._dislikes.add(user_id)
    
    def status(self):
        """Return the count of likes and dislikes."""
        return len(self._likes), len(self._dislikes)
```

```{important}
Ensure your custom annotation class can be [pickled](https://docs.python.org/3/library/pickle.html#what-can-be-pickled-and-unpickled).
In Zope, this means you cannot hold references to content objects directly in your annotation.
Use the UID of a content object if you need to keep a reference.
```

The recommended pattern to get (and create if not existing) your annotation:

```python
from zope.annotation.interfaces import IAnnotations
from zope.annotation.interfaces import IAttributeAnnotatable

KEY = "content.like.dislike"  # Best practice: define in a config module


def get_likes_dislikes_for(item):
    """Factory for LikeDislike as annotation of content.
    
    Args:
        item: Any annotatable object (any Plone content)
        
    Returns:
        LikeDislike instance for this item
    """
    # Ensure the item is annotatable
    if not IAttributeAnnotatable.providedBy(item):
        raise TypeError("Item must be annotatable")
    
    annotations = IAnnotations(item)
    return annotations.setdefault(KEY, LikeDislike())
```

This pattern ensures that:

- You won't create annotations on objects that can't support them.
- A new annotation is created for your context object if it doesn't already exist.
- You can work with your `LikeDislike` annotation object like any Python object.
  All attribute changes will be stored automatically in the annotations.


### Wrapping your annotation with an adapter

The `zope.annotation` package provides a `factory()` function that transforms an annotation class into an adapter.
Annotations created this way have location awareness, with `__parent__` and `__name__` attributes.

Here's the improved example using `zope.annotation.factory()`:

```python
from zope.annotation import factory
from zope.annotation.interfaces import IAnnotations
from zope.component import adapter
from zope.interface import Interface
from zope.interface import implementer

KEY = "content.like.dislike"


class ILikeDislike(Interface):
    """Interface for like/dislike annotation."""
    
    def reset():
        """Reinitialize counters."""
    
    def liked_by(user_id):
        """Record that a user liked this item."""
    
    def disliked_by(user_id):
        """Record that a user disliked this item."""
    
    def status():
        """Return tuple of (likes_count, dislikes_count)."""


@implementer(ILikeDislike)
@adapter(Interface)  # Adapts any content; use a specific interface for targeted behavior
class LikeDislike:
    """Track likes and dislikes for content items."""
    
    def __init__(self):
        # Unlike regular adapters, the constructor takes no arguments.
        # Access the annotated object through self.__parent__
        self.reset()
    
    def reset(self):
        self._likes = set()
        self._dislikes = set()
    
    def liked_by(self, user_id):
        self._dislikes.discard(user_id)
        self._likes.add(user_id)
    
    def disliked_by(self, user_id):
        self._likes.discard(user_id)
        self._dislikes.add(user_id)
    
    def status(self):
        return len(self._likes), len(self._dislikes)


# Create the adapter factory
LikeDislikeFactory = factory(LikeDislike, key=KEY)
```

Register the adapter in ZCML:

```xml
<adapter factory=".likedislike.LikeDislikeFactory" />
```

Or register programmatically:

```python
from zope.component import provideAdapter

provideAdapter(LikeDislikeFactory)
```

Usage:

```python
# Get a content item
item = portal["my-document"]

# Get its annotation via the adapter
like_dislike = ILikeDislike(item)

# Use the annotation
like_dislike.liked_by("joe")
like_dislike.disliked_by("jane")

assert like_dislike.status() == (1, 1)
assert like_dislike.__parent__ is item
assert like_dislike.__name__ == KEY
```

```{tip}
Read the full documentation in the `README.txt` file in the `zope.annotation` package for more advanced usages.
```


### Using annotations in behaviors

The most common use of annotations in Plone 6 is through behaviors.
The `plone.behavior` package uses `AnnotationStorage` to store behavior data.

Example behavior using annotation storage:

```python
from plone.autoform.interfaces import IFormFieldProvider
from plone.behavior import AnnotationStorage
from plone.supermodel import model
from zope import schema
from zope.interface import provider


@provider(IFormFieldProvider)
class IReviewers(model.Schema):
    """Behavior to assign reviewers to content."""
    
    official_reviewers = schema.List(
        title="Official Reviewers",
        description="Users who are official reviewers",
        value_type=schema.TextLine(),
        required=False,
    )
    
    unofficial_reviewers = schema.List(
        title="Unofficial Reviewers", 
        description="Users who are unofficial reviewers",
        value_type=schema.TextLine(),
        required=False,
    )
```

Register the behavior in ZCML with annotation storage:

```xml
<plone:behavior
    title="Reviewers"
    description="The ability to assign reviewers to an item."
    provides=".behaviors.IReviewers"
    factory="plone.behavior.AnnotationStorage"
    marker=".behaviors.IReviewersMarker"
    />
```

The `AnnotationStorage` factory automatically stores field values in annotations, using the behavior interface's identifier as the annotation key.


### Cleaning up content annotations

```{warning}
If you store Python objects in annotations, you need to clean them up during add-on uninstallation.
Otherwise, if the Python code is removed, you can no longer import or export the Plone site.
Annotations are pickled objects in the database, and pickles don't work if the code is not present.
```

Here's how to clean up annotations on content objects:

```python
from io import StringIO
from zope.annotation.interfaces import IAnnotations
from plone.dexterity.interfaces import IDexterityContainer


def clean_up_content_annotations(portal, names):
    """Remove annotation entries from content objects in a Plone site.
    
    This is useful for removing objects that might make the site
    un-exportable when add-on code has been removed.
    
    Args:
        portal: Plone site object
        names: List of annotation key names to remove
        
    Returns:
        StringIO with log output
    """
    output = StringIO()
    
    def recurse(context):
        """Recurse through all content on the Plone site."""
        annotations = IAnnotations(context)
        
        for name in names:
            if name in annotations:
                print(
                    f"Cleaning up annotation {name} on item {context.absolute_url()}",
                    file=output
                )
                del annotations[name]
        
        # Only recurse into actual folders
        if IDexterityContainer.providedBy(context):
            for item_id, item in context.contentItems():
                recurse(item)
    
    recurse(portal)
    return output
```

You can call this from an uninstall profile or upgrade step:

```python
def uninstall(context):
    """Uninstall handler."""
    portal = context.getSite()
    clean_up_content_annotations(
        portal,
        ["mypackage.annotation.key1", "mypackage.annotation.key2"]
    )
```


### Make your code persistence-free

There's an issue with custom annotation classes: they create new persistent classes, so your data requires your source code.
This makes your code hard to uninstall, requiring both backward compatibility code and database cleanup.

An alternative pattern is to use existing persistent base classes instead of creating your own:

- `BTrees` (for large data sets)
- `persistent.list.PersistentList`
- `persistent.mapping.PersistentMapping`

Example using `PersistentMapping`:

```python
from persistent.mapping import PersistentMapping
from zope.annotation.interfaces import IAnnotations

KEY = "mypackage.likes"


def get_likes_for(item):
    """Get likes data using PersistentMapping.
    
    This approach doesn't require custom persistent classes.
    """
    annotations = IAnnotations(item)
    
    if KEY not in annotations:
        annotations[KEY] = PersistentMapping({
            "likes": set(),
            "dislikes": set(),
        })
    
    return annotations[KEY]


def like_item(item, user_id):
    """Record a like from a user."""
    data = get_likes_for(item)
    data["dislikes"].discard(user_id)
    data["likes"].add(user_id)


def dislike_item(item, user_id):
    """Record a dislike from a user."""
    data = get_likes_for(item)
    data["likes"].discard(user_id)
    data["dislikes"].add(user_id)


def get_status(item):
    """Get the like/dislike counts."""
    data = get_likes_for(item)
    return len(data["likes"]), len(data["dislikes"])
```

This pattern is used by add-ons such as `cioppino.twothumbs` and `collective.favoriting`.


## Related content

- [`zope.annotation` on PyPI](https://pypi.org/project/zope.annotation/)
- {doc}`behaviors`
- {doc}`content-types/index`
