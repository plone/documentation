How to scale images using PiL in Page Templates
===============================================

A quick description of how to scale images from an image field using the
Python Image Library in your Page Templates using TAL.

PROBLEM:

I have a custom type with an ImageField.  I'm customizing a folder
listing of these types and I wanted a thumbnail of each image shown in
the folder listing.  This is very straightforward using PiL (Python
Imaging Library), if you know what to do.  I was also presented with the
problem of working with brains rather than the object itself.

ASSUMPTIONS:

-  You have PiL installed and working.
-  You know how to make a custom Archetype

OVERVIEW:

When you get the folder contents for a folder listing, brains objects
are returned and iterated over to produce the list.  This is of course,
much more efficient than waking up each object.  The problem being, you
cannot get to your Image field in a brain (that I know of).  The
following is a snippet from 'folder\_listing.pt' showing this.

::

    <tal:foldercontents define="contentFilter contentFilter|request/contentFilter|nothing;

                                contentsMethod python:test(here.portal_type=='Topic', here.queryCatalog, here.getFolderContents);

                                folderContents folderContents|python:contentsMethod(contentFilter);">



        <tal:entry tal:repeat="item folderContents">

        <tal:block tal:define="item_url item/getURL|item/absolute_url;">

As you can see, while iterating over 'item' you're accessing brains-y
things in a brains-y way, like 'item/getURL'.  But you'll notice that
you cannot do 'item/my\_image' because it's not in the brain.  What to
do?! you may wail.  Well, you could wake up the objects, get the image
field, and then call the image scaling on it in a pythonic way, but this
is a performance hit, puts python in your TAL, which you should avoid.

Instead you'll just be crafty.  You already have 'item\_url' and you
know the name of your image field (my-image) so put those together and
you'll get right at the image.  Try this in your browser:

http://full/url/to/your/object/my-image

and you should see your image! Translating this into TAL, you would go:

::

    <img src="#" tal:attributes="src string:${item_url}/my-image" />

Now to add the image scaling bit, and this is where I went wrong.  Much
of the Plone documentation about PiL assume you're working with an
ATImage object, but you're not.  You're working with an AT ImageField. 
An AT ImageField only defines ONE image scale size by default:

::

    sizes = {'thumb': (80,80)}

 whereas ATImage defines a bunch:

::

    sizes = {'large'   : (768, 768),

               'preview' : (400, 400),

               'mini'    : (200, 200),

               'thumb'   : (128, 128),

               'tile'    :  (64, 64),

               'icon'    :  (32, 32),

               'listing' :  (16, 16),

              },

To make matters worse, notice that the sizes defined for the same size
key are different.  Bad dog.  No cookie.  Anyhow, what this means is
that in order to access the size you want, you have to define it in your
schema in advance, like so:

::

        ImageField(

            name='my-image',

            widget=ImageWidget(

                label="My Image",

                description="An image!",

            ),

            storage=AttributeStorage(),

            sizes= {'large'   : (768, 768),

               'preview' : (400, 400),

               'mini'    : (200, 200),

               'thumb'   : (128, 128),

               'tile'    :  (64, 64),

               'icon'    :  (32, 32),

               'listing' :  (16, 16),

              },

        ),

Ok, so now that you have defined the sizes you want in your custom
type's schema, you're ready to use it in your Page Template.  Remember
the way we accessed it before?

::

    <img src="#" tal:attributes="src string:${item_url}/my-image" />

To access the sizes defined in your schema, just add the name to the end
of your image, preceded by an underscore.

::

    <img src="#" tal:attributes="src string:${item_url}/my-image_mini" />

It's that easy, and it should be.  You shouldn't have to access and
therefore wake up your objects!  There are also other ways to get at
PiL's image scaling, but this I found was easiest and didn't throw any
bizarro "Unauthorized" or "TypeError: a float is required" errors.

Enjoy!
~Spanky

ALSO SEE:

`http://plone.org/documentation/manual/archetypes-developer-manual/fields/fields-reference <http://plone.org/kb/manual/archetypes-developer-manual/fields/fields-reference>`_\ `http://plone.org/documentation/tutorial/richdocument/pil <http://plone.org/kb/tutorial/richdocument/pil>`_
