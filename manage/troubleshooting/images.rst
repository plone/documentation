=======================
 Image troubleshooting
=======================

.. admonition:: Description

        Problems with imaging libraries, image loading and image scaling.

.. contents:: :local:

How to test see if your Python Imaging set-up works
======================================================

Example how to check if Python, Python Imaging Library (PIL) and
libjpeg are correctly working together.

Get a sample image::

    wget http://upload.wikimedia.org/wikipedia/commons/b/bb/JohnCarrollGilbertStuart.jpg

Start Python with Zope libraries in PYTHONPATH or Plone debug shell (latter)::

     bin/zopepy 

     # bin/instance debug  # <--- needs Plone site stopped first

Run the following on the interactive Python prompt started above::

    
    import PIL
    from PIL import Image
    im = Image.open("JohnCarrollGilbertStuart.jpg")  # Open downloaded image
    im.thumbnail((64, 64), Image.ANTIALIAS)  # See that PIL resize works
    im.save("test.jpg")  # See that PIL JPEG writing works

No Python exceptions should be risen.


Images are not loading
=======================

Plone is not loading images or resized images are not available
is usually caused by broken PIL installation: PIL used by Python virtual machine driving
Plone does not have proper native libraries (libjpeg) available to perform imaging operations.

If you run Zope on foreground you usually see errors like this::

    2009-10-22T17:31:04 ERROR Archetypes None
    Traceback (most recent call last):
      File "/home/xxx/xxx/parts/plone/Archetypes/Field.py", line 2333, in createScales
        imgdata, format = self.scale(data, w, h)
      File "/home/xxx/xxx/parts/plone/Archetypes/Field.py", line 2382, in scale
        image.thumbnail(size, self.pil_resize_algo)
      File "/usr/lib/python2.5/site-packages/PIL/Image.py", line 1523, in thumbnail
        self.load()
      File "/usr/lib/python2.5/site-packages/PIL/ImageFile.py", line 155, in load
        self.load_prepare()
      File "/usr/lib/python2.5/site-packages/PIL/ImageFile.py", line 223, in load_prepare
        self.im = Image.core.new(self.mode, self.size)
      File "/usr/lib/python2.5/site-packages/PIL/Image.py", line 36, in __getattr__
        raise ImportError("The _imaging C module is not installed")
    ImportError: The _imaging C module is not installed


In the above case PYTHONPATH incorrectly tries to load Python 2.5 libraries,
though Plone 3.x exclusively uses Python 2.4. In this case the proper fix
is to clean-up damaged start up scripts in bin/ folder::

    xxx@xxx:~/xxx/bin$ grep -Ri "python2.5" *
    buildout:  '/usr/lib/python2.5/site-packages',
    instance:  '/usr/lib/python2.5/site-packages',
    zopepy:  '/usr/lib/python2.5/site-packages',

This can be achieved by

* Removed all py2.5 eggs under eggs/ folder

* Removing setuptools egg which may contain references to Python 2.5

* Running bootstrap.py using python2.4

* Rerunning buildout after this

For further debugging the problem you can start the particular Python interpreter and try to import _imaging yourself.

Run Python in verbose mode to print all imports (the example below has been shortened)::

        (python-2.4)moo@murskaamo:~/isleofback$ python -v
        Python 2.4.6 (#1, Jul 16 2010, 10:31:46) 
        [GCC 4.4.3] on linux2
        Type "help", "copyright", "credits" or "license" for more information.
        >>> import _imaging
        Traceback (most recent call last):
          File "<stdin>", line 1, in ?
        ImportError: libjpeg.so.8: cannot open shared object file: No such file or directory
        >>> exit
        
In this case we have a custom Python build based on `collective.buildout.python <http://blog.mfabrik.com/2010/07/16/easily-install-all-python-versions-under-linux-and-osx-using-collective-buildout-python/>`_ recipe.
It will compile us a custom libjpeg version and should not use OS libjpeg::

        (python-2.4)moo@murskaamo:~/code/python$ find . -iname libjpeg*
        ./python-2.4/lib/libjpeg.la
        ./python-2.4/lib/libjpeg.so.8
        ./python-2.4/lib/libjpeg.so
        ./python-2.4/lib/libjpeg.so.8.0.2
        ./python-2.4/lib/libjpeg.a

However, looks like this libjpeg does not end up in the OS LD_LIBRARY_PATH import list automatically.

For more information see

* http://permalink.gmane.org/gmane.comp.web.zope.plone.product-developers/4946         

IOError when scaling images on Plone 4
========================================

Example::
        
        Traceback (most recent call last):
          File "/srv/plone/xxx/plone-new/eggs/plone.app.imaging-1.0.4-py2.6.egg/plone/app/imaging/traverse.py", line 73, in createScale
            imgdata, format = field.scale(data, width, height)
          File "/srv/plone/xxx/plone-new/eggs/Products.Archetypes-1.6.6-py2.6.egg/Products/Archetypes/Field.py", line 2501, in scale
            image.save(thumbnail_file, format, quality=self.pil_quality)
          File "/srv/plone/python/python-2.6/lib/python2.6/site-packages/PIL-1.1.6-py2.6-linux-x86_64.egg/PIL/Image.py", line 1372, in save
            self.load()
          File "/srv/plone/python/python-2.6/lib/python2.6/site-packages/PIL-1.1.6-py2.6-linux-x86_64.egg/PIL/ImageFile.py", line 207, in load
            raise IOError(error + " when reading image file")
        IOError: decoding error when reading image file

This means that libjpeg setup is not working. See above to how to test your set-up.

Installing libraries on Ubuntu / Debian
==========================================

This applies if you are using system Python to run Plone.
Version may vary so ``apt-cache search`` and ``grep``
commands are your friends::

        sudo apt-get install libpng12-dev  libjpeg62-dev python-imaging
               
Forcing libjpeg path
======================

Try in buildout.cfg::

        [instance]
        ...
        environment-vars =
                LD_LIBRARY_PATH /srv/plone/python/python-2.6/lib
        

libjpeg.so.8: cannot open shared object file: No such file or directory
=========================================================================

On Ubuntu you'll get this error when you try::

   bin/zopepy
   import _imaging

Some tips

* http://stackoverflow.com/questions/5545580/pil-libjpeg-so-8-cannot-open-shared-object-file-no-such-file-or-directory



