Annotations 
=============

**Using the zope.annotation package**


Annotations are a convenient feature used throughout Zope and Plone.
They also serve as a useful real-world example of adapters.

The `zope.annotation`_ package defines an interface *IAnnotations*. By
adapting an object (often a content item) to this interface, you can get
and set values using a dict-like API. These values are then persisted
against the context object.

Remember that we often use adapters to model different aspects of an
object. A content object may have a basic schema - its content data
model - but there may be any number of adapters providing functionality
which in turn may need to persist other information. The annotations API
provides a simple and consistent storage abstraction for such
information.

The basic syntax for using an annotation is:

::

    >>> from zope.annotation.interfaces import IAnnotations
    >>> annotations = IAnnotations(context)
    >>> annotations['my.package.key'] = 1234

Notes:

-  Since annotations can be used by any number of packages, we tend to
   use dotted names as keys, to reduce the risk of colissions when two
   packages are writing annotations onto the same object.
-  The values stored in annotation must be persitable. Primitives are
   fine, as are objects deriving from *persistence.Persistent*.
-  The *IAnnotations*interface promises all the usual methods of a
   Python dictionary. For example, you can use *setdefault()* to set a
   default value if you are not sure that it has been created yet.

But where are annotations stored? As users of the *IAnnotations*
interface we don’t care: that logic is implemented by the *IAnnotations*
adapter. We could implement our own such adapter, but we normally don’t:
the *zope.annotation* package comes with an adapter providing
*IAnnotations* and adapting a marker interface *IAttributeAnnotations*.
This stores the values in an efficient, persistent *BTree* structure.
(That BTree happens to be stored as an attribute of the content object
called *\_\_annotations\_\_*, although we don’t ever access that
directly.)

Most content objects and the request object in Zope and Plone provide
this marker interface, making them “annotatable”. If you are working on
a simpler object, you can declare support for
*IAttributeAnnotations* with a directive like:

::

    from persistence import Persistent
    from five import grok
    from zope.annotation.interfaces import IAttributeAnnotations

    class SomeType(Persistent):
        grok.implements(IAttributeAnnotations)

        ...

Let’s now show a more complete example of using annotations. Recall the
following interface, which we used to implement a multi-adapter in the
previous section:

::

    class IMessageBroadcaster(Interface):
        """Multi-adapt a context and a blogging service to this interface
        """

        def send():
            """Send the context as a message using the given service
            """

Let’s say that we wanted to count the number of messages sent against
each each content object. Here is an implementation of the multi-adapter
that uses annotations to do that:

::

    from five import grok
    from zope.annotation.interfaces import IAnnotations

    class BloggingBroadcaster(grok.MultiAdapter):
        grok.provides(IMessageBroadcaster)
        grok.adapts(IContent, IBloggingService)
        
        COUNTER_KEY = 'example.messaging.counter'
        
        def __init__(self, context, service):
            self.context = context
            self.service = service
        
        def send(self):
            message = IMessage(self.context)
            text = message.format()
            
            annotations = IAnnotations(self.context, None)
            if annotations is not None:
                messageCount = annotations.get(COUNTER_KEY, 0)
                messageCount += 1
                annotations[COUNTER_KEY] = messageCount
                print "This is message number", messageCount
            
            print text

This code is defensive in that we gracefully handle the case where the
context is not annotatable. When it is, we get the current counter (if
set), increment it, and then save it back again, before printing the
value.

.. _zope.annotation: http://pypi.python.org/pypi/zope.annotation
