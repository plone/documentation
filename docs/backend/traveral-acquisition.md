---
myst:
  html_meta:
    "description": ""
    "property=og:description": ""
    "property=og:title": ""
    "keywords": ""
---

(traversal-and-acquisition-label)=

# Traversal and Acquisition

# Traversal

In Zope and Plone, traversal is the process of determining the object that is the target of a request by examining the URL path of the request or in code and looking up objects in the object hierarchy.
The object hierarchy in Zope is made up of "containers" and "item" objects.
Containers can contain other objects, while item objects cannot.
This is to some degree like the tree structure of a filesystem with folders, subfolders, and files.

When a request is made to the server, it examines the URL path of the request and starts at the root of the object hierarchy.
It then looks up each element of the URL path, starting with the first element in the current container, and if it finds an object with a matching name, it sets that object as the current container and continues to the next element of the URL path.
This process continues until the final element of the URL path is reached, at which point the server has determined the target object of the request.
If not explicitly given, at the end a default view is looked up.
This can be a registered page template or a callable view class.

(details see chapter about views)

In code, traversal can be achieved by using the `restrictedTraverse` and `unrestrictedTraverse` methods of content objects.
While request traversal always includes security checks, these checks can be bypassed when using these methods in code.
This means that when using `unrestrictedTraverse`, the developer has more control over the traversal process and can access objects without the normal security restrictions.
Anyway, security restrictions have to be implemented by the developer accordingly.


# Acquisition

In Zope, "acquisition" is a mechanism that allows objects to inherit attributes from their parent objects in the object hierarchy.
This enables objects to "acquire" attributes from their parent objects, rather than having to define all attributes themselves.

For example, if object A contains object B, and object A has an attribute "x", then object B can access the attribute x via acquisition, without having to define the attribute itself.

## Influences on traversal

This concept influences traversal in Zope because it allows objects to be accessed on traversal by acquisition in the object hierarchy, rather than having to know the exact location of an object.
For example, if an object "C" is located at the path "/A/B/C", it can also be accessed by traversing the hierarchy starting from object E in the path "/A/B/D/E" with "E.C", because it is acquiring attributes of objects D, B and A along the way.
This makes it at the same time easier and more confusing to find and access objects in a large, complex object hierarchy.


## Explicit vs Implicit Acquisition

In Zope, acquisition can be either explicit or implicit.

Explicit acquisition refers to the ability of an object to specifically request attributes from its parent object.
This is done by using the "Acquire" or "aq_acquire" method to acquire a specific attribute from a parent object.
For example, if object A contains object B, and object A has an attribute "x", object B can explicitly acquire attribute x by calling `B.aq_acquire("x")`.

Implicit acquisition refers to the automatic inheritance of attributes from parent objects without the need for explicit requests.
This is the default behavior in Zope, where objects automatically inherit attributes from their parent objects if they don't have the property defined themselves.
For example, if object A contains object B, and object A has a property "x", object B can implicitly acquire property x by simply accessing the property x without calling the acquire method: `B.x`.

The attribute is always acquired from its nearest parent and if it does not exist there it looks at the next parent up the hierarchy.
If the root is reached and no such attribute was found an `AttributeError` is raised.

A common use of implicit acquisition in Plone is to access tools like the `portal_catalog` from deep within the object hierarchy.
This is done by calling methods on the tool, such as `context.portal_catalog.searchResults(**query)`, where `context` is a content object located deep within the hierarchy.
This works because the `portal_catalog` tool is a child object of the Plone portal root, and is automatically acquired by objects further down the hierarchy.
This allows developers to access the tool without having to know its exact location within the hierarchy.
However, getting tools this way is discouraged, as this includes extra processing overhead.

In general, implicit acquisition is more commonly used in Zope, as it allows for a more natural and less verbose way of working with objects and their attributes.
On the other hand, implicit acquisition needs to be blocked to be sure to not acquire attributes using the `aq_base` method.
For example, if object A contains object B, and object A has a property "x", and the question is whether an attribute x exists on object B or not, then `getattr(B.aq_base, 'x', _marker)` avoids acquisition from A.
