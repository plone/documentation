==================
The ExtensionClass
==================

.. admonition:: Description

    What is ``ExtensionClass.Base`` used for?

.. contents :: :local:

What is an ``ExtensionClass``?
==============================

Before Python 2.2 and "new-style" classes, the ``ExtensionClass.ExtensionClass``
metaclass provided features now found in Python itself. Nowadays, it mainly
provides three features:

* Support for a class initialiser. Classes deriving from ``ExtensionClass.Base``
  can define a method ``__class_init__(self)``, which is called when the
  class is initialised (usually at module import time). Note that ``self``
  here is the class object, not an instance of the class.
* Ensuring that any class that has ``ExtensionClass`` as a ``__metaclass__``
  implicitly gets ``ExtensionClass.Base`` as a base class.
* Providing an ``inheritedAttribute`` method, which acts a lot like ``super()``
  and is hence superfluous except for in legacy code.

The base class ``ExtensionClass.Base`` provides the ``__of__`` protocol that is
used by acquisition. It is similar to the ``__get__`` hook used in Python
descriptors, except that ``__of__`` is called when an implementor is retrieved
from an instance as well as from a class. Here is an example:

.. code-block:: python

    >>> from ExtensionClass import Base
    >>> class Container(Base):
    ...     pass

    >>> class Item(Base):
    ...     def __init__(self):
    ...         self.visited = []
    ...     def __of__(self, parent):
    ...         self.visited.append(parent)
    ...         return self

    >>> container = Container()
    >>> item = Item()
    >>> item.visited
    []
    >>> container.item1 = item
    >>> item.visited
    []
    >>> container.item1
    <__main__.O object at 0x10cc0ddd0>
    >>> item.visited
    [<__main__.C object at 0x10cc0dc90>]

    >>> container.item1 # again
    <__main__.O object at 0x10cc0ddd0>
    >>> item.visited
    [<__main__.C object at 0x10cc0dc90>, <__main__.C object at 0x10cc0dc90>]

There is probably little reason to use ``ExtensionClass.Base`` in new code,
though when deriving from ``Acquisition.Implicit`` or ``Acquisition.Explicit``,
it will be included as a base class of those classes.

How does acquisition work?
==========================

Black magic.
