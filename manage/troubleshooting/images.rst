=======================
 Image troubleshooting
=======================

.. admonition:: Description

        Problems with imaging libraries, image loading and image scaling.


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

Plone is not loading images or resized images are not available is usually caused by broken PIL installation: PIL used by the Python version that Plone is using does not have proper native libraries (libjpeg etcetera) available to perform imaging operations.

Solution: install the required native libraries for your operating system.




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



