.. _annotations:

.. index:: ! annotation

============
 Annotations
============

.. admonition:: Description

   How to use annotation design pattern to store arbitrary values on Python
   objects (Plone site, HTTP request) for storage and caching purposes.


Introduction
============

Annotations is conflict-free way to stick attributes on arbitrary Python objects.

Plone uses annotations for:

* Storing field data in Archetypes (Annotation storage).

* Caching values on HTTP request object (plone.memoize cache decorators).

* Storing settings information in portal or content object (various add-on
  products).

See `zope.annotation package <https://pypi.python.org/pypi/zope.annotation/3.4.1>`_.

HTTP request example
====================

Store cached values on HTTP request during the life cycle of one request
processing.  This allows you to cache computed values if the computation
function is called from the different, unrelated, code paths.

.. code-block:: python

   from zope.annotation.interfaces import IAnnotations

   # Non-conflicting key
   KEY = "mypackage.something"

   annotations = IAnnotations(request)

   value = annotations.get(KEY, None)
   if value is None:
       # Compute value and store it on request object for further look-ups
       value = annotations[KEY] = something()

Content annotations
===================

Overview and basic usage
------------------------

If you want to extend any Plone content to contain "custom" settings annotations
is the recommended way to do it.

* Your add-on can store its settings in Plone site root object using local
  utilities or annotations.

* You can store custom settings on content objects using annotations.

By default, in content annotations are stored:

* Assigned portlets and their settings.

* Archetypes content type fields using ``AnnotationStorage`` (like ``text``
  field on Document).

* Behavior data from :mod:`plone.behavior` package.

Example:

.. code-block:: python

   # Assume context variable refers to some content item

   # Non-conflicting key
   KEY = "yourcompany.packagename.magicalcontentnavigationsetting"

   annotations = IAnnotations(context)

   # Store some setting on the content item
   annotations[KEY] = True

Advanced content annotation
---------------------------

The above example is enough for storing simple values as annotations. You may
provide more complex annotation objects depending on your application logic on
various content types. This example shows how to add a simple "Like / Dislike"
counter on a content object.

.. code-block:: python

   class LikeDislike(object):
       def __init__(self):
           self.reset()

       def reset(self):
           self._likes = set()
           self._dislikes = set()

       def likedBy(self, user_id):
           self._dislikes.discard(user_id)
           self._likes.add(user_id)

       def dislikedBy(self, user_id):
           self._likes.discard(user_id)
           self._dislikes.add(user_id)

       def status(self):
           return len(self._likes), len(self._dislikes)

At this step it is essential to check that your custom annotation class can be
`pickled
<http://docs.python.org/library/pickle.html#what-can-be-pickled-and-unpickled>`_. In
the Zope world, this means that you cannot hold in your annotation object any
reference to a content too.

.. tip::

   Use the UID of a content object if you need to keep the reference of that
   content object in an annotation.

The most pythonic recipe to get (and set if not existing) your annotation for a
given key is:

.. code-block:: python

   from zope.annotation import IAttributeAnnotatable, IAnnotations

   KEY = 'content.like.dislike'  # It's best place is config.py in a real app

   def getLikesDislikeFor(item):
       """Factory for LikeDislike as annotation of a contentish
       @param item: any annotatable object, thus any Plone content
       """
       # Ensure the item is annotatable
       assert IAttributeAnnotatable.providedBy(item)  # Won't work otherwise
       annotations = IAnnotations(item)
       return annotations.setdefault(KEY, LikeDislike())

This way, you're sure that :

* You won't create annotations on an object that can't support them.

* You will create a new fresh annotation mastered with your :class:`LikeDislike`
  for your context object if it does not already exist.

* You can play with your :class:`LikeDislike` annotation object as with any
  Python object, all attributes changes will be stored automatically in the
  annotations of the associated content object.

.. index:: adapter

Wrapping your annotation with an adapter
----------------------------------------

:mod:`zope.annotation` comes with the :func:`factory` function that transforms
the annotation class into an adapter (possibly named as the annotation key).

In addition the annotation created this way have location awareness, having
:attr:`__parent__` and :attr:`__name__` attributes.

Let's go back to the above sample and use the :func:`zope.annotation.factory`
function.

.. code-block:: python

   import zope.interface
   import zope.component
   import zope.annotation

   from zope.interface import implements
   from zope.annotation import factory

   from some.contenttype.interfaces import ISomeContent

   KEY = 'content.like.dislike'  # It's best place is config.py in a real app

   class ILikeDislike(zope.interface.Interface):
       """Model for like/dislike annotation
       """
       def reset():
           """Reinitialize everything
           """

       def likedBy(user_id):
           """User liked the associated content
           """

       def dislikedBy(user_id):
           """User disliked the associated content
           """


   class LikeDislike(object):
       implements(ILikeDislike)
       zope.component.adapts(ISomeContent)

       def __init__(self):
           # Does not expect argument as usual adapters
           # You can access annotated object through ``self.__parent__``
           self.reset()

       def reset(self):
           self._likes = set()
           self._dislikes = set()

       def likedBy(self, user_id):
           self._dislikes.discard(user_id)
           self._likes.add(user_id)

       def dislikedBy(self, user_id):
           self._likes.discard(user_id)
           self._dislikes.add(user_id)

       def status(self):
           return len(self._likes), len(self._dislikes)


   # Register as adapter (you may do this in ZCML too)
   zope.component.provideAdapter(factory(LikeDislike, key=KEY))

   # Lets play with some content
   item = getSomeContentImplementingISomeContent()  # Guess what :)

   # Let's have its annotation
   like_dislike = ILikeDislike(item)

   # Play with this annotation
   like_dislike.likedBy('joe')
   like_dislike.dislikedBy('jane')

   assert like_dislike.status() == (1, 1)
   assert like_dislike.__parent__ is item
   assert like_dislike.__name__ == KEY

.. tip::

   Read a full doc / test / demo of the :func:`zope.annotation.factory` in the
   :file:`README.txt` file in the root of :mod:`zope.annotation` package for
   more advanced usages.

Cleaning up content annotations
-------------------------------

.. warning ::

   If you store full Python objects in annotations you need to clean them up
   during your add-on uninstallation. Otherwise if Python code is not present
   you can no longer import or export Plone site (annotations are pickled
   objects in the database and pickles do no longer work if the code is not
   present).

How to clean up annotations on content objects:

.. code-block:: python

   def clean_up_content_annotations(portal, names):
       """
       Remove objects from content annotations in Plone site,

       This is mostly to remove objects which might make the site un-exportable
       when eggs / Python code has been removed.

       @param portal: Plone site object

       @param names: Names of the annotation entries to remove
       """

       output = StringIO()

       def recurse(context):
           """ Recurse through all content on Plone site """

           annotations = IAnnotations(context)

           #print  >> output, "Recusring to item:" + str(context)
           print annotations

           for name in names:
               if name in annotations:
                   print >> output, "Cleaning up annotation %s on item %s" % (name, context.absolute_url())
                   del annotations[name]

           # Make sure that we recurse to real folders only,
           # otherwise contentItems() might be acquired from higher level
           if IFolderish.providedBy(context):
               for id, item in context.contentItems():
                   recurse(item)

       recurse(portal)

       return output

Make your code persistence free
-------------------------------

There is one issue with the above methods: you are creating new persistent
classes so your data need your source code.
That makes your code hard to uninstall (have to keep the code BBB + cleaning
up the DB by walking throw all objects)

Another pattern to store data in annotations: Use already existing
persistent base code instead of creating your own.

Please use one of theses:

* BTrees
* PersistentList
* PersistentDict

This pattern is used by cioppino.twothumbs and collective.favoriting addons.

How to achieve this: https://gist.github.com/toutpt/7680498

Other resources
---------------

* https://plone.org/documentation/tutorial/embrace-and-extend-the-zope-3-way/annotations
